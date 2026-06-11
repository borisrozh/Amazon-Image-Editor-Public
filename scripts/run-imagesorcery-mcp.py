#!/usr/bin/env python3
"""Run ImageSorcery MCP with this project as the working directory."""

from __future__ import annotations

import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

os.environ.setdefault("DISABLE_TELEMETRY", "1")
os.environ.setdefault(
    "IMAGESORCERY_AVAILABLE_PATHS",
    os.pathsep.join(
        str(ROOT / part)
        for part in (
            "assets/input",
            "assets/product-cutouts",
            "assets/backgrounds",
            "assets/templates",
            "assets/output",
        )
    ),
)

# Upstream imports change cwd to site-packages; restore the project root after import.
from imagesorcery_mcp.server import main  # noqa: E402

os.chdir(ROOT)

if __name__ == "__main__":
    main()
