import sys, argparse, pathlib
from lxml import etree
def validate(path: pathlib.Path) -> bool:
    try:
        etree.parse(str(path)); return True
    except Exception as e:
        print(f"INVALID: {path}: {e}"); return False
if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--paths', default='tiles'); args = ap.parse_args()
    base = pathlib.Path(args.paths); files = list(base.rglob('*.xml'))
    ok = all(validate(p) for p in files); sys.exit(0 if ok else 1)
