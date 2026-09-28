"""JoRoScope Muhurtham Finder
Auspicious daytime windows for common undertakings by the classical Muhurta rules (Muhurta
Chintamani): an event-specific nakshatra, a good weekday and tithi, clear of the difficult
parts of the nitya yogas, no Vishti karana, outside Rahu Kalam, Yamagandam and Gulika, and for
marriage and griha pravesam not in Aadi, Purattasi or Margazhi. With the person's birth star
and Moon sign it also applies Tara and Chandra Bala. The Tamil (Amirthathi) yogam must be Siddha
or Amirtha, and each window keeps one rising Lagna that passes Lagna Shuddhi: no malefic in the
8th, the Moon not in the 6th, 8th or 12th, and not the person's Janma Ashtama rasi. A clear 7th
for marriage is noted as a preference, as Tamil almanacs treat it. Regional customs still vary, so the final time is for the family astrologer to confirm.
"""
import math
from datetime import timedelta

from .engine import (AYAN, NITYA_YOGAS, KARANAS, SIGNS, STARS, TAMIL, TAMIL_STARS, TITHIS, swe, local_to_utc,
                     sidereal_position, sun_events)
from .south_indian import (
    TARAS, CHANDRA_BALAM_HOUSES, VAARAM, TITHI_TA, NAK_SPAN, _elongation, _moon, _yoga_sum, _local_iso, _zone,
    tamil_calendar, tamil_yogam
)

# Nakshatra indices (Ashwini = 0) favoured for each undertaking
MUHURTHA_EVENTS = {
    'marriage': dict(en='Marriage (Vivaham)', ta='திருமணம்', stars=(3, 4, 9, 11, 12, 14, 16, 18, 20, 25, 26),
                     avoid_months=(3, 5, 8)),
    'griha_pravesam': dict(en='House-warming (Griha Pravesam)', ta='கிரகப் பிரவேசம்', stars=(3, 4, 11, 13, 16, 20, 22, 23, 25, 26),
                           avoid_months=(3, 5, 8)),
    'business': dict(en='Opening a business', ta='தொழில் / கடை திறப்பு', stars=(0, 3, 4, 7, 11, 12, 13, 16, 20, 21, 25, 26),
                     avoid_months=()),
    'vehicle': dict(en='Buying a vehicle', ta='வாகனம் வாங்குதல்', stars=(0, 4, 6, 7, 12, 13, 14, 16, 21, 22, 23, 26),
                    avoid_months=()),
    'general': dict(en='Any auspicious beginning', ta='பொதுவான சுப காரியம்',
                    stars=(0, 3, 4, 6, 7, 11, 12, 13, 14, 16, 20, 21, 22, 23, 25, 26), avoid_months=())
}
GOOD_WEEKDAYS = (0, 1, 3, 4, 5)             # Tuesday and Saturday avoided; Sunday allowed, as in Tamil practice
GOOD_TITHIS = (2, 3, 5, 7, 10, 11, 12, 13)  # within a paksha; Rikta (4, 9, 14), Ashtami and the 15th avoided
# Difficult nitya yogas (Muhurta Chintamani): Vyatipata and Vaidhriti are avoided whole, Parigha for
# its first half, the rest only for their first ghatis
YOGA_AVOID_GHATIS = {'Vishkambha': 5, 'Atiganda': 6, 'Shula': 7, 'Ganda': 6, 'Vyaghata': 9, 'Vajra': 9,
                     'Parigha': 30, 'Vyatipata': 60, 'Vaidhriti': 60}
TAMIL_MONTHS_AVOIDED = {3: ('Aadi', 'ஆடி'), 5: ('Purattasi', 'புரட்டாசி'), 8: ('Margazhi', 'மார்கழி')}
# Eighths of the daytime (1-8) under Rahu Kalam, Yamagandam and Gulika Kalam, Sunday first
RAHU_KALAM = (8, 2, 7, 5, 6, 4, 3)
YAMAGANDAM = (5, 4, 3, 2, 1, 7, 6)
GULIKA_KALAM = (7, 6, 5, 4, 3, 2, 1)
# Grahas checked for Lagna Shuddhi, and the benefics that strengthen a Lagna from a kendra
SHUDDHI_BODIES = (('Sun', swe.SUN), ('Moon', swe.MOON), ('Mars', swe.MARS), ('Mercury', swe.MERCURY),
                  ('Jupiter', swe.JUPITER), ('Venus', swe.VENUS), ('Saturn', swe.SATURN), ('Rahu', swe.MEAN_NODE))
LAGNA_BENEFICS = ('Jupiter', 'Venus')
LAGNA_MALEFICS = ('Sun', 'Mars', 'Saturn', 'Rahu', 'Ketu')
FIXED_SIGNS = (1, 4, 7, 10)
STEP_MINUTES = 10
MIN_WINDOW_MINUTES = 30


def _karana(elongation):
    half = int(elongation // 6) + 1  # 1-60
    if half == 1:
        return 'Kimstughna'
    if half >= 58:
        return KARANAS[7 + half - 58]  # Shakuni, Chatushpada, Naga
    return KARANAS[(half - 2) % 7]


def _graha_signs(jd):
    signs = {name: int(sidereal_position(jd, body)[0] // 30) for name, body in SHUDDHI_BODIES}
    signs['Ketu'] = (signs['Rahu'] + 6) % 12
    return signs


def _lagna(jd, lat, lon):
    return int(swe.houses_ex(jd, lat, lon, b'P', swe.FLG_SIDEREAL)[1][0] // 30)


def _lagna_ok(lagna, signs, natal_sign):
    house = lambda name: (signs[name] - lagna) % 12 + 1
    if any(house(name) == 8 for name in LAGNA_MALEFICS) or house('Moon') in (6, 8, 12):
        return False
    if natal_sign is not None and (lagna - natal_sign) % 12 + 1 == 8:
        return False
    return True


def _angas(jd):
    elongation = _elongation(jd)[0]
    tithi = int(elongation // 12) + 1
    yoga_value = _yoga_sum(jd)[0]
    yoga = NITYA_YOGAS[int(yoga_value / NAK_SPAN) % 27][0]
    elapsed_ghatis = (yoga_value % NAK_SPAN) / NAK_SPAN * 60  # a yoga spans about 60 ghatis
    return dict(tithi=tithi, star=int(_moon(jd)[0] / NAK_SPAN) % 27, moon_sign=int(_moon(jd)[0] // 30),
                yoga=yoga, yoga_good=elapsed_ghatis >= YOGA_AVOID_GHATIS.get(yoga, 0), karana=_karana(elongation))


def _day_rejections(event, weekday, tamil_month):
    reasons = []
    if weekday not in GOOD_WEEKDAYS:
        reasons.append(('weekday', f"{VAARAM[weekday][0]} is not a muhurtham weekday", f"{VAARAM[weekday][1]} முகூர்த்தத்திற்கு உகந்த நாள் அல்ல"))
    if tamil_month in event['avoid_months']:
        en, ta = TAMIL_MONTHS_AVOIDED[tamil_month]
        reasons.append(('month', f"{en} month is avoided for this event", f"இந்த நிகழ்விற்கு {ta} மாதம் தவிர்க்கப்படுகிறது"))
    return reasons


def _moment_ok(event, angas, natal_star, natal_sign, weekday):
    tithi = angas['tithi']
    in_paksha = (tithi - 1) % 15 + 1
    if angas['star'] not in event['stars'] or in_paksha not in GOOD_TITHIS:
        return False
    if tithi > 15 and in_paksha > 10:  # late in the waning fortnight
        return False
    if not angas['yoga_good'] or angas['karana'] == 'Vishti':
        return False
    if not tamil_yogam(weekday, angas['star'])['good']:
        return False
    if natal_star is not None and TARAS[((angas['star'] - natal_star) % 27) % 9][2] == 'bad':
        return False
    if natal_sign is not None and (angas['moon_sign'] - natal_sign) % 12 + 1 == 8:  # Chandrashtamam
        return False
    return True


def find_muhurthams(event_key, start_date, days, tz_name, lat, lon, natal_star=None, natal_sign=None, ayanamsa='Lahiri',
                    limit=12):
    """Auspicious daytime windows over the coming days, best-supported first within each day."""
    if event_key not in MUHURTHA_EVENTS:
        raise ValueError('Choose a muhurtham event: ' + ', '.join(MUHURTHA_EVENTS))
    if not math.isfinite(lat) or not -66 <= lat <= 66:
        raise ValueError('Latitude must be between 66° south and 66° north in this version.')
    days = max(1, min(int(days), 120))
    event = MUHURTHA_EVENTS[event_key]
    tz = _zone(tz_name)
    swe.set_sid_mode(AYAN[ayanamsa])
    first = local_to_utc(start_date, '12:00', tz_name, 0).astimezone(tz).date()
    results, skipped = [], {}
    for offset in range(days):
        day = first + timedelta(days=offset)
        weekday = (day.weekday() + 1) % 7
        cal = tamil_calendar(day, tz, lat, lon)
        rejections = _day_rejections(event, weekday, cal['month_index'])
        if rejections:
            for key, _, _ in rejections:
                skipped[key] = skipped.get(key, 0) + 1
            continue
        ev = sun_events(day, tz, lat, lon)
        eighth = (ev['sunset'] - ev['sunrise']) / 8
        kalams = [(ev['sunrise'] + (k - 1) * eighth, ev['sunrise'] + k * eighth)
                  for k in (RAHU_KALAM[weekday], YAMAGANDAM[weekday], GULIKA_KALAM[weekday])]
        step = STEP_MINUTES / 1440

        def state(jd):
            # The rising Lagna when every rule holds at this moment, else None
            if not _moment_ok(event, _angas(jd), natal_star, natal_sign, weekday):
                return None
            lagna = _lagna(jd, lat, lon)
            return lagna if _lagna_ok(lagna, _graha_signs(jd), natal_sign) else None

        def edge(before, after, current):
            # Bisect to about half a minute where the state stops being `current`
            for _ in range(5):
                mid = (before + after) / 2
                before, after = (mid, after) if state(mid) == current else (before, mid)
            return before

        spans, start, current, prev_t = [], None, None, ev['sunrise']
        t = ev['sunrise']
        while t < ev['sunset']:
            probe = min(t + step / 2, ev['sunset'])
            now = state(probe)
            if now != current:
                boundary = ev['sunrise'] if t == ev['sunrise'] else edge(prev_t, probe, current)
                if current is not None:
                    spans.append((start, boundary, current))
                start, current = boundary, now
            prev_t = probe
            t += step
        if current is not None:
            spans.append((start, ev['sunset'], current))
        # Cut Rahu Kalam, Yamagandam and Gulika out exactly
        for k_start, k_end in kalams:
            spans = [piece for a, b, lg in spans for piece in ((a, min(b, k_start), lg), (max(a, k_end), b, lg))
                     if piece[1] > piece[0]]
        windows = [(dict(start=a, lagna=lg, angas=_angas((a + b) / 2), signs=_graha_signs((a + b) / 2)), b)
                   for a, b, lg in sorted(spans)]
        windows = [(w, end) for w, end in windows if (end - w['start']) * 1440 >= MIN_WINDOW_MINUTES]
        if not windows:
            continue
        rows = []
        for w, end in windows:
            a = w['angas']
            in_paksha = (a['tithi'] - 1) % 15 + 1
            notes_en, notes_ta = [], []
            if a['tithi'] <= 15:
                notes_en.append('waxing Moon')
                notes_ta.append('வளர்பிறை')
            if natal_star is not None:
                tara = TARAS[((a['star'] - natal_star) % 27) % 9]
                notes_en.append(f"{tara[0]} tara")
                notes_ta.append(f"{tara[1]} தாரை")
            lagna = w['lagna']
            if any((w['signs'][g] - lagna) % 12 + 1 in (1, 4, 7, 10) for g in LAGNA_BENEFICS):
                notes_en.append('Jupiter or Venus in a kendra')
                notes_ta.append('குரு / சுக்கிரன் கேந்திரத்தில்')
            if event_key == 'marriage' and not any((sg - lagna) % 12 == 6 for sg in w['signs'].values()):
                notes_en.append('7th house clear')
                notes_ta.append('7-ஆம் இடம் சுத்தம்')
            if lagna in FIXED_SIGNS and event_key == 'griha_pravesam':
                notes_en.append('fixed Lagna')
                notes_ta.append('ஸ்திர லக்னம்')
            if natal_sign is not None:
                house = (a['moon_sign'] - natal_sign) % 12 + 1
                if house in CHANDRA_BALAM_HOUSES:
                    notes_en.append('Chandra Balam')
                    notes_ta.append('சந்திர பலம்')
            rows.append(dict(
                start_local=_local_iso(w['start'], tz), end_local=_local_iso(end, tz),
                minutes=round((end - w['start']) * 1440),
                nakshatra=STARS[a['star']], nakshatra_ta=TAMIL_STARS[a['star']],
                tithi=TITHIS[a['tithi'] - 1], tithi_ta=TITHI_TA[in_paksha - 1],
                paksha='Shukla' if a['tithi'] <= 15 else 'Krishna', yoga=a['yoga'], karana=a['karana'],
                tamil_yogam=tamil_yogam(weekday, a['star']), lagna=SIGNS[lagna], lagna_ta=TAMIL[lagna], lagna_index=lagna,
                notes_en=notes_en, notes_ta=notes_ta))
        results.append(dict(date=day.isoformat(), weekday=VAARAM[weekday][0], weekday_ta=VAARAM[weekday][1],
                            tamil_date=f"{cal['month_ta']} {cal['day']}", windows=rows))
        if len(results) >= limit:
            break
    return dict(event=event_key, event_en=event['en'], event_ta=event['ta'], start=first.isoformat(), days=days,
                personal=natal_star is not None or natal_sign is not None, days_found=len(results), results=results,
                skipped_days=skipped)
