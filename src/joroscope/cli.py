"""JoRoScope Command Line Interface
"""

import argparse
import json
import sys
from . import __version__
from .server import run_server
from .core.engine import calculate, calculate_match


def main():
    parser = argparse.ArgumentParser(
        prog="joroscope",
        description="JoRoScope — Modern Precision Vedic Astrology Calculation Suite"
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Serve command
    serve_parser = subparsers.add_parser("serve", help="Start the local JoRoScope web server and interface")
    serve_parser.add_argument("-p", "--port", type=int, default=8765, help="Port to bind (default: 8765)")
    serve_parser.add_argument("--no-browser", action="store_true", help="Do not automatically launch browser")

    # Chart calculation command
    chart_parser = subparsers.add_parser("chart", help="Calculate horoscope from JSON input file or stdin")
    chart_parser.add_argument("-i", "--input", help="Path to input JSON file containing birth details")
    chart_parser.add_argument("-o", "--output", help="Path to write output JSON")

    args = parser.parse_args()

    if args.command == "serve" or args.command is None:
        port = getattr(args, "port", 8765)
        open_browser = not getattr(args, "no_browser", False)
        run_server(port=port, open_browser=open_browser)
    elif args.command == "chart":
        if args.input:
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = json.load(sys.stdin)
        result = calculate(data)
        out_json = json.dumps(result, indent=2, ensure_ascii=False)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(out_json)
        else:
            print(out_json)


if __name__ == "__main__":
    main()
