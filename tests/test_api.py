"""API Integration Tests for JoRoScope
Verifies HTTP endpoints (/api/health, /api/chart, /api/match, /api/panchangam).
"""

import unittest
import json
import threading
import sys
from pathlib import Path
from http.server import HTTPServer
import urllib.request

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from joroscope.server import Handler


class ApiIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(('127.0.0.1', 0), Handler)
        cls.port = cls.server.server_port
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_health_endpoint(self):
        url = f"http://127.0.0.1:{self.port}/api/health"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode())
            self.assertEqual(data.get("application"), "joroscope")
            self.assertEqual(data.get("version"), "2.6.0")

    def test_chart_endpoint(self):
        url = f"http://127.0.0.1:{self.port}/api/chart"
        payload = {
            "name": "API Test",
            "date": "1990-01-01",
            "time": "12:00:00",
            "city": "Chennai",
            "latitude": 13.0827,
            "longitude": 80.2707,
            "timezone": "Asia/Kolkata",
            "ayanamsa": "Lahiri"
        }
        body = json.dumps(payload).encode()
        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode())
            self.assertIn("planets", data)
            self.assertIn("vargas", data)
            self.assertIn("predictions", data)
            self.assertIn("shadbala", data["predictions"])

    def test_timeline_details_are_deferred_and_gzipped(self):
        import gzip
        payload = json.dumps({"name": "API Test", "date": "1990-01-01", "time": "12:00:00", "latitude": 13.0827,
                              "longitude": 80.2707, "timezone": "Asia/Kolkata", "ayanamsa": "Lahiri"}).encode()
        headers = {"Content-Type": "application/json", "Accept-Encoding": "gzip"}
        req = urllib.request.Request(f"http://127.0.0.1:{self.port}/api/chart", data=payload, headers=headers)
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.headers.get("Content-Encoding"), "gzip")
            raw = gzip.decompress(resp.read())
        chart = json.loads(raw)
        self.assertLess(len(raw), 800_000)  # a guard against runaway growth; about 770 KB, with the long chapters deferred
        periods = chart["predictions"]["timeline_predictions"]["periods"]
        deferred = [p for p in periods if p.get("details_deferred")]
        self.assertGreater(len(deferred), 70)
        self.assertTrue(all("career_en" not in p for p in deferred))
        req = urllib.request.Request(f"http://127.0.0.1:{self.port}/api/timeline", data=payload,
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as resp:
            self.assertIsNone(resp.headers.get("Content-Encoding"))
            details = json.loads(resp.read())["details"]
        self.assertEqual(set(details), {p["id"] for p in periods})
        self.assertTrue(all(d["remedy_ta"] and d["career_en"] for d in details.values()))

    def test_match_endpoint(self):
        url = f"http://127.0.0.1:{self.port}/api/match"
        payload = {
            "boy": {"nakshatra_index": 0, "sign_index": 0},
            "girl": {"nakshatra_index": 23, "sign_index": 10}
        }
        body = json.dumps(payload).encode()
        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode())
            self.assertIn("guna_milan", data)
            self.assertIn("poruthams", data)
            self.assertIn("verdict", data)

    def test_panchangam_endpoint(self):
        url = f"http://127.0.0.1:{self.port}/api/panchangam"
        payload = {
            "date": "2026-09-12",
            "time": "12:00:00",
            "latitude": 13.0827,
            "longitude": 80.2707,
            "timezone": "Asia/Kolkata"
        }
        body = json.dumps(payload).encode()
        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode())
            self.assertIn("tithi_name", data)
            self.assertIn("nakshatra", data)
            self.assertIn("yoga_name", data)

    def test_origin_check(self):
        """Requests from the server's own host pass over http or https (a tunnel); other sites are refused."""
        url = f"http://127.0.0.1:{self.port}/api/panchangam"
        body = json.dumps({"date": "2026-09-12", "timezone": "Asia/Kolkata"}).encode()
        host = f"127.0.0.1:{self.port}"
        for origin, status in ((f"http://{host}", 200), (f"https://{host}", 200), ("https://evil.example", 403)):
            req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json", "Origin": origin})
            try:
                with urllib.request.urlopen(req) as resp:
                    code = resp.status
            except urllib.error.HTTPError as err:
                code = err.code
            self.assertEqual(code, status, origin)


if __name__ == "__main__":
    unittest.main()
