"""Parihara (remedies): what in this chart calls for a remedy, and the traditional remedy for it.
The reasons are the doshas (Chevvai, Kaal Sarp, Rahu-Ketu), a running Sade Sati, Ashtama or
Kandaka Sani, grahas below their required Shadbala or debilitated, the running Maha Dasa and
Bhukti lords when they are weak or rule dusthanas, and difficult yogas. Each graha's remedy is its
Navagraha temple in Tamil Nadu, deity, day, beeja mantra with the japa count commonly given,
charity and fasting. Remedies here are worship, mantra, charity and conduct; gemstones are left to
the Lucky Factors chapter, which names only the Lagna and 9th lords' stones.
"""
from datetime import datetime, timezone

from .common import PLANET_ML, PLANET_ML_CASE, PLANET_TAMIL, SIGN_LORDS, _functional_role
from .report import card, chapter, table

# graha: (temple, temple_ta, deity, deity_ta, day, day_ta, beeja mantra, japa count, charity, charity_ta)
GRAHA_REMEDIES = {
    'Sun': ('Suryanar Kovil', 'சூரியனார் கோவில்', 'Lord Shiva and Surya', 'சிவன், சூரிய பகவான்', 'Sunday', 'ஞாயிறு',
            'Om Hraam Hreem Hraum Sah Suryaya Namah', 7000, 'wheat, jaggery and red cloth', 'கோதுமை, வெல்லம், சிவப்புத் துணி'),
    'Moon': ('Thingalur', 'திங்களூர்', 'Goddess Parvati', 'பார்வதி தேவி', 'Monday', 'திங்கள்',
             'Om Shraam Shreem Shraum Sah Chandraya Namah', 11000, 'rice, milk and white cloth', 'அரிசி, பால், வெள்ளைத் துணி'),
    'Mars': ('Vaitheeswaran Koil', 'வைத்தீஸ்வரன் கோவில்', 'Lord Murugan (Subramanya)', 'முருகப் பெருமான்', 'Tuesday', 'செவ்வாய்',
             'Om Kraam Kreem Kraum Sah Bhaumaya Namah', 10000, 'red lentils (thuvaram paruppu) and red cloth', 'துவரம் பருப்பு, சிவப்புத் துணி'),
    'Mercury': ('Thiruvenkadu', 'திருவெண்காடு', 'Lord Vishnu', 'மகாவிஷ்ணு', 'Wednesday', 'புதன்',
                'Om Braam Breem Braum Sah Budhaya Namah', 9000, 'green gram and green cloth', 'பச்சைப் பயறு, பச்சைத் துணி'),
    'Jupiter': ('Alangudi', 'ஆலங்குடி', 'Dakshinamurthy', 'தட்சிணாமூர்த்தி', 'Thursday', 'வியாழன்',
                'Om Graam Greem Graum Sah Gurave Namah', 19000, 'chickpeas (kondakadalai), turmeric and yellow cloth', 'கொண்டைக்கடலை, மஞ்சள், மஞ்சள் துணி'),
    'Venus': ('Kanjanur', 'கஞ்சனூர்', 'Goddess Mahalakshmi', 'மகாலட்சுமி', 'Friday', 'வெள்ளி',
              'Om Draam Dreem Draum Sah Shukraya Namah', 16000, 'white rice, curd and white silk', 'அரிசி, தயிர், வெண் பட்டு'),
    'Saturn': ('Thirunallar', 'திருநள்ளாறு', 'Lord Shani and Hanuman', 'சனீஸ்வர பகவான், ஆஞ்சநேயர்', 'Saturday', 'சனி',
               'Om Praam Preem Praum Sah Shanaischaraya Namah', 23000, 'sesame (ellu), sesame oil and black cloth', 'எள், நல்லெண்ணெய், கருப்புத் துணி'),
    'Rahu': ('Thirunageswaram', 'திருநாகேஸ்வரம்', 'Goddess Durga', 'துர்கை அம்மன்', 'Saturday', 'சனி',
             'Om Bhraam Bhreem Bhraum Sah Rahave Namah', 18000, 'black gram (ulundu) and a blue cloth', 'உளுந்து, நீலத் துணி'),
    'Ketu': ('Keezhaperumpallam', 'கீழப்பெரும்பள்ளம்', 'Lord Ganesha', 'விநாயகப் பெருமான்', 'Tuesday', 'செவ்வாய்',
             'Om Sraam Sreem Sraum Sah Ketave Namah', 17000, 'horse gram (kollu) and a multicoloured cloth', 'கொள்ளு, பல வண்ணத் துணி'),
}
# Fasting day for each graha (the Tamil viratham)
FASTING = {'Sun': ('Sunday', 'ஞாயிறு'), 'Moon': ('Monday (Somavara viratham)', 'திங்கள் (சோமவார விரதம்)'),
           'Mars': ('Tuesday (Sevvai viratham)', 'செவ்வாய் (செவ்வாய் விரதம்)'), 'Mercury': ('Wednesday', 'புதன்'),
           'Jupiter': ('Thursday (Guru viratham)', 'வியாழன் (குரு விரதம்)'), 'Venus': ('Friday (Sukravara viratham)', 'வெள்ளி (சுக்கிரவார விரதம்)'),
           'Saturn': ('Saturday (Sani viratham)', 'சனி (சனி விரதம்)'), 'Rahu': ('Saturday, with Rahu Kalam worship', 'சனி, ராகு கால வழிபாட்டுடன்'),
           'Ketu': ('Tuesday, with Ganesha worship', 'செவ்வாய், விநாயகர் வழிபாட்டுடன்')}

DOSHA_REMEDIES = {
    'chevvai': ('Chevvai Dosham', 'செவ்வாய் தோஷம்', 'Mars',
                'Worship Lord Murugan on Tuesdays and during Sashti; visit Vaitheeswaran Koil or Palani; chant the Kanda Sashti Kavasam. '
                'Matching with a partner who has a similar Chevvai Dosham (dosha samyam) is the traditional balance.',
                'செவ்வாய்க்கிழமைகளிலும் சஷ்டியிலும் முருகப் பெருமானை வழிபடவும்; வைத்தீஸ்வரன் கோவில் அல்லது பழனி செல்லவும்; கந்த சஷ்டி கவசம் படிக்கவும். '
                'இதே அளவு செவ்வாய் தோஷம் உள்ள வரனுடன் பொருத்துவது (தோஷ சாம்யம்) பாரம்பரிய சமன்பாடு.'),
    'kaal_sarp': ('Kaal Sarp Dosham', 'கால சர்ப்ப தோஷம்', 'Rahu',
                  'A Rahu-Ketu (Sarpa) shanti at Srikalahasti or Thirunageswaram; worship Lord Shiva on Mondays and during Pradosham; '
                  'offer milk to the snake idols at a Naga shrine on Naga Panchami.',
                  'ஸ்ரீகாளஹஸ்தி அல்லது திருநாகேஸ்வரத்தில் ராகு-கேது (சர்ப்ப) சாந்தி; திங்கள், பிரதோஷ நாட்களில் சிவ வழிபாடு; '
                  'நாக பஞ்சமியன்று நாகர் சிலைகளுக்குப் பால் அபிஷேகம்.'),
    'rahu_ketu': ('Rahu-Ketu (Naga) Dosham', 'ராகு-கேது (நாக) தோஷம்', 'Rahu',
                  'Worship at Thirunageswaram (Rahu) and Keezhaperumpallam (Ketu); light a lamp to Durga during Rahu Kalam on Tuesdays and Fridays; '
                  'Naga pratishtha under a peepal and neem tree is the traditional parihara before marriage.',
                  'திருநாகேஸ்வரம் (ராகு), கீழப்பெரும்பள்ளம் (கேது) வழிபாடு; செவ்வாய், வெள்ளிக்கிழமைகளில் ராகு காலத்தில் துர்கைக்கு விளக்கு; '
                  'திருமணத்திற்கு முன் அரச-வேம்பு மரத்தடியில் நாக பிரதிஷ்டை பாரம்பரிய பரிகாரம்.'),
}
SATURN_CYCLE_REMEDY = {
    'sade_sati': ('Ezharai Sani (Sade Sati) is running', 'ஏழரைச் சனி நடக்கிறது'),
    'ashtama': ('Ashtama Sani is running', 'அஷ்டம சனி நடக்கிறது'),
    'kandaka': ('Kandaka Sani is running', 'கண்டக சனி நடக்கிறது'),
    'ardhashtama': ('Ardhashtama Sani is running', 'அர்த்தாஷ்டம சனி நடக்கிறது'),
}

# graha: (temple, deity, day, charity, fasting) in Malayalam
GRAHA_REMEDIES_ML = {
    'Sun': ('സൂര്യനാർ കോവിൽ', 'ശിവനും സൂര്യഭഗവാനും', 'ഞായറാഴ്ച', 'ഗോതമ്പ്, ശർക്കര, ചുവന്ന തുണി', 'ഞായർ'),
    'Moon': ('തിങ്കളൂർ', 'പാർവ്വതീദേവി', 'തിങ്കളാഴ്ച', 'അരി, പാൽ, വെള്ളത്തുണി', 'തിങ്കൾ (സോമവാര വ്രതം)'),
    'Mars': ('വൈത്തീശ്വരൻ കോവിൽ', 'സുബ്രഹ്മണ്യൻ', 'ചൊവ്വാഴ്ച', 'തുവരപ്പരിപ്പ്, ചുവന്ന തുണി', 'ചൊവ്വ (ചൊവ്വാ വ്രതം)'),
    'Mercury': ('തിരുവെൺകാട്', 'മഹാവിഷ്ണു', 'ബുധനാഴ്ച', 'ചെറുപയർ, പച്ചത്തുണി', 'ബുധൻ'),
    'Jupiter': ('ആലങ്കുടി', 'ദക്ഷിണാമൂർത്തി', 'വ്യാഴാഴ്ച', 'കടല, മഞ്ഞൾ, മഞ്ഞത്തുണി', 'വ്യാഴം (ഗുരു വ്രതം)'),
    'Venus': ('കഞ്ചനൂർ', 'മഹാലക്ഷ്മി', 'വെള്ളിയാഴ്ച', 'അരി, തൈര്, വെള്ളപ്പട്ട്', 'വെള്ളി (ശുക്രവാര വ്രതം)'),
    'Saturn': ('തിരുനള്ളാർ', 'ശനീശ്വരനും ഹനുമാനും', 'ശനിയാഴ്ച', 'എള്ള്, നല്ലെണ്ണ, കറുത്ത തുണി', 'ശനി (ശനി വ്രതം)'),
    'Rahu': ('തിരുനാഗേശ്വരം', 'ദുർഗ്ഗാദേവി', 'ശനിയാഴ്ച', 'ഉഴുന്ന്, നീലത്തുണി', 'ശനി, രാഹുകാല ആരാധനയോടെ'),
    'Ketu': ('കീഴപ്പെരുമ്പള്ളം', 'ഗണപതി', 'ചൊവ്വാഴ്ച', 'മുതിര, പലനിറത്തുണി', 'ചൊവ്വ, ഗണപതി ആരാധനയോടെ'),
}
DOSHA_REMEDIES_ML = {
    'chevvai': ('ചൊവ്വാദോഷം',
                'ചൊവ്വാഴ്ചകളിലും ഷഷ്ഠിയിലും സുബ്രഹ്മണ്യനെ ആരാധിക്കുക; വൈത്തീശ്വരൻ കോവിലോ പഴനിയോ സന്ദർശിക്കുക; കന്ദഷഷ്ഠി കവചം ചൊല്ലുക. '
                'സമാന അളവിൽ ചൊവ്വാദോഷമുള്ള പങ്കാളിയുമായി ചേർക്കുന്നത് (ദോഷസാമ്യം) പരമ്പരാഗത സന്തുലനമാണ്.'),
    'kaal_sarp': ('കാലസർപ്പ ദോഷം',
                  'ശ്രീകാളഹസ്തിയിലോ തിരുനാഗേശ്വരത്തോ രാഹു-കേതു (സർപ്പ) ശാന്തി; തിങ്കളാഴ്ചകളിലും പ്രദോഷത്തിലും ശിവാരാധന; '
                  'നാഗപഞ്ചമിക്ക് സർപ്പക്കാവിൽ നാഗപ്രതിമകൾക്ക് പാലഭിഷേകം.'),
    'rahu_ketu': ('രാഹു-കേതു (നാഗ) ദോഷം',
                  'തിരുനാഗേശ്വരം (രാഹു), കീഴപ്പെരുമ്പള്ളം (കേതു) ആരാധന; ചൊവ്വ, വെള്ളി ദിവസങ്ങളിൽ രാഹുകാലത്ത് ദുർഗ്ഗയ്ക്ക് വിളക്ക്; '
                  'വിവാഹത്തിന് മുമ്പ് അരയാൽ-വേപ്പ് ചുവട്ടിൽ നാഗപ്രതിഷ്ഠ പരമ്പരാഗത പരിഹാരമാണ്.'),
}
SATURN_CYCLE_ML = {'sade_sati': 'ഏഴരശ്ശനി നടക്കുന്നു', 'ashtama': 'അഷ്ടമശ്ശനി നടക്കുന്നു', 'kandaka': 'കണ്ടകശ്ശനി നടക്കുന്നു',
                   'ardhashtama': 'അർദ്ധാഷ്ടമശ്ശനി നടക്കുന്നു'}


def graha_remedy_ml(g):
    temple, deity, day, charity, fast = GRAHA_REMEDIES_ML[g]
    mantra, japa = GRAHA_REMEDIES[g][6], GRAHA_REMEDIES[g][7]
    return (f"{day}കളിൽ {deity} ആരാധന; {PLANET_ML_CASE['gen'][g]} നവഗ്രഹ ക്ഷേത്രമായ {temple} സന്ദർശിക്കുക. "
            f"\"{mantra}\" മന്ത്രം ഒരു മണ്ഡലകാലത്ത് (48 ദിവസം) {japa:,} തവണ ജപിക്കുക. {charity} ദാനം ചെയ്യുക; "
            f"{fast} വ്രതം നോക്കുക.")


def graha_remedy_text(g):
    temple, temple_ta, deity, deity_ta, day, day_ta, mantra, japa, charity, charity_ta = GRAHA_REMEDIES[g]
    fast_en, fast_ta = FASTING[g]
    return (f"Worship {deity} on {day}s and visit {temple}, the Navagraha temple of {g}. Chant \"{mantra}\" "
            f"{japa:,} times over a mandala (48 days). Give {charity} in charity, and keep a fast on {fast_en}.",
            f"{day_ta}க்கிழமைகளில் {deity_ta} வழிபாடு; {PLANET_TAMIL[g]} நவக்கிரகத் தலமான {temple_ta} செல்லவும். "
            f"\"{mantra}\" மந்திரத்தை ஒரு மண்டலத்தில் (48 நாட்கள்) {japa:,} முறை ஜபிக்கவும். {charity_ta} தானம் செய்யவும்; "
            f"{fast_ta} விரதம் இருக்கவும்.")


def calculate_remedies(chart):
    planets = chart['planets']
    asc = planets['Ascendant']['sign_index']
    doshas = chart.get('doshas') or {}
    shadbala = chart.get('shadbala') or {}
    reasons = {}  # graha -> list of (en, ta, ml) reasons
    cards = []

    def add(g, en, ta, ml):
        reasons.setdefault(g, [])
        if (en, ta, ml) not in reasons[g]:
            reasons[g].append((en, ta, ml))

    # Doshas
    chevvai = doshas.get('chevvai') or {}
    for dosha_key, present in (('chevvai', chevvai.get('effective', chevvai.get('present') and not chevvai.get('cancelled'))),
                               ('kaal_sarp', (doshas.get('kaal_sarp') or {}).get('present')),
                               ('rahu_ketu', (doshas.get('rahu_ketu') or {}).get('present'))):
        if present:
            en, ta, g, rem_en, rem_ta = DOSHA_REMEDIES[dosha_key]
            ml, rem_ml = DOSHA_REMEDIES_ML[dosha_key]
            cards.append(card('🛡️', en, ta, rem_en, rem_ta, 'Dosha in the birth chart', 'ஜாதகத்தில் உள்ள தோஷம்', verdict='bad',
                              title_ml=ml, body_ml=rem_ml, sub_ml='ജാതകത്തിലുള്ള ദോഷം'))
            add(g, f'{en} in the chart', f'ஜாதகத்தில் {ta}', f'ജാതകത്തിൽ {ml}')

    # Saturn's cycle running now
    now = datetime.now(timezone.utc)
    for cycle in (chart.get('gochara') or {}).get('saturn_cycles', []):
        try:
            running = datetime.fromisoformat(cycle['start']) <= now < datetime.fromisoformat(cycle['end'])
        except (KeyError, ValueError):
            continue
        if running and cycle.get('kind') in SATURN_CYCLE_REMEDY:
            en, ta = SATURN_CYCLE_REMEDY[cycle['kind']]
            ml = SATURN_CYCLE_ML[cycle['kind']]
            until = cycle['end'][:10]
            cards.append(card(
                '🪔', en, ta,
                f"Until about {until}. Light a sesame-oil lamp to Lord Shani on Saturdays, worship Hanuman (the Hanuman Chalisa or "
                f"Sundara Kandam), visit Thirunallar if you can, and serve the elderly and labourers. Keep promises and avoid shortcuts: "
                f"Saturn rewards patience and honest work.",
                f"சுமார் {until} வரை. சனிக்கிழமைகளில் சனி பகவானுக்கு நல்லெண்ணெய் தீபம் ஏற்றவும்; ஆஞ்சநேயரை வழிபடவும் (ஹனுமான் சாலீசா அல்லது "
                f"சுந்தர காண்டம்); இயன்றால் திருநள்ளாறு செல்லவும்; முதியோருக்கும் உழைப்பாளர்களுக்கும் உதவவும். வாக்குறுதிகளைக் காத்து "
                f"குறுக்கு வழிகளைத் தவிர்க்கவும்: பொறுமைக்கும் நேர்மையான உழைப்பிற்கும் சனி பலன் தரும்.",
                'Saturn transit from the natal Moon', 'ஜன்ம சந்திரனிலிருந்து சனி கோச்சாரம்', verdict='bad',
                title_ml=ml,
                body_ml=(f"ഏകദേശം {until} വരെ. ശനിയാഴ്ചകളിൽ ശനിഭഗവാന് നല്ലെണ്ണ വിളക്ക് കത്തിക്കുക; ഹനുമാനെ ആരാധിക്കുക (ഹനുമാൻ ചാലിസ അല്ലെങ്കിൽ "
                         f"സുന്ദരകാണ്ഡം); സാധിക്കുമെങ്കിൽ തിരുനള്ളാർ സന്ദർശിക്കുക; പ്രായമായവരെയും തൊഴിലാളികളെയും സഹായിക്കുക. വാക്ക് പാലിക്കുക, "
                         f"കുറുക്കുവഴികൾ ഒഴിവാക്കുക: ക്ഷമയ്ക്കും സത്യസന്ധമായ അധ്വാനത്തിനും ശനി ഫലം നൽകും."),
                sub_ml='ജന്മചന്ദ്രനിൽ നിന്നുള്ള ശനി ഗോചരം'))
            add('Saturn', en, ta, ml)

    # Weak or debilitated grahas
    for g in ('Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'):
        sb = shadbala.get(g) or {}
        if sb.get('rupas') is not None and sb.get('required_rupas') and sb['rupas'] < sb['required_rupas']:
            add(g, f"Shadbala {sb['rupas']:.2f} of the {sb['required_rupas']} rupas it needs",
                f"ஷட்பலம் தேவையான {sb['required_rupas']} ரூபத்தில் {sb['rupas']:.2f} மட்டுமே",
                f"ഷഡ്ബലം ആവശ്യമായ {sb['required_rupas']} രൂപത്തിൽ {sb['rupas']:.2f} മാത്രം")
        if planets[g].get('dignity') == 'Debilitated':
            add(g, 'debilitated', 'நீசம்', 'നീചം')

    # The running dasa lords, when weak or ruling dusthanas
    active = chart.get('active_dasha') or {}
    for level, level_en, level_ta, level_ml in (('dasa', 'Maha Dasa', 'மகா தசை', 'മഹാദശ'), ('bhukti', 'Bhukti', 'புக்தி', 'ഭുക്തി')):
        g = active.get(level)
        if not g:
            continue
        lord_of = g if g not in ('Rahu', 'Ketu') else SIGN_LORDS[planets[g]['sign_index']]
        role, _ = _functional_role(lord_of, asc)
        if g in reasons or role == 'malefic' or g in ('Rahu', 'Ketu'):
            add(g, f'its {level_en} is running now', f'அதன் {level_ta} தற்போது நடக்கிறது', f'അതിന്റെ {level_ml} ഇപ്പോൾ നടക്കുന്നു')

    # Difficult yogas
    for y in chart.get('yogas') or []:
        if y.get('nature') == 'bad':
            for g in y.get('planets', []):
                if g in GRAHA_REMEDIES:
                    add(g, y['name'], y.get('name_ta', y['name']), y.get('name_ml', y['name']))

    for g, why in reasons.items():
        rem_en, rem_ta = graha_remedy_text(g)
        cards.append(card(
            '🕉️', f'{g} (strengthen and pacify)', f'{PLANET_TAMIL[g]} (பலப்படுத்தவும் சாந்தப்படுத்தவும்)',
            rem_en, rem_ta,
            'Why: ' + '; '.join(w[0] for w in why), 'காரணம்: ' + '; '.join(w[1] for w in why), verdict='mixed',
            title_ml=f'{PLANET_ML[g]} (ബലപ്പെടുത്താനും ശാന്തമാക്കാനും)', body_ml=graha_remedy_ml(g),
            sub_ml='കാരണം: ' + '; '.join(w[2] for w in why)))

    if not cards:
        cards.append(card('✅', 'No major affliction', 'பெரிய தோஷம் இல்லை',
                          'No dosha, Saturn cycle or weak graha in this chart calls for a special remedy. Regular worship of the family deity '
                          '(kula deivam) and the Navagrahas keeps the chart\'s strengths working.',
                          'இந்த ஜாதகத்தில் சிறப்புப் பரிகாரம் தேவைப்படும் தோஷம், சனி சுழற்சி அல்லது பலவீன கிரகம் இல்லை. குலதெய்வ வழிபாடும் '
                          'நவக்கிரக வழிபாடும் ஜாதக பலத்தைத் தொடர்ந்து காக்கும்.', verdict='good',
                          title_ml='വലിയ ദോഷമില്ല',
                          body_ml='ഈ ജാതകത്തിൽ പ്രത്യേക പരിഹാരം ആവശ്യമുള്ള ദോഷമോ ശനിചക്രമോ ബലഹീന ഗ്രഹമോ ഇല്ല. കുലദേവതാ ആരാധനയും '
                                  'നവഗ്രഹ ആരാധനയും ജാതകബലം തുടർന്നും കാക്കും.'))

    R, M = GRAHA_REMEDIES, GRAHA_REMEDIES_ML
    ref_rows = [((g, PLANET_TAMIL[g], PLANET_ML[g]), (R[g][0], R[g][1], M[g][0]), (R[g][2], R[g][3], M[g][1]),
                 (R[g][4], R[g][5], M[g][2]), f'{R[g][7]:,}') for g in GRAHA_REMEDIES]
    return chapter(
        'parihara', 'Parihara (Remedies)', 'பரிகாரங்கள்',
        'Remedies for what this chart shows: its doshas, the Saturn cycle running now, weak or debilitated grahas and the running '
        'dasa lords. They are worship, mantra, charity and conduct; begin on the graha\'s weekday, in its hora if you can.',
        'இந்த ஜாதகம் காட்டுவதற்கான பரிகாரங்கள்: தோஷங்கள், தற்போதைய சனி சுழற்சி, பலவீனமான அல்லது நீச கிரகங்கள், நடப்பு தசா அதிபதிகள். '
        'இவை வழிபாடு, மந்திரம், தானம், ஒழுக்கம்; கிரகத்தின் கிழமையில், இயன்றால் அதன் ஓரையில் தொடங்கவும்.',
        cards=cards,
        tables=[table('Navagraha temples and japa', 'நவக்கிரகத் தலங்களும் ஜபமும்',
                      [('Graha', 'கிரகம்', 'ഗ്രഹം'), ('Temple', 'தலம்', 'ക്ഷേത്രം'), ('Deity', 'தெய்வம்', 'ദേവത'), ('Day', 'கிழமை', 'ദിവസം'),
                       ('Japa count', 'ஜப எண்ணிக்கை', 'ജപ സംഖ്യ')],
                      ref_rows, title_ml='നവഗ്രഹ ക്ഷേത്രങ്ങളും ജപവും')],
        title_ml='പരിഹാരങ്ങൾ',
        intro_ml=('ഈ ജാതകം കാണിക്കുന്നവയ്ക്കുള്ള പരിഹാരങ്ങൾ: ദോഷങ്ങൾ, ഇപ്പോഴത്തെ ശനിചക്രം, ബലഹീനമോ നീചമോ ആയ ഗ്രഹങ്ങൾ, നടപ്പ് ദശാനാഥന്മാർ. '
                  'ഇവ ആരാധന, മന്ത്രം, ദാനം, സദാചാരം എന്നിവയാണ്; ഗ്രഹത്തിന്റെ ആഴ്ചയിൽ, സാധിക്കുമെങ്കിൽ അതിന്റെ ഹോരയിൽ തുടങ്ങുക.'),
        grahas=sorted(reasons))
