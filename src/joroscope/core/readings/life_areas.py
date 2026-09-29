"""Life-area reports beside marriage and career: education, children, health, wealth and property,
foreign travel and settlement, and spiritual life.

Each reads its house (the 4th, 5th, 1st, 2nd, 12th or 9th), the house's lord (placement and
dignity), the grahas in and aspecting it and the karakas, then the classical combinations for
that area, and lists the coming Dasa-Bhukti periods whose lords signify it (strongest when both
the Dasa and Bhukti lords do), with K.N. Rao's double-transit windows where the report has them.
For health the periods listed are the ones that need care: those of the 6th, 8th and 12th lords
and the malefics tenanting the 1st, 6th or 8th.
"""
from datetime import datetime, timezone

from .common import (
    DIGNITY_SCORE, DUSTHANAS, HOUSE_THEMES, HOUSE_THEMES_ML, KENDRAS, MALAYALAM_SIGNS, PLANET_ML, PLANET_TAMIL,
    SIGN_LORDS, SIGNS, TAMIL_SIGNS, TRIKONAS, _ordinal
)
from .life_reports import (
    BENEFICS, DIGNITY_ML, MALEFICS, WINDOW_HEAD, _aspecting, _dig_ml, _dt_windows, _house, _karaka, _ml_list,
    _window_rows, period_windows
)
from .report import card, chapter, table

GRAHAS = ('Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu')
DIGNITY_TA = {'Exalted': 'உச்சம்', 'Own Sign': 'ஆட்சி', 'Moolatrikona': 'மூலத்திரிகோணம்', 'Great Friend': 'அதி நட்பு',
              'Friend': 'நட்பு', 'Neutral': 'சமம்', 'Enemy': 'பகை', 'Great Enemy': 'அதி பகை', 'Debilitated': 'நீசம்'}
BODY = {  # what each graha rules in the body (Brihat Parashara Hora Shastra ch. 3, in plain terms)
    'Sun': ('heart, eyes and vitality', 'இதயம், கண், உயிர்ச்சக்தி', 'ഹൃദയം, കണ്ണ്, ജീവശക്തി'),
    'Moon': ('mind, sleep and body fluids', 'மனம், தூக்கம், உடல் நீர்மங்கள்', 'മനസ്സ്, ഉറക്കം, ശരീരദ്രവങ്ങൾ'),
    'Mars': ('blood, muscles, injuries and surgery', 'இரத்தம், தசை, காயம், அறுவை சிகிச்சை', 'രക്തം, പേശികൾ, മുറിവുകൾ, ശസ്ത്രക്രിയ'),
    'Mercury': ('nerves, skin and speech', 'நரம்பு, தோல், பேச்சு', 'നാഡികൾ, ത്വക്ക്, സംസാരം'),
    'Jupiter': ('liver, fat and sugar balance', 'கல்லீரல், கொழுப்பு, சர்க்கரை சமநிலை', 'കരൾ, കൊഴുപ്പ്, പഞ്ചസാര സന്തുലനം'),
    'Venus': ('kidneys, hormones and reproductive health', 'சிறுநீரகம், ஹார்மோன், இனப்பெருக்க நலம்', 'വൃക്കകൾ, ഹോർമോണുകൾ, പ്രത്യുൽപ്പാദന ആരോഗ്യം'),
    'Saturn': ('bones, joints, teeth and long-standing ailments', 'எலும்பு, மூட்டு, பல், நீண்டகால நோய்கள்', 'അസ്ഥി, സന്ധികൾ, പല്ല്, ദീർഘകാല രോഗങ്ങൾ'),
    'Rahu': ('hard-to-diagnose conditions, allergies and anxiety', 'கண்டறிய கடினமான நோய், ஒவ்வாமை, பதற்றம்', 'കണ്ടെത്താൻ പ്രയാസമുള്ള രോഗങ്ങൾ, അലർജി, ഉത്കണ്ഠ'),
    'Ketu': ('sudden fevers, infections and minor operations', 'திடீர் காய்ச்சல், தொற்று, சிறு அறுவை', 'പെട്ടെന്നുള്ള പനി, അണുബാധ, ചെറിയ ശസ്ത്രക്രിയ'),
}

AREAS = {
    'education': dict(
        house=4, houses=(4, 5, 9), karakas=('Mercury', 'Jupiter'), dt=None, icon='🎓',
        title=('Education Report', 'கல்வி அறிக்கை', 'വിദ്യാഭ്യാസ റിപ്പോർട്ട്'),
        intro=('Learning from the 4th (schooling), 5th (intelligence) and 9th (higher studies), with Mercury and Jupiter.',
               '4-ஆம் இடம் (அடிப்படைக் கல்வி), 5-ஆம் இடம் (புத்தி), 9-ஆம் இடம் (உயர்கல்வி), புதன், குரு வழியாகக் கல்வி.',
               '4-ാം ഭാവം (അടിസ്ഥാന വിദ്യാഭ്യാസം), 5-ാം ഭാവം (ബുദ്ധി), 9-ാം ഭാവം (ഉന്നത വിദ്യാഭ്യാസം), ബുധൻ, വ്യാഴം എന്നിവയിലൂടെ വിദ്യ.'),
        when=('Periods favouring study, examinations and qualifications', 'படிப்பு, தேர்வு, தகுதிகளுக்குச் சாதகமான காலங்கள்',
              'പഠനം, പരീക്ഷ, യോഗ്യതകൾ എന്നിവയ്ക്ക് അനുകൂല കാലങ്ങൾ')),
    'children': dict(
        house=5, houses=(5, 11), karakas=('Jupiter',), dt='children', icon='👶',
        title=('Children (Santana) Report', 'புத்திர (சந்தான) அறிக்கை', 'സന്താന റിപ്പോർട്ട്'),
        intro=('Progeny from the 5th house and its lord, Jupiter as putrakaraka, and the Jaimini Putrakaraka.',
               '5-ஆம் இடம், அதன் அதிபதி, புத்திரகாரகன் குரு, ஜைமினி புத்திரகாரகன் வழியாகக் குழந்தைப் பேறு.',
               '5-ാം ഭാവം, അതിന്റെ അധിപൻ, പുത്രകാരകനായ വ്യാഴം, ജൈമിനി പുത്രകാരകൻ എന്നിവയിലൂടെ സന്താനഭാഗ്യം.'),
        when=('Periods for the blessing of children', 'புத்திர பாக்கியத்துக்கான காலங்கள்', 'സന്താനഭാഗ്യത്തിനുള്ള കാലങ്ങൾ')),
    'health': dict(
        house=1, houses=(1, 6, 8), karakas=('Sun', 'Moon'), dt=None, icon='🩺',
        title=('Health Report', 'உடல்நல அறிக்கை', 'ആരോഗ്യ റിപ്പോർട്ട്'),
        intro=('Vitality from the Lagna and its lord, the Sun and the Moon; illness from the 6th, chronic matters from the 8th.',
               'லக்னம், லக்னாதிபதி, சூரியன், சந்திரன் வழியாக உயிர்ச்சக்தி; 6-ஆம் இடம் நோய், 8-ஆம் இடம் நீண்டகால விஷயங்கள்.',
               'ലഗ്നം, ലഗ്നാധിപൻ, സൂര്യൻ, ചന്ദ്രൻ എന്നിവയിലൂടെ ജീവശക്തി; 6-ാം ഭാവം രോഗം, 8-ാം ഭാവം ദീർഘകാല കാര്യങ്ങൾ.'),
        when=('Periods that need care with health', 'உடல்நலத்தில் கவனம் தேவைப்படும் காலங்கள்', 'ആരോഗ്യത്തിൽ ശ്രദ്ധ വേണ്ട കാലങ്ങൾ')),
    'wealth': dict(
        house=2, houses=(2, 11, 4), karakas=('Jupiter', 'Venus'), dt='property', icon='💰',
        title=('Wealth & Property Report', 'செல்வம் & சொத்து அறிக்கை', 'സമ്പത്ത് & സ്വത്ത് റിപ്പോർട്ട്'),
        intro=('Savings from the 2nd, gains from the 11th, land, house and vehicles from the 4th, with Jupiter, Venus and Mars.',
               '2-ஆம் இடம் சேமிப்பு, 11-ஆம் இடம் லாபம், 4-ஆம் இடம் நிலம், வீடு, வாகனம்; குரு, சுக்கிரன், செவ்வாய்.',
               '2-ാം ഭാവം സമ്പാദ്യം, 11-ാം ഭാവം ലാഭം, 4-ാം ഭാവം ഭൂമി, വീട്, വാഹനം; വ്യാഴം, ശുക്രൻ, ചൊവ്വ.'),
        when=('Periods of gains, savings and property', 'லாபம், சேமிப்பு, சொத்துக்கான காலங்கள்', 'ലാഭം, സമ്പാദ്യം, സ്വത്ത് എന്നിവയ്ക്കുള്ള കാലങ്ങൾ')),
    'foreign': dict(
        house=12, houses=(12, 9, 3), karakas=('Rahu',), dt=None, icon='✈️',
        title=('Foreign Travel & Settlement Report', 'வெளிநாட்டுப் பயணம் & குடியேற்ற அறிக்கை', 'വിദേശയാത്ര & താമസ റിപ്പോർട്ട്'),
        intro=('Life abroad from the 12th house, long journeys from the 9th and short travel from the 3rd, with Rahu.',
               '12-ஆம் இடம் வெளிநாட்டு வாழ்க்கை, 9-ஆம் இடம் நீண்ட பயணம், 3-ஆம் இடம் குறும்பயணம்; ராகு.',
               '12-ാം ഭാവം വിദേശജീവിതം, 9-ാം ഭാവം ദീർഘയാത്ര, 3-ാം ഭാവം ചെറുയാത്ര; രാഹു.'),
        when=('Periods for travel, work or study abroad', 'பயணம், வெளிநாட்டுப் பணி அல்லது படிப்புக்கான காலங்கள்',
              'യാത്ര, വിദേശ ജോലി അല്ലെങ്കിൽ പഠനം എന്നിവയ്ക്കുള്ള കാലങ്ങൾ')),
    'spiritual': dict(
        house=9, houses=(9, 12, 5), karakas=('Jupiter', 'Ketu'), dt=None, icon='🕉️',
        title=('Spiritual Life Report', 'ஆன்மீக வாழ்க்கை அறிக்கை', 'ആത്മീയ ജീവിത റിപ്പോർട്ട്'),
        intro=('Dharma and faith from the 9th, liberation from the 12th, mantra and devotion from the 5th, with Jupiter and Ketu.',
               '9-ஆம் இடம் தர்மம், நம்பிக்கை; 12-ஆம் இடம் மோட்சம்; 5-ஆம் இடம் மந்திரம், பக்தி; குரு, கேது.',
               '9-ാം ഭാവം ധർമ്മം, വിശ്വാസം; 12-ാം ഭാവം മോക്ഷം; 5-ാം ഭാവം മന്ത്രം, ഭക്തി; വ്യാഴം, കേതു.'),
        when=('Periods for pilgrimage, study of scripture and inner growth', 'தீர்த்த யாத்திரை, சாஸ்திரக் கல்வி, அக வளர்ச்சிக்கான காலங்கள்',
              'തീർത്ഥയാത്ര, ശാസ്ത്രപഠനം, ആന്തരിക വളർച്ച എന്നിവയ്ക്കുള്ള കാലങ്ങൾ')),
}
VERDICT_WORDS = {  # (en, ta, ml) summing up the promise
    'good': ('The chart gives this area good support.', 'இந்தத் துறைக்கு ஜாதகம் நல்ல ஆதரவு தருகிறது.', 'ഈ മേഖലയ്ക്ക് ജാതകം നല്ല പിന്തുണ നൽകുന്നു.'),
    'mixed': ('The chart gives this area mixed support: results come with steady effort.',
              'இந்தத் துறைக்குக் கலப்பான ஆதரவு: நிலையான முயற்சியால் பலன் வரும்.',
              'ഈ മേഖലയ്ക്ക് സമ്മിശ്ര പിന്തുണ: സ്ഥിരമായ പ്രയത്നത്താൽ ഫലം വരും.'),
    'bad': ('This area needs patience and care; the remedies in the Parihara chapter help.',
            'இந்தத் துறையில் பொறுமையும் கவனமும் தேவை; பரிகார அத்தியாயம் உதவும்.',
            'ഈ മേഖലയിൽ ക്ഷമയും ശ്രദ്ധയും വേണം; പരിഹാര അധ്യായം സഹായിക്കും.'),
}


def _strength(planets, g):
    d = planets[g].get('dignity', 'Neutral')
    h = _house(planets, g)
    return DIGNITY_SCORE.get(d, 0) + (1 if h in KENDRAS + TRIKONAS + (11,) else (-1 if h in DUSTHANAS else 0))


def _lord_of(planets, house):
    return SIGN_LORDS[(planets['Ascendant']['sign_index'] + house - 1) % 12]


def _in(planets, house):
    sign = (planets['Ascendant']['sign_index'] + house - 1) % 12
    return [g for g in GRAHAS if planets[g]['sign_index'] == sign]


def _names(gs, lang):
    return {'en': lambda: ', '.join(gs), 'ta': lambda: ', '.join(PLANET_TAMIL[g] for g in gs), 'ml': lambda: _ml_list(gs)}[lang]()


def _promise(planets, spec):
    """The house, its lord, its occupants and aspects and the karakas: a verdict and the three texts."""
    h = spec['house']
    asc = planets['Ascendant']['sign_index']
    sign = (asc + h - 1) % 12
    lord = SIGN_LORDS[sign]
    occupants = _in(planets, h)
    aspects = [g for g in _aspecting(planets, sign) if g not in occupants]
    good = [g for g in occupants + aspects if g in BENEFICS]
    hard = [g for g in occupants + aspects if g in MALEFICS and g != lord]
    lh = _house(planets, lord)
    dig = planets[lord].get('dignity', 'Neutral')
    karaka_scores = [_strength(planets, k) for k in spec['karakas']]
    score = (DIGNITY_SCORE.get(dig, 0) + (1 if lh in KENDRAS + TRIKONAS + (11,) else (-1 if lh in DUSTHANAS else 0))
             + sum(karaka_scores) / len(karaka_scores) + len(good) - len(hard))
    verdict = 'good' if score >= 2 else ('bad' if score <= -1.5 else 'mixed')
    kar = lambda lang: '; '.join(
        {'en': f"{k} in house {_house(planets, k)}, {planets[k].get('dignity', 'Neutral').lower()}",
         'ta': f"{PLANET_TAMIL[k]} {_house(planets, k)}-ஆம் இடத்தில், {DIGNITY_TA.get(planets[k].get('dignity', 'Neutral'), '')}",
         'ml': f"{PLANET_ML[k]} {_house(planets, k)}-ാം ഭാവത്തിൽ, {DIGNITY_ML.get(planets[k].get('dignity', 'Neutral'), '')}"}[lang]
        for k in spec['karakas'])
    en = (f"The {_ordinal(h)} house is {SIGNS[sign]}, for {HOUSE_THEMES[h][0]}. Its lord {lord} is in house {lh} ({HOUSE_THEMES[lh][0]}), "
          f"{dig.lower()}. " + (f"In the house: {', '.join(occupants)}. " if occupants else 'No graha occupies it. ')
          + (f"Aspecting it: {', '.join(aspects)}. " if aspects else '') + f"Karakas: {kar('en')}. {VERDICT_WORDS[verdict][0]}")
    ta = (f"{h}-ஆம் இடம் {TAMIL_SIGNS[sign]}: {HOUSE_THEMES[h][1]}. அதன் அதிபதி {PLANET_TAMIL[lord]} {lh}-ஆம் இடத்தில் "
          f"({HOUSE_THEMES[lh][1]}), {DIGNITY_TA.get(dig, '')}. " + (f"இந்த இடத்தில்: {_names(occupants, 'ta')}. " if occupants else 'இந்த இடத்தில் கிரகம் இல்லை. ')
          + (f"பார்வை: {_names(aspects, 'ta')}. " if aspects else '') + f"காரகர்கள்: {kar('ta')}. {VERDICT_WORDS[verdict][1]}")
    ml = (f"{h}-ാം ഭാവം {MALAYALAM_SIGNS[sign]}: {HOUSE_THEMES_ML[h]}. അതിന്റെ അധിപൻ {PLANET_ML[lord]} {lh}-ാം ഭാവത്തിൽ "
          f"({HOUSE_THEMES_ML[lh]}), {_dig_ml(dig)}. " + (f"ഈ ഭാവത്തിൽ: {_ml_list(occupants)}. " if occupants else 'ഈ ഭാവത്തിൽ ഗ്രഹമില്ല. ')
          + (f"ദൃഷ്ടി: {_ml_list(aspects)}. " if aspects else '') + f"കാരകന്മാർ: {kar('ml')}. {VERDICT_WORDS[verdict][2]}")
    return verdict, (en, ta, ml), sign, lord, occupants


# ---- the classical combinations for each area: lists of (en, ta, ml) ----

def _yoga(chart, key):
    return next((y for y in chart.get('yogas') or [] if y.get('key') == key), None)


def notes_education(chart, planets):
    out = []
    if _yoga(chart, 'saraswati'):
        out.append(('Saraswati Yoga is present: learning, eloquence and skill in the arts come naturally.',
                    'சரஸ்வதி யோகம் உள்ளது: கல்வி, பேச்சாற்றல், கலைத் திறன் இயல்பாக அமையும்.',
                    'സരസ്വതീ യോഗമുണ്ട്: വിദ്യ, വാക്ചാതുര്യം, കലാവൈദഗ്ധ്യം എന്നിവ സ്വാഭാവികമായി ലഭിക്കും.'))
    merc, jup = _strength(planets, 'Mercury'), _strength(planets, 'Jupiter')
    if merc >= 2:
        out.append(('A strong Mercury gives a quick, analytical mind: mathematics, accounts, languages or computing suit you.',
                    'பலமான புதன் கூர்மையான பகுப்பாய்வு அறிவு தரும்: கணிதம், கணக்கியல், மொழிகள், கணினி பொருந்தும்.',
                    'ബലമുള്ള ബുധൻ വേഗമേറിയ വിശകലനബുദ്ധി നൽകും: ഗണിതം, അക്കൗണ്ടിംഗ്, ഭാഷകൾ, കമ്പ്യൂട്ടർ എന്നിവ യോജിക്കും.'))
    elif merc <= -1 or planets['Mercury'].get('combust'):
        out.append(('Mercury is weak or close to the Sun: studies need steady routine and revision rather than last-minute effort.',
                    'புதன் பலவீனம் அல்லது சூரியனுக்கு அருகில்: கடைசி நேர முயற்சியை விட ஒழுங்கான படிப்பும் மீள்பார்வையும் தேவை.',
                    'ബുധൻ ദുർബലനോ സൂര്യനോട് അടുത്തോ ആണ്: അവസാന നിമിഷ പ്രയത്നത്തേക്കാൾ ക്രമമായ പഠനവും ആവർത്തനവും വേണം.'))
    if jup >= 2:
        out.append(('A strong Jupiter supports higher studies, teaching, law or philosophy, and the guidance of good teachers.',
                    'பலமான குரு உயர்கல்வி, ஆசிரியப் பணி, சட்டம், தத்துவம், நல்ல ஆசிரியர்களின் வழிகாட்டுதலுக்குத் துணை.',
                    'ബലമുള്ള വ്യാഴം ഉന്നത വിദ്യാഭ്യാസം, അധ്യാപനം, നിയമം, തത്ത്വചിന്ത, നല്ല ഗുരുക്കന്മാരുടെ മാർഗ്ഗനിർദ്ദേശം എന്നിവയ്ക്ക് പിന്തുണ.'))
    l5 = _lord_of(planets, 5)
    h5 = _house(planets, l5)
    if h5 in DUSTHANAS:
        out.append((f"The 5th lord {l5} in house {h5}: studies may see breaks or a change of stream before they settle.",
                    f"5-ஆம் அதிபதி {PLANET_TAMIL[l5]} {h5}-ஆம் இடத்தில்: படிப்பில் இடைவெளி அல்லது துறை மாற்றம் வரலாம்.",
                    f"5-ാം അധിപൻ {PLANET_ML[l5]} {h5}-ാം ഭാവത്തിൽ: പഠനത്തിൽ ഇടവേളയോ വിഷയമാറ്റമോ വരാം."))
    elif h5 in KENDRAS + TRIKONAS:
        out.append((f"The 5th lord {l5} in house {h5}: a sound intellect that learns well.",
                    f"5-ஆம் அதிபதி {PLANET_TAMIL[l5]} {h5}-ஆம் இடத்தில்: நன்கு கற்கும் தெளிவான அறிவு.",
                    f"5-ാം അധിപൻ {PLANET_ML[l5]} {h5}-ാം ഭാവത്തിൽ: നന്നായി പഠിക്കുന്ന തെളിഞ്ഞ ബുദ്ധി."))
    if any(g in ('Rahu', 'Ketu') for g in _in(planets, 9) + _in(planets, 12)) or _house(planets, _lord_of(planets, 9)) == 12:
        out.append(('Rahu or Ketu on the 9th or 12th, or the 9th lord in the 12th: study abroad or in an unusual, technical field.',
                    '9 அல்லது 12-இல் ராகு/கேது, அல்லது 9-ஆம் அதிபதி 12-இல்: வெளிநாட்டுப் படிப்பு அல்லது தனித்துவமான, தொழில்நுட்பத் துறை.',
                    '9-ലോ 12-ലോ രാഹു/കേതു, അല്ലെങ്കിൽ 9-ാം അധിപൻ 12-ൽ: വിദേശ പഠനം അല്ലെങ്കിൽ അസാധാരണ, സാങ്കേതിക മേഖല.'))
    if [g for g in _in(planets, 4) if g in ('Saturn', 'Rahu', 'Ketu', 'Mars')]:
        out.append(('A malefic in the 4th: schooling may have been disturbed or changed schools; persistence pays.',
                    '4-இல் பாப கிரகம்: பள்ளிக் கல்வியில் இடையூறு அல்லது பள்ளி மாற்றம் இருந்திருக்கலாம்; விடாமுயற்சி பலன் தரும்.',
                    '4-ൽ പാപഗ്രഹം: സ്കൂൾ വിദ്യാഭ്യാസത്തിൽ തടസ്സമോ സ്കൂൾ മാറ്റമോ ഉണ്ടായിരിക്കാം; സ്ഥിരോത്സാഹം ഫലം നൽകും.'))
    return out


FERTILE, LESS_FERTILE = (3, 7, 11), (2, 4, 5)  # watery signs; Gemini, Leo, Virgo (alpa-putra signs)


def notes_children(chart, planets, jaimini):
    out = []
    sign5 = (planets['Ascendant']['sign_index'] + 4) % 12
    in5 = _in(planets, 5)
    if 'Jupiter' in in5:
        out.append(('Jupiter, the karaka of children, in the 5th: children come, though often after some delay (karako bhava nashaya).',
                    'புத்திரகாரகன் குரு 5-இல்: குழந்தைப் பேறு உண்டு, ஆனால் சற்றுத் தாமதமாகலாம் (காரகோ பாவ நாசாய).',
                    'പുത്രകാരകനായ വ്യാഴം 5-ൽ: സന്താനഭാഗ്യമുണ്ട്, എന്നാൽ അല്പം വൈകാം (കാരകോ ഭാവ നാശായ).'))
    harsh = [g for g in in5 if g in ('Saturn', 'Rahu', 'Ketu', 'Mars')]
    if harsh:
        out.append((f"{', '.join(harsh)} in the 5th: children may be delayed or need medical care; timely treatment and remedies help.",
                    f"5-இல் {_names(harsh, 'ta')}: குழந்தைப் பேறு தாமதமாகலாம் அல்லது மருத்துவ உதவி தேவைப்படலாம்; உரிய சிகிச்சையும் பரிகாரமும் உதவும்.",
                    f"5-ൽ {_ml_list(harsh)}: സന്താനലബ്ധി വൈകാം അല്ലെങ്കിൽ വൈദ്യസഹായം വേണ്ടിവരാം; യഥാസമയ ചികിത്സയും പരിഹാരവും സഹായിക്കും."))
    if sign5 in FERTILE:
        out.append((f"The 5th is {SIGNS[sign5]}, a watery sign that classical texts call fruitful for children.",
                    f"5-ஆம் இடம் {TAMIL_SIGNS[sign5]}, புத்திர பாக்கியத்துக்குச் சாதகமான ஜல ராசி.",
                    f"5-ാം ഭാവം {MALAYALAM_SIGNS[sign5]}, സന്താനഭാഗ്യത്തിന് അനുകൂലമായ ജലരാശി."))
    elif sign5 in LESS_FERTILE:
        out.append((f"The 5th is {SIGNS[sign5]}, which classical texts count among the signs of few children.",
                    f"5-ஆம் இடம் {TAMIL_SIGNS[sign5]}, குறைவான குழந்தைகளைக் குறிக்கும் ராசிகளில் ஒன்று.",
                    f"5-ാം ഭാവം {MALAYALAM_SIGNS[sign5]}, കുറഞ്ഞ സന്താനങ്ങളെ സൂചിപ്പിക്കുന്ന രാശികളിൽ ഒന്ന്."))
    pk = _karaka(jaimini, 'PK')
    if pk:
        out.append((f"The Jaimini Putrakaraka is {pk}, in house {_house(planets, pk)}; its periods also bring news of children.",
                    f"ஜைமினி புத்திரகாரகன் {PLANET_TAMIL[pk]}, {_house(planets, pk)}-ஆம் இடத்தில்; அதன் காலங்களிலும் குழந்தைச் செய்தி வரும்.",
                    f"ജൈമിനി പുത്രകാരകൻ {PLANET_ML[pk]}, {_house(planets, pk)}-ാം ഭാവത്തിൽ; അതിന്റെ കാലങ്ങളിലും സന്താനവാർത്ത വരും."))
    return out


def notes_health(chart, planets, pred):
    out = []
    ll = _lord_of(planets, 1)
    s = _strength(planets, ll)
    out.append((f"The Lagna lord {ll} is {'strong' if s >= 1 else 'weak' if s <= -1 else 'moderate'}: "
                + ('good vitality and recovery.' if s >= 1 else 'guard energy with rest and routine.' if s <= -1 else 'average vitality.'),
                f"லக்னாதிபதி {PLANET_TAMIL[ll]} {'பலமாக' if s >= 1 else 'பலவீனமாக' if s <= -1 else 'மிதமாக'} உள்ளார்: "
                + ('நல்ல உயிர்ச்சக்தி, விரைவான குணம்.' if s >= 1 else 'ஓய்வும் ஒழுங்கும் மூலம் சக்தியைக் காக்கவும்.' if s <= -1 else 'சராசரி உயிர்ச்சக்தி.'),
                f"ലഗ്നാധിപൻ {PLANET_ML[ll]} {'ബലവാൻ' if s >= 1 else 'ദുർബലൻ' if s <= -1 else 'മിതബലൻ'}: "
                + ('നല്ല ജീവശക്തി, വേഗത്തിലുള്ള രോഗശാന്തി.' if s >= 1 else 'വിശ്രമവും ക്രമവും കൊണ്ട് ഊർജ്ജം കാക്കുക.' if s <= -1 else 'ശരാശരി ജീവശക്തി.')))
    for h in (1, 6, 8):
        for g in _in(planets, h):
            if g in MALEFICS:
                b = BODY[g]
                out.append((f"{g} in the {_ordinal(h)}: watch {b[0]}.",
                            f"{h}-இல் {PLANET_TAMIL[g]}: {b[1]} கவனம்.", f"{h}-ൽ {PLANET_ML[g]}: {b[2]} ശ്രദ്ധിക്കുക."))
    moon_with = [g for g in ('Saturn', 'Rahu', 'Ketu') if planets[g]['sign_index'] == planets['Moon']['sign_index']]
    if moon_with:
        out.append((f"The Moon with {', '.join(moon_with)}: stress and sleep need attention; meditation and regular hours help.",
                    f"சந்திரனுடன் {_names(moon_with, 'ta')}: மன அழுத்தம், தூக்கத்தில் கவனம்; தியானமும் ஒழுங்கான நேரமும் உதவும்.",
                    f"ചന്ദ്രനോടൊപ്പം {_ml_list(moon_with)}: മാനസിക സമ്മർദ്ദത്തിലും ഉറക്കത്തിലും ശ്രദ്ധ; ധ്യാനവും ക്രമമായ സമയവും സഹായിക്കും."))
    ayur = (pred or {}).get('ayur_jyotish') or {}
    if ayur.get('anatomical_vulnerabilities_en'):
        out.append((f"From the 6th house sign: {ayur['anatomical_vulnerabilities_en'].lower()}.",
                    f"6-ஆம் இட ராசியின்படி: {ayur.get('anatomical_vulnerabilities_ta', '')}.",
                    f"6-ാം ഭാവ രാശി പ്രകാരം: {ayur.get('anatomical_vulnerabilities_ml', '')}."))
    if ayur.get('prakriti_en'):
        out.append((f"Constitution {ayur['prakriti_en']}: see Ayur-Jyotish for diet and routine.",
                    f"உடல் அமைப்பு {ayur.get('prakriti_ta', '')}: உணவு, நடைமுறைக்கு ஆயுர்-ஜோதிடம் பார்க்கவும்.",
                    f"ശരീരപ്രകൃതി {ayur.get('prakriti_ml', '')}: ഭക്ഷണത്തിനും ദിനചര്യയ്ക്കും ആയുർ-ജ്യോതിഷം കാണുക."))
    return out


def notes_wealth(chart, planets):
    out = []
    for key, en, ta, ml in (('lakshmi', 'Lakshmi Yoga', 'லட்சுமி யோகம்', 'ലക്ഷ്മീ യോഗം'), ('dhana', 'Dhana Yoga', 'தன யோகம்', 'ധന യോഗം')):
        if _yoga(chart, key):
            out.append((f"{en} is present: wealth grows through the grahas that form it.",
                        f"{ta} உள்ளது: அதை அமைக்கும் கிரகங்கள் வழியாகச் செல்வம் வளரும்.",
                        f"{ml} ഉണ്ട്: അത് രൂപപ്പെടുത്തുന്ന ഗ്രഹങ്ങളിലൂടെ സമ്പത്ത് വളരും."))
    l2, l11 = _lord_of(planets, 2), _lord_of(planets, 11)
    if l2 != l11 and (planets[l2]['sign_index'] == planets[l11]['sign_index']
                      or (_house(planets, l2) == 11 and _house(planets, l11) == 2)):
        out.append((f"The 2nd and 11th lords ({l2}, {l11}) are joined or exchanged: a classic Dhana link between income and savings.",
                    f"2, 11-ஆம் அதிபதிகள் ({PLANET_TAMIL[l2]}, {PLANET_TAMIL[l11]}) சேர்ந்து அல்லது பரிவர்த்தனையில்: வருமானம்-சேமிப்பு தன இணைப்பு.",
                    f"2, 11-ാം അധിപന്മാർ ({PLANET_ML[l2]}, {PLANET_ML[l11]}) ഒന്നിച്ചോ പരിവർത്തനത്തിലോ: വരുമാനവും സമ്പാദ്യവും തമ്മിലുള്ള ധനബന്ധം."))
    for lord, h in ((l2, 2), (l11, 11)):
        if _house(planets, lord) == 12:
            out.append((f"The {_ordinal(h)} lord {lord} in the 12th: money flows out as easily as it comes; budget and invest regularly.",
                        f"{h}-ஆம் அதிபதி {PLANET_TAMIL[lord]} 12-இல்: வந்த வேகத்தில் பணம் செலவாகும்; திட்டமிட்டுச் சேமிக்கவும்.",
                        f"{h}-ാം അധിപൻ {PLANET_ML[lord]} 12-ൽ: വരുന്ന വേഗത്തിൽ പണം ചെലവാകും; ആസൂത്രണം ചെയ്ത് സമ്പാദിക്കുക."))
    l4 = _lord_of(planets, 4)
    if _strength(planets, l4) >= 1 and _strength(planets, 'Mars') >= 0:
        out.append((f"The 4th lord {l4} and Mars are well placed: owning land or a house is well supported.",
                    f"4-ஆம் அதிபதி {PLANET_TAMIL[l4]}, செவ்வாய் நல்ல நிலையில்: நிலம், வீடு வாங்கும் யோகம் நன்று.",
                    f"4-ാം അധിപൻ {PLANET_ML[l4]}, ചൊവ്വ എന്നിവ നല്ല നിലയിൽ: ഭൂമി, വീട് സ്വന്തമാക്കാനുള്ള യോഗം നല്ലത്."))
    if 'Saturn' in _in(planets, 4):
        out.append(('Saturn in the 4th: property comes through patient effort, often an older or ancestral house.',
                    '4-இல் சனி: பொறுமையான முயற்சியால் சொத்து; பெரும்பாலும் பழைய அல்லது பூர்வீக வீடு.',
                    '4-ൽ ശനി: ക്ഷമയോടെയുള്ള പ്രയത്നത്താൽ സ്വത്ത്; പലപ്പോഴും പഴയതോ പൂർവ്വികമോ ആയ വീട്.'))
    if _strength(planets, 'Venus') >= 2:
        out.append(('A strong Venus brings vehicles, comforts and a well-furnished home.',
                    'பலமான சுக்கிரன் வாகனம், சுகம், அழகான இல்லம் தரும்.',
                    'ബലമുള്ള ശുക്രൻ വാഹനം, സുഖസൗകര്യങ്ങൾ, നന്നായി സജ്ജീകരിച്ച വീട് എന്നിവ നൽകും.'))
    return out


MOVABLE = (0, 3, 6, 9)


def notes_foreign(chart, planets):
    out = []
    l12, l9 = _lord_of(planets, 12), _lord_of(planets, 9)
    if _house(planets, l12) in (9, 12) or _house(planets, l9) == 12:
        out.append(('The 12th and 9th lords are linked with each other\'s houses: work or settlement abroad is strongly indicated.',
                    '12, 9-ஆம் அதிபதிகள் ஒருவர் இடத்தில் மற்றவர்: வெளிநாட்டில் பணி அல்லது குடியேற்றம் வலுவாகச் சுட்டப்படுகிறது.',
                    '12, 9-ാം അധിപന്മാർ പരസ്പരം ഭാവങ്ങളിൽ ബന്ധപ്പെട്ടിരിക്കുന്നു: വിദേശ ജോലിയോ താമസമോ ശക്തമായി സൂചിപ്പിക്കുന്നു.'))
    rh = _house(planets, 'Rahu')
    if rh in (1, 3, 7, 9, 10, 12):
        out.append((f"Rahu in the {_ordinal(rh)} links you with foreign lands, cultures or companies.",
                    f"{rh}-இல் ராகு: வெளிநாடு, பிற பண்பாடு அல்லது நிறுவனங்களுடன் தொடர்பு.",
                    f"{rh}-ൽ രാഹു: വിദേശം, മറ്റ് സംസ്കാരങ്ങൾ, സ്ഥാപനങ്ങൾ എന്നിവയുമായി ബന്ധം."))
    if _house(planets, 'Moon') == 12 or _house(planets, _lord_of(planets, 1)) == 12:
        out.append(('The Moon or the Lagna lord in the 12th: much of life is spent away from the place of birth.',
                    'சந்திரன் அல்லது லக்னாதிபதி 12-இல்: வாழ்வின் பெரும்பகுதி பிறந்த ஊரிலிருந்து தொலைவில்.',
                    'ചന്ദ്രനോ ലഗ്നാധിപനോ 12-ൽ: ജീവിതത്തിന്റെ വലിയൊരു ഭാഗം ജന്മസ്ഥലത്തു നിന്ന് അകലെ.'))
    if planets['Ascendant']['sign_index'] in MOVABLE:
        out.append((f"A movable Lagna ({SIGNS[planets['Ascendant']['sign_index']]}) favours travel and change of place.",
                    f"சர லக்னம் ({TAMIL_SIGNS[planets['Ascendant']['sign_index']]}) பயணத்துக்கும் இட மாற்றத்துக்கும் சாதகம்.",
                    f"ചര ലഗ്നം ({MALAYALAM_SIGNS[planets['Ascendant']['sign_index']]}) യാത്രയ്ക്കും സ്ഥലംമാറ്റത്തിനും അനുകൂലം."))
    if [g for g in _in(planets, 4) if g in ('Saturn', 'Rahu', 'Ketu')]:
        out.append(('A malefic in the 4th weakens ties to the home town, which also favours living elsewhere.',
                    '4-இல் பாப கிரகம் சொந்த ஊர்ப் பிணைப்பைக் குறைக்கும்; வேறிடத்தில் வாழவும் சாதகம்.',
                    '4-ൽ പാപഗ്രഹം ജന്മനാടുമായുള്ള ബന്ധം കുറയ്ക്കും; മറ്റൊരിടത്ത് ജീവിക്കാനും അനുകൂലം.'))
    return out


def notes_spiritual(chart, planets):
    out = []
    if _house(planets, 'Ketu') == 12:
        out.append(('Ketu in the 12th: a classical sign of moksha, detachment and deep meditation.',
                    '12-இல் கேது: மோட்சம், பற்றின்மை, ஆழ்ந்த தியானத்தின் பாரம்பரிய அறிகுறி.',
                    '12-ൽ കേതു: മോക്ഷം, നിസ്സംഗത, ആഴത്തിലുള്ള ധ്യാനം എന്നിവയുടെ പരമ്പരാഗത ലക്ഷണം.'))
    jh = _house(planets, 'Jupiter')
    if jh in (1, 5, 9, 12):
        out.append((f"Jupiter in the {_ordinal(jh)}: faith, study of scripture and respect for teachers run through life.",
                    f"{jh}-இல் குரு: நம்பிக்கை, சாஸ்திரக் கல்வி, குருபக்தி வாழ்நாள் முழுதும்.",
                    f"{jh}-ൽ വ്യാഴം: വിശ്വാസം, ശാസ്ത്രപഠനം, ഗുരുഭക്തി ജീവിതത്തിലുടനീളം."))
    l9 = _lord_of(planets, 9)
    if _strength(planets, l9) >= 1:
        out.append((f"A strong 9th lord ({l9}): blessings of dharma, pilgrimages and a helpful guru.",
                    f"பலமான 9-ஆம் அதிபதி ({PLANET_TAMIL[l9]}): தர்ம பலம், தீர்த்த யாத்திரை, உதவும் குரு.",
                    f"ബലമുള്ള 9-ാം അധിപൻ ({PLANET_ML[l9]}): ധർമ്മബലം, തീർത്ഥയാത്ര, സഹായിക്കുന്ന ഗുരു."))
    moksha = [g for h in (4, 8, 12) for g in _in(planets, h)]
    if len(moksha) >= 3:
        out.append((f"Several grahas in the moksha houses 4, 8 and 12 ({', '.join(moksha)}): an inward-looking, seeking nature.",
                    f"மோட்ச இடங்களான 4, 8, 12-இல் பல கிரகங்கள் ({_names(moksha, 'ta')}): அகநோக்கும் தேடலும் உள்ள இயல்பு.",
                    f"മോക്ഷ ഭാവങ്ങളായ 4, 8, 12-ൽ പല ഗ്രഹങ്ങൾ ({_ml_list(moksha)}): ഉള്ളിലേക്ക് നോക്കുന്ന, അന്വേഷിക്കുന്ന സ്വഭാവം."))
    if 'Saturn' in _aspecting(planets, planets['Moon']['sign_index']) or planets['Saturn']['sign_index'] == planets['Moon']['sign_index']:
        out.append(('Saturn joins or aspects the Moon: a serious, renouncing streak that deepens with age.',
                    'சனி சந்திரனுடன் சேர்க்கை அல்லது பார்வை: வயதுடன் ஆழமாகும் துறவு மனப்பான்மை.',
                    'ശനി ചന്ദ്രനോടൊപ്പമോ ദൃഷ്ടിയിലോ: പ്രായത്തോടൊപ്പം ആഴമേറുന്ന വൈരാഗ്യഭാവം.'))
    return out


def _significators(planets, spec, extra=()):
    lords = {_lord_of(planets, h) for h in spec['houses']}
    tenants = {g for h in spec['houses'] for g in _in(planets, h)}
    return lords | tenants | set(spec['karakas']) | set(extra)


def calculate_life_area(key, chart, jaimini=None, double_transit=None, ayur=None, now=None):
    spec = AREAS[key]
    now = now or datetime.now(timezone.utc)
    planets = chart['planets']
    pred = dict(ayur_jyotish=ayur) if ayur else (chart.get('predictions') or {})
    verdict, promise, sign, lord, occupants = _promise(planets, spec)
    notes = {'education': lambda: notes_education(chart, planets),
             'children': lambda: notes_children(chart, planets, jaimini),
             'health': lambda: notes_health(chart, planets, pred),
             'wealth': lambda: notes_wealth(chart, planets),
             'foreign': lambda: notes_foreign(chart, planets),
             'spiritual': lambda: notes_spiritual(chart, planets)}[key]()
    if key == 'health':
        significators = ({_lord_of(planets, h) for h in (6, 8, 12)}
                         | {g for h in (1, 6, 8) for g in _in(planets, h) if g in MALEFICS})
    else:
        extra = ('Mars',) if key == 'wealth' else ()
        pk = _karaka(jaimini, 'PK') if key == 'children' else None
        significators = _significators(planets, spec, extra + ((pk,) if pk else ()))
    windows = period_windows(chart.get('dasha') or [], significators, now)
    dt = _dt_windows(double_transit, spec['dt']) if spec['dt'] else []
    title, intro, when = spec['title'], spec['intro'], spec['when']
    sig_names = sorted(significators)
    cards = [card(spec['icon'], f"The {_ordinal(spec['house'])} house: {SIGNS[sign]}",
                  f"{spec['house']}-ஆம் இடம்: {TAMIL_SIGNS[sign]}", promise[0], promise[1], verdict=verdict,
                  title_ml=f"{spec['house']}-ാം ഭാവം: {MALAYALAM_SIGNS[sign]}", body_ml=promise[2])]
    if notes:
        cards.append(card('📜', 'Classical indications', 'பாரம்பரியக் குறிப்புகள்',
                          ' '.join(n[0] for n in notes), ' '.join(n[1] for n in notes),
                          title_ml='പരമ്പരാഗത സൂചനകൾ', body_ml=' '.join(n[2] for n in notes)))
    care = key == 'health'
    cards.append(card(
        '⏳', when[0], when[1],
        ((f"Periods ruled by {', '.join(sig_names)} are listed below; "
          + ('keep up check-ups and rest then, the more so when both lords are listed.' if care
             else 'the strongest are those where both the Dasa and Bhukti lords signify this area.'))
         if windows else 'No strongly marked period falls in the coming years.')
        + (f" Saturn and Jupiter together activate the house (double transit) in {len(dt)} window(s) ahead." if dt else ''),
        ((f"{_names(sig_names, 'ta')} ஆளும் காலங்கள் கீழே; "
          + ('அப்போது பரிசோதனையும் ஓய்வும் தொடரவும்; இரு அதிபதிகளும் இருந்தால் கூடுதல் கவனம்.' if care
             else 'தசா, புக்தி அதிபதிகள் இருவரும் இத்துறையைக் குறித்தால் வலுவானவை.'))
         if windows else 'வரும் ஆண்டுகளில் தெளிவான காலம் இல்லை.')
        + (f" சனியும் குருவும் சேர்ந்து இந்த இடத்தைத் தூண்டும் (இரட்டைக் கோச்சாரம்) காலங்கள்: {len(dt)}." if dt else ''),
        verdict='mixed' if care else None, title_ml=when[2],
        body_ml=((f"{_ml_list(sig_names)} ഭരിക്കുന്ന കാലങ്ങൾ താഴെ; "
                  + ('അപ്പോൾ പരിശോധനയും വിശ്രമവും തുടരുക; രണ്ട് അധിപന്മാരും ഉണ്ടെങ്കിൽ കൂടുതൽ ശ്രദ്ധ.' if care
                     else 'ദശ, ഭുക്തി അധിപന്മാർ രണ്ടും ഈ മേഖലയെ സൂചിപ്പിക്കുമ്പോൾ അവ ശക്തം.'))
                 if windows else 'വരുന്ന വർഷങ്ങളിൽ വ്യക്തമായ കാലമില്ല.')
        + (f" ശനിയും വ്യാഴവും ചേർന്ന് ഈ ഭാവത്തെ ഉണർത്തുന്ന (ഇരട്ട ഗോചരം) കാലങ്ങൾ: {len(dt)}." if dt else '')))
    return chapter(
        key, title[0], title[1], intro[0], intro[1], cards=cards,
        tables=[table(when[0], when[1], WINDOW_HEAD, _window_rows(windows), title_ml=when[2])],
        title_ml=title[2], intro_ml=intro[2],
        significators=sig_names, windows=windows, verdict=verdict)


LIFE_AREA_KEYS = tuple(AREAS)
