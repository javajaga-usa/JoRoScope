"""Shadbala, Bhava Bala and Vimsopaka readings, and the Krishnamurti Paddhati (KP) system.
"""

from .common import (
    DASA_LORDS, PLANET_TAMIL, SIGNS, SIGN_LORDS, STARS, TAMIL_SIGNS, VIMSHOTTARI_YEARS, _ordinal
)


def get_kp_sublord(lon):
    """Sign, star and KP sub of a longitude. Worked in arc-minutes, where a nakshatra is
    exactly 800', so boundaries such as 280° (the start of Shravana) fall the right way."""
    minutes = round((lon % 360) * 60, 6)
    sign_idx = int(minutes // 1800) % 12
    star_idx = int(minutes // 800) % 27
    star_lord = DASA_LORDS[star_idx % 9]
    offset = minutes - (minutes // 800) * 800
    start = DASA_LORDS.index(star_lord)
    sub_lord = DASA_LORDS[(start + 8) % 9]
    accum = 0.0
    for i in range(9):
        lord = DASA_LORDS[(start + i) % 9]
        accum += 800 * VIMSHOTTARI_YEARS[lord] / 120
        if offset < accum:
            sub_lord = lord
            break
    return sign_idx, SIGNS[sign_idx], TAMIL_SIGNS[sign_idx], SIGN_LORDS[sign_idx], STARS[star_idx], star_lord, sub_lord

# 1. SHADBALA ENGINE & PREDICTIONS
SHADBALA_READINGS = {
    'Sun': {
        'theme_en': 'executive authority, vitality, leadership, and public recognition',
        'theme_ta': 'அதிகார ஆளுமை, உடல் நலம், தலைமைத்துவம் மற்றும் சமூக புகழ்',
        'strong_en': 'Endows radiant confidence, dignified integrity, natural leadership charisma, and strong support from government or senior authorities.',
        'strong_ta': 'சூரியன் உயர் பலம் பெற்றுள்ளதால் அசைக்க முடியாத தன்னம்பிக்கை, கம்பீரமான ஆளுமை, அரசு வழியில் நன்மைகள் மற்றும் தலைமைப் பொறுப்புகள் அமையும்.',
        'weak_en': 'May induce occasional self-doubt or struggle with organizational superiors. Daily Surya Namaskar and honoring father figures strengthen solar vigor.',
        'weak_ta': 'சூரியன் குறைந்த பலம் உள்ளதால் சில சமயங்களில் தயக்கமும், அதிகாரிகளுடன் பிணக்குகளும் நேரலாம். ஆதித்ய ஹிருதய ஸ்தோத்திரம் மற்றும் தந்தையிடம் ஆசி பெறுதல் நலம்.'
    },
    'Moon': {
        'theme_en': 'emotional equanimity, intuitive perception, mental tranquility, and public popularity',
        'theme_ta': 'மன அமைதி, உள்ளுணர்வுத் தெளிவு, பொதுஜன ஆதரவு மற்றும் கற்பனைத் திறன்',
        'strong_en': 'Bestows serene emotional balance, maternal grace, fertile creative instincts, and wide social affection.',
        'strong_ta': 'சந்திரன் உன்னத பலம் பெற்றுள்ளதால் மன அமைதி, தெளிவான உள்ளுணர்வு, கற்பனை ஆற்றல் மற்றும் மக்கள் மத்தியில் நன்மதிப்பு கூடும்.',
        'weak_en': 'Indicates mood sensitivity or over-thinking during stressful periods. Meditation and honoring mother energies cultivate inner stability.',
        'weak_ta': 'சந்திரன் குறைந்த பலம் பெற்றுள்ளதால் மன அமைதியின்மை அல்லது அதீத சிந்தனை ஏற்படலாம். தியானம் மற்றும் தாய்க்கு பணிவிடை செய்வது அமைதி தரும்.'
    },
    'Mars': {
        'theme_en': 'courage, real estate prowess, physical stamina, engineering acumen, and fearlessness',
        'theme_ta': 'துணிச்சல், பூமி யோகம், பொறியியல்/தொழில்நுட்பத் திறன் மற்றும் எதிரிகளை வெல்லும் வலிமை',
        'strong_en': 'Commands heroic willpower, strategic fearlessness, property success, and razor-sharp executive decisiveness.',
        'strong_ta': 'செவ்வாய் மிகுந்த பலம் பெற்றுள்ளதால் அஞ்சாத நெஞ்சம், பூமி-மனை வாங்கும் யோகம், தொழில்நுட்பம் மற்றும் நிர்வாகத்தில் அபார வெற்றி கிட்டும்.',
        'weak_en': 'Can prompt impulsive haste or friction. Channeling fire into sports, yoga, or methodical engineering maintains harmonious energy.',
        'weak_ta': 'செவ்வாய் பலம் குறைவாக இருந்தால் அவசர முடிவுகளும், கோபமும் வரலாம். உடற்பயிற்சி மற்றும் சுப்ரமணியர் வழிபாடு செய்வது ஆற்றலை சமப்படுத்தும்.'
    },
    'Mercury': {
        'theme_en': 'commercial acumen, analytical intellect, communication flair, and diplomatic wit',
        'theme_ta': 'வணிக சாதுரியம், கூர்மையான புத்தி, தகவல் தொடர்புத் திறன் மற்றும் கணக்கியல் விவேகம்',
        'strong_en': 'Fosters multifaceted intellectual brilliance, linguistic elegance, swift mathematical intuition, and prosperous trade associations.',
        'strong_ta': 'புதன் மிகச் சிறந்த பலம் பெற்றுள்ளதால் பேச்சுத் திறமை, எழுத்து, கணிதம், வியாபாரம் மற்றும் கணினித் துறைகளில் அசாத்திய சாதனை புரியலாம்.',
        'weak_en': 'May result in scattered multitasking or mental restlessness. Grounding routines and green color alignments enhance focus.',
        'weak_ta': 'புதன் பலம் குறைவாக உள்ளதால் கவனச்சிதறல் ஏற்படலாம். புதன்கிழமை விஷ்ணு சஹஸ்ரநாமம் பாராயணம் செய்வது அறிவாற்றலை கூர்மையாக்கும்.'
    },
    'Jupiter': {
        'theme_en': 'divine grace, moral wisdom, financial expansion, mentorship, and progeny blessings',
        'theme_ta': 'தெய்வ அனுகூலம், தர்ம சிந்தனை, பொருளாதார வளர்ச்சி, புத்திர பாக்கியம் மற்றும் வழிகாட்டும் பெருமை',
        'strong_en': 'Radiates magnanimous benevolence, deep philosophical comprehension, ethical prosperity, and revered advisor standing.',
        'strong_ta': 'குரு பகவான் பரிபூரண பலம் பெற்றுள்ளதால் நற்குணங்கள், பொருளாதார பெருக்கம், ஆன்மீக அறிவு மற்றும் பெரியோர்களின் ஆசிகள் நிறைவாகக் கிட்டும்.',
        'weak_en': 'Suggests vigilance against financial complacency or over-promising. Honoring preceptors and engaging in philanthropic teaching elevates Jupiter.',
        'weak_ta': 'குரு பலம் குறைவாக இருந்தால் விரயச் செலவுகள் வரலாம். வியாழக்கிழமை தட்சிணாமூர்த்தி வழிபாடு மற்றும் குருமார்களுக்கு மரியாதை செய்தல் சிறப்பு.'
    },
    'Venus': {
        'theme_en': 'artistic refinement, marital harmony, aesthetic luxury, and relational elegance',
        'theme_ta': 'கலை ரசனை, தாம்பத்திய மகிழ்ச்சி, ஆடம்பர சுகபோகம் மற்றும் கவர்ச்சியான தோற்றம்',
        'strong_en': 'Confers exquisite aesthetic discernment, magnetic charm, sensual fulfillment, and enduring joy in matrimonial companionship.',
        'strong_ta': 'சுக்கிரன் நிறைந்த பலம் பெற்றுள்ளதால் கலை, வாகனம், ஆடை ஆபரண சேர்க்கை, வசதியான வாழ்க்கை மற்றும் இனிமையான தாம்பத்தியம் அமையும்.',
        'weak_en': 'May indicate relationship compromises or indulgence. Cultivating devotion to Mahalakshmi and refined artistic discipline brings balance.',
        'weak_ta': 'சுக்கிரன் பலம் குறைவாக இருந்தால் உறவுகளில் சமரசம் தேவைப்படலாம். வெள்ளிக்கிழமை மகாலட்சுமி வழிபாடு செய்வது வாழ்வில் சுப யோகங்களை சேர்க்கும்.'
    },
    'Saturn': {
        'theme_en': 'monumental endurance, career longevity, discipline, organization, and karmic resilience',
        'theme_ta': 'தளராத உழைப்பு, நீண்ட ஆயுள், நிர்வாக ஒழுக்கம் மற்றும் கர்ம வினைகளை வெல்லும் மன உறுதி',
        'strong_en': 'Instills unshakeable stoicism, structural organizing mastery, deep humility, and a career that rises steadily to legendary permanence.',
        'strong_ta': 'சனி பகவான் மிகுந்த பலம் பெற்றுள்ளதால் இரும்பைப் போன்ற மன உறுதி, கடின உழைப்பால் படிப்படியான உயர்ந்த பதவி மற்றும் நிலைத்த செல்வம் கிட்டும்.',
        'weak_en': 'May bring experiences of delay or emotional gravity. Serving underprivileged communities and disciplined consistency transform Saturnian karma.',
        'weak_ta': 'சனி பலம் குறைவாக இருந்தால் காரியத் தடைகளும், தாமதங்களும் வரலாம். ஏழை எளியவர்களுக்கு அன்னதானம் செய்வதும், அனுமன் வழிபாடும் தடைகளை நீக்கும்.'
    }
}
# Why a graha is strong or weak, read from its Shadbala components (virupas)
SHADBALA_FACTORS = [
    ('uchcha', lambda v: v >= 45, 1, 'Close to its exaltation point', 'உச்ச நிலைக்கு அருகில் உள்ளது'),
    ('uchcha', lambda v: v <= 15, -1, 'Close to its debilitation point', 'நீச நிலைக்கு அருகில் உள்ளது'),
    ('saptavargaja', lambda v: v >= 150, 1, 'Dignified across the seven vargas', 'சப்த வர்க்கங்களில் நல்ல கௌரவம் பெற்றது'),
    ('saptavargaja', lambda v: v <= 60, -1, 'With unfriendly lords in most vargas', 'பெரும்பாலான வர்க்கங்களில் பகை வீடுகளில் உள்ளது'),
    ('dig', lambda v: v >= 45, 1, 'Near its direction of strength', 'திக் பலம் நிறைந்த நிலையில் உள்ளது'),
    ('dig', lambda v: v <= 15, -1, 'Far from its direction of strength', 'திக் பலம் குறைந்த நிலையில் உள்ளது'),
    ('cheshta', lambda v: v >= 45, 1, 'Strong in motion (retrograde or slowing)', 'வக்ர/மந்த கதியால் சேஷ்டா பலம் பெற்றது'),
    ('drik', lambda v: v >= 10, 1, 'Aspected mainly by benefics', 'சுப கிரகப் பார்வை பெற்றது'),
    ('drik', lambda v: v <= -10, -1, 'Aspected mainly by malefics', 'பாப கிரகப் பார்வை பெற்றது'),
    ('yuddha', lambda v: v > 0, 1, 'Victorious in a planetary war', 'கிரக யுத்தத்தில் வெற்றி பெற்றது'),
    ('yuddha', lambda v: v < 0, -1, 'Defeated in a planetary war', 'கிரக யுத்தத்தில் தோல்வியுற்றது')
]
# Vimsopaka Bala grades out of 20 (BPHS ch. 7)
VIMSOPAKA_GRADES = [(15, ('Excellent', 'மிகச் சிறப்பு')), (10, ('Good', 'நன்று')), (5, ('Average', 'சராசரி')),
                    (0, ('Poor', 'பலவீனம்'))]
SHADBALA_COMPONENTS = ('uchcha', 'saptavargaja', 'ojayugma', 'kendra', 'drekkana', 'nathonnatha', 'paksha', 'tribhaga',
                       'abda', 'masa', 'vara', 'hora', 'ayana', 'yuddha', 'cheshta', 'drik')


def calculate_shadbala(chart):
    """Interpret the engine's Shadbala (BPHS, as worked in B.V. Raman's Graha and Bhava Balas)."""
    raw = chart['shadbala']
    shadbala_list = []
    for p_name in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']:
        r = raw[p_name]
        ratio = round(r['ratio'], 2)
        is_adequate = ratio >= 1.0
        factors = [dict(en=en, ta=ta, effect=effect) for key, test, effect, en, ta in SHADBALA_FACTORS if test(r[key])]
        if p_name == 'Moon':
            bright = r['paksha'] >= 60
            factors.insert(0, dict(en='A bright Moon' if bright else 'A dim Moon near Amavasai',
                                   ta='ஒளி மிகுந்த சந்திரன்' if bright else 'அமாவாசைக்கு அருகில் ஒளி குறைந்த சந்திரன்',
                                   effect=1 if bright else -1))
        ishta, kashta = r['ishta'], r['kashta']
        favourable = ishta >= kashta
        phala_en = (f"Ishta Phala {ishta:.1f} against Kashta Phala {kashta:.1f}: its dasa and bhukti lean towards "
                    + ('favourable results.' if favourable else 'testing results that reward patience.'))
        phala_ta = (f"இஷ்ட பலன் {ishta:.1f}, கஷ்ட பலன் {kashta:.1f}: இதன் தசா புக்திகள் பெரும்பாலும் "
                    + ('நற்பலன்களைத் தரும்.' if favourable else 'பொறுமையைச் சோதிக்கும் பலன்களைத் தரும்.'))
        interp = SHADBALA_READINGS[p_name]
        shadbala_list.append({
            'planet': p_name,
            'planet_ta': PLANET_TAMIL[p_name],
            'sthana_bala': round(r['sthana'], 2),
            'dig_bala': round(r['dig'], 2),
            'kaala_bala': round(r['kaala'], 2),
            'chesta_bala': round(r['cheshta'], 2),
            'naisargika_bala': round(r['naisargika'], 2),
            'drik_bala': round(r['drik'], 2),
            'components': {k: round(r[k], 2) for k in SHADBALA_COMPONENTS},
            'total_virupas': round(r['total'], 2),
            'total_rupas': round(r['rupas'], 2),
            'min_required_rupas': r['required_rupas'],
            'strength_ratio': ratio,
            'is_adequate': is_adequate,
            'ishta_phala': round(ishta, 2),
            'kashta_phala': round(kashta, 2),
            'factors': factors,
            'theme_en': interp['theme_en'],
            'theme_ta': interp['theme_ta'],
            'reading_en': (interp['strong_en'] if is_adequate else interp['weak_en']) + ' ' + phala_en,
            'reading_ta': (interp['strong_ta'] if is_adequate else interp['weak_ta']) + ' ' + phala_ta
        })

    shadbala_list.sort(key=lambda x: x['strength_ratio'], reverse=True)
    for idx, item in enumerate(shadbala_list):
        item['rank'] = idx + 1

    dominant = shadbala_list[0]
    vulnerable = shadbala_list[-1]
    adequate = [x for x in shadbala_list if x['is_adequate']]

    bhava_rows = []
    for row in chart.get('bhava_bala', []):
        bhava_rows.append(dict(bhava=row['bhava'], lord=row['lord'], lord_ta=PLANET_TAMIL[row['lord']],
                               adhipati=round(row['adhipati'], 2), dig=round(row['dig'], 2), drishti=round(row['drishti'], 2),
                               total_virupas=round(row['total'], 2), rupas=round(row['rupas'], 2), is_strong=row['strong']))
    for rank, row in enumerate(sorted(bhava_rows, key=lambda r: -r['rupas']), 1):
        row['rank'] = rank

    vimsopaka_rows = []
    for p_name, schemes in chart.get('vimsopaka', {}).items():
        row = dict(planet=p_name, planet_ta=PLANET_TAMIL[p_name])
        for scheme, v in schemes.items():
            score = round(v['score'], 2)
            grade = next(g for limit, g in VIMSOPAKA_GRADES if score >= limit)
            row[scheme] = dict(score=score, dignified=v['dignified'], grade_en=grade[0], grade_ta=grade[1],
                               bheda_en=v['bheda'][0] if v['bheda'] else None,
                               bheda_ta=v['bheda'][1] if v['bheda'] else None)
        vimsopaka_rows.append(row)

    return {
        'dominant_planet': dominant,
        'vulnerable_planet': vulnerable,
        'adequate_count': len(adequate),
        'bhavas': bhava_rows,
        'vimsopaka': vimsopaka_rows,
        'method_en': 'Brihat Parashara Hora Shastra, as worked in B.V. Raman\'s Graha and Bhava Balas; minimum strengths per BPHS.',
        'method_ta': 'பிருஹத் பராசர ஹோரா சாஸ்திரம் (பி.வி. ராமனின் கிரக-பாவ பலம் நூல் வழி); குறைந்தபட்ச பலம் பராசரர் வகுத்தபடி.',
        'summary_en': (f"{dominant['planet']} is the strongest graha at {dominant['strength_ratio']}x its required Shadbala, "
                       f"fuelling your {dominant['theme_en']}. {len(adequate)} of 7 grahas meet their classical minimum; "
                       f"{vulnerable['planet']} ({vulnerable['strength_ratio']}x) is the one to strengthen."),
        'summary_ta': (f"உங்கள் ஜாதகத்தில் அதிக பலம் பெற்ற கிரகம் {dominant['planet_ta']} (தேவையான ஷட்பலத்தின் "
                       f"{dominant['strength_ratio']} மடங்கு); இது உங்கள் {dominant['theme_ta']}-க்கு வலு சேர்க்கும். "
                       f"7 கிரகங்களில் {len(adequate)} கிரகங்கள் குறைந்தபட்ச பலத்தைப் பெற்றுள்ளன; "
                       f"பலம் கூட்ட வேண்டிய கிரகம் {vulnerable['planet_ta']} ({vulnerable['strength_ratio']} மடங்கு)."),
        'planets': shadbala_list
    }

# 2. KRISHNAMURTI PADDHATI (KP SYSTEM)
# Cusps judged by their sub-lord, with the houses that promise each matter and the houses
# (12th from them) that negate it (K.S. Krishnamurti, KP Readers).
KP_MATTERS = [
    (1, 'Health & Personality', 'உடல் நலம் & சுய ஆளுமை', (1, 5, 11), (6, 8, 12)),
    (2, 'Wealth & Family', 'தனம் & குடும்பம்', (2, 6, 11), (5, 8, 12)),
    (5, 'Children & Intellect', 'புத்திர பாக்கியம் & புத்தி', (2, 5, 11), (1, 4, 10)),
    (7, 'Marriage & Partnership', 'திருமணம் & கூட்டாண்மை', (2, 7, 11), (1, 6, 10)),
    (10, 'Profession & Status', 'தொழில் & அந்தஸ்து', (2, 6, 10, 11), (1, 5, 9)),
    (11, 'Gains & Fulfilment of Desires', 'லாபம் & விருப்பங்கள் நிறைவேறுதல்', (2, 6, 11), (5, 8, 12))
]
KP_VERDICTS = {
    'promised': ('Promised', 'உறுதி'),
    'mixed': ('Promised with delays', 'தாமதத்துடன் உறுதி'),
    'weak': ('Weakly supported', 'பலம் குறைவு'),
    'denied': ('Obstructed', 'தடை'),
    'neutral': ('Not clearly indicated', 'தெளிவில்லை')
}


def _kp_house(lon, cusps):
    """Placidus bhava (1-12) holding a longitude: from its cusp up to the next cusp."""
    for n in range(12):
        if (lon - cusps[n]) % 360 < (cusps[(n + 1) % 12] - cusps[n]) % 360:
            return n + 1
    return 1


def _houses_en(houses):
    hs = sorted(houses)
    if len(hs) < 2:
        return f"house {hs[0]}" if hs else 'no house'
    return 'houses ' + ', '.join(map(str, hs[:-1])) + f' and {hs[-1]}'


def _houses_ta(houses, case):
    """Tamil house list in the accusative ('acc', before a verb) or genitive ('gen')."""
    hs = sorted(houses)
    if len(hs) == 1:
        return f"{hs[0]}-ஆம் பாவத்தைக்" if case == 'acc' else f"{hs[0]}-ஆம் பாவத்"
    joined = ', '.join(map(str, hs))
    return f"{joined} ஆகிய பாவங்களைக்" if case == 'acc' else f"{joined} ஆகிய பாவங்களின்"


def calculate_kp_system(chart):
    kp = chart.get('kp')
    if kp:
        cusps, longitudes = kp['cusps'], kp['planets']
    else:  # a chart built without the engine's KP block: equal houses in the chart's ayanamsa
        asc_lon = chart['planets']['Ascendant']['longitude']
        cusps = [(asc_lon + i * 30) % 360 for i in range(12)]
        longitudes = {p: chart['planets'][p]['longitude'] for p in DASA_LORDS}
    grahas = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
    info = {p: get_kp_sublord(longitudes[p]) for p in grahas}
    occupied = {p: {_kp_house(longitudes[p], cusps)} for p in grahas}
    owned = {p: {n + 1 for n, c in enumerate(cusps) if SIGN_LORDS[int(c // 30) % 12] == p} for p in grahas}
    for node in ('Rahu', 'Ketu'):
        # A node acts as an agent of the lord of the sign it occupies
        agent = info[node][3]
        occupied[node] |= occupied[agent]
        owned[node] = set(owned[agent])

    def signified(p):
        star_lord = info[p][5]
        return dict(star_lord_occupies=sorted(occupied[star_lord]), occupies=sorted(occupied[p]),
                    star_lord_owns=sorted(owned[star_lord]), owns=sorted(owned[p]))

    def row(label, lon, extra):
        sign_idx, sign_name, sign_ta, sign_lord, star_name, star_lord, sub_lord = get_kp_sublord(lon)
        deg_in_sign = lon % 30
        d = int(deg_in_sign); m = int((deg_in_sign * 60) % 60); sec = int((deg_in_sign * 3600) % 60)
        return dict(label, longitude=round(lon, 4), degree_str=f"{d}° {m:02d}′ {sec:02d}″",
                    sign=sign_name, sign_ta=sign_ta, sign_lord=sign_lord, sign_lord_ta=PLANET_TAMIL[sign_lord],
                    star_name=star_name, star_lord=star_lord, star_lord_ta=PLANET_TAMIL[star_lord],
                    sub_lord=sub_lord, sub_lord_ta=PLANET_TAMIL[sub_lord], **extra)

    cusp_rows = [row(dict(cusp=i + 1), lon, {}) for i, lon in enumerate(cusps)]
    planet_rows = []
    for p in grahas:
        levels = signified(p)
        houses = sorted(set().union(*levels.values()))
        planet_rows.append(row(dict(planet=p, planet_ta=PLANET_TAMIL[p]), longitudes[p],
                               dict(kp_house=_kp_house(longitudes[p], cusps),
                                    significations=houses, signification_levels=levels)))

    interpretations = {}
    for cusp, title_en, title_ta, favourable, negating in KP_MATTERS:
        sub = cusp_rows[cusp - 1]['sub_lord']
        star_lord = info[sub][5]
        primary = occupied[star_lord] | owned[star_lord]
        secondary = occupied[sub] | owned[sub]
        good, bad, own_good = primary & set(favourable), primary & set(negating), secondary & set(favourable)
        if good and not bad:
            verdict = 'promised'
        elif good:
            verdict = 'mixed'
        elif own_good:
            verdict = 'weak'
        elif bad:
            verdict = 'denied'
        else:
            verdict = 'neutral'
        sub_ta, star_ta = PLANET_TAMIL[sub], PLANET_TAMIL[star_lord]
        basis_en = (f"The {_ordinal(cusp)} cusp sub-lord is {sub}, in the star of {star_lord}, which signifies "
                    f"{_houses_en(primary)}; {sub} itself signifies {_houses_en(secondary)}.")
        basis_ta = (f"{cusp}-ஆம் பாவ ஆரம்பத்தின் உப-அதிபதி {sub_ta}; அது {star_ta} நட்சத்திரத்தில் உள்ளது. "
                    f"{star_ta} {_houses_ta(primary, 'acc')} குறிக்கிறது; {sub_ta} தானாக {_houses_ta(secondary, 'acc')} குறிக்கிறது.")
        outcome = {
            'promised': (f"{title_en} is clearly promised through {_houses_en(good)}.",
                         f"{title_ta} {_houses_ta(good, 'gen')} தொடர்பால் உறுதியாக வாக்களிக்கப்பட்டுள்ளது."),
            'mixed': (f"{title_en} is promised through {_houses_en(good)}, but the link to {_houses_en(bad)} brings delays or struggle.",
                      f"{title_ta} {_houses_ta(good, 'gen')} தொடர்பால் உறுதி; ஆனால் {_houses_ta(bad, 'gen')} தொடர்பால் தாமதமோ போராட்டமோ இருக்கும்."),
            'weak': (f"{title_en} is possible but only modestly supported, through the sub-lord's own {_houses_en(own_good)}.",
                     f"{title_ta} சாத்தியம்; ஆனால் உப-அதிபதியின் சொந்த {_houses_ta(own_good, 'gen')} தொடர்பு வழியே மட்டுமே குறைந்த ஆதரவு உள்ளது."),
            'denied': (f"{title_en} meets obstruction from {_houses_en(bad)}, so only a supporting dasa can deliver it.",
                       f"{title_ta} தடைகளைச் சந்திக்கும்: {_houses_ta(bad, 'gen')} தொடர்பு இதற்கு எதிராக உள்ளது; சாதகமான தசையில் மட்டுமே பலன் கிட்டும்."),
            'neutral': (f"{title_en} is not clearly indicated either way by this sub-lord; the dasa lords decide.",
                        f"{title_ta} இந்த உப-அதிபதியால் தெளிவாகச் சுட்டப்படவில்லை; நடப்பு தசா நாதர்களே தீர்மானிப்பர்.")
        }[verdict]
        interpretations[f'cusp_{cusp}'] = dict(
            cusp_num=cusp,
            title_en=f"{_ordinal(cusp)} Cusp Sub-Lord ({title_en})",
            title_ta=f"{cusp}-ஆம் பாவ உப-அதிபதி ({title_ta})",
            sub_lord=sub, sub_lord_ta=sub_ta, star_lord=star_lord, star_lord_ta=star_ta,
            signified_houses=sorted(primary), favourable_houses=list(favourable), negating_houses=list(negating),
            verdict=verdict, verdict_en=KP_VERDICTS[verdict][0], verdict_ta=KP_VERDICTS[verdict][1],
            reading_en=f"{basis_en} {outcome[0]}", reading_ta=f"{basis_ta} {outcome[1]}"
        )

    # Ruling planets at birth: Lagna sign, star and sub lords, Moon sign and star lords, and the day lord
    asc = cusp_rows[0]
    moon = next(r for r in planet_rows if r['planet'] == 'Moon')
    weekday = chart.get('vedic_weekday')
    ruling = [('Lagna sign lord', 'லக்ன ராசி அதிபதி', asc['sign_lord']), ('Lagna star lord', 'லக்ன நட்சத்திர அதிபதி', asc['star_lord']),
              ('Lagna sub-lord', 'லக்ன உப-அதிபதி', asc['sub_lord']), ('Moon sign lord', 'சந்திர ராசி அதிபதி', moon['sign_lord']),
              ('Moon star lord', 'சந்திர நட்சத்திர அதிபதி', moon['star_lord'])]
    if weekday is not None:
        day_lord = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'][weekday]
        ruling.append(('Day lord', 'கிழமை அதிபதி', day_lord))
    ruling_planets = [dict(role_en=en, role_ta=ta, planet=p, planet_ta=PLANET_TAMIL[p]) for en, ta, p in ruling]

    return {
        'ayanamsa': 'Krishnamurti' if kp else None,
        'ayanamsa_degrees': round(kp['ayanamsa'], 4) if kp else None,
        'cusps': cusp_rows,
        'planets': planet_rows,
        'cuspal_predictions': interpretations,
        'ruling_planets': ruling_planets
    }
