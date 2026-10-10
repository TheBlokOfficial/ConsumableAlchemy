"""HTML comparison report of the recipe table: vanilla vs full vs copy, cost, effort, rule findings.

  python tools/recipes/report.py [--base <git-ref>] [--out <file>]

Findings come from rules.py (error / warn / info), the same rules validate.py prints. Effort = sum((e-1)*qty) / max.
--base also loads recipes_table.json from <git-ref> and shows the base full/copy and their numbers under rows that differ.
Reads recipes_table.json, data.json (vanilla recipes) and ingredient_catalog.json (run ingredients.py first).
Output: report.html (single file, inline CSS + JS, gitignored).
"""
import argparse, datetime, json, os, subprocess, sys

import rules

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
TABLE = 'tools/recipes/recipes_table.json'


def as_map(lst):
    return {n: q for n, q in lst}


def git_table(ref):
    r = subprocess.run(['git', '-C', ROOT, 'show', '%s:%s' % (ref, TABLE)], capture_output=True)
    if r.returncode != 0:
        sys.exit('git show %s:%s failed: %s' % (ref, TABLE, r.stderr.decode('utf-8', 'replace').strip()))
    short = subprocess.run(['git', '-C', ROOT, 'rev-parse', '--short', ref], capture_output=True, text=True)
    return json.loads(r.stdout.decode('utf-8')), short.stdout.strip()


def build(base_ref):
    ctx = rules.load_context()
    table, cat, excluded, items, vanilla = ctx.table, ctx.catalog, ctx.excluded, ctx.items, ctx.vanilla
    base, base_hash = (git_table(base_ref) if base_ref else (None, ''))
    found = rules.run(ctx)

    rows = []
    for key in ctx.keys:
        r = table[key]
        van = vanilla.get(key, {}).get('ings', [])
        row = {'key': key, 'item': r['item'], 'family': r['family'], 'level': r['level'], 'kind': r['kind'],
               'note': r.get('note', ''), 'vanilla': van, 'full': r['full'], 'copy': r['copy'],
               'fullStats': ctx.stats(r['full'])[0], 'copyStats': ctx.stats(r['copy'])[0], 'flags': found[key],
               'inVanilla': key in vanilla}
        if base is not None:
            b = base.get(key)
            if b is None:
                row['baseNew'] = True
            else:
                if as_map(b['full']) != as_map(r['full']):
                    row['baseFull'], row['baseFullStats'] = b['full'], ctx.stats(b['full'])[0]
                if as_map(b['copy']) != as_map(r['copy']):
                    row['baseCopy'], row['baseCopyStats'] = b['copy'], ctx.stats(b['copy'])[0]
        rows.append(row)

    used = {n for r in rows for fld in ('vanilla', 'full', 'copy', 'baseFull', 'baseCopy') for n, _ in r.get(fld, [])}
    info = {}
    for n in sorted(used):
        i = items.get(n, {})
        e = cat.get(n)
        d = {'price': int(i['price']) if 'price' in i else None}
        if e:
            d.update({'type': e['type'], 'effort': e['effort'], 'reason': e['effort_reason'],
                      'shops': e['shops']['count'], 'regions': e['shops']['regions'], 'world': e['world'],
                      'monsters': ['%s %d%% x%s' % (m['table'], m['chance'], m['qty']) for m in e['monsters']]})
        elif n in excluded:
            d['type'] = 'lower-level item'
        info[n] = d
    removed = sorted(set(base) - set(table)) if base is not None else []
    return {'rows': rows, 'info': info, 'generated': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
            'baseRef': base_ref or '', 'baseHash': base_hash, 'baseRemoved': removed}

def render(payload):
    blob = json.dumps(payload, ensure_ascii=True).replace('</', '<\\/')
    return PAGE.replace('/*DATA*/', blob)


PAGE = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Recipe report</title>
<style>
:root {
  color-scheme: light dark;
  --bg: #f6f5f1; --fg: #1d1d1b; --muted: #6b6a64; --line: #d9d6cc; --panel: #ffffff; --head: #ecebe4;
  --add: #d6f0d8; --add-fg: #14591d; --chg: #fff0c2; --chg-fg: #6b4e00; --rem: #f8d7d4; --rem-fg: #8a1c14;
  --err: #b3261e; --warn: #9a6a00; --info: #6b6a64;
  --e1: #3f9142; --e2: #86a63a; --e3: #d2a21b; --e4: #d9742a; --e5: #c03a30; --e0: #8a8a82; --ebg: #fff;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #1a1a18; --fg: #e8e6df; --muted: #9a988f; --line: #3a3a36; --panel: #232321; --head: #2c2c29;
    --add: #1e3b22; --add-fg: #9ad7a1; --chg: #433812; --chg-fg: #f0cf72; --rem: #4a2220; --rem-fg: #f2a39d;
    --err: #f08a82; --warn: #e0b33a; --info: #9a988f;
    --e1: #4fae52; --e2: #98b84a; --e3: #e0b33a; --e4: #e8863c; --e5: #de5a50; --e0: #8a8a82; --ebg: #111;
  }
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--fg); font: 13px/1.4 system-ui, sans-serif; }
header { padding: 12px 16px; border-bottom: 1px solid var(--line); background: var(--panel); }
h1 { margin: 0 0 4px; font-size: 18px; }
.sum { color: var(--muted); }
.sum b { color: var(--fg); }
.controls { display: flex; flex-wrap: wrap; gap: 8px 12px; align-items: center; padding: 10px 16px;
  position: sticky; top: 0; background: var(--bg); border-bottom: 1px solid var(--line); z-index: 3; }
.controls label { display: flex; align-items: center; gap: 4px; }
select, input[type=search] { background: var(--panel); color: var(--fg); border: 1px solid var(--line);
  border-radius: 4px; padding: 3px 6px; font: inherit; }
input[type=search] { min-width: 180px; }
.wrap { padding: 0 16px 24px; }
table { border-collapse: collapse; width: auto; background: var(--panel); }
th, td { border: 1px solid var(--line); padding: 4px 6px; vertical-align: top; text-align: left; }
th { background: var(--head); position: sticky; top: 46px; z-index: 2; cursor: pointer; user-select: none; }
th.nosort { cursor: default; }
th .arr { color: var(--muted); }
tr.group td { background: var(--head); font-weight: 600; color: var(--muted); padding: 3px 6px; }
tr.sev-error > td:first-child { box-shadow: inset 3px 0 0 var(--err); }
tr.sev-warn > td:first-child { box-shadow: inset 3px 0 0 var(--warn); }
.rname { font-weight: 600; }
.rmeta { color: var(--muted); font-size: 12px; }
.ing { display: flex; width: fit-content; align-items: center; gap: 3px; margin: 1px 0; padding: 0 3px;
  border-radius: 3px; white-space: nowrap; cursor: help; }
.ing.add { background: var(--add); color: var(--add-fg); }
.ing.chg { background: var(--chg); color: var(--chg-fg); }
.ing.rem { background: var(--rem); color: var(--rem-fg); text-decoration: line-through; }
.ing small { opacity: .75; }
.legend .ing { display: inline-flex; margin-right: 4px; }
.eb { display: inline-block; min-width: 15px; height: 15px; line-height: 15px; text-align: center; border-radius: 8px;
  font-size: 10px; font-weight: 700; color: var(--ebg); background: var(--e0); }
.e1 { background: var(--e1); } .e2 { background: var(--e2); } .e3 { background: var(--e3); }
.e4 { background: var(--e4); } .e5 { background: var(--e5); }
.base { margin-top: 3px; padding-top: 2px; border-top: 1px dashed var(--line); opacity: .65; }
.base .lbl { display: block; font-size: 11px; color: var(--muted); }
.base .ing.gone { text-decoration: line-through; }
.base.nums { margin-top: 3px; }
.num { text-align: right; white-space: nowrap; font-variant-numeric: tabular-nums; }
.flag { display: block; max-width: 220px; }
.flag.error { color: var(--err); font-weight: 600; } .flag.warn { color: var(--warn); } .flag.info { color: var(--info); }
.empty { padding: 24px; color: var(--muted); }
.legend { color: var(--muted); font-size: 12px; margin-top: 4px; }
</style>
</head>
<body>
<header>
  <h1>Recipe report</h1>
  <div class="sum" id="sum"></div>
  <div class="legend">Ingredient badge = effort 1-5 (hover for catalog details). Full recipe: <span class="ing add">added</span>
    <span class="ing chg">quantity changed</span> <span class="ing rem">removed</span> vs vanilla.
    Effort = sum of (ingredient effort - 1) x quantity / highest ingredient effort; lower-level items count in cost only. Findings: <span class="flag error" style="display:inline">error</span> <span class="flag warn" style="display:inline">warn</span> <span class="flag info" style="display:inline">info</span>.</div>
</header>
<div class="controls">
  <label>Kind <select id="fKind"></select></label>
  <label>Family <select id="fFam"></select></label>
  <label>Search <input type="search" id="fText" placeholder="recipe or ingredient"></label>
  <label><input type="checkbox" id="fFlag"> only rows with errors or warnings</label>
  <span class="sum" id="count"></span>
</div>
<div class="wrap"><table id="tbl"><thead></thead><tbody></tbody></table><div class="empty" id="empty" hidden>No rows.</div></div>
<script id="data" type="application/json">/*DATA*/</script>
<script>
(function () {
  var D = JSON.parse(document.getElementById('data').textContent);
  var rows = D.rows, info = D.info;
  var cols = [
    {id: 'default', label: 'Recipe', get: function (r) { return r.__idx; }},
    {id: 'van', label: 'Vanilla', nosort: true},
    {id: 'full', label: 'Full (table)', nosort: true},
    {id: 'copy', label: 'Copy (table)', nosort: true},
    {id: 'fcost', label: 'Full cost', get: function (r) { return r.fullStats.cost; }, num: true},
    {id: 'feff', label: 'Full effort (Σ(e−1)×q) / max', get: function (r) { return r.fullStats.effort_max * 1000 + r.fullStats.effort; }, num: true},
    {id: 'ccost', label: 'Copy cost', get: function (r) { return r.copyStats.cost; }, num: true},
    {id: 'ceff', label: 'Copy effort (Σ(e−1)×q) / max', get: function (r) { return r.copyStats.effort_max * 1000 + r.copyStats.effort; }, num: true},
    {id: 'flags', label: 'Findings', get: function (r) { return nsev(r, 'error') * 1000 + nsev(r, 'warn') * 10 + nsev(r, 'info'); }, num: true}
  ];
  rows.forEach(function (r, i) { r.__idx = i; });
  var sortId = 'default', sortDir = 1;

  function nsev(r, s) { return r.flags.filter(function (f) { return f.severity === s; }).length; }
  function flagged(r) { return nsev(r, 'error') + nsev(r, 'warn') > 0; }
  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  function tip(n) {
    var i = info[n] || {}, t = [n];
    if (i.price != null) t.push('price ' + i.price);
    if (i.type) t.push('type ' + i.type);
    if (i.effort) {
      t.push('effort ' + i.effort + ' (' + i.reason + ')');
      var reg = Object.keys(i.regions || {}).map(function (k) { return k + ' ' + i.regions[k]; }).join(', ');
      t.push('shops ' + i.shops + (reg ? ' (' + reg + ')' : ''));
      t.push('world: herb nodes ' + i.world.herb_nodes + ', containers ' + i.world.containers);
      t.push(i.monsters.length ? 'monsters:\n  ' + i.monsters.slice(0, 8).join('\n  ') +
        (i.monsters.length > 8 ? '\n  +' + (i.monsters.length - 8) + ' more' : '') : 'monsters: none');
    } else if (!i.type) t.push('NOT IN CATALOG');
    return t.join('\n');
  }
  function ing(n, q, cls, extra) {
    var s = el('span', 'ing' + (cls ? ' ' + cls : ''));
    s.title = tip(n);
    s.appendChild(document.createTextNode(n + ' ×' + q));
    if (extra) s.appendChild(el('small', null, extra));
    var i = info[n];
    var b = el('span', 'eb' + (i && i.effort ? ' e' + i.effort : ''), i && i.effort ? i.effort : '–');
    s.appendChild(b);
    return s;
  }
  function map(l) { var m = {}; l.forEach(function (x) { m[x[0]] = x[1]; }); return m; }
  // full list against vanilla: added / quantity changed / removed
  function fullCell(r) {
    var td = el('td'), v = map(r.vanilla), f = map(r.full);
    r.full.forEach(function (x) {
      if (!(x[0] in v)) td.appendChild(ing(x[0], x[1], 'add'));
      else if (v[x[0]] !== x[1]) td.appendChild(ing(x[0], x[1], 'chg', ' (vanilla ' + v[x[0]] + ')'));
      else td.appendChild(ing(x[0], x[1]));
    });
    r.vanilla.forEach(function (x) { if (!(x[0] in f)) td.appendChild(ing(x[0], x[1], 'rem')); });
    if (r.baseFull) td.appendChild(baseBlock(r.baseFull, r.full));
    return td;
  }
  function plain(l) { var td = el('td'); l.forEach(function (x) { td.appendChild(ing(x[0], x[1])); }); return td; }
  function copyCell(r) {
    var td = plain(r.copy);
    if (r.baseCopy) td.appendChild(baseBlock(r.baseCopy, r.copy));
    return td;
  }
  function baseBlock(b, cur) {
    var d = el('div', 'base'), c = map(cur);
    d.appendChild(el('span', 'lbl', 'base ' + (D.baseHash || D.baseRef)));
    b.forEach(function (x) { d.appendChild(ing(x[0], x[1], c[x[0]] === x[1] ? '' : 'gone')); });
    return d;
  }
  function statCells(tr, s, b) {
    var c = el('td', 'num', s.cost), e = el('td', 'num', s.effort + ' / ' + s.effort_max);
    if (b) {
      c.appendChild(el('div', 'base nums', 'base ' + b.cost));
      e.appendChild(el('div', 'base nums', 'base ' + b.effort + ' / ' + b.effort_max));
    }
    tr.appendChild(c); tr.appendChild(e);
  }

  function filtered() {
    var k = document.getElementById('fKind').value, f = document.getElementById('fFam').value;
    var q = document.getElementById('fText').value.trim().toLowerCase();
    var only = document.getElementById('fFlag').checked;
    return rows.filter(function (r) {
      if (k && r.kind !== k) return false;
      if (f && r.family !== f) return false;
      if (only && !flagged(r)) return false;
      if (q) {
        var hay = (r.key + ' ' + r.family + ' ' + r.full.concat(r.copy, r.vanilla).map(function (x) { return x[0]; }).join(' ')).toLowerCase();
        if (hay.indexOf(q) < 0) return false;
      }
      return true;
    });
  }
  function render() {
    var list = filtered(), col = cols.filter(function (c) { return c.id === sortId; })[0];
    list.sort(function (a, b) {
      var x = col.get(a), y = col.get(b);
      return (x < y ? -1 : x > y ? 1 : a.__idx - b.__idx) * sortDir;
    });
    var tb = document.querySelector('#tbl tbody');
    tb.textContent = '';
    var grouped = sortId === 'default' && sortDir === 1, last = '';
    list.forEach(function (r) {
      if (grouped && last !== r.kind + '/' + r.family) {
        last = r.kind + '/' + r.family;
        var g = el('tr', 'group'), gt = el('td', null, r.kind + ' → ' + r.family);
        gt.colSpan = cols.length; g.appendChild(gt); tb.appendChild(g);
      }
      var tr = el('tr', nsev(r, 'error') ? 'sev-error' : nsev(r, 'warn') ? 'sev-warn' : '');
      var t0 = el('td');
      t0.appendChild(el('div', 'rname', r.item));
      t0.appendChild(el('div', 'rmeta', 'level ' + r.level + ' · ' + r.kind + ' · ' + r.family +
        (r.baseNew ? ' · NEW vs base' : '') + (r.inVanilla ? '' : ' · no vanilla recipe')));
      if (r.note) t0.appendChild(el('div', 'rmeta', r.note));
      tr.appendChild(t0);
      var tv = plain(r.vanilla); tr.appendChild(tv);
      tr.appendChild(fullCell(r));
      tr.appendChild(copyCell(r));
      statCells(tr, r.fullStats, r.baseFullStats);
      statCells(tr, r.copyStats, r.baseCopyStats);
      var tf = el('td');
      // Rules with several findings per recipe (near collisions) collapse to one line; the list is in the tooltip.
      var byId = {};
      r.flags.forEach(function (f) { (byId[f.id] = byId[f.id] || []).push(f); });
      Object.keys(byId).forEach(function (id) {
        var fs = byId[id], sp;
        if (fs.length === 1) { sp = el('span', 'flag ' + fs[0].severity, fs[0].text); sp.title = id; }
        else {
          sp = el('span', 'flag ' + fs[0].severity, id.replace(/_/g, ' ') + ' ×' + fs.length);
          sp.title = fs.map(function (f) { return f.text; }).join('\n');
          sp.style.cursor = 'help';
        }
        tf.appendChild(sp);
      });
      tr.appendChild(tf);
      tb.appendChild(tr);
    });
    document.getElementById('empty').hidden = list.length > 0;
    document.getElementById('count').textContent = list.length + ' of ' + rows.length + ' rows';
    var heads = document.querySelectorAll('#tbl th');
    cols.forEach(function (c, i) {
      var a = heads[i].querySelector('.arr');
      if (a) a.textContent = c.id === sortId ? (sortDir > 0 ? ' ▲' : ' ▼') : '';
    });
  }
  function init() {
    var th = document.querySelector('#tbl thead'), tr = el('tr');
    cols.forEach(function (c) {
      var h = el('th', c.nosort ? 'nosort' : '', c.label);
      // the effort columns show "sum / max", so say what sorts them
      if (c.id === 'feff' || c.id === 'ceff') h.title = 'sorted by max, then sum';
      if (!c.nosort) {
        h.appendChild(el('span', 'arr'));
        h.addEventListener('click', function () {
          if (sortId === c.id) sortDir = -sortDir; else { sortId = c.id; sortDir = c.num ? -1 : 1; }
          render();
        });
      }
      tr.appendChild(h);
    });
    th.appendChild(tr);
    function opts(sel, vals, all) {
      sel.appendChild(new Option(all, ''));
      vals.forEach(function (v) { sel.appendChild(new Option(v, v)); });
    }
    var kinds = [], fams = [];
    rows.forEach(function (r) {
      if (kinds.indexOf(r.kind) < 0) kinds.push(r.kind);
      if (fams.indexOf(r.family) < 0) fams.push(r.family);
    });
    opts(document.getElementById('fKind'), kinds, 'all kinds');
    opts(document.getElementById('fFam'), fams.slice().sort(), 'all families');
    ['fKind', 'fFam', 'fFlag'].forEach(function (id) { document.getElementById(id).addEventListener('change', render); });
    document.getElementById('fText').addEventListener('input', render);

    var counts = {}, withErr = 0, withWarn = 0;
    rows.forEach(function (r) { counts[r.kind] = (counts[r.kind] || 0) + 1; if (nsev(r, 'error')) withErr++; if (nsev(r, 'warn')) withWarn++; });
    var s = document.getElementById('sum');
    s.innerHTML = '';
    function part(label, val) { var b = document.createElement('b'); b.textContent = val; s.appendChild(document.createTextNode(label + ' ')); s.appendChild(b); s.appendChild(document.createTextNode(' · ')); }
    part('rows', rows.length);
    kinds.forEach(function (k) { part(k, counts[k]); });
    part('rows with errors', withErr);
    part('rows with warnings', withWarn);
    part('generated', D.generated);
    if (D.baseRef) {
      part('base', D.baseRef + (D.baseHash ? ' (' + D.baseHash + ')' : ''));
      part('rows differing from base', rows.filter(function (r) { return r.baseFull || r.baseCopy || r.baseNew; }).length);
      if (D.baseRemoved.length) part('removed since base', D.baseRemoved.join(', '));
    }
    render();
  }
  init();
})();
</script>
</body>
</html>
'''


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--base', metavar='REF', help='git ref whose recipes_table.json is shown under differing rows')
    ap.add_argument('--out', default=os.path.join(HERE, 'report.html'), help='output file (default report.html)')
    a = ap.parse_args()
    html = render(build(a.base))
    with open(a.out, 'w', encoding='utf-8', newline='\n') as f:
        f.write(html)
    print(os.path.abspath(a.out))


if __name__ == '__main__':
    main()
