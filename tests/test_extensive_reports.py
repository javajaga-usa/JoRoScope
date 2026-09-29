"""The year-by-year forecast, the six life-area reports and the Pratyantara narrowing of past events."""

import sys
import unittest
from collections import Counter
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from joroscope.core import engine
from joroscope.core.readings.life_areas import LIFE_AREA_KEYS

BIRTHS = [
    dict(date='1990-01-01', time='12:00', timezone='Asia/Kolkata', latitude=13.0827, longitude=80.2707),
    dict(date='1985-06-15', time='08:30', timezone='Asia/Kolkata', latitude=10.5, longitude=76.2),
]


class ExtensiveReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.charts = [engine.calculate(dict(b, name='Test', ayanamsa='Lahiri', lang='ml')) for b in BIRTHS]

    def test_yearly_covers_twelve_years_in_three_languages(self):
        for chart in self.charts:
            ch = chart['predictions']['yearly']
            years = [y['year'] for y in ch['years']]
            self.assertEqual(years, list(range(date.today().year, date.today().year + 12)))
            self.assertEqual(len(ch['cards']), 12)
            for c in ch['cards']:
                for lang in ('en', 'ta', 'ml'):
                    self.assertIn('\n', c['body'][lang])  # one line per part
                self.assertIn('Career', c['body']['en'])
            for y in ch['years']:
                self.assertTrue(y['bhuktis'], y['year'])
                for m in y['good_months'] + y['care_months']:
                    self.assertTrue(m['start'][:4] == m['end'][:4] == str(y['year']) or m['end'] == f"{y['year'] + 1}-01-01")

    def test_yearly_verdicts_separate_better_and_harder_years(self):
        # Years are ranked against each other per area, so no area calls every year alike
        for chart in self.charts:
            years = chart['predictions']['yearly']['years']
            for area in ('career', 'money', 'family', 'health', 'travel'):
                counts = Counter(y['verdicts'][area] for y in years)
                self.assertLess(max(counts.values()), 12, (area, counts))

    def test_life_area_reports(self):
        for chart in self.charts:
            for key in LIFE_AREA_KEYS:
                ch = chart['predictions'][key]
                self.assertEqual(ch['key'], key)
                self.assertIn(ch['verdict'], ('good', 'mixed', 'bad'))
                self.assertGreaterEqual(len(ch['cards']), 2)
                self.assertNotIn(' 1th ', ch['cards'][0]['body']['en'])
                for w in ch['windows']:
                    self.assertLessEqual(w['start'], w['end'])
                    self.assertTrue(w['bhukti'] in ch['significators'])

    def test_past_events_are_narrowed_to_pratyantara_months(self):
        narrowed = 0
        for chart in self.charts:
            for s in chart['predictions']['parisodhanai']['statements']:
                for w in s.get('windows', []):
                    for m in w['months']:
                        self.assertTrue(w['start'] <= m['start'] <= m['end'] <= w['end'])
                        narrowed += 1
        self.assertGreater(narrowed, 0)
