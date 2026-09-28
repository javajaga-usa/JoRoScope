"""Yoga Tests
Hand-built charts for the classical yoga rules (BPHS, Phaladeepika and B.V. Raman's Three
Hundred Important Combinations) that yogas.py implements.
"""
import unittest, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from joroscope.core.engine import calculate, calculate_dignity, calculate_vargas
from joroscope.core.yogas import detect, YOGAS

SIGN = {s: i for i, s in enumerate(['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio',
                                     'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'])}


def chart(asc, **bodies):
    """bodies: name -> (sign, degree); Ketu follows Rahu. Unplaced grahas default to spread signs."""
    defaults = {'Sun': ('Leo', 10), 'Moon': ('Taurus', 10), 'Mars': ('Aries', 10), 'Mercury': ('Virgo', 5),
                'Jupiter': ('Sagittarius', 10), 'Venus': ('Libra', 10), 'Saturn': ('Aquarius', 10), 'Rahu': ('Gemini', 10)}
    defaults.update(bodies)
    planets = {}
    for name, (sign, deg) in defaults.items():
        lon = SIGN[sign] * 30 + deg
        planets[name] = {'longitude': lon, 'sign_index': SIGN[sign], 'degree': deg, 'vargas': calculate_vargas(lon), 'combust': False}
    rahu = planets['Rahu']['longitude']
    planets['Ketu'] = {'longitude': (rahu + 180) % 360, 'sign_index': int(((rahu + 180) % 360) // 30), 'degree': rahu % 30,
                       'vargas': calculate_vargas((rahu + 180) % 360), 'combust': False}
    planets['Ascendant'] = {'longitude': SIGN[asc] * 30 + 15, 'sign_index': SIGN[asc], 'degree': 15,
                            'vargas': calculate_vargas(SIGN[asc] * 30 + 15)}
    for name in ('Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu'):
        planets[name]['dignity'] = calculate_dignity(name, planets[name]['sign_index'], planets[name]['degree'], planets)
    return planets


def keys(planets):
    return {y['key'] for y in detect(planets)}


class YogaTests(unittest.TestCase):
    def test_every_yoga_is_bilingual(self):
        for key, (en, ta, category, nature, desc_en, desc_ta) in YOGAS.items():
            self.assertTrue(en and ta and desc_en and desc_ta, key)

    def test_mahapurusha(self):
        # Capricorn Lagna, Mars exalted in the 1st: Ruchaka
        self.assertIn('ruchaka', keys(chart('Capricorn', Mars=('Capricorn', 20))))
        # Mars exalted but in the 2nd: no Ruchaka
        self.assertNotIn('ruchaka', keys(chart('Sagittarius', Mars=('Capricorn', 20))))

    def test_gaja_kesari_needs_a_strong_supported_jupiter(self):
        base = dict(Moon=('Aries', 10), Jupiter=('Cancer', 5), Venus=('Cancer', 20), Sun=('Leo', 10), Mercury=('Leo', 20))
        self.assertIn('gaja_kesari', keys(chart('Aries', **base)))
        # Jupiter debilitated in Capricorn (a kendra from an Aries Moon): no Gaja Kesari
        self.assertNotIn('gaja_kesari', keys(chart('Aries', **dict(base, Jupiter=('Capricorn', 5), Venus=('Capricorn', 20)))))
        # No benefic joins or aspects Jupiter
        self.assertNotIn('gaja_kesari', keys(chart('Aries', **dict(base, Venus=('Gemini', 20), Mercury=('Leo', 20)))))

    def test_chandra_yogas_are_exclusive(self):
        both = keys(chart('Aries', Moon=('Leo', 10), Mars=('Virgo', 10), Venus=('Cancer', 10), Sun=('Aries', 5),
                          Mercury=('Aries', 20), Jupiter=('Sagittarius', 10), Saturn=('Aquarius', 10)))
        self.assertIn('durudhara', both)
        self.assertFalse({'sunapha', 'anapha'} & both)

    def test_kemadruma_and_its_cancellation(self):
        # Moon alone in Leo, nothing in Cancer or Virgo, but grahas in kendras cancel it
        lone = dict(Moon=('Leo', 10), Sun=('Aries', 10), Mars=('Aries', 20), Mercury=('Pisces', 10), Jupiter=('Sagittarius', 10),
                    Venus=('Taurus', 10), Saturn=('Capricorn', 10), Rahu=('Gemini', 10))
        self.assertIn('kemadruma_bhanga', keys(chart('Aries', **lone)))
        # Same grahas, Lagna chosen so no graha sits in a kendra from it or from the Moon
        self.assertIn('kemadruma', keys(chart('Taurus', **dict(lone, Venus=('Pisces', 20), Saturn=('Pisces', 25)))) |
                      keys(chart('Taurus', **dict(lone, Venus=('Pisces', 20), Saturn=('Pisces', 25), Jupiter=('Pisces', 5)))))

    def test_parivartana_kinds(self):
        # Aries Lagna: Mars (1st lord) in Cancer, Moon (4th lord) in Aries: Maha Parivartana
        self.assertIn('maha_parivartana', keys(chart('Aries', Mars=('Cancer', 10), Moon=('Aries', 10))))
        # Mercury (6th lord from Aries) in Scorpio, Mars (8th lord) in Virgo: Dainya
        self.assertIn('dainya_parivartana', keys(chart('Aries', Mercury=('Scorpio', 10), Mars=('Virgo', 10))))

    def test_vipareeta_and_neechabhanga(self):
        # Aries Lagna: Mercury, lord of the 6th, in the 8th (Scorpio): Harsha
        self.assertIn('harsha', keys(chart('Aries', Mercury=('Scorpio', 10))))
        # Jupiter debilitated in Capricorn, joined there by its dispositor Saturn in the 10th (a kendra)
        found = [y for y in detect(chart('Aries', Jupiter=('Capricorn', 5), Saturn=('Capricorn', 10))) if y['key'] == 'neechabhanga']
        self.assertEqual([y['planets'] for y in found], [['Jupiter']])
        self.assertIn('Saturn, lord of the sign, is in a kendra', found[0]['description'])

    def test_amala_needs_only_benefics(self):
        self.assertIn('amala', keys(chart('Aries', Venus=('Capricorn', 10))))
        self.assertNotIn('amala', keys(chart('Aries', Venus=('Capricorn', 10), Saturn=('Capricorn', 20), Moon=('Taurus', 10))))

    def test_nabhasa_shapes(self):
        # All seven grahas in the 1st and 7th: Sakata (Nabhasa)
        packed = dict(Sun=('Aries', 1), Moon=('Aries', 5), Mars=('Aries', 9), Mercury=('Libra', 1), Jupiter=('Libra', 5),
                      Venus=('Libra', 9), Saturn=('Libra', 13))
        found = keys(chart('Aries', **packed))
        self.assertIn('sakata_nabhasa', found)
        self.assertFalse({'vallaki', 'dama', 'pasa', 'kedara', 'shula', 'yuga', 'gola'} & found)
        # Spread over five signs with no shape: the Sankhya yoga Pasa
        spread = keys(chart('Aries', Sun=('Leo', 10), Moon=('Taurus', 10), Mars=('Leo', 20), Mercury=('Virgo', 5),
                            Jupiter=('Sagittarius', 10), Venus=('Libra', 10), Saturn=('Libra', 20)))
        self.assertIn('pasa', spread)

    def test_real_chart(self):
        c = calculate({'name': 'Y', 'date': '1985-06-15', 'time': '21:40:00', 'timezone': 'Asia/Kolkata',
                       'latitude': 13.0827, 'longitude': 80.2707, 'ayanamsa': 'Lahiri'})
        natures = [y['nature'] for y in c['yogas']]
        self.assertEqual(natures, sorted(natures, key=['good', 'mixed', 'cancelled', 'bad'].index))
        for y in c['yogas']:
            self.assertTrue(y['name_ta'] and y['description_ta'] and y['category_ta'] and y['auspiciousness_ta'])


if __name__ == '__main__':
    unittest.main()
