#!/usr/bin/env python3
"""Sync a folder of original photos into web-ready images for the site.

Usage:  python3 build_photos.py <source_folder> [site_root]

- Resizes each photo to a full-size (2400px) and thumbnail (900px) JPEG
- Fixes rotation and strips ALL metadata (including GPS location)
- Removes web images whose originals were deleted
- Writes photos.json (newest first, by capture date)
Re-running is cheap: unchanged photos are skipped.
"""
import hashlib, json, sys
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageOps
try:
    import pillow_heif; pillow_heif.register_heif_opener()  # iPhone HEIC photos
except ImportError:
    pass

EXTS = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff", ".heic", ".heif"}
FULL_PX, THUMB_PX = 2400, 900

def capture_time(img, path):
    try:
        exif = img.getexif()
        raw = exif.get_ifd(0x8769).get(36867) or exif.get(306)  # DateTimeOriginal / DateTime
        if raw:
            return datetime.strptime(raw.strip(), "%Y:%m:%d %H:%M:%S").timestamp()
    except Exception:
        pass
    return path.stat().st_mtime

def save(img, dest, px, quality):
    im = img.copy()
    im.thumbnail((px, px), Image.LANCZOS)
    im.save(dest, "JPEG", quality=quality, optimize=True, progressive=True)

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = Path(sys.argv[1])
    root = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).resolve().parent
    full_dir, thumb_dir = root / "photos/full", root / "photos/thumb"
    full_dir.mkdir(parents=True, exist_ok=True)
    thumb_dir.mkdir(parents=True, exist_ok=True)

    entries, keep = [], set()
    for path in sorted(p for p in src.rglob("*") if p.suffix.lower() in EXTS and not p.name.startswith(".")):
        data = path.read_bytes()
        name = hashlib.sha1(data).hexdigest()[:16] + ".jpg"
        if name in keep:  # exact duplicate file
            continue
        keep.add(name)
        with Image.open(path) as img:
            taken = capture_time(img, path)
            full, thumb = full_dir / name, thumb_dir / name
            if not (full.exists() and thumb.exists()):
                img = ImageOps.exif_transpose(img).convert("RGB")  # new image, no metadata
                save(img, full, FULL_PX, 82)
                save(img, thumb, THUMB_PX, 78)
                print("added", path.name)
        with Image.open(full_dir / name) as f:
            w, h = f.size
        entries.append({"full": f"photos/full/{name}", "thumb": f"photos/thumb/{name}", "w": w, "h": h,
                        "alt": path.stem.replace("_", " ").replace("-", " "), "_t": taken})

    for d in (full_dir, thumb_dir):
        for f in d.glob("*.jpg"):
            if f.name not in keep:
                f.unlink()
                print("removed", f.name) if d is full_dir else None

    entries.sort(key=lambda e: e.pop("_t"), reverse=True)
    (root / "photos.json").write_text(json.dumps({"photos": entries}, indent=1))
    print(f"{len(entries)} photos in gallery")

if __name__ == "__main__":
    main()
