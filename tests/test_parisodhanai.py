"""Parisodhanai (chart verification): sibling counts from the 3rd and 11th houses, parents, and
past event windows that lie between birth and today within the usual ages."""

import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from joroscope.core import engine
from joroscope.core.readings.parisodhanai import EVENT_AGES, sibling_reading

BIRTH = dict(date='1990-01-01', time='12:00', timezone='Asia/Kolkata', latitude=13.0827, longitude=80.2707,
             name='Test', ayanamsa='Lahiri')


class ParisodhanaiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chart = engine.calculate(BIRTH)
        cls.ch = cls.chart['predictions']['parisodhanai']

    def test_statements_are_trilingual_and_graded(self):
        keys = [s['key'] for s in self.ch['statements']]
        self.assertEqual(keys[:4], ['siblings_elder', 'siblings_younger', 'father', 'mother'])
        self.assertEqual(len(keys), len(set(keys)))
        for s in self.ch['statements']:
            for field in ('en', 'ta', 'ml', 'basis_en', 'basis_ta', 'basis_ml'):
                self.assertTrue(s[field], (s['key'], field))
            self.assertIn(s['confidence'], ('strong', 'moderate', 'weak'))

    def test_siblings_follow_the_grahas_linked_to_the_house(self):
        planets = self.chart['planets']
        for house in (3, 11):
            s = sibling_reading(planets, house)
            if s['grahas']:
                self.assertEqual(s['brothers'] + s['sisters'], len(s['grahas']))
        # Capricorn is the 11th from this Pisces Lagna; Mercury, Venus and Rahu there are read as three sisters
        elder = sibling_reading(planets, 11)
        self.assertEqual((elder['brothers'], elder['sisters']), (0, 3))

    def test_event_windows_are_past_and_within_usual_ages(self):
        birth = datetime(1990, 1, 1, 6, 30, tzinfo=timezone.utc)
        today = datetime.now(timezone.utc).date().isoformat()
        for s in self.ch['statements']:
            if not s.get('event'):
                continue
            self.assertIn(s['confidence'], ('moderate', 'weak'))  # dasa timing is never "strong"
            low, high = EVENT_AGES[s['event']]
            for w in s['windows']:
                self.assertLessEqual(w['end'], today)
                self.assertGreaterEqual(w['start'], birth.date().isoformat())
                self.assertLessEqual(low - 1, w['age_to'])
                self.assertLessEqual(w['age_from'], high + 1)
