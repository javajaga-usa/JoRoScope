"""JoRoScope Local HTTP Application & API Server
Serves the local SPA frontend and responds to JSON calculation endpoints.
Zero external tracking — 100% private and offline capable.
"""

import json
import mimetypes
import sys
import webbrowser
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlsplit, unquote

try:
    from .core.engine import calculate, calculate_match
    from .core.south_indian import daily_panchangam
except (ImportError, ValueError):
    from core.engine import calculate, calculate_match
    from core.south_indian import daily_panchangam

MODULE_DIR = Path(__file__).resolve().parent
# Locate web assets directory
if (MODULE_DIR / 'web').is_dir():
    WEB_DIR = MODULE_DIR / 'web'
elif (MODULE_DIR.parent.parent / 'web').is_dir():
    WEB_DIR = MODULE_DIR.parent.parent / 'web'
else:
    WEB_DIR = MODULE_DIR / 'web'


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def send(self, body, status=200, kind='application/json; charset=utf-8'):
        self.send_response(status)
        self.send_header('Content-Type', kind)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        name = unquote(urlsplit(self.path).path)
        if name == '/api/health':
            self.send(b'{"application":"joroscope","version":"2.0.0","status":"healthy"}')
            return
        if name == '/':
            name = '/index.html'

        file_path = (WEB_DIR / name.lstrip('/')).resolve()
        if not file_path.is_relative_to(WEB_DIR.resolve()) or not file_path.is_file():
            self.send(b'Not found', 404, 'text/plain')
            return

        content_type = mimetypes.guess_type(str(file_path))[0] or 'application/octet-stream'
        self.send(file_path.read_bytes(), kind=content_type)

    def do_POST(self):
        req_path = urlsplit(self.path).path
        if req_path not in ('/api/chart', '/api/match', '/api/panchangam'):
            self.send(b'{}', 404)
            return

        origin = self.headers.get('Origin')
        if origin and origin != f'http://{self.headers.get("Host")}':
            self.send(b'{"error":"Origin rejected"}', 403)
            return

        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= 65536:
                raise ValueError('Invalid request size.')
            data = json.loads(self.rfile.read(length))

            if req_path == '/api/chart':
                result = calculate(data)
                self.send(json.dumps(result, ensure_ascii=False, allow_nan=False).encode())
            elif req_path == '/api/match':
                boy = data.get('boy')
                girl = data.get('girl')
                if not boy or not girl:
                    raise ValueError('Both boy and girl data are required for matchmaking.')
                boy_chart = calculate(boy) if 'date' in boy else boy
                girl_chart = calculate(girl) if 'date' in girl else girl
                match_result = calculate_match(boy_chart, girl_chart)
                self.send(json.dumps(match_result, ensure_ascii=False, allow_nan=False).encode())
            elif req_path == '/api/panchangam':
                tz_str = data.get('timezone', 'Asia/Kolkata')
                try:
                    now_local = datetime.now(ZoneInfo(tz_str))
                except ZoneInfoNotFoundError:
                    raise ValueError('Enter a valid IANA timezone, such as Asia/Kolkata.')
                natal_star = data.get('natal_nakshatra_index')
                natal_sign = data.get('natal_sign_index')
                # No date: right now. A date without a time: at that day's sunrise.
                if data.get('date'):
                    date_str, time_str = data['date'], data.get('time')
                else:
                    date_str, time_str = now_local.strftime('%Y-%m-%d'), now_local.strftime('%H:%M:%S')
                panch = daily_panchangam(
                    date_str,
                    time_str,
                    tz_str,
                    float(data.get('latitude', 13.0827)),
                    float(data.get('longitude', 80.2707)),
                    natal_star=None if natal_star in (None, '') else int(natal_star),
                    natal_sign=None if natal_sign in (None, '') else int(natal_sign)
                )
                self.send(json.dumps(panch, ensure_ascii=False, allow_nan=False).encode())
        except Exception as err:
            self.send(json.dumps({'error': str(err)}).encode(), 400)


def run_server(port=8765, open_browser=True):
    # Try preferred port, fallback to sequential ports if occupied
    server = None
    actual_port = port
    for p in range(port, port + 10):
        try:
            server = HTTPServer(('127.0.0.1', p), Handler)
            actual_port = p
            break
        except OSError:
            continue

    if not server:
        raise RuntimeError(f"Could not bind HTTP server to any port from {port} to {port + 9}")

    url = f"http://127.0.0.1:{actual_port}"
    print(f"============================================================")
    print(f"  JoRoScope v2.0 — Modern Precision Vedic Astrology")
    print(f"  Live at: {url}")
    print(f"  Web root: {WEB_DIR}")
    print(f"============================================================")

    if open_browser:
        try:
            webbrowser.open(url)
        except Exception:
            pass

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down JoRoScope server gracefully.")
    finally:
        server.server_close()


def main():
    args = sys.argv[1:]
    port = 8765
    open_browser = '--no-browser' not in args

    for a in args:
        if a.isdigit():
            port = int(a)

    run_server(port=port, open_browser=open_browser)


if __name__ == '__main__':
    main()
