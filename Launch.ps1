$ErrorActionPreference = 'Stop'
$appFolder = $PSScriptRoot
$serverScript = Join-Path $appFolder 'server.py'

# 1. Check bundled runtime
$bundledPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
if (Test-Path -LiteralPath $bundledPython) {
    & $bundledPython $serverScript
    exit $LASTEXITCODE
}

# 2. Check py -3.12 launcher
$pyCmd = Get-Command py -ErrorAction SilentlyContinue
if ($pyCmd) {
    & py -3.12 $serverScript
    if ($LASTEXITCODE -eq 0) { exit 0 }
}

# 3. Check default python
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if ($pythonCmd) {
    & python $serverScript
    if ($LASTEXITCODE -eq 0) { exit 0 }
}

Write-Host "JoRoScope requires Python 3.12 (64-bit) with swisseph." -ForegroundColor Yellow
Write-Host "Please ensure Python 3.12 is installed or run 'py -3.12 server.py'." -ForegroundColor Cyan
Read-Host "Press Enter to close"
