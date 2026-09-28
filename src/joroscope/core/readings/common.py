"""Shared vocabulary for the readings: signs, lords, Tamil and Malayalam names, dignity and house
themes, and the helpers that describe a graha's house lordship and functional role.
"""

SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
TAMIL_SIGNS = ['மேஷம்', 'ரிஷபம்', 'மிதுனம்', 'கடகம்', 'சிம்மம்', 'கன்னி', 'துலாம்', 'விருச்சிகம்', 'தனுசு', 'மகரம்', 'கும்பம்', 'மீனம்']
SIGN_LORDS = ['Mars', 'Venus', 'Mercury', 'Moon', 'Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Saturn', 'Jupiter']
PLANET_TAMIL = {
    'Sun': 'சூரியன்', 'Moon': 'சந்திரன்', 'Mars': 'செவ்வாய்', 'Mercury': 'புதன்',
    'Jupiter': 'குரு', 'Venus': 'சுக்கிரன்', 'Saturn': 'சனி', 'Rahu': 'ராகு', 'Ketu': 'கேது',
    'Ascendant': 'லக்னம்'
}
MALAYALAM_SIGNS = ['മേടം', 'ഇടവം', 'മിഥുനം', 'കർക്കടകം', 'ചിങ്ങം', 'കന്നി', 'തുലാം', 'വൃശ്ചികം', 'ധനു', 'മകരം', 'കുംഭം', 'മീനം']
PLANET_ML = {
    'Sun': 'സൂര്യൻ', 'Moon': 'ചന്ദ്രൻ', 'Mars': 'ചൊവ്വ', 'Mercury': 'ബുധൻ', 'Jupiter': 'വ്യാഴം', 'Venus': 'ശുക്രൻ',
    'Saturn': 'ശനി', 'Rahu': 'രാഹു', 'Ketu': 'കേതു', 'Ascendant': 'ലഗ്നം'
}
# Malayalam inflects names: the case forms of each graha, so sentences never glue a suffix to a name
PLANET_ML_CASE = {
    'dat': {'Sun': 'സൂര്യന്', 'Moon': 'ചന്ദ്രന്', 'Mars': 'ചൊവ്വയ്ക്ക്', 'Mercury': 'ബുധന്', 'Jupiter': 'വ്യാഴത്തിന്',
            'Venus': 'ശുക്രന്', 'Saturn': 'ശനിക്ക്', 'Rahu': 'രാഹുവിന്', 'Ketu': 'കേതുവിന്'},
    'acc': {'Sun': 'സൂര്യനെ', 'Moon': 'ചന്ദ്രനെ', 'Mars': 'ചൊവ്വയെ', 'Mercury': 'ബുധനെ', 'Jupiter': 'വ്യാഴത്തെ',
            'Venus': 'ശുക്രനെ', 'Saturn': 'ശനിയെ', 'Rahu': 'രാഹുവിനെ', 'Ketu': 'കേതുവിനെ'},
    'loc': {'Sun': 'സൂര്യനിൽ', 'Moon': 'ചന്ദ്രനിൽ', 'Mars': 'ചൊവ്വയിൽ', 'Mercury': 'ബുധനിൽ', 'Jupiter': 'വ്യാഴത്തിൽ',
            'Venus': 'ശുക്രനിൽ', 'Saturn': 'ശനിയിൽ', 'Rahu': 'രാഹുവിൽ', 'Ketu': 'കേതുവിൽ'},
    'gen': {'Sun': 'സൂര്യന്റെ', 'Moon': 'ചന്ദ്രന്റെ', 'Mars': 'ചൊവ്വയുടെ', 'Mercury': 'ബുധന്റെ', 'Jupiter': 'വ്യാഴത്തിന്റെ',
            'Venus': 'ശുക്രന്റെ', 'Saturn': 'ശനിയുടെ', 'Rahu': 'രാഹുവിന്റെ', 'Ketu': 'കേതുവിന്റെ'},
}
MALAYALAM_STARS = [
    'അശ്വതി', 'ഭരണി', 'കാർത്തിക', 'രോഹിണി', 'മകയിരം', 'തിരുവാതിര', 'പുണർതം', 'പൂയം', 'ആയില്യം', 'മകം', 'പൂരം', 'ഉത്രം',
    'അത്തം', 'ചിത്തിര', 'ചോതി', 'വിശാഖം', 'അനിഴം', 'തൃക്കേട്ട', 'മൂലം', 'പൂരാടം', 'ഉത്രാടം', 'തിരുവോണം', 'അവിട്ടം', 'ചതയം',
    'പൂരുരുട്ടാതി', 'ഉത്രട്ടാതി', 'രേവതി'
]
# Shared vocabulary for the chart-specific readings below
NATURAL_BENEFICS = ('Jupiter', 'Venus', 'Mercury', 'Moon')
KENDRAS, TRIKONAS, DUSTHANAS, UPACHAYAS = (1, 4, 7, 10), (1, 5, 9), (6, 8, 12), (3, 6, 10, 11)
DIG_BALA_HOUSE = {'Sun': 10, 'Mars': 10, 'Jupiter': 1, 'Mercury': 1, 'Moon': 4, 'Venus': 4, 'Saturn': 7}
DIGNITY_SCORE = {'Exalted': 2, 'Own Sign': 2, 'Moolatrikona': 2, 'Great Friend': 1, 'Friend': 1,
                 'Neutral': 0, 'Enemy': -1, 'Great Enemy': -1, 'Debilitated': -2}
DIGNITY_PHRASE = {
    'Exalted': ('exaltation', 'உச்ச நிலையில்'), 'Own Sign': ('its own sign', 'ஆட்சி வீட்டில்'),
    'Moolatrikona': ('its moolatrikona sign', 'மூலத்திரிகோண வீட்டில்'),
    'Great Friend': ("a great friend's sign", 'அதி நட்பு வீட்டில்'), 'Friend': ("a friend's sign", 'நட்பு வீட்டில்'),
    'Neutral': ('a neutral sign', 'சம வீட்டில்'), 'Enemy': ("an enemy's sign", 'பகை வீட்டில்'),
    'Great Enemy': ("a great enemy's sign", 'அதி பகை வீட்டில்'), 'Debilitated': ('debilitation', 'நீச நிலையில்')
}
DIGNITY_PHRASE_ML = {
    'Exalted': 'ഉച്ചത്തിൽ', 'Own Sign': 'സ്വക്ഷേത്രത്തിൽ', 'Moolatrikona': 'മൂലത്രികോണത്തിൽ', 'Great Friend': 'അതിമിത്ര ക്ഷേത്രത്തിൽ',
    'Friend': 'മിത്ര ക്ഷേത്രത്തിൽ', 'Neutral': 'സമ ക്ഷേത്രത്തിൽ', 'Enemy': 'ശത്രു ക്ഷേത്രത്തിൽ', 'Great Enemy': 'അതിശത്രു ക്ഷേത്രത്തിൽ',
    'Debilitated': 'നീചത്തിൽ'
}
HOUSE_THEMES = {
    1: ('health, personality and life direction', 'உடல்நலம், ஆளுமை, வாழ்க்கைப் பாதை'),
    2: ('wealth, family and speech', 'செல்வம், குடும்பம், வாக்கு'),
    3: ('courage, siblings and initiative', 'தைரியம், உடன்பிறப்புகள், முயற்சி'),
    4: ('mother, home, property and peace of mind', 'தாய், வீடு, சொத்து, மன நிம்மதி'),
    5: ('children, intelligence and past merit', 'குழந்தைகள், அறிவு, பூர்வ புண்ணியம்'),
    6: ('health battles, debts, rivals and service', 'நோய், கடன், எதிரிகள், சேவை'),
    7: ('marriage, partnerships and public dealings', 'திருமணம், கூட்டாண்மை, பொது உறவுகள்'),
    8: ('longevity, sudden events and hidden matters', 'ஆயுள், திடீர் நிகழ்வுகள், மறைவான விஷயங்கள்'),
    9: ('fortune, father, dharma and higher learning', 'பாக்கியம், தந்தை, தர்மம், உயர்கல்வி'),
    10: ('career, status and authority', 'தொழில், அந்தஸ்து, அதிகாரம்'),
    11: ('gains, income and fulfilled wishes', 'லாபம், வருமானம், ஆசைகள் நிறைவேறுதல்'),
    12: ('expenses, foreign lands, sleep and liberation', 'செலவுகள், வெளிநாடு, உறக்கம், மோட்சம்')
}
VERDICT_TAMIL = {'strong': 'பலம் வாய்ந்தது', 'moderate': 'மத்திமம்', 'weak': 'கவனம் தேவை'}
HOUSE_THEMES_ML = {
    1: 'ആരോഗ്യം, വ്യക്തിത്വം, ജീവിതദിശ', 2: 'ധനം, കുടുംബം, വാക്ക്', 3: 'ധൈര്യം, സഹോദരങ്ങൾ, പ്രയത്നം',
    4: 'അമ്മ, വീട്, സ്വത്ത്, മനസ്സമാധാനം', 5: 'സന്താനം, ബുദ്ധി, പൂർവ്വപുണ്യം', 6: 'രോഗം, കടം, ശത്രുക്കൾ, സേവനം',
    7: 'വിവാഹം, പങ്കാളിത്തം, പൊതുബന്ധങ്ങൾ', 8: 'ആയുസ്സ്, ആകസ്മിക സംഭവങ്ങൾ, രഹസ്യ കാര്യങ്ങൾ',
    9: 'ഭാഗ്യം, അച്ഛൻ, ധർമ്മം, ഉന്നത വിദ്യ', 10: 'തൊഴിൽ, പദവി, അധികാരം', 11: 'ലാഭം, വരുമാനം, ആഗ്രഹസാഫല്യം',
    12: 'ചെലവ്, വിദേശം, ഉറക്കം, മോക്ഷം'
}
VERDICT_ML = {'strong': 'ബലവത്ത്', 'moderate': 'മധ്യമം', 'weak': 'ശ്രദ്ധ വേണം'}


def _ordinal(n):
    return f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


def _house_list(houses, lang):
    if lang == 'ml':
        return ', '.join(f'{h}-ാം' for h in houses) + ' ഭാവങ്ങൾ' if len(houses) > 1 else f'{houses[0]}-ാം ഭാവം'
    if lang == 'ta':
        return ', '.join(f'{h}-ம்' for h in houses) + ' பாவங்கள்' if len(houses) > 1 else f'{houses[0]}-ம் பாவம்'
    words = [_ordinal(h) for h in houses]
    return (' and '.join(words) if len(words) < 3 else ', '.join(words[:-1]) + ' and ' + words[-1]) + (' houses' if len(words) > 1 else ' house')


def _verdict(score, strong_at=3):
    return 'strong' if score >= strong_at else ('weak' if score <= -1 else 'moderate')


def _owned_houses(planet, asc_sign):
    """Houses (from the Lagna) whose sign this planet rules; none for the nodes."""
    return [h for h in range(1, 13) if SIGN_LORDS[(asc_sign + h - 1) % 12] == planet]


def _functional_role(planet, asc_sign):
    """Functional nature from lordship: Yogakaraka, benefic, malefic or mixed."""
    owned = _owned_houses(planet, asc_sign)
    if not owned:
        return None, owned
    if any(h in (4, 7, 10) for h in owned) and any(h in (5, 9) for h in owned):
        return 'yogakaraka', owned
    if 1 in owned or any(h in (5, 9) for h in owned):
        return 'benefic', owned
    if any(h in DUSTHANAS for h in owned):
        return 'malefic', owned
    return 'neutral', owned


# Vimshottari lords and the nakshatras, for the KP and pada readings
VIMSHOTTARI_YEARS = {'Ketu': 7, 'Venus': 20, 'Sun': 6, 'Moon': 10, 'Mars': 7, 'Rahu': 18, 'Jupiter': 16, 'Saturn': 19, 'Mercury': 17}
DASA_LORDS = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']

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
