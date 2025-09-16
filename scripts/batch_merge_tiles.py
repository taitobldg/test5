import argparse, pathlib
from lxml import etree
def merge_tile(tile_dir: pathlib.Path) -> str:
    header = '<?xml version="1.0" encoding="UTF-8"?>\n<core:CityModel xmlns:core="http://www.opengis.net/citygml/2.0" xmlns:gml="http://www.opengis.net/gml" xmlns:bldg="http://www.opengis.net/citygml/building/2.0" xmlns:app="http://www.opengis.net/citygml/appearance/2.0">\n'
    footer = '</core:CityModel>'
    parts = []; app = None
    for p in sorted(tile_dir.glob('*.xml')):
        t = p.read_text(encoding='utf-8', errors='ignore')
        if p.name.endswith('-appearance.xml'): app = t
        else: parts.append(t)
    return header + '\n'.join(parts + ([app] if app else [])) + footer
if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--tiles-dir', default='tiles'); ap.add_argument('--out-dir', default='out'); ap.add_argument('--formats', default='xml'); args = ap.parse_args()
    out = pathlib.Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)
    for tile in set(p.parent for p in pathlib.Path(args.tiles_dir).rglob('*-bldg-*.xml')):
        xml = merge_tile(tile); name = tile.name + '.xml'; (out / name).write_text(xml, encoding='utf-8')
