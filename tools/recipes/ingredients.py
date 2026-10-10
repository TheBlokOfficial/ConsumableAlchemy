"""Ingredient catalog: every ingredient used by recipes_table.json with price, type, sources and an effort level 1-5.

Effort is computed only by the rules below (no per-ingredient overrides); the thresholds are echoed into _meta.
Output: ingredient_catalog.json (deterministic: sorted keys, indent=1, utf-8).
"""
import json, os, collections
import loot

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'ingredient_catalog.json')

# --- effort thresholds ---------------------------------------------------------------------------------------
SHOPS_LV1 = 10           # >= this many shops (herb: also needs a herb node) -> 1
SHOPS_LV2 = 5            # >= this many shops, or a herb node -> 2
MONSTER_COMMON_CHANCE = 35   # percent per kill (always = 100); at or above this a table is a "common" drop
MONSTER_COMMON_TABLES = 2    # common drop = this many tables with chance >= MONSTER_COMMON_CHANCE -> 3
MONSTER_LESS_CHANCE = 10     # any monster table with chance >= this (or always) -> 4, below it -> 5
RARE_TAG = 'mod_valuable'    # the game's own tag for rarer monster parts: caps a monster drop at 4
SHOP_ONLY_TYPES = ('mineral', 'alcohol', 'other')   # types for which level 1 needs shops alone
# shops of a single DLC region only (none in base game) -> 4
NO_SOURCE = 5

# type by icon folder (the game has no tag separating minerals from monster parts)
ICON_HERB, ICON_MONSTER, ICON_MINERAL = '/herb/', '/monstrous/', '/alchemy/'
ICON_ANIMAL_PART = '/alchemy/food_'

EFFORT_RULES = collections.OrderedDict([
    ('1', 'shops >= %d and (herb: also a herb node; mineral / alcohol / other: shops alone; monster parts and '
          'mutagens never)' % SHOPS_LV1),
    ('2', 'shops >= %d, or a herb node' % SHOPS_LV2),
    ('3', 'shops 1..%d, or a common monster drop: >= %d monster loot tables with chance >= %d%% (always counts as '
          '100%%), unless the item carries tag %s' % (SHOPS_LV2 - 1, MONSTER_COMMON_TABLES, MONSTER_COMMON_CHANCE,
                                                       RARE_TAG)),
    ('4', 'all shops in a single DLC region (none in base game), or a less common monster drop: a monster loot '
          'table with chance >= %d%% (or always) that is not common as in 3' % MONSTER_LESS_CHANCE),
    ('5', 'anything else: monster drops below %d%%, container / quest / unique tables only, no known source'
          % MONSTER_LESS_CHANCE),
])


def load():
    d = json.load(open(os.path.join(HERE, 'data.json'), encoding='utf-8'))
    t = json.load(open(os.path.join(HERE, 'recipes_table.json'), encoding='utf-8'))
    return d['items'], t


def ingredient_type(item):
    tags, icon = item.get('tags', []), item.get('icon_path', '')
    if 'MutagenIngredient' in tags: return 'mutagen'
    if 'StrongAlcohol' in tags: return 'alcohol'
    if 'HerbGameplay' in tags or ICON_HERB in '/' + icon: return 'herb'
    if ICON_ANIMAL_PART in '/' + icon or ICON_MONSTER in '/' + icon: return 'monster_part'
    if ICON_MINERAL in '/' + icon: return 'mineral'
    return 'other'


def shop_effort(shops, regions, typ, herb_nodes):
    """Effort of the best shop / herb-node source: (level, reason) or None."""
    best = []
    n = len(shops)
    if n:
        if set(regions) <= {'ep1', 'bob'} and len(regions) == 1:
            best.append((4, 'all %d shop(s) in DLC region %s only' % (n, next(iter(regions)))))
        elif n >= SHOPS_LV1 and (typ in SHOP_ONLY_TYPES or (typ == 'herb' and herb_nodes)):
            best.append((1, '%d shops%s' % (n, ' + herb node' if typ == 'herb' else '')))
        elif n >= SHOPS_LV2:
            best.append((2, '%d shops' % n))
        else:
            best.append((3, '%d shop(s)' % n))
    if herb_nodes:
        best.append((2, 'herb node'))
    return min(best) if best else None


def monster_effort(drops, rare):
    """Effort of the best monster source: (level, reason) or None."""
    if not drops:
        return None
    common = [m for m in drops if m['chance'] >= MONSTER_COMMON_CHANCE]
    if len(common) >= MONSTER_COMMON_TABLES and not rare:
        return 3, 'common monster drop: %d tables >= %d%%' % (len(common), MONSTER_COMMON_CHANCE)
    top = max(m['chance'] for m in drops)
    if top >= MONSTER_LESS_CHANCE:
        why = ('%d table(s) >= %d%% but tag %s' % (len(common), MONSTER_COMMON_CHANCE, RARE_TAG) if rare and
               len(common) >= MONSTER_COMMON_TABLES else 'best monster table %d%%, %d table(s) >= %d%%' %
               (top, len(common), MONSTER_COMMON_CHANCE))
        return 4, 'less common monster drop: ' + why
    return 5, 'monster drops only below %d%% (best %d%%)' % (MONSTER_LESS_CHANCE, top)


def build():
    items, table = load()
    used, excluded = collections.OrderedDict(), set()
    for r in table.values():
        for fld in ('full', 'copy'):
            for n, q in r[fld]:
                if n not in items:
                    raise SystemExit('ingredient not in data.json: ' + n)
                if items[n].get('category') in ('potion', 'petard'):
                    excluded.add(n)
                else:
                    used[n] = None

    shops = collections.defaultdict(dict)                       # item -> shop table -> region
    herb = collections.defaultdict(set)
    cont = collections.defaultdict(set)
    other = collections.defaultdict(set)
    mons = collections.defaultdict(dict)                        # item -> table -> drop
    for e in loot.entries():
        n = e['item']
        if n not in used:
            continue
        if e['kind'] == 'shop':
            if 'store' in e['table']:                           # loot_include_* are templates, not shops
                shops[n][e['table']] = e['region']
        elif e['kind'] == 'herb':
            herb[n].add(e['table'])
        elif e['kind'] == 'container':
            cont[n].add(e['table'])
        elif e['kind'] == 'monster':
            c = 100 if e['chance'] is None else e['chance']
            q = str(e['qmin']) if e['qmin'] == e['qmax'] else '%s-%s' % (e['qmin'], e['qmax'])
            d = {'table': e['table'], 'chance': c, 'qty': q, 'region': e['region']}
            old = mons[n].get(e['table'])
            if old is None or c > old['chance']:
                mons[n][e['table']] = d
        else:
            other[n].add(e['table'])

    cat = {}
    for n in sorted(used):
        it = items[n]
        typ = ingredient_type(it)
        sh = shops[n]
        regions = collections.Counter(sh.values())
        drops = sorted(mons[n].values(), key=lambda m: (-m['chance'], m['table']))
        rare = RARE_TAG in it.get('tags', [])
        cands = [c for c in (shop_effort(sh, regions, typ, herb[n]), monster_effort(drops, rare)) if c]
        lvl, why = min(cands) if cands else (NO_SOURCE, 'no shop, herb node or monster source' +
                                             (' (containers/other only)' if cont[n] or other[n] else ''))
        cat[n] = {
            'price': int(it['price']),
            'type': typ,
            'shops': {'count': len(sh), 'regions': dict(sorted(regions.items())), 'list': sorted(sh)},
            'world': {'herb_nodes': len(herb[n]), 'containers': len(cont[n]), 'other_tables': len(other[n])},
            'monsters': [{'table': m['table'], 'chance': m['chance'], 'qty': m['qty'], 'region': m['region']}
                         for m in drops],
            'effort': lvl,
            'effort_reason': why,
        }

    meta = {
        'about': 'Generated by tools/recipes/ingredients.py from recipes_table.json, data.json and the loot tables '
                 'in x/. Do not edit by hand.',
        'ingredients': 'every item in a full or copy list of recipes_table.json, except lower-level potions and bombs',
        'excluded_lower_level_items': sorted(excluded),
        'effort_scale': EFFORT_RULES,
        'effort_rule': 'effort = minimum over sources (shops, herb nodes, monster drops); computed by the script, '
                       'no per-ingredient overrides',
        'thresholds': {
            'SHOPS_LV1': SHOPS_LV1, 'SHOPS_LV2': SHOPS_LV2, 'MONSTER_COMMON_CHANCE': MONSTER_COMMON_CHANCE,
            'MONSTER_COMMON_TABLES': MONSTER_COMMON_TABLES, 'MONSTER_LESS_CHANCE': MONSTER_LESS_CHANCE,
            'RARE_TAG': RARE_TAG,
        },
        'threshold_notes': {
            'MONSTER_COMMON_CHANCE': '35% separates deliberate drops (Ghoul blood, Nekker heart: always; Drowner '
                                     'brain: 45/35) from borderline ones (Endriag heart 30/26, Nekker 20)',
            'MONSTER_COMMON_TABLES': '2 tables: one lucky table is not a source; nest and boss tables count as '
                                     'tables because they are real drop places',
            'MONSTER_LESS_CHANCE': '10% is still worth hunting for; below it the part is incidental loot',
            'RARE_TAG': 'loot tables do not say how rare a monster is (Golem heart drops always, golems are rare); '
                        'the game tags its rarer parts mod_valuable, so they never reach level 3 via monsters',
        },
        'type_rules': 'mutagen: tag MutagenIngredient; alcohol: tag StrongAlcohol; herb: tag HerbGameplay or icon '
                      'folder herb; monster_part: icon folder monstrous or alchemy/food_*; mineral: other icon '
                      'folder alchemy; other: the rest (Optima mater, Powdered pearl, Oil)',
        'sources': {
            'shops': 'loot tables with "store" in the name in *shop*.xml; region = folder the XML came from '
                     '(base, ep1 = Hearts of Stone, bob = Blood and Wine); stock is counted whatever the entry '
                     'chance (almost all shop entries are "always")',
            'herb_nodes': 'tables _herb__* in def_loot_herbs.xml',
            'monsters': 'tables in def_loot_monsters.xml / def_loot_animals.xml / def_loot_actors.xml (names '
                        'identify the monster, e.g. _monster__Ghoul, Drowner Nest); chance in percent per kill, '
                        '"always" (-1 in the XML) stored as 100; the best chance per table is kept',
            'containers': 'containers, treasure hunt and unique tables (count only)',
            'other_tables': 'living world, quest and other loot tables (count only)',
        },
        'not_modelled': ['respawn: monster loot has no respawn data in the XML (respawn_time 0); herb entries carry '
                         'respawn_time 1440 but it is not used',
                         'how many monsters of a kind exist or how far they are',
                         'quest rewards and crafting of ingredients (e.g. White Gull 1 can be brewed)'],
    }
    return {'_meta': meta, 'ingredients': cat}


def main():
    out = build()
    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(out, f, indent=1, sort_keys=True, ensure_ascii=False)
        f.write('\n')
    dist = collections.Counter(v['effort'] for v in out['ingredients'].values())
    print('%d ingredients -> %s' % (len(out['ingredients']), OUT))
    print('effort: ' + ', '.join('%d: %d' % (k, dist[k]) for k in sorted(dist)))


if __name__ == '__main__':
    main()
