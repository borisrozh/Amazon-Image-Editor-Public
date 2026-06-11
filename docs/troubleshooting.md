# Troubleshooting

## Codex Cannot See MCP Servers

Run:

```powershell
codex mcp list
```

Inside the Codex TUI, use:

```text
/mcp
```

Check whether `.codex/config.toml` exists and whether the project is trusted.

## GIMP MCP Cannot Connect

- Confirm GIMP 3.2+ is installed.
- Confirm the plugin file was copied into the GIMP plug-ins directory.
- Restart GIMP after copying the plugin.
- Open an image in GIMP.
- Start the server from `Tools > Start MCP Server`.
- Confirm local port `9877` is not blocked.
- On this Windows machine, `.\scripts\start-mcp.ps1 -Server gimp-plugin` can start the socket through `gimp-console-3.2.exe`. Keep that terminal open. If GIMP reports a display-constructor warning in headless mode, try the full GIMP UI menu path for interactive editing.

## ImageSorcery Fails to Start

- Confirm `.venv-imagesorcery310` exists.
- Confirm `scripts\run-imagesorcery-mcp.py` runs with `.venv-imagesorcery310\Scripts\python.exe`.
- Confirm model files exist in `models\` and `mobileclip_blt.ts` exists in the project root.
- Do not assume object detection works until model downloads have been approved and run.
- The launch script sets `DISABLE_TELEMETRY=1` and limits file access to project asset folders with `IMAGESORCERY_AVAILABLE_PATHS`.
- The upstream post-install entrypoint was not used here because its import path changes the working directory inside the venv. Use `scripts\install-imagesorcery-models.py` for this project.

## Inkscape MCP on Windows

`inkmcp` is not planned as native Windows Phase 1. Use manual Inkscape or WSL/Linux.

## ComfyUI MCP

ComfyUI is optional Phase 2. Confirm ComfyUI is running locally before starting the MCP server.

## Amazon Main Image Fails White Background Check

- Re-export on pure white.
- Check edges and shadows.
- Confirm no text or graphics are present.
- Use the verification script as a heuristic, then visually inspect.
