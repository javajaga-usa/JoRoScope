"""Numerology in the Chaldean (Cheiro) system used in India: the birth (psychic) number from the day,
the destiny number from the whole date, and the name number from the letters of the English
spelling. Each number 1-9 has a ruling graha (1 Sun, 2 Moon, 3 Jupiter, 4 Rahu, 5 Mercury,
6 Venus, 7 Ketu, 8 Saturn, 9 Mars); numbers agree when their grahas are natural friends, with Rahu
read as Saturn and Ketu as Mars, as Indian numerologists do.
"""
from .common import PLANET_ML, PLANET_TAMIL
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
NUMBER_DAYS_ML = {1: 'ഞായർ', 2: 'തിങ്കൾ', 3: 'വ്യാഴം', 4: 'ശനി', 5: 'ബുധൻ', 6: 'വെള്ളി', 7: 'തിങ്കൾ', 8: 'ശനി', 9: 'ചൊവ്വ'}
NUMBER_READINGS_ML = {
    1: 'നേതൃത്വവും സ്വാതന്ത്ര്യവും: ലക്ഷ്യബോധവും മൗലികതയും ആത്മവിശ്വാസവും ഉള്ളവർ; സ്വന്തം ജോലി സ്വയം നടത്തുന്നതിൽ സന്തോഷിക്കും. അഹങ്കാരവും അക്ഷമയും ഒഴിവാക്കുക.',
    2: 'സൗമ്യതയും സഹകരണവും: കനിവും ഭാവനയും സഹകരണമനോഭാവവും ഉള്ളവർ; നയതന്ത്രത്തിലും കലകളിലും കഴിവ്. മനോഭാവം മാറാം; ക്രമമായ ദിനചര്യ സഹായിക്കും.',
    3: 'ജ്ഞാനവും വളർച്ചയും: ശുഭാപ്തിവിശ്വാസവും അച്ചടക്കവും പഠനതാൽപ്പര്യവും ഉള്ളവർ; അധ്യാപകനായോ ഉപദേശകനായോ ആദരിക്കപ്പെടും. പിടിവാശി ഒഴിവാക്കുക.',
    4: 'വേറിട്ട ഊർജ്ജം: പ്രായോഗികബുദ്ധിയും അധ്വാനശീലവും പുതുമയും ഉള്ളവർ; പലപ്പോഴും പതിവിന് വിരുദ്ധമായി നീങ്ങും. പെട്ടെന്നുള്ള മാറ്റങ്ങൾ വരും; ധനം ശ്രദ്ധയോടെ ആസൂത്രണം ചെയ്യുക.',
    5: 'ബുദ്ധിയും വാണിജ്യവും: മൂർച്ചയുള്ള ബുദ്ധിയും ബഹുമുഖ കഴിവും സംസാരശേഷിയും ഉള്ളവർ; വ്യാപാരം, യാത്ര, പഠനം എന്നിവയിൽ മികവ്. അസ്വസ്ഥതയെ ശരിയായ ദിശയിലേക്ക് തിരിക്കുക.',
    6: 'ഐക്യവും സുഖവും: കലാതാൽപ്പര്യവും സ്നേഹവും സൗന്ദര്യം, വീട്, കുടുംബം എന്നിവയോട് അടുപ്പവും ഉള്ളവർ; സുഹൃത്തുക്കളെയും സൗകര്യങ്ങളെയും ആകർഷിക്കും. അമിതാസക്തി ഒഴിവാക്കുക.',
    7: 'ഉൾക്കാഴ്ചയും ആത്മീയതയും: ചിന്താശീലവും ഉൾക്കാഴ്ചയും തത്ത്വചിന്താതാൽപ്പര്യവും ഉള്ളവർ; ഗവേഷണം, യാത്ര, ആന്തരികജീവിതം എന്നിവയിൽ ആകർഷണം. പദ്ധതികൾ മറ്റുള്ളവരുമായി പങ്കുവെക്കുക.',
    8: 'സഹനവും ഉത്തരവാദിത്തവും: ഗൗരവവും സ്ഥിരോത്സാഹവും നീതിബോധവും ഉള്ളവർ; വിജയം വൈകി വന്നാലും നിലനിൽക്കും. ക്ഷമയും സേവനവും തടസ്സങ്ങൾ കുറയ്ക്കും.',
    9: 'ധൈര്യവും ആവേശവും: ഉന്മേഷവും വീര്യവും ഉദാരമനസ്സും ഉള്ളവർ; പ്രവർത്തനത്തിലും നേതൃത്വത്തിലും മികവ്. കോപവും തിടുക്കവും നിയന്ത്രിക്കുക.',
}
RELATION_WORDS_ML = {1: 'ഇണങ്ങുന്നവ', 0: 'നിഷ്പക്ഷം', -1: 'പൊരുത്തപ്പെടാത്തവ'}
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
    graha_ml = lambda n: PLANET_ML[NUMBER_GRAHA[n]]
    day_cell = lambda n: (*NUMBER_DAYS[n], NUMBER_DAYS_ML[n])

    cards = [
        card('🎂', f'Birth number {birth} ({graha(birth)})', f'பிறவி எண் {birth} ({graha_ta(birth)})',
             NUMBER_READINGS[birth][0], NUMBER_READINGS[birth][1],
             f'From the day of birth, {day}: how you think and act day to day.',
             f'பிறந்த தேதி {day}-இலிருந்து: அன்றாட எண்ணமும் செயலும்.',
             title_ml=f'ജന്മസംഖ്യ {birth} ({graha_ml(birth)})', body_ml=NUMBER_READINGS_ML[birth],
             sub_ml=f'ജനനതീയതി {day}-ൽ നിന്ന്: ദൈനംദിന ചിന്തയും പ്രവൃത്തിയും.'),
        card('🧭', f'Destiny number {destiny} ({graha(destiny)})', f'விதி எண் {destiny} ({graha_ta(destiny)})',
             NUMBER_READINGS[destiny][0], NUMBER_READINGS[destiny][1],
             'From the whole date of birth: the direction life takes.',
             'முழுப் பிறந்த தேதியிலிருந்து: வாழ்க்கை செல்லும் திசை.',
             title_ml=f'ഭാഗ്യസംഖ്യ {destiny} ({graha_ml(destiny)})', body_ml=NUMBER_READINGS_ML[destiny],
             sub_ml='മുഴുവൻ ജനനതീയതിയിൽ നിന്ന്: ജീവിതം നീങ്ങുന്ന ദിശ.'),
    ]
    rows = [(('Birth number', 'பிறவி எண்', 'ജന്മസംഖ്യ'), birth, (graha(birth), graha_ta(birth), graha_ml(birth)), day_cell(birth)),
            (('Destiny number', 'விதி எண்', 'ഭാഗ്യസംഖ്യ'), destiny, (graha(destiny), graha_ta(destiny), graha_ml(destiny)),
             day_cell(destiny))]
    name_info = None
    if named:
        total, number = named
        rows.append((('Name number', 'பெயர் எண்', 'നാമസംഖ്യ'), f'{number} ({total})', (graha(number), graha_ta(number), graha_ml(number)),
                     day_cell(number)))
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
        advice_ml = ('പേര് ജന്മസംഖ്യയെയും ഭാഗ്യസംഖ്യയെയും പിന്തുണയ്ക്കുന്നു.' if worst >= 0 else
                     f"ആകെത്തുക {', '.join(map(str, good_totals))} വരുന്ന അക്ഷരവിന്യാസം ജന്മ, ഭാഗ്യ സംഖ്യകളുമായി കൂടുതൽ ഇണങ്ങും.")
        cards.append(card(
            '✍️', f'Name number {number} ({graha(number)})', f'பெயர் எண் {number} ({graha_ta(number)})',
            f"{NUMBER_READINGS[number][0]} With the birth number it is {en_b}; with the destiny number it is {en_d}. {advice_en}",
            f"{NUMBER_READINGS[number][1]} பிறவி எண்ணுடன் {ta_b}; விதி எண்ணுடன் {ta_d}. {advice_ta}",
            f'"{name}" totals {total} in the Chaldean values.', f'"{name}" கல்தேய மதிப்புகளில் {total}.',
            verdict=RELATION_WORDS[worst][2], title_ml=f'നാമസംഖ്യ {number} ({graha_ml(number)})',
            body_ml=(f"{NUMBER_READINGS_ML[number]} ജന്മസംഖ്യയുമായി {RELATION_WORDS_ML[with_birth]}; "
                     f"ഭാഗ്യസംഖ്യയുമായി {RELATION_WORDS_ML[with_destiny]}. {advice_ml}"),
            sub_ml=f'"{name}" കാൽഡിയൻ മൂല്യങ്ങളിൽ {total}.'))
        name_info = dict(name=name, total=total, number=number, with_birth=with_birth, with_destiny=with_destiny,
                         harmonious_numbers=good_totals)
    else:
        cards.append(card('✍️', 'Name number', 'பெயர் எண்',
                          'Numerology reads the English spelling of the name; enter the name in English letters to see its number.',
                          'எண் கணிதம் பெயரின் ஆங்கில எழுத்துக்கூட்டலைப் படிக்கிறது; பெயர் எண்ணைக் காண ஆங்கில எழுத்துகளில் பெயரை உள்ளிடவும்.',
                          title_ml='നാമസംഖ്യ',
                          body_ml='സംഖ്യാശാസ്ത്രം പേരിന്റെ ഇംഗ്ലീഷ് അക്ഷരവിന്യാസമാണ് വായിക്കുന്നത്; നാമസംഖ്യ കാണാൻ ഇംഗ്ലീഷ് അക്ഷരങ്ങളിൽ പേര് നൽകുക.'))

    lucky = sorted({birth, destiny} | {n for n in range(1, 10) if relation(n, birth) > 0})
    return chapter(
        'numerology', 'Numerology', 'எண் கணிதம்',
        'Chaldean numerology as practised in India: each number is ruled by a graha, and numbers agree when their grahas are friends.',
        'இந்தியாவில் பின்பற்றப்படும் கல்தேய எண் கணிதம்: ஒவ்வொரு எண்ணுக்கும் ஒரு கிரகம் அதிபதி; அவற்றின் கிரகங்கள் நட்பானால் எண்கள் இணங்கும்.',
        cards=cards,
        tables=[table('Your numbers', 'உங்கள் எண்கள்',
                      [('Number', 'எண்', 'സംഖ്യ'), ('Value', 'மதிப்பு', 'മൂല്യം'), ('Ruling graha', 'அதிபதி கிரகம்', 'അധിപ ഗ്രഹം'),
                       ('Favourable day', 'உகந்த நாள்', 'അനുകൂല ദിവസം')],
                      rows, title_ml='നിങ്ങളുടെ സംഖ്യകൾ')],
        title_ml='സംഖ്യാശാസ്ത്രം',
        intro_ml=('ഇന്ത്യയിൽ പിന്തുടരുന്ന കാൽഡിയൻ സംഖ്യാശാസ്ത്രം: ഓരോ സംഖ്യയ്ക്കും ഒരു ഗ്രഹം അധിപനാണ്; അവയുടെ ഗ്രഹങ്ങൾ മിത്രങ്ങളെങ്കിൽ '
                  'സംഖ്യകൾ ഇണങ്ങും.'),
        birth_number=birth, destiny_number=destiny, name_number=name_info, lucky_numbers=lucky)
