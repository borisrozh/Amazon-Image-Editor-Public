#!/usr/bin/env python3
"""Install ImageSorcery model assets into the project root.

This avoids the upstream post-install entrypoint because imagesorcery_mcp imports
its server at package import time, and that server changes cwd into site-packages.
"""

from __future__ import annotations

import json
import subprocess
import sys
import uuid
from pathlib import Path

import requests
from tqdm import tqdm


ROOT = Path(__file__).resolve().parents[1]
MODELS = [
    "yoloe-11l-seg-pf.pt",
    "yoloe-11s-seg-pf.pt",
    "yoloe-11l-seg.pt",
    "yoloe-11s-seg.pt",
]
CLIP_URL = "https://github.com/ultralytics/assets/releases/download/v8.3.0/mobileclip_blt.ts"


def ensure_config() -> None:
    config = ROOT / "config.toml"
    if not config.exists():
        config.write_text(
            "\n".join(
                [
                    "[telemetry]",
                    "enabled = false",
                    "",
                    "[detection]",
                    'default_model = "yoloe-11l-seg-pf.pt"',
                    "confidence_threshold = 0.75",
                    "",
                    "[find]",
                    'default_model = "yoloe-11l-seg.pt"',
                    "confidence_threshold = 0.75",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        print(f"created {config}")
    else:
        print(f"exists {config}")

    user_id = ROOT / ".user_id"
    if not user_id.exists():
        user_id.write_text(str(uuid.uuid4()), encoding="utf-8")
        print(f"created {user_id}")
    else:
        print(f"exists {user_id}")


def ensure_model_descriptions() -> None:
    models_dir = ROOT / "models"
    models_dir.mkdir(exist_ok=True)
    descriptions = models_dir / "model_descriptions.json"
    data = {
        "yoloe-11l-seg-pf.pt": "Ultralytics YOLOE large segmentation model with prompt-free vocabulary support.",
        "yoloe-11s-seg-pf.pt": "Ultralytics YOLOE small segmentation model with prompt-free vocabulary support.",
        "yoloe-11l-seg.pt": "Ultralytics YOLOE large segmentation model.",
        "yoloe-11s-seg.pt": "Ultralytics YOLOE small segmentation model.",
        "mobileclip_blt.ts": "MobileCLIP model used for text-guided visual prompts.",
    }
    descriptions.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    print(f"wrote {descriptions}")


def install_clip_package() -> None:
    print("installing CLIP package from https://github.com/ultralytics/CLIP.git")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "git+https://github.com/ultralytics/CLIP.git"],
        cwd=ROOT,
        check=True,
    )


def download_yolo_models() -> None:
    from ultralytics import YOLO

    models_dir = ROOT / "models"
    models_dir.mkdir(exist_ok=True)

    for model_name in MODELS:
        destination = models_dir / model_name
        if destination.exists():
            print(f"exists {destination}")
            continue

        print(f"downloading {model_name}")
        model = YOLO(model_name)
        downloaded = Path(model.ckpt_path) if getattr(model, "ckpt_path", None) else Path(model_name)
        if downloaded.exists() and downloaded.resolve() != destination.resolve():
            destination.write_bytes(downloaded.read_bytes())
        if not destination.exists():
            raise RuntimeError(f"expected model at {destination}")
        print(f"wrote {destination}")


def download_file(url: str, destination: Path) -> None:
    if destination.exists():
        print(f"exists {destination}")
        return

    print(f"downloading {url}")
    with requests.get(url, stream=True, timeout=60) as response:
        response.raise_for_status()
        total = int(response.headers.get("content-length", 0))
        with destination.open("wb") as handle, tqdm(
            total=total,
            unit="B",
            unit_scale=True,
            desc=destination.name,
        ) as progress:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    handle.write(chunk)
                    progress.update(len(chunk))
    print(f"wrote {destination}")


def main() -> int:
    ensure_config()
    ensure_model_descriptions()
    download_yolo_models()
    install_clip_package()
    download_file(CLIP_URL, ROOT / "mobileclip_blt.ts")
    print("ImageSorcery model setup complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
