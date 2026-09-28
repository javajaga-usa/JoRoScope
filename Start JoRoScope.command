#!/bin/bash
# JoRoScope launcher for macOS: double-click in Finder, or run ./"Start JoRoScope.command".
# The first run creates a private Python environment (.venv) and installs the Swiss
# Ephemeris; later runs start straight away. Extra arguments go to server.py
# (a port number, --no-browser).
cd "$(dirname "$0")" || exit 1
printf '\033]0;JoRoScope - Vedic Astrology\007'

fail() {
    echo
    echo "$1"
    read -r -p "Press Return to close. "
    exit 1
}

# Python 3.11 or newer; macOS's own /usr/bin/python3 is too old
PYTHON=""
for candidate in python3.13 python3.12 python3.11 python3; do
    if command -v "$candidate" >/dev/null 2>&1 &&
        "$candidate" -c 'import sys; sys.exit(sys.version_info < (3, 11))' 2>/dev/null; then
        PYTHON="$(command -v "$candidate")"
        break
    fi
done
[ -n "$PYTHON" ] || fail "JoRoScope needs Python 3.11 or newer. Install it from https://www.python.org/downloads/macos/ and open this launcher again."

VENV_PYTHON=".venv/bin/python"
if [ ! -x "$VENV_PYTHON" ]; then
    echo "First run: creating a Python environment for JoRoScope..."
    "$PYTHON" -m venv .venv || fail "Could not create the Python environment in .venv."
fi

if ! "$VENV_PYTHON" -c 'import swisseph' 2>/dev/null; then
    echo "Installing the Swiss Ephemeris and time-zone data (one time)..."
    "$VENV_PYTHON" -m pip install --quiet --disable-pip-version-check -r requirements.txt ||
        fail "Installing the requirements failed. Check the internet connection, or install Xcode's command line tools with: xcode-select --install"
fi

"$VENV_PYTHON" server.py "$@" || fail "JoRoScope stopped with an error (shown above)."
