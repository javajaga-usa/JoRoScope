"""Jaimini: the seven chara karakas, the Karakamsa and the bhava arudhas (arudha padas).
"""

from .common import PLANET_TAMIL, SIGNS, SIGN_LORDS, TAMIL_SIGNS


# 8. Jaimini 7 Chara Karakas & Karakamsha System
# Results of grahas in the Karakamsa (Jaimini Upadesa Sutras 1.2, in present-day terms)
KARAKAMSA_RESULTS = {
    'Sun': ('Sun in the Karakamsa: work connected with government, politics or public administration.',
            'காரகாம்சத்தில் சூரியன்: அரசு, அரசியல் அல்லது பொது நிர்வாகம் தொடர்பான பணி.'),
    'Moon': ('Moon in the Karakamsa: a life of comforts, living by learning, the more so with Venus.',
             'காரகாம்சத்தில் சந்திரன்: சுக போகங்கள் நிறைந்த வாழ்க்கை, கல்வியால் ஜீவனம்; சுக்கிரனுடன் மேலும் சிறப்பு.'),
    'Mars': ('Mars in the Karakamsa: work with metals, chemistry, fire or weapons, such as engineering or defence.',
             'காரகாம்சத்தில் செவ்வாய்: உலோகம், வேதியியல், நெருப்பு அல்லது ஆயுதம் தொடர்பான பணி, பொறியியல் அல்லது பாதுகாப்புத் துறை போன்றவை.'),
    'Mercury': ('Mercury in the Karakamsa: trade, skilled crafts, textiles, or law and business dealings.',
                'காரகாம்சத்தில் புதன்: வணிகம், கைத்திறன் கலைகள், ஜவுளி, அல்லது சட்டம் மற்றும் வர்த்தக விவகாரங்கள்.'),
    'Jupiter': ('Jupiter in the Karakamsa: a learned, dutiful person versed in scripture: teaching, ritual or philosophy.',
                'காரகாம்சத்தில் குரு: சாஸ்திர ஞானமும் கடமையுணர்வும் கொண்டவர்: கற்பித்தல், வைதீகம் அல்லது தத்துவம்.'),
    'Venus': ('Venus in the Karakamsa: an official in government service, fond of pleasures, with keen senses and long life.',
              'காரகாம்சத்தில் சுக்கிரன்: அரசுப் பணியில் அதிகாரி, இன்ப நாட்டம், கூர்மையான புலன்கள் மற்றும் நீண்ட ஆயுள்.'),
    'Saturn': ('Saturn in the Karakamsa: renown through the family\'s traditional line of work.',
               'காரகாம்சத்தில் சனி: குடும்பப் பாரம்பரியத் தொழிலில் புகழ்.'),
    'Rahu': ('Rahu in the Karakamsa: work with machinery and metals, or with poisons and medicines; avoid dishonest ways.',
             'காரகாம்சத்தில் ராகு: இயந்திரம் மற்றும் உலோகம், அல்லது விஷம் மற்றும் மருந்துகள் தொடர்பான பணி; நேர்மையற்ற வழிகளைத் தவிர்க்க வேண்டும்.'),
    'Ketu': ('Ketu in the Karakamsa: dealings in large animals or vehicles; avoid dishonest ways.',
             'காரகாம்சத்தில் கேது: பெரிய விலங்குகள் அல்லது வாகனங்கள் தொடர்பான வியாபாரம்; நேர்மையற்ற வழிகளைத் தவிர்க்க வேண்டும்.')
}
def calculate_jaimini_karakas(planets, vargas=None):
    seven_planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']
    extracted = []
    for p_name in seven_planets:
        p_data = planets.get(p_name)
        if not p_data: continue
        deg_in_sign = p_data['degree'] % 30.0
        extracted.append({
            'planet': p_name,
            'tamil_planet': PLANET_TAMIL.get(p_name, p_name),
            'degree_in_sign': deg_in_sign,
            'degree_str': f"{int(deg_in_sign)}° {int((deg_in_sign*60)%60):02d}′",
            'sign': p_data['sign'],
            'tamil_sign': p_data['tamil'],
            'house': p_data['house'],
            'dignity': p_data.get('dignity', 'Neutral')
        })

    # Sort descending by degree within sign
    extracted.sort(key=lambda x: x['degree_in_sign'], reverse=True)

    karaka_defs = [
        ('AK', 'Atmakaraka', 'ஆன்ம காரகன்', 'Soul Indicator & Supreme Spiritual Evolution'),
        ('AmK', 'Amatyakaraka', 'அமாத்திய காரகன்', 'Career, Executive Intellect & Social Status'),
        ('BK', 'Bhratrikaraka', 'பிராத்ரு காரகன்', 'Mentors, Gurus, Guidance & Siblings'),
        ('MK', 'Matrikaraka', 'மாத்ரு காரகன்', 'Mother, Domestic Peace, Land & Fixed Assets'),
        ('PK', 'Putrakaraka', 'புத்ர காரகன்', 'Intellectual Genius, Progeny & Purva Punya'),
        ('GK', 'Gnatikaraka', 'ஞாதி காரகன்', 'Karmic Obstacles, Resilience & Competitive Victory'),
        ('DK', 'Darakaraka', 'தார காரகன்', 'Spouse Characteristics & Sacred Partnerships')
    ]

    karaka_readings = {
        'AK': {
            'Sun': ('Soul learns leadership through selfless duty, shedding pride and embodying righteous integrity.',
                    'ஆன்ம பலம் தலைமைப் பண்பையும், கௌரவத்தையும் நோக்கியது; தர்ம நெறியுடன் கூடிய கடமையுணர்வே உயர்வை தரும்.'),
            'Moon': ('Soul cultivates unconditional compassion, emotional equanimity, and nurturing universal empathy.',
                     'மனத்தெளிவு, இரக்க குணம், உலகளாவிய தாய்மை அன்பு ஆகியவற்றின் வழியே ஆன்மீக மேன்மை உண்டாகும்.'),
            'Mars': ('Soul masters courageous resolve, protection of the vulnerable, and discipline over raw anger.',
                     'வீரமும், துணிச்சலும் உங்கள் ஆன்மாவின் பலம்; கோபத்தைக் கட்டுப்படுத்தி நல்வழியில் உழைப்பது பெரும் வெற்றியைத் தரும்.'),
            'Mercury': ('Soul evolves through truthful eloquence, intellectual discrimination, and pursuit of sacred knowledge.',
                        'அறிவாற்றல், வாய்மை, கல்வி மற்றும் சாதுரியமான பேச்சாற்றல் மூலம் ஆன்ம விகாசம் உண்டாகும்.'),
            'Jupiter': ('Soul embodies supreme spiritual wisdom, benevolent teaching, moral guidance, and dharmic reverence.',
                        'ஞானம், ஆசார அனுஷ்டானங்கள், தர்ம போதனை மற்றும் பிறருக்கு வழிகாட்டும் ஆசான் தன்மை உங்கள் ஆன்ம குணம்.'),
            'Venus': ('Soul refines devotional love, aesthetic elegance, sensual mastery, and radiant harmony.',
                      'கலை நேர்த்தி, தூய அன்பு, சுய கட்டுப்பாடு மற்றும் குடும்பத்தில் அமைதியை நிலைநாட்டுவதே ஆன்ம வழி.'),
            'Saturn': ('Soul attains liberation through enduring humility, selfless service to society, and patience through trials.',
                       'பொறுமை, கடின உழைப்பு, எளியோருக்கு உதவும் தியாக மனப்பான்மை வழியே முக்தி நிலை கைகூடும்.')
        },
        'AmK': {
            'Sun': ('Dominates in government, executive leadership, political statecraft, and prominent administrative roles.',
                    'அரசு நிர்வாகம், தலைமைப் பதவிகள், அதிகாரமிக்க பொறுப்புகளில் முன்னிலை வகிப்பீர்கள்.'),
            'Moon': ('Excels in public relations, healthcare, administration, maritime trade, hospitality, and psychology.',
                     'மக்கள் தொடர்பு, பொதுச்சேவை, உளவியல், மருத்துவம் மற்றும் உணவகத் துறையில் பெரும் வெற்றி.'),
            'Mars': ('Flourishes in engineering, technology, military/police, surgery, real estate development, and sports.',
                     'பொறியியல், நிலம்-கட்டடம், பாதுகாப்புத் துறை, அறுவை சிகிச்சை மற்றும் தொழில்நுட்பத்தில் உச்சம்.'),
            'Mercury': ('Thrives in software, data analytics, journalism, finance, auditing, writing, and commercial commerce.',
                        'மென்பொருள், கணக்கியல், வணிகம், எழுத்து, வங்கி மற்றும் தகவல் தொடர்புத் துறையில் சாதனை.'),
            'Jupiter': ('Shines in judiciary, law, higher education, banking, ministerial advisory, and philosophy.',
                        'சட்டம், நீதித்துறை, பேராசிரியர், வங்கி மற்றும் உயர்மட்ட ஆலோசகர் பதவிகளில் கௌரவம்.'),
            'Venus': ('Succeeds in luxury enterprise, creative design, arts, media, diplomacy, and boutique commerce.',
                      'கலை, வடிவமைப்பு, ஆடை ஆபரணம், திரைப்படம், ஊடகம் மற்றும் தூதரகப் பணிகளில் மேன்மை.'),
            'Saturn': ('Rises steadily in large-scale industry, civil infrastructure, manufacturing, labor law, and mining.',
                       'பெருந்தொழில், உற்பத்தி, கட்டமைப்பு, சுரங்கம் மற்றும் மக்கள் நல அமைப்புகளில் நிலையான அதிகாரம்.')
        },
        'DK': {
            'Sun': ('Spouse possesses dignified presence, strong moral compass, noble heritage, and commanding leadership.',
                    'வாழ்க்கைத் துணை கம்பீரமான தோற்றமும், நிர்வாகத் திறமையும், சிறந்த குலப் பெருமையும் கொண்டவர்.'),
            'Moon': ('Spouse is gentle, deeply affectionate, intuitive, domestic-loving, and emotionally supportive.',
                     'வாழ்க்கைத் துணை மென்மையான உள்ளமும், பாசமும், சிறந்த விருந்தோம்பல் குணமும் உடையவர்.'),
            'Mars': ('Spouse is dynamic, athletic, fiercely loyal, courageous, ambitious, and quick to take decisive action.',
                     'வாழ்க்கைத் துணை சுறுசுறுப்பும், துணிச்சலும், குடும்பத்தின் மீது அதீத அக்கறையும் கொண்டவர்.'),
            'Mercury': ('Spouse is witty, youthful, highly educated, commercially shrewd, and a gifted communicator.',
                        'வாழ்க்கைத் துணை புத்தி கூர்மையும், இளமைத் தோற்றமும், சிறந்த பேச்சாற்றலும் கொண்டவர்.'),
            'Jupiter': ('Spouse is virtuous, religious, spiritually inclined, scholarly, respected, and wise counselor.',
                        'வாழ்க்கைத் துணை தெய்வ பக்தியும், சாந்த குணமும், குடும்பத்திற்கு பெருமை சேர்க்கும் நற்குணமும் கொண்டவர்.'),
            'Venus': ('Spouse is exquisitely charming, aesthetically refined, artistic, affectionate, and elegant.',
                      'வாழ்க்கைத் துணை பேரழகும், கலை ரசனையும், வசீகரமான ஆளுமையும் கொண்டவர்.'),
            'Saturn': ('Spouse is highly responsible, mature, practical, hardworking, disciplined, and enduringly loyal.',
                       'வாழ்க்கைத் துணை பக்குவமும், பொறுமையும், குடும்பத்தை கட்டிக்காக்கும் உழைப்பும் கொண்டவர்.')
        }
    }

    karakas_list = []
    ak_planet = None
    amk_planet = None

    for i, (code, title_en, title_ta, signification) in enumerate(karaka_defs):
        if i < len(extracted):
            item = extracted[i]
            p = item['planet']
            if code == 'AK': ak_planet = p
            if code == 'AmK': amk_planet = p

            reading_en = karaka_readings.get(code, {}).get(p, (f"{p} acts as your {title_en}, illuminating matters of {signification}.", ''))[0]
            reading_ta = karaka_readings.get(code, {}).get(p, ('', f"{PLANET_TAMIL.get(p, p)} உங்கள் {title_ta}வாக விளங்கி சுப பலன்களை அருளுகிறார்."))[1]

            if not reading_en:
                reading_en = f"{p} acts as your {title_en}, orchestrating matters of {signification}."
            if not reading_ta:
                reading_ta = f"{PLANET_TAMIL.get(p, p)} உங்கள் {title_ta}வாக விளங்கி அப்பாவக நற்பலன்களை இயக்குவார்."

            karakas_list.append({
                'code': code,
                'title_en': title_en,
                'title_ta': title_ta,
                'signification': signification,
                'planet': p,
                'tamil_planet': item['tamil_planet'],
                'degree_str': item['degree_str'],
                'degree_in_sign': round(item['degree_in_sign'], 4),
                'sign': item['sign'],
                'tamil_sign': item['tamil_sign'],
                'house': item['house'],
                'dignity': item['dignity'],
                'reading_en': reading_en,
                'reading_ta': reading_ta
            })

    # Karakamsha (Navamsa sign of Atmakaraka)
    karakamsha_sign_idx = 0
    if vargas and 'D9' in vargas and ak_planet in vargas['D9']:
        karakamsha_sign_idx = vargas['D9'][ak_planet]
    elif ak_planet and ak_planet in planets:
        karakamsha_sign_idx = int(planets[ak_planet]['longitude'] * 9 // 30) % 12

    karakamsha_sign = SIGNS[karakamsha_sign_idx]
    karakamsha_tamil = TAMIL_SIGNS[karakamsha_sign_idx]

    karakamsha_interpretations = {
        'Aries': ('Karakamsha in Mesha bestows courageous pioneering spirit, independent entrepreneurship, and mastery over tactical ventures.',
                  'காரகாம்சம் மேஷத்தில் அமைந்ததால் தளராத தைரியமும், சுயமாக சிந்தித்து தொழில் நடத்தும் தலைமைப் பண்பும் அமையும்.'),
        'Taurus': ('Karakamsha in Vrishabha grants artistic refinement, financial abundance, love for sacred music, and agricultural/real estate gains.',
                   'காரகாம்சம் ரிஷபத்தில் அமைந்ததால் கலை ஞானம், வாக்கு வன்மை, நிலையான சொத்துக்கள் மற்றும் தன சேர்க்கை கிட்டும்.'),
        'Gemini': ('Karakamsha in Mithuna bestows versatile communicative intellect, commercial genius, writing eloquence, and technical versatility.',
                   'காரகாம்சம் மிதுனத்தில் அமைந்ததால் சிறந்த பேச்சாற்றல், எழுத்து, கணினி மற்றும் வியாபாரத் துறையில் சாதனை படைப்பீர்கள்.'),
        'Cancer': ('Karakamsha in Kataka blesses with profound emotional empathy, intuitive psychology, public welfare, and protective maternal care.',
                   'காரகாம்சம் கடகத்தில் அமைந்ததால் மக்கள் நல்வாழ்வு, பொதுச் சேவை, உளவியல் மற்றும் ஆழ்ந்த உள்ளுணர்வு ஆற்றல் உண்டாகும்.'),
        'Leo': ('Karakamsha in Simha awakens royal dignity, executive command, noble statecraft, and fearless devotion to truth.',
                'காரகாம்சம் சிம்மத்தில் அமைந்ததால் அரசு வழி கௌரவம், அதிகாரமிக்க பதவிகள் மற்றும் அசைக்க முடியாத தன்னம்பிக்கை மிளிரும்.'),
        'Virgo': ('Karakamsha in Kanya grants analytical mastery, healing acumen, mathematical precision, and meticulous scholarship.',
                  'காரகாம்சம் கன்னியில் அமைந்ததால் மருத்துவ ஞானம், கணக்கு, ஆராய்ச்சி மற்றும் கூர்மையான பகுத்தறிவுத் திறன் அமையும்.'),
        'Libra': ('Karakamsha in Thula fosters diplomatic harmony, judicial fairness, mercantile eloquence, and visual aesthetics.',
                  'காரகாம்சம் துலாமில் அமைந்ததால் சட்டம், நீதி, சமரசப் பேச்சுவார்த்தை மற்றும் வணிகத் துறையில் நற்பெயர் கிட்டும்.'),
        'Scorpio': ('Karakamsha in Vrischika awakens occult wisdom, deep research penetration, investigative surgery, and transformative spiritual power.',
                    'காரகாம்சம் விருச்சிகத்தில் அமைந்ததால் மறைபொருள் அறிவு, ஆன்மீக தவம், ஆராய்ச்சி மற்றும் சோதனைகளை வெல்லும் சக்தி உண்டு.'),
        'Sagittarius': ('Karakamsha in Dhanus inspires philosophical righteousness, sacred teaching, judicial authority, and spiritual pilgrimage.',
                        'காரகாம்சம் தனுசில் அமைந்ததால் வேதாந்த ஞானம், ஆசிரியர், நீதித்துறை மற்றும் தர்ம சிந்தனை வழி பெரும் புகழ் பெறுவீர்கள்.'),
        'Capricorn': ('Karakamsha in Makara builds endurance, structural organizational mastery, industrial management, and solid worldly achievements.',
                     'காரகாம்சம் மகரத்தில் அமைந்ததால் கடின உழைப்பு, நிர்வாக வல்லமை, பொதுஜன ஆதரவு மற்றும் நிலைத்த சொத்துக்கள் அமையும்.'),
        'Aquarius': ('Karakamsha in Kumbha awakens humanitarian vision, philosophical depth, innovative science, and universal service.',
                     'காரகாம்சம் கும்பத்தில் அமைந்ததால் சமுதாய சீர்திருத்தம், புதிய கண்டுபிடிப்புகள் மற்றும் பொதுநலத் தொண்டில் ஈடுபாடு கூடும்.'),
        'Pisces': ('Karakamsha in Meena guides toward highest spiritual liberation (Moksha), divine surrender, meditation, and benevolent charity.',
                   'காரகாம்சம் மீனத்தில் அமைந்ததால் மோட்ச நாட்டம், இறை பக்தி, தியானம் மற்றும் எல்லையற்ற தர்ம சிந்தனை வாய்க்கும்.')
    }

    kk_en, kk_ta = karakamsha_interpretations.get(karakamsha_sign, ('Spiritual illumination through Atmakaraka dharma.', 'ஆன்ம வழிகாட்டுதல்.'))

    # Grahas sharing the Atmakaraka's Navamsa sign (Jaimini Upadesa Sutras 1.2), and Ketu in the 12th from it
    navamsa_of = lambda p: vargas['D9'][p] if vargas and 'D9' in vargas else planets[p]['vargas']['D9']
    occupants = [p for p in KARAKAMSA_RESULTS if p != ak_planet and navamsa_of(p) == karakamsha_sign_idx]
    karakamsa_results = [dict(planet=p, planet_ta=PLANET_TAMIL[p], en=KARAKAMSA_RESULTS[p][0], ta=KARAKAMSA_RESULTS[p][1])
                         for p in occupants]
    if navamsa_of('Ketu') == (karakamsha_sign_idx + 11) % 12:
        karakamsa_results.append(dict(planet='Ketu', planet_ta=PLANET_TAMIL['Ketu'],
                                      en='Ketu in the 12th from the Karakamsa promises final liberation (moksha), the more so with benefics.',
                                      ta='காரகாம்சத்திலிருந்து 12-இல் கேது இருப்பதால் மோட்ச பாக்கியம் உண்டு; சுப கிரகச் சேர்க்கையால் மேலும் வலுப்பெறும்.'))
    if karakamsa_results:
        kk_en += ' ' + ' '.join(r['en'] for r in karakamsa_results)
        kk_ta += ' ' + ' '.join(r['ta'] for r in karakamsa_results)

    # Arudha padas and the classical readings from the Arudha Lagna and the Upapada
    padas = jaimini_arudhas(planets)
    asc_sign = planets['Ascendant']['sign_index']
    arudha_rows = [dict(code=f"A{h}", house=h, sign=SIGNS[s], sign_ta=TAMIL_SIGNS[s], from_lagna=(s - asc_sign) % 12 + 1,
                        name_en=ARUDHA_NAMES.get(h, (f"A{h}", f"A{h}"))[0], name_ta=ARUDHA_NAMES.get(h, (f"A{h}", f"A{h}"))[1])
                   for h, s in enumerate(padas, 1)]
    grahas = ('Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu')
    in_sign = lambda s: [g for g in grahas if planets[g]['sign_index'] == s]
    benefic = lambda g: g in ('Jupiter', 'Venus', 'Mercury', 'Moon')
    al, ul = padas[0], padas[11]
    notes = []
    gains = in_sign((al + 10) % 12)
    if gains:
        fair = all(benefic(g) for g in gains)
        notes.append(dict(
            en=f"{', '.join(gains)} in the 11th from the Arudha Lagna bring steady gains{' by fair means' if fair else ', not always by conventional means'}.",
            ta=f"ஆரூட லக்னத்திலிருந்து 11-இல் {', '.join(PLANET_TAMIL[g] for g in gains)} இருப்பதால் நிலையான வருமானம் உண்டு{' (நேர்மையான வழியில்)' if fair else ' (எப்போதும் வழக்கமான வழியில் அல்ல)'}."))
    losses = in_sign((al + 11) % 12)
    if losses:
        good = all(benefic(g) for g in losses)
        notes.append(dict(
            en=f"{', '.join(losses)} in the 12th from the Arudha Lagna {'direct spending to good causes' if good else 'bring expenses and losses to guard against'}.",
            ta=f"ஆரூட லக்னத்திலிருந்து 12-இல் {', '.join(PLANET_TAMIL[g] for g in losses)} இருப்பதால் {'நல்ல காரியங்களுக்குச் செலவு ஏற்படும்' if good else 'செலவுகளிலும் இழப்புகளிலும் கவனம் தேவை'}."))
    second_ul = in_sign((ul + 1) % 12)
    if second_ul:
        harsh = [g for g in second_ul if not benefic(g)]
        notes.append(dict(
            en=(f"{', '.join(harsh)} in the 2nd from the Upapada can strain the continuity of marriage; remedies and patience help."
                if harsh else "Benefics in the 2nd from the Upapada sustain a lasting marriage."),
            ta=(f"உபபதத்திலிருந்து 2-இல் {', '.join(PLANET_TAMIL[g] for g in harsh)} இருப்பதால் இல்லற வாழ்வின் தொடர்ச்சியில் சோதனைகள் வரலாம்; பரிகாரமும் பொறுமையும் உதவும்."
                if harsh else "உபபதத்திலிருந்து 2-இல் சுப கிரகங்கள் இருப்பதால் இல்லறம் நீடித்து நிலைக்கும்.")))

    return {
        'arudhas': arudha_rows,
        'arudha_notes': notes,
        'karakas': karakas_list,
        'atmakaraka': ak_planet,
        'amatyakaraka': amk_planet,
        'scheme_en': 'Seven chara karakas (Sun to Saturn), by degrees within the sign',
        'scheme_ta': 'ஏழு சர காரகங்கள் (சூரியன் முதல் சனி வரை), ராசிக்குள் உள்ள பாகைகளின்படி',
        'karakamsha': {
            'sign': karakamsha_sign,
            'tamil_sign': karakamsha_tamil,
            'occupants': karakamsa_results,
            'interpretation_en': kk_en,
            'interpretation_ta': kk_ta
        }
    }

# Jaimini Arudha padas (bhava arudhas A1-A12; A1 the Arudha Lagna, A12 the Upapada)
ARUDHA_NAMES = {1: ('Arudha Lagna (AL)', 'ஆரூட லக்னம் (AL)'), 7: ('Dara Pada (A7)', 'தார பதம் (A7)'),
                10: ('Rajya Pada (A10)', 'ராஜ்ய பதம் (A10)'), 11: ('Labha Pada (A11)', 'லாப பதம் (A11)'),
                12: ('Upapada (UL)', 'உபபதம் (UL)')}


def _rasi_drishti(sign):
    """Signs a sign aspects by Jaimini rasi drishti: movable signs the fixed ones but the next,
    fixed signs the movable ones but the previous, dual signs the other duals."""
    kind = sign % 3
    if kind == 0:
        return {s for s in (1, 4, 7, 10) if s != (sign + 1) % 12}
    if kind == 1:
        return {s for s in (0, 3, 6, 9) if s != (sign - 1) % 12}
    return {s for s in (2, 5, 8, 11) if s != sign}


def _jaimini_lord(sign, planets):
    """Lord of a sign; Scorpio and Aquarius take the stronger of their two lords (Mars/Ketu,
    Saturn/Rahu) by P.V.R. Narasimha Rao's rules."""
    if sign not in (7, 10):
        return SIGN_LORDS[sign]
    main, node = ('Mars', 'Ketu') if sign == 7 else ('Saturn', 'Rahu')
    at = {q: planets[q]['sign_index'] for q in ('Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu', 'Ascendant')}
    if at[main] == sign and at[node] != sign:
        return node
    if at[node] == sign and at[main] != sign:
        return main

    def company(p):
        return sum(1 for q, s in at.items() if q != p and s == at[p])

    def support(p):
        dispositor = SIGN_LORDS[at[p]]
        return sum((at[q] == at[p]) + (at[p] in _rasi_drishti(at[q])) for q in ('Mercury', 'Jupiter', dispositor))

    def exalted(p):
        return planets[p].get('dignity') == 'Exalted'

    def modality(p):
        return (at[p] % 3 == 2) * 2 + (at[p] % 3 == 1)  # dual 2, fixed 1, movable 0

    for rule in (company, support, exalted, modality):
        a, b = rule(main), rule(node)
        if a != b:
            return main if a > b else node
    return main if planets[main]['degree'] > planets[node]['degree'] else node


def jaimini_arudhas(planets):
    asc = planets['Ascendant']['sign_index']
    padas = []
    for house in range(1, 13):
        sign = (asc + house - 1) % 12
        lord_sign = planets[_jaimini_lord(sign, planets)]['sign_index']
        pada = (2 * lord_sign - sign) % 12
        if (pada - sign) % 12 in (0, 6):  # never the house itself or its 7th: take the 10th from there
            pada = (pada + 9) % 12
        padas.append(pada)
    return padas
