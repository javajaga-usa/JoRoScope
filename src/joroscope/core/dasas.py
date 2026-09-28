"""JoRoScope Additional Dasa Systems
Ashtottari Dasa (108 years, eight lords) and Jaimini Chara Dasa (K.N. Rao's method), plus the
dasa-year lengths the Vimshottari, Yogini and these dasas can be counted in.
"""
from datetime import datetime, timedelta, timezone

from .engine import SIGNS, TAMIL
from .readings.common import SIGN_LORDS
from .readings.jaimini import _jaimini_lord

NAK_SPAN = 40 / 3

# Length of a dasa year in days. Most South Indian almanacs count the Julian year; Jagannatha
# Hora defaults to the sidereal year; the Savana year of 360 days is the classical one.
DASA_YEARS = {
    'julian': (365.25, 'Julian year (365.25 days)', 'ஜூலியன் ஆண்டு (365.25 நாட்கள்)'),
    'sidereal': (365.256363, 'Sidereal year (365.2564 days)', 'நட்சத்திர ஆண்டு (365.2564 நாட்கள்)'),
    'savana': (360.0, 'Savana year (360 days)', 'சாவன ஆண்டு (360 நாட்கள்)'),
}


def year_days(kind):
    if kind in (None, ''):
        kind = 'julian'
    if kind not in DASA_YEARS:
        raise ValueError('Dasa year must be one of: ' + ', '.join(DASA_YEARS))
    return DASA_YEARS[kind][0]


# Ashtottari: lords in dasa order with their years, and the birth stars (Ashwini = 0) each rules,
# counted from Ardra as in Jagannatha Hora (Abhijit is not a separate star)
ASHTOTTARI = [('Sun', 6, (5, 6, 7, 8)), ('Moon', 15, (9, 10, 11)), ('Mars', 8, (12, 13, 14, 15)),
              ('Mercury', 17, (16, 17, 18)), ('Saturn', 10, (19, 20, 21)), ('Jupiter', 19, (22, 23, 24)),
              ('Rahu', 12, (25, 26, 0, 1)), ('Venus', 21, (2, 3, 4))]
ASHTOTTARI_TOTAL = 108


def ashtottari_applicable(planets):
    """Classical condition: Rahu in a kendra or trikona from the Lagna lord, but not in the Lagna."""
    asc = planets['Ascendant']['sign_index']
    lord_sign = planets[SIGN_LORDS[asc]]['sign_index']
    rahu = planets['Rahu']['sign_index']
    return rahu != asc and (rahu - lord_sign) % 12 + 1 in (1, 4, 5, 7, 9, 10)


def ashtottari_dasha(moon, birth, now=None, year=365.25):
    """Ashtottari Maha Dasas from the birth star's group balance, each with its eight bhuktis
    (starting from the Dasa lord, each lasting dasa years x bhukti years / 108)."""
    now = now or datetime.now(timezone.utc)
    star = int(moon / NAK_SPAN) % 27
    first = next(i for i, (_, _, stars) in enumerate(ASHTOTTARI) if star in stars)
    group = ASHTOTTARI[first][2]
    group_start = group[0] * NAK_SPAN
    elapsed = (moon - group_start) % 360 / (len(group) * NAK_SPAN)
    start = birth - timedelta(days=elapsed * ASHTOTTARI[first][1] * year)
    rows = []
    for k in range(len(ASHTOTTARI)):
        i = (first + k) % len(ASHTOTTARI)
        lord, years, _ = ASHTOTTARI[i]
        end = start + timedelta(days=years * year)
        subs, sub_start = [], start
        for m in range(len(ASHTOTTARI)):
            b_lord, b_years, _ = ASHTOTTARI[(i + m) % len(ASHTOTTARI)]
            sub_end = sub_start + timedelta(days=years * b_years / ASHTOTTARI_TOTAL * year)
            subs.append(dict(lord=b_lord, start=sub_start.isoformat(), end=sub_end.isoformat(),
                             is_active=sub_start <= now < sub_end))
            sub_start = sub_end
        rows.append(dict(lord=lord, years=years, start=start.isoformat(), end=end.isoformat(), subperiods=subs,
                         is_active=start <= now < end))
        start = end
    return rows


# Jaimini Chara Dasa. Odd-footed (savya) signs count forward, even-footed (apasavya) backward.
ODD_FOOTED = (0, 1, 2, 6, 7, 8)
# Exaltation and debilitation signs, whole-sign as Chara Dasa reads them. The nodes follow both
# classical views (Rahu exalted in Taurus or Gemini, Ketu in Scorpio or Sagittarius) as Jagannatha
# Hora does; Mercury counts as exalted in Virgo, where PyJHora treats it as only its own sign.
EXALTATION = {'Sun': (0,), 'Moon': (1,), 'Mars': (9,), 'Mercury': (5,), 'Jupiter': (3,), 'Venus': (11,),
              'Saturn': (6,), 'Rahu': (1, 2), 'Ketu': (7, 8)}
DEBILITATION = {name: tuple((s + 6) % 12 for s in signs) for name, signs in EXALTATION.items()}


def chara_dasa_years(sign, planets):
    """K.N. Rao: count from the sign to its lord (backward for even-footed signs), less one; 12
    when the lord is in the sign; otherwise a year more if the lord is in its exaltation sign and
    a year less in its debilitation sign. Scorpio and Aquarius take the stronger of their two lords."""
    lord = _jaimini_lord(sign, planets)
    at = planets[lord]['sign_index']
    if at == sign:
        return 12, lord
    count = (at - sign) % 12 + 1 if sign in ODD_FOOTED else (sign - at) % 12 + 1
    years = count - 1
    if at in EXALTATION[lord]:
        years += 1
    elif at in DEBILITATION[lord]:
        years -= 1
    return years, lord


def chara_dasha(planets, birth, now=None, year=365.25, max_years=120):
    """Chara Dasa from the Lagna: forward when the 9th sign is odd-footed, else backward. The
    second round gives each sign 12 less its first-round years. Each dasa has twelve equal
    antardasas, starting from the next sign in the dasa sign's own direction and ending with it."""
    now = now or datetime.now(timezone.utc)
    asc = planets['Ascendant']['sign_index']
    step = 1 if (asc + 8) % 12 in ODD_FOOTED else -1
    order = [(asc + step * i) % 12 for i in range(12)]
    first_round = {sign: chara_dasa_years(sign, planets) for sign in order}
    rows, start, total = [], birth, 0
    for round_no in (1, 2):
        for sign in order:
            years, lord = first_round[sign]
            if round_no == 2:
                years = 12 - years
            if years <= 0:
                continue
            end = start + timedelta(days=years * year)
            sub_step = 1 if sign in ODD_FOOTED else -1
            subs, sub_start = [], start
            for m in range(1, 13):
                sub_sign = (sign + sub_step * m) % 12
                sub_end = sub_start + timedelta(days=years / 12 * year)
                subs.append(dict(sign=SIGNS[sub_sign], sign_ta=TAMIL[sub_sign], sign_index=sub_sign,
                                 start=sub_start.isoformat(), end=sub_end.isoformat(), is_active=sub_start <= now < sub_end))
                sub_start = sub_end
            rows.append(dict(sign=SIGNS[sign], sign_ta=TAMIL[sign], sign_index=sign, lord=lord, years=years,
                             round=round_no, start=start.isoformat(), end=end.isoformat(), subperiods=subs,
                             is_active=start <= now < end))
            start, total = end, total + years
            if total >= max_years:
                return rows
    return rows
