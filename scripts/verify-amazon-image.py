#!/usr/bin/env python3
"""Heuristic checks for Amazon listing image exports."""

from __future__ import annotations

import argparse
import os
import struct
import sys
from pathlib import Path


def read_png_size(path: Path) -> tuple[int, int] | None:
    with path.open("rb") as handle:
        header = handle.read(24)
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", header[16:24])


def get_image_type(path: Path) -> str | None:
    with path.open("rb") as handle:
        header = handle.read(12)
    if header.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if header.startswith(b"\xff\xd8"):
        return "jpeg"
    return None


def read_jpeg_size(path: Path) -> tuple[int, int] | None:
    with path.open("rb") as handle:
        data = handle.read()
    if not data.startswith(b"\xff\xd8"):
        return None
    index = 2
    while index < len(data):
        if data[index] != 0xFF:
            index += 1
            continue
        marker = data[index + 1]
        index += 2
        if marker in {0xD8, 0xD9}:
            continue
        if index + 2 > len(data):
            return None
        length = struct.unpack(">H", data[index : index + 2])[0]
        if marker in range(0xC0, 0xC4) or marker in range(0xC5, 0xC8) or marker in range(0xC9, 0xCC) or marker in range(0xCD, 0xD0):
            if index + 7 > len(data):
                return None
            height, width = struct.unpack(">HH", data[index + 3 : index + 7])
            return width, height
        index += length
    return None


def get_size(path: Path) -> tuple[int, int] | None:
    kind = get_image_type(path)
    if kind == "png":
        return read_png_size(path)
    if kind == "jpeg":
        return read_jpeg_size(path)
    return None


def white_background_score(path: Path) -> float | None:
    try:
        from PIL import Image
    except ImportError:
        return None

    with Image.open(path) as image:
        image = image.convert("RGB")
        width, height = image.size
        sample_points: list[tuple[int, int]] = []
        step_x = max(width // 20, 1)
        step_y = max(height // 20, 1)

        for x in range(0, width, step_x):
            sample_points.append((x, 0))
            sample_points.append((x, height - 1))
        for y in range(0, height, step_y):
            sample_points.append((0, y))
            sample_points.append((width - 1, y))

        if not sample_points:
            return None

        white = 0
        for point in sample_points:
            red, green, blue = image.getpixel(point)
            if red >= 245 and green >= 245 and blue >= 245:
                white += 1
        return white / len(sample_points)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Amazon listing image export basics.")
    parser.add_argument("image", type=Path)
    parser.add_argument("--kind", choices=["main", "secondary"], default="secondary")
    parser.add_argument("--min-size", type=int, default=1000)
    parser.add_argument("--recommended-size", type=int, default=2000)
    parser.add_argument("--max-mb", type=float, default=10.0)
    args = parser.parse_args()

    path = args.image
    failures: list[str] = []
    warnings: list[str] = []

    if not path.exists():
        print(f"FAIL: file does not exist: {path}")
        return 2

    file_size = path.stat().st_size
    size_mb = file_size / (1024 * 1024)
    if size_mb > args.max_mb:
        failures.append(f"file is {size_mb:.2f} MB, above {args.max_mb:.2f} MB")

    image_type = get_image_type(path)
    if image_type not in {"jpeg", "png"}:
        failures.append(f"expected JPEG or PNG, got {image_type or 'unknown'}")

    dimensions = get_size(path)
    if dimensions is None:
        failures.append("could not read image dimensions")
    else:
        width, height = dimensions
        if width != height:
            warnings.append(f"image is not square: {width} x {height}")
        if width < args.min_size or height < args.min_size:
            failures.append(f"image is smaller than minimum: {width} x {height}")
        if width != args.recommended_size or height != args.recommended_size:
            warnings.append(f"recommended size is {args.recommended_size} x {args.recommended_size}; got {width} x {height}")

    if args.kind == "main":
        score = white_background_score(path)
        if score is None:
            warnings.append("install Pillow to run white-background heuristic: python -m pip install Pillow")
        elif score < 0.95:
            failures.append(f"main image border is not likely pure white enough: {score:.0%} white-ish border samples")

    print(f"Image: {path}")
    print(f"Type: {image_type or 'unknown'}")
    print(f"Size: {size_mb:.2f} MB")
    if dimensions:
        print(f"Dimensions: {dimensions[0]} x {dimensions[1]}")

    for warning in warnings:
        print(f"WARN: {warning}")
    for failure in failures:
        print(f"FAIL: {failure}")

    if failures:
        return 1

    print("PASS: basic Amazon export checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
