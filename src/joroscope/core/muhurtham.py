"""JoRoScope Muhurtham Finder
Auspicious daytime windows for common undertakings by the classical Muhurta rules (Muhurta
Chintamani): an event-specific nakshatra, a good weekday and tithi, clear of the difficult
parts of the nitya yogas, no Vishti karana, outside Rahu Kalam, Yamagandam and Gulika, and for
marriage and griha pravesam not in Aadi, Purattasi or Margazhi. With the person's birth star
and Moon sign it also applies Tara and Chandra Bala. Published Tamil calendars add the Lagna
and regional customs, so the final time is for the family astrologer to confirm.
"""
import math
from datetime import timedelta

from .engine import AYAN, NITYA_YOGAS, KARANAS, STARS, TAMIL_STARS, TITHIS, swe, local_to_utc, sun_events
from .south_indian import (
    TARAS, CHANDRA_BALAM_HOUSES, VAARAM, TITHI_TA, NAK_SPAN, _elongation, _moon, _yoga_sum, _local_iso, _zone,
    tamil_calendar
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
STEP_MINUTES = 10
MIN_WINDOW_MINUTES = 30


def _karana(elongation):
    half = int(elongation // 6) + 1  # 1-60
    if half == 1:
        return 'Kimstughna'
    if half >= 58:
        return KARANAS[7 + half - 58]  # Shakuni, Chatushpada, Naga
    return KARANAS[(half - 2) % 7]


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


def _moment_ok(event, angas, natal_star, natal_sign):
    tithi = angas['tithi']
    in_paksha = (tithi - 1) % 15 + 1
    if angas['star'] not in event['stars'] or in_paksha not in GOOD_TITHIS:
        return False
    if tithi > 15 and in_paksha > 10:  # late in the waning fortnight
        return False
    if not angas['yoga_good'] or angas['karana'] == 'Vishti':
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
        good = lambda jd: _moment_ok(event, _angas(jd), natal_star, natal_sign)

        def edge(inside, outside):
            # Bisect to about half a minute where the angas stop (or start) qualifying
            for _ in range(5):
                mid = (inside + outside) / 2
                inside, outside = (mid, outside) if good(mid) else (inside, mid)
            return inside

        spans, start = [], None
        t = ev['sunrise']
        while t < ev['sunset']:
            ok = good(min(t + step / 2, ev['sunset']))
            if ok and start is None:
                start = ev['sunrise'] if t == ev['sunrise'] else edge(t + step / 2, t - step / 2)
            elif not ok and start is not None:
                spans.append((start, edge(t - step / 2, t + step / 2)))
                start = None
            t += step
        if start is not None:
            spans.append((start, ev['sunset']))
        # Cut Rahu Kalam, Yamagandam and Gulika out exactly
        for k_start, k_end in kalams:
            spans = [piece for a, b in spans for piece in ((a, min(b, k_start)), (max(a, k_end), b)) if piece[1] > piece[0]]
        windows = [(dict(start=a, angas=_angas((a + b) / 2)), b) for a, b in sorted(spans)]
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
                notes_en=notes_en, notes_ta=notes_ta))
        results.append(dict(date=day.isoformat(), weekday=VAARAM[weekday][0], weekday_ta=VAARAM[weekday][1],
                            tamil_date=f"{cal['month_ta']} {cal['day']}", windows=rows))
        if len(results) >= limit:
            break
    return dict(event=event_key, event_en=event['en'], event_ta=event['ta'], start=first.isoformat(), days=days,
                personal=natal_star is not None or natal_sign is not None, days_found=len(results), results=results,
                skipped_days=skipped)
