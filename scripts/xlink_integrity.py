import sys, argparse, pathlib
from lxml import etree
def check_tile(tile_dir: pathlib.Path) -> bool:
    app_files = list(tile_dir.glob('*-appearance.xml'))
    if not app_files: return True
    app_tree = etree.parse(str(app_files[0]))
    app_ids = set(el.get('{http://www.opengis.net/gml}id') for el in app_tree.xpath('//*[@gml:id]', namespaces={'gml':'http://www.opengis.net/gml'}))
    ok = True
    for p in tile_dir.glob('*-bldg-*.xml'):
        tree = etree.parse(str(p))
        for el in tree.xpath('//*[@xlink:href]', namespaces={'xlink':'http://www.w3.org/1999/xlink'}):
            href = el.get('{http://www.w3.org/1999/xlink}href')
            if href and '#' in href:
                frag = href.split('#',1)[1]
                if frag not in app_ids: print(f"BROKEN XLink: {href} in {p}"); ok = False
    return ok
if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--paths', default='tiles'); args = ap.parse_args()
    base = pathlib.Path(args.paths); ok = True
    for tile in set(p.parent for p in base.rglob('*-bldg-*.xml')):
        if not check_tile(tile): ok = False
    sys.exit(0 if ok else 1)
