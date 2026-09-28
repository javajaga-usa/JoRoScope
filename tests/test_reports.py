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
        r = c['predictions']['parihara']
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


class MonthlyTransitTests(unittest.TestCase):
    def test_twelve_months_with_vedha_and_bindus(self):
        from datetime import datetime, timezone
        from joroscope.core.monthly import calculate_monthly_transits, VEDHA
        chart = calculate(BIRTH)
        m = calculate_monthly_transits(dict(planets=chart['planets'], ashtakavarga=chart['ashtakavarga'],
                                            timezone='Asia/Kolkata', ayanamsa='Lahiri'),
                                       now=datetime(2026, 9, 28, tzinfo=timezone.utc))
        check_chapter(self, m)
        self.assertEqual([x['month'] for x in m['months']][:2], ['2026-09', '2026-10'])
        october = m['months'][1]
        self.assertIn(('Jupiter', 'Leo', '2026-10-31'), [(c['planet'], c['sign'], c['date']) for c in october['changes']])
        moon = chart['planets']['Moon']['sign_index']
        for month in m['months']:
            for c in month['chandrashtamam']:
                self.assertTrue(c['start'] < c['end'])
            for g in month['grahas']:
                if g['vedha_by']:
                    self.assertIn(g['house'], VEDHA[g['planet']])
        self.assertEqual(moon, 10)  # Aquarius Moon: Chandrashtamam is the Moon in Virgo


class VarshaphalTests(unittest.TestCase):
    def test_annual_chart_matches_pyjhora(self):
        from datetime import datetime, timezone
        from joroscope.core.engine import calculate as calc
        from joroscope.core import varshaphal
        captured = {}
        orig = varshaphal.calculate_varshaphal

        def at(chart, now=None):
            captured['chart'] = chart
            return orig(chart, now)
        varshaphal.calculate_varshaphal = at
        try:
            calc(BIRTH)
        finally:
            varshaphal.calculate_varshaphal = orig
        v = orig(captured['chart'], now=datetime(2026, 9, 28, tzinfo=timezone.utc))
        check_chapter(self, v)
        # PyJHora annual_chart (Lahiri, Chennai): 2026-01-01 17:35:19 IST, Gemini Lagna
        self.assertEqual(v['pravesh'][:16], '2026-01-01T17:35')
        self.assertEqual((v['lagna'], v['years_completed']), ('Gemini', 36))
        # Muntha: Pisces Lagna + 36 years = Pisces, the 10th from Gemini
        self.assertEqual((v['muntha'], v['muntha_house']), ('Pisces', 10))
        self.assertTrue(v['day_year'])
        # Mudda Dasa: 36 years on from the Mars star (Dhanishtha) is Mars again, nearly spent, then Rahu
        self.assertEqual(v['mudda'][0]['lord'], 'Rahu')
        self.assertIn(v['year_lord'], ('Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'))


class LifeReportTests(unittest.TestCase):
    def test_marriage_and_career(self):
        from datetime import datetime, timezone
        from joroscope.core.readings.life_reports import period_windows
        c = calculate(dict(BIRTH, date='2001-11-23', time='04:05:00'))
        m, k = c['predictions']['marriage'], c['predictions']['career_report']
        check_chapter(self, m)
        check_chapter(self, k)
        # Libra Lagna: the 7th is Aries, lord Mars; Venus is always a significator
        self.assertIn('Mars', m['significators'])
        self.assertIn('Venus', m['significators'])
        self.assertTrue(m['cards'][0]['title']['en'].endswith('Aries'))
        # Mars in the 4th aspects the 7th by its 4th-house drishti
        self.assertIn('Aspecting it: Mars', m['cards'][0]['body']['en'])
        for w in m['windows'] + k['windows']:
            self.assertLess(w['start'], w['end'])
        rows = [{'lord': 'Venus', 'subperiods': [
            {'lord': 'Venus', 'start': '2030-01-01T00:00:00+00:00', 'end': '2033-01-01T00:00:00+00:00'},
            {'lord': 'Sun', 'start': '2033-01-01T00:00:00+00:00', 'end': '2034-01-01T00:00:00+00:00'}]}]
        w = period_windows(rows, {'Venus'}, datetime(2026, 1, 1, tzinfo=timezone.utc))
        self.assertEqual([(x['bhukti'], x['strength']) for x in w], [('Venus', 'strong')])


class PrasnaTests(unittest.TestCase):
    def test_rules_and_ithasala(self):
        from joroscope.core.prasna import calculate_prasna, SHIRSHODAYA
        r = calculate_prasna('career', '2026-09-29', '04:15:00', 'Asia/Kolkata', 13.0827, 80.2707, arudha=7)
        check_chapter(self, r)
        self.assertEqual(r['lagna'], 'Leo')
        self.assertIn(4, SHIRSHODAYA)                      # Leo rises head first
        self.assertEqual(r['arudha'], 'Libra')
        self.assertIn(r['verdict'], ('good', 'mixed', 'bad'))
        factors = [row[0]['en'] for row in r['tables'][0]['rows']]
        self.assertTrue(any('Shirshodaya' in f for f in factors))
        with self.assertRaises(ValueError):
            calculate_prasna('career', '', '', 'Asia/Kolkata', 13.08, 80.27, arudha=13)

    def test_api(self):
        import json, threading, urllib.request
        from http.server import HTTPServer
        from joroscope.server import Handler
        server = HTTPServer(('127.0.0.1', 0), Handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            body = json.dumps({'question': 'marriage', 'latitude': 13.08, 'longitude': 80.27, 'timezone': 'Asia/Kolkata'}).encode()
            req = urllib.request.Request(f'http://127.0.0.1:{server.server_port}/api/prasna', data=body,
                                         headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read())
            self.assertEqual(data['question'], 'marriage')
            self.assertTrue(data['cards'][0]['title']['en'].startswith('Answer'))
        finally:
            server.shutdown()
            server.server_close()


class ChakraTests(unittest.TestCase):
    def test_sarvatobhadra_layout(self):
        from joroscope.core.chakras import SBC_GRID, STAR_CELL, SIGN_CELL, star28, star28_name, vedha_cells
        # East on top: Krittika to Ashlesha; Abhijit on the west side next to Shravana
        self.assertEqual([star28_name(v)[0] for v in SBC_GRID[0][1:8]],
                         ['Krittika', 'Rohini', 'Mrigashira', 'Ardra', 'Punarvasu', 'Pushya', 'Ashlesha'])
        self.assertEqual(len(STAR_CELL), 28)
        self.assertEqual(len(SIGN_CELL), 12)
        self.assertEqual(STAR_CELL[22], (8, 2))
        self.assertEqual(star28(277.0), 22)   # Abhijit
        self.assertEqual(star28(281.0), 23)   # Shravana
        # Krittika's Vedha ahead runs down its column to the west side (Shravana)
        cells = vedha_cells(3, 'ahead')
        self.assertEqual(cells[-1], (8, 1))
        self.assertEqual(star28_name(SBC_GRID[8][1])[0], 'Shravana')

    def test_chart(self):
        c = calculate(BIRTH)
        ch = c['predictions']['chakras']
        check_chapter(self, ch)
        self.assertEqual(len(ch['grid']), 9)
        self.assertTrue(all(len(row) == 9 for row in ch['grid']))
        self.assertEqual(ch['kota_swami'], 'Saturn')          # Aquarius Moon
        for row in ch['tables'][1]['rows']:
            count = int(row[2]['en'])
            if count in (4, 11, 18, 25):
                self.assertTrue(row[3]['en'].startswith('Stambha'))


class RectificationTests(unittest.TestCase):
    def test_ranks_candidates(self):
        from joroscope.core.rectification import rectify, EVENT_MAX
        data = dict(BIRTH)
        events = [{'date': '2016-02-10', 'type': 'marriage'}, {'date': '2018-06-01', 'type': 'child'},
                  {'date': '2013-07-01', 'type': 'career'}]
        r = rectify(data, events, 60, 2)
        check_chapter(self, r)
        self.assertLessEqual(abs(r['best_offset']), 60)
        self.assertEqual(r['max_score'], EVENT_MAX * 3)
        scores = [int(row[4]['en']) for row in r['tables'][0]['rows']]
        self.assertEqual(scores, sorted(scores, reverse=True))
        # Each event is explained with its running dasa lords
        self.assertTrue(all(' Dasa, ' in c['body']['en'] for c in r['cards'][1:]))

    def test_validation(self):
        from joroscope.core.rectification import rectify
        with self.assertRaises(ValueError):
            rectify(dict(BIRTH), [], 60, 2)
        with self.assertRaises(ValueError):
            rectify(dict(BIRTH), [{'date': '1980-01-01', 'type': 'marriage'}], 60, 2)   # before birth
        with self.assertRaises(ValueError):
            rectify(dict(BIRTH), [{'date': '2016-01-01', 'type': 'lottery'}], 60, 2)

if __name__ == '__main__':
    unittest.main()
