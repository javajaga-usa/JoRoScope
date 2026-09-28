"""JoRoScope Shadbala
The six-fold planetary strength of Brihat Parashara Hora Shastra, computed as worked
in B.V. Raman's "Graha and Bhava Balas" (the reference examples in the tests).
All values are virupas; 60 virupas make one rupa.

Sthana (positional): Uchcha, Saptavargaja, Ojayugma, Kendra, Drekkana
Dig (directional), Kaala (temporal): Nathonnatha, Paksha, Tribhaga, Abda, Masa, Vara,
Hora, Ayana, Yuddha; Cheshta (motional), Naisargika (natural), Drik (aspectual).
"""
import math

from .engine import swe

PLANETS = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']
SIGN_LORDS = ['Mars', 'Venus', 'Mercury', 'Moon', 'Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Saturn', 'Jupiter']
OWN_SIGNS = {'Sun': (4,), 'Moon': (3,), 'Mars': (0, 7), 'Mercury': (2, 5), 'Jupiter': (8, 11),
             'Venus': (1, 6), 'Saturn': (9, 10)}
MOOLATRIKONA = {'Sun': (4, 0, 20), 'Moon': (1, 3, 30), 'Mars': (0, 0, 12), 'Mercury': (5, 15, 20),
                'Jupiter': (8, 0, 10), 'Venus': (6, 0, 15), 'Saturn': (10, 0, 20)}
# Drekkana (decanate) that strengthens each graha: males the 1st, eunuchs the 2nd, females the 3rd
DREKKANA_PART = {'Sun': 0, 'Mars': 0, 'Jupiter': 0, 'Mercury': 1, 'Saturn': 1, 'Moon': 2, 'Venus': 2}
# Bhava madhya (0 = Lagna) where each graha has no directional strength
POWERLESS_BHAVA = {'Sun': 3, 'Mars': 3, 'Moon': 9, 'Venus': 9, 'Mercury': 6, 'Jupiter': 6, 'Saturn': 0}
DEEP_EXALTATION = {'Sun': 10, 'Moon': 33, 'Mars': 298, 'Mercury': 165, 'Jupiter': 95, 'Venus': 357, 'Saturn': 200}
# Natural friendship: 1 friend, 0 neutral, -1 enemy
NATURAL = {
    'Sun': {'Moon': 1, 'Mars': 1, 'Jupiter': 1, 'Mercury': 0, 'Venus': -1, 'Saturn': -1},
    'Moon': {'Sun': 1, 'Mercury': 1, 'Mars': 0, 'Jupiter': 0, 'Venus': 0, 'Saturn': 0},
    'Mars': {'Sun': 1, 'Moon': 1, 'Jupiter': 1, 'Venus': 0, 'Saturn': 0, 'Mercury': -1},
    'Mercury': {'Sun': 1, 'Venus': 1, 'Mars': 0, 'Jupiter': 0, 'Saturn': 0, 'Moon': -1},
    'Jupiter': {'Sun': 1, 'Moon': 1, 'Mars': 1, 'Saturn': 0, 'Mercury': -1, 'Venus': -1},
    'Venus': {'Mercury': 1, 'Saturn': 1, 'Mars': 0, 'Jupiter': 0, 'Sun': -1, 'Moon': -1},
    'Saturn': {'Mercury': 1, 'Venus': 1, 'Jupiter': 0, 'Sun': -1, 'Moon': -1, 'Mars': -1}
}
SAPTAVARGAS = ('D1', 'D2', 'D3', 'D7', 'D9', 'D12', 'D30')
# Saptavargaja points by compound relationship with the varga sign's lord (-2 .. +2)
COMPOUND_POINTS = {2: 22.5, 1: 15, 0: 7.5, -1: 3.75, -2: 1.875}
NAISARGIKA = {'Sun': 60.0, 'Moon': 51.43, 'Mars': 17.14, 'Mercury': 25.71, 'Jupiter': 34.29, 'Venus': 42.86, 'Saturn': 8.57}
# Minimum Shadbala in rupas (BPHS; B.V. Raman lowers the Sun's to 5)
REQUIRED_RUPAS = {'Sun': 6.5, 'Moon': 6.0, 'Mars': 5.0, 'Mercury': 7.0, 'Jupiter': 6.5, 'Venus': 5.5, 'Saturn': 5.0}
WEEKDAY_LORDS = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']  # Sunday first
HORA_SEQUENCE = ['Sun', 'Venus', 'Mercury', 'Moon', 'Saturn', 'Jupiter', 'Mars']
# Disc diameters used to share out Yuddha Bala between warring planets
DISC_DIAMETERS = {'Mars': 9.4, 'Mercury': 6.6, 'Jupiter': 190.4, 'Venus': 16.6, 'Saturn': 158.0}
SWE_BODIES = {'Mars': swe.MARS, 'Mercury': swe.MERCURY, 'Jupiter': swe.JUPITER, 'Venus': swe.VENUS, 'Saturn': swe.SATURN}
# Ahargana (days since the Kali epoch) is counted from Thursday 17 Feb 3102 BCE (JDN 588465);
# the lords of its 360-day years and 30-day months give Abda and Masa Bala.
KALI_EPOCH_JDN = 588465
ORDINAL_TO_JDN = 1721425  # date.toordinal() + this = Julian Day Number

# Madhya grahas for Cheshta Bala from B.V. Raman's tables: sidereal (Raman ayanamsa) mean
# longitudes at 1900-01-01 00:00 Ujjain mean time, mean daily motions and the yearly bija
# corrections (constant, per year since 1900). For Mars, Jupiter and Saturn this is the mean
# planet; for Mercury and Venus it is their seeghrochcha.
RAMAN_EPOCH_JD = 2415020.5 - 76 / 360
RAMAN_MEAN = {
    'Sun': (257.4568, 0.98560265, 0, 0),
    'Mars': (270.22, 0.524019, 0, 0),
    'Mercury': (164.0, 4.092318, 6.67, -0.00133),
    'Jupiter': (220.04, 0.083096, -3.3, -0.0067),
    'Venus': (328.51, 1.602146, -5.0, -0.0001),
    'Saturn': (236.74, 0.033439, 5.0, 0.001)
}


def _arc(a, b):
    """Shortest angular distance between two longitudes, 0-180."""
    d = abs(a - b) % 360
    return 360 - d if d > 180 else d


def _compound(planet, other, signs):
    """Panchadha (compound) relationship: natural plus temporal, -2 .. +2."""
    temporal = 1 if (signs[other] - signs[planet]) % 12 + 1 in (2, 3, 4, 10, 11, 12) else -1
    return NATURAL[planet][other] + temporal


def _raman_mean(body, jd, ayanamsa):
    """Raman's mean longitude of a body, moved into the chart's ayanamsa."""
    epoch, motion, bija, bija_rate = RAMAN_MEAN[body]
    days = jd - RAMAN_EPOCH_JD
    raman_ayanamsa = 21.01444 + days / 365.25 * 50.2564 / 3600
    return (epoch + days * motion + bija + bija_rate * days / 365.25 + raman_ayanamsa - ayanamsa) % 360


def _drishti(angle, aspecting):
    """Sphuta drishti in virupas for a directed angle aspecting -> aspected (BPHS)."""
    a = angle % 360
    if a < 30:
        value = 0.0
    elif a < 60:
        value = (a - 30) / 2
    elif a < 90:
        value = a - 45 + (45 if aspecting == 'Saturn' else 0)
    elif a < 120:
        value = (120 - a) / 2 + 30 + (15 if aspecting == 'Mars' else 0)
    elif a < 150:
        value = 150 - a + (30 if aspecting == 'Jupiter' else 0)
    elif a < 180:
        value = 2 * (a - 150)
    elif a < 300:
        value = (300 - a) / 2
        if aspecting == 'Mars' and 210 <= a < 240:
            value += 15
        elif aspecting == 'Jupiter' and 240 <= a < 270:
            value += 30
        elif aspecting == 'Saturn' and 270 <= a < 300:
            value += 45
    else:
        value = 0.0
    return value


def _benefics(lon, signs, waxing):
    """Chart benefics for Paksha and Drik Bala: Jupiter, Venus, the waxing Moon, and
    Mercury unless the malefics sharing his sign outnumber the benefics."""
    benefic = {'Jupiter', 'Venus'} | ({'Moon'} if waxing else set())
    malefic = {'Sun', 'Mars', 'Saturn'} | (set() if waxing else {'Moon'})
    with_mercury = [p for p in PLANETS if p != 'Mercury' and signs[p] == signs['Mercury']]
    good = [p for p in with_mercury if p in benefic]
    bad = [p for p in with_mercury if p in malefic]
    if len(good) > len(bad) or not with_mercury:
        benefic.add('Mercury')
    elif len(bad) > len(good):
        malefic.add('Mercury')
    else:  # a tie goes to whichever companion is nearer to Mercury
        nearest = min(with_mercury, key=lambda p: _arc(lon[p], lon['Mercury']))
        (benefic if nearest in benefic else malefic).add('Mercury')
    return benefic


def compute_shadbala(planets, jd, events, vedic_date, madhya, ayanamsa):
    """Shadbala of the seven grahas, in virupas per component.

    planets:    the engine's planet dicts (sidereal longitude, sign_index, degree, vargas, dignity)
    jd:         birth moment (Julian day, UT)
    events:     JDs of the Vedic day's sunrise, sunset and next_sunrise, and of the
                previous day's sunset (prev_sunset)
    vedic_date: the civil date whose sunrise begins the Vedic day of birth
    madhya:     the twelve Sripati bhava madhyas, the first being the Ascendant
    ayanamsa:   the chart's ayanamsa in degrees
    """
    lon = {p: planets[p]['longitude'] for p in PLANETS}
    signs = {p: planets[p]['sign_index'] for p in PLANETS}
    elongation = (lon['Moon'] - lon['Sun']) % 360
    benefics = _benefics(lon, signs, elongation < 180)
    asc_sign = planets['Ascendant']['sign_index']

    # Day-level factors shared by every graha
    midnights = ((events['prev_sunset'] + events['sunrise']) / 2, (events['sunset'] + events['next_sunrise']) / 2)
    hours_from_midnight = min(abs(jd - m) for m in midnights) * 24
    unnata = min(60.0, hours_from_midnight * 5)  # 2 virupas per ghati from midnight
    phase = min(elongation, 360 - elongation) / 3
    if jd < events['sunset']:
        third = (events['sunset'] - events['sunrise']) / 3
        tribhaga_lord = ('Mercury', 'Sun', 'Saturn')[min(2, int((jd - events['sunrise']) // third))]
    else:
        third = (events['next_sunrise'] - events['sunset']) / 3
        tribhaga_lord = ('Moon', 'Venus', 'Mars')[min(2, int((jd - events['sunset']) // third))]
    jdn = vedic_date.toordinal() + ORDINAL_TO_JDN
    ahargana = jdn - KALI_EPOCH_JDN
    lord_of_jdn = lambda n: WEEKDAY_LORDS[(n + 1) % 7]
    abda_lord = lord_of_jdn(KALI_EPOCH_JDN + 360 * (ahargana // 360))
    masa_lord = lord_of_jdn(KALI_EPOCH_JDN + 30 * (ahargana // 30))
    vara_lord = lord_of_jdn(jdn)
    hours_since_sunrise = int((jd - events['sunrise']) * 24)
    hora_lord = HORA_SEQUENCE[(HORA_SEQUENCE.index(vara_lord) + hours_since_sunrise) % 7]
    mean_sun = _raman_mean('Sun', jd, ayanamsa)

    result = {}
    for p in PLANETS:
        pl = planets[p]
        r = result[p] = {}
        # --- Sthana Bala ---
        r['uchcha'] = _arc(lon[p], (DEEP_EXALTATION[p] + 180) % 360) / 3
        sapta = 0.0
        for varga in SAPTAVARGAS:
            s = pl['vargas'][varga]
            m_sign, m_start, m_end = MOOLATRIKONA[p]
            if varga == 'D1' and s == m_sign and m_start <= pl['degree'] < m_end:
                sapta += 45
            elif s in OWN_SIGNS[p]:
                sapta += 30
            else:
                sapta += COMPOUND_POINTS[_compound(p, SIGN_LORDS[s], signs)]
        r['saptavargaja'] = sapta
        wants_odd = p not in ('Moon', 'Venus')
        r['ojayugma'] = sum(15 for s in (signs[p], pl['vargas']['D9']) if (s % 2 == 0) == wants_odd)
        house = (signs[p] - asc_sign) % 12
        r['kendra'] = (60, 30, 15)[house % 3]
        r['drekkana'] = 15.0 if int(pl['degree'] // 10) == DREKKANA_PART[p] else 0.0

        # --- Dig Bala: a third of the distance from the powerless bhava madhya ---
        r['dig'] = _arc(lon[p], madhya[POWERLESS_BHAVA[p]]) / 3

        # --- Kaala Bala ---
        r['nathonnatha'] = 60.0 if p == 'Mercury' else (unnata if p in ('Sun', 'Jupiter', 'Venus') else 60 - unnata)
        paksha = phase if p in benefics else 60 - phase
        r['paksha'] = 2 * paksha if p == 'Moon' else paksha
        r['tribhaga'] = 60.0 if p in ('Jupiter', tribhaga_lord) else 0.0
        r['abda'] = 15.0 if p == abda_lord else 0.0
        r['masa'] = 30.0 if p == masa_lord else 0.0
        r['vara'] = 45.0 if p == vara_lord else 0.0
        r['hora'] = 60.0 if p == hora_lord else 0.0
        # Ayana Bala from the kranti (declination) of the sayana longitude
        kranti = math.degrees(math.asin(math.sin(math.radians(24)) * math.sin(math.radians(lon[p] + ayanamsa))))
        if p == 'Mercury':
            kranti = abs(kranti)
        elif p in ('Moon', 'Saturn'):
            kranti = -kranti
        r['ayana'] = (24 + kranti) * 1.25 * (2 if p == 'Sun' else 1)
        r['yuddha'] = 0.0

        # --- Cheshta Bala: the Sun's and Moon's are carried by their doubled Ayana and Paksha ---
        if p in ('Sun', 'Moon'):
            r['cheshta'] = 0.0
        else:
            madhya_graha, seeghrochcha = _raman_mean(p, jd, ayanamsa), mean_sun
            if p in ('Mercury', 'Venus'):
                madhya_graha, seeghrochcha = seeghrochcha, madhya_graha
            average = (madhya_graha + ((lon[p] - madhya_graha + 180) % 360 - 180) / 2) % 360
            r['cheshta'] = _arc(seeghrochcha, average) / 3

        r['naisargika'] = NAISARGIKA[p]

        # --- Drik Bala: a quarter of the benefic less the malefic sphuta drishti received ---
        received = sum(_drishti(lon[p] - lon[q], q) * (1 if q in benefics else -1) for q in PLANETS if q != p)
        r['drik'] = received / 4

    # Graha Yuddha: Mars to Saturn within a degree. The one further north (ecliptic latitude)
    # wins (Surya Siddhanta) and takes the difference of their balas up to Hora Bala, shared
    # out by the difference of their disc diameters.
    upto_hora = ('uchcha', 'saptavargaja', 'ojayugma', 'kendra', 'drekkana', 'dig',
                 'nathonnatha', 'paksha', 'tribhaga', 'abda', 'masa', 'vara', 'hora')
    warriors = list(SWE_BODIES)
    for i, a in enumerate(warriors):
        for b in warriors[i + 1:]:
            if _arc(lon[a], lon[b]) < 1:
                lat = {x: swe.calc_ut(jd, SWE_BODIES[x], swe.FLG_MOSEPH)[0][1] for x in (a, b)}
                winner, loser = (a, b) if lat[a] >= lat[b] else (b, a)
                strength = {x: sum(result[x][k] for k in upto_hora) for x in (a, b)}
                share = abs(strength[a] - strength[b]) / abs(DISC_DIAMETERS[a] - DISC_DIAMETERS[b])
                result[winner]['yuddha'] += share
                result[loser]['yuddha'] -= share

    for p, r in result.items():
        r['sthana'] = r['uchcha'] + r['saptavargaja'] + r['ojayugma'] + r['kendra'] + r['drekkana']
        r['kaala'] = sum(r[k] for k in ('nathonnatha', 'paksha', 'tribhaga', 'abda', 'masa', 'vara', 'hora', 'ayana', 'yuddha'))
        r['total'] = r['sthana'] + r['dig'] + r['kaala'] + r['cheshta'] + r['naisargika'] + r['drik']
        r['rupas'] = r['total'] / 60
        r['required_rupas'] = REQUIRED_RUPAS[p]
        r['ratio'] = r['rupas'] / REQUIRED_RUPAS[p]
        # Ishta and Kashta Phala (BPHS): the capacity to give good or bad results, 0-60, from
        # Uchcha and Cheshta Bala; the Sun's Cheshta is his Ayana Bala and the Moon's her Paksha Bala.
        cheshta = r['ayana'] / 2 if p == 'Sun' else (r['paksha'] / 2 if p == 'Moon' else r['cheshta'])
        cheshta = min(60.0, max(0.0, cheshta))
        r['ishta'] = math.sqrt(r['uchcha'] * cheshta)
        r['kashta'] = math.sqrt((60 - r['uchcha']) * (60 - cheshta))
    return result
