"""JoRoScope South Indian (Tamil) Jathagam Module
Tamil-tradition calculations layered on the core engine:
- Vaaram (Vedic weekday, sunrise to sunrise) and Udayadi Nazhigai
- Tamil solar calendar: 60-year cycle, month and date (sunset rule)
- Dasa Irruppu (balance of the birth Maha Dasa in years, months, days)
- Mandi (Maandhi) rising per the Prasna Marga ghatika rule
- Chevvai Dosham from Lagna, Moon and Venus with classical exemptions
- Rahu-Ketu Dosham, Papa Samyam points and Dosha Samyam for matching
- Daily Tamil Panchangam: anga end times, Hora, Soolam, Chandrashtamam, Tara/Chandra Balam
- Personal almanac: upcoming Chandrashtamam periods and the Nakshatra birthday
- Monthly Tamil calendar with observance days, rules matched to Drik Panchang
"""
import math
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .engine import (
    swe, AYAN, SIGNS, TAMIL, SIGN_LORDS, STARS, TAMIL_STARS, DASHA_NAMES, DASHA_YEARS, TITHIS,
    STAR_GANAS, STAR_YONIS, STAR_RAJJUS, STAR_NADIS, GANA_TA, RAJJU_TA, NADI_TA, YONI_TA,
    placement, local_to_utc, utc_to_jd, jd_to_utc, sun_events, sidereal_position, calculate_panchangam
)
from .predictions import PLANET_TAMIL

NAK_SPAN = 40 / 3

TAMIL_MONTHS = ['Chithirai', 'Vaikasi', 'Aani', 'Aadi', 'Aavani', 'Purattasi',
                'Aippasi', 'Karthigai', 'Margazhi', 'Thai', 'Maasi', 'Panguni']
TAMIL_MONTHS_TA = ['சித்திரை', 'வைகாசி', 'ஆனி', 'ஆடி', 'ஆவணி', 'புரட்டாசி',
                   'ஐப்பசி', 'கார்த்திகை', 'மார்கழி', 'தை', 'மாசி', 'பங்குனி']

# 60-year cycle, starting from Prabhava (Tamil year beginning April 1987)
TAMIL_YEARS = [
    ('Prabhava', 'பிரபவ'), ('Vibhava', 'விபவ'), ('Shukla', 'சுக்ல'), ('Pramodhoota', 'பிரமோதூத'),
    ('Prajorpatti', 'பிரஜோற்பத்தி'), ('Angirasa', 'ஆங்கீரச'), ('Srimukha', 'ஸ்ரீமுக'), ('Bhava', 'பவ'),
    ('Yuva', 'யுவ'), ('Dhatu', 'தாது'), ('Eeswara', 'ஈஸ்வர'), ('Vehudhanya', 'வெகுதானிய'),
    ('Pramathi', 'பிரமாதி'), ('Vikrama', 'விக்கிரம'), ('Vishu', 'விஷு'), ('Chitrabhanu', 'சித்திரபானு'),
    ('Subhanu', 'சுபானு'), ('Dharana', 'தாரண'), ('Parthiba', 'பார்த்திப'), ('Viya', 'விய'),
    ('Sarvajith', 'சர்வசித்து'), ('Sarvadhari', 'சர்வதாரி'), ('Virodhi', 'விரோதி'), ('Vikruthi', 'விக்ருதி'),
    ('Kara', 'கர'), ('Nandana', 'நந்தன'), ('Vijaya', 'விஜய'), ('Jaya', 'ஜய'),
    ('Manmatha', 'மன்மத'), ('Dhunmuki', 'துன்முகி'), ('Hevilambi', 'ஹேவிளம்பி'), ('Vilambi', 'விளம்பி'),
    ('Vikari', 'விகாரி'), ('Sarvari', 'சார்வரி'), ('Plava', 'பிலவ'), ('Subhakrith', 'சுபகிருது'),
    ('Sobhakrith', 'சோபகிருது'), ('Krodhi', 'குரோதி'), ('Visuvavasu', 'விசுவாவசு'), ('Parabhava', 'பராபவ'),
    ('Plavanga', 'பிலவங்க'), ('Keelaka', 'கீலக'), ('Saumya', 'சௌமிய'), ('Sadharana', 'சாதாரண'),
    ('Virodhikrithu', 'விரோதகிருது'), ('Paridhabi', 'பரிதாபி'), ('Pramadhicha', 'பிரமாதீச'), ('Ananda', 'ஆனந்த'),
    ('Rakshasa', 'ராட்சச'), ('Nala', 'நள'), ('Pingala', 'பிங்கள'), ('Kalayukthi', 'காளயுக்தி'),
    ('Siddharthi', 'சித்தார்த்தி'), ('Raudhri', 'ரௌத்திரி'), ('Dhunmathi', 'துன்மதி'), ('Dhundubhi', 'துந்துபி'),
    ('Rudhrodhgari', 'ருத்ரோத்காரி'), ('Raktakshi', 'ரக்தாட்சி'), ('Krodhana', 'குரோதன'), ('Akshaya', 'அட்சய')
]
TAMIL_CYCLE_EPOCH = 1987

# Sunday first
VAARAM = [('Sunday', 'ஞாயிற்றுக்கிழமை'), ('Monday', 'திங்கட்கிழமை'), ('Tuesday', 'செவ்வாய்க்கிழமை'),
          ('Wednesday', 'புதன்கிழமை'), ('Thursday', 'வியாழக்கிழமை'), ('Friday', 'வெள்ளிக்கிழமை'),
          ('Saturday', 'சனிக்கிழமை')]
# Soolam: direction to avoid travelling and its Parigaram (remedy), Sunday first
SOOLAM = [
    ('West', 'மேற்கு', 'Jaggery', 'வெல்லம்'), ('East', 'கிழக்கு', 'Curd', 'தயிர்'),
    ('North', 'வடக்கு', 'Milk', 'பால்'), ('North', 'வடக்கு', 'Milk', 'பால்'),
    ('South', 'தெற்கு', 'Sesame oil', 'தைலம்'), ('West', 'மேற்கு', 'Jaggery', 'வெல்லம்'),
    ('East', 'கிழக்கு', 'Curd', 'தயிர்')
]
# Prasna Marga: ghatikas (of a 30-ghatika day or night) after which Mandi rises, Sunday first
MANDI_DAY_GHATI = [26, 22, 18, 14, 10, 6, 2]
MANDI_NIGHT_GHATI = [10, 6, 2, 26, 22, 18, 14]

TARAS = [
    ('Janma', 'ஜன்ம', 'mixed'), ('Sampat', 'சம்பத்', 'good'), ('Vipat', 'விபத்', 'bad'),
    ('Kshema', 'க்ஷேம', 'good'), ('Pratyak', 'பிரத்யக்', 'bad'), ('Sadhana', 'சாதக', 'good'),
    ('Naidhana', 'நைதன', 'bad'), ('Mitra', 'மித்ர', 'good'), ('Parama Mitra', 'பரம மித்ர', 'good')
]
CHANDRA_BALAM_HOUSES = (1, 3, 6, 7, 10, 11)
# Amirthathi (Tamil) yogam by weekday (Sunday first) and nakshatra (Ashwini first), as printed in
# Tamil calendars: S Siddha, A Amirtha, M Marana, P Prabalarishta. Cross-checked with PyJHora's table;
# Monday + Purattathi is Marana as in the Sringeri Tamil Panchangam.
TAMIL_YOGAM_TABLE = (
    'SPSSSSSSSMSASSSMMMASAAMSSAA',
    'SSMASSASSMSSSPAMSSSMMASSMSS',
    'SSSASMSSSSSASSSMSMASPSSMMAS',
    'MSASSSSSSSAAMSSSSSMAASPSASM',
    'ASMMMMASSASMSSASSPSSSSSMSSS',
    'ASSMSSSMMMSSASSSSMAPSMSSSSS',
    'SSSASSSSMASMMMSSSSSSSSSAMSP',
)
TAMIL_YOGAMS = {
    'S': ('siddha', 'Siddha Yogam', 'சித்த யோகம்', True),
    'A': ('amirtha', 'Amirtha Yogam', 'அமிர்த யோகம்', True),
    'M': ('marana', 'Marana Yogam', 'மரண யோகம்', False),
    'P': ('prabalarishta', 'Prabalarishta Yogam', 'பிரபலாரிஷ்ட யோகம்', False),
}


def tamil_yogam(weekday, star):
    """Amirthathi yogam for a weekday (0 = Sunday) and nakshatra index (0 = Ashwini)."""
    key, en, ta, good = TAMIL_YOGAMS[TAMIL_YOGAM_TABLE[weekday % 7][star % 27]]
    return dict(key=key, en=en, ta=ta, good=good)

# Hora lords run in descending Chaldean order; a day's first hora belongs to its weekday lord.
HORA_SEQUENCE = ['Sun', 'Venus', 'Mercury', 'Moon', 'Saturn', 'Jupiter', 'Mars']
WEEKDAY_LORDS = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']  # Sunday first
SUBHA_HORAS = ('Moon', 'Mercury', 'Jupiter', 'Venus')

# Gowri Panchangam (Nalla Neram): eight equal parts of the day and of the night, Sunday first.
# Tables as published by Drik Panchang (from the Pambu Panchangam), including the repeated
# Soram in Saturday's night.
GOWRI_DAY = [
    ['Uthi', 'Amirdha', 'Rogam', 'Laabam', 'Dhanam', 'Sugam', 'Soram', 'Visham'],
    ['Amirdha', 'Visham', 'Rogam', 'Laabam', 'Dhanam', 'Sugam', 'Soram', 'Uthi'],
    ['Rogam', 'Laabam', 'Dhanam', 'Sugam', 'Soram', 'Uthi', 'Visham', 'Amirdha'],
    ['Laabam', 'Dhanam', 'Sugam', 'Soram', 'Visham', 'Uthi', 'Amirdha', 'Rogam'],
    ['Dhanam', 'Sugam', 'Soram', 'Uthi', 'Amirdha', 'Visham', 'Rogam', 'Laabam'],
    ['Sugam', 'Soram', 'Uthi', 'Visham', 'Amirdha', 'Rogam', 'Laabam', 'Dhanam'],
    ['Soram', 'Uthi', 'Visham', 'Amirdha', 'Rogam', 'Laabam', 'Dhanam', 'Sugam']
]
GOWRI_NIGHT = [
    ['Dhanam', 'Sugam', 'Soram', 'Visham', 'Uthi', 'Amirdha', 'Rogam', 'Laabam'],
    ['Sugam', 'Soram', 'Uthi', 'Amirdha', 'Visham', 'Rogam', 'Laabam', 'Dhanam'],
    ['Soram', 'Uthi', 'Visham', 'Amirdha', 'Rogam', 'Laabam', 'Dhanam', 'Sugam'],
    ['Uthi', 'Amirdha', 'Rogam', 'Laabam', 'Dhanam', 'Sugam', 'Soram', 'Visham'],
    ['Amirdha', 'Visham', 'Rogam', 'Laabam', 'Dhanam', 'Sugam', 'Soram', 'Uthi'],
    ['Rogam', 'Laabam', 'Dhanam', 'Sugam', 'Soram', 'Uthi', 'Visham', 'Amirdha'],
    ['Laabam', 'Dhanam', 'Sugam', 'Soram', 'Uthi', 'Visham', 'Amirdha', 'Soram']
]
GOWRI_TA = {
    'Amirdha': 'அமிர்தம்', 'Uthi': 'உத்தி', 'Laabam': 'லாபம்', 'Dhanam': 'தனம்', 'Sugam': 'சுகம்',
    'Rogam': 'ரோகம்', 'Soram': 'சோரம்', 'Visham': 'விஷம்'
}
GOWRI_GOOD = ('Amirdha', 'Uthi', 'Laabam', 'Dhanam', 'Sugam')

# Upagrahas. The day and the night are each split into eight parts ruled in weekday order
# from the day's lord (the night from the fifth lord), one part being unruled. Kaala, Mrityu,
# Artha Praharaka and Yama Ghantaka rise at the middle of their lord's part and Gulika at the
# start of Saturn's (Jagannatha Hora's convention); Mandi keeps the Prasna Marga rule above.
PART_CYCLE = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', None]
TIME_UPAGRAHAS = [
    ('Kaala', 'காலன்', 'Sun', 0.5), ('Mrityu', 'மிருத்யு', 'Mars', 0.5),
    ('Artha Praharaka', 'அர்த்தப்பிரகரன்', 'Mercury', 0.5), ('Yama Ghantaka', 'எமகண்டன்', 'Jupiter', 0.5),
    ('Gulika', 'குளிகன்', 'Saturn', 0.0)
]
# Sun-based upagrahas (BPHS): Dhuma = Sun + 133°20', then each derived from the previous
SOLAR_UPAGRAHAS = [('Dhuma', 'தூமம்'), ('Vyatipata', 'வியதீபாதம்'), ('Parivesha', 'பரிவேடம்'),
                   ('Indrachapa', 'இந்திரசாபம்'), ('Upaketu', 'உபகேது')]

# Monthly observances. Each rule reproduces Drik Panchang's published dates for Chennai
# across 2025 and 2026 (see tests/test_tamil_calendar.py).
OBSERVANCES = {
    'amavasai': ('Amavasai', 'அமாவாசை'), 'pournami': ('Pournami', 'பௌர்ணமி'),
    'ekadasi': ('Ekadasi', 'ஏகாதசி'), 'pradosham': ('Pradosham', 'பிரதோஷம்'),
    'sashti': ('Sashti', 'சஷ்டி'), 'sankatahara': ('Sankatahara Chaturthi', 'சங்கடஹர சதுர்த்தி'),
    'shivaratri': ('Masa Shivaratri', 'மாத சிவராத்திரி'), 'karthigai': ('Karthigai', 'கார்த்திகை'),
    'month_start': ('Tamil month begins', 'மாதப் பிறப்பு')
}
TITHI_TA = ['பிரதமை', 'துவிதியை', 'திருதியை', 'சதுர்த்தி', 'பஞ்சமி', 'சஷ்டி', 'சப்தமி', 'அஷ்டமி',
            'நவமி', 'தசமி', 'ஏகாதசி', 'துவாதசி', 'திரயோதசி', 'சதுர்த்தசி']

# Mean daily motions (degrees) used to seed the Newton searches
SUN_RATE, MOON_RATE = 0.9856, 13.176

DOSHA_REFERENCES = [('Ascendant', 'Lagna', 'லக்னம்'), ('Moon', 'Chandra', 'சந்திரன்'), ('Venus', 'Sukra', 'சுக்கிரன்')]
CHEVVAI_HOUSES = (2, 4, 7, 8, 12)
# Mars in these signs does not afflict from the given house (classical Tamil exemptions)
CHEVVAI_SIGN_EXEMPTIONS = {2: (2, 5), 4: (0, 7), 7: (3, 9), 8: (8, 11), 12: (1, 6)}
RAHU_KETU_HOUSES = (1, 2, 7, 8)
PAPA_GRAHAS = ('Sun', 'Mars', 'Saturn', 'Rahu', 'Ketu')
PAPA_HOUSES = (1, 2, 4, 7, 8, 12)


def _zone(tz_name):
    try:
        return ZoneInfo(tz_name)
    except ZoneInfoNotFoundError:
        raise ValueError('Enter a valid IANA timezone, such as Asia/Kolkata.')


def _local_iso(jd, tz):
    return jd_to_utc(jd).astimezone(tz).isoformat(timespec='seconds')


def _house_from(sign_idx, ref_sign_idx):
    return (sign_idx - ref_sign_idx) % 12 + 1


def _sun(jd):
    return sidereal_position(jd, swe.SUN)


def _moon(jd):
    return sidereal_position(jd, swe.MOON)


def _elongation(jd):
    (s, ss), (m, ms) = _sun(jd), _moon(jd)
    return (m - s) % 360, ms - ss


def _yoga_sum(jd):
    (s, ss), (m, ms) = _sun(jd), _moon(jd)
    return (m + s) % 360, ms + ss


def _solve_crossing(jd, value_fn, target):
    """Newton-solve for the moment nearest jd when value_fn (degrees) equals target."""
    t = jd
    for _ in range(50):
        value, rate = value_fn(t)
        diff = (target - value + 180) % 360 - 180
        if abs(diff) < 1e-7:
            break
        t += diff / rate
    return t


def _next_entry(jd, value_fn, target, rate):
    """First moment after jd when a longitude advancing at about rate deg/day reaches target."""
    guess = jd + ((target - value_fn(jd)[0]) % 360) / rate
    return _solve_crossing(guess, value_fn, target)


def _next_boundary(jd, value_fn, span):
    """Moment after jd when value_fn next crosses a multiple of span (an anga ends)."""
    value, _ = value_fn(jd)
    target = ((math.floor(value / span) + 1) * span) % 360
    return _solve_crossing(jd, value_fn, target)


def vedic_day(moment_jd, tz, lat, lon):
    """The Vedic day (sunrise to sunrise) containing a moment, with its sun events."""
    civil = jd_to_utc(moment_jd).astimezone(tz).date()
    events = sun_events(civil, tz, lat, lon)
    if moment_jd < events['sunrise']:
        civil -= timedelta(days=1)
        events = sun_events(civil, tz, lat, lon)
    return civil, events


def _month_first_day(ingress, tz, lat, lon):
    """A Tamil month begins on the day the Sun enters the sign if the sankranti
    falls before sunset, otherwise on the following day."""
    ingress_day = jd_to_utc(ingress).astimezone(tz).date()
    if ingress >= sun_events(ingress_day, tz, lat, lon)['sunset']:
        return ingress_day + timedelta(days=1)
    return ingress_day


def tamil_calendar(day, tz, lat, lon):
    """Tamil solar date for a day, by the sunset rule for the month's first day."""
    sunset = sun_events(day, tz, lat, lon)['sunset']
    month = int(_sun(sunset)[0] // 30)
    ingress = _solve_crossing(sunset, _sun, month * 30.0)
    first_day = _month_first_day(ingress, tz, lat, lon)
    # Margazhi (in January) through Panguni belong to the year that began the previous April
    start_year = day.year - 1 if month >= 8 and day.month <= 4 else day.year
    year_idx = (start_year - TAMIL_CYCLE_EPOCH) % 60
    return dict(
        year_number=year_idx + 1,
        year=TAMIL_YEARS[year_idx][0],
        year_ta=TAMIL_YEARS[year_idx][1],
        month_index=month,
        month=TAMIL_MONTHS[month],
        month_ta=TAMIL_MONTHS_TA[month],
        day=(day - first_day).days + 1,
        month_start=first_day.isoformat(),
        sankranti_local=_local_iso(ingress, tz)
    )


def udayadi_nazhigai(moment_jd, events):
    """Time elapsed since sunrise in nazhigai (24 min) and vinadi (24 s)."""
    ghati = (moment_jd - events['sunrise']) * 60
    nazhigai = int(ghati)
    return dict(
        nazhigai=nazhigai,
        vinadi=int((ghati - nazhigai) * 60),
        ghati=round(ghati, 4),
        dinamanam=round((events['sunset'] - events['sunrise']) * 60, 2),
        is_day_birth=moment_jd < events['sunset']
    )


def dasa_irruppu(moon_lon):
    """Balance of the Vimshottari Maha Dasa running at birth, in the traditional
    years / months (of 12) / days (of 30) notation."""
    portion = moon_lon / NAK_SPAN
    idx = int(portion) % 9
    balance = (1 - portion % 1) * DASHA_YEARS[idx]
    years = int(balance)
    months_f = (balance - years) * 12
    months = int(months_f)
    return dict(
        lord=DASHA_NAMES[idx],
        lord_ta=PLANET_TAMIL[DASHA_NAMES[idx]],
        years=years,
        months=months,
        days=int((months_f - months) * 30),
        balance_years=round(balance, 6)
    )


def mandi_longitude(moment_jd, events, weekday, lat, lon):
    """Mandi is the ascendant at the moment it rises: a fixed number of ghatikas
    into the day or night (Prasna Marga), scaled to the actual day or night length."""
    if moment_jd < events['sunset']:
        start, span, ghati = events['sunrise'], events['sunset'] - events['sunrise'], MANDI_DAY_GHATI[weekday]
    else:
        start, span, ghati = events['sunset'], events['next_sunrise'] - events['sunset'], MANDI_NIGHT_GHATI[weekday]
    rise_jd = start + span * ghati / 30
    asc = swe.houses_ex(rise_jd, lat, lon, b'P', swe.FLG_SIDEREAL)[1][0]
    return asc, rise_jd


def solar_upagraha_longitudes(sun_lon):
    dhuma = (sun_lon + 133 + 20 / 60) % 360
    vyatipata = (360 - dhuma) % 360
    parivesha = (vyatipata + 180) % 360
    indrachapa = (360 - parivesha) % 360
    return [dhuma, vyatipata, parivesha, indrachapa, (sun_lon - 30) % 360]


def upagrahas(moment_jd, events, weekday, lat, lon, planets):
    """Time-based upagrahas (the ascendant when each rises) and the Sun-based Dhuma group."""
    if moment_jd < events['sunset']:
        start, span, lord = events['sunrise'], events['sunset'] - events['sunrise'], WEEKDAY_LORDS[weekday]
    else:
        start, span, lord = events['sunset'], events['next_sunrise'] - events['sunset'], WEEKDAY_LORDS[(weekday + 4) % 7]
    part = span / 8
    asc_sign = planets['Ascendant']['sign_index']
    rows = []

    def add(name, name_ta, lon_value, kind):
        pl = placement(lon_value)
        rows.append(dict(name=name, name_ta=name_ta, kind=kind, longitude=lon_value,
                         sign=pl['sign'], tamil=pl['tamil'], sign_index=pl['sign_index'], degree=pl['degree'],
                         nakshatra=pl['nakshatra'], tamil_nakshatra=pl['tamil_nakshatra'], pada=pl['pada'],
                         house=_house_from(pl['sign_index'], asc_sign)))

    for name, name_ta, ruler, offset in TIME_UPAGRAHAS:
        index = (PART_CYCLE.index(ruler) - PART_CYCLE.index(lord)) % 8
        rise = start + (index + offset) * part
        add(name, name_ta, swe.houses_ex(rise, lat, lon, b'P', swe.FLG_SIDEREAL)[1][0], 'time')
    for (name, name_ta), lon_value in zip(SOLAR_UPAGRAHAS, solar_upagraha_longitudes(planets['Sun']['longitude'])):
        add(name, name_ta, lon_value, 'solar')
    return rows


def chevvai_dosham(planets):
    """Chevvai (Kuja) Dosham per Tamil tradition: Mars in 2, 4, 7, 8 or 12 from
    Lagna, Moon or Venus, less the sign exemptions and classical cancellations."""
    mars = planets['Mars']
    mars_sign = mars['sign_index']
    references = []
    for key, name, name_ta in DOSHA_REFERENCES:
        house = _house_from(mars_sign, planets[key]['sign_index'])
        exempt = house in CHEVVAI_HOUSES and mars_sign in CHEVVAI_SIGN_EXEMPTIONS[house]
        references.append(dict(
            reference=name, reference_ta=name_ta, house=house,
            afflicting=house in CHEVVAI_HOUSES and not exempt,
            exempt=exempt
        ))
    present = any(r['afflicting'] for r in references)

    cancellations = []
    if present:
        if mars_sign in (4, 10):
            cancellations.append(dict(en='Mars in Leo or Aquarius does not cause Chevvai Dosham',
                                      ta='சிம்மம் அல்லது கும்பத்தில் உள்ள செவ்வாய்க்கு தோஷம் இல்லை'))
        if mars.get('dignity') in ('Own Sign', 'Exalted', 'Moolatrikona'):
            cancellations.append(dict(en=f'Mars is strong in its {mars["dignity"].lower()} ({SIGNS[mars_sign]})',
                                      ta=f'செவ்வாய் ஆட்சி / உச்சம் பெற்றுள்ளது ({TAMIL[mars_sign]})'))
        if _house_from(mars_sign, planets['Jupiter']['sign_index']) in (1, 5, 7, 9):
            cancellations.append(dict(en='Jupiter conjoins or aspects Mars',
                                      ta='குருவின் சேர்க்கை அல்லது பார்வை செவ்வாய்க்கு உள்ளது'))
        if planets['Ascendant']['sign_index'] in (3, 4):
            cancellations.append(dict(en='Mars is Yogakaraka for Cancer and Leo Lagna',
                                      ta='கடக, சிம்ம லக்னத்திற்கு செவ்வாய் யோககாரகன்'))
    cancelled = bool(cancellations)
    return dict(
        present=present,
        cancelled=cancelled,
        effective=present and not cancelled,
        severity=sum(r['afflicting'] for r in references),
        mars_sign=SIGNS[mars_sign],
        mars_sign_ta=TAMIL[mars_sign],
        references=references,
        cancellations=cancellations,
        rule='Mars in houses 2, 4, 7, 8 or 12 from Lagna, Moon or Venus'
    )


def rahu_ketu_dosham(planets):
    """Rahu-Ketu (Sarpa) Dosham for marriage: a node in houses 1, 2, 7 or 8 from Lagna or Moon."""
    references = []
    for key, name, name_ta in DOSHA_REFERENCES[:2]:
        ref = planets[key]['sign_index']
        rahu_house = _house_from(planets['Rahu']['sign_index'], ref)
        ketu_house = _house_from(planets['Ketu']['sign_index'], ref)
        references.append(dict(
            reference=name, reference_ta=name_ta,
            rahu_house=rahu_house, ketu_house=ketu_house,
            afflicting=rahu_house in RAHU_KETU_HOUSES or ketu_house in RAHU_KETU_HOUSES
        ))
    return dict(
        present=any(r['afflicting'] for r in references),
        from_lagna=references[0]['afflicting'],
        references=references,
        rule='Rahu or Ketu in houses 1, 2, 7 or 8 from Lagna or Moon'
    )


def papa_points(planets):
    """Papa (malefic) points for Papa Samyam: one point for each of Sun, Mars,
    Saturn, Rahu and Ketu in houses 1, 2, 4, 7, 8 or 12 from Lagna, Moon and Venus."""
    breakdown = []
    for key, name, name_ta in DOSHA_REFERENCES:
        ref = planets[key]['sign_index']
        hits = []
        for p in PAPA_GRAHAS:
            house = _house_from(planets[p]['sign_index'], ref)
            if house in PAPA_HOUSES:
                hits.append(dict(planet=p, planet_ta=PLANET_TAMIL[p], house=house))
        breakdown.append(dict(reference=name, reference_ta=name_ta, planets=hits, points=len(hits)))
    return dict(total=sum(b['points'] for b in breakdown), breakdown=breakdown)


DASA_SANDHI_DAYS = 182      # changes this close together form a Dasa Sandhi
DASA_SANDHI_HORIZON = 30    # years ahead that are checked


def dasa_sandhi(boy_dasha, girl_dasha, now=None):
    """Dasa Sandhi: the bride's and groom's Maha Dasas changing within about six months
    of each other in the coming years, traditionally a strain on the marriage."""
    now = now or datetime.now(timezone.utc)
    horizon = now + timedelta(days=DASA_SANDHI_HORIZON * 365.25)

    def changes(rows):
        out = []
        for current, following in zip(rows, rows[1:]):
            when = datetime.fromisoformat(current['end'])
            if now < when < horizon:
                out.append((when, current['lord'], following['lord']))
        return out

    conflicts = []
    for b_when, b_from, b_to in changes(boy_dasha):
        for g_when, g_from, g_to in changes(girl_dasha):
            gap = abs((b_when - g_when).days)
            if gap <= DASA_SANDHI_DAYS:
                conflicts.append(dict(
                    groom_date=b_when.isoformat(timespec='seconds'), groom_from=b_from, groom_to=b_to,
                    bride_date=g_when.isoformat(timespec='seconds'), bride_from=g_from, bride_to=g_to,
                    gap_days=gap
                ))
    return dict(present=bool(conflicts), window_days=DASA_SANDHI_DAYS,
                horizon_years=DASA_SANDHI_HORIZON, conflicts=conflicts)


def compare_dosha_samyam(boy_planets, girl_planets, boy_dasha=None, girl_dasha=None):
    """Dosha Samyam: Chevvai Dosham should be present in both or neither chart,
    and the bride's Papa points should not exceed the groom's. Dasa Sandhi is
    reported alongside when both Dasa tables are given."""
    boy = dict(chevvai=chevvai_dosham(boy_planets), rahu_ketu=rahu_ketu_dosham(boy_planets),
               papa=papa_points(boy_planets))
    girl = dict(chevvai=chevvai_dosham(girl_planets), rahu_ketu=rahu_ketu_dosham(girl_planets),
                papa=papa_points(girl_planets))
    chevvai_balanced = boy['chevvai']['effective'] == girl['chevvai']['effective']
    papa_balanced = boy['papa']['total'] >= girl['papa']['total']
    return dict(
        boy=boy,
        girl=girl,
        chevvai_balanced=chevvai_balanced,
        papa_balanced=papa_balanced,
        balanced=chevvai_balanced and papa_balanced,
        dasa_sandhi=dasa_sandhi(boy_dasha, girl_dasha) if boy_dasha and girl_dasha else None
    )


def birth_star_attributes(star_idx):
    gana, rajju, nadi = STAR_GANAS[star_idx], STAR_RAJJUS[star_idx], STAR_NADIS[star_idx]
    yoni = STAR_YONIS[star_idx][0]
    return dict(
        gana=gana, gana_ta=GANA_TA[gana],
        yoni=yoni, yoni_ta=YONI_TA[yoni],
        rajju=rajju, rajju_ta=RAJJU_TA[rajju],
        nadi=nadi, nadi_ta=NADI_TA[nadi]
    )


def hora_table(events, weekday, tz, moment_jd=None):
    """24 horas from sunrise: twelve equal parts of the day, then twelve of the night."""
    first = HORA_SEQUENCE.index(WEEKDAY_LORDS[weekday])
    day_hora = (events['sunset'] - events['sunrise']) / 12
    night_hora = (events['next_sunrise'] - events['sunset']) / 12
    rows = []
    for i in range(24):
        daytime = i < 12
        start = events['sunrise'] + i * day_hora if daytime else events['sunset'] + (i - 12) * night_hora
        end = start + (day_hora if daytime else night_hora)
        lord = HORA_SEQUENCE[(first + i) % 7]
        rows.append(dict(
            number=i + 1, lord=lord, lord_ta=PLANET_TAMIL[lord], daytime=daytime,
            auspicious=lord in SUBHA_HORAS,
            start_local=_local_iso(start, tz), end_local=_local_iso(end, tz),
            current=moment_jd is not None and start <= moment_jd < end
        ))
    return rows


def gowri_panchangam(events, weekday, tz, moment_jd=None):
    """Gowri Panchangam: the day and the night each split into eight equal parts."""
    rows = []
    for daytime, start, end, table in (
            (True, events['sunrise'], events['sunset'], GOWRI_DAY),
            (False, events['sunset'], events['next_sunrise'], GOWRI_NIGHT)):
        part = (end - start) / 8
        for i, name in enumerate(table[weekday]):
            t0, t1 = start + i * part, start + (i + 1) * part
            rows.append(dict(
                name=name, name_ta=GOWRI_TA[name], good=name in GOWRI_GOOD, daytime=daytime,
                start_local=_local_iso(t0, tz), end_local=_local_iso(t1, tz),
                current=moment_jd is not None and t0 <= moment_jd < t1
            ))
    return rows


def upcoming_chandrashtamam(jd, natal_sign, tz, count=3):
    """The next periods when the Moon transits the 8th sign from the natal Moon."""
    sign = (natal_sign + 7) % 12
    moon_lon = _moon(jd)[0]
    if int(moon_lon // 30) == sign:  # already running: find when it began
        start = _solve_crossing(jd - (moon_lon - sign * 30) / MOON_RATE, _moon, sign * 30.0)
    else:
        start = _next_entry(jd, _moon, sign * 30.0, MOON_RATE)
    periods = []
    for _ in range(count):
        end = _next_entry(start + 0.5, _moon, ((sign + 1) % 12) * 30.0, MOON_RATE)
        periods.append(dict(start_local=_local_iso(start, tz), end_local=_local_iso(end, tz),
                            active=start <= jd < end))
        start = _next_entry(end + 20, _moon, sign * 30.0, MOON_RATE)
    return dict(sign_index=sign, sign=SIGNS[sign], sign_ta=TAMIL[sign], periods=periods)


def next_star_birthday(jd, birth_star, birth_month, tz, lat, lon):
    """Nakshatra birthday: the day(s) in the Tamil birth month on which the birth star
    prevails at sunrise. A star that begins and ends between two sunrises (kshaya)
    is assigned to the day it begins."""
    today = jd_to_utc(jd).astimezone(tz).date()
    search_from = jd - 32  # also catches a birth month that is already running
    for _ in range(2):
        ingress = _next_entry(search_from, _sun, birth_month * 30.0, SUN_RATE)
        first = _month_first_day(ingress, tz, lat, lon)
        following = _next_entry(ingress + 20, _sun, ((birth_month + 1) % 12) * 30.0, SUN_RATE)
        last = _month_first_day(following, tz, lat, lon) - timedelta(days=1)

        span = [first + timedelta(days=i) for i in range((last - first).days + 2)]
        star_at_sunrise = {d: int(_moon(sun_events(d, tz, lat, lon)['sunrise'])[0] / NAK_SPAN) for d in span}
        month_days = span[:-1]
        matches = [d for d in month_days if star_at_sunrise[d] == birth_star]
        if not matches:
            matches = [d for d in month_days
                       if star_at_sunrise[d] == (birth_star - 1) % 27
                       and star_at_sunrise[d + timedelta(days=1)] == (birth_star + 1) % 27]
        upcoming = [d for d in matches if d >= today]
        if upcoming:
            return dict(dates=[d.isoformat() for d in upcoming],
                        month=TAMIL_MONTHS[birth_month], month_ta=TAMIL_MONTHS_TA[birth_month],
                        star=STARS[birth_star], star_ta=TAMIL_STARS[birth_star])
        search_from = ingress + 300
    return None


# Dagdha (burnt) rasis of the birth tithi, by its number within the paksha (Muhurta Chintamani);
# Pournami and Amavasai have none
DAGDHA_RASIS = {1: (6, 9), 2: (8, 11), 3: (4, 9), 4: (1, 10), 5: (2, 5), 6: (0, 4), 7: (3, 8), 8: (2, 5),
                9: (4, 7), 10: (4, 7), 11: (8, 11), 12: (6, 9), 13: (1, 4), 14: (2, 5, 8, 11)}
COMBUSTION_ORBS = {'Moon': 12, 'Mars': 17, 'Mercury': 14, 'Jupiter': 11, 'Venus': 10, 'Saturn': 15}


def birth_extras(planets):
    """Birth-chart notes Tamil and Kerala horoscopes print: Yogi, Duplicate Yogi and Avayogi,
    Dagdha Rasis, Chandra Avastha / Vela / Kriya and Moudhyam (combust grahas)."""
    sun, moon = planets['Sun']['longitude'], planets['Moon']['longitude']
    lords = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']

    def point(lon):
        star = int(lon / NAK_SPAN) % 27
        lord = lords[star % 9]
        sign = int(lon // 30) % 12
        return dict(longitude=round(lon, 4), sign=SIGNS[sign], tamil=TAMIL[sign], star=STARS[star], star_ta=TAMIL_STARS[star],
                    planet=lord, planet_ta=PLANET_TAMIL[lord])

    yogi_lon = (sun + moon + 93 + 20 / 60) % 360
    yogi = point(yogi_lon)
    duplicate = SIGN_LORDS[int(yogi_lon // 30)]
    yogi.update(duplicate=duplicate, duplicate_ta=PLANET_TAMIL[duplicate])
    avayogi = point((yogi_lon + 186 + 40 / 60) % 360)

    tithi = int(((moon - sun) % 360) // 12) + 1
    in_paksha = (tithi - 1) % 15 + 1
    dagdha = [dict(en=SIGNS[s], ta=TAMIL[s]) for s in DAGDHA_RASIS.get(in_paksha, ())]

    # Chandra Avastha, Vela and Kriya: the Moon's progress through its nakshatra in 12, 36 and 60 parts
    progress = (moon % NAK_SPAN) / NAK_SPAN
    chandra = dict(avastha=int(progress * 12) + 1, vela=int(progress * 36) + 1, kriya=int(progress * 60) + 1)

    moudhyam = []
    for name, orb in COMBUSTION_ORBS.items():
        gap = abs((planets[name]['longitude'] - sun + 180) % 360 - 180)
        if gap <= orb - (2 if name in ('Mercury', 'Venus') and planets[name].get('retrograde') else 0):
            moudhyam.append(dict(planet=name, planet_ta=PLANET_TAMIL[name], distance=round(gap, 2)))
    return dict(yogi=yogi, avayogi=avayogi, dagdha_rasis=dagdha, chandra=chandra, moudhyam=moudhyam)


def build_south_indian_details(planets, utc, tz_name, lat, lon, now=None):
    """Tamil Jathaga Kurippu (birth notes) and the person's upcoming almanac dates.
    Uses the ayanamsa mode already set by the engine."""
    tz = _zone(tz_name)
    jd = utc_to_jd(utc)
    day, events = vedic_day(jd, tz, lat, lon)
    weekday = (day.weekday() + 1) % 7  # Sunday = 0

    mandi_lon, mandi_jd = mandi_longitude(jd, events, weekday, lat, lon)
    mandi = placement(mandi_lon)
    mandi['house'] = _house_from(mandi['sign_index'], planets['Ascendant']['sign_index'])
    mandi['rises_local'] = _local_iso(mandi_jd, tz)

    moon = planets['Moon']
    birth_star = int(moon['longitude'] / NAK_SPAN)
    birth_calendar = tamil_calendar(day, tz, lat, lon)
    now_jd = utc_to_jd(now or datetime.now(timezone.utc))
    return dict(
        vedic_date=day.isoformat(),
        vaaram=dict(index=weekday, en=VAARAM[weekday][0], ta=VAARAM[weekday][1]),
        tamil_calendar=birth_calendar,
        sunrise_local=_local_iso(events['sunrise'], tz),
        sunset_local=_local_iso(events['sunset'], tz),
        nazhigai=udayadi_nazhigai(jd, events),
        dasa_irruppu=dasa_irruppu(moon['longitude']),
        birth_star=birth_star_attributes(birth_star),
        mandi=mandi,
        upagrahas=upagrahas(jd, events, weekday, lat, lon, planets),
        papa_points=papa_points(planets),
        extras=birth_extras(planets),
        upcoming=dict(
            chandrashtamam=upcoming_chandrashtamam(now_jd, moon['sign_index'], tz),
            star_birthday=next_star_birthday(now_jd, birth_star, birth_calendar['month_index'], tz, lat, lon)
        )
    )


def _stars_in_sign(sign_idx):
    first = int(sign_idx * 30 / NAK_SPAN)
    last = int((sign_idx * 30 + 29.9999) / NAK_SPAN)
    return [dict(en=STARS[i], ta=TAMIL_STARS[i]) for i in range(first, last + 1)]


def _tithi_at(jd):
    return int(_elongation(jd)[0] // 12) + 1


def _star_at(jd):
    return int(_moon(jd)[0] / NAK_SPAN)


def _moonrise(day, tz, lat, lon):
    midnight = utc_to_jd(datetime(day.year, day.month, day.day, tzinfo=tz).astimezone(timezone.utc))
    res, tret = swe.rise_trans(midnight, swe.MOON, swe.CALC_RISE, (lon, lat, 0), 0, 0, swe.FLG_MOSEPH)
    return tret[0] if res == 0 and tret[0] < midnight + 1 else None


def _observances(d, ev, tithi_at, moonrise):
    """Observance keys falling on day d; ev maps days (d-1 .. d+2) to sun events."""
    prev, nxt, nxt2 = d - timedelta(days=1), d + timedelta(days=1), d + timedelta(days=2)
    sr = lambda x: ev[x]['sunrise']
    ss = lambda x: ev[x]['sunset']
    at = lambda x, f: sr(x) + f * (ss(x) - sr(x))
    found = []

    # Amavasai: the new moon prevailing at mid-afternoon (Aparahna)
    if tithi_at(at(d, 0.7)) == 30:
        found.append('amavasai')
    # Pournami: the full moon at the close of Madhyahna, the first such day; else at sunrise
    if tithi_at(at(prev, 0.6)) != 15 and (tithi_at(at(d, 0.6)) == 15 or tithi_at(sr(d)) == 15):
        found.append('pournami')

    # Ekadasi (Smarta): Ekadasi at sunrise, with the Dwadashi needed for next morning's
    # parana, the arunodaya test when it spans two sunrises, and the kshaya case
    ek = lambda t: tithi_at(t) in (11, 26)
    dw = lambda t: tithi_at(t) in (12, 27)
    aruna = lambda x: sr(x) - 96 / 1440
    if ek(sr(d)):
        if ek(sr(prev)):
            ekadasi = not ek(aruna(prev))
        elif ek(sr(nxt)):
            ekadasi = ek(aruna(d))
        else:
            ekadasi = dw(sr(nxt))
    else:
        ekadasi = ek(ss(d)) and (not ek(sr(nxt)) or (not ek(sr(nxt2)) and not dw(sr(nxt2))))
    if ekadasi:
        found.append('ekadasi')

    # Pradosham: the day whose Pradosha (first fifth of the night) holds Trayodashi longest
    def pradosha(x):
        t0 = ss(x)
        span = (ev[x]['next_sunrise'] - t0) / 5
        return sum(tithi_at(t0 + span * (i + 0.5) / 12) in (13, 28) for i in range(12))
    here = pradosha(d)
    if here and here >= pradosha(prev) and here > pradosha(nxt):
        found.append('pradosham')

    # Skanda Sashti: Shukla Shashti beginning in daytime, else Shashti at sunrise
    starts_by_day = lambda x: tithi_at(sr(x)) != 6 and tithi_at(ss(x)) == 6
    if starts_by_day(d) or (tithi_at(sr(d)) == 6 and not starts_by_day(prev)):
        found.append('sashti')
    # Sankatahara Chaturthi: Krishna Chaturthi at moonrise
    rise = moonrise(d)
    if rise is not None and tithi_at(rise) == 19:
        found.append('sankatahara')
    # Masa Shivaratri: Krishna Chaturdashi at Nishita, the 8th of 15 night muhurtas
    if tithi_at(ss(d) + 7.5 * (ev[d]['next_sunrise'] - ss(d)) / 15) == 29:
        found.append('shivaratri')
    # Karthigai: Krittika at sunset; if it touches no sunset, the day it holds at sunrise
    if _star_at(ss(d)) == 2 or (_star_at(sr(d)) == 2 and _star_at(ss(d)) != 2 and _star_at(ss(prev)) != 2):
        found.append('karthigai')
    return found


def month_calendar(year, month, tz_name, lat, lon, ayanamsa='Lahiri'):
    """A Tamil panchangam month: each day's Tamil date, tithi and star at sunrise, and observances."""
    if not math.isfinite(lat) or not -66 <= lat <= 66:
        raise ValueError('Latitude must be between 66° south and 66° north in this version.')
    if not math.isfinite(lon) or not -180 <= lon <= 180:
        raise ValueError('Longitude must be between -180 and 180.')
    if not 1800 <= year <= 2200 or not 1 <= month <= 12:
        raise ValueError('Choose a date between 1800 and 2200.')
    tz = _zone(tz_name)
    swe.set_sid_mode(AYAN[ayanamsa])
    first = date(year, month, 1)
    last = (first + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    ev = {}
    day = first - timedelta(days=1)
    while day <= last + timedelta(days=2):
        ev[day] = sun_events(day, tz, lat, lon)
        day += timedelta(days=1)

    cal = tamil_calendar(first, tz, lat, lon)
    tamil_month, tamil_day, year_idx = cal['month_index'], cal['day'] - 1, cal['year_number'] - 1
    days = []
    day = first
    while day <= last:
        month_now = int(_sun(ev[day]['sunset'])[0] // 30)  # the sunset rule, day by day
        if month_now != tamil_month:
            tamil_month, tamil_day = month_now, 0
            if month_now == 0:
                year_idx = (year_idx + 1) % 60
        tamil_day += 1
        sunrise = ev[day]['sunrise']
        tithi = _tithi_at(sunrise)
        star = _star_at(sunrise)
        keys = _observances(day, ev, _tithi_at, lambda x: _moonrise(x, tz, lat, lon))
        if tamil_day == 1:
            keys.insert(0, 'month_start')
        weekday = (day.weekday() + 1) % 7
        days.append(dict(
            date=day.isoformat(),
            weekday=VAARAM[weekday][0], weekday_ta=VAARAM[weekday][1],
            tamil_month=TAMIL_MONTHS[tamil_month], tamil_month_ta=TAMIL_MONTHS_TA[tamil_month], tamil_day=tamil_day,
            tamil_year=TAMIL_YEARS[year_idx][0], tamil_year_ta=TAMIL_YEARS[year_idx][1],
            tithi=tithi, tithi_name=TITHIS[tithi - 1], tithi_ta=TITHI_TA[(tithi - 1) % 15] if tithi not in (15, 30) else ('பௌர்ணமி' if tithi == 15 else 'அமாவாசை'),
            paksha='Shukla' if tithi <= 15 else 'Krishna',
            nakshatra=STARS[star], nakshatra_ta=TAMIL_STARS[star],
            sunrise_local=_local_iso(sunrise, tz)[11:16], sunset_local=_local_iso(ev[day]['sunset'], tz)[11:16],
            observances=[dict(key=k, en=OBSERVANCES[k][0], ta=OBSERVANCES[k][1]) for k in keys]
        ))
        day += timedelta(days=1)
    return dict(year=year, month=month, timezone=tz_name, days=days)


def daily_panchangam(date_str, time_str, tz_name, lat, lon, natal_star=None, natal_sign=None, ayanamsa='Lahiri'):
    """Tamil daily panchangam for a local date and time, with anga end times,
    Tamil date, Soolam, Chandrashtamam and optional personal Tara / Chandra Balam.
    Without a time, the angas are those prevailing at sunrise, as almanacs list them."""
    if not math.isfinite(lat) or not -66 <= lat <= 66:
        raise ValueError('Latitude must be between 66° south and 66° north in this version.')
    if not math.isfinite(lon) or not -180 <= lon <= 180:
        raise ValueError('Longitude must be between -180 and 180.')
    tz = _zone(tz_name)
    if time_str:
        utc = local_to_utc(date_str, time_str, tz_name, 0)
    else:
        civil = local_to_utc(date_str, '12:00', tz_name, 0).astimezone(tz).date()
        utc = jd_to_utc(sun_events(civil, tz, lat, lon)['sunrise'] + 1 / 1440)
    jd = utc_to_jd(utc)
    swe.set_sid_mode(AYAN[ayanamsa])
    sun_lon, _ = _sun(jd)
    moon_lon, _ = _moon(jd)

    panch = calculate_panchangam(utc, lat, lon, sun_lon, moon_lon, tz_name)
    civil = utc.astimezone(tz).date()
    weekday = (civil.weekday() + 1) % 7
    moon_sign = int(moon_lon // 30)
    star_idx = int(moon_lon / NAK_SPAN)

    panch['ends_local'] = dict(
        tithi=_local_iso(_next_boundary(jd, _elongation, 12), tz),
        nakshatra=_local_iso(_next_boundary(jd, _moon, NAK_SPAN), tz),
        yoga=_local_iso(_next_boundary(jd, _yoga_sum, NAK_SPAN), tz),
        karana=_local_iso(_next_boundary(jd, _elongation, 6), tz)
    )
    panch['moment_local'] = utc.astimezone(tz).isoformat(timespec='seconds')
    civil_events = sun_events(civil, tz, lat, lon)
    panch['horas'] = hora_table(civil_events, weekday, tz, jd)
    panch['gowri'] = gowri_panchangam(civil_events, weekday, tz, jd)
    panch['tamil_calendar'] = tamil_calendar(civil, tz, lat, lon)
    panch['vaaram'] = dict(index=weekday, en=VAARAM[weekday][0], ta=VAARAM[weekday][1])
    # The Tamil yogam changes with the nakshatra (and the weekday at sunrise)
    star_end = _next_boundary(jd, _moon, NAK_SPAN)
    next_weekday = weekday + (1 if star_end >= sun_events(civil + timedelta(days=1), tz, lat, lon)['sunrise'] else 0)
    panch['tamil_yogam'] = dict(tamil_yogam(weekday, star_idx), until_local=_local_iso(star_end, tz),
                                next=tamil_yogam(next_weekday, star_idx + 1))
    direction, direction_ta, remedy, remedy_ta = SOOLAM[weekday]
    panch['soolam'] = dict(direction=direction, direction_ta=direction_ta, parigaram=remedy, parigaram_ta=remedy_ta)
    panch['moon_sign'] = dict(index=moon_sign, en=SIGNS[moon_sign], ta=TAMIL[moon_sign])
    affected = (moon_sign - 7) % 12
    panch['chandrashtamam'] = dict(sign_index=affected, sign=SIGNS[affected], sign_ta=TAMIL[affected],
                                   stars=_stars_in_sign(affected))

    personal = {}
    if natal_star is not None:
        count = (star_idx - int(natal_star)) % 27 + 1
        name, name_ta, quality = TARAS[(count - 1) % 9]
        personal['tara'] = dict(count=count, name=name, name_ta=name_ta, quality=quality)
    if natal_sign is not None:
        house = _house_from(moon_sign, int(natal_sign))
        personal['chandra_balam'] = dict(house=house, favourable=house in CHANDRA_BALAM_HOUSES)
        personal['chandrashtamam'] = house == 8
    panch['personal'] = personal or None
    return panch
