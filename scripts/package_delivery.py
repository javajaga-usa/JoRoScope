"""Release packaging script.
Packages clean source code, documentation, launchers, and compiled binaries into a verified ZIP.
Usage:
    py -3.12 scripts/package_delivery.py
"""

from pathlib import Path
import zipfile
import hashlib
import json

root = Path(__file__).resolve().parent.parent
destination = root / "JoRoScope-Complete.zip"

entries = {}

# Include standalone binary if present
exe_path = root / "dist" / "JoRoScope.exe"
if not exe_path.is_file() and (root / "Astrology-Reborn" / "dist" / "JoRoScope.exe").is_file():
    exe_path = root / "Astrology-Reborn" / "dist" / "JoRoScope.exe"

if exe_path.is_file():
    entries["JoRoScope.exe"] = exe_path

# Root files
for filename in ["README.md", "LICENSE", "pyproject.toml", "requirements.txt", "Launch.ps1", "Start JoRoScope.cmd", "server.py", "engine.py", "predictions.py"]:
    fpath = root / filename
    if fpath.is_file():
        entries[filename] = fpath

# Directories
for folder_name in ["src", "tests", "docs", "scripts", "licenses", "vendor"]:
    folder_path = root / folder_name
    if folder_path.is_dir():
        for p in folder_path.rglob("*"):
            if p.is_file() and not p.name.endswith((".pyc", ".log", ".tmp")) and "__pycache__" not in p.parts:
                entries[p.relative_to(root).as_posix()] = p

manifest = {
    name: {
        "bytes": p.stat().st_size,
        "sha256": hashlib.sha256(p.read_bytes()).hexdigest()
    }
    for name, p in entries.items()
}

with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED, compresslevel=8) as z:
    for name, p in entries.items():
        z.write(p, name)
    z.writestr("DELIVERY-MANIFEST.json", json.dumps(manifest, indent=2))

with zipfile.ZipFile(destination) as z:
    assert z.testzip() is None

print(f"Packaged: {destination} ({destination.stat().st_size:,} bytes, {len(entries)} files; ZIP CRC verified)")
