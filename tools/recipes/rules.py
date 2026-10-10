"""Shared recipe rules: used by validate.py (console) and report.py (HTML).

Inputs: recipes_table.json (the table), data.json (items, vanilla recipes), ingredient_catalog.json (effort 1-5).

Effort of a recipe: sum((ingredient effort - 1) * qty) over catalog ingredients (effort 1 = free, so a bundle of
common herbs counts nothing), plus effort_max = highest ingredient effort. Lower-level potions / bombs are not in the
catalog and count in cost only.

Each rule is registered in RULES as Rule(id, severity, fn); fn(ctx) returns a list of (recipe key, message).
Per-recipe rules are written as fn(key, recipe, ctx) -> [message] and wrapped by @per_recipe; rules that need the
whole table (collisions, signature, monotonic) read ctx.table. Messages are plain ASCII.
Severities: error (table is wrong, check.ps1 gates on it), warn (design smell to look at), info (shown only).
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
KIND_ORDER = {'potion': 0, 'bomb': 1, 'decoction': 2}
BOMB_BASES = ('Saltpetre', 'Stammelfords dust', 'Alchemists powder')
LOWER_LEVEL_CATEGORIES = ('potion', 'petard')  # an ingredient of this category is a lower-level consumable

# Highest allowed copy effort (sum((e-1)*qty)) per recipe level. Starting values, tuned on the data.
COPY_EFFORT_MAX = {1: 2, 2: 4, 3: 6}


def load_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


class Ctx:
    """Everything a rule may look at."""

    def __init__(self, table, data, catalog):
        self.table = table
        self.items = data['items']
        self.vanilla = data['recipes']
        self.catalog = catalog['ingredients']
        self.excluded = set(catalog['_meta']['excluded_lower_level_items'])
        self.keys = sort_keys(table)

    def is_alcohol(self, n):
        return 'StrongAlcohol' in self.items.get(n, {}).get('tags', [])

    def is_lower_level(self, n):
        return self.items.get(n, {}).get('category') in LOWER_LEVEL_CATEGORIES

    def stats(self, lst):
        """cost, effort (sum((e-1)*qty)), effort_max and ingredients missing from the catalog for one list."""
        cost, effort, emax, missing = 0, 0, 0, []
        for n, q in lst:
            if n in self.items:
                cost += int(self.items[n]['price']) * q
            if n in self.catalog:
                e = self.catalog[n]['effort']
                effort += (e - 1) * q
                emax = max(emax, e)
            elif n not in self.excluded:
                missing.append(n)
        return {'cost': cost, 'effort': effort, 'effort_max': emax}, missing


def sort_keys(table):
    return sorted(table, key=lambda k: (KIND_ORDER.get(table[k]['kind'], 9), table[k]['family'], table[k]['level'], k))


def load_context(table=None):
    """table: a dict (e.g. from git), or None for recipes_table.json."""
    if table is None:
        table = load_json(os.path.join(HERE, 'recipes_table.json'))
    return Ctx(table, load_json(os.path.join(HERE, 'data.json')), load_json(os.path.join(HERE, 'ingredient_catalog.json')))


def per_recipe(fn):
    def run(ctx):
        out = []
        for k in ctx.keys:
            out += [(k, m) for m in fn(k, ctx.table[k], ctx)]
        return out
    return run


def names(lst):
    return [n for n, _ in lst]


# --- errors: single recipe ---------------------------------------------------------------------------------------
@per_recipe
def unknown_ingredient(k, r, ctx):
    bad = sorted({n for n in names(r['full']) + names(r['copy']) if n not in ctx.items})
    return ['ingredient not in data.json items: ' + ', '.join(bad)] if bad else []


@per_recipe
def no_alcohol(k, r, ctx):
    if r['kind'] not in ('potion', 'decoction'):
        return []
    return ['%s has no alcohol (StrongAlcohol)' % lst for lst in ('full', 'copy')
            if not any(ctx.is_alcohol(n) for n in names(r[lst]))]


@per_recipe
def no_powder(k, r, ctx):
    if r['kind'] != 'bomb':
        return []
    return ['%s has no bomb powder (%s)' % (lst, ' / '.join(BOMB_BASES)) for lst in ('full', 'copy')
            if not any(n in BOMB_BASES for n in names(r[lst]))]


@per_recipe
def copy_lower_level(k, r, ctx):
    low = [n for n in names(r['copy']) if ctx.is_lower_level(n)]  # D28
    return ['copy contains a lower-level item: ' + ', '.join(low)] if low else []


@per_recipe
def copy_costs_more(k, r, ctx):
    f, c = ctx.stats(r['full'])[0], ctx.stats(r['copy'])[0]
    return ['copy costs more than full (%d > %d)' % (c['cost'], f['cost'])] if c['cost'] > f['cost'] else []


@per_recipe
def copy_effort_higher(k, r, ctx):
    f, c = ctx.stats(r['full'])[0], ctx.stats(r['copy'])[0]
    return ['copy effort %d > full effort %d' % (c['effort'], f['effort'])] if c['effort'] > f['effort'] else []


@per_recipe
def copy_effort_max_higher(k, r, ctx):
    f, c = ctx.stats(r['full'])[0], ctx.stats(r['copy'])[0]
    if c['effort_max'] > f['effort_max']:
        return ['copy max effort %d > full max effort %d' % (c['effort_max'], f['effort_max'])]
    return []


@per_recipe
def missing_from_catalog(k, r, ctx):
    miss = sorted(set(ctx.stats(r['full'])[1] + ctx.stats(r['copy'])[1]))
    return ['not in ingredient catalog: ' + ', '.join(miss)] if miss else []


# --- warnings: single recipe -------------------------------------------------------------------------------------
@per_recipe
def copy_effort_over_threshold(k, r, ctx):
    cap = COPY_EFFORT_MAX.get(r['level'])
    e = ctx.stats(r['copy'])[0]['effort']
    return ['copy effort %d above level %d threshold %d' % (e, r['level'], cap)] if cap is not None and e > cap else []


# --- warnings: whole table ---------------------------------------------------------------------------------------
_PAIR_LISTS = (('copy', 'copy'), ('full', 'full'), ('copy', 'full'), ('full', 'copy'))  # (list of A, list of B)


def _relation(a, b):
    """'identical' if the ingredient-name sets are equal; 'near' if they differ by exactly one ingredient: one set
    has one extra name (symmetric difference 1) or one name is swapped for another (same size, difference 2)."""
    if a == b:
        return 'identical'
    if (len(a - b), len(b - a)) in ((1, 0), (0, 1), (1, 1)):
        return 'near'
    return None


def _pairs(ctx):
    """Yield (key A, key B, {'identical': [text], 'near': [text]}) for every unordered pair of recipes with a relation.
    Lists compared: copy-copy, full-full, and copy of one against full of the other; a recipe's own copy against
    its own full is not compared. Texts are from A's point of view; B's view is built by swapping."""
    sets = {k: {l: frozenset(names(ctx.table[k][l])) for l in ('full', 'copy')} for k in ctx.keys}
    for i, ka in enumerate(ctx.keys):
        for kb in ctx.keys[i + 1:]:
            found = {'identical': [], 'near': []}
            for la, lb in _PAIR_LISTS:
                rel = _relation(sets[ka][la], sets[kb][lb])
                if rel:
                    found[rel].append((la, lb, sets[ka][la] - sets[kb][lb], sets[kb][lb] - sets[ka][la]))
            if found['identical'] or found['near']:
                yield ka, kb, found


def _pair_text(ctx, other, parts, near, flip):
    out = []
    for la, lb, only_a, only_b in parts:
        if flip:
            la, lb, only_a, only_b = lb, la, only_b, only_a
        t = '%s ~ %s %s' % (la, ctx.table[other]['item'], lb)
        if near:
            t += ' (' + ' '.join(['+' + n for n in sorted(only_b)] + ['-' + n for n in sorted(only_a)]) + ')'
        out.append(t)
    return '; '.join(out)


def _collisions(ctx, rel):
    out = []
    for ka, kb, found in _pairs(ctx):
        parts = found[rel]
        if not parts:
            continue
        same = ' (same family)' if (ctx.table[ka]['kind'], ctx.table[ka]['family']) == (ctx.table[kb]['kind'], ctx.table[kb]['family']) else ''
        near = rel == 'near'
        out.append((ka, ('differs by one ingredient: ' if near else 'identical ingredient set: ') + _pair_text(ctx, kb, parts, near, False) + same))
        out.append((kb, ('differs by one ingredient: ' if near else 'identical ingredient set: ') + _pair_text(ctx, ka, parts, near, True) + same))
    return out


def collision(ctx):
    """Two different recipes with the same set of ingredient names (quantities ignored), see _pairs."""
    return _collisions(ctx, 'identical')


def near_collision(ctx):
    """Two different recipes whose ingredient-name sets differ by exactly one ingredient, see _relation / _pairs.
    Reported once per pair (a message on each of the two recipes)."""
    return _collisions(ctx, 'near')


def no_signature(ctx):
    """The copy must have an ingredient that is in no copy of another family of the same kind. Alcohols and bomb
    powders are shared by design and do not count."""
    out = []
    for k in ctx.keys:
        r = ctx.table[k]
        others = {n for k2 in ctx.keys for n in names(ctx.table[k2]['copy'])
                  if (ctx.table[k2]['kind'], ctx.table[k2]['family']) != (r['kind'], r['family']) and ctx.table[k2]['kind'] == r['kind']}
        own = [n for n in names(r['copy']) if not ctx.is_alcohol(n) and n not in BOMB_BASES]
        if not [n for n in own if n not in others]:
            out.append((k, 'copy has no signature ingredient (none unique among other families of the same kind)'))
    return out


def effort_not_monotonic(ctx):
    """Within a family the copy effort must not drop from level n to level n+1."""
    fams = {}
    for k in ctx.keys:
        fams.setdefault((ctx.table[k]['kind'], ctx.table[k]['family']), []).append(k)
    out = []
    for ks in fams.values():
        ks = sorted(ks, key=lambda k: ctx.table[k]['level'])
        for a, b in zip(ks, ks[1:]):
            ea, eb = ctx.stats(ctx.table[a]['copy'])[0]['effort'], ctx.stats(ctx.table[b]['copy'])[0]['effort']
            if eb < ea:
                out.append((b, 'copy effort %d at level %d is lower than %d at level %d' % (
                    eb, ctx.table[b]['level'], ea, ctx.table[a]['level'])))
    return out


# --- info --------------------------------------------------------------------------------------------------------
@per_recipe
def full_differs_vanilla(k, r, ctx):
    van = ctx.vanilla.get(k, {}).get('ings', [])
    return ['table full differs from vanilla'] if {n: q for n, q in r['full']} != {n: q for n, q in van} else []


class Rule:
    def __init__(self, id, severity, fn):
        self.id, self.severity, self.fn = id, severity, fn


RULES = [
    Rule('unknown_ingredient', 'error', unknown_ingredient),
    Rule('no_alcohol', 'error', no_alcohol),
    Rule('no_powder', 'error', no_powder),
    Rule('copy_lower_level', 'error', copy_lower_level),
    Rule('copy_costs_more', 'error', copy_costs_more),
    Rule('copy_effort_higher', 'error', copy_effort_higher),
    Rule('copy_effort_max_higher', 'error', copy_effort_max_higher),
    Rule('missing_from_catalog', 'error', missing_from_catalog),
    # D30: uniqueness comes from the signature ingredient; a one-ingredient difference is only informative.
    # collision becomes an error once the polished table has none (it would block check.ps1 now).
    Rule('collision', 'warn', collision),
    Rule('near_collision', 'info', near_collision),
    Rule('no_signature', 'warn', no_signature),
    Rule('effort_not_monotonic', 'warn', effort_not_monotonic),
    Rule('copy_effort_over_threshold', 'warn', copy_effort_over_threshold),
    Rule('full_differs_vanilla', 'info', full_differs_vanilla),
]


def run(ctx):
    """{recipe key: [{'id', 'severity', 'text'}]} for every key of the table, in RULES order."""
    res = {k: [] for k in ctx.keys}
    for rule in RULES:
        for k, text in rule.fn(ctx):
            res[k].append({'id': rule.id, 'severity': rule.severity, 'text': text})
    return res
