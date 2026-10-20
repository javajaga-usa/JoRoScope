"""The trust features: chance baselines and year ratings in the accuracy report, the public figures,
the past-years forecast with its factor lines and sources, the citations in Chart Verification and
the check-yourself facts of the panchangam."""
import json
import os
import sys
import tempfile
import threading
import unittest
import urllib.request
from datetime import datetime, timezone
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from joroscope.core import feedback
from joroscope.core.engine import calculate
from joroscope.core.readings.yearly import AREAS, calculate_past_years, calculate_yearly_forecast, past_years_range
from joroscope.core.south_indian import daily_panchangam
from joroscope.server import Handler

BIRTH = dict(name='Trust', date='1980-05-05', time='06:30:00', timezone='Asia/Kolkata', latitude=13.0827,
             longitude=80.2707, ayanamsa='Lahiri')
NOW = datetime(2026, 10, 17, tzinfo=timezone.utc)


class YearlyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chart = calculate(BIRTH)

    def test_factors_explain_every_point(self):
        yearly = self.chart['predictions']['yearly']
        self.assertEqual(len(yearly['sources']), 3)
        for year, card in zip(yearly['years'], yearly['cards']):
            self.assertEqual(card['year'], year['year'])
            self.assertEqual([w['area'] for w in card['why']], [k for k, _, _ in AREAS])
            for w in card['why']:
                total = round(sum(f['points'] for f in w['items']), 1)
                self.assertAlmostEqual(total, year['scores'][w['area']], delta=0.06, msg=(year['year'], w['area']))
                for f in w['items']:
                    self.assertTrue(f['en'] and f['ta'] and f['ml'])

    def test_past_years_cover_memory_and_rank_among_themselves(self):
        past = calculate_past_years(self.chart, now=NOW)
        self.assertEqual(past['key'], 'yearly_past')
        self.assertEqual((past['years'][0]['year'], past['years'][-1]['year']), (1995, 2025))  # from age 15 to last year
        self.assertEqual(set(y['level'] for y in past['years']) <= {'good', 'steady', 'care'}, True)
        self.assertIn('good', [y['level'] for y in past['years']])
        self.assertIn('care', [y['level'] for y in past['years']])
        # Overlapping years give the same raw scores as the forward forecast; only the ranking differs
        forward = calculate_yearly_forecast(self.chart, now=datetime(2020, 6, 1, tzinfo=timezone.utc))
        fwd_2022 = next(y for y in forward['years'] if y['year'] == 2022)
        past_2022 = next(y for y in past['years'] if y['year'] == 2022)
        self.assertEqual(fwd_2022['scores'], past_2022['scores'])
        self.assertEqual(fwd_2022['bhuktis'], past_2022['bhuktis'])

    def test_past_years_range(self):
        young = calculate(dict(BIRTH, date='2015-03-01'))
        self.assertEqual(list(past_years_range(young, NOW)), list(range(2016, 2026)))  # too young for age 15: from the year after birth
        self.assertIsNone(past_years_range(calculate(dict(BIRTH, date='2025-03-01')), NOW))
        self.assertIsNone(calculate_past_years(calculate(dict(BIRTH, date='2025-03-01')), now=NOW))


class ParisodhanaiSourceTests(unittest.TestCase):
    def test_every_statement_cites_its_source(self):
        ch = calculate(BIRTH)['predictions']['parisodhanai']
        self.assertEqual(len(ch['sources']), 3)
        for s in ch['statements']:
            self.assertTrue(s['source_en'] and s['source_ta'] and s['source_ml'], s['key'])
            self.assertIn('Parashara', s['source_en'])


class CheckPointTests(unittest.TestCase):
    def test_moon_phases_sankranti_and_eclipses(self):
        cp = daily_panchangam('2026-10-17', '10:00', 'Asia/Kolkata', 13.0827, 80.2707)['check_points']
        self.assertEqual([p['kind'] for p in cp['phases']], ['full_moon', 'new_moon'])
        self.assertEqual(cp['phases'][0]['when_local'][:10], '2026-10-26')  # Pournami, Drik Panchang: Oct 25/26 2026
        self.assertEqual(cp['phases'][1]['when_local'][:10], '2026-11-09')  # Amavasai, Drik Panchang: Nov 8/9 2026
        self.assertEqual((cp['sankranti']['sign'], cp['sankranti']['month']), ('Libra', 'Aippasi'))
        self.assertEqual(cp['sankranti']['when_local'][:10], '2026-10-17')
        self.assertTrue(0 <= cp['moon_illumination_pct'] <= 100)
        self.assertTrue(cp['waxing'])
        self.assertEqual(cp['solar_eclipse']['when_utc'][:10], '2027-02-06')  # annular eclipse of 6 Feb 2027
        self.assertTrue(cp['solar_eclipse']['annular'])
        self.assertEqual(cp['lunar_eclipse']['when_utc'][:10], '2027-02-20')  # penumbral eclipse of 20 Feb 2027


class AccuracyBaselineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.env = mock.patch.dict(os.environ, {'JOROSCOPE_DATA_DIR': cls.tmp.name, 'JOROSCOPE_OWNER_PASSCODE': 'owner-7'})
        cls.env.start()
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.url = f'http://127.0.0.1:{cls.server.server_port}'
        cls.chart = calculate(BIRTH)
        cls.statements = cls.chart['predictions']['parisodhanai']['statements']

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.env.stop()
        cls.tmp.cleanup()

    def get(self, route):
        with urllib.request.urlopen(self.url + route) as resp:
            return json.loads(resp.read())

    def test_coverage_is_the_share_of_eligible_years(self):
        marriage = next(s for s in self.statements if s.get('event') == 'marriage')
        cov, months = feedback.coverage(self.chart, marriage, now=NOW)
        windows_days = sum((datetime.fromisoformat(w['end']) - datetime.fromisoformat(w['start'])).days for w in marriage['windows'])
        eligible_days = 365.25 * (45 - 18)  # marriage is judged between 18 and 45, all in the past for a 1980 birth
        self.assertAlmostEqual(cov, windows_days / eligible_days, places=3)
        self.assertTrue(0 < months <= cov < 1)

    def test_entry_and_report_carry_baselines_lift_and_year_ratings(self):
        marriage = next(s for s in self.statements if s.get('event') == 'marriage')
        inside = marriage['windows'][0]['start']
        marks = {'event_marriage': {'mark': 'right', 'date': inside}, 'years': {'2010': 'matched', '2011': 'no', '2012': 'partly', '1800': 'matched', '2013': 'x'}}
        entry = feedback.entry_from_marks(self.chart, marks, 'trust-entry-1')
        item = entry['items'][0]
        self.assertTrue(item['in_window'])
        self.assertTrue(0 < item['coverage'] < 1)
        self.assertEqual(len(entry['years']), 3)  # the unknown year and the unknown mark are dropped
        self.assertEqual({y['mark'] for y in entry['years']}, {'matched', 'no', 'partly'})
        self.assertTrue(all(y['level'] in ('good', 'steady', 'care') and 'year' not in y for y in entry['years']))
        feedback.save(entry)
        r = feedback.report()
        row = next(s for s in r['statements'] if s['key'] == 'event_marriage')
        self.assertEqual(row['in_window_pct'], 100)
        self.assertEqual(row['baseline_pct'], round(100 * item['coverage']))
        self.assertAlmostEqual(row['lift'], round(100 / row['baseline_pct'], 1), places=1)
        self.assertEqual(sum(y['count'] for y in r['years']), 3)
        # Only year ratings: still a valid entry
        self.assertEqual(feedback.entry_from_marks(self.chart, {'years': {'2010': 'matched'}}, 'trust-entry-2')['items'], [])

    def test_public_report_hides_small_groups(self):
        for i in range(25):
            feedback.save(dict(id=f'public-{i:02d}', date='2026-10-17', version='x',
                               items=[dict(key='siblings_elder', topic='siblings', confidence='strong', mark='right' if i % 5 else 'wrong'),
                                      dict(key='father', topic='parents', confidence='weak', mark='right')] if i < 10 else
                               [dict(key='siblings_elder', topic='siblings', confidence='strong', mark='right')],
                               siblings=[], years=[dict(level='good', mark='matched')]))
        public = feedback.public_report()
        self.assertEqual([s['key'] for s in public['statements']], ['siblings_elder'])  # 'father' has only 10 marks
        self.assertGreaterEqual(public['years'][0]['count'], 25)  # plus any ratings an earlier test shared
        self.assertEqual(public['confidence'][0]['level'], 'strong')
        via_http = self.get('/api/accuracy')  # no passcode needed
        self.assertEqual(via_http['min_n'], 20)
        self.assertEqual([s['key'] for s in via_http['statements']], ['siblings_elder'])
        self.assertNotIn('father', json.dumps(via_http))


if __name__ == '__main__':
    unittest.main()
