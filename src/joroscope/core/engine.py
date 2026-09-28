"""JoRoScope Calculation Engine
High-precision Vedic & modern astrological calculation engine using Swiss Ephemeris.
Supports 14 Divisional Vargas (D1-D60), Ashtakavarga, Dignities, Aspects,
Yogas, Doshas, 3-Tier Vimshottari Dasa, Matchmaking, and Daily Panchangam.
"""
import sys, math
from pathlib import Path

# Vendor path lookup (local or project root)
_root = Path(__file__).resolve().parent
for _candidate in (_root / 'vendor', _root.parent / 'vendor', _root.parent.parent.parent / 'vendor'):
    if _candidate.is_dir():
        sys.path.insert(0, str(_candidate))
        break

import swisseph as swe
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .predictions import generate_comprehensive_predictions, PLANET_TAMIL

SIGNS = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']
TAMIL = ['மேஷம்','ரிஷபம்','மிதுனம்','கடகம்','சிம்மம்','கன்னி','துலாம்','விருச்சிகம்','தனுசு','மகரம்','கும்பம்','மீனம்']
SIGN_LORDS = ['Mars','Venus','Mercury','Moon','Sun','Mercury','Venus','Mars','Jupiter','Saturn','Saturn','Jupiter']

STARS = [
    'Ashwini','Bharani','Krittika','Rohini','Mrigashira','Ardra',
    'Punarvasu','Pushya','Ashlesha','Magha','Purva Phalguni','Uttara Phalguni',
    'Hasta','Chitra','Swati','Vishakha','Anuradha','Jyeshtha',
    'Mula','Purva Ashadha','Uttara Ashadha','Shravana','Dhanishtha','Shatabhisha',
    'Purva Bhadrapada','Uttara Bhadrapada','Revati'
]
TAMIL_STARS = [
    'அசுவினி','பரணி','கிருத்திகை','ரோகிணி','மிருகசீரிஷம்','திருவாதிரை',
    'புனர்பூசம்','பூசம்','ஆயில்யம்','மகம்','பூரம்','உத்திரம்',
    'அஸ்தம்','சித்திரை','சுவாதி','விசாகம்','அனுஷம்','கேட்டை',
    'மூலம்','பூராடம்','உத்திராடம்','திருவோணம்','அவிட்டம்','சதயம்',
    'பூரட்டாதி','உத்திரட்டாதி','ரேவதி'
]
STAR_LORDS = [
    'Ketu','Venus','Sun','Moon','Mars','Rahu','Jupiter','Saturn','Mercury',
    'Ketu','Venus','Sun','Moon','Mars','Rahu','Jupiter','Saturn','Mercury',
    'Ketu','Venus','Sun','Moon','Mars','Rahu','Jupiter','Saturn','Mercury'
]
STAR_GANAS = [
    'Deva','Manushya','Rakshasa','Manushya','Deva','Manushya',
    'Deva','Deva','Rakshasa','Rakshasa','Manushya','Manushya',
    'Deva','Rakshasa','Deva','Rakshasa','Deva','Rakshasa',
    'Rakshasa','Manushya','Manushya','Deva','Rakshasa','Rakshasa',
    'Manushya','Manushya','Deva'
]
STAR_YONIS = [
    ('Horse','M'),('Elephant','F'),('Sheep','F'),('Serpent','M'),('Serpent','F'),('Dog','F'),
    ('Cat','F'),('Sheep','M'),('Cat','M'),('Rat','M'),('Rat','F'),('Cow','M'),
    ('Buffalo','F'),('Tiger','F'),('Buffalo','M'),('Tiger','M'),('Deer','F'),('Deer','M'),
    ('Dog','M'),('Monkey','M'),('Mongoose','M'),('Monkey','F'),('Lion','F'),('Horse','F'),
    ('Lion','M'),('Cow','F'),('Elephant','M')
]
STAR_RAJJUS = [
    'Pada','Ooru','Udara','Kantha','Siro','Kantha',
    'Udara','Ooru','Pada','Pada','Ooru','Udara',
    'Kantha','Siro','Kantha','Udara','Ooru','Pada',
    'Pada','Ooru','Udara','Kantha','Siro','Kantha',
    'Udara','Ooru','Pada'
]
# What a shared Rajju is said to threaten (Tamil marriage tradition)
RAJJU_EFFECTS = {
    'Siro': "the husband's longevity",
    'Kantha': "the wife's longevity",
    'Udara': 'progeny',
    'Ooru': 'family wealth',
    'Pada': 'stability (frequent travel or separation)'
}
RAJJU_EFFECTS_TA = {
    'Siro': 'கணவரின் ஆயுளை', 'Kantha': 'மனைவியின் ஆயுளை', 'Udara': 'சந்ததியை',
    'Ooru': 'குடும்பச் செல்வத்தை', 'Pada': 'நிலைத்தன்மையை (அடிக்கடி பயணம் அல்லது பிரிவு)'
}
GANA_TA = {'Deva': 'தேவ கணம்', 'Manushya': 'மனுஷ கணம்', 'Rakshasa': 'ராட்சச கணம்'}
RAJJU_TA = {'Siro': 'சிரசு', 'Kantha': 'கண்டம்', 'Udara': 'உதரம்', 'Ooru': 'தொடை', 'Pada': 'பாதம்'}
NADI_TA = {'Aadi': 'ஆதி', 'Madhya': 'மத்திய', 'Antya': 'அந்திய'}
YONI_TA = {
    'Horse': 'குதிரை', 'Elephant': 'யானை', 'Sheep': 'ஆடு', 'Serpent': 'பாம்பு', 'Dog': 'நாய்',
    'Cat': 'பூனை', 'Rat': 'எலி', 'Cow': 'பசு', 'Buffalo': 'எருமை', 'Tiger': 'புலி',
    'Deer': 'மான்', 'Monkey': 'குரங்கு', 'Mongoose': 'கீரி', 'Lion': 'சிங்கம்'
}
EKA_GRADE_TA = {'uthamam': 'உத்தமம்', 'madhyamam': 'மத்திமம்', 'avoid': 'பொருந்தாது'}
MATCH_VERDICT_TA = {
    'Auspicious Match': 'உத்தமப் பொருத்தம்',
    'Moderate Match': 'மத்திமப் பொருத்தம்',
    'Inauspicious / Needs Remedies': 'பொருத்தம் குறைவு / பரிகாரம் தேவை'
}

KAAL_SARP_TYPES = [
    ('Anant', 'அனந்த'), ('Kulik', 'குளிக'), ('Vasuki', 'வாசுகி'), ('Shankhapal', 'சங்கபால'),
    ('Padma', 'பத்ம'), ('Mahapadma', 'மகாபத்ம'), ('Takshak', 'தக்ஷக'), ('Karkotak', 'கார்கோடக'),
    ('Shankhachur', 'சங்கசூட'), ('Ghatak', 'காதக'), ('Vishdhar', 'விஷதர'), ('Sheshnag', 'சேஷநாக')
]

STAR_NADIS = [
    'Aadi','Madhya','Antya','Antya','Madhya','Aadi','Aadi','Madhya','Antya',
    'Antya','Madhya','Aadi','Aadi','Madhya','Antya','Antya','Madhya','Aadi',
    'Aadi','Madhya','Antya','Antya','Madhya','Aadi','Aadi','Madhya','Antya'
]
# Mutually obstructing (Vedha) stars; Mrigashira, Chitra and Dhanishtha form a triad.
VEDHA_GROUPS = [
    {0, 17}, {1, 16}, {2, 15}, {3, 14}, {5, 21}, {6, 20}, {7, 19},
    {8, 18}, {9, 26}, {10, 25}, {11, 24}, {12, 23}, {4, 13, 22}
]
# Dina Porutham: favourable counts from the girl's star to the boy's star
DINA_GOOD_COUNTS = (2, 4, 6, 8, 9, 11, 13, 15, 18, 20, 24, 26)
# Eka Nakshatra (bride and groom share the birth star) grading
EKA_NAKSHATRA_GRADE = [
    'madhyamam','avoid','madhyamam','uthamam','madhyamam','uthamam','madhyamam','madhyamam','avoid',
    'uthamam','madhyamam','madhyamam','uthamam','madhyamam','avoid','uthamam','madhyamam','avoid',
    'avoid','madhyamam','madhyamam','uthamam','avoid','avoid','avoid','uthamam','uthamam'
]

NITYA_YOGAS = [
    ('Vishkambha','Inauspicious'),('Priti','Auspicious'),('Ayushman','Auspicious'),('Saubhagya','Auspicious'),
    ('Shobhana','Auspicious'),('Atiganda','Inauspicious'),('Sukarma','Auspicious'),('Dhriti','Auspicious'),
    ('Shula','Inauspicious'),('Ganda','Inauspicious'),('Vriddhi','Auspicious'),('Dhruva','Auspicious'),
    ('Vyaghata','Inauspicious'),('Harshana','Auspicious'),('Vajra','Inauspicious'),('Siddhi','Auspicious'),
    ('Vyatipata','Inauspicious'),('Variyan','Auspicious'),('Parigha','Inauspicious'),('Shiva','Auspicious'),
    ('Siddha','Auspicious'),('Sadhya','Auspicious'),('Shubha','Auspicious'),('Shukla','Auspicious'),
    ('Brahma','Auspicious'),('Indra','Auspicious'),('Vaidhriti','Inauspicious')
]

TITHIS = [
    'Prathama','Dwitiya','Tritiya','Chaturthi','Panchami',
    'Shashthi','Saptami','Ashtami','Navami','Dashami',
    'Ekadashi','Dwadashi','Trayodashi','Chaturdashi','Purnima',
    'Prathama','Dwitiya','Tritiya','Chaturthi','Panchami',
    'Shashthi','Saptami','Ashtami','Navami','Dashami',
    'Ekadashi','Dwadashi','Trayodashi','Chaturdashi','Amavasya'
]

KARANAS = ['Bava','Balava','Kaulava','Taitila','Gara','Vanija','Vishti','Shakuni','Chatushpada','Naga','Kimstughna']

DASHA_NAMES = ['Ketu','Venus','Sun','Moon','Mars','Rahu','Jupiter','Saturn','Mercury']
DASHA_YEARS = [7, 20, 6, 10, 7, 18, 16, 19, 17]
AYAN = {
    'Lahiri': swe.SIDM_LAHIRI,
    'Raman': swe.SIDM_RAMAN,
    'Krishnamurti': swe.SIDM_KRISHNAMURTI,
    'Fagan-Bradley': swe.SIDM_FAGAN_BRADLEY
}
YEAR = 365.25

# Natural Relationships (Naisargika Maitri)
# 1 = Friend, 0 = Neutral, -1 = Enemy
NATURAL_FRIENDS = {
    'Sun': {'Moon': 1, 'Mars': 1, 'Jupiter': 1, 'Mercury': 0, 'Venus': -1, 'Saturn': -1},
    'Moon': {'Sun': 1, 'Mercury': 1, 'Mars': 0, 'Jupiter': 0, 'Venus': 0, 'Saturn': 0},
    'Mars': {'Sun': 1, 'Moon': 1, 'Jupiter': 1, 'Venus': 0, 'Saturn': 0, 'Mercury': -1},
    'Mercury': {'Sun': 1, 'Venus': 1, 'Mars': 0, 'Jupiter': 0, 'Saturn': 0, 'Moon': -1},
    'Jupiter': {'Sun': 1, 'Moon': 1, 'Mars': 1, 'Saturn': 0, 'Mercury': -1, 'Venus': -1},
    'Venus': {'Mercury': 1, 'Saturn': 1, 'Mars': 0, 'Jupiter': 0, 'Sun': -1, 'Moon': -1},
    'Saturn': {'Mercury': 1, 'Venus': 1, 'Jupiter': 0, 'Sun': -1, 'Moon': -1, 'Mars': -1},
    'Rahu': {'Mercury': 1, 'Venus': 1, 'Saturn': 1, 'Jupiter': 0, 'Sun': -1, 'Moon': -1, 'Mars': -1},
    'Ketu': {'Mars': 1, 'Venus': 1, 'Jupiter': 1, 'Mercury': 0, 'Sun': -1, 'Moon': -1, 'Saturn': -1}
}

# Parashara Ashtakavarga Bindu Points
ASHTAKAVARGA_RULES = {
    'Sun': {
        'Sun': [1, 2, 4, 7, 8, 9, 10, 11],
        'Moon': [3, 6, 10, 11],
        'Mars': [1, 2, 4, 7, 8, 9, 10, 11],
        'Mercury': [3, 5, 6, 9, 10, 11, 12],
        'Jupiter': [5, 6, 9, 11],
        'Venus': [6, 7, 12],
        'Saturn': [1, 2, 4, 7, 8, 9, 10, 11],
        'Ascendant': [3, 4, 6, 10, 11, 12]
    },
    'Moon': {
        'Sun': [3, 6, 7, 8, 10, 11],
        'Moon': [1, 3, 6, 7, 10, 11],
        'Mars': [2, 3, 5, 6, 9, 10, 11],
        'Mercury': [1, 3, 4, 5, 7, 8, 10, 11],
        'Jupiter': [1, 4, 7, 8, 10, 11, 12],
        'Venus': [3, 4, 5, 7, 9, 10, 11],
        'Saturn': [3, 5, 6, 11],
        'Ascendant': [3, 6, 10, 11]
    },
    'Mars': {
        'Sun': [3, 5, 6, 10, 11],
        'Moon': [3, 6, 11],
        'Mars': [1, 2, 4, 7, 8, 10, 11],
        'Mercury': [3, 5, 6, 11],
        'Jupiter': [6, 10, 11, 12],
        'Venus': [6, 8, 11, 12],
        'Saturn': [1, 4, 7, 8, 9, 10, 11],
        'Ascendant': [1, 3, 6, 10, 11]
    },
    'Mercury': {
        'Sun': [5, 6, 9, 11, 12],
        'Moon': [2, 4, 6, 8, 10, 11],
        'Mars': [1, 2, 4, 7, 8, 9, 10, 11],
        'Mercury': [1, 3, 5, 6, 9, 10, 11, 12],
        'Jupiter': [6, 8, 11, 12],
        'Venus': [1, 2, 3, 4, 5, 8, 9, 11],
        'Saturn': [1, 2, 4, 7, 8, 9, 10, 11],
        'Ascendant': [1, 2, 4, 6, 8, 10, 11]
    },
    'Jupiter': {
        'Sun': [1, 2, 3, 4, 7, 8, 9, 10, 11],
        'Moon': [2, 5, 7, 9, 11],
        'Mars': [1, 2, 4, 7, 8, 10, 11],
        'Mercury': [1, 2, 4, 5, 6, 9, 10, 11],
        'Jupiter': [1, 2, 3, 4, 7, 8, 10, 11],
        'Venus': [2, 5, 6, 9, 10, 11],
        'Saturn': [3, 5, 6, 12],
        'Ascendant': [1, 2, 4, 5, 6, 7, 9, 10, 11]
    },
    'Venus': {
        'Sun': [8, 11, 12],
        'Moon': [1, 2, 3, 4, 5, 8, 9, 11, 12],
        'Mars': [3, 5, 6, 9, 11, 12],
        'Mercury': [3, 5, 6, 9, 11],
        'Jupiter': [5, 8, 9, 10, 11],
        'Venus': [1, 2, 3, 4, 5, 8, 9, 10, 11],
        'Saturn': [3, 4, 5, 8, 9, 10, 11],
        'Ascendant': [1, 2, 3, 4, 5, 8, 9, 11]
    },
    'Saturn': {
        'Sun': [1, 2, 4, 7, 8, 10, 11],
        'Moon': [3, 6, 11],
        'Mars': [3, 5, 6, 10, 11, 12],
        'Mercury': [6, 8, 9, 10, 11, 12],
        'Jupiter': [5, 6, 11, 12],
        'Venus': [6, 11, 12],
        'Saturn': [3, 5, 6, 11],
        'Ascendant': [1, 3, 4, 6, 10, 11]
    }
}

def local_to_utc(date, time, zone, fold=None):
    naive = datetime.fromisoformat(date + 'T' + time)
    if not 1800 <= naive.year <= 2200:
        raise ValueError('Choose a date between 1800 and 2200.')
    try:
        tz = ZoneInfo(zone)
    except ZoneInfoNotFoundError:
        raise ValueError('Enter a valid IANA timezone, such as Asia/Kolkata.')
    candidates = []
    for f in (0, 1):
        dt = naive.replace(tzinfo=tz, fold=f)
        utc = dt.astimezone(timezone.utc)
        if utc.astimezone(tz).replace(tzinfo=None) == naive and utc not in [x[1] for x in candidates]:
            candidates.append((f, utc))
    if not candidates:
        raise ValueError('This local time did not exist because of a clock change. Correct the birth time.')
    if len(candidates) > 1 and fold not in (0, 1):
        raise ValueError('This time occurred twice during a clock change. Select the first or second occurrence.')
    return next((u for f, u in candidates if f == fold), candidates[0][1])

def utc_to_jd(utc):
    return swe.julday(utc.year, utc.month, utc.day,
                      utc.hour + utc.minute / 60 + (utc.second + utc.microsecond / 1e6) / 3600)

def jd_to_utc(jd):
    y, m, d, h = swe.revjul(jd)
    return datetime(y, m, d, tzinfo=timezone.utc) + timedelta(hours=h)

def sun_events(civil_date, tz, lat, lon):
    """Sunrise, sunset and next sunrise (Julian days, UT) for a local civil date.

    Uses Swiss Ephemeris rise/set of the Sun's upper limb with standard refraction,
    the convention followed by modern (Thirukanitha) Tamil panchangams.
    """
    midnight = datetime(civil_date.year, civil_date.month, civil_date.day, tzinfo=tz)
    geopos = (lon, lat, 0)
    events = []
    jd = utc_to_jd(midnight.astimezone(timezone.utc))
    for rsmi in (swe.CALC_RISE, swe.CALC_SET, swe.CALC_RISE):
        res, tret = swe.rise_trans(jd, swe.SUN, rsmi, geopos, 0, 0, swe.FLG_MOSEPH)
        if res != 0:
            raise ValueError('The Sun does not rise or set at this latitude on this date.')
        jd = tret[0]
        events.append(jd)
    return dict(sunrise=events[0], sunset=events[1], next_sunrise=events[2])

GRAHA_BODIES = [
    ('Sun', swe.SUN), ('Moon', swe.MOON), ('Mars', swe.MARS),
    ('Mercury', swe.MERCURY), ('Jupiter', swe.JUPITER),
    ('Venus', swe.VENUS), ('Saturn', swe.SATURN), ('Rahu', swe.MEAN_NODE)
]
# Houses from the natal Moon where a transiting graha gives good results (Phaladeepika)
GOCHARA_GOOD_HOUSES = {
    'Sun': (3, 6, 10, 11), 'Moon': (1, 3, 6, 7, 10, 11), 'Mars': (3, 6, 11),
    'Mercury': (2, 4, 6, 8, 10, 11), 'Jupiter': (2, 5, 7, 9, 11),
    'Venus': (1, 2, 3, 4, 5, 8, 9, 11, 12), 'Saturn': (3, 6, 11), 'Rahu': (3, 6, 11), 'Ketu': (3, 6, 11)
}
SLOW_TRANSIT_YEARS = 6  # look-ahead for Saturn and Jupiter double-transit windows
# Slow grahas whose sign changes (Peyarchi) are tracked, with a search horizon in days
PEYARCHI_BODIES = [('Saturn', swe.SATURN, 1100), ('Jupiter', swe.JUPITER, 450), ('Rahu', swe.MEAN_NODE, 650)]

def sidereal_position(jd, body):
    """Sidereal longitude and daily speed; the caller sets the ayanamsa mode."""
    pos = swe.calc_ut(jd, body, swe.FLG_MOSEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED)[0]
    return pos[0], pos[3]

def next_sign_change(jd, body, max_days):
    """First moment after jd when a graha enters another sign (retrograde re-entries included)."""
    sign = int(sidereal_position(jd, body)[0] // 30)
    t = jd
    while t - jd < max_days:
        if int(sidereal_position(t + 1, body)[0] // 30) != sign:
            lo, hi = t, t + 1
            for _ in range(30):  # ~0.1 s resolution
                mid = (lo + hi) / 2
                if int(sidereal_position(mid, body)[0] // 30) == sign:
                    lo = mid
                else:
                    hi = mid
            return hi, int(sidereal_position(hi, body)[0] // 30)
        t += 1
    return None, None

def sign_ingresses(body, jd_start, jd_end, step=5.0):
    """Every sign change of a graha between two dates, found in one sweep and
    bisected to about a second; retrograde re-entries appear as their own changes."""
    changes = []
    sign = int(sidereal_position(jd_start, body)[0] // 30)
    t = jd_start
    while t < jd_end:
        t_next = min(t + step, jd_end)
        next_sign = int(sidereal_position(t_next, body)[0] // 30)
        if next_sign != sign:
            lo, hi = t, t_next
            for _ in range(24):
                mid = (lo + hi) / 2
                if int(sidereal_position(mid, body)[0] // 30) == sign:
                    lo = mid
                else:
                    hi = mid
            changes.append((hi, sign, next_sign))
            sign = next_sign
        t = t_next
    return changes

# Saturn's transit from the natal Moon sign that Tamil astrology tracks through life
SATURN_CYCLES = {12: ('sade_sati', 1), 1: ('sade_sati', 2), 2: ('sade_sati', 3),
                 4: ('ardhashtama', None), 7: ('kandaka', None), 8: ('ashtama', None)}

def saturn_life_cycles(birth_jd, moon_sign, years=100, now_jd=None):
    """Ezharai Sani (Sade Sati, with its three phases), Ardhashtama, Kandaka and Ashtama
    Sani periods over a lifetime, merging retrograde back-and-forth into one period."""
    end_jd = birth_jd + years * YEAR
    boundaries = [birth_jd] + [c[0] for c in sign_ingresses(swe.SATURN, birth_jd, end_jd)] + [end_jd]
    stretches = []
    for start, stop in zip(boundaries, boundaries[1:]):
        house = (int(sidereal_position((start + stop) / 2, swe.SATURN)[0] // 30) - moon_sign) % 12 + 1
        kind, phase = SATURN_CYCLES.get(house, (None, None))
        if kind:
            stretches.append(dict(kind=kind, phase=phase, house=house, start=start, end=stop))

    # Almanacs quote each cycle from first entry to final exit, so stretches of one kind
    # separated only by a retrograde excursion (under ~13 months) form one period.
    periods = []
    for kind in ('sade_sati', 'ardhashtama', 'kandaka', 'ashtama'):
        for st in (x for x in stretches if x['kind'] == kind):
            last = next((pd for pd in reversed(periods) if pd['kind'] == kind), None)
            if last and st['start'] - last['_end'] < 400:
                last['_end'] = st['end']
            else:
                last = dict(kind=kind, _start=st['start'], _end=st['end'], _phases={})
                periods.append(last)
            if st['phase']:
                span = last['_phases'].setdefault(st['phase'], [st['start'], st['end']])
                span[0], span[1] = min(span[0], st['start']), max(span[1], st['end'])
    periods.sort(key=lambda pd: pd['_start'])

    iso = lambda jd: jd_to_utc(jd).isoformat(timespec='seconds')
    now_jd = now_jd if now_jd is not None else utc_to_jd(datetime.now(timezone.utc))
    for period in periods:
        period.update(start=iso(period['_start']), end=iso(period['_end']),
                      age_start=round((period['_start'] - birth_jd) / YEAR, 1),
                      active=period['_start'] <= now_jd < period['_end'],
                      from_birth=period['_start'] <= birth_jd, to_horizon=period['_end'] >= end_jd,
                      phases=[dict(phase=n, start=iso(a), end=iso(b)) for n, (a, b) in sorted(period['_phases'].items())])
        del period['_start'], period['_end'], period['_phases']
    return periods

def calculate_gochara(jd, planets, ashtakavarga):
    """Current transits (Gochara) against the natal chart, with Ashtakavarga bindus
    and the next sign change (Peyarchi) of Saturn, Jupiter and Rahu-Ketu."""
    moon_sign = planets['Moon']['sign_index']
    asc_sign = planets['Ascendant']['sign_index']
    bav = ashtakavarga['BAV']
    positions = {name: sidereal_position(jd, body) for name, body in GRAHA_BODIES}
    rahu_lon, rahu_speed = positions['Rahu']
    positions['Ketu'] = ((rahu_lon + 180) % 360, rahu_speed)

    rows = {}
    for name, (lon, speed) in positions.items():
        sign = int(lon // 30)
        house = (sign - moon_sign) % 12 + 1
        row = dict(
            longitude=lon, sign_index=sign, sign=SIGNS[sign], tamil=TAMIL[sign], degree=lon % 30,
            retrograde=speed < 0 and name not in ('Rahu', 'Ketu'),
            house_from_moon=house,
            house_from_lagna=(sign - asc_sign) % 12 + 1,
            favourable=house in GOCHARA_GOOD_HOUSES[name],
            bindus=bav[name][sign] if name in bav else None
        )
        rows[name] = row

    peyarchi = []
    for name, body, horizon in PEYARCHI_BODIES:
        when, to_sign = next_sign_change(jd, body, horizon)
        if when is None:
            continue
        from_sign = rows[name]['sign_index']
        entry = dict(planet=name, date=jd_to_utc(when).isoformat(timespec='seconds'),
                     from_sign=SIGNS[from_sign], from_tamil=TAMIL[from_sign],
                     to_sign=SIGNS[to_sign], to_tamil=TAMIL[to_sign],
                     house_from_moon=(to_sign - moon_sign) % 12 + 1)
        peyarchi.append(entry)
        if name == 'Rahu':
            ketu_from, ketu_to = (from_sign + 6) % 12, (to_sign + 6) % 12
            peyarchi.append(dict(entry, planet='Ketu', from_sign=SIGNS[ketu_from], from_tamil=TAMIL[ketu_from],
                                 to_sign=SIGNS[ketu_to], to_tamil=TAMIL[ketu_to],
                                 house_from_moon=(ketu_to - moon_sign) % 12 + 1))
    # Saturn's and Jupiter's sign periods for the coming years, for double-transit timing
    horizon = jd + SLOW_TRANSIT_YEARS * YEAR
    slow_transits = {}
    for name, body in (('Saturn', swe.SATURN), ('Jupiter', swe.JUPITER)):
        edges = [jd] + [c[0] for c in sign_ingresses(body, jd, horizon)] + [horizon]
        slow_transits[name] = [dict(sign_index=int(sidereal_position(start + 0.5 * (end - start), body)[0] // 30),
                                    start=jd_to_utc(start).isoformat(timespec='seconds'),
                                    end=jd_to_utc(end).isoformat(timespec='seconds'))
                               for start, end in zip(edges, edges[1:]) if end > start]
    return dict(computed_at=jd_to_utc(jd).isoformat(timespec='seconds'), planets=rows, peyarchi=peyarchi,
                slow_transits=slow_transits)

def sripati_bhavas(jd, lat, lon):
    """Sripati bhavas: madhyas trisect each quadrant (Porphyry cusps, the 1st being the
    Ascendant) and each sandhi lies midway between neighbouring madhyas."""
    madhya = list(swe.houses_ex(jd, lat, lon, b'O', swe.FLG_SIDEREAL)[0][-12:])
    sandhi = [(m + ((madhya[(i + 1) % 12] - m) % 360) / 2) % 360 for i, m in enumerate(madhya)]
    return madhya, sandhi

def bhava_of(lon, sandhi):
    """Bhava number (1-12) of a longitude; bhava n runs from sandhi[n-2] to sandhi[n-1]."""
    for n in range(1, 13):
        start = sandhi[n - 2]
        if (lon - start) % 360 < (sandhi[n - 1] - start) % 360:
            return n
    return 1

def calculate_vargas(lon):
    """The 16 Parashara divisional vargas (Shodasavarga, D1 - D60)."""
    lon = lon % 360
    sign = int(lon // 30)
    deg = lon % 30
    is_odd = (sign % 2 == 0)  # 0=Aries (odd), 1=Taurus (even)
    movable = (sign in (0, 3, 6, 9))
    fixed = (sign in (1, 4, 7, 10))

    vargas = {}
    # D1 - Rasi
    vargas['D1'] = sign

    # D2 - Hora (Parashara)
    if is_odd:
        vargas['D2'] = 4 if deg < 15 else 3  # Leo then Cancer
    else:
        vargas['D2'] = 3 if deg < 15 else 4  # Cancer then Leo

    # D3 - Drekkana
    k3 = int(deg // 10)
    vargas['D3'] = (sign + k3 * 4) % 12

    # D4 - Chaturthamsa
    k4 = int(deg / 7.5)
    vargas['D4'] = (sign + k4 * 3) % 12

    # D7 - Saptamsa
    k7 = min(int(deg / (30 / 7)), 6)
    vargas['D7'] = (sign + k7) % 12 if is_odd else (sign + 6 + k7) % 12

    # D9 - Navamsa
    vargas['D9'] = int(lon * 9 // 30) % 12

    # D10 - Dasamsa
    k10 = min(int(deg // 3), 9)
    vargas['D10'] = (sign + k10) % 12 if is_odd else (sign + 8 + k10) % 12

    # D12 - Dwadasamsa
    k12 = min(int(deg / 2.5), 11)
    vargas['D12'] = (sign + k12) % 12

    # D16 - Shodasamsa
    k16 = min(int(deg / 1.875), 15)
    start16 = 0 if movable else (4 if fixed else 8)
    vargas['D16'] = (start16 + k16) % 12

    # D20 - Vimsamsa
    k20 = min(int(deg / 1.5), 19)
    start20 = 0 if movable else (8 if fixed else 4)
    vargas['D20'] = (start20 + k20) % 12

    # D24 - Chaturvimsamsa
    k24 = min(int(deg / 1.25), 23)
    start24 = 4 if is_odd else 3
    vargas['D24'] = (start24 + k24) % 12

    # D27 - Saptavimsamsa
    k27 = min(int(deg / (10 / 9)), 26)
    element = sign % 4  # 0=Fire, 1=Earth, 2=Air, 3=Water
    start27 = element * 3
    vargas['D27'] = (start27 + k27) % 12

    # D30 - Trimsamsa
    if is_odd:
        if deg < 5: vargas['D30'] = 0      # Aries (Mars)
        elif deg < 10: vargas['D30'] = 10  # Aquarius (Saturn)
        elif deg < 18: vargas['D30'] = 8   # Sagittarius (Jupiter)
        elif deg < 25: vargas['D30'] = 2   # Gemini (Mercury)
        else: vargas['D30'] = 6            # Libra (Venus's odd sign)
    else:
        if deg < 5: vargas['D30'] = 1      # Taurus (Venus)
        elif deg < 12: vargas['D30'] = 5   # Virgo (Mercury)
        elif deg < 20: vargas['D30'] = 11  # Pisces (Jupiter)
        elif deg < 25: vargas['D30'] = 9   # Capricorn (Saturn)
        else: vargas['D30'] = 7            # Scorpio (Mars)

    # D40 - Khavedamsa: 45' parts from Aries (odd signs) or Libra (even signs)
    k40 = min(int(deg / 0.75), 39)
    vargas['D40'] = ((0 if is_odd else 6) + k40) % 12

    # D45 - Akshavedamsa: 40' parts from Aries (movable), Leo (fixed) or Sagittarius (dual)
    k45 = min(int(deg / (2 / 3)), 44)
    vargas['D45'] = ((0 if movable else (4 if fixed else 8)) + k45) % 12

    # D60 - Shashtiamsa
    k60 = min(int(deg * 2), 59)
    vargas['D60'] = (sign + k60) % 12

    return vargas

def placement(lon, speed=0):
    lon %= 360
    sign = int(lon // 30)
    star = int(lon / (40 / 3))
    pada = int((lon % (40 / 3)) / (10 / 3)) + 1
    vargas = calculate_vargas(lon)
    return dict(
        longitude=lon,
        sign=SIGNS[sign],
        tamil=TAMIL[sign],
        sign_index=sign,
        degree=lon % 30,
        nakshatra=STARS[star],
        tamil_nakshatra=TAMIL_STARS[star],
        nakshatra_lord=STAR_LORDS[star],
        pada=pada,
        navamsa=vargas['D9'],
        vargas=vargas,
        retrograde=speed < 0,
        speed=speed
    )

def calculate_dignity(planet_name, sign_idx, deg, planet_positions):
    """Determine planetary dignity and Panchadha Maitri friendship."""
    if planet_name in ('Ascendant', 'Rahu', 'Ketu'):
        if planet_name == 'Rahu':
            if sign_idx in (1, 2): return 'Exalted'
            if sign_idx in (7, 8): return 'Debilitated'
            if sign_idx == 10: return 'Own Sign'
            return 'Neutral'
        if planet_name == 'Ketu':
            if sign_idx in (7, 8): return 'Exalted'
            if sign_idx in (1, 2): return 'Debilitated'
            return 'Neutral'
        return 'Ascendant'

    # Exaltation & Debilitation points
    exalt_info = {
        'Sun': (0, 10), 'Moon': (1, 3), 'Mars': (9, 28),
        'Mercury': (5, 15), 'Jupiter': (3, 5), 'Venus': (11, 27),
        'Saturn': (6, 20)
    }
    ex_sign, _ = exalt_info[planet_name]
    deb_sign = (ex_sign + 6) % 12

    if sign_idx == ex_sign:
        return 'Exalted'
    if sign_idx == deb_sign:
        return 'Debilitated'

    # Moolatrikona zones
    moolatrikona = {
        'Sun': (4, 0, 20), 'Moon': (1, 3, 30), 'Mars': (0, 0, 12),
        'Mercury': (5, 15, 20), 'Jupiter': (8, 0, 10), 'Venus': (6, 0, 15),
        'Saturn': (10, 0, 20)
    }
    m_sign, m_start, m_end = moolatrikona[planet_name]
    if sign_idx == m_sign and m_start <= deg <= m_end:
        return 'Moolatrikona'

    # Own Sign
    lord = SIGN_LORDS[sign_idx]
    if lord == planet_name:
        return 'Own Sign'

    # Compound Friendship (Panchadha Maitri) with sign lord
    natural = NATURAL_FRIENDS.get(planet_name, {}).get(lord, 0)
    # Temporal relationship (Tatkalika):
    lord_sign = None
    for p_name, p_data in planet_positions.items():
        if p_name == lord:
            lord_sign = p_data['sign_index']
            break
    if lord_sign is not None:
        diff = (lord_sign - sign_idx) % 12
        temporal = 1 if diff in (1, 2, 3, 9, 10, 11) else -1
    else:
        temporal = 0

    combined = natural + temporal
    if combined >= 2: return 'Great Friend'
    if combined == 1: return 'Friend'
    if combined == 0: return 'Neutral'
    if combined == -1: return 'Enemy'
    return 'Great Enemy'

def varga_dignity(planet_name, varga_sign, planets):
    """Dignity of a graha in a divisional sign: exaltation, debilitation or own sign, else its
    compound relationship with the sign's lord, the temporal part taken from the Rasi chart."""
    dignity = calculate_dignity(planet_name, varga_sign, -1, planets)  # -1: no Moolatrikona degrees in a varga
    if dignity in ('Exalted', 'Debilitated', 'Own Sign') or planet_name in ('Rahu', 'Ketu', 'Ascendant'):
        return dignity
    lord = SIGN_LORDS[varga_sign]
    natural = NATURAL_FRIENDS.get(planet_name, {}).get(lord, 0)
    temporal = 1 if (planets[lord]['sign_index'] - planets[planet_name]['sign_index']) % 12 in (1, 2, 3, 9, 10, 11) else -1
    return {2: 'Great Friend', 1: 'Friend', 0: 'Neutral', -1: 'Enemy', -2: 'Great Enemy'}[natural + temporal]

# Pushkara navamsas (1-9 within the sign) by the sign's element: fire, earth, air, water
PUSHKARA_NAVAMSAS = {0: (7, 9), 1: (3, 5), 2: (6, 8), 3: (1, 3)}


def navamsa_table(planets):
    """Each graha's Navamsa: sign and lord, dignity there, Vargottama and Pushkara Navamsa."""
    rows = []
    for name in ('Ascendant', 'Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu'):
        p = planets[name]
        d9 = p['vargas']['D9']
        part = int(p['degree'] / (30 / 9)) + 1
        rows.append(dict(
            body=name, rasi=SIGNS[p['sign_index']], rasi_ta=TAMIL[p['sign_index']],
            navamsa_index=d9, navamsa=SIGNS[d9], navamsa_ta=TAMIL[d9], navamsa_part=part,
            lord=SIGN_LORDS[d9], dignity=None if name == 'Ascendant' else varga_dignity(name, d9, planets),
            vargottama=d9 == p['sign_index'], pushkara=part in PUSHKARA_NAVAMSAS[p['sign_index'] % 4]
        ))
    return rows

def calculate_aspects(planets):
    """Calculate Vedic Drishti (aspects) for all planets."""
    aspects = {name: {'casts_to_houses': [], 'aspects_received_from': []} for name in planets}
    for name, p in planets.items():
        if name == 'Ascendant': continue
        h = p['house']
        cast_houses = [(h + 6) % 12 or 12]  # 7th aspect for all
        if name == 'Mars':
            cast_houses.extend([(h + 3) % 12 or 12, (h + 7) % 12 or 12])  # 4th and 8th
        elif name == 'Jupiter':
            cast_houses.extend([(h + 4) % 12 or 12, (h + 8) % 12 or 12])  # 5th and 9th
        elif name == 'Saturn':
            cast_houses.extend([(h + 2) % 12 or 12, (h + 9) % 12 or 12])  # 3rd and 10th
        elif name in ('Rahu', 'Ketu'):
            cast_houses.extend([(h + 4) % 12 or 12, (h + 8) % 12 or 12])  # 5th and 9th
        aspects[name]['casts_to_houses'] = sorted(list(set(cast_houses)))

    for name, data in aspects.items():
        if name == 'Ascendant': continue
        for target_name, target_p in planets.items():
            if name != target_name and target_p['house'] in data['casts_to_houses']:
                aspects[target_name]['aspects_received_from'].append(name)
    return aspects

def calculate_ashtakavarga(planets):
    """Calculate Parashara Ashtakavarga for all 7 planets and Sarvashtakavarga."""
    bav = {}
    sav = [0] * 12
    classical = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']

    # Prastara: which contributor gave each bindu, the basis of Kakshya transit timing
    prastara = {}
    for p_name in classical:
        bav[p_name] = [0] * 12
        prastara[p_name] = {}
        rules = ASHTAKAVARGA_RULES.get(p_name, {})
        for ref_name, houses in rules.items():
            ref_sign = planets[ref_name]['sign_index']
            row = prastara[p_name][ref_name] = [0] * 12
            for h in houses:
                target_sign = (ref_sign + h - 1) % 12
                bav[p_name][target_sign] += 1
                row[target_sign] = 1

        for s in range(12):
            sav[s] += bav[p_name][s]

    # Sodhana: Trikona then Ekadhipatya reduction, and the Sodhya Pinda from the reduced bindus.
    # Checked against P.V.R. Narasimha Rao's worked Charts 7 and 11 (Vedic Astrology: An
    # Integrated Approach, ch. 12): a sign counts as occupied when it holds a graha or the Lagna.
    occupied = {planets[p]['sign_index'] for p in classical + ['Ascendant']}
    sodhita, pindas = {}, {}
    for p_name in classical:
        reduced = _ekadhipatya_sodhana(_trikona_sodhana(bav[p_name]), occupied)
        sodhita[p_name] = reduced
        rasi = sum(b * m for b, m in zip(reduced, RASI_GUNAKARA))
        graha = sum(GRAHA_GUNAKARA[q] * reduced[planets[q]['sign_index']] for q in classical)
        pindas[p_name] = dict(rasi=rasi, graha=graha, sodhya=rasi + graha)

    return {
        'BAV': bav,
        'SAV': sav,
        'prastara': prastara,
        'sodhita': sodhita,
        'pindas': pindas,
        'total_points': sum(sav)  # Guaranteed 337
    }


# Multipliers for the Sodhya Pinda: signs Aries-Pisces and the seven grahas
RASI_GUNAKARA = [7, 10, 8, 4, 10, 5, 7, 8, 9, 5, 11, 12]
GRAHA_GUNAKARA = {'Sun': 5, 'Moon': 5, 'Mars': 8, 'Mercury': 5, 'Jupiter': 10, 'Venus': 7, 'Saturn': 5}
DUAL_LORDSHIPS = [(0, 7), (1, 6), (2, 5), (8, 11), (9, 10)]  # Mars, Venus, Mercury, Jupiter, Saturn


def _trikona_sodhana(bindus):
    """In each trine of signs, remove the smallest count from all three (all of it when the
    three are equal); a trine holding a zero is left alone."""
    b = list(bindus)
    for r in range(4):
        trine = (r, r + 4, r + 8)
        values = [b[k] for k in trine]
        if 0 not in values:
            low = min(values)
            for k in trine:
                b[k] -= low
    return b


def _ekadhipatya_sodhana(bindus, occupied):
    """Reduce the two signs of one lord: untouched if either is zero or both are occupied;
    both empty: equal counts become zero, unequal both take the lower; one occupied: the
    empty sign becomes zero unless it holds more, when it drops to the occupied sign's count."""
    b = list(bindus)
    for r1, r2 in DUAL_LORDSHIPS:
        o1, o2 = r1 in occupied, r2 in occupied
        if b[r1] == 0 or b[r2] == 0 or (o1 and o2):
            continue
        if not o1 and not o2:
            b[r1] = b[r2] = 0 if b[r1] == b[r2] else min(b[r1], b[r2])
        else:
            full, empty = (r1, r2) if o1 else (r2, r1)
            b[empty] = b[full] if b[empty] > b[full] else 0
    return b

def detect_yogas(planets):
    """Yogas (see yogas.py) and the Manglik and Kaal Sarp doshas."""
    from .yogas import detect
    yogas = detect(planets)
    mars, jupiter = planets.get('Mars'), planets.get('Jupiter')

    # 9. Manglik / Kuja Dosha
    kuja_houses = [1, 2, 4, 7, 8, 12]
    mars_h = mars['house'] if mars else 0
    is_manglik = mars_h in kuja_houses
    reasons = []
    if is_manglik:
        if mars['dignity'] in ('Own Sign', 'Exalted'):
            reasons.append(f'Mars is strong in {mars["dignity"]}')
        if (mars['house'] - jupiter['house']) % 12 + 1 in (1, 5, 9, 7):
            reasons.append('Jupiter casts protective aspect or conjunction onto Mars')
        if mars['sign_index'] in (0, 7) and mars_h == 1:
            reasons.append('Mars in 1st house in Aries/Scorpio cancels Kuja Dosha')
    doshas = {
        'manglik': {
            'present': is_manglik,
            'house': mars_h,
            'cancelled': len(reasons) > 0,
            'reasons': reasons
        }
    }

    # 10. Kaal Sarp Dosha
    rahu = planets.get('Rahu')
    ketu = planets.get('Ketu')
    if rahu and ketu:
        r_lon = rahu['longitude']
        classical_7 = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']
        diffs = [((planets[p]['longitude'] - r_lon) % 360) for p in classical_7]
        all_one_side = all(d < 180 for d in diffs) or all(d >= 180 for d in diffs)
        if all_one_side:
            r_house = rahu['house']
            ks_en, ks_ta = KAAL_SARP_TYPES[(r_house - 1) % 12]
            doshas['kaal_sarp'] = {
                'present': True,
                'type': f'{ks_en} Kaal Sarp',
                'type_ta': f'{ks_ta} கால சர்ப்ப தோஷம்',
                'rahu_house': r_house,
                'description': f'All 7 classical planets are hemmed between Rahu and Ketu ({ks_en} Kaal Sarp). Fosters intense ambition and karmic acceleration.',
                'description_ta': f'ஏழு கிரகங்களும் ராகு-கேது அச்சுக்குள் அடங்கியுள்ளன ({ks_ta} கால சர்ப்பம்). தீவிர லட்சியத்தையும் கர்ம வேகத்தையும் தூண்டும்.'
            }
        else:
            doshas['kaal_sarp'] = {
                'present': False, 'type': 'None', 'type_ta': 'இல்லை',
                'description': 'Planets are freely dispersed around the nodal axis.',
                'description_ta': 'கிரகங்கள் ராகு-கேது அச்சின் இரு பக்கங்களிலும் பரவியுள்ளன.'
            }

    return yogas, doshas

def dasha(moon, birth, now=None, year=YEAR):
    """Calculate 3-Tier Vimshottari Dasa (Maha Dasa, Bhukti, Pratyantardasa)."""
    portion = moon / (40 / 3)
    index = int(portion) % 9
    start = birth - timedelta(days=(portion % 1) * DASHA_YEARS[index] * year)
    rows = []
    if now is None:
        now = datetime.now(timezone.utc)

    for k in range(9):
        i = (index + k) % 9
        d_years = DASHA_YEARS[i]
        end = start + timedelta(days=d_years * year)
        subs = []
        substart = start
        for m in range(9):
            j = (i + m) % 9
            b_years = DASHA_YEARS[j]
            subend = substart + timedelta(days=d_years * b_years / 120 * year)
            # Level 3: Pratyantardasa
            prats = []
            pstart = substart
            for n in range(9):
                p_idx = (j + n) % 9
                p_years = DASHA_YEARS[p_idx]
                pend = pstart + timedelta(days=d_years * b_years * p_years / (120 * 120) * year)
                is_p_active = (pstart <= now < pend)
                prats.append(dict(
                    lord=DASHA_NAMES[p_idx],
                    start=pstart.isoformat(),
                    end=pend.isoformat(),
                    is_active=is_p_active
                ))
                pstart = pend

            subs.append(dict(
                lord=DASHA_NAMES[j],
                start=substart.isoformat(),
                end=subend.isoformat(),
                pratyantars=prats,
                is_active=(substart <= now < subend)
            ))
            substart = subend

        rows.append(dict(
            lord=DASHA_NAMES[i],
            start=start.isoformat(),
            end=end.isoformat(),
            subperiods=subs,
            is_active=(start <= now < end)
        ))
        start = end

    return rows

# Yogini Dasa: eight yoginis in a 36-year cycle; the birth star fixes the first
# ((nakshatra number + 3) mod 8), bhuktis start from the Dasa's own yogini.
YOGINIS = [('Mangala', 'மங்களா', 'Moon', 1), ('Pingala', 'பிங்களா', 'Sun', 2), ('Dhanya', 'தான்யா', 'Jupiter', 3),
           ('Bhramari', 'பிராமரி', 'Mars', 4), ('Bhadrika', 'பத்ரிகா', 'Mercury', 5), ('Ulka', 'உல்கா', 'Saturn', 6),
           ('Siddha', 'சித்தா', 'Venus', 7), ('Sankata', 'சங்கடா', 'Rahu', 8)]

def yogini_dasha(moon, birth, now=None, cycles=4, year=YEAR):
    """Yogini Dasa periods from the birth-star balance, with bhuktis."""
    portion = moon / (40 / 3)
    first = (int(portion) + 1 + 3) % 8 - 1  # zero-based yogini, (star number + 3) mod 8
    first_years = YOGINIS[first][3]
    start = birth - timedelta(days=(portion % 1) * first_years * year)
    now = now or datetime.now(timezone.utc)
    rows = []
    for k in range(8 * cycles):
        i = (first + k) % 8
        name, name_ta, lord, years = YOGINIS[i]
        end = start + timedelta(days=years * year)
        subs, sub_start = [], start
        for m in range(8):
            j = (i + m) % 8
            sub_end = sub_start + timedelta(days=years * YOGINIS[j][3] / 36 * year)
            subs.append(dict(yogini=YOGINIS[j][0], yogini_ta=YOGINIS[j][1], lord=YOGINIS[j][2],
                             start=sub_start.isoformat(), end=sub_end.isoformat(), is_active=sub_start <= now < sub_end))
            sub_start = sub_end
        rows.append(dict(yogini=name, yogini_ta=name_ta, lord=lord, years=years,
                         start=start.isoformat(), end=end.isoformat(), subperiods=subs, is_active=start <= now < end))
        start = end
    return rows

def get_active_dasha(dasha_rows):
    """Extract currently active 3-tier dasa from calculated rows."""
    for d in dasha_rows:
        if d.get('is_active'):
            for b in d.get('subperiods', []):
                if b.get('is_active'):
                    for p in b.get('pratyantars', []):
                        if p.get('is_active'):
                            return {
                                'dasa': d['lord'],
                                'bhukti': b['lord'],
                                'pratyantar': p['lord'],
                                'start': p['start'],
                                'end': p['end'],
                                'dasa_end': d['end'],
                                'bhukti_end': b['end']
                            }
    return None


def calculate_panchangam(utc_dt, lat, lon, sun_lon, moon_lon, tz_name='UTC'):
    """Compute complete Vedic Panchangam and Muhurtha windows.

    Muhurtha windows are for the local civil date of utc_dt in tz_name and are
    returned both in UTC (``*_utc``) and in local clock time (``*_local``).
    """
    elong = (moon_lon - sun_lon) % 360
    tithi_num = int(elong // 12) + 1
    tithi_rem = 1.0 - ((elong % 12) / 12.0)
    paksha = 'Shukla (waxing)' if elong < 180 else 'Krishna (waning)'

    star_idx = int(moon_lon / (40 / 3))
    pada = int((moon_lon % (40 / 3)) / (10 / 3)) + 1

    yoga_num = int(((moon_lon + sun_lon) % 360) / (40 / 3)) + 1
    yoga_name, yoga_ausp = NITYA_YOGAS[(yoga_num - 1) % 27]

    karana_half = int(elong // 6) + 1
    if karana_half == 1:
        karana_name = 'Kimstughna'
    elif karana_half >= 58:
        karana_name = ['Shakuni', 'Chatushpada', 'Naga'][karana_half - 58]
    else:
        karana_name = KARANAS[(karana_half - 2) % 7]

    # Sunrise / sunset of the local civil date (Swiss Ephemeris rise/set)
    try:
        tz = ZoneInfo(tz_name)
    except ZoneInfoNotFoundError:
        raise ValueError('Enter a valid IANA timezone, such as Asia/Kolkata.')
    local_date = utc_dt.astimezone(tz).date()
    sun = sun_events(local_date, tz, lat, lon)
    sunrise_jd, sunset_jd = sun['sunrise'], sun['sunset']
    day_len = sunset_jd - sunrise_jd

    def fmt_time(jd, zone):
        return jd_to_utc(jd).astimezone(zone).strftime('%H:%M')

    def window(start_jd, end_jd):
        return {
            'utc': f"{fmt_time(start_jd, timezone.utc)} - {fmt_time(end_jd, timezone.utc)}",
            'local': f"{fmt_time(start_jd, tz)} - {fmt_time(end_jd, tz)}"
        }

    # Muhurtha 8-segment calculation based on the local weekday
    weekday = local_date.weekday()  # 0=Monday, ..., 6=Sunday
    seg = day_len / 8.0

    rahu_segs = [2, 7, 5, 6, 4, 3, 8]       # Mon-Sun (1-based)
    yama_segs = [4, 3, 2, 1, 7, 6, 5]
    guli_segs = [6, 5, 4, 3, 2, 1, 7]

    def seg_window(seg_idx):
        start = sunrise_jd + (seg_idx - 1) * seg
        return window(start, start + seg)

    # Abhijit Muhurtham: 8th of 15 daytime muhurthas
    abhijit_st = sunrise_jd + 7 * (day_len / 15.0)
    abhijit = window(abhijit_st, abhijit_st + day_len / 15.0)
    rahu = seg_window(rahu_segs[weekday])
    yama = seg_window(yama_segs[weekday])
    guli = seg_window(guli_segs[weekday])

    return dict(
        tithi=tithi_num,
        tithi_name=TITHIS[tithi_num - 1],
        paksha=paksha,
        tithi_percent_remaining=round(tithi_rem * 100, 1),
        nakshatra=STARS[star_idx],
        tamil_nakshatra=TAMIL_STARS[star_idx],
        nakshatra_lord=STAR_LORDS[star_idx],
        nakshatra_gana=STAR_GANAS[star_idx],
        nakshatra_yoni=STAR_YONIS[star_idx][0],
        nakshatra_rajju=STAR_RAJJUS[star_idx],
        pada=pada,
        yoga_number=yoga_num,
        yoga_name=yoga_name,
        yoga_auspiciousness=yoga_ausp,
        karana_half_number=karana_half,
        karana_name=karana_name,
        timezone=tz_name,
        local_date=local_date.isoformat(),
        weekday=local_date.strftime('%A'),
        sunrise_utc=fmt_time(sunrise_jd, timezone.utc),
        sunset_utc=fmt_time(sunset_jd, timezone.utc),
        sunrise_local=fmt_time(sunrise_jd, tz),
        sunset_local=fmt_time(sunset_jd, tz),
        day_length_hours=round(day_len * 24, 2),
        rahu_kalam_utc=rahu['utc'],
        yamagandam_utc=yama['utc'],
        gulika_kalam_utc=guli['utc'],
        abhijit_muhurtham_utc=abhijit['utc'],
        rahu_kalam_local=rahu['local'],
        yamagandam_local=yama['local'],
        gulika_kalam_local=guli['local'],
        abhijit_muhurtham_local=abhijit['local']
    )

def calculate_match(boy, girl):
    """
    Compute South Indian 10 Poruthams & North Indian 36 Guna Milan.
    Parameters boy and girl can be either chart calculation objects or
    dictionaries with 'nakshatra_index' (0-26) and 'sign_index' (0-11).
    """
    def get_indices(p):
        if 'planets' in p:
            m = p['planets']['Moon']
            return STARS.index(m['nakshatra']), m['sign_index']
        return int(p['nakshatra_index']), int(p['sign_index'])

    b_star, b_sign = get_indices(boy)
    g_star, g_sign = get_indices(girl)

    def summary(p, star, sign):
        """Star attributes of one partner, plus name, pada and Lagna when a full chart was given."""
        gana, yoni, rajju, nadi = STAR_GANAS[star], STAR_YONIS[star][0], STAR_RAJJUS[star], STAR_NADIS[star]
        out = dict(nakshatra=STARS[star], nakshatra_ta=TAMIL_STARS[star], nakshatra_index=star,
                   sign=SIGNS[sign], sign_ta=TAMIL[sign], sign_index=sign,
                   gana=gana, gana_ta=GANA_TA[gana], yoni=yoni, yoni_ta=YONI_TA[yoni],
                   rajju=rajju, rajju_ta=RAJJU_TA[rajju], nadi=nadi, nadi_ta=NADI_TA[nadi])
        if 'planets' in p:
            asc = p['planets']['Ascendant']
            out.update(name=p.get('profile', {}).get('name', ''), pada=p['planets']['Moon']['pada'],
                       lagna=asc['sign'], lagna_ta=asc['tamil'])
        return out

    poruthams = []

    # 1. Dina Porutham (Health & Prosperity): count from the girl's star to the boy's.
    # When both share one star, Tamil tradition grades the star itself (Eka Nakshatra).
    star_dist = (b_star - g_star) % 27 + 1
    if star_dist == 1:
        eka = EKA_NAKSHATRA_GRADE[g_star]
        dina_ok = eka != 'avoid'
        dina_pts = 3 if eka == 'uthamam' else (1.5 if eka == 'madhyamam' else 0)
        dina_desc = f'Same birth star ({STARS[g_star]}): graded {eka} under Eka Nakshatra rules.'
        dina_desc_ta = f'இருவருக்கும் ஒரே நட்சத்திரம் ({TAMIL_STARS[g_star]}): ஏக நட்சத்திர விதிப்படி {EKA_GRADE_TA[eka]}.'
    else:
        dina_ok = star_dist in DINA_GOOD_COUNTS
        dina_pts = 3 if dina_ok else 0
        dina_desc = f"Boy's star is {star_dist} from the girl's. Harmony in day-to-day vitality, health, and mutual longevity."
        dina_desc_ta = f'பெண் நட்சத்திரத்திலிருந்து ஆண் நட்சத்திரம் {star_dist}-வது. அன்றாட ஆரோக்கியம், நலம் மற்றும் ஆயுள் ஒற்றுமை.'
    poruthams.append({
        'name': 'Dina Porutham',
        'tamil': 'தினப் பொருத்தம்',
        'passed': dina_ok,
        'points': dina_pts,
        'max_points': 3,
        'description': dina_desc,
        'description_ta': dina_desc_ta
    })

    # 2. Gana Porutham (Temperament)
    b_gana = STAR_GANAS[b_star]
    g_gana = STAR_GANAS[g_star]
    gana_ok = (b_gana == g_gana) or (b_gana == 'Deva' and g_gana == 'Manushya')
    poruthams.append({
        'name': 'Gana Porutham',
        'tamil': 'கணப் பொருத்தம்',
        'passed': gana_ok,
        'points': 6 if gana_ok else (3 if b_gana == 'Manushya' and g_gana == 'Deva' else 0),
        'max_points': 6,
        'description': f'Temperament alignment ({g_gana} & {b_gana}).',
        'description_ta': f'குண ஒற்றுமை ({GANA_TA[g_gana]} & {GANA_TA[b_gana]}).'
    })

    # 3. Mahendra Porutham (Progeny & Lineage)
    mahendra_dist = (b_star - g_star) % 27 + 1
    mahendra_ok = mahendra_dist in (4, 7, 10, 13, 16, 19, 22, 25)
    poruthams.append({
        'name': 'Mahendra Porutham',
        'tamil': 'மகேந்திரப் பொருத்தம்',
        'passed': mahendra_ok,
        'points': 2 if mahendra_ok else 0,
        'max_points': 2,
        'description': 'Family continuity, children, and enduring attachment.',
        'description_ta': 'குடும்ப விருத்தி, சந்ததி மற்றும் நிலைத்த பந்தம்.'
    })

    # 4. Stree Deergha Porutham (Longevity of Bride)
    stree_ok = star_dist >= 13
    poruthams.append({
        'name': 'Stree Deergha Porutham',
        'tamil': 'ஸ்திரீ தீர்க்கப் பொருத்தம்',
        'passed': stree_ok,
        'points': 1 if stree_ok else (0.5 if star_dist >= 7 else 0),
        'max_points': 1,
        'description': 'Auspicious fortune and well-being for the bride.',
        'description_ta': 'மணமகளின் நலமும் சௌபாக்கியமும்.'
    })

    # 5. Yoni Porutham (Physical Affinity)
    b_animal = STAR_YONIS[b_star][0]
    g_animal = STAR_YONIS[g_star][0]
    enemies = {
        'Horse': 'Buffalo', 'Buffalo': 'Horse', 'Elephant': 'Lion', 'Lion': 'Elephant',
        'Sheep': 'Monkey', 'Monkey': 'Sheep', 'Serpent': 'Mongoose', 'Mongoose': 'Serpent',
        'Dog': 'Deer', 'Deer': 'Dog', 'Cat': 'Rat', 'Rat': 'Cat', 'Cow': 'Tiger', 'Tiger': 'Cow'
    }
    is_enemy = (enemies.get(b_animal) == g_animal)
    yoni_ok = (b_animal == g_animal) or not is_enemy
    yoni_pts = 4 if b_animal == g_animal else (0 if is_enemy else 2)
    poruthams.append({
        'name': 'Yoni Porutham',
        'tamil': 'யோனிப் பொருத்தம்',
        'passed': yoni_ok and not is_enemy,
        'points': yoni_pts,
        'max_points': 4,
        'description': f'Physical and sexual harmony ({g_animal} & {b_animal}).',
        'description_ta': f'உடல் மற்றும் தாம்பத்திய ஒற்றுமை ({YONI_TA[g_animal]} & {YONI_TA[b_animal]}).'
    })

    # 6. Rasi Porutham (Family Unity)
    sign_dist = (b_sign - g_sign) % 12 + 1
    rasi_ok = sign_dist in (7, 11, 10, 9, 3, 4, 5)
    poruthams.append({
        'name': 'Rasi Porutham',
        'tamil': 'ராசிப் பொருத்தம்',
        'passed': rasi_ok,
        'points': 7 if rasi_ok else 0,
        'max_points': 7,
        'description': 'Family harmony, mutual understanding, and fortune.',
        'description_ta': 'குடும்ப ஒற்றுமை, பரஸ்பர புரிதல் மற்றும் அதிர்ஷ்டம்.'
    })

    # 7. Rasiyathipathi Porutham (Sign Lords Friendship)
    b_lord = SIGN_LORDS[b_sign]
    g_lord = SIGN_LORDS[g_sign]
    lord_rel = NATURAL_FRIENDS.get(b_lord, {}).get(g_lord, 0)
    lord_ok = (b_lord == g_lord or lord_rel >= 0)
    poruthams.append({
        'name': 'Rasiyathipathi Porutham',
        'tamil': 'ராசியாதிபதிப் பொருத்தம்',
        'passed': lord_ok,
        'points': 5 if b_lord == g_lord or lord_rel == 1 else (3 if lord_rel == 0 else 0),
        'max_points': 5,
        'description': f'Cordial friendship between sign rulers {g_lord} and {b_lord}.',
        'description_ta': f'ராசி அதிபதிகள் {PLANET_TAMIL[g_lord]} மற்றும் {PLANET_TAMIL[b_lord]} இடையிலான நட்பு.'
    })

    # 8. Vasiya Porutham (Magnetic Attraction)
    vasiya_pairs = {
        0: [4, 7], 1: [3, 6], 2: [5], 3: [7, 8], 4: [6], 5: [11, 2],
        6: [9], 7: [3], 8: [11], 9: [0, 10], 10: [0], 11: [9]
    }
    vasiya_ok = (b_sign in vasiya_pairs.get(g_sign, [])) or (g_sign in vasiya_pairs.get(b_sign, []))
    poruthams.append({
        'name': 'Vasiya Porutham',
        'tamil': 'வசியப் பொருத்தம்',
        'passed': vasiya_ok,
        'points': 2 if vasiya_ok else 0,
        'max_points': 2,
        'description': 'Mutual magnetism and enduring emotional devotion.',
        'description_ta': 'பரஸ்பர ஈர்ப்பு மற்றும் நிலைத்த அன்பு.'
    })

    # 9. Rajju Porutham (Marital Longevity - Critical)
    b_rajju = STAR_RAJJUS[b_star]
    g_rajju = STAR_RAJJUS[g_star]
    rajju_ok = (b_rajju != g_rajju)  # Must be different!
    poruthams.append({
        'name': 'Rajju Porutham',
        'tamil': 'ரஜ்ஜுப் பொருத்தம்',
        'passed': rajju_ok,
        'points': 8 if rajju_ok else 0,
        'max_points': 8,
        'critical': True,
        'description': f'Essential marriage knot stability (Girl: {g_rajju}, Boy: {b_rajju}).' if rajju_ok else
                       f'Both stars share {b_rajju} Rajju, traditionally said to threaten {RAJJU_EFFECTS[b_rajju]}.',
        'description_ta': f'மாங்கல்ய பலம் (பெண்: {RAJJU_TA[g_rajju]}, ஆண்: {RAJJU_TA[b_rajju]}).' if rajju_ok else
                          f'இருவருக்கும் {RAJJU_TA[b_rajju]} ரஜ்ஜு; இது {RAJJU_EFFECTS_TA[b_rajju]} பாதிக்கும் என்பது மரபு.'
    })

    # 10. Vedha Porutham (Absence of Affliction)
    is_vedha = any({b_star, g_star} <= group and b_star != g_star for group in VEDHA_GROUPS)
    poruthams.append({
        'name': 'Vedha Porutham',
        'tamil': 'வேதைப் பொருத்தம்',
        'passed': not is_vedha,
        'points': 4 if not is_vedha else 0,
        'max_points': 4,
        'description': 'Shield from invisible conflicts, sorrow, and sudden obstacles.',
        'description_ta': 'மறைமுக முரண்பாடுகள், துயரங்கள் மற்றும் திடீர் தடைகளிலிருந்து பாதுகாப்பு.'
    })

    # North Indian 36 Guna Milan
    # 1. Varna (1): water signs Brahmin (4), fire Kshatriya (3), earth Vaishya (2), air Shudra (1)
    varna_rank = [3, 2, 1, 4]  # indexed by sign % 4: fire, earth, air, water
    varna_pts = 1 if varna_rank[b_sign % 4] >= varna_rank[g_sign % 4] else 0
    # 2. Vashya (2)
    vashya_pts = 2 if vasiya_ok else 1
    # 3. Tara (3): 1.5 for each direction whose tara is not Vipat, Pratyak or Naidhana
    def tara_good(from_star, to_star):
        return ((to_star - from_star) % 27) % 9 + 1 not in (3, 5, 7)
    tara_pts = 1.5 * tara_good(g_star, b_star) + 1.5 * tara_good(b_star, g_star)
    # 4. Yoni (4)
    yoni_milan_pts = yoni_pts
    # 5. Graha Maitri (5): natural friendship of the two Moon-sign lords, seen from both sides
    if b_lord == g_lord:
        graha_pts = 5
    else:
        views = sorted((lord_rel, NATURAL_FRIENDS.get(g_lord, {}).get(b_lord, 0)))
        graha_pts = {(1, 1): 5, (0, 1): 4, (0, 0): 3, (-1, 1): 1, (-1, 0): 0.5, (-1, -1): 0}[tuple(views)]
    # 6. Gana (6)
    gana_pts = 6 if b_gana == g_gana else (3 if b_gana == 'Deva' and g_gana == 'Manushya' else 0)
    # 7. Bhakoot (7): the 2/12, 5/9 and 6/8 sign relationships are doshas
    bhakoot_pts = 7 if sign_dist in (1, 3, 4, 7, 10, 11) else 0
    # 8. Nadi (8)
    nadi_pts = 8 if STAR_NADIS[b_star] != STAR_NADIS[g_star] else 0

    guna_score = varna_pts + vashya_pts + tara_pts + yoni_milan_pts + graha_pts + gana_pts + bhakoot_pts + nadi_pts
    passed_poruthams = sum(1 for p in poruthams if p['passed'])

    verdict = 'Auspicious Match' if (passed_poruthams >= 6 and rajju_ok and guna_score >= 18) else \
              ('Moderate Match' if (passed_poruthams >= 5 and rajju_ok) else 'Inauspicious / Needs Remedies')

    # Dosha Samyam needs the full birth charts, not just star and sign.
    dosha_samyam = None
    verdict_notes = []
    if 'planets' in boy and 'planets' in girl:
        # Imported here: south_indian builds on this module's primitives.
        from .south_indian import compare_dosha_samyam
        dosha_samyam = compare_dosha_samyam(boy['planets'], girl['planets'], boy.get('dasha'), girl.get('dasha'))
        # An unbalanced dosha or a Dasa Sandhi lowers the porutham verdict by one step
        if not dosha_samyam['chevvai_balanced']:
            verdict_notes.append(('Chevvai Dosham is not balanced between the charts',
                                  'செவ்வாய் தோஷம் இருவருக்கும் சமமாக இல்லை'))
        if not dosha_samyam['papa_balanced']:
            verdict_notes.append(("The bride's Papa points exceed the groom's",
                                  'பெண்ணின் பாப புள்ளிகள் ஆணின் புள்ளிகளை விட அதிகம்'))
        if dosha_samyam['dasa_sandhi'] and dosha_samyam['dasa_sandhi']['present']:
            verdict_notes.append(('A Dasa Sandhi falls in the coming years', 'வரும் ஆண்டுகளில் தசா சந்தி ஏற்படுகிறது'))
        if verdict_notes:
            verdict = {'Auspicious Match': 'Moderate Match'}.get(verdict, 'Inauspicious / Needs Remedies')

    return {
        'poruthams': poruthams,
        'passed_count': passed_poruthams,
        'total_poruthams': 10,
        'rajju_agreement': rajju_ok,
        'guna_milan': {
            'varna': varna_pts,
            'vashya': vashya_pts,
            'tara': tara_pts,
            'yoni': yoni_milan_pts,
            'graha_maitri': graha_pts,
            'gana': gana_pts,
            'bhakoot': bhakoot_pts,
            'nadi': nadi_pts,
            'total_score': round(guna_score, 1),
            'max_score': 36
        },
        'dosha_samyam': dosha_samyam,
        'groom': summary(boy, b_star, b_sign),
        'bride': summary(girl, g_star, g_sign),
        'verdict': verdict,
        'verdict_ta': MATCH_VERDICT_TA[verdict],
        'verdict_notes': [{'en': en, 'ta': ta} for en, ta in verdict_notes]
    }

def synthesize_readings(planets, dasha_active, yogas):
    """Generate synthesized astrological life readings."""
    asc = planets['Ascendant']
    moon = planets['Moon']
    sun = planets['Sun']
    tenth_h = [p_name for p_name, p in planets.items() if p['house'] == 10]
    seventh_h = [p_name for p_name, p in planets.items() if p['house'] == 7]
    second_h = [p_name for p_name, p in planets.items() if p['house'] == 2]
    eleventh_h = [p_name for p_name, p in planets.items() if p['house'] == 11]

    career_planets = ', '.join(tenth_h) if tenth_h else f"governed by 10th Lord {SIGN_LORDS[(asc['sign_index'] + 9) % 12]}"
    partner_planets = ', '.join(seventh_h) if seventh_h else f"governed by 7th Lord {SIGN_LORDS[(asc['sign_index'] + 6) % 12]}"
    wealth_planets = ', '.join(second_h + eleventh_h) if (second_h or eleventh_h) else f"anchored by {SIGN_LORDS[(asc['sign_index'] + 1) % 12]} and {SIGN_LORDS[(asc['sign_index'] + 10) % 12]}"

    active_summary = "Period information available upon chart date computation."
    if dasha_active:
        active_summary = f"Currently traversing {dasha_active['dasa']} Maha Dasa, {dasha_active['bhukti']} Bhukti, and {dasha_active['pratyantar']} Pratyantardasa. Focus aligns with the qualities and house lordship of {dasha_active['bhukti']}."

    yoga_titles = [y['name'] for y in yogas if y.get('nature') == 'good'][:4]
    yoga_text = f"Empowered by auspicious yogas including {', '.join(yoga_titles)}." if yoga_titles else "A balanced natal configuration with dynamic potential across houses."

    return {
        'lagna': f"Born with {asc['sign']} ({asc['tamil']}) Ascendant. Bestows distinct individuality, resilient constitution, and leadership driven by {SIGN_LORDS[asc['sign_index']]}.",
        'moon': f"Chandra sits in {moon['sign']} ({moon['tamil']}) under {moon['nakshatra']} Nakshatra (Pada {moon['pada']}). Reflects deep intuition, thoughtful perceptiveness, and emotional responsiveness.",
        'sun': f"Surya illuminates {sun['sign']} ({sun['tamil']}). Commands inner willpower, creative ambition, and personal authority.",
        'career': f"10th House of Karma and Profession is {career_planets}. Directs worldly vocational focus toward strategic leadership, enterprise, and public credibility.",
        'wealth': f"2nd House of Possessions and 11th House of Gains are influenced by {wealth_planets}. Supports sustained prosperity, progressive capital accumulation, and profitable associations.",
        'relationships': f"7th House of Partnership is {partner_planets}. Emphasizes devotion, contractual integrity, and companionship based on mutual respect.",
        'dasa_focus': active_summary,
        'yogas_summary': yoga_text
    }

def calculate(data):
    """Main calculation entry point."""
    lat = float(data['latitude'])
    lon = float(data['longitude'])
    if not math.isfinite(lat) or not -66 <= lat <= 66:
        raise ValueError('Latitude must be between 66° south and 66° north in this version.')
    if not math.isfinite(lon) or not -180 <= lon <= 180:
        raise ValueError('Longitude must be between -180 and 180.')

    ayan = data.get('ayanamsa', 'Lahiri')
    if ayan not in AYAN:
        raise ValueError('Unsupported ayanamsa.')

    fold = data.get('fold')
    fold = None if fold in (None, '') else int(fold)
    utc = local_to_utc(data['date'], data['time'], data['timezone'], fold)
    jd = swe.julday(utc.year, utc.month, utc.day, utc.hour + utc.minute / 60 + utc.second / 3600)

    swe.set_sid_mode(AYAN[ayan])
    flags = swe.FLG_MOSEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED

    planets = {}
    for name, number in GRAHA_BODIES:
        pos = swe.calc_ut(jd, number, flags)[0]
        planets[name] = placement(pos[0], pos[3])
    ayanamsa_degrees = swe.get_ayanamsa_ut(jd)

    # Ketu is opposite Rahu
    planets['Ketu'] = placement(planets['Rahu']['longitude'] + 180, planets['Rahu']['speed'])

    # Ascendant (Lagna)
    asc = swe.houses_ex(jd, lat, lon, b'P', swe.FLG_SIDEREAL)[1][0]
    planets['Ascendant'] = placement(asc)

    # Krishnamurti Paddhati works in its own (Krishnamurti) ayanamsa whatever the chart uses:
    # sub-lords are arc-minutes wide, so a Lahiri or Raman offset would change them.
    # Placidus cusps: pyswisseph returns 12, the pysweph fork pads index 0 and returns 13.
    swe.set_sid_mode(swe.SIDM_KRISHNAMURTI)
    kp = dict(
        cusps=list(swe.houses_ex(jd, lat, lon, b'P', swe.FLG_SIDEREAL)[0][-12:]),
        planets={name: swe.calc_ut(jd, number, flags)[0][0] for name, number in GRAHA_BODIES},
        ayanamsa=swe.get_ayanamsa_ut(jd)
    )
    kp['planets']['Ketu'] = (kp['planets']['Rahu'] + 180) % 360
    swe.set_sid_mode(AYAN[ayan])

    # Calculate whole-sign houses from Ascendant
    asc_sign = planets['Ascendant']['sign_index']
    for p in planets.values():
        p['house'] = (p['sign_index'] - asc_sign) % 12 + 1

    # Sripati Bhava Chakra: the 'Bhava' chart places each graha in its bhava counted from the Lagna sign
    bhava_madhya, bhava_sandhi = sripati_bhavas(jd, lat, lon)
    for p in planets.values():
        p['bhava'] = bhava_of(p['longitude'], bhava_sandhi)
        p['vargas']['Bhava'] = (asc_sign + p['bhava'] - 1) % 12

    # Calculate Dignities and Combustion
    sun_lon = planets['Sun']['longitude']
    combust_thresholds = {'Moon': 12, 'Mars': 17, 'Mercury': 14, 'Jupiter': 11, 'Venus': 10, 'Saturn': 15}
    for p_name, p in planets.items():
        if p_name != 'Ascendant':
            p['dignity'] = calculate_dignity(p_name, p['sign_index'], p['degree'], planets)
            if p_name in combust_thresholds:
                dist = min((p['longitude'] - sun_lon) % 360, (sun_lon - p['longitude']) % 360)
                thresh = combust_thresholds[p_name]
                if p['retrograde'] and p_name in ('Mercury', 'Venus'): thresh -= 2
                p['combust'] = (dist <= thresh)
            else:
                p['combust'] = False

    # Calculate Aspects (Drishti)
    aspects_info = calculate_aspects(planets)
    for p_name, asp in aspects_info.items():
        planets[p_name]['aspects_cast'] = asp['casts_to_houses']
        planets[p_name]['aspects_received'] = asp['aspects_received_from']

    # Ashtakavarga
    ashtakavarga = calculate_ashtakavarga(planets)

    # Current transits (Gochara), in this chart's ayanamsa
    gochara = calculate_gochara(utc_to_jd(datetime.now(timezone.utc)), planets, ashtakavarga)
    gochara['saturn_cycles'] = saturn_life_cycles(jd, planets['Moon']['sign_index'])

    # Yogas and Doshas
    yogas, doshas = detect_yogas(planets)

    # 3-Tier Vimshottari Dasa
    moon_lon = planets['Moon']['longitude']
    from .dasas import DASA_YEARS, year_days, ashtottari_dasha, ashtottari_applicable, chara_dasha
    dasa_year_kind = data.get('dasa_year') or 'julian'
    dasa_year = year_days(dasa_year_kind)
    dasha_rows = dasha(moon_lon, utc, year=dasa_year)
    active_dasha = get_active_dasha(dasha_rows)
    yogini_rows = yogini_dasha(moon_lon, utc, year=dasa_year)
    ashtottari_rows = ashtottari_dasha(moon_lon, utc, year=dasa_year)
    chara_rows = chara_dasha(planets, utc, year=dasa_year)

    # Panchangam
    panchangam = calculate_panchangam(utc, lat, lon, sun_lon, moon_lon, data['timezone'])

    # South Indian (Tamil) jathagam details and doshas. Imported here:
    # south_indian builds on this module's primitives.
    from .south_indian import build_south_indian_details, chevvai_dosham, rahu_ketu_dosham, vedic_day
    from .shadbala import compute_shadbala, compute_bhava_bala, compute_vimsopaka
    doshas['chevvai'] = chevvai_dosham(planets)
    doshas['rahu_ketu'] = rahu_ketu_dosham(planets)
    south_indian = build_south_indian_details(planets, utc, data['timezone'], lat, lon)
    mandi = south_indian['mandi']
    mandi['bhava'] = bhava_of(mandi['longitude'], bhava_sandhi)
    mandi['vargas']['Bhava'] = (asc_sign + mandi['bhava'] - 1) % 12

    # Shadbala over the Vedic day (sunrise to sunrise) of birth
    birth_tz = ZoneInfo(data['timezone'])
    vedic_date, day_events = vedic_day(jd, birth_tz, lat, lon)
    day_events['prev_sunset'] = sun_events(vedic_date - timedelta(days=1), birth_tz, lat, lon)['sunset']
    shadbala = compute_shadbala(planets, jd, day_events, vedic_date, bhava_madhya, ayanamsa_degrees)
    bhava_bala = compute_bhava_bala(planets, bhava_madhya, shadbala)
    vimsopaka = compute_vimsopaka(planets)
    # Graha Yuddha: Mars to Saturn within a degree; the one Shadbala credits won
    warriors = ['Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']
    south_indian['extras']['graha_yuddha'] = [
        dict(winner=a, loser=b) if shadbala[a]['yuddha'] >= shadbala[b]['yuddha'] else dict(winner=b, loser=a)
        for i, a in enumerate(warriors) for b in warriors[i + 1:]
        if abs((planets[a]['longitude'] - planets[b]['longitude'] + 180) % 360 - 180) < 1]

    # Synthesized readings
    readings = synthesize_readings(planets, active_dasha, yogas)

    # House Details Summary
    house_details = []
    for h in range(1, 13):
        h_sign = (asc_sign + h - 1) % 12
        occupants = [n for n, p in planets.items() if p['house'] == h]
        aspected_by = [
            n for n, p in planets.items()
            if n != 'Ascendant' and h in p.get('aspects_cast', [])
        ]
        house_details.append({
            'house': h,
            'sign': SIGNS[h_sign],
            'tamil': TAMIL[h_sign],
            'sign_index': h_sign,
            'lord': SIGN_LORDS[h_sign],
            'sav_points': ashtakavarga['SAV'][h_sign],
            'occupants': occupants,
            'aspected_by': aspected_by
        })

    # Vargas quick map for frontend renderers
    vargas_map = {}
    varga_keys = ['D1', 'D2', 'D3', 'D4', 'D7', 'D9', 'D10', 'D12', 'D16', 'D20', 'D24', 'D27', 'D30', 'D40', 'D45', 'D60', 'Bhava']
    for v_key in varga_keys:
        vargas_map[v_key] = {
            p_name: p['vargas'][v_key]
            for p_name, p in planets.items()
        }

    chart_summary = dict(
        planets=planets,
        panchanga=panchangam,
        active_dasha=active_dasha,
        dasha=dasha_rows,
        house_details=house_details,
        ashtakavarga=ashtakavarga,
        vargas=vargas_map,
        yogas=yogas,
        doshas=doshas,
        jd=jd,
        lat=lat,
        lon=lon,
        utc=utc,
        kp_cusps=kp['cusps'],
        kp=kp,
        gochara=gochara,
        shadbala=shadbala,
        bhava_bala=bhava_bala,
        vimsopaka=vimsopaka,
        vedic_weekday=south_indian['vaaram']['index'],
        timezone=data['timezone']
    )
    predictions = generate_comprehensive_predictions(chart_summary)

    return dict(
        profile={k: str(data.get(k, ''))[:200] for k in ['name', 'date', 'time', 'timezone', 'city', 'latitude', 'longitude', 'ayanamsa', 'fold', 'dasa_year']},
        utc=utc.isoformat(),
        julian_day=jd,
        ayanamsa_degrees=ayanamsa_degrees,
        planets=planets,
        dasha=dasha_rows,
        active_dasha=active_dasha,
        yogini_dasha=yogini_rows,
        ashtottari_dasha=ashtottari_rows,
        ashtottari_applicable=ashtottari_applicable(planets),
        chara_dasha=chara_rows,
        dasa_year=dict(key=dasa_year_kind, days=dasa_year, en=DASA_YEARS[dasa_year_kind][1], ta=DASA_YEARS[dasa_year_kind][2]),
        panchanga=panchangam,
        ashtakavarga=ashtakavarga,
        yogas=yogas,
        doshas=doshas,
        vargas=vargas_map,
        house_details=house_details,
        readings=readings,
        kp_cusps=kp['cusps'],
        gochara=gochara,
        navamsa_table=navamsa_table(planets),
        bhava_chakra=dict(system='Sripati', madhya=bhava_madhya, sandhi=bhava_sandhi),
        south_indian=south_indian,
        predictions=predictions,
        method=dict(
            engine='Swiss Ephemeris ' + swe.version,
            ephemeris='Moshier analytical ephemeris',
            ayanamsa=ayan,
            houses='Whole sign',
            nodes='Mean node',
            dasha_year_days=dasa_year,
            ashtakavarga_standard='Parashara (337 points)',
            legacy_match='Enhanced high-precision Vedic & modern algorithms'
        )
    )
