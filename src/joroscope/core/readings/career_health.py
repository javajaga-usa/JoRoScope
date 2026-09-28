"""Career from the Karmajeeva and the D-10, and Ayur-Jyotish (tridosha) health readings.
"""

from .common import DIGNITY_SCORE, PLANET_TAMIL, SIGNS, SIGN_LORDS, TAMIL_SIGNS, _ordinal


# 10. D-10 Dasamsa & Career Vocation Aptitude Engine
EXALTATION_SIGN = {'Sun': 0, 'Moon': 1, 'Mars': 9, 'Mercury': 5, 'Jupiter': 3, 'Venus': 11, 'Saturn': 6}
# Means of livelihood of the Karmajeeva graha (Brihat Jataka 10.2-4, in present-day terms)
KARMAJEEVA = {
    'Sun': ('government and administration, medicine and pharmacy, gold, textiles and work under authority',
            'அரசு மற்றும் நிர்வாகம், மருத்துவம் மற்றும் மருந்துகள், தங்கம், ஜவுளி, அதிகார அமைப்புகளின் கீழ் பணி'),
    'Moon': ('agriculture, water and marine produce, dairy, hospitality, nursing and public-facing work',
             'விவசாயம், நீர் மற்றும் கடல் சார்ந்த பொருட்கள், பால் பண்ணை, விருந்தோம்பல், செவிலியம் மற்றும் மக்கள் தொடர்புப் பணிகள்'),
    'Mars': ('engineering, metals and minerals, fire and energy, defence and police, surgery and real estate',
             'பொறியியல், உலோகம் மற்றும் கனிமங்கள், நெருப்பு மற்றும் எரிசக்தி, ராணுவம் மற்றும் காவல்துறை, அறுவை சிகிச்சை, நிலம்-மனை'),
    'Mercury': ('writing, accounting, commerce, communication and information technology, and skilled crafts',
                'எழுத்து, கணக்கியல், வணிகம், தகவல் தொடர்பு மற்றும் தகவல் தொழில்நுட்பம், கைத்திறன் தொழில்கள்'),
    'Jupiter': ('teaching, law, banking and finance, religion and advisory roles',
                'ஆசிரியப் பணி, சட்டம், வங்கி மற்றும் நிதி, ஆன்மீகம், ஆலோசனைப் பணிகள்'),
    'Venus': ('arts and entertainment, fashion, jewellery and gems, luxury goods and hospitality',
              'கலை மற்றும் பொழுதுபோக்கு, ஆடை அலங்காரம், நகை மற்றும் ரத்தினங்கள், ஆடம்பரப் பொருட்கள், விருந்தோம்பல்'),
    'Saturn': ('industry and manufacturing, mining and oil, labour-intensive enterprises, public works and service organisations',
               'தொழிற்சாலை மற்றும் உற்பத்தி, சுரங்கம் மற்றும் எண்ணெய், உழைப்பு சார்ந்த நிறுவனங்கள், பொதுப்பணி மற்றும் சேவை அமைப்புகள்')
}
# Through whom wealth comes when a planet occupies the 10th (Brihat Jataka 10.1)
KARMA_SOURCE = {'Sun': ('father', 'தந்தை'), 'Moon': ('mother', 'தாய்'), 'Mars': ('rivals and competition', 'போட்டியாளர்கள்'),
                'Mercury': ('friends', 'நண்பர்கள்'), 'Jupiter': ('siblings', 'உடன்பிறந்தோர்'),
                'Venus': ('spouse and women', 'வாழ்க்கைத் துணை மற்றும் பெண்கள்'), 'Saturn': ('servants and workers', 'பணியாளர்கள்')}

def calculate_career_vocation_d10(chart):
    planets = chart['planets']
    vargas = chart.get('vargas', {})
    d10 = vargas.get('D10', {})

    asc_sign = planets['Ascendant']['sign_index']
    h10_sign = (asc_sign + 9) % 12
    h10_lord = SIGN_LORDS[h10_sign]

    archetypes = [
        {
            'id': 'executive',
            'title_en': 'Executive, Governance & Civil Administration',
            'title_ta': 'அரசு, பொதுத்துறை & தலைமை நிர்வாகம்',
            'planets': ['Sun', 'Mars', 'Jupiter'],
            'sectors_en': 'Government services, Public Policy, Corporate C-Suite, Defence, Judiciary',
            'sectors_ta': 'அரசுப் பணிகள், ஐ.ஏ.எஸ் / ஐ.பி.எஸ், தலைமை அதிகாரி, பாதுகாப்பு, நீதித்துறை'
        },
        {
            'id': 'technology',
            'title_en': 'Engineering, Software, Data & Technology',
            'title_ta': 'பொறியியல், மென்பொருள் & நவீன தொழில்நுட்பம்',
            'planets': ['Mars', 'Rahu', 'Mercury', 'Saturn'],
            'sectors_en': 'Software Engineering, AI/Data Science, Hardware, Civil Construction, Aerospace',
            'sectors_ta': 'கணினி மென்பொருள், செயற்கை நுண்ணறிவு, கட்டடப் பொறியியல், விண்வெளி, மின்னணு'
        },
        {
            'id': 'commerce',
            'title_en': 'Commerce, Finance, Enterprise & Banking',
            'title_ta': 'வணிகம், வங்கி, முதலீடு & நிதித்துறை',
            'planets': ['Mercury', 'Venus', 'Jupiter'],
            'sectors_en': 'Investment Banking, Wealth Management, FinTech, Retail Empire, Corporate Trade',
            'sectors_ta': 'வங்கி, நிதி மேலாண்மை, பங்குச் சந்தை, ஏற்றுமதி இறக்குமதி, பெரு வர்த்தகம்'
        },
        {
            'id': 'medicine',
            'title_en': 'Medicine, Healthcare, Pharmacology & Healing',
            'title_ta': 'மருத்துவம், அறுவை சிகிச்சை & மக்கள் நல்வாழ்வு',
            'planets': ['Sun', 'Mars', 'Moon', 'Jupiter', 'Ketu'],
            'sectors_en': 'Physician, Surgery, Biotechnology, Pharmaceuticals, Holistic Wellness, Nursing',
            'sectors_ta': 'மருத்துவர், அறுவை சிகிச்சை, மருந்தியல், உயிரி தொழில்நுட்பம், இயற்கை மருத்துவம்'
        },
        {
            'id': 'creative',
            'title_en': 'Law, Advisory, Academia, Creative Arts & Media',
            'title_ta': 'சட்டம், நீதி, கல்வி, கலை & ஊடகம்',
            'planets': ['Jupiter', 'Venus', 'Mercury', 'Moon'],
            'sectors_en': 'Legal Counsel, Higher Education, Film & Media, Journalism, Architecture, Creative Direction',
            'sectors_ta': 'சட்ட ஆலோசகர், பேராசிரியர், திரைப்படம், இதழியல், கட்டடக்கலை, படைப்புக் கலைகள்'
        }
    ]

    # Karmajeeva (Brihat Jataka ch. 10): from the strongest of Lagna, Moon and Sun, the lord of
    # the Navamsa held by the 10th lord shows the means of livelihood; planets in the 10th from
    # them show through whom wealth comes.
    shadbala = chart.get('shadbala', {})
    strength = lambda p: shadbala.get(p, {}).get('ratio', 0)
    references = [('Lagna', 'லக்னம்', asc_sign, strength(SIGN_LORDS[asc_sign])),
                  ('Moon', 'சந்திரன்', planets['Moon']['sign_index'], strength('Moon')),
                  ('Sun', 'சூரியன்', planets['Sun']['sign_index'], strength('Sun'))]
    ref_en, ref_ta, ref_sign, _ = max(references, key=lambda r: r[3])
    karma_sign = (ref_sign + 9) % 12
    karma_lord = SIGN_LORDS[karma_sign]
    karma_navamsa = planets[karma_lord]['vargas']['D9']
    karmajeeva = SIGN_LORDS[karma_navamsa]
    tenth_occupants = sorted({p for p in KARMAJEEVA
                              for _, _, sign, _ in references if planets[p]['sign_index'] == (sign + 9) % 12})

    d10_asc = d10.get('Ascendant', planets['Ascendant']['vargas']['D10'])

    def d10_standing(p_name):
        sign = planets[p_name]['vargas']['D10']
        if p_name in EXALTATION_SIGN and sign == EXALTATION_SIGN[p_name]:
            return 2, 'exalted', 'உச்சம்'
        if SIGN_LORDS[sign] == p_name:
            return 2, 'own sign', 'ஆட்சி'
        if p_name in EXALTATION_SIGN and sign == (EXALTATION_SIGN[p_name] + 6) % 12:
            return -1, 'debilitated', 'நீசம்'
        return 0, None, None

    def contribution(p_name):
        """How well a graha is placed for career work, roughly -10 to +20."""
        value = 3 * DIGNITY_SCORE.get(planets[p_name].get('dignity', 'Neutral'), 0) + 3 * d10_standing(p_name)[0]
        if (planets[p_name]['vargas']['D10'] - d10_asc) % 12 in (0, 3, 6, 9):
            value += 3
        if strength(p_name) >= 1:
            value += 2
        if p_name in tenth_occupants:
            value += 5
        return value

    scored = []
    for arch in archetypes:
        members = [p for p in arch['planets'] if p in planets]
        score = 50 + 1.5 * sum(contribution(p) for p in members) / len(members)
        if karmajeeva in members:
            score += 15
        if h10_lord in members:
            score += 8
        score = round(score)
        score = max(30, min(score, 98))
        scored.append({
            'id': arch['id'],
            'title_en': arch['title_en'],
            'title_ta': arch['title_ta'],
            'score': score,
            'suitability': 'Prime Calling (Highest Fit)' if score >= 80 else ('Strong Alignment' if score >= 70 else 'Moderate Potential'),
            'suitability_ta': 'முதன்மைத் தொழில் யோகம்' if score >= 80 else ('சிறந்த பொருத்தம்' if score >= 70 else 'மிதமான வாய்ப்பு'),
            'key_sectors_en': arch['sectors_en'],
            'key_sectors_ta': arch['sectors_ta']
        })

    scored.sort(key=lambda x: x['score'], reverse=True)
    top_arch = scored[0]

    kj_en, kj_ta = KARMAJEEVA[karmajeeva]
    sources_en = ', '.join(f"{p} ({KARMA_SOURCE[p][0]})" for p in tenth_occupants)
    sources_ta = ', '.join(f"{PLANET_TAMIL[p]} ({KARMA_SOURCE[p][1]})" for p in tenth_occupants)
    lord_d10_score, lord_d10_en, lord_d10_ta = d10_standing(h10_lord)
    d10_house = (planets[h10_lord]['vargas']['D10'] - d10_asc) % 12 + 1
    narrative_en = (
        f"Karmajeeva: the {ref_en} is the strongest of Lagna, Moon and Sun; the 10th from it is {SIGNS[karma_sign]}, whose lord "
        f"{karma_lord} occupies the {SIGNS[karma_navamsa]} Navamsa, ruled by {karmajeeva}. {karmajeeva} points to a livelihood "
        f"through {kj_en}. "
        + (f"Planets in the 10th from Lagna, Moon or Sun show earnings helped by {sources_en}. " if tenth_occupants else '')
        + f"In the Dasamsa (D-10), your 10th lord {h10_lord} sits in the {_ordinal(d10_house)} house"
        + (f", {lord_d10_en}" if lord_d10_en else '') + ". "
        + f"Best-fitting field: {top_arch['title_en']} ({top_arch['score']}%), for example {top_arch['key_sectors_en']}."
    )
    narrative_ta = (
        f"கர்மஜீவ விதி: லக்னம், சந்திரன், சூரியன் ஆகியவற்றில் {ref_ta} அதிக பலம் பெற்றுள்ளது; அதிலிருந்து 10-ஆம் ராசி "
        f"{TAMIL_SIGNS[karma_sign]}, அதன் அதிபதி {PLANET_TAMIL[karma_lord]} {TAMIL_SIGNS[karma_navamsa]} நவாம்சத்தில் உள்ளார்; "
        f"அந்த நவாம்ச அதிபதி {PLANET_TAMIL[karmajeeva]}. ஆகவே {kj_ta} வழியாக ஜீவனம் அமையும். "
        + (f"லக்னம், சந்திரன் அல்லது சூரியனுக்கு 10-இல் உள்ள கிரகங்களால் {sources_ta} வழியாக வருமானத்திற்கு உதவி கிட்டும். " if tenth_occupants else '')
        + f"தசாம்சத்தில் (D-10) உங்கள் 10-ஆம் அதிபதி {PLANET_TAMIL[h10_lord]} {d10_house}-ஆம் பாவத்தில்"
        + (f" {lord_d10_ta} பெற்று" if lord_d10_ta else '') + " உள்ளார். "
        + f"மிகப் பொருத்தமான துறை: {top_arch['title_ta']} ({top_arch['score']}%), உதாரணமாக {top_arch['key_sectors_ta']}."
    )

    return {
        'top_archetype': top_arch,
        'all_archetypes': scored,
        'tenth_lord': h10_lord,
        'tenth_sign': SIGNS[h10_sign],
        'tamil_tenth_sign': TAMIL_SIGNS[h10_sign],
        'karmajeeva': {
            'reference': ref_en, 'reference_ta': ref_ta,
            'tenth_sign': SIGNS[karma_sign], 'tenth_sign_ta': TAMIL_SIGNS[karma_sign],
            'tenth_lord': karma_lord, 'navamsa_sign': SIGNS[karma_navamsa], 'navamsa_sign_ta': TAMIL_SIGNS[karma_navamsa],
            'planet': karmajeeva, 'planet_ta': PLANET_TAMIL[karmajeeva],
            'livelihood_en': kj_en, 'livelihood_ta': kj_ta,
            'tenth_occupants': tenth_occupants
        },
        'd10': {'lagna': SIGNS[d10_asc], 'lagna_ta': TAMIL_SIGNS[d10_asc], 'tenth_lord_house': d10_house,
                'tenth_lord_dignity': lord_d10_en, 'tenth_lord_dignity_ta': lord_d10_ta},
        'narrative_en': narrative_en,
        'narrative_ta': narrative_ta
    }

# 11. Ayur-Jyotish & Tridosha Medical Wellness
# (Vata, Pitta, Kapha) shares: grahas per BPHS ch. 3 (Rahu like Saturn, Ketu like Mars);
# signs by element, earth signs mixed Vata-Kapha
GRAHA_DOSHA = {'Sun': (0, 1, 0), 'Moon': (0.5, 0, 0.5), 'Mars': (0, 1, 0), 'Mercury': (1 / 3, 1 / 3, 1 / 3),
               'Jupiter': (0, 0, 1), 'Venus': (0.5, 0, 0.5), 'Saturn': (1, 0, 0), 'Rahu': (1, 0, 0), 'Ketu': (0, 1, 0)}
SIGN_DOSHA = [((0, 1, 0), (0.5, 0, 0.5), (1, 0, 0), (0, 0, 1))[i % 4] for i in range(12)]
DOSHA_NAMES = (('Vata', 'வாதம்'), ('Pitta', 'பித்தம்'), ('Kapha', 'கபம்'))


def _dosha_label(shares):
    """Name of the dominant dosha(s) in a (vata, pitta, kapha) share."""
    top = max(shares)
    leading = [i for i in range(3) if shares[i] == top]
    if len(leading) == 3:
        return 'Tridosha', 'திரிதோஷம்'
    return '-'.join(DOSHA_NAMES[i][0] for i in leading), '-'.join(DOSHA_NAMES[i][1] for i in leading)

def calculate_ayur_jyotish(chart):
    planets = chart['planets']
    asc = planets['Ascendant']
    asc_sign = asc['sign_index']
    moon_sign = planets['Moon']['sign_index']
    sun_sign = planets['Sun']['sign_index']
    h6_sign = (asc_sign + 5) % 12
    h6_lord = SIGN_LORDS[h6_sign]

    # Prakriti from the Lagna, its lord, the Moon and the grahas on the Lagna (weights as in
    # Ayurvedic astrology); graha doshas per BPHS ch. 3, sign doshas by element.
    waxing = (planets['Moon']['longitude'] - planets['Sun']['longitude']) % 360 < 180
    graha_dosha = dict(GRAHA_DOSHA, Moon=(0.3, 0, 0.7) if waxing else (0.7, 0, 0.3))
    lagna_lord = SIGN_LORDS[asc_sign]
    contributions = [(3, SIGN_DOSHA[asc_sign], f"Lagna in {SIGNS[asc_sign]}", f"லக்னம் {TAMIL_SIGNS[asc_sign]}"),
                     (3, graha_dosha[lagna_lord], f"Lagna lord {lagna_lord}", f"லக்னாதிபதி {PLANET_TAMIL[lagna_lord]}"),
                     (2, SIGN_DOSHA[moon_sign], f"Moon in {SIGNS[moon_sign]}", f"சந்திரன் {TAMIL_SIGNS[moon_sign]} ராசியில்"),
                     (1, graha_dosha['Moon'], f"{'Waxing' if waxing else 'Waning'} Moon", 'வளர்பிறைச் சந்திரன்' if waxing else 'தேய்பிறைச் சந்திரன்'),
                     (1, SIGN_DOSHA[sun_sign], f"Sun in {SIGNS[sun_sign]}", f"சூரியன் {TAMIL_SIGNS[sun_sign]} ராசியில்")]
    for name in ('Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu'):
        if planets[name]['house'] == 1:
            contributions.append((2, graha_dosha[name], f"{name} in the Lagna", f"லக்னத்தில் {PLANET_TAMIL[name]}"))
        elif 1 in planets[name].get('aspects_cast', []):
            contributions.append((1, graha_dosha[name], f"{name} aspecting the Lagna", f"லக்னத்தைப் பார்க்கும் {PLANET_TAMIL[name]}"))
    vata_pts = sum(w * d[0] for w, d, _, _ in contributions)
    pitta_pts = sum(w * d[1] for w, d, _, _ in contributions)
    kapha_pts = sum(w * d[2] for w, d, _, _ in contributions)
    factors = [dict(en=f"{en}: {_dosha_label(d)[0]}", ta=f"{ta}: {_dosha_label(d)[1]}", weight=w)
               for w, d, en, ta in contributions]

    total = vata_pts + pitta_pts + kapha_pts
    v_pct = int(round(vata_pts / total * 100))
    p_pct = int(round(pitta_pts / total * 100))
    k_pct = 100 - (v_pct + p_pct)

    scores = sorted([('Vata', v_pct, 'வாத'), ('Pitta', p_pct, 'பித்த'), ('Kapha', k_pct, 'கப')], key=lambda x: x[1], reverse=True)
    dom1, dom2 = scores[0], scores[1]
    prakriti_en = f"{dom1[0]}-{dom2[0]} Dominant" if abs(dom1[1] - dom2[1]) <= 12 else f"{dom1[0]} Dominant"
    prakriti_ta = f"{dom1[2]}-{dom2[2]} பிரகிருதி" if abs(dom1[1] - dom2[1]) <= 12 else f"{dom1[2]} பிரதான பிரகிருதி"

    body_map = {
        'Aries': ('Head, cranium, facial nerves, and ocular vitality', 'தலை, மூளை, கண் மற்றும் நரம்பு மண்டலம்'),
        'Taurus': ('Throat, vocal cords, thyroid gland, and cervical spine', 'தொண்டை, தைராய்டு சுரப்பி மற்றும் கழுத்துப் பகுதி'),
        'Gemini': ('Respiratory airways, bronchial tract, shoulders, and arms', 'சுவாசக் குழாய், நுரையீரல், தோள்பட்டை மற்றும் கைகள்'),
        'Cancer': ('Chest, gastric stomach lining, digestion, and breast tissue', 'மார்பகம், இரைப்பை, செரிமானம் மற்றும் நுரையீரல்'),
        'Leo': ('Heart circulation, spine, mid-back, and solar vitality', 'இதயம், ரத்த ஓட்டம், முதுகுத்தண்டு மற்றும் ஆன்ம பலம்'),
        'Virgo': ('Intestinal assimilation, abdominal metabolism, and nervous digestion', 'குடல் பகுதி, செரிமான மண்டலம் மற்றும் வயிற்று நரம்புகள்'),
        'Libra': ('Kidneys, lumbar lower back, and fluid osmotic balance', 'சிறுநீரகம், இடுப்புப் பகுதி மற்றும் நீர்க்கட்டு சமநிலை'),
        'Scorpio': ('Excretory organs, pelvic reproductive tract, and colon', 'மர்ம உறுப்புகள், கழிவு மண்டலம் மற்றும் இடுப்பு எலும்பு'),
        'Sagittarius': ('Hips, thighs, arterial circulation, and hepatic liver enzymes', 'இடுப்பு, தொடைகள், கல்லீரல் மற்றும் தமனி ரத்த ஓட்டம்'),
        'Capricorn': ('Knee joints, skeletal bone density, skin, and cartilage', 'முழங்கால் மூட்டுகள், எலும்பு உறுதி மற்றும் தோல் பகுதி'),
        'Aquarius': ('Calves, shins, ankles, and autonomic nervous circulation', 'கால் முட்டி, கணுக்கால் மற்றும் ரத்த ஓட்ட நரம்புகள்'),
        'Pisces': ('Feet, lymphatic drainage, immune immunity, and sleep cycles', 'பாதங்கள், நிணநீர் மண்டலம், நோய் எதிர்ப்பு சக்தி மற்றும் தூக்கம்')
    }

    vuln_en, vuln_ta = body_map.get(SIGNS[h6_sign], ('Metabolic balance and vitality', 'உடல் நலம் மற்றும் சீரான இயக்கம்'))
    # Grahas in the 6th (disease) and 8th (chronic ailments) and where the 6th lord sits
    health_watch = []
    for name in ('Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu'):
        house = planets[name]['house']
        if house in (6, 8):
            label_en, label_ta = _dosha_label(GRAHA_DOSHA[name])
            health_watch.append(dict(
                en=f"{name} in the {_ordinal(house)} house: watch {label_en} imbalance and {body_map[SIGNS[planets[name]['sign_index']]][0].lower()}.",
                ta=f"{house}-ஆம் பாவத்தில் {PLANET_TAMIL[name]}: {label_ta} சமநிலையிலும் {body_map[SIGNS[planets[name]['sign_index']]][1]} பகுதியிலும் கவனம் தேவை."))
    h6_lord_house = planets[h6_lord]['house']
    health_watch.append(dict(
        en=f"The 6th lord {h6_lord} sits in the {_ordinal(h6_lord_house)} house, in {planets[h6_lord]['sign']}.",
        ta=f"6-ஆம் அதிபதி {PLANET_TAMIL[h6_lord]} {h6_lord_house}-ஆம் பாவத்தில், {planets[h6_lord]['tamil']} ராசியில் உள்ளார்."))

    lifestyle_en = (
        f"Your constitution is characterized by {prakriti_en} (Vata: {v_pct}%, Pitta: {p_pct}%, Kapha: {k_pct}%). "
        f"{'Focus on warm nourishing foods, regular sleep timing, and grounding warm sesame oil massages.' if 'Vata' in prakriti_en else ''}"
        f"{'Favor cooling hydrating foods, sweet/bitter tastes, moderate physical exertion, and avoid excess spices.' if 'Pitta' in prakriti_en else ''}"
        f"{'Emphasize light stimulating foods, warming spices (ginger/black pepper), active cardio exercise, and early rising.' if 'Kapha' in prakriti_en else ''}"
    )

    lifestyle_ta = (
        f"உங்கள் உடல் அமைப்பு {prakriti_ta} தன்மை கொண்டது (வாதம்: {v_pct}%, பித்தம்: {p_pct}%, கபம்: {k_pct}%). "
        f"{'மிதமான சூடான சத்தான உணவுகள், சீரான தூக்க நேரம் மற்றும் நல்லெண்ணெய் மசாஜ் நலம் தரும்.' if 'Vata' in prakriti_en else ''}"
        f"{'குளிர்ச்சியான நீர்ச்சத்து மிக்க உணவுகள், அதிக காரத்தைத் தவிர்த்தல் மற்றும் மன அமைதி தரும் தியானம் நலம்.' if 'Pitta' in prakriti_en else ''}"
        f"{'எளிதில் செரிக்கும் உணவுகள், மிளகு/இஞ்சி சேர்த்த சுக்குநீர் மற்றும் சுறுசுறுப்பான உடற்பயிற்சி ஆரோக்கியம் காக்கும்.' if 'Kapha' in prakriti_en else ''}"
    )

    return {
        'prakriti_en': prakriti_en,
        'prakriti_ta': prakriti_ta,
        'vata_percentage': v_pct,
        'pitta_percentage': p_pct,
        'kapha_percentage': k_pct,
        'sixth_house_sign': SIGNS[h6_sign],
        'sixth_house_tamil': TAMIL_SIGNS[h6_sign],
        'sixth_house_lord': h6_lord,
        'anatomical_vulnerabilities_en': vuln_en,
        'anatomical_vulnerabilities_ta': vuln_ta,
        'lifestyle_guidance_en': lifestyle_en,
        'lifestyle_guidance_ta': lifestyle_ta,
        'factors': factors,
        'health_watch': health_watch
    }
