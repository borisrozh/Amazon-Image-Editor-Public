param(
    [ValidateSet("gimp", "gimp-plugin", "imagesorcery", "comfyui")]
    [string]$Server = "gimp"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

switch ($Server) {
    "gimp" {
        $repo = Join-Path $root "external\mcp\gimp-mcp"
        $server = Join-Path $repo "gimp_mcp_server.py"
        if (-not (Test-Path -LiteralPath $server)) {
            throw "GIMP MCP server not found at $server. Add the upstream repo under external\mcp\gimp-mcp first."
        }
        Write-Warning "Before this works, GIMP must be running, an image must be open, and Tools > Start MCP Server must be active in GIMP."
        & uv run --directory $repo $server
    }
    "gimp-plugin" {
        $candidates = @(
            "$HOME\AppData\Local\Programs\GIMP 3\bin\gimp-console-3.2.exe",
            "$HOME\AppData\Local\Programs\GIMP 3\bin\gimp-console-3.exe",
            "C:\Program Files\GIMP 3\bin\gimp-console-3.2.exe",
            "C:\Program Files\GIMP 3\bin\gimp-console-3.exe"
        )
        $gimpConsole = $candidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
        if (-not $gimpConsole) {
            throw "GIMP console executable not found. Start the plugin manually in GIMP with Tools > MCP > Start MCP Server."
        }
        Write-Host "Starting the GIMP MCP plugin socket on 127.0.0.1:9877. Keep this terminal open while using GIMP MCP."
        Write-Warning "Headless console mode can load/export images, but GIMP may warn when a display cannot be created. For interactive editing, use GIMP UI: Tools > MCP > Start MCP Server."
        & $gimpConsole -n -i -c --batch-interpreter=plug-in-script-fu-eval -b "(plug-in-mcp-server RUN-NONINTERACTIVE)"
    }
    "imagesorcery" {
        $py310 = Join-Path $root ".venv-imagesorcery310\Scripts\python.exe"
        $py313 = Join-Path $root ".venv-imagesorcery\Scripts\python.exe"
        $python = if (Test-Path -LiteralPath $py310) { $py310 } else { $py313 }
        if (-not (Test-Path -LiteralPath $python)) {
            throw "ImageSorcery Python environment not found. Create the local venv and install imagesorcery-mcp first."
        }
        $allowedPaths = @(
            (Join-Path $root "assets\input"),
            (Join-Path $root "assets\product-cutouts"),
            (Join-Path $root "assets\backgrounds"),
            (Join-Path $root "assets\templates"),
            (Join-Path $root "assets\output")
        )
        $env:DISABLE_TELEMETRY = "1"
        $env:IMAGESORCERY_AVAILABLE_PATHS = ($allowedPaths -join ";")
        & $python (Join-Path $root "scripts\run-imagesorcery-mcp.py")
    }
    "comfyui" {
        $repo = Join-Path $root "external\mcp\comfyui-mcp-server"
        $server = Join-Path $repo "server.py"
        if (-not (Test-Path -LiteralPath $server)) {
            throw "ComfyUI MCP server not found at $server. This is optional Phase 2."
        }
        Write-Warning "ComfyUI must already be running locally, usually at http://127.0.0.1:8188."
        Push-Location $repo
        try {
            & python $server
        } finally {
            Pop-Location
        }
    }
}
