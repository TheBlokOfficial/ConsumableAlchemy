"""Run the recipe rules (rules.py) on recipes_table.json and print the findings per recipe.

  python tools/recipes/validate.py [--errors-only] [--table <file>]

Lines: ERROR|WARN <recipe key>: [rule id] message; then counts per rule and per severity.
Exit code 1 if any error, else 0. Needs data.json and ingredient_catalog.json (see recipes.md).
"""
import argparse, collections, sys

import rules


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--errors-only', action='store_true', help='print only errors')
    ap.add_argument('--table', metavar='FILE', help='validate this table instead of recipes_table.json')
    a = ap.parse_args()
    table = rules.load_json(a.table) if a.table else None
    ctx = rules.load_context(table)
    res = rules.run(ctx)

    shown = ('error',) if a.errors_only else ('error', 'warn')
    per_rule, per_sev, rows = collections.Counter(), collections.Counter(), collections.defaultdict(set)
    for k in ctx.keys:
        for f in res[k]:
            if f['severity'] not in shown:
                continue
            print('%s %s: [%s] %s' % (f['severity'].upper(), k, f['id'], f['text']))
            per_rule[f['id']] += 1
            per_sev[f['severity']] += 1
            rows[f['severity']].add(k)

    print()
    print('recipes: %d' % len(ctx.keys))
    for rule in rules.RULES:
        if rule.severity in shown:
            print('  %-5s %-28s %d' % (rule.severity, rule.id, per_rule[rule.id]))
    for sev in shown:
        print('%s: %d findings in %d recipes' % (sev, per_sev[sev], len(rows[sev])))
    sys.exit(1 if per_sev['error'] else 0)


if __name__ == '__main__':
    main()
