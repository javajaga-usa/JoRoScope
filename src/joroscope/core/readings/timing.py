"""Timing: K.N. Rao's double transit and the Ashtakavarga kakshya transits.
"""

from datetime import datetime
from zoneinfo import ZoneInfo

from .common import MALAYALAM_SIGNS, PLANET_ML, PLANET_TAMIL, SIGNS, SIGN_LORDS, TAMIL_SIGNS, _ordinal


KAKSHYA_LORDS = ['Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon', 'Ascendant']
KAKSHYA_LORDS_TA = ['சனி', 'குரு', 'செவ்வாய்', 'சூரியன்', 'சுக்கிரன்', 'புதன்', 'சந்திரன்', 'லக்னம்']
KAKSHYA_LORDS_ML = [PLANET_ML[p] for p in KAKSHYA_LORDS]

# 9. K.N. Rao & BVB Double Transit (Dwi-Gochara) Engine
# An event needs transit Saturn and Jupiter both to influence (occupy or aspect) the house or
# its lord, and a running Maha or Antar dasa connected with the matter (K.N. Rao).
SATURN_ASPECTS, JUPITER_ASPECTS = (0, 2, 6, 9), (0, 4, 6, 8)
DOUBLE_TRANSIT_EVENTS = [
    ('marriage', 7, ('Venus',), 'Marriage & Relationship', 'திருமணம் & இல்லறம்'),
    ('career', 10, ('Sun', 'Saturn'), 'Career Rise & Promotion', 'தொழில் முன்னேற்றம் & பதவி உயர்வு'),
    ('children', 5, ('Jupiter',), 'Progeny & Children', 'புத்திர பாக்கியம்'),
    ('property', 4, ('Mars', 'Venus'), 'Property, Home & Vehicle', 'பூமி, வீடு & வாகனம்')
]
DT_TITLES_ML = {'marriage': 'വിവാഹം & ദാമ്പത്യം', 'career': 'തൊഴിൽ പുരോഗതി & സ്ഥാനക്കയറ്റം', 'children': 'സന്താനഭാഗ്യം',
                'property': 'ഭൂമി, വീട് & വാഹനം'}
DT_STATUS_ML = {'active': 'സജീവ കാലം: ഇരട്ട ഗോചരവും ദശാ പിന്തുണയും', 'transit': 'ഗോചരം അനുകൂലം; പിന്തുണയ്ക്കുന്ന ദശയ്ക്കായി കാത്തിരിക്കുന്നു',
                'building': 'രൂപപ്പെടുന്നു: ദശാ പിന്തുണ, ഒരു ഗോചരം മാത്രം അനുകൂലം', 'quiet': 'ശാന്തമായ കാലം'}
DT_STATUS = {
    'active': (90, 'Active window: double transit with dasa support', 'செயல்படும் காலம்: இரட்டைப் பெயர்ச்சியுடன் தசா ஆதரவு'),
    'transit': (65, 'Transit ready, awaiting a supporting dasa', 'பெயர்ச்சி சாதகம்; ஆதரவான தசைக்காகக் காத்திருக்கிறது'),
    'building': (50, 'Building: dasa supports, one transit in place', 'உருவாகிறது: தசா ஆதரவு, ஒரு பெயர்ச்சி மட்டும் சாதகம்'),
    'quiet': (25, 'Quiet period', 'அமைதியான காலம்')
}


def _dasa_at(dasha_rows, moment):
    for d in dasha_rows:
        if datetime.fromisoformat(d['start']) <= moment < datetime.fromisoformat(d['end']):
            for b in d.get('subperiods', []):
                if datetime.fromisoformat(b['start']) <= moment < datetime.fromisoformat(b['end']):
                    return d['lord'], b['lord']
            return d['lord'], None
    return None, None


def calculate_double_transit(chart):
    gochara = chart['gochara']
    transit = gochara['planets']
    planets = chart['planets']
    asc_sign = planets['Ascendant']['sign_index']
    tz = ZoneInfo(chart.get('timezone') or 'UTC')
    now = datetime.fromisoformat(gochara['computed_at'])
    sat_sign, jup_sign = transit['Saturn']['sign_index'], transit['Jupiter']['sign_index']
    periods = gochara.get('slow_transits', {})

    def influences(aspects, from_sign, targets):
        return any((t - from_sign) % 12 in aspects for t in targets)

    milestones = []
    for key, house, karakas, title_en, title_ta in DOUBLE_TRANSIT_EVENTS:
        house_sign = (asc_sign + house - 1) % 12
        lord = SIGN_LORDS[house_sign]
        targets = {house_sign, planets[lord]['sign_index']}

        def connected(dasa_lord):
            if dasa_lord is None:
                return False
            ruler = SIGN_LORDS[planets[dasa_lord]['sign_index']] if dasa_lord in ('Rahu', 'Ketu') else dasa_lord
            return (dasa_lord in (lord,) + karakas or ruler == lord or planets[dasa_lord]['house'] == house
                    or planets[dasa_lord]['sign_index'] == planets[lord]['sign_index'])

        sat_now = influences(SATURN_ASPECTS, sat_sign, targets)
        jup_now = influences(JUPITER_ASPECTS, jup_sign, targets)
        maha, antar = _dasa_at(chart.get('dasha', []), now)
        dasa_now = connected(maha) or connected(antar)
        status = ('active' if sat_now and jup_now and dasa_now else 'transit' if sat_now and jup_now
                  else 'building' if dasa_now and (sat_now or jup_now) else 'quiet')

        # Upcoming double-transit windows, each checked against the dasa running when it opens
        windows = []
        for sp in periods.get('Saturn', []):
            if not influences(SATURN_ASPECTS, sp['sign_index'], targets):
                continue
            for jp in periods.get('Jupiter', []):
                start, end = max(sp['start'], jp['start']), min(sp['end'], jp['end'])
                if start < end and influences(JUPITER_ASPECTS, jp['sign_index'], targets):
                    if windows and windows[-1]['_end'] == start:
                        windows[-1]['_end'] = end
                    else:
                        windows.append(dict(_start=start, _end=end))
        windows.sort(key=lambda w: w['_start'])
        window_rows = []
        for w in windows[:4]:
            opens = datetime.fromisoformat(w['_start'])
            w_maha, w_antar = _dasa_at(chart.get('dasha', []), opens)
            window_rows.append(dict(
                start=opens.astimezone(tz).date().isoformat(),
                end=datetime.fromisoformat(w['_end']).astimezone(tz).date().isoformat(),
                dasa=w_maha, bhukti=w_antar, dasa_support=connected(w_maha) or connected(w_antar)))
        supported = [w for w in window_rows if w['dasa_support']]
        best = supported[0] if supported else (window_rows[0] if window_rows else None)

        score, status_en, status_ta = DT_STATUS[status]
        lord_ta = PLANET_TAMIL[lord]
        transit_en = (f"Transit Saturn in {SIGNS[sat_sign]} {'influences' if sat_now else 'does not influence'} your "
                      f"{_ordinal(house)} house ({SIGNS[house_sign]}) or its lord {lord}; transit Jupiter in "
                      f"{SIGNS[jup_sign]} {'influences it' if jup_now else 'does not'}.")
        transit_ta = (f"கோச்சார சனி ({TAMIL_SIGNS[sat_sign]}) உங்கள் {house}-ஆம் பாவம் ({TAMIL_SIGNS[house_sign]}) அல்லது "
                      f"அதன் அதிபதி {lord_ta} மீது {'தொடர்பு கொள்கிறார்' if sat_now else 'தொடர்பு கொள்ளவில்லை'}; "
                      f"கோச்சார குரு ({TAMIL_SIGNS[jup_sign]}) {'தொடர்பு கொள்கிறார்' if jup_now else 'தொடர்பு கொள்ளவில்லை'}.")
        if maha:
            dasa_en = (f" The running {maha}{'–' + antar if antar else ''} dasa is "
                       f"{'connected' if dasa_now else 'not connected'} with this matter.")
            dasa_ta = (f" நடப்பு {PLANET_TAMIL[maha]}{'–' + PLANET_TAMIL[antar] if antar else ''} தசை இந்த விஷயத்துடன் "
                       f"{'தொடர்பு கொண்டுள்ளது' if dasa_now else 'தொடர்பில்லை'}.")
        else:
            dasa_en = dasa_ta = ''
        if best:
            next_en = (f" Next {'dasa-supported ' if best['dasa_support'] else ''}double-transit window: "
                       f"{best['start']} to {best['end']} ({best['dasa']}–{best['bhukti']} dasa).")
            next_ta = (f" அடுத்த {'தசா ஆதரவுள்ள ' if best['dasa_support'] else ''}இரட்டைப் பெயர்ச்சி காலம்: "
                       f"{best['start']} முதல் {best['end']} வரை ({PLANET_TAMIL[best['dasa']]}–{PLANET_TAMIL[best['bhukti']]} தசை).")
        else:
            next_en = " No double-transit window opens in the next 6 years."
            next_ta = " அடுத்த 6 ஆண்டுகளில் இரட்டைப் பெயர்ச்சி காலம் இல்லை."
        M, lord_ml = MALAYALAM_SIGNS, PLANET_ML[lord]
        linked, unlinked = 'ബന്ധപ്പെടുന്നു', 'ബന്ധപ്പെടുന്നില്ല'
        desc_ml = (f"ഗോചര ശനി ({M[sat_sign]}) നിങ്ങളുടെ {house}-ാം ഭാവവുമായോ ({M[house_sign]}) അതിന്റെ അധിപനായ {lord_ml}-ുമായോ "
                   f"{linked if sat_now else unlinked}; ഗോചര വ്യാഴം ({M[jup_sign]}) {linked if jup_now else unlinked}.")
        if maha:
            desc_ml += (f" നടപ്പ് {PLANET_ML[maha]}{'–' + PLANET_ML[antar] if antar else ''} ദശ ഈ കാര്യവുമായി "
                        f"{'ബന്ധപ്പെട്ടിരിക്കുന്നു' if dasa_now else 'ബന്ധപ്പെട്ടിട്ടില്ല'}.")
        if best:
            desc_ml += (f" അടുത്ത {'ദശാ പിന്തുണയുള്ള ' if best['dasa_support'] else ''}ഇരട്ട ഗോചര കാലം: "
                        f"{best['start']} മുതൽ {best['end']} വരെ ({PLANET_ML[best['dasa']]}–{PLANET_ML[best['bhukti']]} ദശ).")
        else:
            desc_ml += " അടുത്ത 6 വർഷത്തിൽ ഇരട്ട ഗോചര കാലമില്ല."
        milestones.append({
            'title_ml': DT_TITLES_ML[key],
            'target_house_ml': f"{house}-ാം ഭാവം ({M[house_sign]}) & അധിപൻ {lord_ml}",
            'status_ml': DT_STATUS_ML[status],
            'desc_ml': desc_ml,
            'key': key,
            'title_en': title_en,
            'title_ta': title_ta,
            'target_house': f"{_ordinal(house)} house ({SIGNS[house_sign]}) & its lord {lord}",
            'target_house_ta': f"{house}-ஆம் பாவம் ({TAMIL_SIGNS[house_sign]}) & அதிபதி {lord_ta}",
            'is_active': status == 'active',
            'status': status,
            'score': score,
            'status_en': status_en,
            'status_ta': status_ta,
            'saturn_influence': sat_now,
            'jupiter_influence': jup_now,
            'dasa_support': dasa_now,
            'windows': window_rows,
            'desc_en': transit_en + dasa_en + next_en,
            'desc_ta': transit_ta + dasa_ta + next_ta
        })

    def position(name, sign, aspects):
        lon = transit[name]['longitude']
        deg = lon % 30
        return {
            'sign': SIGNS[sign],
            'tamil_sign': TAMIL_SIGNS[sign],
            'degree_str': f"{int(deg)}° {int((deg * 60) % 60):02d}′",
            'aspects_houses': sorted(((sign + a) - asc_sign) % 12 + 1 for a in aspects)
        }

    return {
        'calculation_date_utc': gochara['computed_at'].replace('T', ' ').replace('+00:00', ' UTC'),
        'transit_saturn': position('Saturn', sat_sign, SATURN_ASPECTS),
        'transit_jupiter': position('Jupiter', jup_sign, JUPITER_ASPECTS),
        'milestones': milestones
    }

# 12. Ashtakavarga Kakshya Precision Transit System
def calculate_kakshya_transits(chart):
    transit = chart['gochara']['planets']
    sat_lon = transit['Saturn']['longitude']
    jup_lon = transit['Jupiter']['longitude']

    sat_sign = int(sat_lon // 30)
    sat_deg = sat_lon % 30
    jup_sign = int(jup_lon // 30)
    jup_deg = jup_lon % 30

    bav = chart['ashtakavarga']['BAV']
    prastara = chart['ashtakavarga']['prastara']
    kakshya_deg_step = 30.0 / 8.0 # 3.75 deg per Kakshya

    def build_kakshya_table(p_name, sign_idx, current_deg):
        # A kakshya bears fruit only if its lord contributed a bindu to this sign in the
        # transiting planet's own Ashtakavarga (the prastara table).
        current_k_idx = min(int(current_deg / kakshya_deg_step), 7)
        rows = []
        for k in range(8):
            start_d = k * kakshya_deg_step
            end_d = (k + 1) * kakshya_deg_step
            k_lord = KAKSHYA_LORDS[k]
            k_lord_ta = KAKSHYA_LORDS_TA[k]
            has_bindu = bool(prastara[p_name][k_lord][sign_idx])
            is_current = (k == current_k_idx)

            rows.append({
                'kakshya_num': k + 1,
                'range_str': f"{int(start_d)}°{int((start_d*60)%60):02d}′ – {int(end_d)}°{int((end_d*60)%60):02d}′",
                'lord': k_lord,
                'lord_ta': k_lord_ta,
                'lord_ml': KAKSHYA_LORDS_ML[k],
                'status_ml': 'ശുഭഫലം (ഫലപ്രദം)' if has_bindu else 'ശ്രദ്ധ (നിഷ്ഫലം)',
                'has_bindu': has_bindu,
                'status_en': 'Fruitful (Phala-Prada)' if has_bindu else 'Caution (Nishphala)',
                'status_ta': 'சுப பலன் (பலப்பிரதம்)' if has_bindu else 'கவனம் (நிஷ்பலம்)',
                'is_current': is_current
            })
        return current_k_idx, rows

    sat_k_idx, sat_table = build_kakshya_table('Saturn', sat_sign, sat_deg)
    jup_k_idx, jup_table = build_kakshya_table('Jupiter', jup_sign, jup_deg)

    sat_curr = sat_table[sat_k_idx]
    jup_curr = jup_table[jup_k_idx]

    return {
        'saturn': {
            'sign': SIGNS[sat_sign],
            'tamil_sign': TAMIL_SIGNS[sat_sign],
            'current_degree': f"{int(sat_deg)}°{int((sat_deg*60)%60):02d}′",
            'current_kakshya': sat_curr,
            'kakshya_timeline': sat_table,
            'bindus': bav['Saturn'][sat_sign],
            'summary_en': f"Saturn transits Kakshya {sat_k_idx + 1} ({sat_curr['lord']}) of {SIGNS[sat_sign]}, where it holds {bav['Saturn'][sat_sign]} of 8 bindus. Status: {sat_curr['status_en']}.",
            'summary_ml': f"ശനി {MALAYALAM_SIGNS[sat_sign]} രാശിയുടെ {sat_k_idx + 1}-ാം കക്ഷ്യയിൽ ({sat_curr['lord_ml']}) സഞ്ചരിക്കുന്നു; ഈ രാശിയിൽ ശനിക്ക് 8-ൽ {bav['Saturn'][sat_sign]} ബിന്ദുക്കളുണ്ട്. ഫലം: {sat_curr['status_ml']}.",
            'summary_ta': f"சனி பகவான் {TAMIL_SIGNS[sat_sign]} ராசியின் {sat_k_idx + 1}-வது கக்ஷ்யையில் ({sat_curr['lord_ta']}) சஞ்சரிக்கிறார்; இந்த ராசியில் சனிக்கு 8-ல் {bav['Saturn'][sat_sign]} பரல்கள் உள்ளன. பலன்: {sat_curr['status_ta']}."
        },
        'jupiter': {
            'sign': SIGNS[jup_sign],
            'tamil_sign': TAMIL_SIGNS[jup_sign],
            'current_degree': f"{int(jup_deg)}°{int((jup_deg*60)%60):02d}′",
            'current_kakshya': jup_curr,
            'kakshya_timeline': jup_table,
            'bindus': bav['Jupiter'][jup_sign],
            'summary_en': f"Jupiter transits Kakshya {jup_k_idx + 1} ({jup_curr['lord']}) of {SIGNS[jup_sign]}, where it holds {bav['Jupiter'][jup_sign]} of 8 bindus. Status: {jup_curr['status_en']}.",
            'summary_ml': f"വ്യാഴം {MALAYALAM_SIGNS[jup_sign]} രാശിയുടെ {jup_k_idx + 1}-ാം കക്ഷ്യയിൽ ({jup_curr['lord_ml']}) സഞ്ചരിക്കുന്നു; ഈ രാശിയിൽ വ്യാഴത്തിന് 8-ൽ {bav['Jupiter'][jup_sign]} ബിന്ദുക്കളുണ്ട്. ഫലം: {jup_curr['status_ml']}.",
            'summary_ta': f"குரு பகவான் {TAMIL_SIGNS[jup_sign]} ராசியின் {jup_k_idx + 1}-வது கக்ஷ்யையில் ({jup_curr['lord_ta']}) சஞ்சரிக்கிறார்; இந்த ராசியில் குருவுக்கு 8-ல் {bav['Jupiter'][jup_sign]} பரல்கள் உள்ளன. பலன்: {jup_curr['status_ta']}."
        }
    }
