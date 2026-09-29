"""Varshaphal (Tajika annual horoscope) for the running year of life.

- Varsha Pravesh: the moment the sidereal Sun returns to its natal longitude; the annual chart is
  cast for it at the birthplace.
- Muntha: the natal Lagna sign advanced one sign per completed year; its house in the annual chart
  colours the year (9th, 10th, 11th best; 1st, 2nd, 3rd, 5th good; 4th, 6th, 7th, 8th, 12th hard).
- Varsheshwara (lord of the year), chosen from the five office-bearers (Pancha Adhikaris): the
  Muntha lord, the natal Lagna lord, the annual Lagna lord, the Tri-rasi lord of the annual Lagna
  and the lord of the sign holding the Sun (a day year) or the Moon (a night year). Among those
  aspecting the annual Lagna by a Tajika aspect, the strongest by Pancha-vargeeya Bala rules; if
  none aspects, the strongest of all (P.V.R. Narasimha Rao, Varshaphal).
- Pancha-vargeeya Bala: Kshetra, Uchcha, Hadda, Drekkana and Navamsa strength, summed and divided
  by four, with the Tajika Hadda table.
- Ithasala: the annual Lagna lord applying to a house lord within their mean deeptamsa orb promises
  that matter this year; a separating aspect (Easarapha) means it is passing.
- Mudda Dasa: Vimshottari compressed into the year, starting one lord later each year from the natal
  star lord, with the natal star's balance, in proportion to 360 days.
"""
from datetime import datetime, timezone

from .engine import (AYAN, NATURAL_FRIENDS, SIGNS, TAMIL, calculate_vargas, jd_to_utc, sidereal_position,
                     swe, utc_to_jd)
from .readings.common import (
    DASA_LORDS, HOUSE_THEMES, HOUSE_THEMES_ML, MALAYALAM_SIGNS, PLANET_ML, PLANET_TAMIL, SIGN_LORDS, _ordinal
)
from .readings.report import card, chapter, table

SIDEREAL_YEAR = 365.256364
SEVEN = ('Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn')
BODIES = (('Sun', swe.SUN), ('Moon', swe.MOON), ('Mars', swe.MARS), ('Mercury', swe.MERCURY), ('Jupiter', swe.JUPITER),
          ('Venus', swe.VENUS), ('Saturn', swe.SATURN), ('Rahu', swe.MEAN_NODE))
TRI_RASI_DAY = ['Sun', 'Venus', 'Saturn', 'Venus', 'Jupiter', 'Moon', 'Mercury', 'Mars', 'Saturn', 'Mars', 'Jupiter', 'Moon']
TRI_RASI_NIGHT = ['Jupiter', 'Moon', 'Mercury', 'Mars', 'Sun', 'Venus', 'Saturn', 'Venus', 'Saturn', 'Mars', 'Jupiter', 'Moon']
# Tajika Hadda (terms): (lord, end degree) for each sign
HADDA = [
    [('Jupiter', 6), ('Venus', 12), ('Mercury', 20), ('Mars', 25), ('Saturn', 30)],
    [('Venus', 8), ('Mercury', 14), ('Jupiter', 22), ('Saturn', 27), ('Mars', 30)],
    [('Mercury', 6), ('Venus', 12), ('Jupiter', 17), ('Mars', 24), ('Saturn', 30)],
    [('Mars', 7), ('Venus', 13), ('Mercury', 19), ('Jupiter', 26), ('Saturn', 30)],
    [('Jupiter', 6), ('Venus', 11), ('Saturn', 18), ('Mercury', 24), ('Mars', 30)],
    [('Mercury', 7), ('Venus', 17), ('Jupiter', 21), ('Mars', 28), ('Saturn', 30)],
    [('Saturn', 6), ('Mercury', 14), ('Jupiter', 21), ('Venus', 28), ('Mars', 30)],
    [('Mars', 7), ('Venus', 11), ('Mercury', 19), ('Jupiter', 24), ('Saturn', 30)],
    [('Jupiter', 12), ('Venus', 17), ('Mercury', 21), ('Mars', 26), ('Saturn', 30)],
    [('Mercury', 7), ('Jupiter', 14), ('Venus', 22), ('Saturn', 26), ('Mars', 30)],
    [('Mercury', 7), ('Venus', 13), ('Jupiter', 20), ('Mars', 25), ('Saturn', 30)],
    [('Venus', 12), ('Jupiter', 16), ('Mercury', 19), ('Mars', 28), ('Saturn', 30)],
]
DEEP_EXALTATION = {'Sun': 10, 'Moon': 33, 'Mars': 298, 'Mercury': 165, 'Jupiter': 95, 'Venus': 357, 'Saturn': 200}
DEEPTAMSA = {'Sun': 15, 'Moon': 12, 'Mars': 8, 'Mercury': 7, 'Jupiter': 9, 'Venus': 7, 'Saturn': 9}
SPEED_ORDER = ('Moon', 'Mercury', 'Venus', 'Sun', 'Mars', 'Jupiter', 'Saturn')  # fastest first (mean motion)
MUDDA_DAYS = {'Ketu': 21, 'Venus': 60, 'Sun': 18, 'Moon': 30, 'Mars': 21, 'Rahu': 54, 'Jupiter': 48, 'Saturn': 57, 'Mercury': 51}
MUNTHA_RESULT = {
    9: ('excellent: fortune, dharma and support from elders', 'மிகச் சிறப்பு: பாக்கியம், தர்மம், பெரியோர் ஆதரவு', 'good'),
    10: ('excellent: rise in work, status and recognition', 'மிகச் சிறப்பு: தொழில் உயர்வு, அந்தஸ்து, அங்கீகாரம்', 'good'),
    11: ('excellent: gains, fulfilled wishes and good friends', 'மிகச் சிறப்பு: லாபம், விருப்பம் நிறைவேறுதல், நல்ல நண்பர்கள்', 'good'),
    1: ('good: health, confidence and new beginnings', 'நன்று: உடல்நலம், தன்னம்பிக்கை, புதிய தொடக்கங்கள்', 'good'),
    2: ('good: wealth and family harmony', 'நன்று: செல்வம், குடும்ப ஒற்றுமை', 'good'),
    3: ('good: courage, effort and help from siblings', 'நன்று: தைரியம், முயற்சி, உடன்பிறப்பு உதவி', 'good'),
    5: ('good: children, learning and wise choices', 'நன்று: குழந்தைகள், கல்வி, விவேகமான முடிவுகள்', 'good'),
    4: ('difficult: worries about home, mother or property', 'கடினம்: வீடு, தாய், சொத்து குறித்த கவலைகள்', 'bad'),
    6: ('difficult: illness, debts or disputes need care', 'கடினம்: நோய், கடன், வழக்குகளில் கவனம்', 'bad'),
    7: ('difficult: friction with partners and in travel', 'கடினம்: வாழ்க்கைத்துணை, கூட்டாளிகளுடன் உரசல், பயணத் தடைகள்', 'bad'),
    8: ('difficult: obstacles, fatigue and unexpected losses', 'கடினம்: தடைகள், சோர்வு, எதிர்பாராத இழப்புகள்', 'bad'),
    12: ('difficult: expenses, restlessness and separation', 'கடினம்: செலவுகள், அமைதியின்மை, பிரிவு', 'bad'),
}
MATTERS = ((2, 'Wealth', 'செல்வம்'), (7, 'Marriage and partnership', 'திருமணம், கூட்டு'), (10, 'Career and status', 'தொழில், அந்தஸ்து'),
           (11, 'Gains and wishes', 'லாபம், விருப்பங்கள்'), (5, 'Children and learning', 'குழந்தைகள், கல்வி'),
           (4, 'Home and property', 'வீடு, சொத்து'))

MUNTHA_RESULT_ML = {
    9: 'അത്യുത്തമം: ഭാഗ്യം, ധർമ്മം, മുതിർന്നവരുടെ പിന്തുണ', 10: 'അത്യുത്തമം: തൊഴിൽ ഉയർച്ച, പദവി, അംഗീകാരം',
    11: 'അത്യുത്തമം: ലാഭം, ആഗ്രഹസാഫല്യം, നല്ല സുഹൃത്തുക്കൾ', 1: 'നല്ലത്: ആരോഗ്യം, ആത്മവിശ്വാസം, പുതിയ തുടക്കങ്ങൾ',
    2: 'നല്ലത്: സമ്പത്ത്, കുടുംബ ഐക്യം', 3: 'നല്ലത്: ധൈര്യം, പ്രയത്നം, സഹോദരസഹായം', 5: 'നല്ലത്: സന്താനങ്ങൾ, വിദ്യ, വിവേകപൂർണ്ണമായ തീരുമാനങ്ങൾ',
    4: 'പ്രയാസം: വീട്, അമ്മ, സ്വത്ത് എന്നിവയെക്കുറിച്ചുള്ള ആകുലതകൾ', 6: 'പ്രയാസം: രോഗം, കടം, തർക്കങ്ങൾ എന്നിവയിൽ ശ്രദ്ധ',
    7: 'പ്രയാസം: പങ്കാളികളുമായി ഉരസൽ, യാത്രാതടസ്സങ്ങൾ', 8: 'പ്രയാസം: തടസ്സങ്ങൾ, ക്ഷീണം, അപ്രതീക്ഷിത നഷ്ടങ്ങൾ',
    12: 'പ്രയാസം: ചെലവുകൾ, അസ്വസ്ഥത, വേർപാട്',
}
MATTERS_ML = {2: 'സമ്പത്ത്', 7: 'വിവാഹം, പങ്കാളിത്തം', 10: 'തൊഴിൽ, പദവി', 11: 'ലാഭം, ആഗ്രഹങ്ങൾ', 5: 'സന്താനങ്ങൾ, വിദ്യ', 4: 'വീട്, സ്വത്ത്'}
OFFICES_ML = {'Muntha lord': 'മുന്ഥാധിപൻ', 'Birth Lagna lord': 'ജന്മലഗ്നാധിപൻ', 'Year Lagna lord': 'വർഷലഗ്നാധിപൻ',
              'Tri-rasi lord': 'ത്രിരാശ്യധിപൻ', 'Sun-sign lord (day year)': 'സൂര്യരാശ്യധിപൻ (പകൽ വർഷം)',
              'Moon-sign lord (night year)': 'ചന്ദ്രരാശ്യധിപൻ (രാത്രി വർഷം)'}


def _to_lord(p, lord):
    if lord == p:
        return 'own'
    rel = NATURAL_FRIENDS[p].get(lord, 0)
    return 'friend' if rel > 0 else ('enemy' if rel < 0 else 'neutral')


def _relation(p, sign):
    return _to_lord(p, SIGN_LORDS[sign])


def pancha_vargeeya_bala(lons):
    """Strength of the seven grahas in the annual chart (units as in the Tajika texts)."""
    scale = {'own': 1.0, 'friend': 0.75, 'neutral': 0.5, 'enemy': 0.25}
    out = {}
    for p in SEVEN:
        lon = lons[p]
        sign, deg = int(lon // 30), lon % 30
        v = calculate_vargas(lon)
        kshetra = 30 * scale[_relation(p, sign)]
        dist = abs((lon - (DEEP_EXALTATION[p] + 180)) % 360)
        uchcha = min(dist, 360 - dist) / 180 * 20
        hadda_lord = next(lord for lord, end in HADDA[sign] if deg < end)
        hadda = 15 * scale[_to_lord(p, hadda_lord)]
        drekkana = 10 * scale[_relation(p, v['D3'])]
        navamsa = 5 * scale[_relation(p, v['D9'])]
        out[p] = round((kshetra + uchcha + hadda + drekkana + navamsa) / 4, 2)
    return out


def tajika_aspect(from_sign, to_sign):
    """'friendly' (3rd, 5th, 9th, 11th), 'inimical' (1st, 4th, 7th, 10th) or None."""
    d = (to_sign - from_sign) % 12 + 1
    return 'friendly' if d in (3, 5, 9, 11) else ('inimical' if d in (1, 4, 7, 10) else None)


def solar_return(natal_sun, approx_jd):
    jd = approx_jd
    for _ in range(8):
        lon, speed = sidereal_position(jd, swe.SUN)
        diff = ((natal_sun - lon + 180) % 360) - 180
        jd += diff / speed
        if abs(diff) < 1e-7:
            break
    return jd


def ithasala(lons, a, b):
    """'applying' when the faster of two grahas in Tajika aspect is behind the slower within their
    mean deeptamsa, 'separating' when just past it, else None."""
    if a == b:
        return None
    if tajika_aspect(int(lons[a] // 30), int(lons[b] // 30)) is None:
        return None
    fast, slow = (a, b) if SPEED_ORDER.index(a) < SPEED_ORDER.index(b) else (b, a)
    orb = (DEEPTAMSA[fast] + DEEPTAMSA[slow]) / 2
    gap = (lons[slow] % 30) - (lons[fast] % 30)
    if 0 <= gap <= orb:
        return 'applying'
    if -orb <= gap < 0:
        return 'separating'
    return None


def varsha_chart(birth_jd, natal, years, lat, lon):
    natal_sun = natal['Sun']['longitude']
    jd = solar_return(natal_sun, birth_jd + years * SIDEREAL_YEAR)
    next_jd = solar_return(natal_sun, jd + SIDEREAL_YEAR)
    lons = {name: sidereal_position(jd, body)[0] for name, body in BODIES}
    lons['Ketu'] = (lons['Rahu'] + 180) % 360
    asc_lon = swe.houses_ex(jd, lat, lon, b'P', swe.FLG_SIDEREAL)[1][0]
    return jd, next_jd, lons, asc_lon


def calculate_varshaphal(chart, now=None):
    swe.set_sid_mode(AYAN[chart.get('ayanamsa') or 'Lahiri'])
    natal = chart['planets']
    birth_jd = chart['jd']
    now_jd = utc_to_jd(now or datetime.now(timezone.utc))
    years = max(0, int((now_jd - birth_jd) / SIDEREAL_YEAR))
    jd, next_jd, lons, asc_lon = varsha_chart(birth_jd, natal, years, chart['lat'], chart['lon'])
    if jd > now_jd and years > 0:  # the birthday this year has not come yet
        years -= 1
        jd, next_jd, lons, asc_lon = varsha_chart(birth_jd, natal, years, chart['lat'], chart['lon'])
    asc = int(asc_lon // 30)
    sign_of = {p: int(l // 30) for p, l in lons.items()}
    house_of = lambda p: (sign_of[p] - asc) % 12 + 1
    day_year = (lons['Sun'] - asc_lon) % 360 > 180  # Sun above the horizon at Varsha Pravesh

    natal_lagna = natal['Ascendant']['sign_index']
    muntha = (natal_lagna + years) % 12
    muntha_house = (muntha - asc) % 12 + 1
    lord = lambda s: SIGN_LORDS[s]
    offices = [('Muntha lord', 'முந்தா அதிபதி', lord(muntha)), ('Birth Lagna lord', 'ஜன்ம லக்னாதிபதி', lord(natal_lagna)),
               ('Year Lagna lord', 'வருட லக்னாதிபதி', lord(asc)),
               ('Tri-rasi lord', 'திரிராசி அதிபதி', (TRI_RASI_DAY if day_year else TRI_RASI_NIGHT)[asc]),
               ('Sun-sign lord (day year)' if day_year else 'Moon-sign lord (night year)',
                'சூரிய ராசி அதிபதி (பகல் வருடம்)' if day_year else 'சந்திர ராசி அதிபதி (இரவு வருடம்)',
                lord(sign_of['Sun'] if day_year else sign_of['Moon']))]
    pvb = pancha_vargeeya_bala(lons)
    candidates = list(dict.fromkeys(p for _, _, p in offices))
    aspecting = [p for p in candidates if tajika_aspect(sign_of[p], asc)]
    year_lord = max(aspecting or candidates, key=lambda p: pvb[p])

    # Mudda Dasa from the Varsha Pravesh
    moon_lon = natal['Moon']['longitude']
    star = int(moon_lon / (40 / 3))
    first = (star + years) % 9  # one lord on from the natal star lord for each completed year
    year_len = next_jd - jd
    elapsed = (moon_lon % (40 / 3)) / (40 / 3) * MUDDA_DAYS[DASA_LORDS[first]] / 360 * year_len
    start = jd - elapsed
    mudda = []
    for k in range(10):
        g = DASA_LORDS[(first + k) % 9]
        end = start + MUDDA_DAYS[g] / 360 * year_len
        if min(end, next_jd) - max(start, jd) >= 1:  # skip a sliver left over at either end of the year
            mudda.append(dict(lord=g, start=jd_to_utc(max(start, jd)).isoformat(timespec='minutes'),
                              end=jd_to_utc(min(end, next_jd)).isoformat(timespec='minutes'),
                              active=start <= now_jd < end))
        start = end

    tz = chart.get('timezone') or 'UTC'
    from zoneinfo import ZoneInfo
    local = lambda j: jd_to_utc(j).astimezone(ZoneInfo(tz))
    pravesh = local(jd)
    m_en, m_ta, m_verdict = MUNTHA_RESULT[muntha_house]
    yl_house = house_of(year_lord)
    yl_strength = 'strong' if pvb[year_lord] >= 10 else 'weak'
    M, P = MALAYALAM_SIGNS, PLANET_ML
    cards = [
        card('🎉', f'Year {years + 1} of life', f'{years + 1}-ஆம் வயது வருடம்',
             f"The Varshaphal year runs from {pravesh:%d %b %Y %H:%M} to {local(next_jd):%d %b %Y}. "
             f"The year's Lagna is {SIGNS[asc]} and it is a {'day' if day_year else 'night'} year.",
             f"இந்த வருடபலன் {pravesh:%d-%m-%Y %H:%M} முதல் {local(next_jd):%d-%m-%Y} வரை. வருட லக்னம் {TAMIL[asc]}; "
             f"இது {'பகல்' if day_year else 'இரவு'} வருடம்.",
             'Varsha Pravesh: the Sun returns to its birth position', 'வருட பிரவேசம்: சூரியன் ஜனன நிலைக்குத் திரும்பும் நேரம்',
             title_ml=f'ജീവിതത്തിലെ {years + 1}-ാം വർഷം',
             body_ml=(f"ഈ വർഷഫലം {pravesh:%d-%m-%Y %H:%M} മുതൽ {local(next_jd):%d-%m-%Y} വരെ. വർഷലഗ്നം {M[asc]}; "
                      f"ഇത് {'പകൽ' if day_year else 'രാത്രി'} വർഷമാണ്."),
             sub_ml='വർഷപ്രവേശം: സൂര്യൻ ജനനസ്ഥാനത്തേക്ക് മടങ്ങുന്ന സമയം'),
        card('🎯', f'Muntha in {SIGNS[muntha]}, house {muntha_house}', f'முந்தா {TAMIL[muntha]}, {muntha_house}-ஆம் இடம்',
             f"Muntha, the progressed Lagna, falls in the {_ordinal(muntha_house)} house of the year: {m_en}. "
             f"Its lord {lord(muntha)} sits in house {house_of(lord(muntha))}.",
             f"முன்னேறிய லக்னமான முந்தா வருட ஜாதகத்தின் {muntha_house}-ஆம் இடத்தில்: {m_ta}. "
             f"அதன் அதிபதி {PLANET_TAMIL[lord(muntha)]} {house_of(lord(muntha))}-ஆம் இடத்தில்.",
             verdict=m_verdict, title_ml=f'മുന്ഥ {M[muntha]}, {muntha_house}-ാം ഭാവം',
             body_ml=(f"പുരോഗമിച്ച ലഗ്നമായ മുന്ഥ വർഷജാതകത്തിന്റെ {muntha_house}-ാം ഭാവത്തിൽ: {MUNTHA_RESULT_ML[muntha_house]}. "
                      f"അതിന്റെ അധിപൻ {P[lord(muntha)]} {house_of(lord(muntha))}-ാം ഭാവത്തിൽ.")),
        card('👑', f'Lord of the year: {year_lord}', f'வருடாதிபதி: {PLANET_TAMIL[year_lord]}',
             f"{year_lord} ({', '.join(en for en, _, p in offices if p == year_lord)}) rules the year from house {yl_house} "
             f"({HOUSE_THEMES[yl_house][0]}) with Pancha-vargeeya Bala {pvb[year_lord]}. "
             + ('A strong year lord brings its matters to fruition.' if yl_strength == 'strong' else
                'The year lord is weak, so results come with effort; its remedies help.'),
             f"{PLANET_TAMIL[year_lord]} ({', '.join(ta for _, ta, p in offices if p == year_lord)}) {yl_house}-ஆம் இடத்திலிருந்து "
             f"({HOUSE_THEMES[yl_house][1]}) வருடத்தை ஆள்கிறது; பஞ்சவர்கீய பலம் {pvb[year_lord]}. "
             + ('பலமான வருடாதிபதி அதன் காரியங்களை நிறைவேற்றும்.' if yl_strength == 'strong' else
                'வருடாதிபதி பலவீனம்; முயற்சியால் பலன் வரும்; அதன் பரிகாரங்கள் உதவும்.'),
             verdict='good' if yl_strength == 'strong' else 'mixed', title_ml=f'വർഷാധിപൻ: {P[year_lord]}',
             body_ml=(f"{P[year_lord]} ({', '.join(OFFICES_ML[en] for en, _, p in offices if p == year_lord)}) {yl_house}-ാം ഭാവത്തിൽ നിന്ന് "
                      f"({HOUSE_THEMES_ML[yl_house]}) വർഷത്തെ ഭരിക്കുന്നു; പഞ്ചവർഗ്ഗീയ ബലം {pvb[year_lord]}. "
                      + ('ബലമുള്ള വർഷാധിപൻ അതിന്റെ കാര്യങ്ങൾ സഫലമാക്കും.' if yl_strength == 'strong' else
                         'വർഷാധിപൻ ബലഹീനനാണ്; പ്രയത്നത്താൽ ഫലം വരും; അതിന്റെ പരിഹാരങ്ങൾ സഹായിക്കും.'))),
    ]
    ylord = lord(asc)
    for h, en, ta in MATTERS:
        hl = lord((asc + h - 1) % 12)
        state = 'same' if hl == ylord else ithasala(lons, ylord, hl)
        if state in ('same', 'applying'):
            cards.append(card('✨', f'{en}: promised this year', f'{ta}: இந்த வருடம் கைகூடும்',
                              (f"The year's Lagna lord {ylord} also rules the {_ordinal(h)} house" if state == 'same' else
                               f"The year's Lagna lord {ylord} applies (Ithasala) to the {_ordinal(h)} house lord {hl}")
                              + f": {HOUSE_THEMES[h][0]} come forward this year.",
                              f"வருட லக்னாதிபதி {PLANET_TAMIL[ylord]} {h}-ஆம் அதிபதி {PLANET_TAMIL[hl]} உடன் "
                              f"{'ஒன்றே' if state == 'same' else 'இத்தசால யோகம்'}: {HOUSE_THEMES[h][1]} இவ்வருடம் முன்னேறும்.",
                              verdict='good', title_ml=f'{MATTERS_ML[h]}: ഈ വർഷം സഫലമാകും',
                              body_ml=(f"വർഷലഗ്നാധിപൻ {P[ylord]}, {h}-ാം അധിപൻ {P[hl]} എന്നിവ "
                                       f"{'ഒന്നുതന്നെ' if state == 'same' else 'ഇത്ഥശാല യോഗത്തിൽ'}: {HOUSE_THEMES_ML[h]} ഈ വർഷം മുന്നേറും.")))
        elif state == 'separating':
            cards.append(card('⌛', f'{en}: passing', f'{ta}: கடந்து செல்கிறது',
                              f"{ylord} is separating from {hl} (Easarapha): a matter of the {_ordinal(h)} house that has just been settled, "
                              f"or an opportunity already passing.",
                              f"{PLANET_TAMIL[ylord]} {PLANET_TAMIL[hl]}-இலிருந்து பிரிகிறது (ஈசராப யோகம்): {h}-ஆம் இடக் காரியம் "
                              f"முடிந்தது அல்லது வாய்ப்பு கடந்து செல்கிறது.", verdict='mixed',
                              title_ml=f'{MATTERS_ML[h]}: കടന്നുപോകുന്നു',
                              body_ml=(f"{P[ylord]} {P[hl]}-ൽ നിന്ന് വേർപിരിയുന്നു (ഈസരാഫ യോഗം): {h}-ാം ഭാവകാര്യം "
                                       f"പൂർത്തിയായി, അല്ലെങ്കിൽ അവസരം കടന്നുപോകുന്നു.")))

    planet_rows = [((p, PLANET_TAMIL[p], P[p]), (SIGNS[sign_of[p]], TAMIL[sign_of[p]], M[sign_of[p]]), f"{lons[p] % 30:.2f}°", house_of(p),
                    str(pvb[p]) if p in pvb else '—') for p in (*SEVEN, 'Rahu', 'Ketu')]
    mudda_rows = [((m['lord'], PLANET_TAMIL[m['lord']], P[m['lord']]), m['start'][:10], m['end'][:10],
                   ('running', 'நடப்பு', 'നടപ്പ്') if m['active'] else '') for m in mudda]
    office_rows = [((en, ta, OFFICES_ML[en]), (p, PLANET_TAMIL[p], P[p]), house_of(p), str(pvb[p]),
                    ('aspects the Lagna', 'லக்னத்தைப் பார்க்கிறது', 'ലഗ്നത്തെ നോക്കുന്നു') if p in aspecting else '')
                   for en, ta, p in offices]
    return chapter(
        'varshaphal', 'Varshaphal (Annual Horoscope)', 'வருட பலன் (தாஜிக வருஷபலன்)',
        'The Tajika annual chart for your current year of life, cast for the moment the Sun returns to its birth position, '
        'with the Muntha, the lord of the year, Ithasala promises and the Mudda Dasa.',
        'சூரியன் ஜனன நிலைக்குத் திரும்பும் நேரத்திற்கான தாஜிக வருட ஜாதகம்: முந்தா, வருடாதிபதி, இத்தசால யோகங்கள், முத்தா தசை.',
        cards=cards,
        tables=[table('Annual chart', 'வருட ஜாதகம்',
                      [('Graha', 'கிரகம்', 'ഗ്രഹം'), ('Sign', 'ராசி', 'രാശി'), ('Degree', 'பாகை', 'ഡിഗ്രി'), ('House', 'இடம்', 'ഭാവം'),
                       ('Pancha-vargeeya Bala', 'பஞ்சவர்கீய பலம்', 'പഞ്ചവർഗ്ഗീയ ബലം')],
                      planet_rows, title_ml='വർഷജാതകം'),
                table('The five office-bearers', 'பஞ்ச அதிகாரிகள்',
                      [('Office', 'பதவி', 'പദവി'), ('Graha', 'கிரகம்', 'ഗ്രഹം'), ('House', 'இடம்', 'ഭാവം'), ('Bala', 'பலம்', 'ബലം'),
                       ('', '', '')], office_rows, title_ml='പഞ്ചാധികാരികൾ'),
                table('Mudda Dasa', 'முத்தா தசை', [('Dasa', 'தசை', 'ദശ'), ('From', 'முதல்', 'മുതൽ'), ('To', 'வரை', 'വരെ'), ('', '', '')],
                      mudda_rows, title_ml='മുദ്ദ ദശ')],
        title_ml='വർഷഫലം (താജിക വാർഷിക ജാതകം)',
        intro_ml='സൂര്യൻ ജനനസ്ഥാനത്തേക്ക് മടങ്ങുന്ന സമയത്തെ താജിക വർഷജാതകം: മുന്ഥ, വർഷാധിപൻ, ഇത്ഥശാല യോഗങ്ങൾ, മുദ്ദ ദശ.',
        years_completed=years, pravesh=pravesh.isoformat(timespec='minutes'), lagna=SIGNS[asc], muntha=SIGNS[muntha],
        muntha_house=muntha_house, year_lord=year_lord, day_year=day_year, pancha_vargeeya_bala=pvb, mudda=mudda,
        annual_signs={p: sign_of[p] for p in sign_of}, annual_lagna=asc)
