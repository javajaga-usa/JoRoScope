"""Timeline Tests
The Dasa-Bhukti ratings come from the chart (house lordship, dignity and the lords' relation),
and the annual view follows the running period and Saturn's cycles, not the calendar year.
"""
import unittest, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from joroscope.core.engine import calculate
from joroscope.core.timeline import calculate_timeline_predictions
from joroscope.core.predictions import generate_lucky_factors, SIGN_LORDS

BIRTHS = [
    {'name': 'A', 'date': '1985-06-15', 'time': '21:40:00', 'timezone': 'Asia/Kolkata', 'latitude': 13.0827, 'longitude': 80.2707},
    {'name': 'B', 'date': '1992-11-03', 'time': '06:10:00', 'timezone': 'Asia/Kolkata', 'latitude': 9.9252, 'longitude': 78.1198},
]


class TimelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.charts = [calculate(dict(b, ayanamsa='Lahiri')) for b in BIRTHS]
        for c in cls.charts:
            c['timeline'] = calculate_timeline_predictions(c)

    def test_ratings_differ_by_chart_and_use_the_whole_scale(self):
        seen = set()
        for c in self.charts:
            periods = c['timeline']['periods']
            self.assertEqual(len(periods), 81)
            seen |= {p['potency'] for p in periods}
            for p in periods:
                self.assertTrue(p['theme_en'] and p['theme_ta'])
        self.assertGreaterEqual(len(seen), 4)
        # The same Dasa-Bhukti pair is not rated identically in every chart
        key = lambda c: {(p['dasa_lord'], p['bhukti_lord']): p['potency'] for p in c['timeline']['periods']}
        a, b = key(self.charts[0]), key(self.charts[1])
        self.assertTrue(any(a[k] != b[k] for k in a))

    def test_swabhukti_wording(self):
        for p in self.charts[0]['timeline']['periods']:
            if p['dasa_lord'] == p['bhukti_lord']:
                self.assertNotIn(f"{p['dasa_lord']} Dasa and {p['dasa_lord']} Bhukti", p['theme_en'])

    def test_annual_scores_follow_the_period(self):
        for c in self.charts:
            gochara_cycles = (c.get('gochara') or {}).get('saturn_cycles', [])
            for yr in c['timeline']['annual_projections']:
                penalty = 6 if yr['saturn_cycle'] in ('sade_sati', 'ashtama') else (3 if yr['saturn_cycle'] else 0)
                period = next(p for p in c['timeline']['periods']
                              if p['dasa_lord'] == yr['dasa_lord'] and p['bhukti_lord'] == yr['bhukti_lord'])
                self.assertEqual(yr['score'], max(40, min(98, 50 + period['potency'] * 9 - penalty)))
            self.assertIsInstance(gochara_cycles, list)

    def test_gems_follow_lagna_and_ninth_lords(self):
        gem_of = {'Sun': 'Ruby', 'Moon': 'Natural Pearl', 'Mars': 'Red Coral', 'Mercury': 'Emerald',
                  'Jupiter': 'Yellow Sapphire', 'Venus': 'Diamond', 'Saturn': 'Blue Sapphire'}
        for lagna in range(12):
            luck = generate_lucky_factors(lagna)
            self.assertEqual(luck['primary_gem'], gem_of[SIGN_LORDS[lagna]], lagna)
            self.assertEqual(luck['fortune_gem'], gem_of[SIGN_LORDS[(lagna + 8) % 12]], lagna)
            self.assertTrue(luck['finger_ta'] and luck['wearing_day_ta'] and luck['gem_basis_ta'])


if __name__ == '__main__':
    unittest.main()
