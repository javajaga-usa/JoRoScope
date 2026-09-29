"""Prasna (horary astrology): a chart for the moment a question is asked, judged by classical rules.

The Udaya Lagna (rising sign) at the question, and optionally the Arudha (a number 1-12 the person
asking chooses), are read with:
- Prasna Marga: a Shirshodaya Lagna (Gemini, Leo, Virgo, Libra, Scorpio, Aquarius) favours
  success, a Prishtodaya one (Aries, Taurus, Cancer, Sagittarius, Capricorn) delay; Pisces is mixed.
  Mandi in the Lagna or with its lord spoils the question.
- Benefics in the Lagna and the kendras help; malefics there obstruct. The Lagna lord in a kendra
  or trikona helps; in the 6th, 8th or 12th it harms.
- The Moon waxing and outside the 6th, 8th and 12th supports the matter.
- Tajika Prasna (Prasna Tantra): the Lagna lord applying (Ithasala) to the lord of the house of the
  question promises it; separating (Easarapha) means it has passed; the same lord is also a yes.
Timing: the degrees left to perfect the Ithasala, in days for a movable, weeks for a dual and
months for a fixed Lagna.
"""
import math
from datetime import datetime, timezone

from .engine import AYAN, SIGNS, TAMIL, jd_to_utc, local_to_utc, sidereal_position, swe, utc_to_jd
from .readings.common import MALAYALAM_SIGNS, PLANET_ML, PLANET_TAMIL, SIGN_LORDS, _ordinal
from .readings.report import card, chapter, table
from .south_indian import mandi_longitude, vedic_day, _zone
from .varshaphal import BODIES, SEVEN, ithasala

QUESTIONS = {
    'general': ('General question', 'பொதுக் கேள்வி', (1,)),
    'marriage': ('Marriage or relationship', 'திருமணம் / உறவு', (7,)),
    'career': ('Job, career or promotion', 'வேலை / தொழில் / பதவி உயர்வு', (10,)),
    'money': ('Money, loans or business gain', 'பணம் / கடன் / வியாபார லாபம்', (2, 11)),
    'health': ('Health or recovery', 'உடல்நலம் / குணமடைதல்', (1, 6)),
    'travel': ('Travel or going abroad', 'பயணம் / வெளிநாடு', (3, 9, 12)),
    'children': ('Children or conception', 'குழந்தை / கருத்தரிப்பு', (5,)),
    'property': ('House, land or vehicle', 'வீடு / நிலம் / வாகனம்', (4,)),
    'education': ('Studies or examinations', 'படிப்பு / தேர்வு', (4, 5)),
    'lost': ('A lost or stolen object', 'தொலைந்த / திருடுபோன பொருள்', (2, 4)),
    'dispute': ('Dispute or court case', 'வழக்கு / தகராறு', (6, 7)),
}
QUESTIONS_ML = {
    'general': 'പൊതുവായ ചോദ്യം', 'marriage': 'വിവാഹം / ബന്ധം', 'career': 'ജോലി / തൊഴിൽ / സ്ഥാനക്കയറ്റം',
    'money': 'പണം / കടം / വ്യാപാര ലാഭം', 'health': 'ആരോഗ്യം / രോഗശാന്തി', 'travel': 'യാത്ര / വിദേശം',
    'children': 'സന്താനം / ഗർഭധാരണം', 'property': 'വീട് / ഭൂമി / വാഹനം', 'education': 'പഠനം / പരീക്ഷ',
    'lost': 'നഷ്ടപ്പെട്ട / മോഷണം പോയ വസ്തു', 'dispute': 'കേസ് / തർക്കം',
}
UNIT_ML = {0: 'ദിവസം', 1: 'മാസം', 2: 'ആഴ്ച'}
SHIRSHODAYA = (2, 4, 5, 6, 7, 10)
PRISHTODAYA = (0, 1, 3, 8, 9)
BENEFICS = ('Jupiter', 'Venus', 'Mercury')
MALEFICS = ('Sun', 'Mars', 'Saturn', 'Rahu', 'Ketu')
UNIT = {0: ('days', 'நாட்கள்'), 1: ('months', 'மாதங்கள்'), 2: ('weeks', 'வாரங்கள்')}  # movable, fixed, dual


def calculate_prasna(question, date_str, time_str, tz_name, lat, lon, arudha=None, ayanamsa='Lahiri'):
    if question not in QUESTIONS:
        raise ValueError('Choose a question type: ' + ', '.join(QUESTIONS))
    if not math.isfinite(lat) or not -66 <= lat <= 66:
        raise ValueError('Latitude must be between 66° south and 66° north in this version.')
    if arudha not in (None, '') and not 1 <= int(arudha) <= 12:
        raise ValueError('The Arudha number must be between 1 and 12.')
    swe.set_sid_mode(AYAN[ayanamsa])
    tz = _zone(tz_name)
    utc = local_to_utc(date_str, time_str, tz_name, 0) if date_str else datetime.now(timezone.utc)
    jd = utc_to_jd(utc)
    lons = {name: sidereal_position(jd, body)[0] for name, body in BODIES}
    lons['Ketu'] = (lons['Rahu'] + 180) % 360
    speeds = {name: sidereal_position(jd, body)[1] for name, body in BODIES}
    asc_lon = swe.houses_ex(jd, lat, lon, b'P', swe.FLG_SIDEREAL)[1][0]
    lagna = int(asc_lon // 30)
    sign = {p: int(l // 30) for p, l in lons.items()}
    house = lambda p: (sign[p] - lagna) % 12 + 1
    day, events = vedic_day(jd, tz, lat, lon)
    mandi_lon, _ = mandi_longitude(jd, events, (day.weekday() + 1) % 7, lat, lon)
    mandi = int(mandi_lon // 30)

    q_en, q_ta, karya_houses = QUESTIONS[question]
    lagna_lord = SIGN_LORDS[lagna]
    factors = []  # (points, en, ta, ml)
    M, P = MALAYALAM_SIGNS, PLANET_ML
    ml_list = lambda ps: ', '.join(P[p] for p in ps)

    def factor(points, en, ta, ml):
        factors.append((points, en, ta, ml))

    if lagna in SHIRSHODAYA:
        factor(1, f'{SIGNS[lagna]} rises head first (Shirshodaya): favours success.', f'{TAMIL[lagna]} சிரோதய ராசி: வெற்றிக்குச் சாதகம்.',
               f'{M[lagna]} ശീർഷോദയ രാശി: വിജയത്തിന് അനുകൂലം.')
    elif lagna in PRISHTODAYA:
        factor(-1, f'{SIGNS[lagna]} rises hind first (Prishtodaya): delay or difficulty.', f'{TAMIL[lagna]} பிருஷ்டோதய ராசி: தாமதம் அல்லது சிரமம்.',
               f'{M[lagna]} പൃഷ്ഠോദയ രാശി: കാലതാമസം അല്ലെങ്കിൽ പ്രയാസം.')
    else:
        factor(0, 'Pisces rises both ways (Ubhayodaya): a mixed start.', 'மீனம் உபயோதய ராசி: கலப்பான தொடக்கம்.',
               'മീനം ഉഭയോദയ രാശി: സമ്മിശ്രമായ തുടക്കം.')
    in_lagna = [p for p in (*SEVEN, 'Rahu', 'Ketu') if sign[p] == lagna]
    good_in = [p for p in in_lagna if p in BENEFICS]
    bad_in = [p for p in in_lagna if p in MALEFICS]
    if good_in:
        factor(1, f"Benefic {', '.join(good_in)} in the Lagna.", f"லக்னத்தில் சுபர் {', '.join(PLANET_TAMIL[p] for p in good_in)}.",
               f"ലഗ്നത്തിൽ ശുഭഗ്രഹം {ml_list(good_in)}.")
    if bad_in:
        factor(-1, f"Malefic {', '.join(bad_in)} in the Lagna.", f"லக்னத்தில் பாபர் {', '.join(PLANET_TAMIL[p] for p in bad_in)}.",
               f"ലഗ്നത്തിൽ പാപഗ്രഹം {ml_list(bad_in)}.")
    kendra_good = [p for p in BENEFICS if house(p) in (4, 7, 10)]
    kendra_bad = [p for p in ('Mars', 'Saturn', 'Rahu', 'Ketu') if house(p) in (4, 7, 10)]
    if len(kendra_good) > len(kendra_bad):
        factor(1, f"Benefics hold the kendras ({', '.join(kendra_good)}).", f"கேந்திரங்களில் சுபர் ({', '.join(PLANET_TAMIL[p] for p in kendra_good)}).",
               f"കേന്ദ്രങ്ങളിൽ ശുഭഗ്രഹങ്ങൾ ({ml_list(kendra_good)}).")
    elif len(kendra_bad) > len(kendra_good):
        factor(-1, f"Malefics hold the kendras ({', '.join(kendra_bad)}).", f"கேந்திரங்களில் பாபர் ({', '.join(PLANET_TAMIL[p] for p in kendra_bad)}).",
               f"കേന്ദ്രങ്ങളിൽ പാപഗ്രഹങ്ങൾ ({ml_list(kendra_bad)}).")
    lh = house(lagna_lord)
    if lh in (1, 4, 5, 7, 9, 10):
        factor(1, f'The Lagna lord {lagna_lord} is well placed in house {lh}.', f'லக்னாதிபதி {PLANET_TAMIL[lagna_lord]} {lh}-ஆம் இடத்தில் நல்ல நிலையில்.',
               f'ലഗ്നാധിപൻ {P[lagna_lord]} {lh}-ാം ഭാവത്തിൽ നല്ല നിലയിൽ.')
    elif lh in (6, 8, 12):
        factor(-1, f'The Lagna lord {lagna_lord} falls in house {lh}.', f'லக்னாதிபதி {PLANET_TAMIL[lagna_lord]} {lh}-ஆம் மறைவிடத்தில்.',
               f'ലഗ്നാധിപൻ {P[lagna_lord]} {lh}-ാം ദുഃസ്ഥാനത്തിൽ.')
    waxing = (lons['Moon'] - lons['Sun']) % 360 < 180
    mh = house('Moon')
    if waxing and mh not in (6, 8, 12):
        factor(1, f'A waxing Moon in house {mh} supports the question.', f'வளர்பிறைச் சந்திரன் {mh}-ஆம் இடத்தில்: கேள்விக்குத் துணை.',
               f'വൃദ്ധിചന്ദ്രൻ {mh}-ാം ഭാവത്തിൽ: ചോദ്യത്തിന് പിന്തുണ.')
    elif not waxing and mh in (6, 8, 12):
        factor(-1, f'A waning Moon in house {mh} weakens the question.', f'தேய்பிறைச் சந்திரன் {mh}-ஆம் இடத்தில்: கேள்வி பலவீனம்.',
               f'ക്ഷയചന്ദ്രൻ {mh}-ാം ഭാവത്തിൽ: ചോദ്യം ദുർബലം.')
    if mandi == lagna or mandi == sign[lagna_lord]:
        factor(-1, f'Mandi ({SIGNS[mandi]}) afflicts the Lagna or its lord.', f'மாந்தி ({TAMIL[mandi]}) லக்னத்தையோ அதன் அதிபதியையோ பாதிக்கிறது.',
               f'മാന്ദി ({M[mandi]}) ലഗ്നത്തെയോ അതിന്റെ അധിപനെയോ ബാധിക്കുന്നു.')

    # The Lagna lord and the lord of the house of the question
    link = None
    for h in karya_houses:
        karya_lord = SIGN_LORDS[(lagna + h - 1) % 12]
        state = 'same' if karya_lord == lagna_lord else ithasala(lons, lagna_lord, karya_lord)
        if state in ('same', 'applying') or (state == 'separating' and link is None):
            link = (h, karya_lord, state)
            if state != 'separating':
                break
    timing = None
    if link and link[2] == 'applying':
        h, kl, _ = link
        fast, slow = sorted((lagna_lord, kl), key=lambda p: -abs(speeds[p]))
        gap = (lons[slow] % 30) - (lons[fast] % 30)
        units, units_ta = UNIT[lagna % 3]
        timing = (max(1, round(gap)), units, units_ta)
        factor(2, f'The Lagna lord {lagna_lord} applies to the {_ordinal(h)} house lord {kl} (Ithasala): the matter will come about.',
               f'லக்னாதிபதி {PLANET_TAMIL[lagna_lord]} {h}-ஆம் அதிபதி {PLANET_TAMIL[kl]} உடன் இத்தசால யோகம்: காரியம் கைகூடும்.',
               f'ലഗ്നാധിപൻ {P[lagna_lord]}, {h}-ാം അധിപൻ {P[kl]} എന്നിവ ഇത്ഥശാല യോഗത്തിൽ: കാര്യം സഫലമാകും.')
    elif link and link[2] == 'same':
        factor(2, f'{lagna_lord} rules both the Lagna and the {_ordinal(link[0])} house: the matter is in your hands.',
               f'{PLANET_TAMIL[lagna_lord]} லக்னத்தையும் {link[0]}-ஆம் இடத்தையும் ஆள்கிறது: காரியம் உங்கள் கையில்.',
               f'{P[lagna_lord]} ലഗ്നത്തെയും {link[0]}-ാം ഭാവത്തെയും ഭരിക്കുന്നു: കാര്യം നിങ്ങളുടെ കൈയിലാണ്.')
    elif link and link[2] == 'separating':
        factor(-1, f'The Lagna lord is separating from the {_ordinal(link[0])} house lord {link[1]} (Easarapha): the chance has passed or is fading.',
               f'லக்னாதிபதி {link[0]}-ஆம் அதிபதி {PLANET_TAMIL[link[1]]}-இலிருந்து பிரிகிறது (ஈசராபம்): வாய்ப்பு கடந்துவிட்டது.',
               f'ലഗ്നാധിപൻ {link[0]}-ാം അധിപനായ {P[link[1]]}-ൽ നിന്ന് വേർപിരിയുന്നു (ഈസരാഫം): അവസരം കടന്നുപോയി.')
    else:
        factor(-1, 'No Tajika link between the Lagna lord and the lord of the matter: delay unless other factors help.',
               'லக்னாதிபதிக்கும் காரிய அதிபதிக்கும் தாஜிகத் தொடர்பு இல்லை: பிற காரணிகள் உதவாவிட்டால் தாமதம்.',
               'ലഗ്നാധിപനും കാര്യാധിപനും തമ്മിൽ താജിക ബന്ധമില്ല: മറ്റു ഘടകങ്ങൾ സഹായിച്ചില്ലെങ്കിൽ കാലതാമസം.')

    arudha_sign = None
    if arudha not in (None, ''):
        arudha_sign = (int(arudha) - 1) % 12  # the chosen number counted from Aries
        a_house = (arudha_sign - lagna) % 12 + 1
        if a_house in (1, 5, 9, 10, 11):
            factor(1, f'The Arudha ({SIGNS[arudha_sign]}) falls in house {a_house} from the Lagna: favourable.',
                   f'ஆரூடம் ({TAMIL[arudha_sign]}) லக்னத்திலிருந்து {a_house}-ஆம் இடம்: சாதகம்.',
               f'ആരൂഢം ({M[arudha_sign]}) ലഗ്നത്തിൽ നിന്ന് {a_house}-ാം ഭാവം: അനുകൂലം.')
        elif a_house in (6, 8, 12):
            factor(-1, f'The Arudha ({SIGNS[arudha_sign]}) falls in house {a_house} from the Lagna: obstacles.',
                   f'ஆரூடம் ({TAMIL[arudha_sign]}) லக்னத்திலிருந்து {a_house}-ஆம் இடம்: தடைகள்.',
               f'ആരൂഢം ({M[arudha_sign]}) ലഗ്നത്തിൽ നിന്ന് {a_house}-ാം ഭാവം: തടസ്സങ്ങൾ.')

    score = sum(f[0] for f in factors)
    verdict = 'good' if score >= 2 else ('bad' if score <= -2 else 'mixed')
    answer_en = {'good': 'Favourable: the matter is likely to succeed.', 'mixed': 'Mixed: success with effort, or partly.',
                 'bad': 'Unfavourable for now: expect delay or obstacles.'}[verdict]
    answer_ta = {'good': 'சாதகம்: காரியம் வெற்றி பெறும் வாய்ப்பு அதிகம்.', 'mixed': 'கலப்பு: முயற்சியால் அல்லது பகுதியாக வெற்றி.',
                 'bad': 'தற்போது சாதகமில்லை: தாமதம் அல்லது தடைகள் எதிர்பார்க்கலாம்.'}[verdict]
    answer_ml = {'good': 'അനുകൂലം: കാര്യം വിജയിക്കാൻ സാധ്യത കൂടുതൽ.', 'mixed': 'സമ്മിശ്രം: പ്രയത്നത്താലോ ഭാഗികമായോ വിജയം.',
                 'bad': 'ഇപ്പോൾ അനുകൂലമല്ല: കാലതാമസമോ തടസ്സങ്ങളോ പ്രതീക്ഷിക്കാം.'}[verdict]
    if timing:
        answer_ml += f' ഏകദേശം {timing[0]} {UNIT_ML[lagna % 3]} കൊണ്ട് പ്രതീക്ഷിക്കാം.'
    if timing:
        answer_en += f' Expected in about {timing[0]} {timing[1]}.'
        answer_ta += f' சுமார் {timing[0]} {timing[2]}இல் எதிர்பார்க்கலாம்.'
    local = jd_to_utc(jd).astimezone(tz)
    cards = [card('🔮', f'Answer: {q_en}', f'பதில்: {q_ta}', answer_en, answer_ta,
                  f"Asked {local:%d %b %Y %H:%M}; {SIGNS[lagna]} rising", f"கேட்ட நேரம் {local:%d-%m-%Y %H:%M}; {TAMIL[lagna]} லக்னம்",
                  verdict=verdict, title_ml=f'ഉത്തരം: {QUESTIONS_ML[question]}', body_ml=answer_ml,
                  sub_ml=f"ചോദിച്ച സമയം {local:%d-%m-%Y %H:%M}; {M[lagna]} ലഗ്നം")]
    factor_rows = [((en, ta, ml), ('helps', 'சாதகம்', 'അനുകൂലം') if p > 0 else
                    (('hinders', 'பாதகம்', 'പ്രതികൂലം') if p < 0 else ('neutral', 'நடுநிலை', 'നിഷ്പക്ഷം')))
                   for p, en, ta, ml in factors]
    rows = [((p, PLANET_TAMIL[p], P[p]), (SIGNS[sign[p]], TAMIL[sign[p]], M[sign[p]]), f'{lons[p] % 30:.2f}°', house(p))
            for p in (*SEVEN, 'Rahu', 'Ketu')]
    rows.insert(0, (('Lagna', 'லக்னம்', 'ലഗ്നം'), (SIGNS[lagna], TAMIL[lagna], M[lagna]), f'{asc_lon % 30:.2f}°', 1))
    rows.append((('Mandi', 'மாந்தி', 'മാന്ദി'), (SIGNS[mandi], TAMIL[mandi], M[mandi]), f'{mandi_lon % 30:.2f}°', (mandi - lagna) % 12 + 1))
    return chapter(
        'prasna', 'Prasna (Horary)', 'பிரசன்னம்',
        'The chart of the moment the question is asked, judged by Prasna Marga and Tajika rules. Ask sincerely, once, '
        'about a matter that concerns you.',
        'கேள்வி கேட்கும் நேரத்தின் ஜாதகம், பிரசன்ன மார்க்க, தாஜிக விதிகளின்படி. உங்களுக்குத் தொடர்புள்ள காரியம் குறித்து ஒருமுறை, மனப்பூர்வமாகக் கேட்கவும்.',
        cards=cards,
        tables=[table('How the answer was reached', 'பதில் கணிக்கப்பட்ட விதம்', [('Factor', 'காரணி', 'ഘടകം'), ('Effect', 'பலன்', 'ഫലം')],
                      factor_rows, title_ml='ഉത്തരം കണ്ടെത്തിയ വിധം'),
                table('Prasna chart', 'பிரசன்ன ஜாதகம்', [('Graha', 'கிரகம்', 'ഗ്രഹം'), ('Sign', 'ராசி', 'രാശി'), ('Degree', 'பாகை', 'ഡിഗ്രി'),
                                                          ('House', 'இடம்', 'ഭാവം')], rows, title_ml='പ്രശ്ന ജാതകം')],
        title_ml='പ്രശ്നം',
        intro_ml=('ചോദ്യം ചോദിക്കുന്ന നിമിഷത്തിലെ ജാതകം, പ്രശ്നമാർഗ്ഗ, താജിക നിയമങ്ങൾ പ്രകാരം. നിങ്ങളെ ബാധിക്കുന്ന കാര്യത്തെക്കുറിച്ച് '
                  'ഒരിക്കൽ, ആത്മാർത്ഥമായി ചോദിക്കുക.'),
        cards_first=True, question=question, asked=local.isoformat(timespec='minutes'), lagna=SIGNS[lagna], verdict=verdict, score=score,
        timing=dict(amount=timing[0], unit=timing[1]) if timing else None,
        arudha=SIGNS[arudha_sign] if arudha_sign is not None else None,
        questions=[dict(key=k, en=v[0], ta=v[1], ml=QUESTIONS_ML[k]) for k, v in QUESTIONS.items()])
