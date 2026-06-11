#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

has_cmd() {
  command -v "$1" >/dev/null 2>&1
}

echo "Amazon Image Editor environment check"
echo "Root: $ROOT"
echo

echo "Git status"
git -C "$ROOT" status --short --branch || true
echo

echo "OS"
uname -a
echo

echo "Core commands"
for cmd in python3 python pip3 pip uv node npm git codex pipx gimp inkscape; do
  if has_cmd "$cmd"; then
    echo "[OK] $cmd: $(command -v "$cmd")"
  else
    echo "[MISSING] $cmd"
  fi
done
echo

echo "Versions"
for cmd in "python3 --version" "python --version" "pip --version" "uv --version" "node --version" "npm --version" "git --version" "codex --version"; do
  sh -c "$cmd" 2>/dev/null || true
done
echo

echo "Codex config"
for path in "$HOME/.codex/config.toml" "$ROOT/.codex/config.toml" "$ROOT/.codex/config.example.toml"; do
  if [[ -f "$path" ]]; then
    echo "[OK] $path"
  else
    echo "[MISSING] $path"
  fi
done
echo

echo "MCP list"
if has_cmd codex; then
  codex mcp list || true
else
  echo "Codex CLI is not available."
fi
