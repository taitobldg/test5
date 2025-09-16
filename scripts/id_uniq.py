import sys, argparse, pathlib
from lxml import etree
def check_ids(tile_dir: pathlib.Path) -> bool:
    ids = set(); ok = True
    for p in sorted(tile_dir.glob('*.xml')):
        try:
            tree = etree.parse(str(p))
            for el in tree.xpath('//*[@gml:id]', namespaces={'gml':'http://www.opengis.net/gml'}):
                gid = el.get('{http://www.opengis.net/gml}id')
                if gid in ids: print(f"DUPLICATE gml:id: {gid} in {p}"); ok = False
                ids.add(gid)
        except Exception as e: print(f"PARSE-ERROR: {p}: {e}"); ok = False
    return ok
if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--paths', default='tiles'); args = ap.parse_args()
    base = pathlib.Path(args.paths); ok = True
    for tile in set(p.parent for p in base.rglob('*-bldg-*.xml')):
        if not check_ids(tile): ok = False
    sys.exit(0 if ok else 1)
