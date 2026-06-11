#!/usr/bin/env bash
set -euo pipefail

SERVER="${1:-gimp}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

case "$SERVER" in
  gimp)
    REPO="$ROOT/external/mcp/gimp-mcp"
    SERVER_FILE="$REPO/gimp_mcp_server.py"
    if [[ ! -f "$SERVER_FILE" ]]; then
      echo "GIMP MCP server not found at $SERVER_FILE" >&2
      exit 1
    fi
    echo "GIMP must be running with Tools > Start MCP Server active." >&2
    exec uv run --directory "$REPO" "$SERVER_FILE"
    ;;
  gimp-plugin)
    GIMP_CONSOLE="${GIMP_CONSOLE:-gimp-console-3.2}"
    echo "Starting the GIMP MCP plugin socket on 127.0.0.1:9877. Keep this terminal open." >&2
    exec "$GIMP_CONSOLE" -n -i -c --batch-interpreter=plug-in-script-fu-eval -b "(plug-in-mcp-server RUN-NONINTERACTIVE)"
    ;;
  imagesorcery)
    if [[ -x "$ROOT/.venv-imagesorcery310/Scripts/python.exe" ]]; then
      export DISABLE_TELEMETRY=1
      export IMAGESORCERY_AVAILABLE_PATHS="$ROOT/assets/input:$ROOT/assets/product-cutouts:$ROOT/assets/backgrounds:$ROOT/assets/templates:$ROOT/assets/output"
      exec "$ROOT/.venv-imagesorcery310/Scripts/python.exe" "$ROOT/scripts/run-imagesorcery-mcp.py"
    fi
    if [[ -x "$ROOT/.venv-imagesorcery/bin/imagesorcery-mcp" ]]; then
      export DISABLE_TELEMETRY=1
      export IMAGESORCERY_AVAILABLE_PATHS="$ROOT/assets/input:$ROOT/assets/product-cutouts:$ROOT/assets/backgrounds:$ROOT/assets/templates:$ROOT/assets/output"
      exec "$ROOT/.venv-imagesorcery/bin/imagesorcery-mcp"
    fi
    echo "ImageSorcery executable not found in .venv-imagesorcery310 or .venv-imagesorcery." >&2
    exit 1
    ;;
  comfyui)
    REPO="$ROOT/external/mcp/comfyui-mcp-server"
    SERVER_FILE="$REPO/server.py"
    if [[ ! -f "$SERVER_FILE" ]]; then
      echo "ComfyUI MCP server not found at $SERVER_FILE. This is optional Phase 2." >&2
      exit 1
    fi
    echo "ComfyUI must already be running locally, usually at http://127.0.0.1:8188." >&2
    cd "$REPO"
    exec python server.py
    ;;
  *)
    echo "Usage: $0 {gimp|gimp-plugin|imagesorcery|comfyui}" >&2
    exit 2
    ;;
esac
