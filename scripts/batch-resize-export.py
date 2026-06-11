#!/usr/bin/env python3
"""Non-destructive batch resize/export helper for Amazon-ready images."""

from __future__ import annotations

import argparse
from pathlib import Path


SUPPORTED = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}


def output_name(path: Path, output_dir: Path, suffix: str, ext: str) -> Path:
    return output_dir / f"{path.stem}{suffix}{ext}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Resize images into square Amazon-ready exports.")
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--size", type=int, default=2000)
    parser.add_argument("--format", choices=["jpg", "png"], default="jpg")
    parser.add_argument("--suffix", default="-amazon-2000")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    try:
        from PIL import Image, ImageOps
    except ImportError:
        print("Pillow is required. Install in a local environment with: python -m pip install Pillow")
        return 2

    if not args.input_dir.is_dir():
        print(f"Input directory does not exist: {args.input_dir}")
        return 2

    args.output_dir.mkdir(parents=True, exist_ok=True)

    ext = ".jpg" if args.format == "jpg" else ".png"
    created = 0
    skipped = 0

    for path in sorted(args.input_dir.iterdir()):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED:
            continue

        destination = output_name(path, args.output_dir, args.suffix, ext)
        if destination.exists() and not args.overwrite:
            print(f"SKIP exists: {destination}")
            skipped += 1
            continue

        with Image.open(path) as image:
            image = ImageOps.exif_transpose(image)
            if args.format == "jpg":
                canvas = Image.new("RGB", (args.size, args.size), "white")
                working = image.convert("RGBA")
            else:
                canvas = Image.new("RGBA", (args.size, args.size), (255, 255, 255, 0))
                working = image.convert("RGBA")

            working.thumbnail((args.size, args.size), Image.Resampling.LANCZOS)
            x = (args.size - working.width) // 2
            y = (args.size - working.height) // 2
            canvas.paste(working, (x, y), working)

            if args.format == "jpg":
                canvas.save(destination, quality=95, optimize=True)
            else:
                canvas.save(destination, optimize=True)

        print(f"CREATE {destination}")
        created += 1

    print(f"Done. Created: {created}. Skipped: {skipped}. Originals untouched.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
