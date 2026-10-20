"""The calculation sheet (every input the engine applied) and the birth-time sensitivity search."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from joroscope.core.calcsheet import birth_time_sensitivity, dms, hms
from joroscope.core.engine import SIGNS, calculate, calculate_vargas, swe

BIRTH = {'name': 'Sheet', 'date': '1990-01-01', 'time': '12:00:00', 'timezone': 'Asia/Kolkata',
         'latitude': 13.0827, 'longitude': 80.2707, 'ayanamsa': 'Lahiri'}


class FormattingTests(unittest.TestCase):
    def test_dms(self):
        self.assertEqual(dms(23.717416985), '23° 43′ 03″')
        self.assertEqual(dms(0), '0° 00′ 00″')
        self.assertEqual(dms(-5.5, signed=True), '-5° 30′ 00″')
        self.assertEqual(dms(29.9999999), '30° 00′ 00″')  # rounds to the second, never 29° 60′

    def test_hms(self):
        self.assertEqual(hms(18.5617), '18:33:42')
        self.assertEqual(hms(24.0), '00:00:00')


class CalculationSheetTests(unittest.TestCase):
    def test_sheet_states_the_inputs(self):
        c = calculate(BIRTH)['calculation']
        self.assertEqual((c['timezone'], c['utc_offset'], c['timezone_abbreviation']), ('Asia/Kolkata', '+05:30', 'IST'))
        self.assertEqual(c['ut'], '1990-01-01 06:30:00')
        self.assertEqual(c['lmt_offset'], '+05:21')  # 80.27° E is 5 h 21 m ahead of Greenwich
        self.assertAlmostEqual(c['clock_ahead_of_lmt_minutes'], 8.9, places=1)
        self.assertEqual(c['ayanamsa_value'], '23° 43′ 03″')
        self.assertEqual(c['lagna_sign'], 'Pisces')
        self.assertIn('Mean node', c['nodes'])
        self.assertIn('Sripati', c['houses'])
        self.assertTrue(c['sunrise'] < '07:00:00' < c['sunset'])
        self.assertGreater(c['delta_t_seconds'], 50)
        self.assertTrue(c['engine'].startswith('Swiss Ephemeris'))

    def test_historical_offsets(self):
        """India kept +06:30 war time in 1942-45; Sri Lanka moved to +06:30 in May 1996, +06:00 that October, and back to +05:30 in 2006."""
        war = calculate(dict(BIRTH, date='1944-06-15', time='10:00:00'))['calculation']
        self.assertEqual((war['utc_offset'], war['ut']), ('+06:30', '1944-06-15 03:30:00'))
        colombo = dict(BIRTH, timezone='Asia/Colombo', latitude=6.93, longitude=79.85, time='10:00:00')
        self.assertEqual(calculate(dict(colombo, date='1996-08-01'))['calculation']['utc_offset'], '+06:30')
        self.assertEqual(calculate(dict(colombo, date='1997-08-01'))['calculation']['utc_offset'], '+06:00')
        self.assertEqual(calculate(dict(colombo, date='2010-08-01'))['calculation']['utc_offset'], '+05:30')


class SensitivityTests(unittest.TestCase):
    def brute_force(self, jd, lat, lon, value_at, limit=1440):
        """Minute-by-minute search for the first change, both ways."""
        base = value_at(jd)
        later = next((m for m in range(1, limit + 1) if value_at(jd + m / 1440) != base), None)
        earlier = next((m for m in range(1, limit + 1) if value_at(jd - m / 1440) != base), None)
        return earlier, later

    def check(self, birth):
        chart = calculate(birth)
        jd, lat, lon = chart['julian_day'], float(birth['latitude']), float(birth['longitude'])
        sens = chart['sensitivity']
        rows = {r['key']: r for r in sens['quantities']}
        lagna = lambda t: swe.houses_ex(t, lat, lon, b'P', swe.FLG_SIDEREAL)[1][0]
        moon = lambda t: swe.calc_ut(t, swe.MOON, swe.FLG_MOSEPH | swe.FLG_SIDEREAL)[0][0] % 360
        checks = {'lagna_sign': lambda t: int(lagna(t) // 30), 'navamsa_lagna': lambda t: calculate_vargas(lagna(t))['D9'],
                  'moon_sign': lambda t: int(moon(t) // 30), 'moon_star': lambda t: int(moon(t) / (40 / 3)),
                  'moon_pada': lambda t: int(moon(t) / (10 / 3))}
        for key, fn in checks.items():
            earlier, later = self.brute_force(jd, lat, lon, fn)
            for side, expected in (('earlier', earlier), ('later', later)):
                got = rows[key][side]
                if expected is None:
                    self.assertIsNone(got, (key, side))
                else:  # the brute force finds the first whole minute past the change; the search is within a tenth of a minute
                    self.assertIsNotNone(got, (key, side))
                    self.assertTrue(expected - 1 <= got <= expected, (key, side, got, expected))
        self.assertEqual(rows['lagna_sign']['value']['en'], chart['planets']['Ascendant']['sign'])
        self.assertEqual(rows['moon_star']['value']['en'], chart['planets']['Moon']['nakshatra'])
        return chart

    def test_matches_brute_force(self):
        self.check(BIRTH)
        self.check(dict(BIRTH, date='1975-11-23', time='04:17:00', latitude=28.61, longitude=77.21))

    def test_sign_labels_are_neighbours(self):
        rows = {r['key']: r for r in calculate(BIRTH)['sensitivity']['quantities']}
        lagna = rows['lagna_sign']
        self.assertEqual(SIGNS[(lagna['value']['index'] + 1) % 12], lagna['after']['en'])
        self.assertEqual(SIGNS[(lagna['value']['index'] - 1) % 12], lagna['before']['en'])

    def test_uncertainty_marks_stability_and_dasa_shift(self):
        sens = calculate(dict(BIRTH, uncertainty='10'))['sensitivity']
        self.assertEqual(sens['uncertainty_minutes'], 10)
        for r in sens['quantities']:
            self.assertEqual(r['stable'], r['margin'] is None or r['margin'] > 10)
        self.assertEqual(sens['unstable'], [r['key'] for r in sens['quantities'] if not r['stable']])
        # The Moon moves about 13° a day: a minute of birth time moves every Dasa date by a day or two
        self.assertTrue(0.5 < sens['dasa_days_per_minute'] < 4)
        self.assertAlmostEqual(sens['dasa_uncertainty_days'], sens['dasa_days_per_minute'] * 10, places=0)
        self.assertNotIn('stable', calculate(BIRTH)['sensitivity']['quantities'][0])  # no uncertainty given
        self.assertIsNone(calculate(dict(BIRTH, uncertainty='abc'))['sensitivity']['uncertainty_minutes'])

    def test_fast(self):
        import time
        chart = calculate(BIRTH)
        t = time.perf_counter()
        birth_time_sensitivity(chart['julian_day'], 13.0827, 80.2707, 365.25, 5)
        self.assertLess(time.perf_counter() - t, 0.5)


if __name__ == '__main__':
    unittest.main()
