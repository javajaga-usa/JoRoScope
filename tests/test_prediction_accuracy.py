"""Prediction Chapter Accuracy Tests
KP sub-lords and significators, Tajika sahams (checked against P.V.R. Narasimha Rao's
worked chart), Kakshya bindus from the prastara Ashtakavarga, the Nakshatra pada's
Navamsa, Lajjitadi avasthas, Karmajeeva, double-transit windows, Ayur prakriti,
Nadi links and the Karakamsa.
"""
import unittest, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from joroscope.core.engine import calculate, calculate_ashtakavarga
from joroscope.core.predictions import (
    get_kp_sublord, calculate_sahams, lajjitadi_avasthas, _bnn_link, _saham
)

BIRTH = {'name': 'Accuracy', 'date': '1990-01-01', 'time': '12:00:00', 'timezone': 'Asia/Kolkata',
         'latitude': 13.0827, 'longitude': 80.2707, 'ayanamsa': 'Lahiri'}


class KPTests(unittest.TestCase):
    def test_sub_lord_boundaries(self):
        # 280° is exactly the start of Shravana: Moon star, Moon sub
        self.assertEqual(get_kp_sublord(280.0)[5:], ('Moon', 'Moon'))
        self.assertEqual(get_kp_sublord(279.9999)[5:], ('Sun', 'Venus'))  # the last sub of a Sun star
        # Aries 0°: Ashwini, Ketu star and sub; the Venus sub starts after Ketu's 7/120 of 13°20'
        self.assertEqual(get_kp_sublord(0.0)[5:], ('Ketu', 'Ketu'))
        self.assertEqual(get_kp_sublord(800 * 7 / 120 / 60 + 1e-6)[6], 'Venus')
        # The last sub of Revati (Mercury star) belongs to Saturn
        self.assertEqual(get_kp_sublord(359.99)[5:], ('Mercury', 'Saturn'))

    def test_kp_uses_krishnamurti_ayanamsa_and_signifies_houses(self):
        chart = calculate(dict(BIRTH, ayanamsa='Raman'))
        kp = chart['predictions']['kp_system']
        self.assertEqual(kp['ayanamsa'], 'Krishnamurti')
        lahiri = calculate(BIRTH)['predictions']['kp_system']
        # KP positions do not depend on the chart's own ayanamsa
        self.assertEqual([c['longitude'] for c in kp['cusps']], [c['longitude'] for c in lahiri['cusps']])
        for key, cp in kp['cuspal_predictions'].items():
            self.assertIn(cp['verdict'], ('promised', 'mixed', 'weak', 'denied', 'neutral'))
            self.assertTrue(cp['signified_houses'])
            self.assertIn(cp['sub_lord'], cp['reading_en'])
        for row in kp['planets']:
            self.assertTrue(1 <= row['kp_house'] <= 12)
            self.assertIn(row['kp_house'], row['significations'])
        self.assertEqual([r['role_en'] for r in kp['ruling_planets']][-1], 'Day lord')


class SahamTests(unittest.TestCase):
    def test_pvr_chart_66(self):
        """Vedic Astrology: An Integrated Approach, Example 121 (night birth)."""
        book = {'Ascendant': (9, 10 + 49 / 60), 'Sun': (10, 23 + 50 / 60), 'Moon': (11, 15 + 13 / 60),
                'Mars': (11, 24 + 58 / 60), 'Mercury': (10, 11 + 27 / 60), 'Jupiter': (0, 10 + 10 / 60),
                'Venus': (9, 29 + 20 / 60), 'Saturn': (0, 19 + 9 / 60), 'Rahu': (3, 7 + 39 / 60), 'Ketu': (9, 7 + 39 / 60)}
        planets = {n: {'longitude': s * 30 + d, 'sign_index': s, 'house': (s - 9) % 12 + 1, 'sign': '', 'dignity': 'Neutral'}
                   for n, (s, d) in book.items()}
        result = calculate_sahams({'planets': planets})
        self.assertFalse(result['is_day_birth'])
        by = {x['name_en']: x for x in result['sahams']}
        self.assertEqual((by['Artha Saham']['sign'], int(by['Artha Saham']['longitude'] % 30)), ('Scorpio', 2))
        self.assertEqual((by['Samartha Saham']['sign'], round(by['Samartha Saham']['longitude'] % 30)), ('Pisces', 5))
        self.assertEqual((by['Vanika Saham']['sign'], int(by['Vanika Saham']['longitude'] % 30)), ('Sagittarius', 7))

    def test_thirty_degree_rule(self):
        # C on the way from B to A: plain A - B + C
        self.assertAlmostEqual(_saham(100, 10, 50), 140)
        # C not on the way: 30° more
        self.assertAlmostEqual(_saham(100, 10, 200), 320)


class AshtakavargaTimingTests(unittest.TestCase):
    def test_prastara_sums_to_bav_and_drives_kakshyas(self):
        chart = calculate(BIRTH)
        av = chart['ashtakavarga']
        for planet, rows in av['prastara'].items():
            for sign in range(12):
                self.assertEqual(sum(row[sign] for row in rows.values()), av['BAV'][planet][sign])
        kakshya = chart['predictions']['kakshya_transits']
        for body in ('saturn', 'jupiter'):
            table = kakshya[body]['kakshya_timeline']
            self.assertEqual(sum(r['has_bindu'] for r in table), kakshya[body]['bindus'])

    def test_classical_bav_totals(self):
        chart = calculate(BIRTH)
        totals = {p: sum(v) for p, v in chart['ashtakavarga']['BAV'].items()}
        self.assertEqual(totals, {'Sun': 48, 'Moon': 49, 'Mars': 39, 'Mercury': 54, 'Jupiter': 56, 'Venus': 52, 'Saturn': 39})
        self.assertEqual(calculate_ashtakavarga(chart['planets'])['total_points'], 337)


class ChapterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chart = calculate(BIRTH)
        cls.preds = cls.chart['predictions']

    def test_pada_navamsa_follows_the_moon(self):
        pada = self.preds['pada_reading']
        moon = self.chart['planets']['Moon']
        self.assertEqual(pada['navamsa_sign'], ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio',
                                                 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'][moon['navamsa']])
        # Dhanishtha pada 4 falls in the Scorpio Navamsa, ruled by Mars
        self.assertEqual((moon['nakshatra'], moon['pada'], pada['navamsa_sign'], pada['pada_lord']),
                         ('Dhanishtha', 4, 'Scorpio', 'Mars'))

    def test_lajjitadi(self):
        planets = self.chart['planets']
        states = {p: {m['key'] for m in lajjitadi_avasthas(p, planets)} for p in ('Sun', 'Mars', 'Jupiter')}
        self.assertIn('Kshudita', states['Sun'])   # Saturn shares the Sun's sign
        self.assertIn('Trushita', states['Mars'])  # watery Scorpio, aspected only by Ketu
        self.assertIn('Kshudita', states['Jupiter'])  # in Mercury's Gemini

    def test_double_transit_windows_are_dasa_checked(self):
        dt = self.preds['double_transit']
        for m in dt['milestones']:
            self.assertIn(m['status'], ('active', 'transit', 'building', 'quiet'))
            for w in m['windows']:
                self.assertLess(w['start'], w['end'])
                self.assertIn(w['dasa'], ('Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury'))
                self.assertIsInstance(w['dasa_support'], bool)

    def test_karmajeeva(self):
        kj = self.preds['career_d10']['karmajeeva']
        self.assertIn(kj['reference'], ('Lagna', 'Moon', 'Sun'))
        lord = kj['tenth_lord']
        signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
        self.assertEqual(kj['navamsa_sign'], signs[self.chart['planets'][lord]['vargas']['D9']])
        self.assertIn(kj['planet'], self.preds['career_d10']['narrative_en'])
        scores = [a['score'] for a in self.preds['career_d10']['all_archetypes']]
        self.assertGreater(max(scores) - min(scores), 3)

    def test_ayur_depends_on_the_chart(self):
        other = calculate(dict(BIRTH, date='1975-03-02', time='06:10:00'))['predictions']['ayur_jyotish']
        mine = self.preds['ayur_jyotish']
        self.assertNotEqual((mine['vata_percentage'], mine['kapha_percentage']),
                            (other['vata_percentage'], other['kapha_percentage']))
        self.assertEqual(mine['vata_percentage'] + mine['pitta_percentage'] + mine['kapha_percentage'], 100)
        self.assertTrue(mine['factors'] and mine['health_watch'])

    def test_nadi_links(self):
        planets = {p: {'sign_index': s, 'retrograde': False} for p, s in
                   (('Jupiter', 0), ('Saturn', 4), ('Venus', 1), ('Mars', 6), ('Sun', 3))}
        self.assertEqual(_bnn_link(planets, 'Jupiter', 'Saturn')[0], 1)  # trine
        self.assertEqual(_bnn_link(planets, 'Jupiter', 'Venus')[0], 3)   # next sign
        self.assertEqual(_bnn_link(planets, 'Jupiter', 'Mars')[0], 2)    # opposite
        self.assertIsNone(_bnn_link(planets, 'Jupiter', 'Sun'))          # 4th: no Nadi link
        planets['Sun']['retrograde'] = True  # a retrograde graha also acts from the previous sign
        self.assertIsNone(_bnn_link(planets, 'Jupiter', 'Sun'))
        planets['Venus']['retrograde'] = True
        self.assertEqual(_bnn_link(planets, 'Jupiter', 'Venus')[0], 0)  # Venus acts from Aries

    def test_karakamsa(self):
        jk = self.preds['jaimini_karakas']
        ak = jk['atmakaraka']
        signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
        self.assertEqual(jk['karakamsha']['sign'], signs[self.chart['planets'][ak]['vargas']['D9']])
        for occupant in jk['karakamsha']['occupants']:
            self.assertNotEqual(occupant['planet'], ak)


if __name__ == '__main__':
    unittest.main()
