"""Bilingual completeness and chart-specific prediction tests.
Every Tamil field the UI shows must be free of English words, and the
readings must follow the chart's actual lordships and dignities.
"""
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from joroscope.core.engine import calculate, calculate_match
from joroscope.core.predictions import PLANET_TAMIL

CHARTS = [('1990-01-01', '12:00'), ('1994-05-18', '08:30'), ('1988-11-22', '18:45'), ('2001-07-15', '03:10')]
ENGLISH_WORD = re.compile('[A-Za-z]{3,}')


def chart(date, time):
    return calculate(dict(name='T', date=date, time=time, timezone='Asia/Kolkata',
                          latitude='13.0827', longitude='80.2707', ayanamsa='Lahiri'))


class BilingualTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.charts = [chart(d, t) for d, t in CHARTS]

    def assertTamil(self, text, where):
        self.assertTrue(text, where)
        self.assertEqual(ENGLISH_WORD.findall(text), [], f'{where}: {text[:120]}')

    def test_prediction_readings_are_pure_tamil(self):
        for r in self.charts:
            pred = r['predictions']
            for b in pred['bhavas']:
                self.assertTamil(b['prediction_ta'], f"bhava {b['house']}")
                for f in b['factors']:
                    self.assertTamil(f['ta'], f"bhava {b['house']} factor")
            for p in pred['planets_in_houses']:
                self.assertTamil(p['prediction_ta'], p['planet'])
            self.assertTamil(pred['dasa_forecast']['active_forecast_ta'], 'active dasa')

    def test_every_tamil_field_is_pure_tamil(self):
        def walk(node, path):
            if isinstance(node, dict):
                for key, value in node.items():
                    if isinstance(value, str) and key.endswith('_ta'):
                        words = [w for w in ENGLISH_WORD.findall(value) if w not in ('SAV', 'BAV', 'AmK')]
                        self.assertEqual(words, [], f'{path}.{key}')
                    else:
                        walk(value, f'{path}.{key}')
            elif isinstance(node, list):
                for item in node:
                    walk(item, path)
        for r in self.charts:
            walk(r, 'chart')

    def test_yogas_and_doshas_have_tamil(self):
        for r in self.charts:
            for y in r['yogas']:
                for key in ('name_ta', 'category_ta', 'auspiciousness_ta', 'description_ta'):
                    self.assertTamil(y[key], f"{y['name']} {key}")
            ks = r['doshas']['kaal_sarp']
            self.assertTamil(ks['description_ta'], 'kaal sarp')

    def test_lucky_factors_have_tamil(self):
        luck = self.charts[0]['predictions']['lucky_factors']
        for key in ('primary_gem_ta', 'fortune_gem_ta', 'wearing_day_ta', 'metal_ta', 'finger_ta'):
            self.assertTamil(luck[key], key)
        self.assertNotIn('(', luck['primary_gem'])  # English name only
        for colour in luck['lucky_colors_ta']:
            self.assertTamil(colour, 'colour')

    def test_porutham_descriptions_have_tamil(self):
        m = calculate_match(self.charts[1], self.charts[2])
        self.assertTamil(m['verdict_ta'], 'verdict')
        for p in m['poruthams']:
            self.assertTamil(p['description_ta'], p['name'])


class PredictionLogicTests(unittest.TestCase):
    def test_bhava_factors_follow_lord_dignity(self):
        for d, t in CHARTS:
            r = chart(d, t)
            for b in r['predictions']['bhavas']:
                first = b['factors'][0]
                dignity = r['planets'][b['lord']]['dignity']
                if dignity in ('Debilitated', 'Enemy', 'Great Enemy'):
                    self.assertLess(first['effect'], 0, (b['house'], dignity))
                if dignity in ('Exalted', 'Own Sign', 'Moolatrikona'):
                    self.assertGreater(first['effect'], 0, (b['house'], dignity))
                self.assertEqual(b['score'], sum(f['effect'] for f in b['factors']))
                self.assertIn(b['strength'], ('strong', 'moderate', 'weak'))

    def test_planet_lordships_are_counted_from_lagna(self):
        r = chart('1990-01-01', '12:00')  # Pisces Lagna
        by_planet = {p['planet']: p for p in r['predictions']['planets_in_houses']}
        self.assertEqual(by_planet['Mars']['owned_houses'], [2, 9])
        self.assertEqual(by_planet['Jupiter']['owned_houses'], [1, 10])
        self.assertEqual(by_planet['Sun']['functional_role'], 'malefic')  # 6th lord for Pisces
        self.assertIsNone(by_planet['Rahu']['functional_role'])

    def test_active_dasa_reading_names_both_lords(self):
        r = chart('2001-07-15', '03:10')
        ad = r['active_dasha']
        reading_ta = r['predictions']['dasa_forecast']['active_forecast_ta']
        self.assertIn(PLANET_TAMIL[ad['dasa']], reading_ta)
        self.assertIn(PLANET_TAMIL[ad['bhukti']], reading_ta)
        self.assertIn(ad['bhukti_end'][:10], r['predictions']['dasa_forecast']['active_forecast_en'])


if __name__ == '__main__':
    unittest.main()
