"""Monthly Tamil calendar tests.
Observance dates are checked against Drik Panchang's published lists for Chennai
(2025 and 2026), so the rules keep matching what Tamil almanac users see.
"""
import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from joroscope.core.south_indian import month_calendar

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Drik Panchang, Chennai (geoname 1264527)
DRIK = {
    2025: {
        'amavasai': 'Jan 29,Feb 27,Mar 29,Apr 27,May 26,Jun 25,Jul 24,Aug 22,Sep 21,Oct 21,Nov 19,Dec 19',
        'pournami': 'Jan 13,Feb 12,Mar 13,Apr 12,May 12,Jun 10,Jul 10,Aug 9,Sep 7,Oct 6,Nov 5,Dec 4',
        'pradosham': 'Jan 11,Jan 27,Feb 9,Feb 25,Mar 11,Mar 27,Apr 10,Apr 25,May 9,May 24,Jun 8,Jun 23,'
                     'Jul 8,Jul 22,Aug 6,Aug 20,Sep 5,Sep 19,Oct 4,Oct 18,Nov 3,Nov 17,Dec 2,Dec 17',
        'sashti': 'Jan 5,Feb 3,Mar 4,Apr 3,May 2,Jun 1,Jun 30,Jul 30,Aug 28,Sep 27,Oct 27,Nov 26,Dec 25',
        'karthigai': 'Jan 9,Feb 6,Mar 5,Apr 1,Apr 29,May 26,Jun 22,Jul 20,Aug 16,Sep 12,Oct 10,Nov 6,Dec 4,Dec 31',
        'ekadasi': 'Jan 10,Jan 25,Feb 8,Feb 24,Mar 10,Mar 25,Apr 8,Apr 24,May 8,May 23,Jun 6,Jun 21,Jul 6,Jul 21,'
                   'Aug 5,Aug 19,Sep 3,Sep 17,Oct 3,Oct 17,Nov 1,Nov 15,Dec 1,Dec 15,Dec 30',
    },
    2026: {
        'amavasai': 'Jan 18,Feb 17,Mar 18,Apr 17,May 16,Jun 14,Jul 14,Aug 12,Sep 10,Oct 10,Nov 8,Dec 8',
        'pournami': 'Jan 3,Feb 1,Mar 3,Apr 1,May 1,May 30,Jun 29,Jul 29,Aug 27,Sep 26,Oct 25,Nov 24,Dec 23',
        'pradosham': 'Jan 1,Jan 16,Jan 30,Feb 14,Mar 1,Mar 16,Mar 30,Apr 15,Apr 28,May 14,May 28,Jun 12,Jun 27,'
                     'Jul 12,Jul 26,Aug 10,Aug 25,Sep 8,Sep 24,Oct 8,Oct 23,Nov 6,Nov 22,Dec 6,Dec 21',
        'sashti': 'Jan 24,Feb 22,Mar 24,Apr 22,May 21,Jun 19,Jul 19,Aug 17,Sep 16,Oct 16,Nov 15,Dec 15',
        'karthigai': 'Jan 27,Feb 23,Mar 23,Apr 19,May 16,Jun 13,Jul 10,Aug 7,Sep 3,Sep 30,Oct 27,Nov 24,Dec 21',
        'ekadasi': 'Jan 14,Jan 29,Feb 13,Feb 27,Mar 15,Mar 29,Apr 13,Apr 27,May 13,May 27,Jun 11,Jun 25,Jul 10,Jul 25,'
                   'Aug 9,Aug 23,Sep 7,Sep 22,Oct 6,Oct 22,Nov 5,Nov 20,Dec 4,Dec 20',
        'sankatahara': 'Jan 6,Feb 5,Mar 6,Apr 5,May 5,Jun 4,Jul 3,Aug 2,Aug 31,Sep 29,Oct 29,Nov 27,Dec 26',
        'shivaratri': 'Jan 16,Feb 15,Mar 17,Apr 15,May 15,Jun 13,Jul 12,Aug 11,Sep 9,Oct 8,Nov 7,Dec 7',
    },
}


def parse(year, text):
    return {date(year, MONTHS.index(item.split()[0]) + 1, int(item.split()[1])) for item in text.split(',')}


class TamilCalendarTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.found = {}
        cls.days = {}
        for year in DRIK:
            for month in range(1, 13):
                for day in month_calendar(year, month, 'Asia/Kolkata', 13.0827, 80.2707)['days']:
                    d = date.fromisoformat(day['date'])
                    cls.days[d] = day
                    for obs in day['observances']:
                        cls.found.setdefault((year, obs['key']), set()).add(d)

    def test_observances_match_drik_panchang(self):
        for year, lists in DRIK.items():
            for key, text in lists.items():
                with self.subTest(year=year, observance=key):
                    self.assertEqual(self.found.get((year, key), set()), parse(year, text))

    def test_tamil_dates_run_continuously(self):
        ordered = sorted(self.days)
        for prev, cur in zip(ordered, ordered[1:]):
            a, b = self.days[prev], self.days[cur]
            if b['tamil_day'] == 1:
                self.assertIn('month_start', [o['key'] for o in b['observances']])
            else:
                self.assertEqual((b['tamil_month'], b['tamil_day']), (a['tamil_month'], a['tamil_day'] + 1))
        self.assertEqual((self.days[date(2025, 4, 14)]['tamil_month'], self.days[date(2025, 4, 14)]['tamil_day']),
                         ('Chithirai', 1))
        self.assertEqual(self.days[date(2025, 4, 14)]['tamil_year'], 'Visuvavasu')
        self.assertEqual(self.days[date(2026, 1, 14)]['tamil_month'], 'Thai')

    def test_every_tamil_label_present(self):
        day = self.days[date(2026, 11, 24)]
        self.assertEqual({o['key'] for o in day['observances']}, {'pournami', 'karthigai'})
        for o in day['observances']:
            self.assertTrue(o['ta'])


if __name__ == '__main__':
    unittest.main()
