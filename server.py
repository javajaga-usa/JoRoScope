"""JoRoScope Root Server Entrypoint
Allows running: py -3.12 server.py [port] [--no-browser]
"""
import sys
from pathlib import Path

# Ensure src directory is in Python path
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from joroscope.server import main

if __name__ == "__main__":
    main()
