import unittest, math, sys
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from joroscope.core.engine import (
    calculate, local_to_utc, placement, dasha, calculate_vargas,
    calculate_match, calculate_panchangam, YEAR, swe
)

class ChartTests(unittest.TestCase):
    def sample(self, **changes):
        return dict(name='Test', date='1990-01-01', time='12:00', timezone='Asia/Kolkata', latitude='13.0827', longitude='80.2707', ayanamsa='Lahiri', **changes)

    def test_j2000_reference(self):
        # Fixed regression reference for the bundled Swiss Ephemeris solar longitude.
        self.assertAlmostEqual(swe.calc_ut(2451545.0, swe.SUN, swe.FLG_MOSEPH)[0][0], 280.36892, places=4)

    def test_timezone(self):
        self.assertEqual(local_to_utc('1990-01-01', '12:00', 'Asia/Kolkata').isoformat(), '1990-01-01T06:30:00+00:00')

    def test_dst_gap_and_fold(self):
        with self.assertRaises(ValueError): local_to_utc('2024-03-10', '02:30', 'America/New_York')
        with self.assertRaises(ValueError): local_to_utc('2024-11-03', '01:30', 'America/New_York')
        a = local_to_utc('2024-11-03', '01:30', 'America/New_York', 0)
        b = local_to_utc('2024-11-03', '01:30', 'America/New_York', 1)
        self.assertEqual((b - a).total_seconds(), 3600)

    def test_chart_invariants(self):
        r = calculate(self.sample())
        p = r['planets']
        self.assertEqual(len(p), 10)
        self.assertAlmostEqual((p['Ketu']['longitude'] - p['Rahu']['longitude']) % 360, 180)
        self.assertEqual(p['Ascendant']['house'], 1)
        for v in p.values():
            self.assertTrue(0 <= v['longitude'] < 360)
            self.assertIn(v['pada'], range(1, 5))
            self.assertIn(v['house'], range(1, 13))

    def test_navamsa_boundaries(self):
        # Movable Aries starts Aries; fixed Taurus starts Capricorn; dual Gemini starts Libra.
        self.assertEqual(placement(0)['navamsa'], 0)
        self.assertEqual(placement(30)['navamsa'], 9)
        self.assertEqual(placement(60)['navamsa'], 6)
        self.assertEqual(placement(359.99)['navamsa'], 11)

    def test_dasha_balance_and_continuity(self):
        birth = datetime(2000, 1, 1, tzinfo=timezone.utc)
        periods = dasha(20 / 3, birth)
        self.assertEqual(periods[0]['lord'], 'Ketu')
        self.assertAlmostEqual((birth - datetime.fromisoformat(periods[0]['start'])).total_seconds() / 86400, 3.5 * YEAR)
        for i, d in enumerate(periods):
            self.assertEqual(d['subperiods'][0]['start'], d['start'])
            self.assertLess(abs((datetime.fromisoformat(d['subperiods'][-1]['end']) - datetime.fromisoformat(d['end'])).total_seconds()), .001)
            if i: self.assertEqual(periods[i - 1]['end'], d['start'])
        span = datetime.fromisoformat(periods[-1]['end']) - datetime.fromisoformat(periods[0]['start'])
        self.assertAlmostEqual(span.total_seconds() / 86400, 120 * YEAR)

    def test_reject_invalid_coordinates(self):
        for value in ('nan', 'inf', '90'):
            p = self.sample()
            p['latitude'] = value
            with self.assertRaises(ValueError): calculate(p)

    def test_equivalent_utc(self):
        a = self.sample()
        b = self.sample()
        b.update(time='06:30', timezone='UTC')
        self.assertEqual(calculate(a)['planets'], calculate(b)['planets'])

    # --- New Enhanced Tests ---
    def test_varga_calculations(self):
        # Test D1-D60 vargas for Aries 2° and Taurus 2°
        v1 = calculate_vargas(2.0)  # Aries 2° (Odd sign)
        self.assertEqual(v1['D1'], 0)  # Aries
        self.assertEqual(v1['D2'], 4)  # Leo (Hora odd 0-15 = Sun/Leo)
        self.assertEqual(v1['D3'], 0)  # Drekkana 0-10 = same sign
        self.assertEqual(v1['D9'], 0)  # Navamsa 0-3.33° = Aries (0)
        self.assertEqual(v1['D10'], 0) # Dasamsa 0-3° = Aries (0)
        self.assertEqual(v1['D30'], 0) # Trimsamsa 0-5° = Aries (0)

        v2 = calculate_vargas(32.0)  # Taurus 2° (Even sign)
        self.assertEqual(v2['D1'], 1)  # Taurus
        self.assertEqual(v2['D2'], 3)  # Cancer (Hora even 0-15 = Moon/Cancer)
        self.assertEqual(v2['D3'], 1)  # Taurus
        self.assertEqual(v2['D30'], 1) # Trimsamsa 0-5° even = Taurus

        # Check all 14 vargas exist
        varga_keys = ['D1', 'D2', 'D3', 'D4', 'D7', 'D9', 'D10', 'D12', 'D16', 'D20', 'D24', 'D27', 'D30', 'D60']
        for k in varga_keys:
            self.assertIn(k, v1)
            self.assertTrue(0 <= v1[k] < 12)

    def test_ashtakavarga_invariant(self):
        res = calculate(self.sample())
        sav = res['ashtakavarga']['SAV']
        self.assertEqual(len(sav), 12)
        # Parashara Sarvashtakavarga invariant total sum is 337
        self.assertEqual(sum(sav), 337)
        self.assertEqual(res['ashtakavarga']['total_points'], 337)

    def test_pratyantardasa_levels(self):
        res = calculate(self.sample())
        d = res['dasha']
        self.assertEqual(len(d), 9)
        first_bhukti = d[0]['subperiods'][0]
        self.assertIn('pratyantars', first_bhukti)
        self.assertEqual(len(first_bhukti['pratyantars']), 9)
        # Check start of first pratyantar matches bhukti start
        self.assertEqual(first_bhukti['pratyantars'][0]['start'], first_bhukti['start'])

    def test_panchangam_and_muhurthas(self):
        res = calculate(self.sample())
        panch = res['panchanga']
        self.assertIn('tithi', panch)
        self.assertTrue(1 <= panch['tithi'] <= 30)
        self.assertIn('yoga_number', panch)
        self.assertTrue(1 <= panch['yoga_number'] <= 27)
        self.assertIn('karana_name', panch)
        self.assertIn('sunrise_utc', panch)
        self.assertIn('sunset_utc', panch)
        self.assertIn('rahu_kalam_utc', panch)
        self.assertIn('abhijit_muhurtham_utc', panch)

    def test_yogas_and_doshas(self):
        res = calculate(self.sample())
        self.assertIn('yogas', res)
        self.assertIn('doshas', res)
        self.assertIn('manglik', res['doshas'])
        self.assertIn('kaal_sarp', res['doshas'])

    def test_horoscope_matching(self):
        boy = {'nakshatra_index': 0, 'sign_index': 0}   # Ashwini, Aries
        girl = {'nakshatra_index': 1, 'sign_index': 0}  # Bharani, Aries
        match = calculate_match(boy, girl)
        self.assertEqual(len(match['poruthams']), 10)
        self.assertIn('guna_milan', match)
        self.assertTrue(0 <= match['guna_milan']['total_score'] <= 36)
        self.assertIn('verdict', match)

    def test_comprehensive_predictions(self):
        res = calculate(self.sample())
        self.assertIn('predictions', res)
        preds = res['predictions']
        self.assertIn('overview', preds)
        self.assertIn('bhavas', preds)
        self.assertEqual(len(preds['bhavas']), 12)
        self.assertIn('planets_in_houses', preds)
        self.assertEqual(len(preds['planets_in_houses']), 9)
        self.assertIn('dasa_forecast', preds)
        self.assertIn('transits', preds)
        self.assertIn('lucky_factors', preds)
        self.assertIn('primary_gem', preds['lucky_factors'])

    def test_approved_studies_predictions(self):
        res = calculate(self.sample())
        preds = res['predictions']

        # 1. Jaimini Karakas
        self.assertIn('jaimini_karakas', preds)
        jk = preds['jaimini_karakas']
        self.assertEqual(len(jk['karakas']), 7)
        self.assertEqual(jk['karakas'][0]['code'], 'AK')
        self.assertEqual(jk['karakas'][1]['code'], 'AmK')
        # Check strictly non-increasing order of degrees
        degs = [k['degree_in_sign'] for k in jk['karakas']]
        self.assertTrue(all(degs[i] >= degs[i+1] for i in range(len(degs)-1)))
        self.assertIn('karakamsha', jk)
        self.assertIn('sign', jk['karakamsha'])

        # 2. Double Transit
        self.assertIn('double_transit', preds)
        dt = preds['double_transit']
        self.assertEqual(len(dt['milestones']), 4)
        for m in dt['milestones']:
            self.assertTrue(0 <= m['score'] <= 100)
            self.assertIn('status_en', m)
            self.assertIn('desc_en', m)

        # 3. Career D-10
        self.assertIn('career_d10', preds)
        c10 = preds['career_d10']
        self.assertEqual(len(c10['all_archetypes']), 5)
        self.assertIn('top_archetype', c10)
        self.assertTrue(0 <= c10['top_archetype']['score'] <= 100)

        # 4. Ayur-Jyotish & Tridosha
        self.assertIn('ayur_jyotish', preds)
        ayur = preds['ayur_jyotish']
        self.assertEqual(ayur['vata_percentage'] + ayur['pitta_percentage'] + ayur['kapha_percentage'], 100)
        self.assertIn('prakriti_en', ayur)
        self.assertIn('anatomical_vulnerabilities_en', ayur)

        # 5. Kakshya Transits
        self.assertIn('kakshya_transits', preds)
        kt = preds['kakshya_transits']
        self.assertIn('saturn', kt)
        self.assertIn('jupiter', kt)
        self.assertEqual(len(kt['saturn']['kakshya_timeline']), 8)
        self.assertEqual(len(kt['jupiter']['kakshya_timeline']), 8)

    def test_advanced_astrological_calculations(self):
        """Test the 6 advanced calculation and prediction modules."""
        chart = calculate({
            'name': 'Test Advance', 'date': '1990-08-20', 'time': '10:30:00',
            'timezone': 'Asia/Kolkata', 'city': 'Chennai',
            'latitude': 13.0827, 'longitude': 80.2707, 'ayanamsa': 'Lahiri'
        })
        preds = chart['predictions']

        # 1. Shadbala
        self.assertIn('shadbala', preds)
        sb = preds['shadbala']
        self.assertEqual(len(sb['planets']), 7)
        self.assertIn('dominant_planet', sb)
        self.assertIn('vulnerable_planet', sb)
        for p in sb['planets']:
            self.assertTrue(p['total_virupas'] > 0)
            self.assertTrue(p['total_rupas'] > 0)
            self.assertIn('reading_en', p)
            self.assertIn('reading_ta', p)

        # 2. KP System
        self.assertIn('kp_system', preds)
        kp = preds['kp_system']
        self.assertEqual(len(kp['cusps']), 12)
        self.assertEqual(len(kp['planets']), 9)
        self.assertIn('cuspal_predictions', kp)
        for c_key in ['cusp_1', 'cusp_2', 'cusp_5', 'cusp_7', 'cusp_10', 'cusp_11']:
            self.assertIn(c_key, kp['cuspal_predictions'])
            self.assertIn('sub_lord', kp['cuspal_predictions'][c_key])
            self.assertIn('reading_ta', kp['cuspal_predictions'][c_key])

        # 3. Bhrigu Nandi Nadi
        self.assertIn('bhrigu_nandi_nadi', preds)
        bnn = preds['bhrigu_nandi_nadi']
        self.assertEqual(len(bnn['trines']), 4)
        self.assertTrue(len(bnn['sutras']) >= 1)
        for s in bnn['sutras']:
            self.assertIn('title_en', s)
            self.assertIn('title_ta', s)
            self.assertIn('significance_ta', s)

        # 4. Planetary Avasthas
        self.assertIn('avasthas', preds)
        av = preds['avasthas']
        self.assertEqual(len(av['avasthas']), 7)
        for a in av['avasthas']:
            self.assertTrue(0 <= a['fruit_potency'] <= 100)
            self.assertIn('baladi_ta', a)
            self.assertIn('jagradadi_ta', a)

        # 5. Nakshatra Pada Reading
        self.assertIn('pada_reading', preds)
        pada = preds['pada_reading']
        self.assertIn(pada['pada'], [1, 2, 3, 4])
        self.assertIn('reading_en', pada)
        self.assertIn('reading_ta', pada)
        self.assertIn('element', pada)

        # 6. Sensitive Sahams
        self.assertIn('sahams', preds)
        sh = preds['sahams']
        self.assertEqual(len(sh['sahams']), 5)
        for s in sh['sahams']:
            self.assertTrue(0 <= s['longitude'] < 360)
            self.assertIn('reading_en', s)
            self.assertIn('reading_ta', s)
            self.assertTrue(1 <= s['house'] <= 12)

    def test_dasa_bhukti_timeline_predictions(self):
        """Test chronological 81 Dasa-Bhukti timeline predictions and annual projections."""
        chart = calculate({
            'name': 'Sri Raman', 'date': '1990-01-01', 'time': '12:00:00',
            'timezone': 'Asia/Kolkata', 'city': 'Chennai',
            'latitude': 13.0827, 'longitude': 80.2707, 'ayanamsa': 'Lahiri'
        })
        preds = chart['predictions']
        self.assertIn('timeline_predictions', preds)
        tp = preds['timeline_predictions']

        # 1. Full 81 Dasa-Bhukti periods verification
        self.assertEqual(tp['total_periods'], 81)
        self.assertEqual(len(tp['periods']), 81)

        active_count = 0
        for p in tp['periods']:
            self.assertIn('dasa_lord', p)
            self.assertIn('bhukti_lord', p)
            self.assertIn('start_date', p)
            self.assertIn('end_date', p)
            self.assertTrue(p['age_start'] <= p['age_end'])
            self.assertTrue(1 <= p['potency'] <= 5)
            self.assertIn(p['mutual_class'], ['trine', 'kendra', 'growth', 'friction', 'transition'])
            self.assertIn('title_en', p)
            self.assertIn('title_ta', p)
            self.assertIn('career_en', p)
            self.assertIn('career_ta', p)
            self.assertIn('wealth_en', p)
            self.assertIn('wealth_ta', p)
            self.assertIn('health_en', p)
            self.assertIn('health_ta', p)
            self.assertIn('family_en', p)
            self.assertIn('family_ta', p)
            self.assertIn('remedy_en', p)
            self.assertIn('remedy_ta', p)
            if p['is_active']:
                active_count += 1

        self.assertEqual(active_count, 1, "Exactly one Dasa-Bhukti should be currently active")

        # 2. Active Spotlight Card verification
        sp = tp['active_spotlight']
        self.assertIsNotNone(sp)
        self.assertTrue(sp['elapsed_days'] >= 0)
        self.assertTrue(sp['remaining_days'] >= 0)
        self.assertTrue(0 <= sp['percent'] <= 100)
        self.assertTrue(sp['age'] > 0)
        self.assertTrue(1 <= sp['potency'] <= 5)
        self.assertIn('strategic_advice_en', sp)
        self.assertIn('strategic_advice_ta', sp)
        self.assertIn('primary_remedy_en', sp)
        self.assertIn('primary_remedy_ta', sp)

        # 3. 10-Year Annual Milestones Projections
        ann = tp['annual_projections']
        self.assertEqual(len(ann), 11)
        current_year_count = 0
        for a in ann:
            self.assertTrue(0 <= a['score'] <= 100)
            self.assertIn('year', a)
            self.assertIn('age', a)
            self.assertIn('theme_en', a)
            self.assertIn('theme_ta', a)
            self.assertIn('icon', a)
            if a['is_current_year']:
                current_year_count += 1
        self.assertEqual(current_year_count, 1, "Exactly one annual projection should be marked current year")

if __name__ == '__main__':
    unittest.main(verbosity=2)
