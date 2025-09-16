import sys, argparse, pathlib
from lxml import etree
def is_canonical(p: pathlib.Path) -> bool:
    try:
        tree = etree.parse(str(p))
        text = etree.tostring(tree, pretty_print=True, encoding='utf-8').decode('utf-8')
        with open(p, 'rb') as f: orig = f.read().decode('utf-8', errors='ignore')
        return text.strip() == orig.strip()
    except Exception as e:
        print(f"FORMAT-ERROR: {p}: {e}"); return False
if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--paths', default='tiles'); ap.add_argument('--check', action='store_true'); args = ap.parse_args()
    base = pathlib.Path(args.paths); files = list(base.rglob('*.xml'))
    ok = True
    for p in files:
        if not is_canonical(p): print(f"NON-CANONICAL: {p}"); ok = False
    sys.exit(0 if ok else 1)
