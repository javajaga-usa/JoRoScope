"""JoRoScope Local HTTP Application & API Server
Serves the local SPA frontend and responds to JSON calculation endpoints.
Zero external tracking — 100% private and offline capable.
"""

import gzip
import json
import mimetypes
import sys
import threading
import time
import webbrowser
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit, unquote

from . import __version__
from .core import ai
from .core.engine import calculate, calculate_match
from .core.south_indian import daily_panchangam, month_calendar
from .core.muhurtham import find_muhurthams
from .core.prasna import calculate_prasna
from .core.rectification import rectify
from .core.timeline import defer_timeline_details, timeline_details

MODULE_DIR = Path(__file__).resolve().parent
# Locate web assets directory
if (MODULE_DIR / 'web').is_dir():
    WEB_DIR = MODULE_DIR / 'web'
elif (MODULE_DIR.parent.parent / 'web').is_dir():
    WEB_DIR = MODULE_DIR.parent.parent / 'web'
else:
    WEB_DIR = MODULE_DIR / 'web'

# Requests are served in parallel so a slow AI answer does not hold up everyone else, but the Swiss
# Ephemeris keeps global settings (the ayanamsa), so calculations still run one at a time.
COMPUTE_LOCK = threading.Lock()
FORWARDING_HEADERS = ('Cf-Connecting-IP', 'X-Forwarded-For', 'Forwarded')
# The longest report chapters leave the chart response and are fetched from /api/chapters when the page
# first needs them, so the first screen arrives sooner on a phone
DEFERRED_CHAPTERS = ('yearly', 'monthly', 'education', 'children', 'health', 'wealth', 'foreign', 'spiritual')


def strip_malayalam(value):
    """Drop the Malayalam texts ("_ml" fields, and "ml" beside "en") from a response for pages
    that are not showing Malayalam; they would add about a third to a chart."""
    if isinstance(value, list):
        return [strip_malayalam(v) for v in value]
    if isinstance(value, dict):
        return {k: strip_malayalam(v) for k, v in value.items()
                if not k.endswith('_ml') and not (k == 'ml' and 'en' in value)}
    return value


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def send(self, body, status=200, kind='application/json; charset=utf-8'):
        compress = len(body) > 2048 and 'gzip' in self.headers.get('Accept-Encoding', '') and \
            kind.split('/')[0] in ('application', 'text')
        if compress:
            body = gzip.compress(body, compresslevel=6)
        self.send_response(status)
        self.send_header('Content-Type', kind)
        if compress:
            self.send_header('Content-Encoding', 'gzip')
            self.send_header('Vary', 'Accept-Encoding')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        name = unquote(urlsplit(self.path).path)
        if name == '/api/ai-status':
            self.send(json.dumps(ai.status(self.is_local())).encode())
            return
        if name == '/api/health':
            self.send(json.dumps({'application': 'joroscope', 'version': __version__, 'status': 'healthy'}).encode())
            return
        if name == '/':
            name = '/index.html'

        file_path = (WEB_DIR / name.lstrip('/')).resolve()
        if not file_path.is_relative_to(WEB_DIR.resolve()) or not file_path.is_file():
            self.send(b'Not found', 404, 'text/plain')
            return

        content_type = mimetypes.guess_type(str(file_path))[0] or 'application/octet-stream'
        self.send(file_path.read_bytes(), kind=content_type)

    def is_local(self):
        """A request made on this computer itself, not relayed through a tunnel or proxy."""
        host = (self.headers.get('Host') or '').rsplit(':', 1)[0].strip('[]')
        return (self.client_address[0] in ('127.0.0.1', '::1') and host in ('localhost', '127.0.0.1', '::1')
                and not any(self.headers.get(h) for h in FORWARDING_HEADERS))

    def ask(self, data):
        local = self.is_local()
        if not ai.status(local)['enabled']:
            self.send(json.dumps({'error': 'AI answers are not set up on this server.'}).encode(), 503)
            return
        if not ai.authorised(data.get('passcode'), local):
            time.sleep(1)  # slows guessing
            message = ('Wrong passcode.' if ai.passcode() else
                       'Questions are available only on the computer running JoRoScope until a passcode is set.')
            self.send(json.dumps({'error': message}).encode(), 401)
            return
        with COMPUTE_LOCK:
            chart = calculate(data.get('birth') or {})
            sheet = ai.fact_sheet(chart, data.get('marks') or {})
        try:
            result = ai.ask(sheet, data.get('question'), data.get('history'), data.get('lang') or 'en', data.get('mode') or 'question')
        except ai.AiError as err:
            self.send(json.dumps({'error': str(err)}).encode(), 502)
            return
        self.send(json.dumps(result, ensure_ascii=False).encode())

    def chat_prompt(self, data):
        """The prompt to paste into Claude: no AI call and no cost, so no passcode."""
        with COMPUTE_LOCK:
            chart = calculate(data.get('birth') or {})
            sheet = ai.fact_sheet(chart, data.get('marks') or {})
        try:
            prompt = ai.chat_prompt(sheet, data.get('question'), data.get('lang') or 'en', data.get('mode') or 'question')
        except ai.AiError as err:
            self.send(json.dumps({'error': str(err)}).encode(), 400)
            return
        self.send(json.dumps({'prompt': prompt}, ensure_ascii=False).encode())

    def do_POST(self):
        req_path = urlsplit(self.path).path
        if req_path not in ('/api/chart', '/api/timeline', '/api/match', '/api/panchangam', '/api/calendar', '/api/muhurtham', '/api/prasna', '/api/rectify', '/api/ask', '/api/ai-prompt', '/api/chapters'):
            self.send(b'{}', 404)
            return

        origin = self.headers.get('Origin')
        host = self.headers.get('Host')
        if origin and origin not in (f'http://{host}', f'https://{host}'):  # https when served through a tunnel or proxy
            self.send(b'{"error":"Origin rejected"}', 403)
            return

        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= (262144 if req_path == '/api/ask' else 65536):  # questions carry the conversation so far
                raise ValueError('Invalid request size.')
            data = json.loads(self.rfile.read(length))

            if req_path == '/api/ask':
                self.ask(data)
                return
            if req_path == '/api/ai-prompt':
                self.chat_prompt(data)
                return
            with COMPUTE_LOCK:
                if req_path == '/api/chart':
                    result = calculate(data)
                    timeline = (result.get('predictions') or {}).get('timeline_predictions')
                    if timeline:
                        defer_timeline_details(timeline)
                    pred = result.get('predictions') or {}
                    pred['deferred_chapters'] = [k for k in DEFERRED_CHAPTERS if pred.pop(k, None) is not None]
                    if data.get('lang') != 'ml':
                        result = strip_malayalam(result)
                    self.send(json.dumps(result, ensure_ascii=False, allow_nan=False).encode())
                elif req_path == '/api/chapters':
                    pred = calculate(data).get('predictions') or {}
                    chapters = {k: pred[k] for k in data.get('keys') or DEFERRED_CHAPTERS if k in DEFERRED_CHAPTERS and k in pred}
                    if data.get('lang') != 'ml':
                        chapters = strip_malayalam(chapters)
                    self.send(json.dumps({'chapters': chapters}, ensure_ascii=False, allow_nan=False).encode())
                elif req_path == '/api/timeline':
                    timeline = (calculate(data).get('predictions') or {}).get('timeline_predictions') or {}
                    details = {'details': timeline_details(timeline)}
                    if data.get('lang') != 'ml':
                        details = strip_malayalam(details)
                    self.send(json.dumps(details, ensure_ascii=False, allow_nan=False).encode())
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
                elif req_path == '/api/muhurtham':
                    tz_str = data.get('timezone', 'Asia/Kolkata')
                    try:
                        today = datetime.now(ZoneInfo(tz_str)).strftime('%Y-%m-%d')
                    except ZoneInfoNotFoundError:
                        raise ValueError('Enter a valid IANA timezone, such as Asia/Kolkata.')
                    natal_star = data.get('natal_nakshatra_index')
                    natal_sign = data.get('natal_sign_index')
                    found = find_muhurthams(
                        data.get('event', 'marriage'), data.get('start_date') or today, int(data.get('days', 60)), tz_str,
                        float(data.get('latitude', 13.0827)), float(data.get('longitude', 80.2707)),
                        natal_star=None if natal_star in (None, '') else int(natal_star),
                        natal_sign=None if natal_sign in (None, '') else int(natal_sign))
                    self.send(json.dumps(found, ensure_ascii=False, allow_nan=False).encode())
                elif req_path == '/api/prasna':
                    found = calculate_prasna(
                        data.get('question', 'general'), data.get('date') or '', data.get('time') or '',
                        data.get('timezone', 'Asia/Kolkata'), float(data.get('latitude', 13.0827)), float(data.get('longitude', 80.2707)),
                        arudha=data.get('arudha') or None, ayanamsa=data.get('ayanamsa') or 'Lahiri')
                    self.send(json.dumps(found, ensure_ascii=False, allow_nan=False).encode())
                elif req_path == '/api/rectify':
                    found = rectify(data.get('birth') or {}, data.get('events') or [], data.get('window', 60), data.get('step', 2))
                    self.send(json.dumps(found, ensure_ascii=False, allow_nan=False).encode())
                elif req_path == '/api/calendar':
                    cal = month_calendar(int(data['year']), int(data['month']), data.get('timezone', 'Asia/Kolkata'),
                                         float(data.get('latitude', 13.0827)), float(data.get('longitude', 80.2707)))
                    self.send(json.dumps(cal, ensure_ascii=False, allow_nan=False).encode())
        except Exception as err:
            self.send(json.dumps({'error': str(err)}).encode(), 400)


def run_server(port=8765, open_browser=True):
    # Try preferred port, fallback to sequential ports if occupied
    server = None
    actual_port = port
    for p in range(port, port + 10):
        try:
            server = ThreadingHTTPServer(('127.0.0.1', p), Handler)
            server.daemon_threads = True
            actual_port = p
            break
        except OSError:
            continue

    if not server:
        raise RuntimeError(f"Could not bind HTTP server to any port from {port} to {port + 9}")

    url = f"http://127.0.0.1:{actual_port}"
    print("============================================================")
    print(f"  JoRoScope v{__version__} — Modern Precision Vedic Astrology")
    print(f"  Live at: {url}")
    print(f"  Web root: {WEB_DIR}")
    print("============================================================")

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
