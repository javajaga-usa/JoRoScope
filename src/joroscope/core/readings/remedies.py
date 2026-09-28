"""Parihara (remedies): what in this chart calls for a remedy, and the traditional remedy for it.
The reasons are the doshas (Chevvai, Kaal Sarp, Rahu-Ketu), a running Sade Sati, Ashtama or
Kandaka Sani, grahas below their required Shadbala or debilitated, the running Maha Dasa and
Bhukti lords when they are weak or rule dusthanas, and difficult yogas. Each graha's remedy is its
Navagraha temple in Tamil Nadu, deity, day, beeja mantra with the japa count commonly given,
charity and fasting. Remedies here are worship, mantra, charity and conduct; gemstones are left to
the Lucky Factors chapter, which names only the Lagna and 9th lords' stones.
"""
from datetime import datetime, timezone

from .common import PLANET_TAMIL, SIGN_LORDS, _functional_role
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
    reasons = {}  # graha -> list of (en, ta) reasons
    cards = []

    def add(g, en, ta):
        reasons.setdefault(g, [])
        if (en, ta) not in reasons[g]:
            reasons[g].append((en, ta))

    # Doshas
    chevvai = doshas.get('chevvai') or {}
    for dosha_key, present in (('chevvai', chevvai.get('effective', chevvai.get('present') and not chevvai.get('cancelled'))),
                               ('kaal_sarp', (doshas.get('kaal_sarp') or {}).get('present')),
                               ('rahu_ketu', (doshas.get('rahu_ketu') or {}).get('present'))):
        if present:
            en, ta, g, rem_en, rem_ta = DOSHA_REMEDIES[dosha_key]
            cards.append(card('🛡️', en, ta, rem_en, rem_ta, 'Dosha in the birth chart', 'ஜாதகத்தில் உள்ள தோஷம்', verdict='bad'))
            add(g, f'{en} in the chart', f'ஜாதகத்தில் {ta}')

    # Saturn's cycle running now
    now = datetime.now(timezone.utc)
    for cycle in (chart.get('gochara') or {}).get('saturn_cycles', []):
        try:
            running = datetime.fromisoformat(cycle['start']) <= now < datetime.fromisoformat(cycle['end'])
        except (KeyError, ValueError):
            continue
        if running and cycle.get('kind') in SATURN_CYCLE_REMEDY:
            en, ta = SATURN_CYCLE_REMEDY[cycle['kind']]
            until = cycle['end'][:10]
            cards.append(card(
                '🪔', en, ta,
                f"Until about {until}. Light a sesame-oil lamp to Lord Shani on Saturdays, worship Hanuman (the Hanuman Chalisa or "
                f"Sundara Kandam), visit Thirunallar if you can, and serve the elderly and labourers. Keep promises and avoid shortcuts: "
                f"Saturn rewards patience and honest work.",
                f"சுமார் {until} வரை. சனிக்கிழமைகளில் சனி பகவானுக்கு நல்லெண்ணெய் தீபம் ஏற்றவும்; ஆஞ்சநேயரை வழிபடவும் (ஹனுமான் சாலீசா அல்லது "
                f"சுந்தர காண்டம்); இயன்றால் திருநள்ளாறு செல்லவும்; முதியோருக்கும் உழைப்பாளர்களுக்கும் உதவவும். வாக்குறுதிகளைக் காத்து "
                f"குறுக்கு வழிகளைத் தவிர்க்கவும்: பொறுமைக்கும் நேர்மையான உழைப்பிற்கும் சனி பலன் தரும்.",
                'Saturn transit from the natal Moon', 'ஜன்ம சந்திரனிலிருந்து சனி கோச்சாரம்', verdict='bad'))
            add('Saturn', en, ta)

    # Weak or debilitated grahas
    for g in ('Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'):
        sb = shadbala.get(g) or {}
        if sb.get('rupas') is not None and sb.get('required_rupas') and sb['rupas'] < sb['required_rupas']:
            add(g, f"Shadbala {sb['rupas']:.2f} of the {sb['required_rupas']} rupas it needs",
                f"ஷட்பலம் தேவையான {sb['required_rupas']} ரூபத்தில் {sb['rupas']:.2f} மட்டுமே")
        if planets[g].get('dignity') == 'Debilitated':
            add(g, 'debilitated', 'நீசம்')

    # The running dasa lords, when weak or ruling dusthanas
    active = chart.get('active_dasha') or {}
    for level, level_en, level_ta in (('dasa', 'Maha Dasa', 'மகா தசை'), ('bhukti', 'Bhukti', 'புக்தி')):
        g = active.get(level)
        if not g:
            continue
        lord_of = g if g not in ('Rahu', 'Ketu') else SIGN_LORDS[planets[g]['sign_index']]
        role, _ = _functional_role(lord_of, asc)
        if g in reasons or role == 'malefic' or g in ('Rahu', 'Ketu'):
            add(g, f'its {level_en} is running now', f'அதன் {level_ta} தற்போது நடக்கிறது')

    # Difficult yogas
    for y in chart.get('yogas') or []:
        if y.get('nature') == 'bad':
            for g in y.get('planets', []):
                if g in GRAHA_REMEDIES:
                    add(g, y['name'], y.get('name_ta', y['name']))

    for g, why in reasons.items():
        rem_en, rem_ta = graha_remedy_text(g)
        cards.append(card(
            '🕉️', f'{g} (strengthen and pacify)', f'{PLANET_TAMIL[g]} (பலப்படுத்தவும் சாந்தப்படுத்தவும்)',
            rem_en, rem_ta,
            'Why: ' + '; '.join(en for en, _ in why), 'காரணம்: ' + '; '.join(ta for _, ta in why), verdict='mixed'))

    if not cards:
        cards.append(card('✅', 'No major affliction', 'பெரிய தோஷம் இல்லை',
                          'No dosha, Saturn cycle or weak graha in this chart calls for a special remedy. Regular worship of the family deity '
                          '(kula deivam) and the Navagrahas keeps the chart\'s strengths working.',
                          'இந்த ஜாதகத்தில் சிறப்புப் பரிகாரம் தேவைப்படும் தோஷம், சனி சுழற்சி அல்லது பலவீன கிரகம் இல்லை. குலதெய்வ வழிபாடும் '
                          'நவக்கிரக வழிபாடும் ஜாதக பலத்தைத் தொடர்ந்து காக்கும்.', verdict='good'))

    ref_rows = [((g, PLANET_TAMIL[g]), (GRAHA_REMEDIES[g][0], GRAHA_REMEDIES[g][1]), (GRAHA_REMEDIES[g][2], GRAHA_REMEDIES[g][3]),
                 (GRAHA_REMEDIES[g][4], GRAHA_REMEDIES[g][5]), f'{GRAHA_REMEDIES[g][7]:,}') for g in GRAHA_REMEDIES]
    return chapter(
        'remedies', 'Parihara (Remedies)', 'பரிகாரங்கள்',
        'Remedies for what this chart shows: its doshas, the Saturn cycle running now, weak or debilitated grahas and the running '
        'dasa lords. They are worship, mantra, charity and conduct; begin on the graha\'s weekday, in its hora if you can.',
        'இந்த ஜாதகம் காட்டுவதற்கான பரிகாரங்கள்: தோஷங்கள், தற்போதைய சனி சுழற்சி, பலவீனமான அல்லது நீச கிரகங்கள், நடப்பு தசா அதிபதிகள். '
        'இவை வழிபாடு, மந்திரம், தானம், ஒழுக்கம்; கிரகத்தின் கிழமையில், இயன்றால் அதன் ஓரையில் தொடங்கவும்.',
        cards=cards,
        tables=[table('Navagraha temples and japa', 'நவக்கிரகத் தலங்களும் ஜபமும்',
                      [('Graha', 'கிரகம்'), ('Temple', 'தலம்'), ('Deity', 'தெய்வம்'), ('Day', 'கிழமை'), ('Japa count', 'ஜப எண்ணிக்கை')],
                      ref_rows)],
        grahas=sorted(reasons))
