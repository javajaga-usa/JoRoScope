"""Features matching Astro-Vision LifeSign's horoscope: Bhava Bala, Shodasavarga (D40/D45),
Vimsopaka Bala and Varga Bheda, Sodhita Ashtakavarga with Sodhya Pinda (checked against
P.V.R. Narasimha Rao's worked Charts 7 and 11), Yogi/Avayogi, Dagdha Rasi, Chandra
Avastha, Moudhyam, Graha Yuddha and the Jaimini Arudha padas.
"""
import unittest, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from joroscope.core.engine import (
    calculate, calculate_vargas, _trikona_sodhana, _ekadhipatya_sodhana, RASI_GUNAKARA, GRAHA_GUNAKARA
)
from joroscope.core.predictions import jaimini_arudhas, _rasi_drishti
from joroscope.core.south_indian import birth_extras

BIRTH = {'name': 'Parity', 'date': '1990-01-01', 'time': '12:00:00', 'timezone': 'Asia/Kolkata',
         'latitude': 13.0827, 'longitude': 80.2707, 'ayanamsa': 'Lahiri'}
PLANETS = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']


def book_pindas(chart_1d, bav):
    signs, occupied = {}, set()
    for sign, cell in enumerate(chart_1d):
        for token in filter(None, cell.split('/')):
            if token == 'L':
                occupied.add(sign)
            elif int(token) < 7:
                signs[PLANETS[int(token)]] = sign
                occupied.add(sign)
    rows = []
    for i, planet in enumerate(PLANETS):
        reduced = _ekadhipatya_sodhana(_trikona_sodhana(bav[i]), occupied)
        rasi = sum(b * m for b, m in zip(reduced, RASI_GUNAKARA))
        graha = sum(GRAHA_GUNAKARA[q] * reduced[signs[q]] for q in PLANETS)
        rows.append((rasi, graha, rasi + graha))
    return rows


class SodhanaTests(unittest.TestCase):
    """Vedic Astrology: An Integrated Approach, ch. 12."""

    def test_example_40_to_42_chart_11(self):
        bav = [7, 4, 7, 4, 4, 3, 4, 4, 4, 3, 6, 4]
        self.assertEqual(_trikona_sodhana(bav), [3, 1, 3, 0, 0, 0, 0, 0, 0, 0, 2, 0])
        chart_11 = ['5/8/L', '', '0/2/3', '', '4/6', '', '7', '', '', '', '', '1']
        self.assertEqual(book_pindas(chart_11, [bav] * 7)[0], (77, 75, 152))

    def test_exercise_22_chart_7(self):
        chart_7 = ['6/1/7', '', '', '', '', '', '8/4', 'L', '3/2', '0', '5', '']
        bav = [[4, 2, 3, 4, 6, 5, 5, 3, 2, 6, 6, 2], [6, 3, 5, 3, 5, 5, 6, 3, 3, 4, 4, 2], [3, 2, 3, 4, 2, 5, 4, 3, 3, 4, 3, 3],
               [4, 6, 4, 3, 4, 7, 4, 5, 6, 3, 5, 3], [4, 4, 3, 5, 6, 5, 6, 4, 6, 4, 3, 6], [3, 5, 5, 4, 6, 2, 3, 6, 5, 2, 7, 4],
               [3, 2, 2, 3, 5, 6, 3, 4, 1, 3, 6, 1]]
        rows = book_pindas(chart_7, bav)
        self.assertEqual([r[0] for r in rows], [152, 85, 52, 95, 68, 154, 162])
        self.assertEqual([r[1] for r in rows], [81, 55, 43, 33, 56, 54, 63])
        self.assertEqual([r[2] for r in rows], [233, 140, 95, 128, 124, 208, 225])

    def test_chart_pindas(self):
        av = calculate(BIRTH)['ashtakavarga']
        for planet in PLANETS:
            self.assertEqual(av['pindas'][planet]['sodhya'], av['pindas'][planet]['rasi'] + av['pindas'][planet]['graha'])
            self.assertTrue(all(0 <= b <= raw for b, raw in zip(av['sodhita'][planet], av['BAV'][planet])))


class VargaTests(unittest.TestCase):
    def test_khavedamsa_and_akshavedamsa(self):
        # D40: 45' parts from Aries in odd signs, from Libra in even signs
        self.assertEqual(calculate_vargas(0.1)['D40'], 0)
        self.assertEqual(calculate_vargas(0.8)['D40'], 1)
        self.assertEqual(calculate_vargas(30.1)['D40'], 6)
        # D45: 40' parts from Aries (movable), Leo (fixed), Sagittarius (dual)
        self.assertEqual(calculate_vargas(0.1)['D45'], 0)
        self.assertEqual(calculate_vargas(30.1)['D45'], 4)
        self.assertEqual(calculate_vargas(60.1)['D45'], 8)
        self.assertEqual(calculate_vargas(60.7)['D45'], 9)

    def test_vimsopaka_and_varga_bheda(self):
        chart = calculate(BIRTH)
        rows = chart['predictions']['shadbala']['vimsopaka']
        self.assertEqual(len(rows), 7)
        for row in rows:
            for scheme in ('shadvarga', 'saptavarga', 'dasavarga', 'shodasavarga'):
                cell = row[scheme]
                self.assertTrue(5 <= cell['score'] <= 20)
                self.assertEqual(cell['bheda_en'] is None, cell['dignified'] < 2)
        # Mars owns Scorpio in the Rasi and gains dignities in the vargas
        mars = next(r for r in rows if r['planet'] == 'Mars')
        self.assertEqual(mars['dasavarga']['bheda_en'], 'Uttamamsa')


class StrengthTests(unittest.TestCase):
    def test_bhava_bala(self):
        chart = calculate(BIRTH)
        bhavas = chart['predictions']['shadbala']['bhavas']
        self.assertEqual(sorted(b['rank'] for b in bhavas), list(range(1, 13)))
        for b in bhavas:
            self.assertTrue(0 <= b['dig'] <= 60)
            self.assertAlmostEqual(b['total_virupas'], b['adhipati'] + b['dig'] + b['drishti'], delta=0.05)
        by_house = {b['house']: b for b in chart['predictions']['bhavas']}
        self.assertEqual(by_house[1]['bhava_bala_rupas'], bhavas[0]['rupas'])


class BirthExtrasTests(unittest.TestCase):
    def test_yogi_avayogi_and_dagdha(self):
        extras = calculate(BIRTH)['south_indian']['extras']
        # Sun 256.87 + Moon 306.47 + 93°20' = 296.66: Dhanishtha (Mars), Capricorn (Saturn)
        self.assertEqual((extras['yogi']['star'], extras['yogi']['planet'], extras['yogi']['duplicate']),
                         ('Dhanishtha', 'Mars', 'Saturn'))
        self.assertEqual(extras['avayogi']['star'], 'Magha')
        # Panchami: Gemini and Virgo are burnt
        self.assertEqual([d['en'] for d in extras['dagdha_rasis']], ['Gemini', 'Virgo'])
        # The Moon is at the very end of Dhanishtha
        self.assertEqual(extras['chandra'], {'avastha': 12, 'vela': 36, 'kriya': 60})
        self.assertEqual([m['planet'] for m in extras['moudhyam']], ['Saturn'])

    def test_amavasai_has_no_dagdha_rasi(self):
        planets = {'Sun': {'longitude': 100.0}, 'Moon': {'longitude': 101.0}}
        for p in ('Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'):
            planets[p] = {'longitude': 250.0}
        self.assertEqual(birth_extras(planets)['dagdha_rasis'][:1], [{'en': 'Libra', 'ta': 'துலாம்'}])  # Pratipada
        planets['Moon']['longitude'] = 99.0  # tithi 30
        self.assertEqual(birth_extras(planets)['dagdha_rasis'], [])

    def test_graha_yuddha(self):
        chart = calculate(dict(BIRTH, date='1981-09-13', time='01:30:00', latitude=28.65, longitude=77.2167))
        self.assertEqual(chart['south_indian']['extras']['graha_yuddha'], [{'winner': 'Jupiter', 'loser': 'Mercury'}])


class ArudhaTests(unittest.TestCase):
    def test_rasi_drishti(self):
        self.assertEqual(_rasi_drishti(0), {4, 7, 10})    # Aries: fixed signs but Taurus
        self.assertEqual(_rasi_drishti(1), {3, 6, 9})     # Taurus: movable signs but Aries
        self.assertEqual(_rasi_drishti(2), {5, 8, 11})    # Gemini: the other dual signs

    def test_arudha_exceptions(self):
        chart = calculate(BIRTH)
        padas = jaimini_arudhas(chart['planets'])
        # Pisces Lagna, Jupiter in Gemini: the count lands on Virgo, 7th from the Lagna, so AL is Gemini
        self.assertEqual(padas[0], 2)
        asc = chart['planets']['Ascendant']['sign_index']
        for house, pada in enumerate(padas, 1):
            self.assertNotIn((pada - (asc + house - 1)) % 12, (0, 6))
        self.assertEqual(len(chart['predictions']['jaimini_karakas']['arudhas']), 12)


if __name__ == '__main__':
    unittest.main()
