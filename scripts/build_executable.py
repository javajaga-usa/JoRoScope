"""Rebuild the standalone Windows executable using PyInstaller.
Usage:
    py -3.12 scripts/build_executable.py
"""

from pathlib import Path
import os
import sys

try:
    import PyInstaller.__main__
except ImportError:
    print("PyInstaller is not installed. Install with: pip install pyinstaller")
    sys.exit(1)

root = Path(__file__).resolve().parent.parent
server_script = root / "server.py"
web_dir = root / "src" / "joroscope" / "web"
vendor_dir = root / "vendor"
dist_dir = root / "dist"
build_dir = root / "build"

print("Building JoRoScope standalone executable...")
print(f"  Entry script: {server_script}")
print(f"  Web assets:   {web_dir}")

PyInstaller.__main__.run([
    str(server_script),
    "--name", "JoRoScope",
    "--onefile",
    "--console",
    "--paths", str(vendor_dir),
    "--paths", str(root / "src"),
    # Bundle the web assets inside the package, where joroscope.server looks for them
    "--add-data", f"{web_dir}{os.pathsep}joroscope/web",
    "--collect-all", "tzdata",
    "--distpath", str(dist_dir),
    "--workpath", str(build_dir),
    "--specpath", str(root),
    "--noconfirm"
])

print("\nBuild complete. Executable located at:")
print(f"  {dist_dir / 'JoRoScope.exe'}")
