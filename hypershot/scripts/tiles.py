#!/usr/bin/env python3
"""Create overlapping tiles and blend already-aligned edited versions."""
import argparse, hashlib, json, math
from pathlib import Path
from PIL import Image, ImageChops


def positions(length, count, overlap):
    size = math.ceil(length / (count - (count - 1) * overlap))
    if count == 1:
        return [(0, length)]
    return [(round(i * (length - size) / (count - 1)), round(i * (length - size) / (count - 1)) + size) for i in range(count)]


def split(args):
    source = Path(args.source)
    im = Image.open(source).convert('RGB')
    folder = Path(args.work) / 'input-tiles'
    folder.mkdir(parents=True, exist_ok=True)
    tiles = []
    for row, (y0, y1) in enumerate(positions(im.height, args.rows, args.overlap)):
        for col, (x0, x1) in enumerate(positions(im.width, args.cols, args.overlap)):
            name = f'tile-{row:02d}-{col:02d}.png'
            im.crop((x0,y0,x1,y1)).save(folder / name)
            tiles.append({'name': name, 'bounds': [x0,y0,x1,y1]})
    meta = {'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(), 'size': list(im.size), 'tiles': tiles}
    (folder / 'manifest.json').write_text(json.dumps(meta, indent=2), encoding='utf-8')
    print(f'{len(tiles)} tiles: {folder}')


def assemble(args):
    meta = json.loads(Path(args.manifest).read_text(encoding='utf-8'))
    scale = args.scale
    w,h = (x*scale for x in meta['size'])
    output = Image.new('RGB',(w,h)); coverage = Image.new('L',(w,h),0)
    for tile in meta['tiles']:
        x0,y0,x1,y1 = [x*scale for x in tile['bounds']]
        piece = Image.open(Path(args.edited) / tile['name']).convert('RGB').resize((x1-x0,y1-y0),Image.Resampling.LANCZOS)
        old = coverage.crop((x0,y0,x1,y1))
        # Preserve previous tiles except at a short feathered transition.
        mask = Image.new('L',piece.size,255)
        if old.getbbox():
            fresh = ImageChops.invert(old)
            mask = ImageChops.lighter(fresh, fresh.filter(__import__('PIL.ImageFilter',fromlist=['GaussianBlur']).GaussianBlur(max(2,20*scale))))
        output.paste(piece,(x0,y0),mask)
        coverage.paste(Image.new('L',piece.size,255),(x0,y0))
    if coverage.getextrema()[0] != 255:
        raise ValueError('Tiles do not cover output')
    output.save(args.output,dpi=(args.dpi,args.dpi))
    print(f'Draft: {args.output} ({w}x{h}); inspect all seams and details')


def main():
    p=argparse.ArgumentParser(description=__doc__); sub=p.add_subparsers(dest='cmd',required=True)
    s=sub.add_parser('split');s.add_argument('source');s.add_argument('work');s.add_argument('--rows',type=int,default=2);s.add_argument('--cols',type=int,default=2);s.add_argument('--overlap',type=float,default=.25)
    a=sub.add_parser('assemble');a.add_argument('manifest');a.add_argument('edited');a.add_argument('output');a.add_argument('--scale',type=int,default=2);a.add_argument('--dpi',type=int,default=300)
    args=p.parse_args()
    if args.cmd=='split':
        if args.rows<1 or args.cols<1 or not 0 <= args.overlap < .8: p.error('rows/cols must be positive; overlap must be in [0, 0.8)')
        split(args)
    else:
        if args.scale<1 or args.dpi<1:p.error('scale and dpi must be positive')
        assemble(args)
if __name__=='__main__': main()
