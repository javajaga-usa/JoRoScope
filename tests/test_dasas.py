"""Additional Dasa Tests
Ashtottari and K.N. Rao's Chara Dasa reproduce PyJHora for real charts; the dasa year option
changes every dasa's length.
"""
import unittest, sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from joroscope.core.engine import calculate

CHENNAI = {'timezone': 'Asia/Kolkata', 'latitude': 13.0827, 'longitude': 80.2707, 'ayanamsa': 'Lahiri'}


def chart(date, time, **extra):
    return calculate(dict(CHENNAI, name='D', date=date, time=time, **extra))


class DasaTests(unittest.TestCase):
    def test_ashtottari_matches_pyjhora(self):
        # PyJHora (Lahiri, sidereal year): Jupiter from 1983-10-07 02:26 IST, then Rahu 2002-10-07
        c = chart('1990-01-01', '12:00:00', dasa_year='sidereal')
        rows = c['ashtottari_dasha']
        self.assertEqual([r['lord'] for r in rows], ['Jupiter', 'Rahu', 'Venus', 'Sun', 'Moon', 'Mars', 'Mercury', 'Saturn'])
        start = datetime.fromisoformat(rows[0]['start'])
        self.assertLess(abs((start - datetime.fromisoformat('1983-10-07T02:26:00+05:30')).total_seconds()), 86400)
        self.assertEqual([b['lord'] for b in rows[0]['subperiods']][:3], ['Jupiter', 'Rahu', 'Venus'])
        self.assertEqual(sum(r['years'] for r in rows), 108)

    def test_chara_matches_pyjhora_kn_rao(self):
        first = lambda c: [(r['sign'][:3], r['years']) for r in c['chara_dasha'] if r['round'] == 1]
        self.assertEqual(first(chart('1990-01-01', '12:00:00')),
                         [('Pis', 9), ('Ari', 7), ('Tau', 8), ('Gem', 7), ('Can', 5), ('Leo', 8), ('Vir', 8), ('Lib', 3),
                          ('Sco', 8), ('Sag', 6), ('Cap', 1), ('Aqu', 1)])
        # Sagittarius gets no years in the first round (Jupiter debilitated in the next sign) and 12 in the second
        c = chart('1985-06-15', '21:40:00')
        self.assertEqual(first(c), [('Cap', 4), ('Sco', 7), ('Lib', 6), ('Vir', 3), ('Leo', 2), ('Can', 3), ('Gem', 12),
                                    ('Tau', 11), ('Ari', 2), ('Pis', 1), ('Aqu', 10)])
        second = {r['sign']: r['years'] for r in c['chara_dasha'] if r['round'] == 2}
        self.assertEqual(second['Sagittarius'], 12)
        self.assertEqual(second['Capricorn'], 8)

    def test_chara_antardasas(self):
        c = chart('1990-01-01', '12:00:00')
        leo = next(r for r in c['chara_dasha'] if r['sign'] == 'Leo')
        # Leo is even-footed: antardasas run backward from Cancer and end with Leo
        self.assertEqual([b['sign'] for b in leo['subperiods']][:2], ['Cancer', 'Gemini'])
        self.assertEqual(leo['subperiods'][-1]['sign'], 'Leo')
        pisces = c['chara_dasha'][0]
        self.assertEqual(pisces['subperiods'][0]['sign'], 'Aquarius')

    def test_dasa_year_option(self):
        julian = chart('1990-01-01', '12:00:00')
        savana = chart('1990-01-01', '12:00:00', dasa_year='savana')
        self.assertEqual(savana['dasa_year']['days'], 360.0)
        length = lambda row: (datetime.fromisoformat(row['end']) - datetime.fromisoformat(row['start'])).days
        self.assertEqual(length(savana['dasha'][1]), round(length(julian['dasha'][1]) * 360 / 365.25))
        self.assertLess(length(savana['yogini_dasha'][1]), length(julian['yogini_dasha'][1]))
        with self.assertRaises(ValueError):
            chart('1990-01-01', '12:00:00', dasa_year='lunar')


if __name__ == '__main__':
    unittest.main()
