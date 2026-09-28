"""Marriage (Kalatra) and career reports: what the chart promises and when it is likely to come.

Marriage reads the 7th house (its sign, lord, occupants and aspects), Venus and Jupiter as karakas,
the Darakaraka and the Upapada (Jaimini), and the 7th of the Navamsa; career reads the 10th house,
its lord, the 10th of the Dasamsa and the Amatyakaraka. The timing lists the Dasa-Bhukti periods
whose lords signify the matter (the house lord, its occupants, the karakas and the Jaimini
significator), strongest when both the Dasa and Bhukti lords do, with K.N. Rao's double-transit
windows when the report has them.
"""
from datetime import datetime, timezone

from .common import DIGNITY_SCORE, HOUSE_THEMES, PLANET_TAMIL, SIGN_LORDS, SIGNS, TAMIL_SIGNS
from .report import card, chapter, table

GRAHA_ASPECTS = {'Mars': (4, 7, 8), 'Jupiter': (5, 7, 9), 'Saturn': (3, 7, 10)}
BENEFICS = ('Jupiter', 'Venus', 'Mercury', 'Moon')
MALEFICS = ('Sun', 'Mars', 'Saturn', 'Rahu', 'Ketu')
SPOUSE_BY_GRAHA = {
    'Sun': ('dignified, principled and proud, often from a respected family', 'கண்ணியமும் கொள்கைப் பிடிப்பும் உடையவர், மதிப்பான குடும்பத்தவர்'),
    'Moon': ('gentle, caring and emotional, fond of home and family', 'மென்மையும் அன்பும் உணர்ச்சியும் உடையவர், இல்லறப் பற்றுள்ளவர்'),
    'Mars': ('energetic, frank and courageous, with a quick temper', 'சுறுசுறுப்பும் வெளிப்படையும் தைரியமும் உடையவர், சற்று முன்கோபம்'),
    'Mercury': ('youthful, witty and educated, good with words and business', 'இளமைத் தோற்றமும் நகைச்சுவையும் கல்வியும் உடையவர், பேச்சிலும் வணிகத்திலும் திறமை'),
    'Jupiter': ('wise, religious and generous, a good adviser', 'ஞானமும் பக்தியும் தாராள மனமும் உடையவர், நல்ல ஆலோசகர்'),
    'Venus': ('attractive, artistic and affectionate, fond of comforts', 'அழகும் கலையுணர்வும் அன்பும் உடையவர், சுகங்களில் விருப்பம்'),
    'Saturn': ('mature, hardworking and serious, possibly older or from a different background', 'முதிர்ச்சியும் உழைப்பும் தீவிரமும் உடையவர், வயதில் மூத்தவர் அல்லது மாறுபட்ட பின்னணி'),
    'Rahu': ('unconventional or from a different culture or place', 'மரபுக்கு மாறானவர் அல்லது வேறு பண்பாடு, இடத்தைச் சேர்ந்தவர்'),
    'Ketu': ('spiritual, reserved and detached', 'ஆன்மீக நாட்டமும் அமைதியும் பற்றின்மையும் உடையவர்'),
}


def _house(planets, g):
    return (planets[g]['sign_index'] - planets['Ascendant']['sign_index']) % 12 + 1


def _aspecting(planets, sign):
    """Grahas that aspect a sign by Parasari drishti (all the 7th; Mars, Jupiter and Saturn their extra ones)."""
    out = []
    for g in ('Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'):
        d = (sign - planets[g]['sign_index']) % 12 + 1
        if d in GRAHA_ASPECTS.get(g, (7,)):
            out.append(g)
    return out


def _dignity_words(planets, g):
    d = planets[g].get('dignity', 'Neutral')
    score = DIGNITY_SCORE.get(d, 0)
    return d, score


def period_windows(dasha_rows, significators, now, horizon_years=25, limit=8):
    """Future Dasa-Bhukti periods (up to horizon_years ahead) whose lords signify a matter."""
    rows = []
    end_limit = now.timestamp() + horizon_years * 365.25 * 86400
    for md in dasha_rows:
        for b in md['subperiods']:
            start, end = datetime.fromisoformat(b['start']), datetime.fromisoformat(b['end'])
            if end <= now or start.timestamp() > end_limit:
                continue
            hits = (md['lord'] in significators) + (b['lord'] in significators)
            if hits and b['lord'] in significators:
                rows.append(dict(dasa=md['lord'], bhukti=b['lord'], start=b['start'][:10], end=b['end'][:10],
                                 strength='strong' if hits == 2 else 'moderate', running=start <= now < end))
    rows.sort(key=lambda r: (r['strength'] != 'strong', r['start']))
    chosen = sorted(rows[:limit], key=lambda r: r['start'])
    return chosen


def _window_rows(windows):
    return [((f"{w['dasa']} / {w['bhukti']}", f"{PLANET_TAMIL[w['dasa']]} / {PLANET_TAMIL[w['bhukti']]}"), w['start'], w['end'],
             ('strong' if w['strength'] == 'strong' else 'moderate', 'வலுவானது' if w['strength'] == 'strong' else 'மிதமானது'))
            for w in windows]


def _karaka(jaimini, code):
    return next((k['planet'] for k in (jaimini or {}).get('karakas', []) if k.get('code') == code), None)


def _dt_windows(double_transit, key):
    for m in (double_transit or {}).get('milestones', []):
        if m.get('key') == key:
            return m.get('windows') or []
    return []


def calculate_marriage_report(chart, jaimini=None, double_transit=None, now=None):
    now = now or datetime.now(timezone.utc)
    planets = chart['planets']
    asc = planets['Ascendant']['sign_index']
    seventh = (asc + 6) % 12
    lord7 = SIGN_LORDS[seventh]
    occupants = [g for g in ('Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu')
                 if planets[g]['sign_index'] == seventh]
    aspects = [g for g in _aspecting(planets, seventh) if g not in occupants]
    lord_house = _house(planets, lord7)
    lord_dig, lord_score = _dignity_words(planets, lord7)
    venus_dig, venus_score = _dignity_words(planets, 'Venus')
    dk = _karaka(jaimini, 'DK')
    d9 = planets['Ascendant']['vargas']['D9']
    d9_lord7 = SIGN_LORDS[(d9 + 6) % 12]
    upapada = None
    arudhas = (jaimini or {}).get('arudhas') or []
    ul = next((a for a in arudhas if a.get('code') in ('A12', 'UL')), None)
    if ul:
        upapada = SIGNS.index(ul['sign'])

    good = [g for g in occupants + aspects if g in BENEFICS]
    hard = [g for g in occupants + aspects if g in MALEFICS]
    score = lord_score + venus_score + len(good) - len(hard) + (1 if lord_house in (1, 4, 5, 7, 9, 10, 11) else -1)
    verdict = 'good' if score >= 2 else ('bad' if score <= -2 else 'mixed')

    traits = [g for g in occupants] or [lord7]
    trait_en = '; '.join(SPOUSE_BY_GRAHA[g][0] for g in traits[:2])
    trait_ta = '; '.join(SPOUSE_BY_GRAHA[g][1] for g in traits[:2])
    cards = [
        card('💞', f'The 7th house: {SIGNS[seventh]}', f'7-ஆம் இடம்: {TAMIL_SIGNS[seventh]}',
             f"The 7th lord {lord7} is in house {lord_house} ({HOUSE_THEMES[lord_house][0]}), {lord_dig.lower()}. "
             + (f"In the 7th: {', '.join(occupants)}. " if occupants else 'No graha occupies the 7th. ')
             + (f"Aspecting it: {', '.join(aspects)}. " if aspects else '')
             + (f"Benefic influence ({', '.join(good)}) supports harmony. " if good else '')
             + (f"Malefic influence ({', '.join(hard)}) asks for patience and understanding." if hard else ''),
             f"7-ஆம் அதிபதி {PLANET_TAMIL[lord7]} {lord_house}-ஆம் இடத்தில் ({HOUSE_THEMES[lord_house][1]}). "
             + (f"7-இல்: {', '.join(PLANET_TAMIL[g] for g in occupants)}. " if occupants else '7-ஆம் இடத்தில் கிரகம் இல்லை. ')
             + (f"பார்வை: {', '.join(PLANET_TAMIL[g] for g in aspects)}. " if aspects else '')
             + (f"சுபர் தொடர்பு ({', '.join(PLANET_TAMIL[g] for g in good)}) இணக்கம் தரும். " if good else '')
             + (f"பாபர் தொடர்பு ({', '.join(PLANET_TAMIL[g] for g in hard)}) பொறுமையும் புரிதலும் கேட்கும்." if hard else ''),
             verdict=verdict),
        card('🌸', f'Venus, the karaka of marriage: {venus_dig}', f'களத்திர காரகன் சுக்கிரன்: {venus_dig}',
             f"Venus is in house {_house(planets, 'Venus')} in {planets['Venus']['sign']}. "
             + ('A well-placed Venus favours affection and a comfortable married life.' if venus_score > 0 else
                'Venus needs support, so nurture romance and shared interests.' if venus_score < 0 else
                'Venus is moderately placed.')
             + ' For a woman\'s chart Jupiter is also read as the husband\'s karaka: it is in house '
             + f"{_house(planets, 'Jupiter')}, {planets['Jupiter'].get('dignity', 'Neutral').lower()}.",
             f"சுக்கிரன் {_house(planets, 'Venus')}-ஆம் இடத்தில் {TAMIL_SIGNS[planets['Venus']['sign_index']]} ராசியில். "
             + ('நன்கு அமைந்த சுக்கிரன் அன்பையும் சுகமான இல்லறத்தையும் தரும்.' if venus_score > 0 else
                'சுக்கிரனுக்கு ஆதரவு தேவை; அன்பையும் பொது ஆர்வங்களையும் வளர்க்கவும்.' if venus_score < 0 else
                'சுக்கிரன் மிதமான நிலையில் உள்ளது.')
             + f" பெண் ஜாதகத்தில் குருவும் கணவர் காரகன்: குரு {_house(planets, 'Jupiter')}-ஆம் இடத்தில்."),
        card('👤', 'The spouse', 'வாழ்க்கைத்துணை',
             f"The 7th house points to a partner who is {trait_en}. The Navamsa's 7th lord is {d9_lord7}"
             + (f", and the Darakaraka is {dk}" if dk else '') + '.',
             f"7-ஆம் இடம் காட்டும் வாழ்க்கைத்துணை: {trait_ta}. நவாம்ச 7-ஆம் அதிபதி {PLANET_TAMIL[d9_lord7]}"
             + (f"; தாரகாரகன் {PLANET_TAMIL[dk]}" if dk else '') + '.'),
    ]
    if upapada is not None:
        second = (upapada + 1) % 12
        in_second = [g for g in ('Sun', 'Mars', 'Saturn', 'Rahu', 'Ketu') if planets[g]['sign_index'] == second]
        cards.append(card('🪷', f'Upapada in {SIGNS[upapada]}', f'உபபதம் {TAMIL_SIGNS[upapada]}',
                          "The Upapada (the arudha of the 12th) shows the marriage itself; the 2nd from it shows its continuity. "
                          + (f"Malefics there ({', '.join(in_second)}) call for care to keep the bond steady." if in_second else
                             'No malefic sits in its 2nd, which supports a lasting bond.'),
                          "உபபதம் (12-ஆம் ஆரூடம்) திருமணத்தையும், அதன் 2-ஆம் இடம் அதன் நீடிப்பையும் காட்டும். "
                          + (f"அங்கு பாபர்கள் ({', '.join(PLANET_TAMIL[g] for g in in_second)}): உறவை நிலைப்படுத்தக் கவனம் தேவை." if in_second else
                             'அதன் 2-இல் பாபர் இல்லை; நீடித்த உறவுக்கு ஆதரவு.'),
                          verdict='mixed' if in_second else 'good'))
    doshas = chart.get('doshas') or {}
    chevvai = doshas.get('chevvai') or {}
    if chevvai.get('effective', chevvai.get('present') and not chevvai.get('cancelled')):
        cards.append(card('🛡️', 'Chevvai Dosham', 'செவ்வாய் தோஷம்',
                          'Chevvai Dosham is present: match with a partner with a similar dosha (dosha samyam), and see the Parihara chapter.',
                          'செவ்வாய் தோஷம் உள்ளது: இதே தோஷம் உள்ள வரனுடன் பொருத்தவும் (தோஷ சாம்யம்); பரிகார அத்தியாயத்தைப் பார்க்கவும்.',
                          verdict='bad'))

    significators = {lord7, 'Venus', d9_lord7, *occupants} | ({dk} if dk else set())
    windows = period_windows(chart.get('dasha') or [], significators, now)
    dt = _dt_windows(double_transit, 'marriage')
    cards.append(card('⏳', 'When', 'எப்போது',
                      (f"Periods whose lords signify marriage ({', '.join(sorted(significators))}) are listed below; the strongest are those where "
                       'both the Dasa and Bhukti lords do.' if windows else 'No strongly marked marriage period falls in the coming years.')
                      + (f" Saturn and Jupiter together activate the 7th (double transit) in {len(dt)} window(s) ahead." if dt else ''),
                      (f"திருமணக் காரகக் கிரகங்களின் ({', '.join(PLANET_TAMIL[g] for g in sorted(significators))}) காலங்கள் கீழே; "
                       'தசா, புக்தி அதிபதிகள் இருவரும் காரகர்களானால் வலுவானவை.' if windows else 'வரும் ஆண்டுகளில் தெளிவான திருமணக் காலம் இல்லை.')
                      + (f" சனியும் குருவும் சேர்ந்து 7-ஆம் இடத்தைத் தூண்டும் (இரட்டைக் கோச்சாரம்) காலங்கள்: {len(dt)}." if dt else '')))
    return chapter(
        'marriage', 'Marriage (Kalatra) Report', 'திருமண (களத்திர) அறிக்கை',
        'What the chart promises for marriage (the 7th house, Venus and Jupiter, the Darakaraka, Upapada and Navamsa) and '
        'the periods that bring it.',
        'திருமணம் குறித்து ஜாதகம் தருவது (7-ஆம் இடம், சுக்கிரன், குரு, தாரகாரகன், உபபதம், நவாம்சம்) மற்றும் அதைத் தரும் காலங்கள்.',
        cards=cards,
        tables=[table('Periods for marriage', 'திருமணக் காலங்கள்',
                      [('Dasa / Bhukti', 'தசை / புக்தி'), ('From', 'முதல்'), ('To', 'வரை'), ('Strength', 'வலு')], _window_rows(windows))],
        significators=sorted(significators), windows=windows, verdict=verdict)


def calculate_career_report(chart, jaimini=None, career_d10=None, double_transit=None, now=None):
    now = now or datetime.now(timezone.utc)
    planets = chart['planets']
    asc = planets['Ascendant']['sign_index']
    tenth = (asc + 9) % 12
    lord10 = SIGN_LORDS[tenth]
    occupants = [g for g in ('Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu')
                 if planets[g]['sign_index'] == tenth]
    amk = _karaka(jaimini, 'AmK')
    d10 = planets['Ascendant']['vargas']['D10']
    d10_lord10 = SIGN_LORDS[(d10 + 9) % 12]
    lord_house = _house(planets, lord10)
    lord_dig, lord_score = _dignity_words(planets, lord10)
    field_en = field_ta = ''
    if career_d10 and career_d10.get('top_archetype'):
        top = career_d10['top_archetype']
        field_en = f" The best-fitting field is {top.get('name_en', top.get('title_en', ''))}."
        field_ta = f" பொருத்தமான துறை: {top.get('name_ta', top.get('title_ta', ''))}."
    cards = [
        card('💼', f'The 10th house: {SIGNS[tenth]}', f'10-ஆம் இடம்: {TAMIL_SIGNS[tenth]}',
             f"The 10th lord {lord10} is in house {lord_house} ({HOUSE_THEMES[lord_house][0]}), {lord_dig.lower()}. "
             + (f"In the 10th: {', '.join(occupants)}, whose nature shapes the work. " if occupants else '')
             + f"The Dasamsa's 10th lord is {d10_lord10}" + (f" and the Amatyakaraka is {amk}" if amk else '') + '.' + field_en,
             f"10-ஆம் அதிபதி {PLANET_TAMIL[lord10]} {lord_house}-ஆம் இடத்தில் ({HOUSE_THEMES[lord_house][1]}). "
             + (f"10-இல்: {', '.join(PLANET_TAMIL[g] for g in occupants)}; இவை தொழிலின் தன்மையை வடிவமைக்கும். " if occupants else '')
             + f"தசாம்ச 10-ஆம் அதிபதி {PLANET_TAMIL[d10_lord10]}" + (f"; அமாத்யகாரகன் {PLANET_TAMIL[amk]}" if amk else '') + '.' + field_ta,
             verdict='good' if lord_score > 0 and lord_house not in (6, 8, 12) else ('bad' if lord_score < 0 and lord_house in (6, 8, 12) else 'mixed')),
    ]
    significators = {lord10, d10_lord10, 'Sun', 'Saturn', *occupants} | ({amk} if amk else set())
    windows = period_windows(chart.get('dasha') or [], significators, now)
    dt = _dt_windows(double_transit, 'career')
    cards.append(card('📈', 'Periods of rise', 'உயர்வுக் காலங்கள்',
                      (f"Periods ruled by the career significators ({', '.join(sorted(significators))}) bring promotions, new roles and "
                       'recognition; the strongest are listed below.' if windows else 'No strongly marked career period falls in the coming years.')
                      + (f" Double transit on the 10th: {len(dt)} window(s) ahead." if dt else ''),
                      (f"தொழில் காரகர்களின் ({', '.join(PLANET_TAMIL[g] for g in sorted(significators))}) காலங்கள் பதவி உயர்வு, புதிய பொறுப்பு, "
                       'அங்கீகாரம் தரும்; வலுவானவை கீழே.' if windows else 'வரும் ஆண்டுகளில் தெளிவான தொழில் உயர்வுக் காலம் இல்லை.')
                      + (f" 10-ஆம் இடத்தில் இரட்டைக் கோச்சாரம்: {len(dt)} காலங்கள்." if dt else '')))
    return chapter(
        'career_report', 'Career Report', 'தொழில் அறிக்கை',
        'The 10th house, its lord, the Dasamsa and the Amatyakaraka, with the periods that bring rise in work.',
        '10-ஆம் இடம், அதன் அதிபதி, தசாம்சம், அமாத்யகாரகன் மற்றும் தொழில் உயர்வுக் காலங்கள்.',
        cards=cards,
        tables=[table('Periods for career', 'தொழில் காலங்கள்',
                      [('Dasa / Bhukti', 'தசை / புக்தி'), ('From', 'முதல்'), ('To', 'வரை'), ('Strength', 'வலு')], _window_rows(windows))],
        significators=sorted(significators), windows=windows)
