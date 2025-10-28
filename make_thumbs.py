#!/usr/bin/env python3

"""
make_thumbs.py — batch-generate fast web thumbnails

What it does:
- Reads source photos from ./images (or --src FOLDER)
- Writes small thumbnails to ./images/small (max 1200px longest side)
- Writes large lightbox versions to ./images/large (max 2400px)
- Keeps names the same so your gallery can map small->large automatically
- Converts HEIC/TIFF/etc. to JPG
- JPEG/WebP quality ~82 for good size/quality

Usage (from your project root):
    python make_thumbs.py
    # or change sizes/folders
    python make_thumbs.py --src images --small images/small --large images/large --max-small 1200 --max-large 2400
"""
from pathlib import Path
from PIL import Image, ImageOps
import argparse

def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)

def is_image(p: Path):
    return p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif", ".tif", ".tiff"}

def convert_mode(img: Image.Image) -> Image.Image:
    if img.mode in ("P", "LA", "RGBA", "CMYK", "P;16", "I;16"):
        return img.convert("RGB")
    if img.mode == "L":
        return img.convert("RGB")
    return img

def save_image(img: Image.Image, out_path: Path):
    ext = out_path.suffix.lower()
    save_kwargs = {}
    if ext in (".jpg", ".jpeg"):
        save_kwargs.update(dict(quality=82, optimize=True, progressive=True))
        img = convert_mode(img)
    elif ext == ".png":
        save_kwargs.update(dict(optimize=True, compress_level=6))
    elif ext == ".webp":
        save_kwargs.update(dict(quality=82, method=6))
    else:
        out_path = out_path.with_suffix(".jpg")
        save_kwargs.update(dict(quality=82, optimize=True, progressive=True))
        img = convert_mode(img)
    img.save(out_path, **save_kwargs)
    return out_path

def resize_fit(img: Image.Image, max_px: int) -> Image.Image:
    im = img.copy()
    im.thumbnail((max_px, max_px), Image.Resampling.LANCZOS)
    return im

def process_image(in_path: Path, small_dir: Path, large_dir: Path, max_small: int, max_large: int):
    try:
        with Image.open(in_path) as im0:
            im0 = ImageOps.exif_transpose(im0)
            ext = in_path.suffix.lower()
            out_ext = ext if ext in (".jpg", ".jpeg", ".png", ".webp") else ".jpg"

            small_out = small_dir / (in_path.stem + out_ext)
            large_out = large_dir / (in_path.stem + out_ext)

            # Skip if already fresh
            if small_out.exists() and small_out.stat().st_mtime >= in_path.stat().st_mtime \
               and large_out.exists() and large_out.stat().st_mtime >= in_path.stat().st_mtime:
                return ("skipped", in_path.name)

            small_im = resize_fit(im0, max_small)
            large_im = resize_fit(im0, max_large)

            save_image(small_im, small_out)
            save_image(large_im, large_out)
            return ("ok", in_path.name, small_out.name, large_out.name)
    except Exception as e:
        return ("error", in_path.name, str(e))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="images")
    ap.add_argument("--small", default="images/small")
    ap.add_argument("--large", default="images/large")
    ap.add_argument("--max-small", type=int, default=1200)
    ap.add_argument("--max-large", type=int, default=2400)
    args = ap.parse_args()

    src = Path(args.src)
    small_dir = Path(args.small)
    large_dir = Path(args.large)
    small_dir.mkdir(parents=True, exist_ok=True)
    large_dir.mkdir(parents=True, exist_ok=True)

    imgs = [p for p in src.iterdir() if p.is_file() and is_image(p)]
    results = {"ok":0, "skipped":0, "error":0}
    for p in imgs:
        kind, *rest = process_image(p, small_dir, large_dir, args.max_small, args.max_large)
        results[kind] += 1
        print(kind, *rest)
    print("Summary:", results)

if __name__ == "__main__":
    main()
