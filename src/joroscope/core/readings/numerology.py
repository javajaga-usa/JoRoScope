"""Numerology in the Chaldean (Cheiro) system used in India: the birth (psychic) number from the day,
the destiny number from the whole date, and the name number from the letters of the English
spelling. Each number 1-9 has a ruling graha (1 Sun, 2 Moon, 3 Jupiter, 4 Rahu, 5 Mercury,
6 Venus, 7 Ketu, 8 Saturn, 9 Mars); numbers agree when their grahas are natural friends, with Rahu
read as Saturn and Ketu as Mars, as Indian numerologists do.
"""
from .common import PLANET_TAMIL
from .report import card, chapter, table

CHALDEAN = {**dict.fromkeys('AIJQY', 1), **dict.fromkeys('BKR', 2), **dict.fromkeys('CGLS', 3),
            **dict.fromkeys('DMT', 4), **dict.fromkeys('EHNX', 5), **dict.fromkeys('UVW', 6),
            **dict.fromkeys('OZ', 7), **dict.fromkeys('FP', 8)}
NUMBER_GRAHA = {1: 'Sun', 2: 'Moon', 3: 'Jupiter', 4: 'Rahu', 5: 'Mercury', 6: 'Venus', 7: 'Ketu', 8: 'Saturn', 9: 'Mars'}
AS_GRAHA = {'Rahu': 'Saturn', 'Ketu': 'Mars'}
NUMBER_DAYS = {1: ('Sunday', 'ஞாயிறு'), 2: ('Monday', 'திங்கள்'), 3: ('Thursday', 'வியாழன்'), 4: ('Saturday', 'சனி'),
               5: ('Wednesday', 'புதன்'), 6: ('Friday', 'வெள்ளி'), 7: ('Monday', 'திங்கள்'), 8: ('Saturday', 'சனி'),
               9: ('Tuesday', 'செவ்வாய்')}
NUMBER_READINGS = {
    1: ('Leadership and independence: ambitious, original and self-reliant, happiest in charge of their own work. Guard against pride and impatience.',
        'தலைமையும் சுதந்திரமும்: லட்சியமும் தனித்தன்மையும் தன்னம்பிக்கையும் உடையவர்; தம் பணியைத் தாமே நடத்துவதில் மகிழ்வர். கர்வம், பொறுமையின்மை தவிர்க்கவும்.'),
    2: ('Sensitivity and partnership: gentle, imaginative and cooperative, gifted in diplomacy and the arts. Moods can swing; steady routines help.',
        'மென்மையும் கூட்டுறவும்: கனிவும் கற்பனையும் ஒத்துழைப்பும் உடையவர்; இராஜதந்திரத்திலும் கலைகளிலும் திறமை. மனநிலை மாறக்கூடும்; ஒழுங்கான நடைமுறை உதவும்.'),
    3: ('Wisdom and expansion: optimistic, disciplined and fond of learning, respected as a teacher or adviser. Avoid being dogmatic.',
        'ஞானமும் வளர்ச்சியும்: நம்பிக்கையும் ஒழுக்கமும் கல்வியார்வமும் உடையவர்; ஆசிரியராகவோ ஆலோசகராகவோ மதிக்கப்படுவர். பிடிவாதம் தவிர்க்கவும்.'),
    4: ('Unconventional energy: practical, hardworking and original, often going against the tide. Sudden changes come; plan finances carefully.',
        'மாறுபட்ட ஆற்றல்: நடைமுறை அறிவும் உழைப்பும் புதுமையும் உடையவர்; பெரும்பாலும் வழக்கத்திற்கு மாறாகச் செல்வர். திடீர் மாற்றங்கள் வரும்; நிதியைக் கவனமாகத் திட்டமிடவும்.'),
    5: ('Intellect and commerce: quick-witted, versatile and communicative, good in trade, travel and learning. Restlessness needs direction.',
        'அறிவும் வணிகமும்: கூர்மையான அறிவும் பல்திறனும் பேச்சுத்திறனும் உடையவர்; வணிகம், பயணம், கல்வியில் சிறப்பர். அமைதியின்மையை நெறிப்படுத்தவும்.'),
    6: ('Harmony and comfort: artistic, affectionate and fond of beauty, home and family; attracts friends and comforts. Avoid overindulgence.',
        'இணக்கமும் சுகமும்: கலையார்வமும் அன்பும் அழகு, இல்லம், குடும்பம் மீது பற்றும் உடையவர்; நண்பர்களையும் வசதிகளையும் ஈர்ப்பர். மிதமிஞ்சிய ஆசை தவிர்க்கவும்.'),
    7: ('Insight and spirituality: reflective, intuitive and philosophical, drawn to research, travel and the inner life. Share plans with others.',
        'உள்ளுணர்வும் ஆன்மீகமும்: சிந்தனையும் உள்ளுணர்வும் தத்துவ நாட்டமும் உடையவர்; ஆராய்ச்சி, பயணம், அகவாழ்வில் ஈர்ப்பு. திட்டங்களைப் பிறருடன் பகிரவும்.'),
    8: ('Endurance and responsibility: serious, persevering and just; success comes slowly but lasts. Patience and service ease the delays.',
        'பொறுமையும் பொறுப்பும்: தீவிரமும் விடாமுயற்சியும் நேர்மையும் உடையவர்; வெற்றி தாமதமாக வந்தாலும் நிலைக்கும். பொறுமையும் சேவையும் தடைகளைக் குறைக்கும்.'),
    9: ('Courage and drive: energetic, brave and generous, a fighter for causes, good in action and command. Temper and haste need control.',
        'தைரியமும் உத்வேகமும்: சுறுசுறுப்பும் வீரமும் தாராள மனமும் உடையவர்; செயலிலும் தலைமையிலும் சிறப்பர். கோபத்தையும் அவசரத்தையும் கட்டுப்படுத்தவும்.'),
}
RELATION_WORDS = {1: ('in harmony', 'இணக்கமானவை', 'good'), 0: ('neutral to each other', 'நடுநிலையானவை', 'mixed'),
                  -1: ('at odds', 'முரண்பட்டவை', 'bad')}


def reduce_number(n):
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n


def name_number(name):
    """(compound total, reduced number) of the Latin letters in a name, or None without any."""
    values = [CHALDEAN[ch] for ch in name.upper() if ch in CHALDEAN]
    if not values:
        return None
    total = sum(values)
    return total, reduce_number(total)


def relation(a, b):
    """Natural friendship between the grahas of two numbers: 1 friends, 0 neutral, -1 enemies."""
    from ..engine import NATURAL_FRIENDS
    ga, gb = (AS_GRAHA.get(NUMBER_GRAHA[n], NUMBER_GRAHA[n]) for n in (a, b))
    if ga == gb:
        return 1
    one, two = NATURAL_FRIENDS[ga].get(gb, 0), NATURAL_FRIENDS[gb].get(ga, 0)
    return 1 if one + two > 0 else (-1 if one + two < 0 else 0)


def calculate_numerology(chart):
    profile = chart.get('profile') or {}
    date = profile.get('date', '')
    name = (profile.get('name') or '').strip()
    try:
        year, month, day = (int(x) for x in date.split('-'))
    except ValueError:
        return None
    birth = reduce_number(day)
    destiny = reduce_number(sum(int(d) for d in f'{day}{month}{year}'))
    named = name_number(name)
    graha = lambda n: NUMBER_GRAHA[n]
    graha_ta = lambda n: PLANET_TAMIL[NUMBER_GRAHA[n]]

    cards = [
        card('🎂', f'Birth number {birth} ({graha(birth)})', f'பிறவி எண் {birth} ({graha_ta(birth)})',
             NUMBER_READINGS[birth][0], NUMBER_READINGS[birth][1],
             f'From the day of birth, {day}: how you think and act day to day.',
             f'பிறந்த தேதி {day}-இலிருந்து: அன்றாட எண்ணமும் செயலும்.'),
        card('🧭', f'Destiny number {destiny} ({graha(destiny)})', f'விதி எண் {destiny} ({graha_ta(destiny)})',
             NUMBER_READINGS[destiny][0], NUMBER_READINGS[destiny][1],
             'From the whole date of birth: the direction life takes.',
             'முழுப் பிறந்த தேதியிலிருந்து: வாழ்க்கை செல்லும் திசை.'),
    ]
    rows = [(('Birth number', 'பிறவி எண்'), birth, (graha(birth), graha_ta(birth)), NUMBER_DAYS[birth]),
            (('Destiny number', 'விதி எண்'), destiny, (graha(destiny), graha_ta(destiny)), NUMBER_DAYS[destiny])]
    name_info = None
    if named:
        total, number = named
        rows.append((('Name number', 'பெயர் எண்'), f'{number} ({total})', (graha(number), graha_ta(number)), NUMBER_DAYS[number]))
        with_birth, with_destiny = relation(number, birth), relation(number, destiny)
        worst = min(with_birth, with_destiny)
        en_b, ta_b, _ = RELATION_WORDS[with_birth]
        en_d, ta_d, _ = RELATION_WORDS[with_destiny]
        good_totals = [n for n in range(1, 10) if relation(n, birth) >= 0 and relation(n, destiny) >= 0 and
                       (relation(n, birth) + relation(n, destiny)) > 0]
        advice_en = ('The name supports the birth and destiny numbers.' if worst >= 0 else
                     f"A spelling that totals to {', '.join(map(str, good_totals))} would agree better with the birth and destiny numbers.")
        advice_ta = ('பெயர் பிறவி எண்ணுக்கும் விதி எண்ணுக்கும் துணை நிற்கிறது.' if worst >= 0 else
                     f"கூட்டுத்தொகை {', '.join(map(str, good_totals))} வரும் எழுத்துக்கூட்டல் பிறவி, விதி எண்களுடன் மேலும் இணங்கும்.")
        cards.append(card(
            '✍️', f'Name number {number} ({graha(number)})', f'பெயர் எண் {number} ({graha_ta(number)})',
            f"{NUMBER_READINGS[number][0]} With the birth number it is {en_b}; with the destiny number it is {en_d}. {advice_en}",
            f"{NUMBER_READINGS[number][1]} பிறவி எண்ணுடன் {ta_b}; விதி எண்ணுடன் {ta_d}. {advice_ta}",
            f'"{name}" totals {total} in the Chaldean values.', f'"{name}" கல்தேய மதிப்புகளில் {total}.',
            verdict=RELATION_WORDS[worst][2]))
        name_info = dict(name=name, total=total, number=number, with_birth=with_birth, with_destiny=with_destiny,
                         harmonious_numbers=good_totals)
    else:
        cards.append(card('✍️', 'Name number', 'பெயர் எண்',
                          'Numerology reads the English spelling of the name; enter the name in English letters to see its number.',
                          'எண் கணிதம் பெயரின் ஆங்கில எழுத்துக்கூட்டலைப் படிக்கிறது; பெயர் எண்ணைக் காண ஆங்கில எழுத்துகளில் பெயரை உள்ளிடவும்.'))

    lucky = sorted({birth, destiny} | {n for n in range(1, 10) if relation(n, birth) > 0})
    return chapter(
        'numerology', 'Numerology', 'எண் கணிதம்',
        'Chaldean numerology as practised in India: each number is ruled by a graha, and numbers agree when their grahas are friends.',
        'இந்தியாவில் பின்பற்றப்படும் கல்தேய எண் கணிதம்: ஒவ்வொரு எண்ணுக்கும் ஒரு கிரகம் அதிபதி; அவற்றின் கிரகங்கள் நட்பானால் எண்கள் இணங்கும்.',
        cards=cards,
        tables=[table('Your numbers', 'உங்கள் எண்கள்',
                      [('Number', 'எண்'), ('Value', 'மதிப்பு'), ('Ruling graha', 'அதிபதி கிரகம்'), ('Favourable day', 'உகந்த நாள்')],
                      rows)],
        birth_number=birth, destiny_number=destiny, name_number=name_info, lucky_numbers=lucky)
