"""JoRoScope South Indian (Tamil) Jathagam Module
Tamil-tradition calculations layered on the core engine:
- Vaaram (Vedic weekday, sunrise to sunrise) and Udayadi Nazhigai
- Tamil solar calendar: 60-year cycle, month and date (sunset rule)
- Dasa Irruppu (balance of the birth Maha Dasa in years, months, days)
- Mandi (Maandhi) rising per the Prasna Marga ghatika rule
- Chevvai Dosham from Lagna, Moon and Venus with classical exemptions
- Rahu-Ketu Dosham, Papa Samyam points and Dosha Samyam for matching
- Daily Tamil Panchangam: anga end times, Soolam, Chandrashtamam, Tara/Chandra Balam
"""
import math
from datetime import timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .engine import (
    swe, AYAN, SIGNS, TAMIL, STARS, TAMIL_STARS, DASHA_NAMES, DASHA_YEARS,
    STAR_GANAS, STAR_YONIS, STAR_RAJJUS, STAR_NADIS,
    placement, local_to_utc, utc_to_jd, jd_to_utc, sun_events, calculate_panchangam
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

GANA_TA = {'Deva': 'தேவ கணம்', 'Manushya': 'மனுஷ கணம்', 'Rakshasa': 'ராட்சச கணம்'}
RAJJU_TA = {'Siro': 'சிரசு', 'Kantha': 'கண்டம்', 'Udara': 'உதரம்', 'Ooru': 'தொடை', 'Pada': 'பாதம்'}
NADI_TA = {'Aadi': 'ஆதி', 'Madhya': 'மத்திய', 'Antya': 'அந்திய'}
YONI_TA = {
    'Horse': 'குதிரை', 'Elephant': 'யானை', 'Sheep': 'ஆடு', 'Serpent': 'பாம்பு', 'Dog': 'நாய்',
    'Cat': 'பூனை', 'Rat': 'எலி', 'Cow': 'பசு', 'Buffalo': 'எருமை', 'Tiger': 'புலி',
    'Deer': 'மான்', 'Monkey': 'குரங்கு', 'Mongoose': 'கீரி', 'Lion': 'சிங்கம்'
}

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


def _sidereal(jd, body):
    """Sidereal longitude and daily speed; the caller sets the ayanamsa mode."""
    pos = swe.calc_ut(jd, body, swe.FLG_MOSEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED)[0]
    return pos[0], pos[3]


def _sun(jd):
    return _sidereal(jd, swe.SUN)


def _moon(jd):
    return _sidereal(jd, swe.MOON)


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


def tamil_calendar(day, tz, lat, lon):
    """Tamil solar date for a day. A month begins on the day the Sun enters the
    sign if the sankranti falls before sunset, otherwise on the following day."""
    sunset = sun_events(day, tz, lat, lon)['sunset']
    month = int(_sun(sunset)[0] // 30)
    ingress = _solve_crossing(sunset, _sun, month * 30.0)
    ingress_day = jd_to_utc(ingress).astimezone(tz).date()
    if ingress >= sun_events(ingress_day, tz, lat, lon)['sunset']:
        first_day = ingress_day + timedelta(days=1)
    else:
        first_day = ingress_day
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


def compare_dosha_samyam(boy_planets, girl_planets):
    """Dosha Samyam: Chevvai Dosham should be present in both or neither chart,
    and the bride's Papa points should not exceed the groom's."""
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
        balanced=chevvai_balanced and papa_balanced
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


def build_south_indian_details(planets, utc, tz_name, lat, lon):
    """Tamil Jathaga Kurippu (birth notes). Uses the ayanamsa mode already set by the engine."""
    tz = _zone(tz_name)
    jd = utc_to_jd(utc)
    day, events = vedic_day(jd, tz, lat, lon)
    weekday = (day.weekday() + 1) % 7  # Sunday = 0

    mandi_lon, mandi_jd = mandi_longitude(jd, events, weekday, lat, lon)
    mandi = placement(mandi_lon)
    mandi['house'] = _house_from(mandi['sign_index'], planets['Ascendant']['sign_index'])
    mandi['rises_local'] = _local_iso(mandi_jd, tz)

    moon = planets['Moon']
    return dict(
        vedic_date=day.isoformat(),
        vaaram=dict(index=weekday, en=VAARAM[weekday][0], ta=VAARAM[weekday][1]),
        tamil_calendar=tamil_calendar(day, tz, lat, lon),
        sunrise_local=_local_iso(events['sunrise'], tz),
        sunset_local=_local_iso(events['sunset'], tz),
        nazhigai=udayadi_nazhigai(jd, events),
        dasa_irruppu=dasa_irruppu(moon['longitude']),
        birth_star=birth_star_attributes(int(moon['longitude'] / NAK_SPAN)),
        mandi=mandi,
        papa_points=papa_points(planets)
    )


def _stars_in_sign(sign_idx):
    first = int(sign_idx * 30 / NAK_SPAN)
    last = int((sign_idx * 30 + 29.9999) / NAK_SPAN)
    return [dict(en=STARS[i], ta=TAMIL_STARS[i]) for i in range(first, last + 1)]


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
    panch['tamil_calendar'] = tamil_calendar(civil, tz, lat, lon)
    panch['vaaram'] = dict(index=weekday, en=VAARAM[weekday][0], ta=VAARAM[weekday][1])
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
