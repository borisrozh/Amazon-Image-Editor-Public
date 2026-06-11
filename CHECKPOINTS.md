# Checkpoints

Use this file to track setup and verification progress.

## Phase 1 - Environment

- [x] Confirmed workspace root.
- [x] Confirmed fresh Git repo.
- [x] Confirmed Windows 11 environment.
- [x] Confirmed Python, pip, uv, Node, npm, Git, and Codex CLI availability.
- [x] Initially confirmed GIMP, Inkscape, and ComfyUI were not detected.
- [x] Installed GIMP 3.2.4 and Inkscape 1.4.4 after approval.
- [x] Confirmed user-level Codex config exists.
- [x] Confirmed project-level Codex config is not present.

## Phase 2 - Project Scaffold

- [x] Add local-first project structure.
- [x] Add Amazon image rules.
- [x] Add workflow docs and prompts.
- [x] Add environment, MCP launch, verification, and batch export scripts.
- [x] Add project-scoped Codex MCP example.

## Phase 3 - MCP Setup

- [x] Add external MCP repos under `external/mcp/`.
- [x] Install GIMP 3.2+ after explicit approval.
- [x] Install GIMP plugin after explicit approval.
- [x] Create local GIMP MCP environment.
- [x] Create local ImageSorcery environment.
- [x] Run ImageSorcery model setup after explicit approval for model downloads.
- [x] Configure project-scoped `.codex/config.toml` after reviewing example.
- [x] Verify with `codex mcp list` or `/mcp`.

## Phase 4 - Workflow Verification

- [x] GIMP MCP responds on local port `9877`.
- [x] GIMP MCP snapshots and exports a sample image to `assets/output/`.
- [x] ImageSorcery local server starts with telemetry disabled through the project wrapper.
- [x] ImageSorcery YOLOE model loads and runs inference.
- [x] ImageSorcery CLIP dependency imports successfully.
- [ ] ImageSorcery background removal against a real product photo through an exposed MCP client.
- [ ] Inkscape Windows fallback creates/export SVG/PNG manually or by CLI.
- [x] Sample image exports to `assets/output/`.
- [x] GIMP MCP export can be resized into a 2000 x 2000 Amazon-ready JPEG.
- [x] `verify-amazon-image.py` checks output dimensions, size, mode, and likely white background.

## Phase 2 Optional - Creative Generation

- [ ] Install or locate ComfyUI after explicit approval.
- [ ] Add ComfyUI MCP only after local ComfyUI works.
- [ ] Use AI-generated backgrounds only for secondary/lifestyle images.
