"""Unit Tests for Multi-Profile Serialization & Lifecycle
"""

import unittest
import json
import uuid
from datetime import datetime


class ProfileLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.sample_profiles = [
            {
                "id": str(uuid.uuid4()),
                "name": "Sri Raman",
                "date": "1990-01-01",
                "time": "12:00:00",
                "city": "Chennai (Madras)",
                "latitude": 13.0827,
                "longitude": 80.2707,
                "timezone": "Asia/Kolkata",
                "ayanamsa": "Lahiri",
                "lagna": "Pisces",
                "moon_sign": "Aquarius",
                "nakshatra": "Shatabhisha",
                "nakshatra_idx": 23,
                "sign_idx": 10,
                "pada": 1,
                "created_at": datetime.now().isoformat()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Kalyani Devi",
                "date": "1994-05-18",
                "time": "08:30:00",
                "city": "Madurai",
                "latitude": 9.9252,
                "longitude": 78.1198,
                "timezone": "Asia/Kolkata",
                "ayanamsa": "Lahiri",
                "lagna": "Gemini",
                "moon_sign": "Leo",
                "nakshatra": "Magha",
                "nakshatra_idx": 9,
                "sign_idx": 4,
                "pada": 2,
                "created_at": datetime.now().isoformat()
            }
        ]

    def test_profile_export_schema(self):
        payload = {
            "version": 2,
            "app": "JoRoScope",
            "exported_at": datetime.now().isoformat(),
            "profiles": self.sample_profiles
        }
        json_str = json.dumps(payload)
        parsed = json.loads(json_str)

        self.assertEqual(parsed["version"], 2)
        self.assertEqual(parsed["app"], "JoRoScope")
        self.assertEqual(len(parsed["profiles"]), 2)
        self.assertEqual(parsed["profiles"][0]["name"], "Sri Raman")

    def test_profile_deduplication_on_import(self):
        existing = list(self.sample_profiles)
        incoming = [
            # Exact duplicate of Raman
            dict(self.sample_profiles[0]),
            # New person
            {
                "id": str(uuid.uuid4()),
                "name": "Vikramaditya",
                "date": "1988-11-22",
                "time": "18:45:00",
                "city": "Coimbatore",
                "latitude": 11.0168,
                "longitude": 76.9558,
                "timezone": "Asia/Kolkata",
                "ayanamsa": "Lahiri"
            }
        ]

        merged = list(existing)
        added_count = 0
        for p in incoming:
            is_dup = any(
                (ep["id"] == p["id"]) or
                (ep["name"].lower() == p["name"].lower() and ep["date"] == p["date"] and ep["time"] == p["time"])
                for ep in merged
            )
            if not is_dup:
                merged.append(p)
                added_count += 1

        self.assertEqual(added_count, 1)
        self.assertEqual(len(merged), 3)
        self.assertEqual(merged[-1]["name"], "Vikramaditya")


if __name__ == "__main__":
    unittest.main()
