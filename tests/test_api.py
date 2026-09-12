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
            self.assertEqual(data.get("version"), "2.0.0")

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


if __name__ == "__main__":
    unittest.main()
