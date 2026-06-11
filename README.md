# Amazon Image Editor

Local-first MCP workflow for creating premium Amazon listing images with open-source image tools.

This project is intentionally approval-first. It provides docs, prompts, scripts, and project-scoped Codex MCP examples. It does not edit your user-level Codex config, install global apps, download model weights, enable telemetry, or use paid APIs without explicit approval.

## Current Status

- Workspace is a fresh Git repo at this project root.
- Python, uv, Node, npm, Git, and Codex CLI are available on this machine.
- GIMP 3.2.4 and Inkscape 1.4.4 have been installed after approval.
- ComfyUI app was not installed; ComfyUI MCP remains optional Phase 2.
- The user-level Codex config at `%USERPROFILE%\.codex\config.toml` is treated as read-only by this project.
- `.codex/config.toml` is local and ignored by Git; `.codex/config.example.toml` is the committed example.
- Upstream MCP projects are added under `external/mcp/` as Git submodules.
- ImageSorcery YOLO/CLIP model assets are installed locally and ignored by Git.
- `codex mcp list` sees the project `gimp-mcp` and `imagesorcery-mcp` entries after local project config is present.
- GIMP MCP socket, snapshot, and export were smoke-tested on local port `9877`.

## Tool Roles

- GIMP MCP: primary Photoshop-like editor after GIMP 3.2+ and the GIMP plugin are installed.
- ImageSorcery MCP: local crop, resize, rotate, background removal, drawing, OCR, and object detection utility.
- Inkscape: Windows fallback is CLI/manual SVG work. `inkmcp` is documented as Linux/WSL Phase 2 because its upstream README says it depends on D-Bus.
- ComfyUI MCP: optional Phase 2 for AI lifestyle backgrounds only. Product pixels should come from real product photos or cutouts.

## Quick Start

1. Check this machine:

   ```powershell
   .\scripts\check-environment.ps1
   ```

2. Read the Amazon image rules:

   ```text
   docs\amazon-image-rules.md
   ```

3. Review the project-scoped MCP example:

   ```text
   .codex\config.example.toml
   ```

4. After installing the approved MCP dependencies, start local servers with:

   ```powershell
   .\scripts\start-mcp.ps1 -Server gimp-plugin
   .\scripts\start-mcp.ps1 -Server gimp
   .\scripts\start-mcp.ps1 -Server imagesorcery
   ```

   `gimp-plugin` starts GIMP's local socket on port `9877`; keep that terminal open. `gimp` starts the MCP stdio bridge that Codex uses to talk to the socket.

5. Verify an exported image:

   ```powershell
   py -3.13 .\scripts\verify-amazon-image.py assets\output\main.jpg --kind main
   ```

6. Batch export local images without touching originals:

   ```powershell
   .\.venv-imagesorcery310\Scripts\python.exe .\scripts\batch-resize-export.py assets\input assets\output --size 2000
   ```

## Verified Smoke Outputs

- ImageSorcery YOLOE model load/inference: `model_loaded YOLOE`, zero detections on the synthetic sample image.
- CLIP import: `clip import ok`.
- GIMP MCP socket check: `running: true`, port `9877`.
- GIMP MCP smoke files: `assets/output/gimp-mcp-smoke-snapshot.png` and `assets/output/gimp-mcp-smoke-export.png`.
- Amazon-ready export: `assets/output/gimp-mcp-smoke-exportamazon-v01.jpg`, 2000 x 2000 JPEG, basic checks passed.

## Working Folders

- `assets/input/`: original product photos. Keep untouched.
- `assets/product-cutouts/`: transparent product cutouts made from real product photos.
- `assets/backgrounds/`: approved secondary/lifestyle backgrounds.
- `assets/templates/`: reusable layout assets.
- `assets/output/`: Amazon-ready exports.

The asset folders are ignored by Git except for `.gitkeep` placeholders.

## MCP Setup Summary

Codex MCP configuration can be stored in `~/.codex/config.toml` or project-scoped `.codex/config.toml` for trusted projects. This repo only ships `.codex/config.example.toml`; copy or adapt it locally after reviewing paths.

Use:

```powershell
codex mcp list
```

Inside the Codex TUI, use `/mcp` to inspect active MCP servers.

## Image Workflows

- Main image cleanup: `docs/workflow-main-image.md`, `prompts/main-image-cleanup.md`
- Secondary benefit infographic: `docs/workflow-secondary-infographic.md`, `prompts/secondary-benefit-infographic.md`
- Dimension image: `docs/workflow-dimensions-image.md`, `prompts/dimension-callout-image.md`
- Lifestyle composite: `docs/workflow-lifestyle-image.md`, `prompts/lifestyle-background-composite.md`
- Batch export: `prompts/batch-export.md`

## Manual Approval Boundaries

Ask before:

- Editing `%USERPROFILE%\.codex\config.toml`
- Installing GIMP, Inkscape, ComfyUI, pipx, or system packages
- Downloading ImageSorcery/ComfyUI model weights
- Enabling telemetry
- Using paid APIs
- Publishing, uploading, or externally sharing product imagery
