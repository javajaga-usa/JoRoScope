"""South Indian (Tamil) Jathagam Tests
Verifies the Tamil calendar, Nazhigai, Dasa Irruppu, Mandi, Chevvai / Rahu-Ketu
Doshams, Papa Samyam, daily panchangam and the corrected Porutham tables.
"""
import unittest, sys
from pathlib import Path
from datetime import date, datetime
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from joroscope.core.engine import (
    calculate, calculate_match, calculate_gochara, sidereal_position, swe, AYAN, STARS, STAR_NADIS,
    VEDHA_GROUPS, EKA_NAKSHATRA_GRADE, utc_to_jd, sun_events
)
from joroscope.core.south_indian import (
    tamil_calendar, dasa_irruppu, chevvai_dosham, rahu_ketu_dosham, papa_points,
    compare_dosha_samyam, daily_panchangam, build_south_indian_details, NAK_SPAN
)

CHENNAI = dict(tz=ZoneInfo('Asia/Kolkata'), lat=13.0827, lon=80.2707)


def synthetic_planets(**signs):
    """Minimal planets dict: sign indices for the grahas, Aries by default."""
    names = ['Ascendant', 'Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
    planets = {n: {'sign_index': signs.get(n, 0), 'dignity': 'Neutral'} for n in names}
    if 'Ketu' not in signs:
        planets['Ketu']['sign_index'] = (planets['Rahu']['sign_index'] + 6) % 12
    return planets


class TamilCalendarTests(unittest.TestCase):
    def setUp(self):
        swe.set_sid_mode(AYAN['Lahiri'])

    def cal(self, d):
        return tamil_calendar(d, CHENNAI['tz'], CHENNAI['lat'], CHENNAI['lon'])

    def test_puthandu_after_sunset_sankranti(self):
        # Mesha sankranti on 13 Apr 2024 fell after sunset, so Chithirai 1 was 14 Apr.
        eve = self.cal(date(2024, 4, 13))
        self.assertEqual((eve['month'], eve['day'], eve['year']), ('Panguni', 31, 'Sobhakrith'))
        new_year = self.cal(date(2024, 4, 14))
        self.assertEqual((new_year['month'], new_year['day'], new_year['year']), ('Chithirai', 1, 'Krodhi'))

    def test_thai_pongal_and_year_rollover(self):
        # Thai belongs to the Tamil year that began the previous April.
        thai = self.cal(date(2025, 1, 14))
        self.assertEqual((thai['month'], thai['day'], thai['year']), ('Thai', 1, 'Krodhi'))
        self.assertEqual(self.cal(date(2025, 4, 14))['year'], 'Visuvavasu')
        self.assertEqual(self.cal(date(2026, 9, 27))['year'], 'Parabhava')

    def test_month_days_are_contiguous(self):
        prev = self.cal(date(2026, 8, 1))
        for offset in range(2, 60):
            cur = self.cal(date(2026, 8, offset) if offset <= 31 else date(2026, 9, offset - 31))
            if cur['month_index'] == prev['month_index']:
                self.assertEqual(cur['day'], prev['day'] + 1)
            else:
                self.assertEqual(cur['day'], 1)
                self.assertEqual(cur['month_index'], (prev['month_index'] + 1) % 12)
            prev = cur


class JathagaKurippuTests(unittest.TestCase):
    def sample(self, **changes):
        base = dict(name='Test', date='1990-01-01', time='12:00', timezone='Asia/Kolkata',
                    latitude='13.0827', longitude='80.2707', ayanamsa='Lahiri')
        base.update(changes)
        return base

    def test_day_birth_details(self):
        si = calculate(self.sample())['south_indian']
        self.assertEqual(si['vaaram']['en'], 'Monday')
        self.assertEqual(si['vedic_date'], '1990-01-01')
        self.assertTrue(si['nazhigai']['is_day_birth'])
        # 12:00 is about 5.5 hours after a ~06:31 sunrise: ~13.7 nazhigai
        self.assertEqual(si['nazhigai']['nazhigai'], 13)
        self.assertIn(si['mandi']['house'], range(1, 13))

    def test_pre_sunrise_birth_belongs_to_previous_vedic_day(self):
        si = calculate(self.sample(date='1994-05-18', time='04:30'))['south_indian']
        self.assertEqual(si['vedic_date'], '1994-05-17')
        self.assertEqual(si['vaaram']['en'], 'Tuesday')
        self.assertFalse(si['nazhigai']['is_day_birth'])
        self.assertGreater(si['nazhigai']['nazhigai'], 50)

    def test_mandi_is_ascendant_at_its_rising(self):
        r = calculate(self.sample())
        mandi = r['south_indian']['mandi']
        rise = datetime.fromisoformat(mandi['rises_local'])
        # Monday day birth: Mandi rises 22 of 30 day-ghatikas after sunrise
        sunrise = datetime.fromisoformat(r['south_indian']['sunrise_local'])
        sunset = datetime.fromisoformat(r['south_indian']['sunset_local'])
        expected = sunrise + (sunset - sunrise) * 22 / 30
        self.assertLess(abs((rise - expected).total_seconds()), 2)
        swe.set_sid_mode(AYAN['Lahiri'])
        asc = swe.houses_ex(utc_to_jd(rise.astimezone(ZoneInfo('UTC'))), 13.0827, 80.2707, b'P', swe.FLG_SIDEREAL)[1][0]
        self.assertAlmostEqual(asc, mandi['longitude'], places=2)

    def test_dasa_irruppu_matches_first_dasha(self):
        r = calculate(self.sample())
        irr = r['south_indian']['dasa_irruppu']
        first = r['dasha'][0]
        self.assertEqual(irr['lord'], first['lord'])
        remaining = datetime.fromisoformat(first['end']) - datetime.fromisoformat(r['utc'])
        self.assertAlmostEqual(irr['balance_years'], remaining.total_seconds() / 86400 / 365.25, places=4)

    def test_dasa_irruppu_notation(self):
        # Moon at the start of Ashwini: the full 7 years of Ketu remain.
        full = dasa_irruppu(0.0)
        self.assertEqual((full['lord'], full['years'], full['months'], full['days']), ('Ketu', 7, 0, 0))
        # Halfway through Bharani: 10 of Venus's 20 years remain.
        half = dasa_irruppu(40 / 3 * 1.5)
        self.assertEqual((half['lord'], half['years'], half['months']), ('Venus', 10, 0))


class DoshaTests(unittest.TestCase):
    def test_chevvai_from_lagna_moon_venus(self):
        # Lagna Aries, Moon Aries, Venus Aries; Mars in Cancer = 4th from all three.
        p = synthetic_planets(Mars=3, Jupiter=6)
        d = chevvai_dosham(p)
        self.assertTrue(d['effective'])
        self.assertEqual(d['severity'], 3)
        self.assertEqual({r['house'] for r in d['references']}, {4})

    def test_chevvai_sign_exemption(self):
        # Mars in Gemini in the 2nd from a Taurus Lagna is exempt.
        p = synthetic_planets(Ascendant=1, Moon=1, Venus=1, Mars=2, Jupiter=6)
        d = chevvai_dosham(p)
        self.assertFalse(d['present'])
        self.assertTrue(all(r['exempt'] for r in d['references']))

    def test_chevvai_jupiter_cancellation(self):
        # Mars in 7th (Libra) from Aries; Jupiter in Aries aspects it with its 7th aspect.
        p = synthetic_planets(Mars=6, Jupiter=0)
        d = chevvai_dosham(p)
        self.assertTrue(d['present'])
        self.assertTrue(d['cancelled'])
        self.assertFalse(d['effective'])

    def test_rahu_ketu_dosham(self):
        self.assertTrue(rahu_ketu_dosham(synthetic_planets(Rahu=7))['present'])  # Rahu 8th, Ketu 2nd
        self.assertFalse(rahu_ketu_dosham(synthetic_planets(Rahu=3, Moon=0))['present'])  # 4th / 10th

    def test_papa_points_and_samyam(self):
        # Everything in Aries except Ketu (Libra): Sun, Mars, Saturn and Rahu fall in the
        # 1st and Ketu in the 7th from each of the three references.
        heavy = synthetic_planets(Rahu=0)
        self.assertEqual(papa_points(heavy)['total'], 3 * 5)
        light = synthetic_planets(Sun=2, Mars=2, Saturn=2, Rahu=4)
        self.assertEqual(papa_points(light)['total'], 0)
        self.assertTrue(compare_dosha_samyam(heavy, light)['papa_balanced'])
        self.assertFalse(compare_dosha_samyam(light, heavy)['papa_balanced'])


class PoruthamTableTests(unittest.TestCase):
    def match(self, boy_star, girl_star, boy_sign=0, girl_sign=0):
        return calculate_match({'nakshatra_index': boy_star, 'sign_index': boy_sign},
                               {'nakshatra_index': girl_star, 'sign_index': girl_sign})

    def porutham(self, m, name):
        return next(p for p in m['poruthams'] if p['name'] == name)

    def test_vedha_groups_cover_every_star_once(self):
        covered = sorted(s for g in VEDHA_GROUPS for s in g)
        self.assertEqual(covered, list(range(27)))

    def test_vedha_pairs(self):
        ashwini, jyeshtha, magha, revati = 0, 17, 9, 26
        mrigashira, chitra, dhanishtha = 4, 13, 22
        for a, b in [(ashwini, jyeshtha), (magha, revati), (mrigashira, dhanishtha), (chitra, dhanishtha)]:
            self.assertFalse(self.porutham(self.match(a, b), 'Vedha Porutham')['passed'], (STARS[a], STARS[b]))
        # Ardra and Hasta are not a Vedha pair
        self.assertTrue(self.porutham(self.match(5, 12), 'Vedha Porutham')['passed'])

    def test_dina_counts_and_eka_nakshatra(self):
        self.assertTrue(self.porutham(self.match(1, 0), 'Dina Porutham')['passed'])     # count 2
        self.assertFalse(self.porutham(self.match(16, 0), 'Dina Porutham')['passed'])   # count 17
        self.assertFalse(self.porutham(self.match(26, 0), 'Dina Porutham')['passed'])   # count 27
        rohini = self.porutham(self.match(3, 3, 1, 1), 'Dina Porutham')
        bharani = self.porutham(self.match(1, 1), 'Dina Porutham')
        self.assertTrue(rohini['passed'])
        self.assertEqual(rohini['points'], 3)
        self.assertFalse(bharani['passed'])
        self.assertEqual(EKA_NAKSHATRA_GRADE.count('uthamam'), 8)
        self.assertEqual(EKA_NAKSHATRA_GRADE.count('avoid'), 8)

    def test_nadi_table(self):
        self.assertEqual([STAR_NADIS.count(n) for n in ('Aadi', 'Madhya', 'Antya')], [9, 9, 9])
        self.assertEqual(STAR_NADIS[3], 'Antya')  # Rohini
        # Ashwini (Aadi) and Ardra (Aadi) share a Nadi
        self.assertEqual(self.match(0, 5)['guna_milan']['nadi'], 0)

    def test_dosha_samyam_with_full_charts(self):
        boy = calculate(dict(name='B', date='1988-11-22', time='18:45', timezone='Asia/Kolkata',
                             latitude='11.0168', longitude='76.9558', ayanamsa='Lahiri'))
        girl = calculate(dict(name='G', date='1994-05-18', time='08:30', timezone='Asia/Kolkata',
                              latitude='9.9252', longitude='78.1198', ayanamsa='Lahiri'))
        m = calculate_match(boy, girl)
        ds = m['dosha_samyam']
        self.assertIsNotNone(ds)
        self.assertEqual(ds['papa_balanced'], ds['boy']['papa']['total'] >= ds['girl']['papa']['total'])
        self.assertIsNone(self.match(0, 1)['dosha_samyam'])


class ClassicalTableTests(unittest.TestCase):
    def match(self, boy_star, boy_sign, girl_star, girl_sign):
        return calculate_match({'nakshatra_index': boy_star, 'sign_index': boy_sign},
                               {'nakshatra_index': girl_star, 'sign_index': girl_sign})['guna_milan']

    def test_trimsamsa_venus_portion_of_odd_signs_is_libra(self):
        from joroscope.core.engine import calculate_vargas
        self.assertEqual(calculate_vargas(27.0)['D30'], 6)       # Aries 27°: Libra
        self.assertEqual(calculate_vargas(30 + 27.0)['D30'], 7)  # Taurus 27°: Scorpio

    def test_bhakoot_doshas(self):
        # Girl in Aries; the boy's sign counted from hers
        for dist, pts in [(1, 7), (2, 0), (3, 7), (4, 7), (5, 0), (6, 0), (7, 7), (8, 0), (9, 0), (10, 7), (11, 7), (12, 0)]:
            self.assertEqual(self.match(0, dist - 1, 0, 0)['bhakoot'], pts, dist)

    def test_tara_is_judged_from_both_stars(self):
        self.assertEqual(self.match(0, 0, 0, 0)['tara'], 3)    # Janma both ways
        self.assertEqual(self.match(2, 0, 0, 0)['tara'], 1.5)  # 3rd (Vipat) one way, 26th (Mitra) the other
        self.assertEqual(self.match(4, 1, 0, 0)['tara'], 1.5)  # 5th (Pratyak) one way only

    def test_graha_maitri_matrix(self):
        # Moon signs Leo (Sun) and Cancer (Moon): mutual friends
        self.assertEqual(self.match(9, 4, 7, 3)['graha_maitri'], 5)
        # Taurus (Venus) and Leo (Sun): mutual enemies
        self.assertEqual(self.match(3, 1, 9, 4)['graha_maitri'], 0)
        # Gemini (Mercury) and Cancer (Moon): the Moon befriends Mercury, Mercury treats the Moon as an enemy
        self.assertEqual(self.match(5, 2, 7, 3)['graha_maitri'], 1)


class DailyPanchangamTests(unittest.TestCase):
    def test_local_timings_and_end_times(self):
        p = daily_panchangam('2026-09-27', '21:00:00', 'Asia/Kolkata', 13.0827, 80.2707,
                             natal_star=23, natal_sign=10)
        self.assertEqual(p['vaaram']['en'], 'Sunday')
        self.assertEqual(p['weekday'], 'Sunday')
        # Sunday Rahu Kalam is the last eighth of the day, ending at sunset
        self.assertTrue(p['rahu_kalam_local'].endswith(p['sunset_local']))
        self.assertEqual(p['soolam']['direction'], 'West')
        moment = datetime.fromisoformat(p['moment_local'])
        for anga, end in p['ends_local'].items():
            self.assertGreater(datetime.fromisoformat(end), moment, anga)
        self.assertEqual((p['moon_sign']['index'] - p['chandrashtamam']['sign_index']) % 12, 7)
        self.assertIn(p['personal']['tara']['quality'], ('good', 'bad', 'mixed'))
        self.assertEqual(p['tamil_calendar']['month'], 'Purattasi')

    def test_rejects_polar_latitude(self):
        with self.assertRaises(ValueError):
            daily_panchangam('2026-06-21', '12:00:00', 'Europe/Oslo', 78.2, 15.6)


class GocharaTests(unittest.TestCase):
    def chart(self, ayanamsa='Lahiri'):
        return calculate(dict(name='T', date='1990-01-01', time='12:00', timezone='Asia/Kolkata',
                              latitude='13.0827', longitude='80.2707', ayanamsa=ayanamsa))

    def test_reported_ayanamsa_matches_chosen_system(self):
        for ayanamsa in ('Lahiri', 'Raman', 'Krishnamurti', 'Fagan-Bradley'):
            r = self.chart(ayanamsa)
            swe.set_sid_mode(AYAN[ayanamsa])
            self.assertAlmostEqual(r['ayanamsa_degrees'], swe.get_ayanamsa_ut(r['julian_day']), places=6)

    def test_transit_chapter_uses_real_positions(self):
        r = self.chart()
        moon_sign = r['planets']['Moon']['sign_index']
        saturn = r['gochara']['planets']['Saturn']
        self.assertEqual(r['predictions']['transits']['saturn']['house_from_moon'],
                         (saturn['sign_index'] - moon_sign) % 12 + 1)
        self.assertEqual(saturn['bindus'], r['ashtakavarga']['BAV']['Saturn'][saturn['sign_index']])

    def test_saturn_life_cycles(self):
        r = self.chart()  # Aquarius Moon
        cycles = r['gochara']['saturn_cycles']
        self.assertEqual([c['start'] for c in cycles], sorted(c['start'] for c in cycles))
        current = next(c for c in cycles if c['kind'] == 'sade_sati' and c['start'][:4] == '2020')
        # Saturn entered sidereal Capricorn (12th from Aquarius) on 24 Jan 2020 and Pisces on 29 Mar 2025
        self.assertEqual(current['start'][:10], '2020-01-24')
        self.assertEqual([ph['phase'] for ph in current['phases']], [1, 2, 3])
        self.assertEqual(current['phases'][2]['start'][:10], '2025-03-29')
        for c in cycles:
            self.assertLess(c['start'], c['end'])
            for ph in c['phases']:
                self.assertTrue(c['start'] <= ph['start'] < ph['end'] <= c['end'])
        # Roughly three Ezharai Sani cycles in a hundred years
        self.assertIn(sum(c['kind'] == 'sade_sati' for c in cycles), (3, 4))

    def test_fixed_date_gochara_and_peyarchi(self):
        r = self.chart()
        swe.set_sid_mode(AYAN['Lahiri'])
        jd = utc_to_jd(datetime(2026, 9, 28, 12, tzinfo=ZoneInfo('UTC')))
        g = calculate_gochara(jd, r['planets'], r['ashtakavarga'])
        self.assertEqual(g['planets']['Saturn']['sign'], 'Pisces')
        self.assertEqual(g['planets']['Jupiter']['sign'], 'Cancer')
        self.assertAlmostEqual((g['planets']['Ketu']['longitude'] - g['planets']['Rahu']['longitude']) % 360, 180)
        peyarchi = {p['planet']: p for p in g['peyarchi']}
        self.assertEqual((peyarchi['Saturn']['to_sign'], peyarchi['Saturn']['date'][:7]), ('Aries', '2027-06'))
        self.assertEqual((peyarchi['Jupiter']['to_sign'], peyarchi['Jupiter']['date'][:7]), ('Leo', '2026-10'))
        self.assertEqual(peyarchi['Rahu']['date'], peyarchi['Ketu']['date'])
        # The sign really changes at the reported moment
        when = utc_to_jd(datetime.fromisoformat(peyarchi['Jupiter']['date']))
        self.assertEqual(int(sidereal_position(when - 0.01, swe.JUPITER)[0] // 30), 3)
        self.assertEqual(int(sidereal_position(when + 0.01, swe.JUPITER)[0] // 30), 4)


class PersonalAlmanacTests(unittest.TestCase):
    def details(self, now):
        r = calculate(dict(name='T', date='1990-01-01', time='12:00', timezone='Asia/Kolkata',
                           latitude='13.0827', longitude='80.2707', ayanamsa='Lahiri'))
        swe.set_sid_mode(AYAN['Lahiri'])
        return r, build_south_indian_details(r['planets'], datetime.fromisoformat(r['utc']), 'Asia/Kolkata',
                                             13.0827, 80.2707, now=now)

    def test_hora_sequence(self):
        p = daily_panchangam('2026-09-28', '10:30:00', 'Asia/Kolkata', 13.0827, 80.2707)
        lords = [h['lord'] for h in p['horas']]
        self.assertEqual(len(lords), 24)
        self.assertEqual(lords[:8], ['Moon', 'Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon'])
        self.assertEqual(lords[-1], 'Jupiter')  # so the next sunrise opens with Mars: Tuesday
        self.assertEqual(sum(h['current'] for h in p['horas']), 1)
        self.assertEqual(p['horas'][11]['end_local'][11:16], p['sunset_local'])

    def test_upcoming_chandrashtamam(self):
        now = datetime(2026, 9, 28, 12, tzinfo=ZoneInfo('UTC'))
        r, si = self.details(now)
        ch = si['upcoming']['chandrashtamam']
        self.assertEqual((r['planets']['Moon']['sign_index'] + 7) % 12, ch['sign_index'])
        for period in ch['periods']:
            start = datetime.fromisoformat(period['start_local'])
            end = datetime.fromisoformat(period['end_local'])
            self.assertGreater(end, now)
            self.assertTrue(1.8 < (end - start).total_seconds() / 86400 < 2.8)
            mid = utc_to_jd(start + (end - start) / 2)
            self.assertEqual(int(sidereal_position(mid, swe.MOON)[0] // 30), ch['sign_index'])

    def test_star_birthday_is_birth_star_at_sunrise_in_birth_month(self):
        now = datetime(2026, 9, 28, 12, tzinfo=ZoneInfo('UTC'))
        r, si = self.details(now)
        sb = si['upcoming']['star_birthday']
        self.assertEqual(sb['month'], si['tamil_calendar']['month'])
        birth_star = STARS.index(r['planets']['Moon']['nakshatra'])
        for iso in sb['dates']:
            d = date.fromisoformat(iso)
            self.assertGreaterEqual(d, now.date())
            self.assertEqual(self.cal_month(d), si['tamil_calendar']['month_index'])
            sunrise = sun_events(d, CHENNAI['tz'], CHENNAI['lat'], CHENNAI['lon'])['sunrise']
            self.assertEqual(int(sidereal_position(sunrise, swe.MOON)[0] / NAK_SPAN), birth_star)

    def cal_month(self, d):
        return tamil_calendar(d, CHENNAI['tz'], CHENNAI['lat'], CHENNAI['lon'])['month_index']


class GowriBhavaSandhiTests(unittest.TestCase):
    def test_gowri_matches_published_tables_and_rahu_kalam(self):
        p = daily_panchangam('2026-09-28', '10:00:00', 'Asia/Kolkata', 13.0827, 80.2707)  # Monday
        gowri = p['gowri']
        self.assertEqual(len(gowri), 16)
        self.assertEqual([g['name'] for g in gowri[:8]],
                         ['Amirdha', 'Visham', 'Rogam', 'Laabam', 'Dhanam', 'Sugam', 'Soram', 'Uthi'])
        visham = next(g for g in gowri[:8] if g['name'] == 'Visham')
        self.assertEqual(f"{visham['start_local'][11:16]} - {visham['end_local'][11:16]}", p['rahu_kalam_local'])
        self.assertEqual(sum(g['current'] for g in gowri), 1)
        self.assertEqual(gowri[7]['end_local'], gowri[8]['start_local'])  # night starts at sunset

    def test_gowri_day_visham_is_always_rahu_kalam(self):
        from joroscope.core.south_indian import GOWRI_DAY
        rahu_segment = [8, 2, 7, 5, 6, 4, 3]  # Sunday first, 1-based
        for weekday, row in enumerate(GOWRI_DAY):
            self.assertEqual(row.index('Visham') + 1, rahu_segment[weekday])

    def test_dasa_sandhi(self):
        from joroscope.core.south_indian import dasa_sandhi
        now = datetime(2026, 1, 1, tzinfo=ZoneInfo('UTC'))
        rows = lambda *ends: [{'lord': lord, 'end': end} for lord, end in zip(('Venus', 'Sun', 'Moon'), ends)]
        close = dasa_sandhi(rows('2030-03-01T00:00:00+00:00', '2036-03-01T00:00:00+00:00', '2046-03-01T00:00:00+00:00'),
                            rows('2030-06-01T00:00:00+00:00', '2040-03-01T00:00:00+00:00', '2050-03-01T00:00:00+00:00'), now)
        self.assertTrue(close['present'])
        self.assertEqual((close['conflicts'][0]['gap_days'], close['conflicts'][0]['groom_to']), (92, 'Sun'))
        apart = dasa_sandhi(rows('2030-03-01T00:00:00+00:00', '2036-03-01T00:00:00+00:00', '2046-03-01T00:00:00+00:00'),
                            rows('2031-06-01T00:00:00+00:00', '2040-03-01T00:00:00+00:00', '2050-03-01T00:00:00+00:00'), now)
        self.assertFalse(apart['present'])

    def test_sripati_bhavas(self):
        from joroscope.core.engine import bhava_of
        differs = 0
        for d, t in [('1990-01-01', '12:00'), ('1994-05-18', '08:30'), ('2001-07-15', '03:10'), ('1975-02-20', '17:25')]:
            r = calculate(dict(name='T', date=d, time=t, timezone='Asia/Kolkata', latitude='13.0827',
                               longitude='80.2707', ayanamsa='Lahiri'))
            bc = r['bhava_chakra']
            self.assertAlmostEqual(bc['madhya'][0], r['planets']['Ascendant']['longitude'], places=4)
            self.assertEqual(r['planets']['Ascendant']['bhava'], 1)
            for p in r['planets'].values():
                self.assertEqual(p['bhava'], bhava_of(p['longitude'], bc['sandhi']))
                self.assertIn(abs(p['bhava'] - p['house']) % 12, (0, 1, 11))  # never more than one house away
                differs += p['bhava'] != p['house']
        self.assertGreater(differs, 0)


if __name__ == '__main__':
    unittest.main()
