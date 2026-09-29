"""Shared verification marks: consent, nothing personal stored, one entry per browser, and the accuracy
report open only to the owner."""

import json
import os
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from joroscope.core import engine, feedback
from joroscope.server import Handler

BIRTH = dict(name='Feedback Test', date='1990-01-01', time='12:00', timezone='Asia/Kolkata', latitude=13.0827,
             longitude=80.2707, ayanamsa='Lahiri')


class FeedbackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.env = mock.patch.dict(os.environ, {'JOROSCOPE_DATA_DIR': cls.tmp.name, 'JOROSCOPE_OWNER_PASSCODE': 'owner-7'})
        cls.env.start()
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.url = f'http://127.0.0.1:{cls.server.server_port}'
        statements = engine.calculate(BIRTH)['predictions']['parisodhanai']['statements']
        marriage = next(s for s in statements if s.get('event') == 'marriage')
        cls.inside = marriage['windows'][0]['start']
        cls.marks = {'siblings_elder': {'mark': 'right'}, 'father': {'mark': 'wrong'},
                     'event_marriage': {'mark': 'right', 'date': cls.inside},
                     'family': {'elder_brothers': '0', 'elder_sisters': '3'}}

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.env.stop()
        cls.tmp.cleanup()

    def post(self, path, body, headers=None):
        req = urllib.request.Request(self.url + path, data=json.dumps(body).encode(),
                                     headers={'Content-Type': 'application/json', **(headers or {})})
        try:
            with urllib.request.urlopen(req) as resp:
                return resp.status, json.loads(resp.read())
        except urllib.error.HTTPError as err:
            return err.code, json.loads(err.read())

    def test_sharing_needs_consent_and_stores_nothing_personal(self):
        status, _ = self.post('/api/feedback', {'birth': BIRTH, 'marks': self.marks, 'submission_id': 'abcdef123456'})
        self.assertEqual(status, 400)
        for _ in range(2):  # sharing again from the same browser replaces the entry
            status, body = self.post('/api/feedback', {'birth': BIRTH, 'marks': self.marks, 'submission_id': 'abcdef123456', 'consent': True})
            self.assertEqual((status, body['items'], body['siblings']), (200, 3, 1))
        stored = feedback.data_file().read_text()
        for personal in ('1990-01-01', '12:00', 'Feedback Test', '13.08', 'Kolkata'):
            self.assertNotIn(personal, stored)
        mine = [e for e in feedback.load() if e['id'] == 'abcdef123456']
        self.assertEqual(len(mine), 1)
        entry = mine[0]
        marriage = next(i for i in entry['items'] if i['key'] == 'event_marriage')
        self.assertTrue(marriage['in_window'])
        self.assertEqual(entry['siblings'][0]['actual'], [0, 3])

    def test_report_is_for_the_owner(self):
        self.post('/api/feedback', {'birth': BIRTH, 'marks': self.marks, 'submission_id': 'report-test-1', 'consent': True})
        status, report = self.post('/api/feedback-report', {})
        self.assertEqual(status, 200)  # on this computer
        self.assertGreaterEqual(report['entries'], 1)
        self.assertIn('siblings_elder', [s['key'] for s in report['statements']])
        tunnel = {'Cf-Connecting-IP': '203.0.113.9'}
        self.assertEqual(self.post('/api/feedback-report', {'passcode': 'guess'}, tunnel)[0], 401)
        self.assertEqual(self.post('/api/feedback-report', {'passcode': 'owner-7'}, tunnel)[0], 200)
