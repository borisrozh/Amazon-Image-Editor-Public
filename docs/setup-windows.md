# Windows Setup

These steps are approval-first. Do not run global installers or model downloads until you have reviewed the commands.

## 1. Check Environment

```powershell
.\scripts\check-environment.ps1
```

## 2. External MCP Repos

The approved location is:

```text
external\mcp\
```

Use Git submodules or clearly separated clones. Do not copy upstream code into this repo.

## 3. GIMP MCP

GIMP MCP requires GIMP 3.2+.

GIMP 3.2.4 is installed on this machine at:

```text
%LOCALAPPDATA%\Programs\GIMP 3\bin\gimp-3.2.exe
```

The GIMP MCP Python environment is installed with `uv sync` under:

```text
external\mcp\gimp-mcp\.venv
```

To refresh it:

```powershell
cd external\mcp\gimp-mcp
uv sync
```

The plugin file has been copied into:

```text
%APPDATA%\GIMP\3.2\plug-ins\gimp-mcp-plugin\gimp-mcp-plugin.py
```

Then restart GIMP, open an image, and use:

```text
Tools > Start MCP Server
```

The GIMP plugin listens on local port `9877`; the MCP stdio server connects Codex to that plugin.

A repeatable console start also works on this machine:

```powershell
.\scripts\start-mcp.ps1 -Server gimp-plugin
```

Keep that terminal open while the GIMP MCP socket is needed. This headless console mode can load, snapshot, and export images, but GIMP may warn when it cannot create a display. For normal visual editing, use the GIMP UI menu path above.

## 4. ImageSorcery MCP

ImageSorcery MCP is installed in a local Python 3.10 venv for model compatibility:

```text
.venv-imagesorcery310
```

To recreate it:

```powershell
py -3.10 -m venv .venv-imagesorcery310
.\.venv-imagesorcery310\Scripts\python.exe -m pip install --upgrade pip
.\.venv-imagesorcery310\Scripts\python.exe -m pip install imagesorcery-mcp==0.12.0
```

The version is pinned to match the reviewed `external/mcp/imagesorcery-mcp` submodule. Update both together.

Do not run model setup until model downloads are explicitly approved:

```powershell
.\.venv-imagesorcery310\Scripts\python.exe .\scripts\install-imagesorcery-models.py
```

This project uses `scripts\install-imagesorcery-models.py` instead of the upstream post-install entrypoint because importing `imagesorcery_mcp` changes the working directory inside the virtual environment. The local script keeps the model files in this project:

Keep telemetry disabled unless you explicitly opt in.

The project launch script sets `DISABLE_TELEMETRY=1` and restricts ImageSorcery file access to the project asset folders. Model assets are stored locally in ignored paths:

```text
models\
mobileclip_blt.ts
```

## 5. Inkscape

Native Windows Inkscape can still be useful for manual SVG and PNG export. The `inkmcp` project is not treated as a native Windows Phase 1 MCP server because upstream documents it as Linux-only due to D-Bus.

Use WSL/Linux for `inkmcp` only as a separate Phase 2 decision.

## 6. Codex MCP

Review:

```text
.codex\config.example.toml
```

If you create `.codex\config.toml`, keep it local and review with:

```powershell
git diff -- .codex\config.toml
codex mcp list
```

Do not edit `%USERPROFILE%\.codex\config.toml` without an exact diff and approval.
