"""Sarvatobhadra Chakra and Kota Chakra: the transit Vedha charts of Narapati Jayacharya.

Sarvatobhadra (9 x 9): the 28 nakshatras (with Abhijit) run round the border, seven to a side with
Krittika at the top (east); inside are the letters, the twelve signs, the tithi groups and the
weekdays (layout as in Jagannatha Hora / PyJHora, turned so east is on top). A graha casts Vedha
from its nakshatra along straight lines through the grid: ahead across the chakra in normal motion,
to its right when retrograde and to its left when fast; the Sun and Moon look ahead and Rahu and
Ketu, always retrograde, to the right. Vedha by benefics on the birth star and its special stars
(Janma 1, Karma 10, Sanghatika 16, Samudaya 18, Vainashika 23, Manasa 25) and on the birth sign
supports, by malefics troubles.

Kota Chakra: the 28 stars counted from the birth star fall in four nested squares, from the outer
Bahya through Prakara and Madhya to the inner Stambha (stars 4, 11, 18, 25). Malefics entering the
fort towards the Stambha bring trouble, benefics there protect; grahas leaving it ease matters.
The Kota Swami is the lord of the birth sign.
"""
from datetime import datetime, timezone

from .engine import AYAN, STARS, TAMIL_STARS, SIGNS, TAMIL, sidereal_position, swe, utc_to_jd
from .readings.common import PLANET_TAMIL, SIGN_LORDS
from .readings.report import card, chapter, table

ABHIJIT_TA = 'அபிஜித்'
# The grid as Jagannatha Hora / PyJHora draw it, north on top. Border integers are nakshatras numbered
# 1 Ashwini ... 27 Revati with 28 for Abhijit; inner integers are signs (1 Aries ... 12 Pisces).
_SBC_NORTH_UP = [
    ['ii', 23, 24, 25, 26, 27, 1, 2, 'a'],
    [22, 'rii', 'g', 's', 'd', 'ch', 'l', 'u', 3],
    [28, 'kh', 'ai', 11, 12, 1, 'lu', 'a', 4],
    [21, 'j', 10, 'ah', 'Rikta<br>Fri', 'o', 2, 'v', 5],
    [20, 'bh', 9, 'Jaya<br>Thu', 'Purna<br>Sat', 'Nanda<br>Sun, Tue', 3, 'k', 6],
    [19, 'y', 8, 'am', 'Bhadra<br>Mon, Wed', 'au', 4, 'h', 7],
    [18, 'n', 'e', 7, 6, 5, 'luu', 'd', 8],
    [17, 'ri', 't', 'r', 'p', 't~', 'm', 'uu', 9],
    ['i', 16, 15, 14, 13, 12, 11, 10, 'aa'],
]


def _east_up(grid):
    """Turn the grid a quarter so east (Krittika to Ashlesha) is on top, and renumber the border stars
    to the 28-star order (Abhijit after Uttara Ashadha)."""
    renumber = lambda v: 22 if v == 28 else (v + 1 if v >= 22 else v)
    turned = [[grid[j][8 - i] for j in range(9)] for i in range(9)]
    return [[renumber(v) if isinstance(v, int) and (r in (0, 8) or c in (0, 8)) else v for c, v in enumerate(row)]
            for r, row in enumerate(turned)]


SBC_GRID = _east_up(_SBC_NORTH_UP)
SPECIAL_STARS = {1: ('Janma', 'ஜன்ம'), 10: ('Karma', 'கர்ம'), 16: ('Sanghatika', 'சங்காதிக'), 18: ('Samudaya', 'சமுதாய'),
                 23: ('Vainashika', 'வைநாசிக'), 25: ('Manasa', 'மானஸ')}
BENEFICS = ('Jupiter', 'Venus', 'Mercury', 'Moon')
MEAN_SPEED = {'Mars': 0.524, 'Mercury': 0.986, 'Jupiter': 0.083, 'Venus': 0.986, 'Saturn': 0.0335}
BODIES = (('Sun', swe.SUN), ('Moon', swe.MOON), ('Mars', swe.MARS), ('Mercury', swe.MERCURY), ('Jupiter', swe.JUPITER),
          ('Venus', swe.VENUS), ('Saturn', swe.SATURN), ('Rahu', swe.MEAN_NODE))
KOTA_RINGS = [('Bahya (outer)', 'பாஹ்யம் (வெளி)'), ('Prakara', 'பிராகாரம்'), ('Madhya', 'மத்யம்'), ('Stambha (inner)', 'ஸ்தம்பம் (உள்)')]
ABHIJIT_START, ABHIJIT_END = 276 + 40 / 60, 280 + 53 / 60 + 20 / 3600


def star28(lon):
    """28-star number (1 Ashwini ... 22 Abhijit ... 28 Revati) of a sidereal longitude."""
    lon %= 360
    if ABHIJIT_START <= lon < ABHIJIT_END:
        return 22
    n = int(lon / (40 / 3)) + 1  # 27-star number
    return n if n <= 21 else n + 1


def star28_name(n):
    if n == 22:
        return 'Abhijit', ABHIJIT_TA
    i = n - 1 if n < 22 else n - 2
    return STARS[i], TAMIL_STARS[i]


def _cells():
    stars, signs = {}, {}
    for r, row in enumerate(SBC_GRID):
        for c, v in enumerate(row):
            if isinstance(v, int):
                (stars if r in (0, 8) or c in (0, 8) else signs)[v] = (r, c)
    return stars, signs


STAR_CELL, SIGN_CELL = _cells()


def _directions(r, c):
    """(ahead, left, right) steps into the grid from a border cell, for an observer facing the centre."""
    if r == 0:
        return (1, 0), (1, 1), (1, -1)
    if c == 8:
        return (0, -1), (1, -1), (-1, -1)
    if r == 8:
        return (-1, 0), (-1, -1), (-1, 1)
    return (0, 1), (-1, 1), (1, 1)


def vedha_cells(star, kind):
    """Cells on a Vedha line from a nakshatra: kind is 'ahead', 'left' or 'right'."""
    r, c = STAR_CELL[star]
    step = dict(zip(('ahead', 'left', 'right'), _directions(r, c)))[kind]
    out = []
    r, c = r + step[0], c + step[1]
    while 0 <= r < 9 and 0 <= c < 9:
        out.append((r, c))
        r, c = r + step[0], c + step[1]
    return out


def vedha_kinds(name, speed):
    if name in ('Sun', 'Moon'):
        return ('ahead',)
    if name in ('Rahu', 'Ketu') or speed < 0:
        return ('right',)
    if speed > 1.1 * MEAN_SPEED[name]:
        return ('left',)
    return ('ahead',)


def calculate_chakras(chart, now=None):
    swe.set_sid_mode(AYAN[chart.get('ayanamsa') or 'Lahiri'])
    jd = utc_to_jd(now or datetime.now(timezone.utc))
    moon = chart['planets']['Moon']
    birth = star28(moon['longitude'])
    birth_sign = moon['sign_index'] + 1
    pos = {name: sidereal_position(jd, body) for name, body in BODIES}
    pos['Ketu'] = ((pos['Rahu'][0] + 180) % 360, pos['Rahu'][1])
    transit_star = {g: star28(lon) for g, (lon, _) in pos.items()}

    # Sarvatobhadra: which cells each transit graha strikes
    hits = {}
    for g, (lon, speed) in pos.items():
        for kind in vedha_kinds(g, speed):
            for cell in vedha_cells(transit_star[g], kind):
                hits.setdefault(cell, []).append(g)
    # The birth star's special stars counted in the 27-star scheme, placed on the 28-star grid
    n27 = int(moon['longitude'] / (40 / 3))
    targets = []
    for count, (label, label_ta) in SPECIAL_STARS.items():
        i27 = (n27 + count - 1) % 27
        s28 = i27 + 1 if i27 < 21 else i27 + 2
        targets.append((label, label_ta, s28))
    rows, good_hits, bad_hits = [], 0, 0
    for label, label_ta, s28 in targets:
        on = sorted(set(hits.get(STAR_CELL[s28], [])) | {g for g, s in transit_star.items() if s == s28})
        benefic = [g for g in on if g in BENEFICS]
        malefic = [g for g in on if g not in BENEFICS]
        good_hits += len(benefic)
        bad_hits += len(malefic) * (2 if label in ('Janma', 'Vainashika') else 1)
        name, name_ta = star28_name(s28)
        rows.append(((label, label_ta), (name, name_ta), (', '.join(on) or '—', ', '.join(PLANET_TAMIL[g] for g in on) or '—'),
                     ('troubled', 'பாதிப்பு') if malefic and not benefic else (('supported', 'துணை') if benefic and not malefic else
                                                                                   (('mixed', 'கலப்பு') if on else ('clear', 'தெளிவு')))))
    sign_on = sorted(set(hits.get(SIGN_CELL[birth_sign], [])))
    rows.append((('Birth sign', 'ஜன்ம ராசி'), (SIGNS[birth_sign - 1], TAMIL[birth_sign - 1]),
                 (', '.join(sign_on) or '—', ', '.join(PLANET_TAMIL[g] for g in sign_on) or '—'),
                 ('troubled', 'பாதிப்பு') if any(g not in BENEFICS for g in sign_on) else (('supported', 'துணை') if sign_on else ('clear', 'தெளிவு'))))

    # The grid with the transit grahas in their stars
    grid = []
    for r, row in enumerate(SBC_GRID):
        out_row = []
        for c, v in enumerate(row):
            border = r in (0, 8) or c in (0, 8)
            if isinstance(v, int) and border:
                name, name_ta = star28_name(v)
                gs = [g for g, s in transit_star.items() if s == v]
                cls = 'star birth' if v == birth else 'star'
                out_row.append(dict(en=name + (' · ' + ' '.join(gs) if gs else ''), ta=name_ta + (' · ' + ' '.join(PLANET_TAMIL[g] for g in gs) if gs else ''),
                                    cls=cls + (' struck' if (r, c) in hits else '')))
            elif isinstance(v, int):
                out_row.append(dict(en=SIGNS[v - 1], ta=TAMIL[v - 1], cls='sign' + (' birth' if v == birth_sign else '') + (' struck' if (r, c) in hits else '')))
            else:
                out_row.append(dict(en=v.replace('<br>', ' · '), ta=v.replace('<br>', ' · '), cls='letter'))
        grid.append(out_row)

    # Kota Chakra
    kota_rows, danger = [], 0
    for g in ('Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu'):
        count = (transit_star[g] - birth) % 28 + 1
        q = (count - 1) % 7 + 1  # place within its quarter: 1 outer ... 4 inner ... 7 outer
        ring = {1: 0, 7: 0, 2: 1, 6: 1, 3: 2, 5: 2, 4: 3}[q]
        motion = ('entering', 'உள்நுழைகிறது') if q < 4 else (('at the centre', 'மையத்தில்') if q == 4 else ('leaving', 'வெளியேறுகிறது'))
        if g not in BENEFICS and ring >= 2 and q <= 4:
            danger += 1
        name, name_ta = star28_name(transit_star[g])
        kota_rows.append(((g, PLANET_TAMIL[g]), (name, name_ta), count, KOTA_RINGS[ring], motion))
    kota_swami = SIGN_LORDS[moon['sign_index']]
    ks_count = (transit_star[kota_swami] - birth) % 28 + 1
    ks_ring = {1: 0, 7: 0, 2: 1, 6: 1, 3: 2, 5: 2, 4: 3}[(ks_count - 1) % 7 + 1]

    sbc_verdict = 'good' if good_hits > bad_hits else ('bad' if bad_hits > good_hits else 'mixed')
    cards = [
        card('🔷', 'Sarvatobhadra Vedha now', 'சர்வதோபத்ர வேதை (இப்போது)',
             f"Benefic Vedha on your birth star and its special stars: {good_hits}; malefic: {bad_hits}. "
             + {'good': 'Transits support you now.', 'bad': 'Transits press on your stars now: go carefully with new ventures and health.',
                'mixed': 'The transit Vedhas balance out.'}[sbc_verdict],
             f"உங்கள் ஜன்ம நட்சத்திரம், சிறப்பு நட்சத்திரங்கள் மீது சுப வேதை: {good_hits}; பாப வேதை: {bad_hits}. "
             + {'good': 'கோச்சாரம் இப்போது துணை நிற்கிறது.', 'bad': 'கோச்சாரம் உங்கள் நட்சத்திரங்களை அழுத்துகிறது: புதிய முயற்சிகளிலும் உடல்நலத்திலும் கவனம்.',
                'mixed': 'கோச்சார வேதைகள் சமநிலையில் உள்ளன.'}[sbc_verdict],
             verdict=sbc_verdict),
        card('🏰', 'Kota Chakra now', 'கோட்டைச் சக்கரம் (இப்போது)',
             (f"{danger} malefic{' is' if danger == 1 else 's are'} inside the fort, heading for the Stambha. " if danger else '')
             + ('Guard health and property this period.' if danger else 'The fort is not under attack.')
             + f" The Kota Swami, {kota_swami}, is in the {KOTA_RINGS[ks_ring][0]} ring"
             + (' and defends the fort well.' if ks_ring >= 2 else '.'),
             f"{danger} பாப கிரகங்கள் கோட்டைக்குள் ஸ்தம்பம் நோக்கிச் செல்கின்றன. "
             + ('இக்காலத்தில் உடல்நலம், சொத்தில் கவனம்.' if danger else 'கோட்டை தாக்குதலின்றி உள்ளது.')
             + f" கோட்டை அதிபதி {PLANET_TAMIL[kota_swami]} {KOTA_RINGS[ks_ring][1]} வளையத்தில்"
             + (', கோட்டையை நன்கு காக்கிறார்.' if ks_ring >= 2 else '.'),
             verdict='bad' if danger >= 2 else ('mixed' if danger == 1 else 'good')),
    ]
    return chapter(
        'chakras', 'Sarvatobhadra & Kota Chakra', 'சர்வதோபத்ர & கோட்டைச் சக்கரம்',
        'Narapati Jayacharya\'s Vedha charts for the transits of today, read against your birth star and sign.',
        'இன்றைய கோச்சாரத்திற்கான நரபதி ஜயசார்யரின் வேதைச் சக்கரங்கள், உங்கள் ஜன்ம நட்சத்திரம், ராசியுடன்.',
        cards=cards,
        tables=[table('Vedha on your stars', 'உங்கள் நட்சத்திரங்கள் மீது வேதை',
                      [('Star', 'நட்சத்திரம்'), ('Name', 'பெயர்'), ('Vedha by', 'வேதை'), ('Result', 'பலன்')], rows),
                table('Kota Chakra', 'கோட்டைச் சக்கரம்',
                      [('Graha', 'கிரகம்'), ('Star', 'நட்சத்திரம்'), ('Count', 'எண்ணிக்கை'), ('Ring', 'வளையம்'), ('Motion', 'நகர்வு')], kota_rows)],
        grid=grid, birth_star28=birth, kota_swami=kota_swami)
