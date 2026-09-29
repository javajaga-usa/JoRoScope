"""Parisodhanai (chart verification): facts about the past that the person can check, as a South
Indian astrologer states them before predicting anything.

- Siblings: the 3rd house for younger and the 11th for elder co-born. Each graha in the house or
  aspecting it by Parashari drishti counts one sibling (Jataka Parijata, Phaladeepika): the Sun,
  Mars and Jupiter a brother, the Moon and Venus a sister, and Mercury, Saturn, Rahu and Ketu by
  the sign they occupy (odd signs male, even female). Mars, the karaka of brothers, in the 3rd
  harms the house it signifies ("karako bhava nashaya"); malefics there mark a sibling with
  hardship or lost early, whom tradition still counts. With no graha linked, the lord's strength
  decides between one sibling and few or none.
- Parents: the father from the Sun and the 9th house, the mother from the Moon and the 4th, by the
  dignity and placement of the karaka and the lord, and malefics joining them.
- Past events: the Dasa-Bhukti periods between birth and today whose lords signify an event
  (the houses and karakas used by the rectification tool), within the ages the event usually
  happens, ranked by whether both the Dasa and Bhukti lords signify it and whether Saturn and
  Jupiter both influenced its main house by transit (K.N. Rao's double transit).

These are classical indications, each with how strongly the chart supports it, for the person to
mark right or wrong; a poor match usually means the birth time needs rectification.
"""
from datetime import datetime, timezone

from .common import (
    DIGNITY_SCORE, DUSTHANAS, KENDRAS, MALAYALAM_SIGNS, PLANET_ML, PLANET_TAMIL, SIGN_LORDS, SIGNS, TAMIL_SIGNS,
    TRIKONAS
)
from .report import card, chapter

GRAHAS = ('Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu')
MALE, FEMALE = ('Sun', 'Mars', 'Jupiter'), ('Moon', 'Venus')
MALEFICS = ('Mars', 'Saturn', 'Rahu', 'Ketu')
EXTRA_ASPECTS = {'Mars': (4, 8), 'Jupiter': (5, 9), 'Saturn': (3, 10)}
CONFIDENCE = {'strong': ('Strong', 'வலுவானது', 'ശക്തം'), 'moderate': ('Moderate', 'மிதமானது', 'മിതം'),
              'weak': ('Weak', 'பலவீனமானது', 'ദുർബലം')}
# (brother, sister) words for elder and younger siblings
SIBLING_WORDS = {
    11: dict(en=('elder brother', 'elder sister', 'Elder siblings'), ta=('அண்ணன்', 'அக்கா', 'மூத்த உடன்பிறப்புகள்'),
             ml=('ജ്യേഷ്ഠൻ', 'ജ്യേഷ്ഠത്തി', 'മൂത്ത സഹോദരങ്ങൾ')),
    3: dict(en=('younger brother', 'younger sister', 'Younger siblings'), ta=('தம்பி', 'தங்கை', 'இளைய உடன்பிறப்புகள்'),
            ml=('അനുജൻ', 'അനുജത്തി', 'ഇളയ സഹോദരങ്ങൾ')),
}
# Usual ages for each event, so a Venus Bhukti at age six is not offered as a marriage
EVENT_AGES = {'marriage': (18, 45), 'child': (19, 50), 'career': (16, 45), 'education': (14, 28), 'relocation': (16, 90),
              'property': (20, 90), 'illness': (1, 90), 'father': (0, 90), 'mother': (0, 90)}
EVENT_ORDER = ('education', 'career', 'marriage', 'child', 'property', 'relocation', 'illness', 'father', 'mother')


def _house_of(planets, g):
    return (planets[g]['sign_index'] - planets['Ascendant']['sign_index']) % 12 + 1


def _aspects(planets, g, sign):
    """Whether a graha aspects a sign by Parashari drishti (the nodes are not counted)."""
    if g in ('Rahu', 'Ketu'):
        return False
    d = (sign - planets[g]['sign_index']) % 12 + 1
    return d == 7 or d in EXTRA_ASPECTS.get(g, ())


def _gender(planets, g):
    if g in MALE:
        return 'male'
    if g in FEMALE:
        return 'female'
    return 'male' if planets[g]['sign_index'] % 2 == 0 else 'female'  # odd signs (Aries, Gemini, ...) are male


def _strength(planets, g):
    """Dignity and placement of a graha: about -3 (weak) to +3 (strong)."""
    score = DIGNITY_SCORE.get(planets[g].get('dignity', 'Neutral'), 0)
    house = _house_of(planets, g)
    return score + (1 if house in KENDRAS + TRIKONAS + (11,) else (-1 if house in DUSTHANAS else 0))


def _names(gs, lang):
    table_ = {'en': {g: g for g in GRAHAS}, 'ta': PLANET_TAMIL, 'ml': PLANET_ML}[lang]
    return ', '.join(table_[g] for g in gs)


def _statement(key, topic, en, ta, ml, basis_en, basis_ta, basis_ml, confidence, **extra):
    return dict(key=key, topic=topic, en=en, ta=ta, ml=ml, basis_en=basis_en, basis_ta=basis_ta, basis_ml=basis_ml,
                confidence=confidence, confidence_en=CONFIDENCE[confidence][0], confidence_ta=CONFIDENCE[confidence][1],
                confidence_ml=CONFIDENCE[confidence][2], **extra)


def sibling_reading(planets, house):
    asc = planets['Ascendant']['sign_index']
    sign = (asc + house - 1) % 12
    lord = SIGN_LORDS[sign]
    occupants = [g for g in GRAHAS if planets[g]['sign_index'] == sign]
    aspecting = [g for g in GRAHAS if g not in occupants and _aspects(planets, g, sign)]
    linked = occupants + aspecting
    brothers = sum(_gender(planets, g) == 'male' for g in linked)
    sisters = len(linked) - brothers
    afflicted = [g for g in occupants if g in MALEFICS]
    lord_strength = _strength(planets, lord)
    words = SIBLING_WORDS[house]
    where = {'en': f"the {'11th' if house == 11 else '3rd'} house ({SIGNS[sign]})",
             'ta': f"{house}-ஆம் இடம் ({TAMIL_SIGNS[sign]})", 'ml': f"{house}-ാം ഭാവം ({MALAYALAM_SIGNS[sign]})"}

    if linked:
        confidence = ('strong' if occupants and lord_strength >= 1 and planets['Mars'].get('dignity') != 'Debilitated'
                      else 'moderate' if lord_strength >= 0 else 'weak')
        def count_in(lang):
            parts = [(n, i) for i, n in enumerate((brothers, sisters)) if n]
            if lang == 'en':
                return ', '.join(f"{n} {words['en'][i]}{'s' if n > 1 else ''}" for n, i in parts)
            return ', '.join(f"{words[lang][i]} {n}" for n, i in parts)
        count = {lang: count_in(lang) for lang in ('en', 'ta', 'ml')}
        basis_en = (f"Grahas in {where['en']}: {_names(occupants, 'en') or 'none'}; aspecting it: {_names(aspecting, 'en') or 'none'}. "
                    "Each counts one sibling; the Sun, Mars and Jupiter a brother, the Moon and Venus a sister, the others by their sign.")
        basis_ta = (f"{where['ta']} உள்ள கிரகங்கள்: {_names(occupants, 'ta') or 'இல்லை'}; பார்வை: {_names(aspecting, 'ta') or 'இல்லை'}. "
                    "ஒவ்வொரு கிரகமும் ஒரு உடன்பிறப்பு; சூரியன், செவ்வாய், குரு ஆண்; சந்திரன், சுக்கிரன் பெண்; பிறர் அவர்கள் நிற்கும் ராசிப்படி.")
        basis_ml = (f"{where['ml']} ഉള്ള ഗ്രഹങ്ങൾ: {_names(occupants, 'ml') or 'ഇല്ല'}; ദൃഷ്ടി: {_names(aspecting, 'ml') or 'ഇല്ല'}. "
                    "ഓരോ ഗ്രഹവും ഒരു സഹോദരൻ/സഹോദരി; സൂര്യൻ, ചൊവ്വ, വ്യാഴം പുരുഷൻ; ചന്ദ്രൻ, ശുക്രൻ സ്ത്രീ; മറ്റുള്ളവ നിൽക്കുന്ന രാശി പ്രകാരം.")
    else:
        one = lord_strength >= 1
        gender = 0 if sign % 2 == 0 else 1
        confidence = 'weak'
        count = {'en': f"1 {words['en'][gender]}" if one else 'few or none',
                 'ta': f"{words['ta'][gender]} 1" if one else 'குறைவு அல்லது இல்லை',
                 'ml': f"{words['ml'][gender]} 1" if one else 'കുറവ് അല്ലെങ്കിൽ ഇല്ല'}
        brothers, sisters = (1 - gender, gender) if one else (0, 0)
        state = 'strong' if one else 'weak'
        basis_en = f"No graha is in or aspects {where['en']}; its lord {lord} is {state}, so the house alone decides."
        basis_ta = (f"{where['ta']} கிரகம் இல்லை, பார்வையும் இல்லை; அதிபதி {PLANET_TAMIL[lord]} "
                    f"{'பலமாக' if one else 'பலவீனமாக'} உள்ளதால் இடமே தீர்மானிக்கிறது.")
        basis_ml = (f"{where['ml']} ഗ്രഹമോ ദൃഷ്ടിയോ ഇല്ല; അധിപൻ {PLANET_ML[lord]} "
                    f"{'ബലവാൻ' if one else 'ദുർബലൻ'} ആയതിനാൽ ഭാവം തന്നെ തീരുമാനിക്കുന്നു.")
    notes_en, notes_ta, notes_ml = [], [], []
    if house == 3 and 'Mars' in occupants:
        notes_en.append('Mars, the karaka of brothers, in the 3rd harms younger brothers (karako bhava nashaya).')
        notes_ta.append('சகோதர காரகன் செவ்வாய் 3-இல் இருப்பது இளைய சகோதரர்களுக்குப் பாதிப்பு (காரகோ பாவ நாசாய).')
        notes_ml.append('സഹോദരകാരകനായ ചൊവ്വ 3-ൽ നിൽക്കുന്നത് ഇളയ സഹോദരന്മാർക്ക് ദോഷം (കാരകോ ഭാവ നാശായ).')
    if afflicted:
        notes_en.append(f"Malefics there ({_names(afflicted, 'en')}) mark a sibling with hardship, or one lost early; tradition still counts them.")
        notes_ta.append(f"அங்குள்ள பாப கிரகங்கள் ({_names(afflicted, 'ta')}) ஒரு உடன்பிறப்புக்குச் சிரமம் அல்லது இளமையில் இழப்பைக் காட்டும்; பாரம்பரியம் அவர்களையும் எண்ணும்.")
        notes_ml.append(f"അവിടെയുള്ള പാപഗ്രഹങ്ങൾ ({_names(afflicted, 'ml')}) ഒരു സഹോദരന് പ്രയാസമോ ചെറുപ്പത്തിലെ നഷ്ടമോ കാണിക്കുന്നു; പാരമ്പര്യം അവരെയും എണ്ണുന്നു.")
    title = {lang: words[lang][2] for lang in ('en', 'ta', 'ml')}
    return _statement(
        f"siblings_{'elder' if house == 11 else 'younger'}", 'siblings',
        f"{title['en']}: {count['en']}.", f"{title['ta']}: {count['ta']}.", f"{title['ml']}: {count['ml']}.",
        ' '.join([basis_en, *notes_en]), ' '.join([basis_ta, *notes_ta]), ' '.join([basis_ml, *notes_ml]), confidence,
        house=house, brothers=brothers, sisters=sisters, grahas=linked)


PARENTS = {
    'father': dict(karaka='Sun', house=9, en='Father', ta='தந்தை', ml='അച്ഛൻ', ta_gen='தந்தையின்', ml_gen='അച്ഛന്റെ'),
    'mother': dict(karaka='Moon', house=4, en='Mother', ta='தாய்', ml='അമ്മ', ta_gen='தாயின்', ml_gen='അമ്മയുടെ'),
}


def parent_reading(planets, who):
    p = PARENTS[who]
    karaka, house = p['karaka'], p['house']
    sign = (planets['Ascendant']['sign_index'] + house - 1) % 12
    lord = SIGN_LORDS[sign]
    harsh_house = [g for g in MALEFICS if planets[g]['sign_index'] == sign]
    harsh_karaka = [g for g in MALEFICS if g != karaka and planets[g]['sign_index'] == planets[karaka]['sign_index']]
    helped = planets['Jupiter']['sign_index'] == planets[karaka]['sign_index'] or _aspects(planets, 'Jupiter', planets[karaka]['sign_index'])
    score = _strength(planets, karaka) + _strength(planets, lord) - len(harsh_house) - len(harsh_karaka) + (1 if helped else 0)
    level = 'good' if score >= 2 else ('hard' if score <= -2 else 'mixed')
    confidence = 'strong' if abs(score) >= 4 else ('moderate' if abs(score) >= 2 else 'weak')
    text = {
        'good': (f"{p['en']}: a long and supportive bond; {p['en'].lower()}'s health and standing are good.",
                 f"{p['ta']}: நீண்ட, ஆதரவான உறவு; {p['ta_gen']} உடல்நலமும் நிலையும் நன்று.",
                 f"{p['ml']}: നീണ്ടതും പിന്തുണയുള്ളതുമായ ബന്ധം; {p['ml_gen']} ആരോഗ്യവും നിലയും നല്ലത്."),
        'mixed': (f"{p['en']}: support with ups and downs; {p['en'].lower()} has faced some health or work difficulties.",
                  f"{p['ta']}: ஏற்ற இறக்கங்களுடன் ஆதரவு; {p['ta']} சில உடல்நல அல்லது பணிச் சிரமங்களைச் சந்தித்தார்.",
                  f"{p['ml']}: ഉയർച്ച താഴ്ചകളോടെ പിന്തുണ; {p['ml']} ചില ആരോഗ്യ അല്ലെങ്കിൽ തൊഴിൽ പ്രയാസങ്ങൾ നേരിട്ടു."),
        'hard': (f"{p['en']}: a testing bond; {p['en'].lower()}'s health, distance or an early loss is indicated.",
                 f"{p['ta']}: சோதனையான உறவு; {p['ta_gen']} உடல்நலக் குறைவு, பிரிவு அல்லது இளமையில் இழப்பு சுட்டப்படுகிறது.",
                 f"{p['ml']}: പരീക്ഷണമുള്ള ബന്ധം; {p['ml_gen']} ആരോഗ്യക്കുറവ്, അകൽച്ച അല്ലെങ്കിൽ നേരത്തെയുള്ള നഷ്ടം സൂചിപ്പിക്കുന്നു."),
    }[level]
    dig = planets[karaka].get('dignity', 'Neutral')
    lord_dig = planets[lord].get('dignity', 'Neutral')
    basis_en = (f"{karaka} (karaka) in house {_house_of(planets, karaka)}, {dig.lower()}; the {house}th lord {lord} in house "
                f"{_house_of(planets, lord)}, {lord_dig.lower()}"
                + (f"; malefics in the {house}th: {_names(harsh_house, 'en')}" if harsh_house else '')
                + (f"; malefics with {karaka}: {_names(harsh_karaka, 'en')}" if harsh_karaka else '')
                + ('; Jupiter protects the karaka' if helped else '') + '.')
    basis_ta = (f"காரகன் {PLANET_TAMIL[karaka]} {_house_of(planets, karaka)}-ஆம் இடத்தில்; {house}-ஆம் அதிபதி {PLANET_TAMIL[lord]} "
                f"{_house_of(planets, lord)}-ஆம் இடத்தில்"
                + (f"; {house}-இல் பாபர்: {_names(harsh_house, 'ta')}" if harsh_house else '')
                + (f"; காரகனுடன் பாபர்: {_names(harsh_karaka, 'ta')}" if harsh_karaka else '')
                + ('; குரு காரகனைக் காக்கிறார்' if helped else '') + '.')
    basis_ml = (f"കാരകൻ {PLANET_ML[karaka]} {_house_of(planets, karaka)}-ാം ഭാവത്തിൽ; {house}-ാം അധിപൻ {PLANET_ML[lord]} "
                f"{_house_of(planets, lord)}-ാം ഭാവത്തിൽ"
                + (f"; {house}-ൽ പാപഗ്രഹങ്ങൾ: {_names(harsh_house, 'ml')}" if harsh_house else '')
                + (f"; കാരകനോടൊപ്പം പാപഗ്രഹങ്ങൾ: {_names(harsh_karaka, 'ml')}" if harsh_karaka else '')
                + ('; വ്യാഴം കാരകനെ കാക്കുന്നു' if helped else '') + '.')
    return _statement(who, 'parents', *text, basis_en, basis_ta, basis_ml, confidence, level=level, score=score)


def past_event_windows(chart, now=None, per_event=2):
    """The strongest past Dasa-Bhukti windows for each event type, from birth to now."""
    from ..engine import AYAN, sidereal_position, swe, utc_to_jd
    from ..rectification import EVENTS, JUPITER_ASPECTS, SATURN_ASPECTS, _influences
    swe.set_sid_mode(AYAN[chart.get('ayanamsa') or 'Lahiri'])
    planets = chart['planets']
    asc = planets['Ascendant']['sign_index']
    birth = chart['utc'] if isinstance(chart['utc'], datetime) else datetime.fromisoformat(chart['utc'])
    now = now or datetime.now(timezone.utc)
    signs = {g: planets[g]['sign_index'] for g in GRAHAS}
    age = lambda moment: (moment - birth).days / 365.25
    transit_cache = {}

    def double_transit(moment, main, main_lord_sign):
        key = moment.date()
        if key not in transit_cache:
            jd = utc_to_jd(moment)
            transit_cache[key] = (int(sidereal_position(jd, swe.SATURN)[0] // 30), int(sidereal_position(jd, swe.JUPITER)[0] // 30))
        sat, jup = transit_cache[key]
        return ((_influences(sat, main, SATURN_ASPECTS) or _influences(sat, main_lord_sign, SATURN_ASPECTS))
                and (_influences(jup, main, JUPITER_ASPECTS) or _influences(jup, main_lord_sign, JUPITER_ASPECTS)))

    out = {}
    for kind in EVENT_ORDER:
        _, _, houses, karakas = EVENTS[kind]
        house_signs = [(asc + h - 1) % 12 for h in houses]
        sig = {SIGN_LORDS[s] for s in house_signs} | {g for g, s in signs.items() if s in house_signs} | set(karakas)
        main = house_signs[0]
        main_lord_sign = signs[SIGN_LORDS[main]]
        low, high = EVENT_AGES[kind]
        found = []
        for md in chart.get('dasha') or []:
            for b in md['subperiods']:
                start, end = datetime.fromisoformat(b['start']), datetime.fromisoformat(b['end'])
                if end <= birth or start >= now or b['lord'] not in sig:
                    continue
                start = max(start, birth)
                end = min(end, now)
                mid = start + (end - start) / 2
                if not low <= age(mid) <= high:
                    continue
                dt = double_transit(mid, main, main_lord_sign)
                score = 2 + (2 if md['lord'] in sig else 0) + (2 if dt else 0)
                if score >= 4:
                    # Narrow the Bhukti to its Pratyantaras whose lords also signify the event (at least 10 days long)
                    months = []
                    for p in b.get('pratyantars') or []:
                        ps, pe = max(datetime.fromisoformat(p['start']), start), min(datetime.fromisoformat(p['end']), end)
                        if p['lord'] in sig and (pe - ps).days >= 10:
                            months.append(dict(lord=p['lord'], start=ps.date().isoformat(), end=pe.date().isoformat()))
                    found.append(dict(dasa=md['lord'], bhukti=b['lord'], start=start.date().isoformat(), end=end.date().isoformat(),
                                      age_from=round(age(start), 1), age_to=round(age(end), 1), score=score, double_transit=dt,
                                      months=months[:2]))
        best = sorted(found, key=lambda w: (-w['score'], w['start']))[:per_event]
        out[kind] = dict(significators=sorted(sig), windows=sorted(best, key=lambda w: w['start']))
    return out


def _ages(w):
    a, b = round(w['age_from']), round(w['age_to'])
    return f"{a}" if a == b else f"{a}–{b}"


def _narrow(w, lang):
    """The Pratyantara months inside a window, the narrowest classical timing."""
    months = w.get('months') or []
    if not months:
        return ''
    name = {'en': lambda g: g, 'ta': lambda g: PLANET_TAMIL[g], 'ml': lambda g: PLANET_ML[g]}[lang]
    span = lambda m: m['start'][:7] if m['start'][:7] == m['end'][:7] else f"{m['start'][:7]}–{m['end'][:7]}"
    parts = ', '.join(f"{span(m)} ({name(m['lord'])})" for m in months)
    return {'en': f", most of all in {parts}", 'ta': f", குறிப்பாக {parts}", 'ml': f", പ്രത്യേകിച്ച് {parts}"}[lang]


def calculate_parisodhanai(chart, now=None):
    from ..rectification import EVENTS, EVENTS_ML
    planets = chart['planets']
    statements = [sibling_reading(planets, 11), sibling_reading(planets, 3),
                  parent_reading(planets, 'father'), parent_reading(planets, 'mother')]
    events = past_event_windows(chart, now)
    for kind in EVENT_ORDER:
        windows = events[kind]['windows']
        if not windows:
            continue
        en_label, ta_label, _, _ = EVENTS[kind]
        ml_label = EVENTS_ML[kind]
        en_w = '; or '.join(f"{w['start'][:7]} to {w['end'][:7]} ({w['dasa']}–{w['bhukti']}, age {_ages(w)}){_narrow(w, 'en')}" for w in windows)
        ta_w = '; அல்லது '.join(f"{w['start'][:7]} முதல் {w['end'][:7]} வரை ({PLANET_TAMIL[w['dasa']]}–{PLANET_TAMIL[w['bhukti']]}, "
                                 f"வயது {_ages(w)}){_narrow(w, 'ta')}" for w in windows)
        ml_w = '; അല്ലെങ്കിൽ '.join(f"{w['start'][:7]} മുതൽ {w['end'][:7]} വരെ ({PLANET_ML[w['dasa']]}–{PLANET_ML[w['bhukti']]}, "
                                    f"പ്രായം {_ages(w)}){_narrow(w, 'ml')}" for w in windows)
        best_score = max(w['score'] for w in windows)
        # Dasa timing is a window, not a date: at best moderate, and weak without both lords or the double transit
        confidence = 'moderate' if best_score >= 6 else 'weak'
        if kind in ('father', 'mother'):
            p = PARENTS[kind]
            en = (f"Difficult periods for your {kind}'s health: {en_w}. "
                  f"If your {kind} has passed away, check whether it was within one of them.")
            ta = (f"{p['ta_gen']} உடல்நலத்துக்குக் கடினமான காலங்கள்: {ta_w}. "
                  "இழப்பு நேர்ந்திருந்தால் அது இவற்றில் ஒன்றுக்குள் இருந்ததா எனப் பாருங்கள்.")
            ml = (f"{p['ml_gen']} ആരോഗ്യത്തിന് പ്രയാസമുള്ള കാലങ്ങൾ: {ml_w}. "
                  "നഷ്ടം സംഭവിച്ചിട്ടുണ്ടെങ്കിൽ അത് ഇവയിലൊന്നിനുള്ളിലായിരുന്നോ എന്ന് നോക്കുക.")
        else:
            en = f"{en_label}: most likely {en_w}."
            ta = f"{ta_label}: பெரும்பாலும் {ta_w}."
            ml = f"{ml_label}: മിക്കവാറും {ml_w}."
        sig = events[kind]['significators']
        statements.append(_statement(
            f"event_{kind}", 'events', en, ta, ml,
            f"Periods when both the Dasa and Bhukti lords signify it ({_names(sig, 'en')}), or the Bhukti lord with Saturn and Jupiter's double transit; "
            "the strongest have both.",
            f"தசா, புக்தி அதிபதிகள் இருவரும் இதைக் குறிக்கும் ({_names(sig, 'ta')}) காலங்கள், அல்லது புக்தி அதிபதியுடன் சனி-குரு இரட்டைக் கோச்சாரம்; "
            "இரண்டும் உள்ளவை வலுவானவை.",
            f"ദശ, ഭുക്തി അധിപന്മാർ രണ്ടും ഇതിനെ സൂചിപ്പിക്കുന്ന ({_names(sig, 'ml')}) കാലങ്ങൾ, അല്ലെങ്കിൽ ഭുക്തി അധിപനോടൊപ്പം ശനി-വ്യാഴ ഇരട്ട ഗോചരം; "
            "രണ്ടുമുള്ളവ ശക്തം.",
            confidence, event=kind, windows=windows))

    cards = [card('🔎', 'How to use this', 'இதை எப்படிப் பயன்படுத்துவது',
                  'Mark each statement right or wrong. Most right: the chart and birth time can be trusted for predictions. '
                  'Several wrong: the birth time may be a few minutes off; enter the real dates of past events and run Birth Time '
                  'Rectification on the Tools page.',
                  'ஒவ்வொரு கூற்றையும் சரி அல்லது தவறு எனக் குறிக்கவும். பெரும்பாலும் சரியானால் ஜாதகமும் பிறந்த நேரமும் பலன்களுக்கு நம்பத்தக்கவை. '
                  'பல தவறானால் பிறந்த நேரம் சில நிமிடங்கள் மாறியிருக்கலாம்; கடந்த நிகழ்வுகளின் உண்மையான தேதிகளை உள்ளிட்டு கருவிகள் பக்கத்தில் '
                  'ஜனன நேரத் திருத்தம் செய்யவும்.',
                  title_ml='ഇത് എങ്ങനെ ഉപയോഗിക്കാം',
                  body_ml=('ഓരോ പ്രസ്താവനയും ശരിയോ തെറ്റോ എന്ന് അടയാളപ്പെടുത്തുക. മിക്കതും ശരിയെങ്കിൽ ജാതകവും ജനനസമയവും ഫലപ്രവചനത്തിന് വിശ്വസിക്കാം. '
                           'പലതും തെറ്റെങ്കിൽ ജനനസമയം ഏതാനും മിനിറ്റ് മാറിയിരിക്കാം; കഴിഞ്ഞ സംഭവങ്ങളുടെ യഥാർത്ഥ തീയതികൾ നൽകി ടൂൾസ് പേജിൽ '
                           'ജനനസമയ തിരുത്തൽ ചെയ്യുക.'))]
    return chapter(
        'parisodhanai', 'Parisodhanai (Chart Verification)', 'ஜாதகப் பரிசோதனை',
        'Facts about your past that the chart indicates: siblings, parents and the periods of past events. They are classical '
        'indications with how strongly the chart supports each, for you to check.',
        'ஜாதகம் சுட்டும் உங்கள் கடந்த காலத் தகவல்கள்: உடன்பிறப்புகள், பெற்றோர், கடந்த நிகழ்வுகளின் காலங்கள். இவை பாரம்பரியக் குறிப்புகள், '
        'ஒவ்வொன்றுக்கும் ஜாதகத்தின் ஆதரவு அளவுடன்; நீங்களே சரிபார்க்கலாம்.',
        cards=cards,  # the statements are the checklist; the print report tables them itself
        title_ml='ജാതക പരിശോധന',
        intro_ml=('ജാതകം സൂചിപ്പിക്കുന്ന നിങ്ങളുടെ കഴിഞ്ഞകാല വിവരങ്ങൾ: സഹോദരങ്ങൾ, മാതാപിതാക്കൾ, കഴിഞ്ഞ സംഭവങ്ങളുടെ കാലങ്ങൾ. ഇവ പരമ്പരാഗത '
                  'സൂചനകളാണ്, ഓരോന്നിനും ജാതകത്തിന്റെ പിന്തുണയുടെ അളവോടെ; നിങ്ങൾക്ക് സ്വയം പരിശോധിക്കാം.'),
        statements=statements)
