Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Test-Command {
    param([Parameter(Mandatory = $true)][string]$Name)
    $cmd = Get-Command $Name -ErrorAction SilentlyContinue
    if ($null -eq $cmd) {
        [pscustomobject]@{ Name = $Name; Found = $false; Detail = "" }
    } else {
        [pscustomobject]@{ Name = $Name; Found = $true; Detail = $cmd.Source }
    }
}

function Test-PathList {
    param([string[]]$Paths)
    foreach ($path in $Paths) {
        if (Test-Path -LiteralPath $path) {
            return $path
        }
    }
    return ""
}

$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

Write-Host "Amazon Image Editor environment check"
Write-Host "Root: $root"
Write-Host ""

Write-Host "Git status"
git -C $root status --short --branch
Write-Host ""

Write-Host "OS"
$os = Get-ComputerInfo | Select-Object OsName, OsVersion, OsArchitecture, WindowsVersion
$os | Format-List

Write-Host "Core commands"
$commands = @("python", "py", "pip", "uv", "node", "npm", "git", "codex", "pipx")
foreach ($name in $commands) {
    $result = Test-Command $name
    if ($result.Found) {
        Write-Host "[OK] $($result.Name): $($result.Detail)"
    } else {
        Write-Host "[MISSING] $($result.Name)"
    }
}
Write-Host ""

Write-Host "Versions"
foreach ($cmd in @(
        @{ Name = "python"; Args = @("--version") },
        @{ Name = "py"; Args = @("--version") },
        @{ Name = "pip"; Args = @("--version") },
        @{ Name = "uv"; Args = @("--version") },
        @{ Name = "node"; Args = @("--version") },
        @{ Name = "npm"; Args = @("--version") },
        @{ Name = "git"; Args = @("--version") },
        @{ Name = "codex"; Args = @("--version") }
    )) {
    if ((Test-Command $cmd.Name).Found) {
        try {
            $output = & $cmd.Name @($cmd.Args) 2>&1
            Write-Host "$($cmd.Name): $output"
        } catch {
            Write-Host "$($cmd.Name): version check failed: $($_.Exception.Message)"
        }
    }
}
Write-Host ""

$gimpPath = Test-PathList @(
    "$HOME\AppData\Local\Programs\GIMP 3\bin\gimp-3.2.exe",
    "$HOME\AppData\Local\Programs\GIMP 3\bin\gimp.exe",
    "C:\Program Files\GIMP 3\bin\gimp-3.0.exe",
    "C:\Program Files\GIMP 3\bin\gimp-console-3.0.exe",
    "C:\Program Files\GIMP 2\bin\gimp-2.10.exe",
    "C:\Program Files\GIMP 2\bin\gimp-console-2.10.exe"
)
$inkscapePath = Test-PathList @(
    "C:\Program Files\Inkscape\bin\inkscape.exe",
    "C:\Program Files\Inkscape\inkscape.exe"
)
$comfyPath = Test-PathList @(
    "C:\ComfyUI",
    "$HOME\ComfyUI",
    "$HOME\OneDrive\Documents\ComfyUI"
)
$comfyMcpPath = Join-Path $root "external\mcp\comfyui-mcp-server"

Write-Host "Graphics tools"
if ($gimpPath) { Write-Host "[OK] GIMP: $gimpPath" } else { Write-Host "[MISSING] GIMP not found in common paths" }
if ($inkscapePath) { Write-Host "[OK] Inkscape: $inkscapePath" } else { Write-Host "[MISSING] Inkscape not found in common paths" }
if ($comfyPath) { Write-Host "[OK] ComfyUI app candidate: $comfyPath" } else { Write-Host "[MISSING] ComfyUI app not found in common paths" }
if (Test-Path -LiteralPath $comfyMcpPath) { Write-Host "[OK] ComfyUI MCP source: $comfyMcpPath" } else { Write-Host "[MISSING] ComfyUI MCP source not found under external\mcp" }
Write-Host ""

Write-Host "Codex config"
$userConfig = Join-Path $HOME ".codex\config.toml"
$projectConfig = Join-Path $root ".codex\config.toml"
$exampleConfig = Join-Path $root ".codex\config.example.toml"
foreach ($path in @($userConfig, $projectConfig, $exampleConfig)) {
    if (Test-Path -LiteralPath $path) {
        $item = Get-Item -LiteralPath $path
        Write-Host "[OK] $path ($($item.Length) bytes)"
    } else {
        Write-Host "[MISSING] $path"
    }
}
Write-Host ""

Write-Host "MCP list"
if ((Test-Command "codex").Found) {
    codex mcp list
} else {
    Write-Host "Codex CLI is not available."
}
