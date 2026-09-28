# JoRoScope launcher for Windows: run .\Launch.ps1, or double-click "Start JoRoScope.cmd".
# The first run creates a private Python environment (.venv) and installs the Swiss
# Ephemeris; later runs start straight away. Extra arguments go to server.py
# (a port number, --no-browser).
# Exit codes are checked explicitly: under 'Stop', Windows PowerShell 5.1 turns any stderr
# output of python or pip (even a warning) into a terminating error.
$ErrorActionPreference = 'Continue'
Set-Location -LiteralPath $PSScriptRoot
$Host.UI.RawUI.WindowTitle = 'JoRoScope - Vedic Astrology'

function Stop-WithMessage([string]$Message) {
    Write-Host ''
    Write-Host $Message -ForegroundColor Yellow
    Read-Host 'Press Enter to close'
    exit 3  # already paused; the .cmd launcher pauses only for other failures
}

# Python 3.11 or newer: the py launcher first (newest version it knows), then python on the PATH.
# The Microsoft Store "python" alias only opens the Store, so it fails the version check.
function Find-Python {
    $check = 'import sys; sys.exit(sys.version_info < (3, 11))'
    $candidates = @()
    if (Get-Command py -ErrorAction SilentlyContinue) {
        $candidates += , @('py', '-3.13')
        $candidates += , @('py', '-3.12')
        $candidates += , @('py', '-3.11')
        $candidates += , @('py', '-3')
    }
    if (Get-Command python -ErrorAction SilentlyContinue) {
        $candidates += , @('python')
    }
    foreach ($candidate in $candidates) {
        $exe = $candidate[0]
        $prefix = @($candidate | Select-Object -Skip 1)
        try {
            & $exe @prefix -c $check 2>$null | Out-Null
            if ($LASTEXITCODE -eq 0) { return , $candidate }
        } catch {
            continue
        }
    }
    return $null
}

$venvPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $venvPython)) {
    $python = Find-Python
    if (-not $python) {
        Stop-WithMessage 'JoRoScope needs Python 3.11 or newer (64-bit). Install it from https://www.python.org/downloads/windows/ (tick "Add python.exe to PATH") and open this launcher again.'
    }
    Write-Host 'First run: creating a Python environment for JoRoScope...'
    $exe = $python[0]
    $prefix = @($python | Select-Object -Skip 1)
    & $exe @prefix -m venv .venv
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $venvPython)) {
        Stop-WithMessage 'Could not create the Python environment in .venv.'
    }
}

& $venvPython -c 'import swisseph' 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host 'Installing the Swiss Ephemeris and time-zone data (one time)...'
    & $venvPython -m pip install --quiet --disable-pip-version-check -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Stop-WithMessage 'Installing the requirements failed. Check the internet connection and try again.'
    }
}

& $venvPython server.py @args
if ($LASTEXITCODE -ne 0) {
    Stop-WithMessage 'JoRoScope stopped with an error (shown above).'
}
