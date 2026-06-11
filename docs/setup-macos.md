# macOS Setup

This project is currently grounded on a Windows machine, but the workflow can be adapted for macOS.

## Environment

```bash
./scripts/check-environment.sh
```

Install local dependencies with project-local virtual environments where possible.

## GIMP MCP

Install GIMP 3.2+ first. Then:

```bash
cd external/mcp/gimp-mcp
uv sync
```

Copy the plugin to:

```text
~/Library/Application Support/GIMP/3.0/plug-ins/gimp-mcp-plugin/gimp-mcp-plugin.py
```

Restart GIMP, open an image, and use:

```text
Tools > Start MCP Server
```

## ImageSorcery MCP

```bash
python3 -m venv .venv-imagesorcery
./.venv-imagesorcery/bin/python -m pip install --upgrade pip
./.venv-imagesorcery/bin/python -m pip install imagesorcery-mcp
```

Run `imagesorcery-mcp --post-install` only after approving model downloads.

## Inkscape MCP

The upstream `inkmcp` project is documented as Linux-only due to D-Bus. Prefer Linux or WSL for MCP automation. On macOS, use manual Inkscape/CLI export unless a compatible transport is added upstream.

## ComfyUI MCP

Treat ComfyUI as optional Phase 2. Use it only for secondary/lifestyle backgrounds, not product generation.
