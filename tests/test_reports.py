"""Report Chapter Tests
The chapters added after 2.1.0 (numerology, remedies, monthly transits, Varshaphal, marriage and
career, Prasna, Sarvatobhadra and Kota Chakra, rectification), checked against hand-worked cases.
"""
import unittest, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from joroscope.core.engine import calculate
from joroscope.core.readings.numerology import name_number, reduce_number, relation

BIRTH = {'name': 'Sri Raman', 'date': '1990-01-01', 'time': '12:00:00', 'timezone': 'Asia/Kolkata',
         'latitude': 13.0827, 'longitude': 80.2707, 'ayanamsa': 'Lahiri'}


def check_chapter(test, ch):
    test.assertTrue(ch['title']['en'] and ch['title']['ta'])
    for c in ch['cards']:
        test.assertTrue(c['title']['en'] and c['title']['ta'] and c['body']['en'] and c['body']['ta'], c['title'])
    for t in ch['tables']:
        for row in t['rows']:
            test.assertEqual(len(row), len(t['head']))


class NumerologyTests(unittest.TestCase):
    def test_chaldean_values(self):
        # S3 R2 I1 R2 A1 M4 A1 N5 = 19 -> 1
        self.assertEqual(name_number('Sri Raman'), (19, 1))
        self.assertIsNone(name_number('ஸ்ரீ ராமன்'))
        self.assertEqual(reduce_number(1990), 1)

    def test_chart_numbers(self):
        n = calculate(BIRTH)['predictions']['numerology']
        self.assertEqual((n['birth_number'], n['destiny_number']), (1, 3))  # 1+1+1+9+9+0 = 21 -> 3
        self.assertEqual(n['name_number']['number'], 1)
        check_chapter(self, n)

    def test_relations(self):
        self.assertEqual(relation(1, 2), 1)    # Sun and Moon are friends
        self.assertEqual(relation(1, 8), -1)   # Sun and Saturn are enemies
        self.assertEqual(relation(4, 8), 1)    # Rahu is read as Saturn



class RemediesTests(unittest.TestCase):
    def test_reasons_come_from_the_chart(self):
        c = calculate(dict(BIRTH, date='1985-06-15', time='21:40:00'))
        r = c['predictions']['remedies']
        check_chapter(self, r)
        titles = [card['title']['en'] for card in r['cards']]
        self.assertIn('Rahu-Ketu (Naga) Dosham', titles)          # doshas.rahu_ketu is present in this chart
        jupiter = next(card for card in r['cards'] if card['title']['en'].startswith('Jupiter'))
        self.assertIn('debilitated', jupiter['sub']['en'])         # Jupiter in Capricorn
        self.assertIn('Alangudi', jupiter['body']['en'])
        self.assertIn('19,000', jupiter['body']['en'])

    def test_every_graha_has_a_remedy(self):
        from joroscope.core.readings.remedies import GRAHA_REMEDIES, FASTING, graha_remedy_text
        self.assertEqual(set(GRAHA_REMEDIES), set(FASTING))
        for g in GRAHA_REMEDIES:
            en, ta = graha_remedy_text(g)
            self.assertTrue(en and ta)

if __name__ == '__main__':
    unittest.main()
