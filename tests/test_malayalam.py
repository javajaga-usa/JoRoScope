"""Malayalam coverage: every reading written in Tamil also carries Malayalam, and the chart API sends
the Malayalam only when the page asks for it.
"""

import json
import re
import sys
import threading
import unittest
import urllib.request
from http.server import HTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from joroscope.core import engine
from joroscope.server import Handler, strip_malayalam

TAMIL = re.compile('[஀-௿]')
BIRTHS = [
    dict(date='1985-06-15', time='08:30', timezone='Asia/Kolkata', latitude=10.5, longitude=76.2, name='Test Person'),
    dict(date='1992-11-03', time='23:10', timezone='Asia/Kolkata', latitude=13.08, longitude=80.27, name='Second Test'),
]


def untranslated(value, path='', out=None):
    """Paths of Tamil sentences (over 30 characters) with no Malayalam beside them."""
    out = [] if out is None else out
    if isinstance(value, dict):
        for key, item in value.items():
            if isinstance(item, str) and len(item) > 30 and TAMIL.search(item):
                has_ml = (key.endswith('_ta') and key[:-3] + '_ml' in value) or (key == 'ta' and 'ml' in value)
                if not has_ml:
                    out.append(f'{path}.{key}')
            untranslated(item, f'{path}.{key}', out)
    elif isinstance(value, list):
        for item in value:
            untranslated(item, path + '[]', out)
    return out


class MalayalamCoverageTests(unittest.TestCase):
    def test_every_tamil_reading_has_malayalam(self):
        for birth in BIRTHS:
            chart = engine.calculate(dict(birth, ayanamsa='Lahiri', lang='ml'))
            chart.pop('readings', None)  # the English-only summary block, not shown on the page
            missing = sorted(set(untranslated(chart)))
            self.assertEqual(missing, [], f"{birth['date']}: {missing[:10]}")

    def test_strip_malayalam(self):
        data = {'a_en': 'x', 'a_ta': 'y', 'a_ml': 'z', 'card': {'en': 'x', 'ta': 'y', 'ml': 'z'}, 'ml': 'kept without en'}
        self.assertEqual(strip_malayalam(data), {'a_en': 'x', 'a_ta': 'y', 'card': {'en': 'x', 'ta': 'y'}, 'ml': 'kept without en'})


class MalayalamApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(('127.0.0.1', 0), Handler)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def chart(self, **extra):
        body = json.dumps(dict(BIRTHS[0], ayanamsa='Lahiri', **extra)).encode()
        req = urllib.request.Request(f'http://127.0.0.1:{self.server.server_port}/api/chart', data=body,
                                     headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as resp:
            return resp.read().decode()

    def test_malayalam_only_when_asked(self):
        plain, malayalam = self.chart(), self.chart(lang='ml')
        self.assertNotIn('_ml"', plain)
        self.assertIn('"reading_ml"', malayalam)
        self.assertIn('"summary_ml"', malayalam)
