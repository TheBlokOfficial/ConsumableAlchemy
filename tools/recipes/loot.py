"""Loot tables from the extracted game XML (tools/recipes/x): shared reader for ingredients.py."""
import os, re, glob

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, 'x')


def file_kind(path):
    """Kind of loot tables in a file, by file name: shop / herb / monster / container / other."""
    fn = os.path.basename(path)
    return ('shop' if 'shop' in fn else 'herb' if 'herb' in fn else
            'monster' if 'monster' in fn or 'animal' in fn or 'actor' in fn else
            'container' if 'container' in fn or 'treasure' in fn or 'unique' in fn else 'other')


def file_region(path):
    """base game / ep1 (Hearts of Stone) / bob (Blood and Wine), by the folder the file was extracted to."""
    rel = os.path.relpath(path, BASE).replace('\\', '/')
    return rel.split('/')[1] if rel.startswith('dlc/') else 'base'


def loot_files():
    fs = (glob.glob(os.path.join(BASE, '**', 'def_loot*.xml'), recursive=True) +
          glob.glob(os.path.join(BASE, '**', '*shop*.xml'), recursive=True))
    return sorted(f for f in set(fs) if 'items_plus' not in f)


def _num(s):
    return int(s) if s is not None and re.fullmatch(r'-?\d+', s) else None


def _attrs(tag):
    return dict(re.findall(r'(\w+)="([^"]*)"', tag))


def entries():
    """Yield one dict per <loot_entry>: kind, region, file, table, item, chance (percent, None = always),
    qmin, qmax, respawn (minutes as given in the XML; 0 = not set)."""
    for f in loot_files():
        kind, region = file_kind(f), file_region(f)
        t = re.sub(r'<!--.*?-->', '', open(f, encoding='utf-8', errors='replace').read(), flags=re.S)
        for m in re.finditer(r'<loot\s+name="([^"]+)"[^>]*>(.*?)</loot>', t, re.S):
            for e in re.finditer(r'<loot_entry\s([^>]*)/?>', m.group(2)):
                a = _attrs(e.group(1))
                if 'name' not in a:
                    continue
                c = _num(a.get('chance'))
                yield {'kind': kind, 'region': region, 'file': os.path.basename(f), 'table': m.group(1),
                       'item': a['name'], 'chance': None if c is None or c < 0 else c,
                       'qmin': _num(a.get('quantity_min')), 'qmax': _num(a.get('quantity_max')),
                       'respawn': _num(a.get('respawn_time')) or 0}
