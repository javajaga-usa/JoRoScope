"""Bhrigu Nandi Nadi, avasthas, nakshatra pada readings, Tajika sahams, Panchanga Phala
and the Sudarshana Chakra.
"""

from datetime import datetime
from zoneinfo import ZoneInfo

from .common import (
    DIGNITY_SCORE, DUSTHANAS, HOUSE_THEMES, HOUSE_THEMES_ML, KENDRAS, MALAYALAM_SIGNS, NATURAL_BENEFICS, PLANET_ML,
    MALAYALAM_STARS, PLANET_TAMIL, SIGNS, STARS,
    SIGN_LORDS, TAMIL_SIGNS, TRIKONAS, _ordinal
)


# 3. BHRIGU NANDI NADI (BNN)
# Nadi links between grahas counted by sign: together, in trine (5th/9th), opposite (7th), in the
# next sign (2nd) or the previous sign (12th). A retrograde graha also acts from the previous sign.
BNN_SUTRAS = [
    ('Jupiter', 'Saturn', 'Dharma-Karma Adhipati Yoga (Guru + Shani)', 'தர்ம-கர்மாதிபதி யோகம் (குரு + சனி சேர்க்கை)',
     'The Divine Worker Sutra. Links Jeeva Karaka (Soul) with Karma Karaka (Duty). Bestows deep sense of social duty, ethical professional standing, steady perseverance through initial delays, and lasting eminence once Saturn matures at 36.',
     'ஜீவகாரகன் குருவும் கர்மகாரகன் சனியும் தொடர்பு கொள்வதால் உண்டாகும் உன்னத யோகம். தொடக்கத்தில் உழைப்புக்கேற்ற அங்கீகாரம் சற்றே தாமதமானாலும், 36 வயதிற்குப் பின் (சனி முதிர்ச்சி பெறும் வயது) அழியாத நற்பெயரும், உயர்ந்த பதவியும், சமூக மரியாதையும் கிட்டும்.'),
    ('Jupiter', 'Mars', 'Deva-Senapati Yoga (Guru + Mangala)', 'தேவ-சேனாதிபதி யோகம் (குரு + செவ்வாய் சேர்க்கை)',
     'Courageous Leader Sutra. Melds divine wisdom with energetic vigor. Bestows commanding executive power, technical/engineering acumen, real estate prosperity, and protective championship of family interests.',
     'குருவும் செவ்வாயும் இணைவதால் அஞ்சாத தைரியம், பூமி-மனை யோகம், பொறியியல்/தொழில்நுட்ப ஆளுமை மற்றும் தலைமை நிர்வாகப் பொறுப்புகள் அமையும்.'),
    ('Jupiter', 'Venus', 'Bhrigu-Guru Yoga (Jupiter + Venus)', 'பிருகு-குரு யோகம் (குரு + சுக்கிரன் சேர்க்கை)',
     'Abundant Fortune Sutra. Harmonizes the two supreme benefics (Deva Guru & Asura Guru). Bestows immense material affluence, refined aesthetic taste, virtuous life companion, and peaceful family prosperity.',
     'இரு பெரும் சுப கிரகங்களான குருவும் சுக்கிரனும் இணையும் மகா சுப யோகம். பொன், பொருள் சேர்க்கை, வாகன யோகம், குடும்ப மகிழ்ச்சி மற்றும் ஆடம்பர வசதிகள் இயல்பாகவே அமையும்.'),
    ('Jupiter', 'Mercury', 'Saraswati Yoga (Guru + Budha)', 'சரஸ்வதி யோகம் (குரு + புதன் சேர்க்கை)',
     'Master of Wisdom & Commerce. Fosters multifaceted intellectual depth, teaching mastery, linguistic wit, successful business enterprise, and diplomatic counsel.',
     'குருவும் புதனும் இணைவதால் வாக்கு வன்மை, எழுத்து, கணிதம், ஜோதிடம், மற்றும் வர்த்தகத் துறைகளில் தனி முத்திரை பதிக்கும் கல்வி ஞானம் உண்டாகும்.'),
    ('Jupiter', 'Sun', 'Shiva-Raja Yoga (Guru + Surya)', 'சிவ-ராஜ யோகம் (குரு + சூரியன் சேர்க்கை)',
     'Honor & Regal Dignity. Grants divine protection, paternal blessings, ethical leadership, and honors from governmental or high corporate bodies.',
     'சூரியனும் குருவும் இணைவதால் தந்தை வழியில் பெருமை, அரசு வழியில் ஆதரவு, கம்பீரமான தோற்றம் மற்றும் நேர்மையான வழியில் உயர்ந்த கௌரவம் கிட்டும்.'),
    ('Jupiter', 'Rahu', 'Guru-Rahu Link (Unconventional Thinker)', 'குரு-ராகு தொடர்பு (புதுமைச் சிந்தனை)',
     'Unconventional Innovator. Drives revolutionary thinking that challenges traditional dogmas. Strongly favors overseas travels, cutting-edge technology, foreign networks, and unconventional success.',
     'குருவும் ராகுவும் இணைவதால் பழமைவாதத்தைத் தாண்டி நவீன அறிவியல், கணினி மற்றும் வெளிநாட்டு தொடர்புகளால் பெரிய முன்னேற்றத்தை அடையும் ஆற்றல் உண்டு.'),
    ('Jupiter', 'Ketu', 'Gnana Mukti Yoga (Guru + Ketu)', 'ஞான முக்தி யோகம் (குரு + கேது சேர்க்கை)',
     'Spiritual Seeker & Mystic. Bestows philosophical detachment, profound intuitive faculties, natural healing talents, and attraction to meditation, astrology, or higher metaphysics.',
     'ஞானகாரகன் கேதுவும் குருவும் இணைவதால் இறை பக்தி, உள்ளுணர்வு, ஜோதிடம் மற்றும் ஆன்மீக ஆராய்ச்சியில் அதீத ஞானம் உண்டாகும்.'),
    ('Saturn', 'Venus', 'Lakshmi-Karma Yoga (Shani + Shukra)', 'லட்சுமி-கர்ம யோகம் (சனி + சுக்கிரன் சேர்க்கை)',
     'Prosperity through Enterprise. Karma Karaka meets Dhanakaraka. Bestows steady accumulation of durable assets, success in corporate/luxury industries, and a supportive partner.',
     'சனி மற்றும் சுக்கிரன் இணைவதால் கடின உழைப்பு பெரும் செல்வமாக மாறும். நிலையான அசையாச் சொத்துக்கள் மற்றும் தொழில் மூலமாக நிரந்தர வருமானம் பெருகும்.'),
    ('Saturn', 'Mercury', 'Vyapara Yoga (Shani + Budha)', 'வியாபார யோகம் (சனி + புதன் சேர்க்கை)',
     'Master of Commerce & Logistics. Combines patient discipline with analytical calculation. Highly favored for auditing, legal trade, software development, and large-scale commerce.',
     'சனி மற்றும் புதன் இணைவதால் கணக்கு, தணிக்கை, மென்பொருள் மற்றும் வணிக மேலாண்மையில் நுட்பமான நிபுணத்துவம் பெற்று தொழிலில் வெற்றி பெறுவீர்கள்.'),
    ('Jupiter', 'Moon', 'Gaja-Kesari Sutra (Guru + Chandra)', 'கஜகேசரி சூத்திரம் (குரு + சந்திரன்)',
     'Respect, a helpful mother and good public standing; a generous, contented mind.',
     'குரு-சந்திரன் தொடர்பால் மரியாதை, தாயின் ஆதரவு, நல்ல பொது அந்தஸ்து; தாராள மனமும் மனநிறைவும் உண்டு.'),
    ('Saturn', 'Mars', 'Karma-Bhumi Sutra (Shani + Mangala)', 'கர்ம-பூமி சூத்திரம் (சனி + செவ்வாய்)',
     'Work with land, machinery, engineering or construction; hard-won results through struggle and technical skill. Guard against accidents and conflict at work.',
     'சனி-செவ்வாய் தொடர்பால் நிலம், இயந்திரம், பொறியியல் அல்லது கட்டுமானத் துறைகளில் உழைப்பு; போராட்டத்தின் மூலம் கிடைக்கும் வெற்றி. பணியிடத்தில் விபத்து மற்றும் மோதல்களில் கவனம் தேவை.'),
    ('Saturn', 'Sun', 'Pitru-Karma Sutra (Shani + Surya)', 'பித்ரு-கர்ம சூத்திரம் (சனி + சூரியன்)',
     'Service under government or large institutions; responsibilities toward the father, with differences of outlook between father and native.',
     'சனி-சூரியன் தொடர்பால் அரசு அல்லது பெரிய நிறுவனங்களின் கீழ் பணி; தந்தை மீதான பொறுப்புகள், தந்தையுடன் கருத்து வேறுபாடுகள் வரலாம்.'),
    ('Saturn', 'Moon', 'Jana-Seva Sutra (Shani + Chandra)', 'ஜன-சேவை சூத்திரம் (சனி + சந்திரன்)',
     'Work that serves the public or deals with the masses; a serious, responsible mind that must guard against worry.',
     'சனி-சந்திரன் தொடர்பால் மக்கள் சேவை அல்லது பொதுமக்களுடன் தொடர்புடைய பணி; பொறுப்பான மனம், ஆனால் கவலையைத் தவிர்க்க வேண்டும்.'),
    ('Saturn', 'Rahu', 'Videsha-Karma Sutra (Shani + Rahu)', 'விதேச-கர்ம சூத்திரம் (சனி + ராகு)',
     'Work in large organisations, technology or foreign lands; sudden rises and changes in career.',
     'சனி-ராகு தொடர்பால் பெரிய நிறுவனங்கள், தொழில்நுட்பம் அல்லது வெளிநாடுகளில் பணி; தொழிலில் திடீர் உயர்வுகளும் மாற்றங்களும் உண்டு.'),
    ('Saturn', 'Ketu', 'Karma-Viraga Sutra (Shani + Ketu)', 'கர்ம-வைராக்ய சூத்திரம் (சனி + கேது)',
     'Breaks or changes in career and a pull toward detachment; success in technical, research or spiritual work.',
     'சனி-கேது தொடர்பால் தொழிலில் இடைவெளிகள் அல்லது மாற்றங்கள், பற்றின்மை நாட்டம்; தொழில்நுட்பம், ஆராய்ச்சி அல்லது ஆன்மீகப் பணிகளில் வெற்றி.'),
]
# Malayalam for the sutras above, in the same order: (title, significance)
BNN_SUTRAS_ML = [
    ('ധർമ്മ-കർമ്മാധിപതി യോഗം (വ്യാഴം + ശനി)', 'ജീവകാരകനായ വ്യാഴവും കർമ്മകാരകനായ ശനിയും ബന്ധപ്പെടുന്ന ഉത്തമ യോഗം. തുടക്കത്തിൽ അധ്വാനത്തിനൊത്ത അംഗീകാരം അല്പം വൈകിയാലും 36 വയസ്സിനുശേഷം (ശനി പക്വത നേടുന്ന പ്രായം) മായാത്ത സൽപ്പേരും ഉന്നത പദവിയും സാമൂഹിക ആദരവും ലഭിക്കും.'),
    ('ദേവ-സേനാപതി യോഗം (വ്യാഴം + ചൊവ്വ)', 'വ്യാഴവും ചൊവ്വയും ചേരുന്നതിനാൽ ഭയമില്ലാത്ത ധൈര്യം, ഭൂമി-വീട് യോഗം, എഞ്ചിനീയറിംഗ്/സാങ്കേതിക വൈദഗ്ധ്യം, നേതൃഭരണ ചുമതലകൾ ലഭിക്കും.'),
    ('ഭൃഗു-ഗുരു യോഗം (വ്യാഴം + ശുക്രൻ)', 'രണ്ട് വലിയ ശുഭഗ്രഹങ്ങളായ വ്യാഴവും ശുക്രനും ചേരുന്ന മഹാശുഭയോഗം. സ്വർണ്ണം, സമ്പത്ത്, വാഹനയോഗം, കുടുംബസന്തോഷം, ആഡംബരസൗകര്യങ്ങൾ സ്വാഭാവികമായി ലഭിക്കും.'),
    ('സരസ്വതീ യോഗം (വ്യാഴം + ബുധൻ)', 'വ്യാഴവും ബുധനും ചേരുന്നതിനാൽ വാക്ചാതുര്യം, എഴുത്ത്, ഗണിതം, ജ്യോതിഷം, വ്യാപാരം എന്നിവയിൽ മുദ്ര പതിപ്പിക്കുന്ന വിദ്യാജ്ഞാനം ഉണ്ടാകും.'),
    ('ശിവ-രാജ യോഗം (വ്യാഴം + സൂര്യൻ)', 'സൂര്യനും വ്യാഴവും ചേരുന്നതിനാൽ പിതൃവഴി അഭിമാനം, സർക്കാർ പിന്തുണ, ഗാംഭീര്യമുള്ള രൂപം, സത്യസന്ധമായ വഴിയിൽ ഉന്നത ആദരവ് ലഭിക്കും.'),
    ('ഗുരു-രാഹു ബന്ധം (നവീന ചിന്ത)', 'വ്യാഴവും രാഹുവും ചേരുന്നതിനാൽ പഴമയെ കടന്ന് ആധുനിക ശാസ്ത്രം, കമ്പ്യൂട്ടർ, വിദേശബന്ധങ്ങൾ എന്നിവയാൽ വലിയ പുരോഗതി നേടാനുള്ള ശേഷിയുണ്ട്.'),
    ('ജ്ഞാന മുക്തി യോഗം (വ്യാഴം + കേതു)', 'ജ്ഞാനകാരകനായ കേതുവും വ്യാഴവും ചേരുന്നതിനാൽ ഈശ്വരഭക്തി, ഉൾക്കാഴ്ച, ജ്യോതിഷം, ആത്മീയ ഗവേഷണം എന്നിവയിൽ അഗാധ ജ്ഞാനം ഉണ്ടാകും.'),
    ('ലക്ഷ്മീ-കർമ്മ യോഗം (ശനി + ശുക്രൻ)', 'ശനിയും ശുക്രനും ചേരുന്നതിനാൽ കഠിനാധ്വാനം വലിയ സമ്പത്തായി മാറും. സ്ഥിരമായ ഭൂസ്വത്തുക്കളും തൊഴിലിലൂടെ സ്ഥിരവരുമാനവും വർധിക്കും.'),
    ('വ്യാപാര യോഗം (ശനി + ബുധൻ)', 'ശനിയും ബുധനും ചേരുന്നതിനാൽ കണക്ക്, ഓഡിറ്റ്, സോഫ്റ്റ്‌വെയർ, വ്യാപാര മാനേജ്‌മെന്റ് എന്നിവയിൽ സൂക്ഷ്മ വൈദഗ്ധ്യം നേടി തൊഴിലിൽ വിജയിക്കും.'),
    ('ഗജകേസരി സൂത്രം (വ്യാഴം + ചന്ദ്രൻ)', 'വ്യാഴ-ചന്ദ്ര ബന്ധത്താൽ ആദരവ്, അമ്മയുടെ പിന്തുണ, നല്ല പൊതുപദവി; ഉദാരമനസ്സും സംതൃപ്തിയും.'),
    ('കർമ്മ-ഭൂമി സൂത്രം (ശനി + ചൊവ്വ)', 'ശനി-ചൊവ്വ ബന്ധത്താൽ ഭൂമി, യന്ത്രം, എഞ്ചിനീയറിംഗ്, നിർമ്മാണ മേഖലകളിൽ അധ്വാനം; പോരാട്ടത്തിലൂടെ നേടുന്ന വിജയം. ജോലിസ്ഥലത്ത് അപകടങ്ങളിലും സംഘർഷങ്ങളിലും ശ്രദ്ധ വേണം.'),
    ('പിതൃ-കർമ്മ സൂത്രം (ശനി + സൂര്യൻ)', 'ശനി-സൂര്യ ബന്ധത്താൽ സർക്കാരിന്റെയോ വലിയ സ്ഥാപനങ്ങളുടെയോ കീഴിൽ ജോലി; അച്ഛനോടുള്ള ഉത്തരവാദിത്തങ്ങൾ, അച്ഛനുമായി അഭിപ്രായവ്യത്യാസങ്ങൾ വരാം.'),
    ('ജനസേവാ സൂത്രം (ശനി + ചന്ദ്രൻ)', 'ശനി-ചന്ദ്ര ബന്ധത്താൽ ജനസേവനമോ പൊതുജനങ്ങളുമായി ബന്ധപ്പെട്ട ജോലിയോ; ഉത്തരവാദിത്തമുള്ള മനസ്സ്, എന്നാൽ ആകുലത ഒഴിവാക്കണം.'),
    ('വിദേശ-കർമ്മ സൂത്രം (ശനി + രാഹു)', 'ശനി-രാഹു ബന്ധത്താൽ വലിയ സ്ഥാപനങ്ങളിലോ സാങ്കേതികവിദ്യയിലോ വിദേശത്തോ ജോലി; തൊഴിലിൽ പെട്ടെന്നുള്ള ഉയർച്ചകളും മാറ്റങ്ങളും.'),
    ('കർമ്മ-വൈരാഗ്യ സൂത്രം (ശനി + കേതു)', 'ശനി-കേതു ബന്ധത്താൽ തൊഴിലിൽ ഇടവേളകളോ മാറ്റങ്ങളോ, നിസ്സംഗതയിലേക്കുള്ള ചായ്‌വ്; സാങ്കേതിക, ഗവേഷണ, ആത്മീയ ജോലികളിൽ വിജയം.'),
]
BNN_LINKS_ML = ['ഒരേ രാശിയിൽ ചേർന്ന്', 'ത്രികോണത്തിൽ (5/9)', 'പരസ്പരം എതിർരാശിയിൽ (7)', 'അടുത്തടുത്ത രാശികളിൽ (2/12)']
BNN_LINKS = [
    ((0,), 'joined in the same sign', 'ஒரே ராசியில் சேர்ந்து'),
    ((4, 8), 'in trine (5th/9th)', 'திரிகோணத்தில் (5/9)'),
    ((6,), 'opposite each other (7th)', 'ஒன்றுக்கொன்று எதிர் ராசியில் (7)'),
    ((1, 11), 'in adjacent signs (2nd/12th)', 'அடுத்தடுத்த ராசிகளில் (2/12)')
]


def _bnn_link(planets, a, b):
    """The strongest Nadi link between two grahas, or None."""
    def signs(p):
        sign = planets[p]['sign_index']
        retro = planets[p].get('retrograde') and p not in ('Rahu', 'Ketu')
        return {sign, (sign - 1) % 12} if retro else {sign}
    distances = {(sb - sa) % 12 for sa in signs(a) for sb in signs(b)}
    for rank, (offsets, en, ta) in enumerate(BNN_LINKS):
        if distances & set(offsets):
            return rank, en, ta
    return None


def calculate_bhrigu_nandi_nadi(chart):
    planets = chart['planets']
    trine_map = {
        'dharma_fire': {'name_en': 'Dharma Trine (Fire: Aries, Leo, Sagittarius)', 'name_ta': 'தர்ம திரிகோணம் (நெருப்பு: மேஷம், சிம்மம், தனுசு)',
                        'name_ml': 'ധർമ്മ ത്രികോണം (അഗ്നി: മേടം, ചിങ്ങം, ധനു)', 'planets': []},
        'artha_earth': {'name_en': 'Artha Trine (Earth: Taurus, Virgo, Capricorn)', 'name_ta': 'அர்த்த திரிகோணம் (நிலம்: ரிஷபம், கன்னி, மகரம்)',
                        'name_ml': 'അർത്ഥ ത്രികോണം (ഭൂമി: ഇടവം, കന്നി, മകരം)', 'planets': []},
        'kama_air': {'name_en': 'Kama Trine (Air: Gemini, Libra, Aquarius)', 'name_ta': 'காம திரிகோணம் (காற்று: மிதுனம், துலாம், கும்பம்)',
                     'name_ml': 'കാമ ത്രികോണം (വായു: മിഥുനം, തുലാം, കുംഭം)', 'planets': []},
        'moksha_water': {'name_en': 'Moksha Trine (Water: Cancer, Scorpio, Pisces)', 'name_ta': 'மோட்ச திரிகோணம் (நீர்: கடகம், விருச்சிகம், மீனம்)',
                         'name_ml': 'മോക്ഷ ത്രികോണം (ജലം: കർക്കടകം, വൃശ്ചികം, മീനം)', 'planets': []}
    }

    p_names = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
    for p_name in p_names:
        s_idx = planets[p_name]['sign_index']
        if s_idx in (0, 4, 8): t_key = 'dharma_fire'
        elif s_idx in (1, 5, 9): t_key = 'artha_earth'
        elif s_idx in (2, 6, 10): t_key = 'kama_air'
        else: t_key = 'moksha_water'
        trine_map[t_key]['planets'].append({
            'name': p_name,
            'tamil': PLANET_TAMIL[p_name],
            'sign': planets[p_name]['sign'],
            'tamil_sign': planets[p_name]['tamil']
        })

    sutras = []
    for (a, b, title_en, title_ta, sig_en, sig_ta), (title_ml, sig_ml) in zip(BNN_SUTRAS, BNN_SUTRAS_ML):
        link = _bnn_link(planets, a, b)
        if link:
            rank, link_en, link_ta = link
            link_ml = BNN_LINKS_ML[rank]
            sutras.append({
                'title_en': title_en,
                'title_ta': title_ta,
                'title_ml': title_ml,
                'planets': [a, b],
                'link_rank': rank,
                'link_en': link_en,
                'link_ta': link_ta,
                'link_ml': link_ml,
                'significance_en': f"{a} and {b} are {link_en}. {sig_en}",
                'significance_ta': f"{PLANET_TAMIL[a]}, {PLANET_TAMIL[b]} {link_ta} உள்ளனர். {sig_ta}",
                'significance_ml': f"{PLANET_ML[a]}, {PLANET_ML[b]} {link_ml} നിൽക്കുന്നു. {sig_ml}"
            })
    sutras.sort(key=lambda x: x['link_rank'])  # conjunctions first, adjacent signs last

    if not sutras:
        sutras.append({
            'title_en': 'Pancha-Bhuta Balance (Nadi Alignment)',
            'title_ta': 'பஞ்சபூத சமநிலை (நாடி யோகம்)',
            'title_ml': 'പഞ്ചഭൂത സന്തുലനം (നാഡി യോഗം)',
            'significance_ml': 'ഗ്രഹങ്ങൾ ധർമ്മ, അർത്ഥ, കാമ, മോക്ഷ ത്രികോണങ്ങളിൽ സമമായി വ്യാപിച്ചിരിക്കുന്നതിനാൽ ജീവിതത്തിന്റെ എല്ലാ ഘട്ടങ്ങളിലും എളുപ്പം ഇണങ്ങി മുന്നേറാനുള്ള സന്തുലനം ലഭിക്കും.',
            'planets': ['Jupiter', 'Ascendant'],
            'significance_en': 'Planetary energies are evenly distributed across Dharma, Artha, Kama, and Moksha trines, bestowing a versatile life orientation that adapts skillfully across all worldly stages.',
            'significance_ta': 'கிரகங்கள் தர்ம, அர்த்த, காம, மோட்ச திரிகோணங்களில் சமச்சீராகப் பரவியுள்ளதால் வாழ்வின் அனைத்து நிலைகளிலும் எளிதில் பழகி முன்னேறும் சமநிலை வாய்க்கும்.'
        })

    return {
        'trines': trine_map,
        'sutras': sutras,
        'summary_en': f"Bhrigu Nandi Nadi reveals {len(sutras)} core karmic sutras anchored by Jeeva Karaka (Jupiter) and Karma Karaka (Saturn). Your primary life lessons and breakthroughs unfold through purposeful service and ethical expansion.",
        'summary_ml': f"ഭൃഗു നന്ദി നാഡി നിയമപ്രകാരം നിങ്ങളുടെ ജാതകത്തിൽ {len(sutras)} പ്രധാന കർമ്മ യോഗങ്ങൾ പ്രവർത്തിക്കുന്നു. ജീവകാരകനായ വ്യാഴത്തിന്റെയും കർമ്മകാരകനായ ശനിയുടെയും സ്ഥിതികൾ അധ്വാനത്താലും ധർമ്മമാർഗ്ഗത്താലും നിങ്ങളെ ജീവിതത്തിന്റെ ഉന്നതിയിലെത്തിക്കും.",
        'summary_ta': f"பிருகு நந்தி நாடி விதிகளின்படி உங்கள் ஜாதகத்தில் {len(sutras)} முதன்மை கர்ம யோகங்கள் செயல்படுகின்றன. ஜீவகாரகன் (குரு) மற்றும் கர்மகாரகன் (சனி) அமைப்புகள் உழைப்பாலும் தர்ம நெறியாலும் உங்கள் வாழ்வின் உச்சத்தை அடையச் செய்யும்."
    }

# 4. PLANETARY AVASTHAS & FRUITION POTENCY
# Lajjitadi avasthas (BPHS): the mood in which a graha gives the results of its house
LAJJITADI = {
    'Lajjita': ('Lajjita (Ashamed)', 'லஜ்ஜித (வெட்கம்)', -1,
                'In the 5th house with Rahu, Ketu, the Sun, Saturn or Mars: it hesitates to give its results fully.',
                '5-ஆம் பாவத்தில் ராகு, கேது, சூரியன், சனி அல்லது செவ்வாயுடன் உள்ளதால் முழுப் பலனைத் தயக்கத்துடன் தரும்.'),
    'Garvita': ('Garvita (Proud)', 'கர்வித (பெருமிதம்)', 1,
                'Exalted or in its Moolatrikona: it gives prosperity, comforts and success in its matters.',
                'உச்சம் அல்லது மூலத்திரிகோணத்தில் உள்ளதால் செல்வம், சுகம் மற்றும் காரிய வெற்றி தரும்.'),
    'Kshudita': ('Kshudita (Starved)', 'க்ஷுதித (பசி)', -1,
                 'In an enemy\'s sign, with or aspected by an enemy, or joined by Saturn: its results come with want and worry.',
                 'பகை வீட்டில், பகைவருடன் சேர்ந்து அல்லது பகைவர் பார்வையில், அல்லது சனியுடன் உள்ளதால் பலன்கள் குறைவுடனும் கவலையுடனும் வரும்.'),
    'Trushita': ('Trushita (Thirsty)', 'த்ருஷித (தாகம்)', -1,
                 'In a watery sign, aspected by a malefic and by no benefic: its results are delayed and leave one wanting.',
                 'நீர் ராசியில் பாப கிரகப் பார்வை பெற்று சுபப் பார்வை இல்லாததால் பலன்கள் தாமதமாகி நிறைவின்றி இருக்கும்.'),
    'Mudita': ('Mudita (Delighted)', 'முதித (மகிழ்ச்சி)', 1,
               'In a friend\'s sign, with or aspected by a friend, or joined by Jupiter: it gives happiness and gains.',
               'நட்பு வீட்டில், நண்பருடன் சேர்ந்து அல்லது நண்பர் பார்வையில், அல்லது குருவுடன் உள்ளதால் மகிழ்ச்சியும் லாபமும் தரும்.'),
    'Kshobhita': ('Kshobhita (Agitated)', 'க்ஷோபித (கலக்கம்)', -1,
                  'Joined by the Sun and aspected by a malefic or an enemy: its results come amid agitation and loss.',
                  'சூரியனுடன் சேர்ந்து பாப அல்லது பகை கிரகப் பார்வை பெற்றதால் பலன்கள் கலக்கத்துடனும் இழப்புடனும் வரும்.')
}
LAJJITADI_ML = {
    'Lajjita': ('ലജ്ജിത (ലജ്ജ)', '5-ാം ഭാവത്തിൽ രാഹു, കേതു, സൂര്യൻ, ശനി അല്ലെങ്കിൽ ചൊവ്വയോടൊപ്പം നിൽക്കുന്നതിനാൽ ഫലം പൂർണ്ണമായി നൽകാൻ മടിക്കും.'),
    'Garvita': ('ഗർവിത (അഭിമാനം)', 'ഉച്ചത്തിലോ മൂലത്രികോണത്തിലോ നിൽക്കുന്നതിനാൽ ഐശ്വര്യവും സുഖവും കാര്യവിജയവും നൽകും.'),
    'Kshudita': ('ക്ഷുധിത (വിശപ്പ്)', 'ശത്രുക്ഷേത്രത്തിലോ ശത്രുവിനോടൊപ്പമോ ശത്രുദൃഷ്ടിയിലോ ശനിയോടൊപ്പമോ നിൽക്കുന്നതിനാൽ ഫലങ്ങൾ കുറവോടെയും ആകുലതയോടെയും വരും.'),
    'Trushita': ('തൃഷിത (ദാഹം)', 'ജലരാശിയിൽ പാപഗ്രഹദൃഷ്ടിയുണ്ടായി ശുഭദൃഷ്ടിയില്ലാത്തതിനാൽ ഫലങ്ങൾ വൈകുകയും തൃപ്തിയില്ലാതിരിക്കുകയും ചെയ്യും.'),
    'Mudita': ('മുദിത (സന്തോഷം)', 'മിത്രക്ഷേത്രത്തിലോ മിത്രത്തോടൊപ്പമോ മിത്രദൃഷ്ടിയിലോ വ്യാഴത്തോടൊപ്പമോ നിൽക്കുന്നതിനാൽ സന്തോഷവും ലാഭവും നൽകും.'),
    'Kshobhita': ('ക്ഷോഭിത (കലക്കം)', 'സൂര്യനോടൊപ്പം നിന്ന് പാപ/ശത്രു ഗ്രഹദൃഷ്ടിയുള്ളതിനാൽ ഫലങ്ങൾ കലക്കത്തോടെയും നഷ്ടത്തോടെയും വരും.'),
}
WATERY_SIGNS = (3, 7, 11)


def lajjitadi_avasthas(p_name, planets):
    """The Lajjitadi states of a graha, judged by rasi (sign) conjunction and Parashari aspect."""
    from ..engine import NATURAL_FRIENDS
    p = planets[p_name]
    friends = NATURAL_FRIENDS[p_name]
    with_it = [q for q in ('Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu')
               if q != p_name and planets[q]['sign_index'] == p['sign_index']]
    aspected_by = [q for q in p.get('aspects_received', []) if q != 'Ascendant']
    malefics = ('Sun', 'Mars', 'Saturn', 'Rahu', 'Ketu')
    sign_lord = SIGN_LORDS[p['sign_index']]
    enemy = lambda q: friends.get(q, 0) < 0
    friend = lambda q: friends.get(q, 0) > 0
    states = []
    if p['house'] == 5 and any(q in ('Rahu', 'Ketu', 'Sun', 'Saturn', 'Mars') for q in with_it):
        states.append('Lajjita')
    if p.get('dignity') in ('Exalted', 'Moolatrikona'):
        states.append('Garvita')
    if ((sign_lord != p_name and enemy(sign_lord)) or any(enemy(q) for q in with_it + aspected_by)
            or 'Saturn' in with_it):
        states.append('Kshudita')
    if (p['sign_index'] in WATERY_SIGNS and any(q in malefics for q in aspected_by)
            and not any(q in NATURAL_BENEFICS for q in aspected_by)):
        states.append('Trushita')
    if ((sign_lord != p_name and friend(sign_lord)) or any(friend(q) for q in with_it + aspected_by)
            or 'Jupiter' in with_it):
        states.append('Mudita')
    if 'Sun' in with_it and any(q in malefics or enemy(q) for q in aspected_by):
        states.append('Kshobhita')
    return [dict(key=k, en=LAJJITADI[k][0], ta=LAJJITADI[k][1], effect=LAJJITADI[k][2],
                 reading_en=LAJJITADI[k][3], reading_ta=LAJJITADI[k][4],
                 ml=LAJJITADI_ML[k][0], reading_ml=LAJJITADI_ML[k][1]) for k in states]


def calculate_planetary_avasthas(chart):
    planets = chart['planets']
    avastha_list = []
    
    for p_name in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']:
        p = planets[p_name]
        deg = p['degree']
        s_idx = p['sign_index']
        is_odd = (s_idx % 2 == 0)
        dignity = p.get('dignity', 'Neutral')

        if is_odd:
            if deg < 6.0: b_en = 'Bala (Infant)'; b_ta = 'பால அவஸ்தை (குழந்தை)'; b_pct = 25
            elif deg < 12.0: b_en = 'Kumara (Youth)'; b_ta = 'குமார அவஸ்தை (இளைஞன்)'; b_pct = 50
            elif deg < 18.0: b_en = 'Yuva (Adult / Prime)'; b_ta = 'யுவ அவஸ்தை (முழு பலம்)'; b_pct = 100
            elif deg < 24.0: b_en = 'Vriddha (Old / Mature)'; b_ta = 'விருத்த அவஸ்தை (முதியவர்)'; b_pct = 10
            else: b_en = 'Mrita (Dead / Dormant)'; b_ta = 'மிருத அவஸ்தை (செயலற்றது)'; b_pct = 0
        else:
            if deg < 6.0: b_en = 'Mrita (Dead / Dormant)'; b_ta = 'மிருத அவஸ்தை (செயலற்றது)'; b_pct = 0
            elif deg < 12.0: b_en = 'Vriddha (Old / Mature)'; b_ta = 'விருத்த அவஸ்தை (முதியவர்)'; b_pct = 10
            elif deg < 18.0: b_en = 'Yuva (Adult / Prime)'; b_ta = 'யுவ அவஸ்தை (முழு பலம்)'; b_pct = 100
            elif deg < 24.0: b_en = 'Kumara (Youth)'; b_ta = 'குமார அவஸ்தை (இளைஞன்)'; b_pct = 50
            else: b_en = 'Bala (Infant)'; b_ta = 'பால அவஸ்தை (குழந்தை)'; b_pct = 25

        if 'Own' in dignity or 'Exalted' in dignity or 'Moolatrikona' in dignity:
            j_en = 'Jagrat (Awake / Alert)'; j_ta = 'ஜாக்ரத் (விழித்த நிலை)'; j_pct = 100
        elif 'Debilitated' in dignity or 'Enemy' in dignity:
            j_en = 'Sushupti (Sleeping / Dormant)'; j_ta = 'சுஷுப்தி (உறங்கும் நிலை)'; j_pct = 25
        else:
            j_en = 'Swapna (Dreaming / Contemplative)'; j_ta = 'ஸ்வப்ன (கனவு நிலை)'; j_pct = 60

        b_ml = {'Bala (Infant)': 'ബാല അവസ്ഥ (ശിശു)', 'Kumara (Youth)': 'കുമാര അവസ്ഥ (യുവാവ്)', 'Yuva (Adult / Prime)': 'യുവ അവസ്ഥ (പൂർണ്ണ ബലം)', 'Vriddha (Old / Mature)': 'വൃദ്ധ അവസ്ഥ (വൃദ്ധൻ)', 'Mrita (Dead / Dormant)': 'മൃത അവസ്ഥ (നിഷ്ക്രിയം)'}[b_en]
        j_ml = {'Jagrat (Awake / Alert)': 'ജാഗ്രത് (ഉണർന്ന നില)', 'Sushupti (Sleeping / Dormant)': 'സുഷുപ്തി (ഉറങ്ങുന്ന നില)', 'Swapna (Dreaming / Contemplative)': 'സ്വപ്ന (സ്വപ്ന നില)'}[j_en]
        fruit_potency = round((b_pct * 0.6) + (j_pct * 0.4))
        moods = lajjitadi_avasthas(p_name, planets)

        avastha_list.append({
            'planet': p_name,
            'planet_ta': PLANET_TAMIL[p_name],
            'degree_str': f"{int(deg)}° {int((deg*60)%60):02d}′",
            'baladi': b_en,
            'baladi_ta': b_ta,
            'baladi_pct': b_pct,
            'jagradadi': j_en,
            'jagradadi_ta': j_ta,
            'baladi_ml': b_ml,
            'jagradadi_ml': j_ml,
            'fruit_potency': fruit_potency,
            'lajjitadi': moods,
            'interpretation_en': f"Operating in {b_en} and {j_en}. Manifests approximately {fruit_potency}% of its innate planetary potential in physical life events.",
            'interpretation_ta': f"{b_ta} மற்றும் {j_ta} நிலையில் உள்ளதால், தனது இயற்கை காரகத்துவங்களில் சுமார் {fruit_potency}% முழு பலன்களை நடைமுறை வாழ்வில் வழங்கும்.",
            'interpretation_ml': f"{b_ml}, {j_ml} എന്നീ നിലകളിലായതിനാൽ സ്വാഭാവിക കാരകത്വത്തിന്റെ ഏകദേശം {fruit_potency}% ഫലം പ്രായോഗിക ജീവിതത്തിൽ നൽകും."
        })

    return {'avasthas': avastha_list}

# 5. NAKSHATRA PADA DEEP READINGS
def calculate_nakshatra_pada_reading(chart):
    moon = chart['planets']['Moon']
    star = moon['nakshatra']
    star_ta = moon['tamil_nakshatra']
    pada = moon['pada']
    nav_idx = moon['navamsa']  # the Navamsa sign index of the Moon's pada
    nav_sign = SIGNS[nav_idx]
    nav_ta = TAMIL_SIGNS[nav_idx]
    pada_lord = SIGN_LORDS[nav_idx]

    elements = ['Fire', 'Earth', 'Air', 'Water']
    elements_ta = ['நெருப்பு', 'நிலம்', 'காற்று', 'நீர்']
    elem = elements[nav_idx % 4]
    elem_ta = elements_ta[nav_idx % 4]
    elem_ml = ['അഗ്നി', 'ഭൂമി', 'വായു', 'ജലം'][nav_idx % 4]
    star_ml = MALAYALAM_STARS[STARS.index(star)]
    nav_ml = MALAYALAM_SIGNS[nav_idx]
    lord_ml = PLANET_ML[pada_lord]
    pada_ml = {
        1: f"{star_ml} നക്ഷത്രം 1-ാം പാദം (ധർമ്മ പാദം). നവാംശത്തിൽ {nav_ml} രാശിയിൽ {lord_ml} ആധിപത്യത്തിൽ. ഉന്മേഷവും നേതൃശേഷിയും എന്തിലും മുന്നിൽ നിൽക്കാനുള്ള ധൈര്യവും ഉണ്ട്. പുതിയ സംരംഭങ്ങൾ തുടങ്ങി വിജയകരമായി പൂർത്തിയാക്കും.",
        2: f"{star_ml} നക്ഷത്രം 2-ാം പാദം (അർത്ഥ പാദം). നവാംശത്തിൽ {nav_ml} രാശിയിൽ {lord_ml} ആധിപത്യത്തിൽ. ക്ഷമയും സംയമനവും ആസൂത്രിതമായ അധ്വാനവും സമ്പാദ്യശീലവും ഉണ്ട്. കുടുംബത്തിൽ സമാധാനവും സ്ഥിരമായ സ്വത്തുസമ്പാദനവും ലഭിക്കും.",
        3: f"{star_ml} നക്ഷത്രം 3-ാം പാദം (കാമ പാദം). നവാംശത്തിൽ {nav_ml} രാശിയിൽ {lord_ml} ആധിപത്യത്തിൽ. സമർത്ഥമായ സംസാരവും അറിവുതേടലും കലാതാൽപ്പര്യവും സുഹൃദ്‌വലയത്തിൽ സ്വാധീനവും ഉണ്ട്. ആശയവിനിമയത്തിലും വ്യാപാരത്തിലും തിളങ്ങും.",
        4: f"{star_ml} നക്ഷത്രം 4-ാം പാദം (മോക്ഷ പാദം). നവാംശത്തിൽ {nav_ml} രാശിയിൽ {lord_ml} ആധിപത്യത്തിൽ. കരുണയും ഉൾക്കാഴ്ചയും ആത്മീയ താൽപ്പര്യവും ത്യാഗമനോഭാവവും ഉണ്ട്. മറ്റുള്ളവരെ സഹായിക്കുന്ന മനസ്സിനാൽ ജനപിന്തുണ ലഭിക്കും.",
    }

    pada_forecasts = {
        1: {
            'en': f"Born in Pada 1 of {star} (Dharma Quarter). Governed by Navamsa in {nav_sign} ({pada_lord}). Bestows high ambition, fiery determination, self-reliance, and pioneering spirit. You are energized by initiating new projects and upholding high moral standards.",
            'ta': f"{star_ta} நட்சத்திரம் 1-ஆம் பாதம் (தர்ம பாதம்). நவாம்சத்தில் {nav_ta} ராசியில் {PLANET_TAMIL[pada_lord]} ஆதிக்கத்தில் இயங்குகிறது. சுறுசுறுப்பும், தலைமை ஏற்கும் ஆற்றலும், எதிலும் முதன்மையாக இருக்கும் துணிச்சலும் உண்டு. புதிய முயற்சிகளைத் தொடங்கி வெற்றிகரமாக முடிப்பீர்கள்."
        },
        2: {
            'en': f"Born in Pada 2 of {star} (Artha Quarter). Governed by Navamsa in {nav_sign} ({pada_lord}). Bestows practical perseverance, financial prudence, stability, and aesthetic appreciation. You build wealth methodically and prize security in both career and home.",
            'ta': f"{star_ta} நட்சத்திரம் 2-ஆம் பாதம் (அர்த்த பாதம்). நவாம்சத்தில் {nav_ta} ராசியில் {PLANET_TAMIL[pada_lord]} ஆதிக்கத்தில் இயங்குகிறது. பொறுமை, நிதானம், திட்டமிட்டு உழைக்கும் குணம் மற்றும் பொருளாதாரச் சேமிப்பு ஆர்வம் உண்டு. குடும்பத்தில் அமைதியும் நிலையான சொத்து சேர்க்கையும் கிட்டும்."
        },
        3: {
            'en': f"Born in Pada 3 of {star} (Kama Quarter). Governed by Navamsa in {nav_sign} ({pada_lord}). Bestows intellectual curiosity, communication eloquence, social charm, and artistic finesse. You thrive in networking, trade, writing, and creative associations.",
            'ta': f"{star_ta} நட்சத்திரம் 3-ஆம் பாதம் (காம பாதம்). நவாம்சத்தில் {nav_ta} ராசியில் {PLANET_TAMIL[pada_lord]} ஆதிக்கத்தில் இயங்குகிறது. சாதுரியமான பேச்சு, அறிவுத் தேடல், கலை ஆர்வம் மற்றும் நட்பு வட்டாரத்தில் செல்வாக்கு உண்டு. தகவல் தொடர்பு மற்றும் வியாபாரத்தில் பிரகாசிப்பீர்கள்."
        },
        4: {
            'en': f"Born in Pada 4 of {star} (Moksha Quarter). Governed by Navamsa in {nav_sign} ({pada_lord}). Bestows deep emotional empathy, intuitive perception, spiritual depth, and compassion. You possess natural healing sensitivity and an innate quest for inner peace.",
            'ta': f"{star_ta} நட்சத்திரம் 4-ஆம் பாதம் (மோட்ச பாதம்). நவாம்சத்தில் {nav_ta} ராசியில் {PLANET_TAMIL[pada_lord]} ஆதிக்கத்தில் இயங்குகிறது. இரக்க குணம், உள்ளுணர்வுத் தெளிவு, ஆன்மீக ஈடுபாடு மற்றும் தியாக மனப்பான்மை உண்டு. பிறருக்கு உதவும் நல்லெண்ணத்தால் மக்கள் ஆதரவு பெறுவீர்கள்."
        }
    }

    f = pada_forecasts.get(pada, pada_forecasts[1])
    return {
        'nakshatra': star,
        'tamil_nakshatra': star_ta,
        'pada': pada,
        'navamsa_sign': nav_sign,
        'navamsa_ta': nav_ta,
        'pada_lord': pada_lord,
        'pada_lord_ta': PLANET_TAMIL[pada_lord],
        'element': elem,
        'element_ta': elem_ta,
        'element_ml': elem_ml,
        'navamsa_ml': nav_ml,
        'pada_lord_ml': lord_ml,
        'reading_en': f['en'],
        'reading_ta': f['ta'],
        'reading_ml': pada_ml.get(pada, pada_ml[1])
    }

# 6. SENSITIVE SAHAMS (TAJIKA & PARASHARA COSMIC POINTS)
# Tajika Neelakanthi formulas A - B + C (C is the Lagna): by night A and B swap where marked.
# When C does not lie on the way from B to A, 30° is added.
SAHAMS = [
    ('Punya Saham', 'புண்ணிய சஹமம்', 'Moon', 'Sun', True, 'Fortune & Divine Merit', 'அதிர்ஷ்டம் & பூர்வ புண்ணியம்',
     'The point of grace and fortune: sudden favourable turns of fate, spiritual merit and virtuous prosperity.',
     'தெய்வ அனுகூலம் மற்றும் பூர்வ புண்ணியத்தின் புள்ளி: எதிர்பாராத அதிர்ஷ்டம், தர்ம சிந்தனை மற்றும் நேர்மையான செல்வம்.'),
    ('Vidya Saham', 'வித்யா சஹமம்', 'Sun', 'Moon', True, 'Education & Learning', 'கல்வி & ஞானம்',
     'The point of learning: scholarship, examinations, analytical depth and quick comprehension.',
     'கல்வியின் புள்ளி: படிப்பு, தேர்வுகள், ஆராய்ச்சி அறிவு மற்றும் விரைவான புரிதல்.'),
    ('Vivaha Saham', 'விவாக சஹமம்', 'Venus', 'Saturn', True, 'Marriage', 'திருமணம்',
     'The point of marriage: the timing of the wedding, harmony with the spouse and lasting devotion.',
     'திருமணத்தின் புள்ளி: திருமண காலம், துணைவருடன் நல்லிணக்கம் மற்றும் நீடித்த அன்பு.'),
    ('Putra Saham', 'புத்திர சஹமம்', 'Jupiter', 'Moon', True, 'Children', 'புத்திர பாக்கியம்',
     'The point of children: the blessing of progeny and joy through them.',
     'குழந்தைப் பேற்றின் புள்ளி: புத்திர பாக்கியமும் அவர்களால் உண்டாகும் மகிழ்ச்சியும்.'),
    ('Karma Saham', 'கர்ம சஹமம்', 'Mars', 'Mercury', True, 'Work & Career', 'தொழில் & கர்மம்',
     'The point of work: professional effort, standing at work and the results of one\'s deeds.',
     'தொழிலின் புள்ளி: பணி முயற்சி, பணியிட அந்தஸ்து மற்றும் செய்த கர்மங்களின் பலன்.'),
    ('Artha Saham', 'அர்த்த சஹமம்', '2nd house', '2nd lord', False, 'Money', 'பணம்',
     'The point of money: earnings, savings and the flow of wealth.',
     'பணத்தின் புள்ளி: வருமானம், சேமிப்பு மற்றும் செல்வ வரவு.'),
    ('Vanika Saham', 'வணிக சஹமம்', 'Moon', 'Mercury', True, 'Commerce', 'வணிகம்',
     'The point of commerce: trade, business dealings and mercantile success.',
     'வணிகத்தின் புள்ளி: வியாபாரம், கொடுக்கல் வாங்கல் மற்றும் வர்த்தக வெற்றி.'),
    ('Samartha Saham', 'சாமர்த்திய சஹமம்', 'Mars', 'Lagna lord', True, 'Ability & Enterprise', 'திறமை & முயற்சி',
     'The point of capability: initiative, competence and the drive to accomplish.',
     'திறமையின் புள்ளி: முனைப்பு, செயல்திறன் மற்றும் காரியங்களைச் சாதிக்கும் ஆற்றல்.'),
    ('Roga Saham', 'ரோக சஹமம்', 'Lagna', 'Moon', False, 'Health & Disease', 'உடல் நலம் & நோய்',
     'The point of illness: where health needs care and how resilient the body is.',
     'நோயின் புள்ளி: உடல் நலத்தில் கவனம் தேவைப்படும் இடமும் உடலின் எதிர்ப்பு சக்தியும்.')
]

# Malayalam for each saham: (name, keyword, reading)
SAHAMS_ML = {
    'Punya Saham': ('പുണ്യ സഹം', 'ഭാഗ്യം & പൂർവ്വപുണ്യം', 'ദൈവാനുഗ്രഹത്തിന്റെയും പൂർവ്വപുണ്യത്തിന്റെയും ബിന്ദു: അപ്രതീക്ഷിത ഭാഗ്യം, ധർമ്മചിന്ത, സത്യസന്ധമായ സമ്പത്ത്.'),
    'Vidya Saham': ('വിദ്യാ സഹം', 'വിദ്യ & ജ്ഞാനം', 'വിദ്യയുടെ ബിന്ദു: പഠനം, പരീക്ഷകൾ, വിശകലനശേഷി, വേഗത്തിലുള്ള ഗ്രാഹ്യം.'),
    'Vivaha Saham': ('വിവാഹ സഹം', 'വിവാഹം', 'വിവാഹത്തിന്റെ ബിന്ദു: വിവാഹകാലം, പങ്കാളിയുമായുള്ള ഐക്യം, നിലനിൽക്കുന്ന സ്നേഹം.'),
    'Putra Saham': ('പുത്ര സഹം', 'സന്താനഭാഗ്യം', 'സന്താനങ്ങളുടെ ബിന്ദു: സന്താനഭാഗ്യവും അവരിലൂടെയുള്ള സന്തോഷവും.'),
    'Karma Saham': ('കർമ്മ സഹം', 'തൊഴിൽ & കർമ്മം', 'തൊഴിലിന്റെ ബിന്ദു: ജോലിയിലെ പ്രയത്നം, ജോലിസ്ഥലത്തെ പദവി, ചെയ്ത കർമ്മങ്ങളുടെ ഫലം.'),
    'Artha Saham': ('അർത്ഥ സഹം', 'ധനം', 'ധനത്തിന്റെ ബിന്ദു: വരുമാനം, സമ്പാദ്യം, ധനാഗമനം.'),
    'Vanika Saham': ('വാണിജ്യ സഹം', 'വ്യാപാരം', 'വ്യാപാരത്തിന്റെ ബിന്ദു: കച്ചവടം, കൊടുക്കൽ-വാങ്ങൽ, വാണിജ്യ വിജയം.'),
    'Samartha Saham': ('സാമർത്ഥ്യ സഹം', 'കഴിവ് & സംരംഭം', 'കഴിവിന്റെ ബിന്ദു: മുൻകൈ, പ്രവർത്തനക്ഷമത, കാര്യങ്ങൾ സാധിക്കാനുള്ള ഉത്സാഹം.'),
    'Roga Saham': ('രോഗ സഹം', 'ആരോഗ്യം & രോഗം', 'രോഗത്തിന്റെ ബിന്ദു: ആരോഗ്യത്തിൽ ശ്രദ്ധ വേണ്ട മേഖലയും ശരീരത്തിന്റെ പ്രതിരോധശേഷിയും.'),
}


def _saham(a, b, c):
    """A - B + C, plus 30° when C does not fall on the way from B to A."""
    value = a - b + c
    if (c - b) % 360 > (a - b) % 360:
        value += 30
    return value % 360


def calculate_sahams(chart):
    planets = chart['planets']
    asc_lon = planets['Ascendant']['longitude']
    asc_sign = planets['Ascendant']['sign_index']
    # By day the Sun is above the horizon: on the ecliptic arc from the Descendant up to the Ascendant
    is_day = (asc_lon - planets['Sun']['longitude']) % 360 < 180
    lagna_lord = SIGN_LORDS[asc_sign]
    second_lord = SIGN_LORDS[(asc_sign + 1) % 12]
    points = {name: planets[name]['longitude'] for name in ('Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn')}
    points.update({'Lagna': asc_lon, '2nd house': (asc_lon + 30) % 360, '2nd lord': planets[second_lord]['longitude'],
                   'Lagna lord': planets[lagna_lord]['longitude']})

    sahams_list = []
    for en_title, ta_title, a, b, reverses, kw_en, kw_ta, r_en, r_ta in SAHAMS:
        swap = reverses and not is_day
        if en_title == 'Samartha Saham' and lagna_lord == 'Mars':
            a, b, swap = 'Jupiter', 'Mars', not swap  # Mars owning the Lagna: Jupiter - Mars + Lagna
        if swap:
            a, b = b, a
        lon = _saham(points[a], points[b], asc_lon)
        s_idx = int(lon // 30)
        deg = lon % 30
        house = (s_idx - asc_sign) % 12 + 1
        lord = SIGN_LORDS[s_idx]
        lord_house = planets[lord]['house']
        lord_dignity = planets[lord].get('dignity', 'Neutral')
        if lord_house in DUSTHANAS or lord_dignity == 'Debilitated':
            strength, note_en, note_ta, note_ml = 'weak', 'needs strengthening', 'பலப்படுத்த வேண்டியது', 'ബലപ്പെടുത്തേണ്ടതാണ്'
        elif lord_house in KENDRAS + TRIKONAS + (11,) and DIGNITY_SCORE.get(lord_dignity, 0) >= 0:
            strength, note_en, note_ta, note_ml = 'strong', 'well supported', 'நல்ல ஆதரவுடன் உள்ளது', 'നല്ല പിന്തുണയോടെയാണ്'
        else:
            strength, note_en, note_ta, note_ml = 'moderate', 'moderately supported', 'மிதமான ஆதரவுடன் உள்ளது', 'മിതമായ പിന്തുണയോടെയാണ്'
        malefics = [q for q in ('Saturn', 'Mars', 'Rahu', 'Ketu') if planets[q]['sign_index'] == s_idx]
        affliction_en = f" {', '.join(malefics)} in the same sign afflicts it." if malefics else ''
        affliction_ta = f" அதே ராசியில் உள்ள {', '.join(PLANET_TAMIL[q] for q in malefics)} இதைப் பாதிக்கிறது." if malefics else ''
        affliction_ml = f" അതേ രാശിയിലുള്ള {', '.join(PLANET_ML[q] for q in malefics)} ഇതിനെ ബാധിക്കുന്നു." if malefics else ''
        name_ml, kw_ml, r_ml = SAHAMS_ML[en_title]
        d = int(deg); m = int((deg * 60) % 60)
        sahams_list.append({
            'name_en': en_title,
            'name_ta': ta_title,
            'formula': f"{a} - {b} + Lagna",
            'longitude': round(lon, 2),
            'degree_str': f"{d}° {m:02d}′",
            'sign': SIGNS[s_idx],
            'tamil_sign': TAMIL_SIGNS[s_idx],
            'house': house,
            'lord': lord,
            'lord_ta': PLANET_TAMIL[lord],
            'lord_house': lord_house,
            'strength': strength,
            'keyword_en': kw_en,
            'keyword_ta': kw_ta,
            'name_ml': name_ml,
            'keyword_ml': kw_ml,
            'malayalam_sign': MALAYALAM_SIGNS[s_idx],
            'lord_ml': PLANET_ML[lord],
            'reading_ml': (f"{r_ml} ഇത് {house}-ാം ഭാവമായ {MALAYALAM_SIGNS[s_idx]} രാശിയിൽ വീഴുന്നു; അതിന്റെ അധിപനായ "
                           f"{PLANET_ML[lord]} {lord_house}-ാം ഭാവത്തിൽ നിൽക്കുന്നതിനാൽ ഈ ജീവിതമേഖല {note_ml}.{affliction_ml}"),
            'reading_en': (f"{r_en} It falls in {SIGNS[s_idx]}, the {_ordinal(house)} house; its lord {lord} sits in the "
                           f"{_ordinal(lord_house)} house, so this area of life is {note_en}.{affliction_en}"),
            'reading_ta': (f"{r_ta} இது {house}-ஆம் பாவமான {TAMIL_SIGNS[s_idx]} ராசியில் விழுகிறது; அதன் அதிபதி "
                           f"{PLANET_TAMIL[lord]} {lord_house}-ஆம் பாவத்தில் இருப்பதால் இந்த வாழ்க்கைத் துறை {note_ta}.{affliction_ta}")
        })

    return {
        'is_day_birth': is_day,
        'birth_type_en': 'Diurnal (Day Birth)' if is_day else 'Nocturnal (Night Birth)',
        'birth_type_ta': 'பகல் பிறப்பு' if is_day else 'இரவு பிறப்பு',
        'birth_type_ml': 'പകൽ ജനനം' if is_day else 'രാത്രി ജനനം',
        'sahams': sahams_list
    }

# PANCHANGA PHALA: the birth weekday, tithi, nitya yoga and karana
VAARA_PHALA = [
    ('Born on a Sunday, ruled by the Sun: self-respecting, courageous and ambitious, with a strong sense of duty and leadership; pride and a quick temper need watching.',
     'ஞாயிற்றுக்கிழமை பிறந்தவர் (சூரியன் ஆதிக்கம்): சுயமரியாதை, துணிவு, லட்சியம், கடமை உணர்வு மற்றும் தலைமைப் பண்பு உடையவர்; கர்வத்தையும் முன்கோபத்தையும் கவனிக்க வேண்டும்.'),
    ('Born on a Monday, ruled by the Moon: gentle, sensitive and imaginative, caring and sociable, fond of travel and comfort; moods can change quickly.',
     'திங்கட்கிழமை பிறந்தவர் (சந்திரன் ஆதிக்கம்): மென்மை, உணர்திறன், கற்பனைத் திறன் கொண்டவர்; அன்பும் அக்கறையும், பயணம் மற்றும் சுகங்களில் விருப்பம்; மனநிலை விரைவில் மாறக்கூடும்.'),
    ('Born on a Tuesday, ruled by Mars: energetic, bold and enterprising, a natural fighter who stands up for others; haste and anger need restraint.',
     'செவ்வாய்க்கிழமை பிறந்தவர் (செவ்வாய் ஆதிக்கம்): சுறுசுறுப்பு, துணிச்சல், முயற்சி உடையவர்; பிறருக்காகப் போராடும் இயல்பு; அவசரமும் கோபமும் கட்டுப்படுத்த வேண்டும்.'),
    ('Born on a Wednesday, ruled by Mercury: intelligent, articulate and witty, quick to learn, and skilled in trade, writing and calculation.',
     'புதன்கிழமை பிறந்தவர் (புதன் ஆதிக்கம்): அறிவுக்கூர்மை, பேச்சுத்திறன், நகைச்சுவை உணர்வு; விரைவாகக் கற்பவர்; வணிகம், எழுத்து, கணக்கில் திறமைசாலி.'),
    ('Born on a Thursday, ruled by Jupiter: wise, principled and generous, respected as a teacher or counsellor, with a spiritual bent.',
     'வியாழக்கிழமை பிறந்தவர் (குரு ஆதிக்கம்): ஞானம், நேர்மை, தாராள மனம் கொண்டவர்; ஆசிரியராக அல்லது ஆலோசகராக மதிக்கப்படுபவர்; ஆன்மீக நாட்டம் உண்டு.'),
    ('Born on a Friday, ruled by Venus: charming and artistic, fond of beauty, comfort and harmony, blessed with a happy family life.',
     'வெள்ளிக்கிழமை பிறந்தவர் (சுக்கிரன் ஆதிக்கம்): வசீகரம், கலை ரசனை கொண்டவர்; அழகு, சுகம், இணக்கத்தை விரும்புபவர்; மகிழ்ச்சியான குடும்ப வாழ்க்கை அமையும்.'),
    ('Born on a Saturday, ruled by Saturn: patient, disciplined and hardworking; success comes steadily through perseverance, often after early struggles.',
     'சனிக்கிழமை பிறந்தவர் (சனி ஆதிக்கம்): பொறுமை, ஒழுக்கம், கடின உழைப்பு உடையவர்; தொடக்கத்தில் போராட்டங்கள் இருந்தாலும் விடாமுயற்சியால் படிப்படியாக வெற்றி பெறுவார்.')
]
VAARA_PHALA_ML = [
    'ഞായറാഴ്ച ജനനം (സൂര്യന്റെ ആധിപത്യം): ആത്മാഭിമാനം, ധൈര്യം, ലക്ഷ്യബോധം, കർത്തവ്യബോധം, നേതൃഗുണം എന്നിവയുണ്ട്; അഹങ്കാരവും മുൻകോപവും ശ്രദ്ധിക്കണം.',
    'തിങ്കളാഴ്ച ജനനം (ചന്ദ്രന്റെ ആധിപത്യം): സൗമ്യത, വൈകാരികത, ഭാവനാശേഷി; സ്നേഹവും കരുതലും, യാത്രയിലും സുഖങ്ങളിലും താൽപ്പര്യം; മനോഭാവം വേഗം മാറാം.',
    'ചൊവ്വാഴ്ച ജനനം (ചൊവ്വയുടെ ആധിപത്യം): ഉന്മേഷം, ധീരത, സംരംഭകത്വം; മറ്റുള്ളവർക്കായി പോരാടുന്ന സ്വഭാവം; തിടുക്കവും കോപവും നിയന്ത്രിക്കണം.',
    'ബുധനാഴ്ച ജനനം (ബുധന്റെ ആധിപത്യം): ബുദ്ധിശക്തി, വാക്ചാതുര്യം, നർമ്മബോധം; വേഗത്തിൽ പഠിക്കും; വ്യാപാരം, എഴുത്ത്, കണക്ക് എന്നിവയിൽ സമർത്ഥൻ.',
    'വ്യാഴാഴ്ച ജനനം (വ്യാഴത്തിന്റെ ആധിപത്യം): ജ്ഞാനം, സത്യസന്ധത, ഉദാരമനസ്സ്; അധ്യാപകനായോ ഉപദേശകനായോ ആദരിക്കപ്പെടും; ആത്മീയ താൽപ്പര്യമുണ്ട്.',
    'വെള്ളിയാഴ്ച ജനനം (ശുക്രന്റെ ആധിപത്യം): ആകർഷണീയത, കലാസ്വാദനം; സൗന്ദര്യം, സുഖം, ഐക്യം എന്നിവ ഇഷ്ടപ്പെടും; സന്തോഷകരമായ കുടുംബജീവിതം ലഭിക്കും.',
    'ശനിയാഴ്ച ജനനം (ശനിയുടെ ആധിപത്യം): ക്ഷമ, അച്ചടക്കം, കഠിനാധ്വാനം; തുടക്കത്തിൽ പ്രയാസങ്ങളുണ്ടായാലും സ്ഥിരോത്സാഹത്താൽ ക്രമേണ വിജയം നേടും.',
]
TITHI_CLASSES_ML = [
    ('നന്ദ (സന്തോഷം)', 'മറ്റുള്ളവർക്ക് സന്തോഷം നൽകുന്ന ഉത്സാഹസ്വഭാവം'),
    ('ഭദ്ര (ക്ഷേമം)', 'സ്ഥിരതയും വിശ്വാസ്യതയുമുള്ള, നിലനിൽക്കുന്നവ പടുത്തുയർത്തുന്ന സ്വഭാവം'),
    ('ജയ (വിജയം)', 'പ്രയത്നത്താൽ വിജയം നേടുന്ന മത്സരബുദ്ധി'),
    ('രിക്ത (ശൂന്യത)', 'അധിക പ്രയത്നത്താൽ ലഭിക്കുന്ന ഫലങ്ങളും തടസ്സങ്ങളെ മറികടക്കാനുള്ള ശക്തിയും'),
    ('പൂർണ്ണ (നിറവ്)', 'ഏറ്റെടുക്കുന്ന കാര്യങ്ങളിൽ പൂർണ്ണതയും സംതൃപ്തിയും'),
]
TITHI_DEITIES_ML = ['അഗ്നി', 'ബ്രഹ്മാവ്', 'ഗൗരി', 'ഗണപതി', 'നാഗങ്ങൾ', 'സുബ്രഹ്മണ്യൻ', 'സൂര്യൻ', 'ശിവൻ', 'ദുർഗ്ഗ', 'യമൻ',
                    'വിശ്വദേവർ', 'വിഷ്ണു', 'കാമദേവൻ', 'ശിവൻ']
TITHI_ML = ['പ്രഥമ', 'ദ്വിതീയ', 'തൃതീയ', 'ചതുർത്ഥി', 'പഞ്ചമി', 'ഷഷ്ഠി', 'സപ്തമി', 'അഷ്ടമി', 'നവമി', 'ദശമി', 'ഏകാദശി',
            'ദ്വാദശി', 'ത്രയോദശി', 'ചതുർദ്ദശി']
TITHI_OBSERVANCE_ML = {
    11: 'വിഷ്ണുവിനുള്ള ഏകാദശി വ്രതമാണ് പരമ്പരാഗത അനുഷ്ഠാനം.',
    13: 'ഇത് പ്രദോഷ ദിവസമാണ്; സന്ധ്യയ്ക്ക് ശിവാരാധന പരമ്പരാഗതമാണ്.',
    30: 'അമാവാസിയിൽ പിതൃക്കൾക്ക് തർപ്പണം ചെയ്യുന്നത് പരമ്പരാഗത അനുഷ്ഠാനമാണ്.',
}
NITYA_YOGA_ML = {
    'Vishkambha': ('വിഷ്കംഭം', 'തൂൺ'), 'Priti': ('പ്രീതി', 'സ്നേഹം'), 'Ayushman': ('ആയുഷ്മാൻ', 'ദീർഘായുസ്സ്'),
    'Saubhagya': ('സൗഭാഗ്യം', 'ഭാഗ്യം'), 'Shobhana': ('ശോഭനം', 'ശോഭ'), 'Atiganda': ('അതിഗണ്ഡം', 'വലിയ ആപത്ത്'),
    'Sukarma': ('സുകർമ്മം', 'സത്കർമ്മം'), 'Dhriti': ('ധൃതി', 'ദൃഢത'), 'Shula': ('ശൂലം', 'കുന്തം'), 'Ganda': ('ഗണ്ഡം', 'ആപത്ത്'),
    'Vriddhi': ('വൃദ്ധി', 'വളർച്ച'), 'Dhruva': ('ധ്രുവം', 'സ്ഥിരത'), 'Vyaghata': ('വ്യാഘാതം', 'ആഘാതം'),
    'Harshana': ('ഹർഷണം', 'ആഹ്ലാദം'), 'Vajra': ('വജ്രം', 'ഇടിമിന്നൽ'), 'Siddhi': ('സിദ്ധി', 'കാര്യസിദ്ധി'),
    'Vyatipata': ('വ്യതീപാതം', 'വിപത്ത്'), 'Variyan': ('വരീയാൻ', 'സുഖം'), 'Parigha': ('പരിഘം', 'തടസ്സം'),
    'Shiva': ('ശിവം', 'മംഗളം'), 'Siddha': ('സിദ്ധം', 'പൂർണ്ണത'), 'Sadhya': ('സാദ്ധ്യം', 'നേട്ടം'), 'Shubha': ('ശുഭം', 'നന്മ'),
    'Shukla': ('ശുക്ലം', 'പ്രകാശം'), 'Brahma': ('ബ്രഹ്മം', 'സൃഷ്ടി'), 'Indra': ('ഐന്ദ്രം', 'നേതൃത്വം'),
    'Vaidhriti': ('വൈധൃതി', 'ഭിന്നത'),
}
KARANA_ML = {'Bava': 'ബവം', 'Balava': 'ബാലവം', 'Kaulava': 'കൗലവം', 'Taitila': 'തൈതിലം', 'Gara': 'ഗരജ',
             'Vanija': 'വണിജ', 'Vishti': 'ഭദ്ര (വിഷ്ടി)', 'Shakuni': 'ശകുനി', 'Chatushpada': 'ചതുഷ്പാദം',
             'Naga': 'നാഗവം', 'Kimstughna': 'കിംസ്തുഘ്നം'}
# Tithi classes (Nanda, Bhadra, Jaya, Rikta, Purna) by the tithi's number within its paksha
TITHI_CLASSES = [
    ('Nanda (joy)', 'நந்தா (மகிழ்ச்சி)', 'a cheerful nature that brings joy to others', 'பிறருக்கு மகிழ்ச்சி தரும் உற்சாக இயல்பு'),
    ('Bhadra (well-being)', 'பத்ரா (நலம்)', 'a steady, dependable nature that builds lasting things', 'நிலையான, நம்பகமான, நீடித்த காரியங்களைக் கட்டியெழுப்பும் இயல்பு'),
    ('Jaya (victory)', 'ஜயா (வெற்றி)', 'a competitive spirit that wins through effort', 'முயற்சியால் வெற்றி பெறும் போட்டி மனப்பான்மை'),
    ('Rikta (emptiness)', 'ரிக்தா (வெறுமை)', 'results that come through extra effort, and strength in overcoming obstacles', 'கூடுதல் முயற்சியால் கிடைக்கும் பலன்களும் தடைகளை வெல்லும் ஆற்றலும்'),
    ('Purna (fullness)', 'பூர்ணா (நிறைவு)', 'contentment and completeness in what one undertakes', 'மேற்கொள்ளும் காரியங்களில் நிறைவும் மனத்திருப்தியும்')
]
# Presiding deity of each tithi of the paksha; the 15th is the Moon's (Pournami) or the Pitrs' (Amavasai)
TITHI_DEITIES = [('Agni', 'அக்னி'), ('Brahma', 'பிரம்மா'), ('Gauri', 'கௌரி'), ('Ganapati', 'விநாயகர்'), ('the Nagas', 'நாகர்கள்'),
                 ('Murugan (Skanda)', 'முருகன்'), ('Surya', 'சூரியன்'), ('Shiva', 'சிவன்'), ('Durga', 'துர்க்கை'), ('Yama', 'யமன்'),
                 ('the Vishvedevas', 'விஸ்வதேவர்கள்'), ('Vishnu', 'விஷ்ணு'), ('Kama (Manmatha)', 'மன்மதன்'), ('Shiva', 'சிவன்')]
# Where Tamil observance differs from worshipping the presiding deity (paksha tithi number; 30 = Amavasai)
TITHI_OBSERVANCE = {
    10: None,
    11: ('The Ekadasi fast, devoted to Vishnu, is the traditional observance.', 'விஷ்ணுவுக்கு உரிய ஏகாதசி விரதம் பாரம்பரிய அனுஷ்டானம்.'),
    13: ('This is Pradosham, when Shiva is worshipped at dusk.', 'இது பிரதோஷ நாள்; மாலை வேளையில் சிவ வழிபாடு பாரம்பரியம்.'),
    30: ('Tarpanam to the ancestors on Amavasai is the traditional observance.', 'அமாவாசையில் பித்ருக்களுக்குத் தர்ப்பணம் செய்வது பாரம்பரிய அனுஷ்டானம்.')
}
NITYA_YOGA_MEANINGS = {
    'Vishkambha': ('the pillar', 'விஷ்கம்பம்', 'தூண்'), 'Priti': ('affection', 'ப்ரீதி', 'அன்பு'),
    'Ayushman': ('long life', 'ஆயுஷ்மான்', 'நீண்ட ஆயுள்'), 'Saubhagya': ('good fortune', 'சௌபாக்கியம்', 'நல்லதிர்ஷ்டம்'),
    'Shobhana': ('splendour', 'சோபனம்', 'பொலிவு'), 'Atiganda': ('great danger', 'அதிகண்டம்', 'பெரும் ஆபத்து'),
    'Sukarma': ('good deeds', 'சுகர்மம்', 'நற்செயல்'), 'Dhriti': ('steadiness', 'திருதி', 'உறுதி'),
    'Shula': ('the spear', 'சூலம்', 'ஈட்டி'), 'Ganda': ('danger', 'கண்டம்', 'ஆபத்து'),
    'Vriddhi': ('growth', 'விருத்தி', 'வளர்ச்சி'), 'Dhruva': ('constancy', 'துருவம்', 'நிலைத்தன்மை'),
    'Vyaghata': ('the blow', 'வியாகாதம்', 'அடி'), 'Harshana': ('delight', 'ஹர்ஷணம்', 'மகிழ்ச்சி'),
    'Vajra': ('the thunderbolt', 'வஜ்ரம்', 'இடி'), 'Siddhi': ('accomplishment', 'சித்தி', 'காரிய சித்தி'),
    'Vyatipata': ('calamity', 'வியதீபாதம்', 'பேரிடர்'), 'Variyan': ('comfort', 'வரீயான்', 'சுகம்'),
    'Parigha': ('the barrier', 'பரிகம்', 'தடை'), 'Shiva': ('auspiciousness', 'சிவம்', 'மங்களம்'),
    'Siddha': ('perfection', 'சித்தம்', 'நிறைவு'), 'Sadhya': ('attainment', 'சாத்தியம்', 'அடைதல்'),
    'Shubha': ('goodness', 'சுபம்', 'நன்மை'), 'Shukla': ('brightness', 'சுக்லம்', 'ஒளி'),
    'Brahma': ('the creator', 'பிரம்மம்', 'படைப்பு'), 'Indra': ('leadership', 'ஐந்திரம்', 'தலைமை'),
    'Vaidhriti': ('discord', 'வைதிருதி', 'பிணக்கு')
}
KARANA_TAMIL = {'Bava': 'பவம்', 'Balava': 'பாலவம்', 'Kaulava': 'கௌலவம்', 'Taitila': 'தைதுலம்', 'Gara': 'கரசை',
                'Vanija': 'வணிசை', 'Vishti': 'பத்திரை (விஷ்டி)', 'Shakuni': 'சகுனி', 'Chatushpada': 'சதுஷ்பாதம்',
                'Naga': 'நாகவம்', 'Kimstughna': 'கிம்ஸ்துக்னம்'}


def generate_panchanga_phala(chart):
    """Readings from the four limbs of the birth panchangam besides the nakshatra."""
    panch = chart['panchanga']
    weekday = chart.get('vedic_weekday')
    weekday = weekday if weekday is not None else ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'].index(panch['weekday'])
    items = []
    en, ta = VAARA_PHALA[weekday]
    items.append(dict(key='vaara', title_en='Weekday (Vaara)', title_ta='கிழமை (வாரம்)', title_ml='ആഴ്ച (വാരം)',
                      reading_en=en, reading_ta=ta, reading_ml=VAARA_PHALA_ML[weekday]))

    tithi = panch['tithi']
    in_paksha = (tithi - 1) % 15 + 1
    class_en, class_ta, trait_en, trait_ta = TITHI_CLASSES[(in_paksha - 1) % 5]
    if in_paksha == 15:
        deity_en, deity_ta = ('the Moon', 'சந்திரன்') if tithi == 15 else ('the ancestors (Pitrs)', 'பித்ருக்கள்')
    else:
        deity_en, deity_ta = TITHI_DEITIES[in_paksha - 1]
    from ..south_indian import TITHI_TA
    tithi_ta = TITHI_TA[in_paksha - 1] if in_paksha < 15 else ('பௌர்ணமி' if tithi == 15 else 'அமாவாசை')
    observance = TITHI_OBSERVANCE.get(30 if tithi == 30 else in_paksha, (
        f"Worshipping {deity_en} on this tithi each month is traditionally recommended.",
        f"ஒவ்வொரு மாதமும் இத்திதியில் {deity_ta} வழிபாடு பாரம்பரியமாகப் பரிந்துரைக்கப்படுகிறது.")) or ('', '')
    paksha_en = 'waxing (Shukla)' if tithi <= 15 else 'waning (Krishna)'
    paksha_ta = 'வளர்பிறை' if tithi <= 15 else 'தேய்பிறை'
    paksha_ml = 'വെളുത്ത പക്ഷം' if tithi <= 15 else 'കറുത്ത പക്ഷം'
    class_ml, trait_ml = TITHI_CLASSES_ML[(in_paksha - 1) % 5]
    if in_paksha == 15:
        deity_ml = 'ചന്ദ്രൻ' if tithi == 15 else 'പിതൃക്കൾ'
        tithi_ml = 'പൗർണ്ണമി' if tithi == 15 else 'അമാവാസി'
    else:
        deity_ml, tithi_ml = TITHI_DEITIES_ML[in_paksha - 1], TITHI_ML[in_paksha - 1]
    obs_key = 30 if tithi == 30 else in_paksha
    observance_ml = ('' if obs_key == 10 else TITHI_OBSERVANCE_ML.get(
        obs_key, f"എല്ലാ മാസവും ഈ തിഥിയിൽ {deity_ml} ആരാധന പരമ്പരാഗതമായി നിർദ്ദേശിക്കപ്പെടുന്നു."))
    items.append(dict(
        key='tithi', title_en='Tithi', title_ta='திதி', title_ml='തിഥി',
        reading_ml=(f"{paksha_ml} {tithi_ml} തിഥിയിൽ ജനനം; ഇത് {class_ml} തിഥിയാണ്: {trait_ml}. "
                    f"അധിദേവത: {deity_ml}. {observance_ml}".rstrip()),
        reading_en=(f"Born on {panch['tithi_name']} of the {paksha_en} fortnight, a {class_en} tithi: {trait_en}. "
                    f"Presiding deity: {deity_en}. {observance[0]}".rstrip()),
        reading_ta=(f"{paksha_ta} {tithi_ta} திதியில் பிறந்தவர்; இது {class_ta} திதி: {trait_ta}. "
                    f"இதன் அதிதேவதை {deity_ta}. {observance[1]}".rstrip())))

    yoga = panch['yoga_name']
    meaning_en, yoga_ta, meaning_ta = NITYA_YOGA_MEANINGS.get(yoga, (yoga, yoga, yoga))
    yoga_ml, meaning_ml = NITYA_YOGA_ML.get(yoga, (yoga, yoga))
    if panch.get('yoga_auspiciousness') == 'Auspicious':
        yoga_ml_text = f"{yoga_ml} യോഗത്തിൽ ('{meaning_ml}') ജനനം; ഇത് ശുഭ നിത്യയോഗമായതിനാൽ ക്ഷേമവും കാര്യവിജയവും ഉണ്ടാകും."
    else:
        yoga_ml_text = (f"{yoga_ml} യോഗത്തിൽ ('{meaning_ml}') ജനനം; ഇത് ഒമ്പത് പ്രയാസകരമായ നിത്യയോഗങ്ങളിൽ ഒന്നാണ്: ക്ഷമയാൽ "
                        f"തടസ്സങ്ങൾ നീങ്ങും; ജന്മനക്ഷത്ര ദിവസം ഈശ്വരാരാധന പരമ്പരാഗതമായി നിർദ്ദേശിക്കപ്പെടുന്നു.")
    if panch.get('yoga_auspiciousness') == 'Auspicious':
        yoga_en_text = f"Born in {yoga} yoga ('{meaning_en}'), an auspicious nitya yoga that supports well-being and success in undertakings."
        yoga_ta_text = f"{yoga_ta} யோகத்தில் ('{meaning_ta}') பிறந்தவர்; இது சுப நித்ய யோகம் என்பதால் நலமும் காரிய வெற்றியும் உண்டு."
    else:
        yoga_en_text = (f"Born in {yoga} yoga ('{meaning_en}'), one of the nine difficult nitya yogas: obstacles are overcome through "
                        f"patience, and prayer on the birth star day is traditionally advised.")
        yoga_ta_text = (f"{yoga_ta} யோகத்தில் ('{meaning_ta}') பிறந்தவர்; இது ஒன்பது கடினமான நித்ய யோகங்களில் ஒன்று: பொறுமையால் "
                        f"தடைகள் நீங்கும்; ஜன்ம நட்சத்திர நாளில் இறை வழிபாடு செய்வது பாரம்பரியமாகப் பரிந்துரைக்கப்படுகிறது.")
    items.append(dict(key='yoga', title_en='Nitya Yoga', title_ta='நித்ய யோகம்', title_ml='നിത്യയോഗം',
                      reading_en=yoga_en_text, reading_ta=yoga_ta_text, reading_ml=yoga_ml_text))

    karana = panch['karana_name']
    karana_ta = KARANA_TAMIL.get(karana, karana)
    karana_ml = KARANA_ML.get(karana, karana)
    if karana == 'Vishti':
        k_en = ("Born in Vishti (Bhadra) karana, traditionally a difficult karana: energy is strong but needs direction; "
                "worship of Ganapati is advised.")
        k_ml = "ഭദ്ര (വിഷ്ടി) കരണത്തിൽ ജനനം; ഇത് പ്രയാസകരമായ കരണമാണ്: ഊർജ്ജം ശക്തമാണ്, അതിനെ നല്ല വഴിക്ക് തിരിക്കണം; ഗണപതി ആരാധന നല്ലത്."
        k_ta = "பத்திரை (விஷ்டி) கரணத்தில் பிறந்தவர்; இது கடினமான கரணம்: ஆற்றல் அதிகம், அதை நல்வழியில் செலுத்த வேண்டும்; விநாயகர் வழிபாடு நலம்."
    elif karana in ('Shakuni', 'Chatushpada', 'Naga', 'Kimstughna'):
        k_en = f"Born in {karana} karana, one of the four fixed karanas: a steady, determined temperament that prefers stability to change."
        k_ml = f"{karana_ml} കരണത്തിൽ ജനനം; ഇത് നാല് സ്ഥിര കരണങ്ങളിൽ ഒന്നാണ്: മാറ്റത്തേക്കാൾ സ്ഥിരത ഇഷ്ടപ്പെടുന്ന ദൃഢസ്വഭാവം."
        k_ta = f"{karana_ta} கரணத்தில் பிறந்தவர்; இது நான்கு ஸ்திர கரணங்களில் ஒன்று: மாற்றத்தை விட நிலைத்தன்மையை விரும்பும் உறுதியான இயல்பு."
    else:
        k_en = f"Born in {karana} karana, a movable karana: an active, adaptable temperament that does well with travel and new ventures."
        k_ml = f"{karana_ml} കരണത്തിൽ ജനനം; ഇത് ചര കരണമാണ്: ഏത് സാഹചര്യത്തിനും ഇണങ്ങുന്ന ഉന്മേഷമുള്ള സ്വഭാവം; യാത്രകളും പുതിയ സംരംഭങ്ങളും ഗുണം ചെയ്യും."
        k_ta = f"{karana_ta} கரணத்தில் பிறந்தவர்; இது சர கரணம்: சுறுசுறுப்பான, எந்தச் சூழலுக்கும் ஏற்றுக்கொள்ளும் இயல்பு; பயணங்களும் புதிய முயற்சிகளும் நலம் தரும்."
    items.append(dict(key='karana', title_en='Karana', title_ta='கரணம்', title_ml='കരണം', reading_en=k_en, reading_ta=k_ta,
                      reading_ml=k_ml))
    return items


# SUDARSHANA CHAKRA: the houses counted together from the Lagna, the Moon and the Sun, with the
# yearly progression of BPHS (each year of life activates the next house from all three)
def calculate_sudarshana_chakra(chart):
    planets = chart['planets']
    grahas = ('Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu')
    refs = [('Lagna', 'லக்னம்', planets['Ascendant']['sign_index']), ('Moon', 'சந்திரன்', planets['Moon']['sign_index']),
            ('Sun', 'சூரியன்', planets['Sun']['sign_index'])]
    rows = []
    for house in range(1, 13):
        row = dict(house=house)
        for name, _, start in refs:
            sign = (start + house - 1) % 12
            row[name.lower()] = dict(sign=SIGNS[sign], sign_ta=TAMIL_SIGNS[sign], sign_ml=MALAYALAM_SIGNS[sign],
                                     planets=[g for g in grahas if planets[g]['sign_index'] == sign])
        rows.append(row)
    tz = ZoneInfo(chart.get('timezone') or 'UTC')
    birth = chart['utc'] if isinstance(chart['utc'], datetime) else datetime.fromisoformat(chart['utc'])
    birth = birth.astimezone(tz)
    now = datetime.fromisoformat(chart['gochara']['computed_at']).astimezone(tz)
    age = now.year - birth.year - ((now.month, now.day) < (birth.month, birth.day))
    active = age % 12 + 1
    themes_en, themes_ta = HOUSE_THEMES[active]
    return dict(
        rows=rows, age=age, active_house=active,
        reading_en=(f"In your {_ordinal(age + 1)} year the Sudarshana Chakra activates the {_ordinal(active)} house from the Lagna, "
                    f"the Moon and the Sun at once ({rows[active - 1]['lagna']['sign']}, {rows[active - 1]['moon']['sign']} and "
                    f"{rows[active - 1]['sun']['sign']}): matters of {themes_en} come to the fore this year."),
        reading_ta=(f"உங்கள் {age + 1}-வது வயதில் சுதர்சன சக்கரம் லக்னம், சந்திரன், சூரியன் மூன்றிலிருந்தும் {active}-ஆம் பாவத்தை "
                    f"({rows[active - 1]['lagna']['sign_ta']}, {rows[active - 1]['moon']['sign_ta']}, {rows[active - 1]['sun']['sign_ta']}) "
                    f"இயக்குகிறது: இந்த ஆண்டு {themes_ta} தொடர்பான விஷயங்கள் முன்னிலை பெறும்."),
        reading_ml=(f"നിങ്ങളുടെ {age + 1}-ാം വയസ്സിൽ സുദർശന ചക്രം ലഗ്നം, ചന്ദ്രൻ, സൂര്യൻ എന്നീ മൂന്നിൽ നിന്നും {active}-ാം ഭാവത്തെ "
                    f"({rows[active - 1]['lagna']['sign_ml']}, {rows[active - 1]['moon']['sign_ml']}, {rows[active - 1]['sun']['sign_ml']}) "
                    f"ഉണർത്തുന്നു: ഈ വർഷം {HOUSE_THEMES_ML[active]} എന്നിവയുമായി ബന്ധപ്പെട്ട കാര്യങ്ങൾ മുന്നിൽ വരും.")
    )


# Master Generator
