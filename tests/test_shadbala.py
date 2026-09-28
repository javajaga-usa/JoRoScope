"""Shadbala Tests
Checks every component of the six-fold strength against the worked examples in
B.V. Raman's "Graha and Bhava Balas" and V.P. Jain's Shadbala book (values as
tabulated in PyJHora's test suite), and the classical limits of each bala.
"""
import unittest, sys
from pathlib import Path
from datetime import datetime, timedelta, timezone

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from joroscope.core.engine import (
    calculate, calculate_dignity, placement, sripati_bhavas, sun_events, swe, AYAN, GRAHA_BODIES
)
from joroscope.core.shadbala import compute_shadbala, PLANETS

PARTS = ['uchcha', 'saptavargaja', 'ojayugma', 'kendra', 'drekkana', 'dig', 'nathonnatha', 'paksha', 'tribhaga',
         'abda', 'masa', 'vara', 'hora', 'ayana', 'cheshta', 'drik']


def book_chart(date, time, utc_offset, lat, lon, ayanamsa):
    """Shadbala for a birth given with a fixed UTC offset, as the books state it."""
    tz = timezone(timedelta(hours=utc_offset))
    local = datetime.fromisoformat(f'{date}T{time}').replace(tzinfo=tz)
    utc = local.astimezone(timezone.utc)
    jd = swe.julday(utc.year, utc.month, utc.day, utc.hour + utc.minute / 60 + utc.second / 3600)
    swe.set_sid_mode(AYAN[ayanamsa])
    planets = {}
    for name, body in GRAHA_BODIES:
        pos = swe.calc_ut(jd, body, swe.FLG_MOSEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED)[0]
        planets[name] = placement(pos[0], pos[3])
    planets['Ascendant'] = placement(swe.houses_ex(jd, lat, lon, b'P', swe.FLG_SIDEREAL)[1][0])
    for name, p in planets.items():
        if name != 'Ascendant':
            p['dignity'] = calculate_dignity(name, p['sign_index'], p['degree'], planets)
    madhya, _ = sripati_bhavas(jd, lat, lon)
    civil = local.date()
    events = sun_events(civil, tz, lat, lon)
    if jd < events['sunrise']:
        civil -= timedelta(days=1)
        events = sun_events(civil, tz, lat, lon)
    events['prev_sunset'] = sun_events(civil - timedelta(days=1), tz, lat, lon)['sunset']
    return compute_shadbala(planets, jd, events, civil, madhya, swe.get_ayanamsa_ut(jd))


class ShadbalaBookExampleTests(unittest.TestCase):
    def assert_close(self, result, expected, tolerance, skip=()):
        for part, values in expected.items():
            for planet, value in zip(PLANETS, values):
                if (part, planet) in skip:
                    continue
                with self.subTest(part=part, planet=planet):
                    self.assertAlmostEqual(result[planet][part], value, delta=tolerance)

    def test_bv_raman_example(self):
        """Graha and Bhava Balas: 16 Oct 1918, 14:22:16 IST, 13N 77E35, Raman ayanamsa."""
        result = book_chart('1918-10-16', '14:22:16', 5.5, 13, 77 + 35 / 60, 'Raman')
        expected = dict(
            uchcha=[3.0, 32.75, 37.06, 54.5, 56.33, 1.95, 34.08],
            saptavargaja=[90, 48.75, 90, 135, 71.25, 116.25, 97.5],
            ojayugma=[30, 15, 15, 30, 15, 30, 15], kendra=[60, 30, 30, 60, 15, 15, 30],
            drekkana=[15, 0, 0, 0, 0, 15, 0], dig=[48.10, 31.56, 64.30, 21.09, 11.50, 15.15, 58.02],
            nathonnatha=[48.32, 11.68, 11.68, 60, 48.32, 48.32, 11.68],
            paksha=[16.54, 86.92, 16.54, 16.54, 43.46, 43.46, 16.54], tribhaga=[0, 0, 0, 0, 60, 0, 60],
            abda=[0, 0, 0, 0, 0, 0, 15], masa=[0, 0, 0, 30, 0, 0, 0], vara=[0, 0, 0, 45, 0, 0, 0],
            hora=[0, 60, 0, 0, 0, 0, 0], ayana=[38.12, 43.44, 1.84, 41.25, 59.4, 23.75, 13.75],
            cheshta=[0, 0, 22.23, 2.3, 35.26, 5.95, 21.14], drik=[15.86, -21.73, 0.95, 15.64, -16.04, 18.47, 7.21])
        # Mars's tabulated Dig Bala (64.30) exceeds the classical maximum of 60: its 193° arc
        # from the 4th madhya was not folded to 167°.
        self.assert_close(result, expected, 1.0, skip={('dig', 'Mars')})
        self.assertAlmostEqual(result['Mars']['dig'], (360 - 64.30 * 3) / 3, delta=1.0)
        rupas = [7.07, 6.5, 5.1, 8.95, 7.23, 6.27, 6.49]
        for planet, value in zip(PLANETS, rupas):
            with self.subTest(planet=planet):
                self.assertAlmostEqual(result[planet]['rupas'], value, delta=0.05 if planet != 'Mars' else 0.2)

    def test_vp_jain_example(self):
        """V.P. Jain: 13 Sep 1981, 01:30 IST, 28N39 77E13, Lahiri ayanamsa."""
        result = book_chart('1981-09-13', '01:30:00', 5.5, 28 + 39 / 60, 77 + 13 / 60, 'Lahiri')
        expected = dict(
            uchcha=[14.54, 32.17, 4.94, 58.16, 34.85, 3.09, 48.81],
            saptavargaja=[127.5, 30, 135, 120, 58.13, 150, 82.5], ojayugma=[15, 0, 15, 0, 0, 15, 0],
            dig=[6.59, 12.22, 20.99, 31.97, 31.99, 53.29, 26.67], nathonnatha=[6.1, 53.9, 53.9, 60.0, 6.1, 6.1, 53.9],
            paksha=[5.62, 108.76, 5.62, 54.38, 54.38, 54.38, 5.62], tribhaga=[0, 0, 0, 0, 60, 60, 0],
            abda=[0, 0, 15, 0, 0, 0, 0], masa=[0, 0, 30, 0, 0, 0, 0], vara=[0, 0, 0, 0, 0, 0, 45],
            hora=[0, 0, 0, 60, 0, 0, 0], ayana=[70.08, 43.19, 53.56, 37.10, 22.94, 15.41, 35.04],
            kaala=[81.80, 205.85, 158.08, 210.68, 144.22, 135.89, 139.56],
            cheshta=[0, 0, 20.93, 28.76, 8.43, 28.18, 5.05], drik=[11.24, -0.32, -5.10, 4.29, 4.32, -2.86, 5.82])
        # The book counts the whole of Leo and Virgo as the Sun's and Mercury's Moolatrikona;
        # BPHS limits it to Leo 0-20 and Virgo 15-20, so the Sun (Leo 26) and Mercury
        # (Virgo 20.5) score own-sign 30 instead of 45 in the Rasi.
        self.assert_close(result, expected, 1.0, skip={('saptavargaja', 'Sun'), ('saptavargaja', 'Mercury')})
        self.assertEqual(result['Sun']['saptavargaja'], 127.5 - 15)
        self.assertEqual(result['Mercury']['saptavargaja'], 120 - 15)
        # Mercury and Jupiter are 4' apart; Jupiter, north of the ecliptic, wins the war
        self.assertLess(result['Mercury']['yuddha'], 0)
        self.assertAlmostEqual(result['Jupiter']['yuddha'], -result['Mercury']['yuddha'])
        rupas = [5.52, 5.78, 6.62, 9.00, 6.27, 7.59, 6.54]
        for planet, value in zip(PLANETS, rupas):
            with self.subTest(planet=planet):
                delta = 0.3 if planet in ('Sun', 'Mercury') else 0.05
                self.assertAlmostEqual(result[planet]['rupas'], value, delta=delta)


class ShadbalaLimitTests(unittest.TestCase):
    def test_components_stay_within_classical_limits(self):
        chart = calculate({'name': 'Limits', 'date': '1990-01-01', 'time': '12:00:00', 'timezone': 'Asia/Kolkata',
                           'latitude': 13.0827, 'longitude': 80.2707, 'ayanamsa': 'Lahiri'})
        for row in chart['predictions']['shadbala']['planets']:
            parts = row['components']
            for part in ('uchcha', 'nathonnatha', 'tribhaga', 'hora', 'cheshta'):
                self.assertTrue(0 <= parts[part] <= 60, (row['planet'], part, parts[part]))
            self.assertTrue(0 <= row['dig_bala'] <= 60)
            self.assertTrue(0 <= row['ishta_phala'] <= 60 and 0 <= row['kashta_phala'] <= 60)
            self.assertAlmostEqual(row['total_rupas'] * 60, row['total_virupas'], delta=0.5)
        # Monday noon in Chennai: the sixth hora from sunrise is Venus's, the day's second third the Sun's
        by = {row['planet']: row for row in chart['predictions']['shadbala']['planets']}
        self.assertEqual(by['Venus']['components']['hora'], 60)
        self.assertEqual(by['Moon']['components']['vara'], 45)
        self.assertEqual(by['Sun']['components']['tribhaga'], 60)
        self.assertEqual(by['Jupiter']['components']['tribhaga'], 60)

    def test_readings_are_bilingual(self):
        chart = calculate({'name': 'Tamil', 'date': '1985-06-15', 'time': '21:40:00', 'timezone': 'Asia/Kolkata',
                           'latitude': 9.9252, 'longitude': 78.1198, 'ayanamsa': 'Lahiri'})
        sb = chart['predictions']['shadbala']
        self.assertIn('ஷட்பல', sb['summary_ta'])
        for row in sb['planets']:
            self.assertIn('இஷ்ட பலன்', row['reading_ta'])
            self.assertIn('Ishta Phala', row['reading_en'])
            for factor in row['factors']:
                self.assertTrue(factor['en'] and factor['ta'] and factor['effect'] in (1, -1))


if __name__ == '__main__':
    unittest.main()
