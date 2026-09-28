"""JoRoScope Yogas
Planetary combinations read in the Rasi chart by the rules of Brihat Parashara Hora Shastra,
Phaladeepika and B.V. Raman's "Three Hundred Important Combinations": the Pancha Mahapurusha,
Chandra and Surya yogas, the 32 Nabhasa yogas, the Raja, Dhana and named yogas, Parivartana
(sign exchange) and the challenging combinations. Houses count whole signs from the Lagna.
The Surya, Chandra and Nabhasa yogas use the seven grahas only; Rahu and Ketu enter only the
yogas that name them.
"""
from .engine import SIGN_LORDS
from .readings.common import PLANET_TAMIL
from .shadbala import _benefics

SEVEN = ('Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn')
FIVE = ('Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn')  # the grahas that form Surya and Chandra yogas
TRIO = ('Mercury', 'Jupiter', 'Venus')                      # natural benefics of the Adhi-type yogas
KENDRA, TRIKONA, DUSTHANA, UPACHAYA = (1, 4, 7, 10), (1, 5, 9), (6, 8, 12), (3, 6, 10, 11)
DIGNIFIED = ('Exalted', 'Own Sign', 'Moolatrikona')
EXALTATION_SIGN = {'Sun': 0, 'Moon': 1, 'Mars': 9, 'Mercury': 5, 'Jupiter': 3, 'Venus': 11, 'Saturn': 6}

CATEGORIES = {
    'mahapurusha': ('Pancha Mahapurusha', 'பஞ்ச மகாபுருஷ யோகம்'),
    'chandra': ('Chandra Yoga', 'சந்திர யோகம்'),
    'surya': ('Surya Yoga', 'சூரிய யோகம்'),
    'raja': ('Raja Yoga', 'ராஜ யோகம்'),
    'dhana': ('Dhana Yoga', 'தன யோகம்'),
    'named': ('Named Yoga', 'சிறப்பு யோகம்'),
    'parivartana': ('Parivartana Yoga', 'பரிவர்த்தனை யோகம்'),
    'vipareeta': ('Vipareeta Raja Yoga', 'விபரீத ராஜ யோகம்'),
    'nabhasa': ('Nabhasa Yoga', 'நாபச யோகம்'),
    'challenge': ('Challenging Combination', 'சவாலான சேர்க்கை')
}
NATURES = {
    'good': ('Auspicious', 'சுபம்'),
    'mixed': ('Mixed', 'கலப்பு பலன்'),
    'bad': ('Challenging', 'சவாலானது'),
    'cancelled': ('Cancelled', 'நிவர்த்தி')
}

# key: (English name, Tamil name, category, nature, English reading, Tamil reading)
YOGAS = {
    'ruchaka': ('Ruchaka Yoga', 'ருசக யோகம்', 'mahapurusha', 'good',
                'Mars strong in a kendra: courage, leadership, victory over rivals and a commanding presence.',
                'கேந்திரத்தில் பலமான செவ்வாய்: வீரம், தலைமைப் பண்பு, எதிரிகளை வெல்லுதல், கம்பீரமான தோற்றம்.'),
    'bhadra': ('Bhadra Yoga', 'பத்ர யோகம்', 'mahapurusha', 'good',
               'Mercury strong in a kendra: a sharp intellect, eloquence, learning and success in trade.',
               'கேந்திரத்தில் பலமான புதன்: கூர்மையான அறிவு, பேச்சுத் திறன், கல்வி, வணிக வெற்றி.'),
    'hamsa': ('Hamsa Yoga', 'ஹம்ச யோகம்', 'mahapurusha', 'good',
              'Jupiter strong in a kendra: wisdom, righteousness, respect and a spiritual nature.',
              'கேந்திரத்தில் பலமான குரு: ஞானம், அறநெறி, மதிப்பு, ஆன்மீக இயல்பு.'),
    'malavya': ('Malavya Yoga', 'மாளவ்ய யோகம்', 'mahapurusha', 'good',
                'Venus strong in a kendra: beauty, artistic taste, comforts, vehicles and a happy married life.',
                'கேந்திரத்தில் பலமான சுக்கிரன்: அழகு, கலை ரசனை, சுக வசதிகள், வாகனம், மகிழ்ச்சியான இல்லறம்.'),
    'sasa': ('Sasa Yoga', 'சச யோகம்', 'mahapurusha', 'good',
             'Saturn strong in a kendra: authority over many, discipline and wealth built through perseverance.',
             'கேந்திரத்தில் பலமான சனி: பலரை நிர்வகிக்கும் அதிகாரம், ஒழுக்கம், விடாமுயற்சியால் செல்வம்.'),

    'sunapha': ('Sunapha Yoga', 'சுனபா யோகம்', 'chandra', 'good',
                'Grahas in the 2nd from the Moon: self-earned wealth, a good name and a sharp mind.',
                'சந்திரனுக்கு 2-இல் கிரகங்கள்: சுயமாக ஈட்டிய செல்வம், நற்பெயர், கூர்மையான புத்தி.'),
    'anapha': ('Anapha Yoga', 'அனபா யோகம்', 'chandra', 'good',
               'Grahas in the 12th from the Moon: a healthy, well-mannered person of good repute and comforts.',
               'சந்திரனுக்கு 12-இல் கிரகங்கள்: நல்ல உடல்நலம், நன்னடத்தை, புகழ், சுக வசதிகள்.'),
    'durudhara': ('Durudhara Yoga', 'துருதுரா யோகம்', 'chandra', 'good',
                  'Grahas on both sides of the Moon: wealth, vehicles, generosity and many comforts.',
                  'சந்திரனின் இரு பக்கங்களிலும் கிரகங்கள்: செல்வம், வாகனம், தாராள மனம், பல சுகங்கள்.'),
    'kemadruma': ('Kemadruma Yoga', 'கேமத்ரும யோகம்', 'chandra', 'bad',
                  'No graha beside the Moon and none in the kendras: periods of loneliness and financial strain that need steady effort.',
                  'சந்திரனின் இருபுறமும் கேந்திரங்களிலும் கிரகம் இல்லை: தனிமையும் பொருளாதார நெருக்கடியும் வரும் காலங்கள்; நிலையான முயற்சி தேவை.'),
    'kemadruma_bhanga': ('Kemadruma Bhanga', 'கேமத்ரும பங்கம்', 'chandra', 'cancelled',
                         'The Moon has no graha beside it, but grahas in the kendras or with the Moon cancel Kemadruma.',
                         'சந்திரனின் இருபுறமும் கிரகம் இல்லை; ஆனால் கேந்திரங்களிலோ சந்திரனுடனோ உள்ள கிரகங்கள் கேமத்ருமத்தை நீக்குகின்றன.'),
    'adhi': ('Adhi Yoga', 'அதி யோகம்', 'chandra', 'good',
             'Mercury, Jupiter and Venus in the 6th, 7th and 8th from the Moon: leadership, trust, health and long life.',
             'சந்திரனுக்கு 6, 7, 8-இல் புதன், குரு, சுக்கிரன்: தலைமைப் பதவி, நம்பகத்தன்மை, உடல்நலம், நீண்ட ஆயுள்.'),
    'lagnadhi': ('Lagnadhi Yoga', 'லக்னாதி யோகம்', 'named', 'good',
                 'Mercury, Jupiter and Venus in the 6th, 7th and 8th from the Lagna: a learned, happy and respected life.',
                 'லக்னத்திற்கு 6, 7, 8-இல் புதன், குரு, சுக்கிரன்: கல்வி, மகிழ்ச்சி, மதிப்பு நிறைந்த வாழ்க்கை.'),
    'gaja_kesari': ('Gaja Kesari Yoga', 'கஜகேசரி யோகம்', 'chandra', 'good',
                    'Jupiter in a kendra from the Moon: victory over rivals, lasting respect, wealth and nobility.',
                    'சந்திரனுக்குக் கேந்திரத்தில் குரு: எதிரிகளை வெல்லுதல், நிலைத்த மதிப்பு, செல்வம், பெருந்தன்மை.'),
    'chandra_mangala': ('Chandra-Mangala Yoga', 'சந்திர மங்கள யோகம்', 'dhana', 'good',
                        'The Moon with or opposite Mars: enterprise and earnings through business and initiative.',
                        'சந்திரனுடன் அல்லது எதிரில் செவ்வாய்: தொழில் முனைவு, வணிகம் மற்றும் முயற்சியால் வருமானம்.'),
    'sakata': ('Sakata Yoga', 'சகட யோகம்', 'chandra', 'bad',
               'Jupiter in the 6th, 8th or 12th from the Moon: fortune rises and falls like a cart wheel; patience steadies it.',
               'சந்திரனுக்கு 6, 8, 12-இல் குரு: வண்டிச் சக்கரம் போல் ஏற்ற இறக்கமான அதிர்ஷ்டம்; பொறுமை நிலைப்படுத்தும்.'),
    'vasumati': ('Vasumati Yoga', 'வசுமதி யோகம்', 'dhana', 'good',
                 'Mercury, Jupiter and Venus in the upachayas (3, 6, 10, 11): steadily growing wealth and independence.',
                 'உபசய ஸ்தானங்களில் (3, 6, 10, 11) புதன், குரு, சுக்கிரன்: படிப்படியாக வளரும் செல்வமும் சுதந்திரமும்.'),

    'vesi': ('Vesi Yoga', 'வேசி யோகம்', 'surya', 'good',
             'Grahas in the 2nd from the Sun: truthful, balanced and fortunate.',
             'சூரியனுக்கு 2-இல் கிரகங்கள்: வாய்மை, சமநிலை, அதிர்ஷ்டம்.'),
    'vasi': ('Vasi Yoga', 'வாசி யோகம்', 'surya', 'good',
             'Grahas in the 12th from the Sun: skilful, charitable and well regarded.',
             'சூரியனுக்கு 12-இல் கிரகங்கள்: திறமை, தான குணம், நல்ல மதிப்பு.'),
    'ubhayachari': ('Ubhayachari Yoga', 'உபயசரி யோகம்', 'surya', 'good',
                    'Grahas on both sides of the Sun: eloquent, prosperous and respected like a king.',
                    'சூரியனின் இரு பக்கங்களிலும் கிரகங்கள்: பேச்சுத் திறன், செல்வம், அரசனைப் போன்ற மதிப்பு.'),
    'budhaditya': ('Budhaditya Yoga', 'புதாதித்ய யோகம்', 'surya', 'good',
                   'The Sun with Mercury: intelligence, skill in work and a good reputation.',
                   'சூரியனுடன் புதன்: அறிவாற்றல், தொழில் திறமை, நற்பெயர்.'),

    'raja': ('Raja Yoga', 'ராஜ யோகம்', 'raja', 'good',
             'A kendra lord joined with a trikona lord: power, status and success in what one undertakes.',
             'கேந்திர அதிபதியும் திரிகோண அதிபதியும் இணைவு: அதிகாரம், அந்தஸ்து, காரிய வெற்றி.'),
    'yogakaraka': ('Yogakaraka Graha', 'யோககாரக கிரகம்', 'raja', 'good',
                   'One graha rules both a kendra and a trikona: its periods bring rise and recognition.',
                   'ஒரே கிரகம் கேந்திரத்திற்கும் திரிகோணத்திற்கும் அதிபதி: அதன் தசையில் உயர்வும் அங்கீகாரமும்.'),
    'dharma_karmadhipati': ('Dharma-Karmadhipati Yoga', 'தர்ம கர்மாதிபதி யோகம்', 'raja', 'good',
                            'The lords of the 9th and 10th joined: fortune and career support each other; a life of purposeful work.',
                            '9, 10-ஆம் அதிபதிகள் இணைவு: பாக்கியமும் தொழிலும் ஒன்றையொன்று உயர்த்தும்; நோக்கமுள்ள உழைப்பு நிறைந்த வாழ்க்கை.'),
    'dhana': ('Dhana Yoga', 'தன யோகம்', 'dhana', 'good',
              'A lord of wealth (2nd or 11th) joined with the lord of the Lagna, 5th or 9th: earnings and savings grow.',
              'தன அதிபதி (2 அல்லது 11) லக்ன, 5, 9-ஆம் அதிபதியுடன் இணைவு: வருமானமும் சேமிப்பும் பெருகும்.'),
    'lakshmi': ('Lakshmi Yoga', 'லட்சுமி யோகம்', 'named', 'good',
                'A strong 9th lord in a kendra or trikona with a well-placed Lagna lord: wealth, grace and a noble life.',
                'கேந்திர/திரிகோணத்தில் பலமான 9-ஆம் அதிபதியும் வலுவான லக்னாதிபதியும்: செல்வம், அருள், உயர்ந்த வாழ்க்கை.'),
    'saraswati': ('Saraswati Yoga', 'சரஸ்வதி யோகம்', 'named', 'good',
                  'Mercury, Jupiter and Venus in kendras, trikonas or the 2nd, with Jupiter well placed: learning, eloquence and fame in the arts.',
                  'கேந்திர, திரிகோண அல்லது 2-இல் புதன், குரு, சுக்கிரன், குரு நல்ல நிலையில்: கல்வி, வாக்கு வன்மை, கலைகளில் புகழ்.'),
    'parvata': ('Parvata Yoga', 'பர்வத யோகம்', 'named', 'good',
                'Benefics in the kendras with the 6th and 8th free of malefics: prosperity, fame and generosity.',
                'கேந்திரங்களில் சுப கிரகங்கள், 6, 8-இல் பாப கிரகம் இல்லை: செல்வம், புகழ், தாராள மனம்.'),
    'kahala': ('Kahala Yoga', 'காஹல யோகம்', 'named', 'good',
               'The lords of the 4th and 9th in mutual kendras with a strong Lagna lord: boldness, authority and command.',
               'ஒன்றுக்கொன்று கேந்திரத்தில் 4, 9-ஆம் அதிபதிகள், பலமான லக்னாதிபதி: துணிச்சல், அதிகாரம், தலைமை.'),
    'chamara': ('Chamara Yoga', 'சாமர யோகம்', 'named', 'good',
                'An exalted Lagna lord in a kendra under Jupiter\'s aspect, or two benefics together in the 1st, 7th, 9th or 10th: honour, learning and long life.',
                'குருவின் பார்வையுடன் கேந்திரத்தில் உச்ச லக்னாதிபதி, அல்லது 1, 7, 9, 10-இல் இரு சுபர்கள்: கௌரவம், கல்வி, நீண்ட ஆயுள்.'),
    'sankha': ('Sankha Yoga', 'சங்க யோகம்', 'named', 'good',
               'The lords of the 5th and 6th in mutual kendras with a strong Lagna lord: a humane, cultured and prosperous life.',
               'ஒன்றுக்கொன்று கேந்திரத்தில் 5, 6-ஆம் அதிபதிகள், பலமான லக்னாதிபதி: மனிதநேயம், பண்பாடு, செல்வம்.'),
    'bheri': ('Bheri Yoga', 'பேரி யோகம்', 'named', 'good',
              'Venus, Jupiter and the Lagna lord in kendras with a strong 9th lord: a long, healthy and prosperous life.',
              'கேந்திரங்களில் சுக்கிரன், குரு, லக்னாதிபதி, பலமான 9-ஆம் அதிபதி: நீண்ட, ஆரோக்கியமான, செல்வ வாழ்க்கை.'),
    'guru_mangala': ('Guru-Mangala Yoga', 'குரு மங்கள யோகம்', 'named', 'good',
                     'Jupiter with or opposite Mars: principled courage, energy for good causes and property.',
                     'குருவுடன் அல்லது எதிரில் செவ்வாய்: நேர்மையான துணிச்சல், நற்காரியங்களுக்கான ஆற்றல், சொத்து.'),
    'amala': ('Amala Yoga', 'அமல யோகம்', 'named', 'good',
              'A natural benefic in the 10th from the Lagna or the Moon: a spotless reputation and lasting fame.',
              'லக்னத்திற்கோ சந்திரனுக்கோ 10-இல் சுப கிரகம்: களங்கமற்ற புகழும் நிலைத்த பெயரும்.'),
    'shubha_kartari': ('Shubha Kartari Yoga', 'சுப கர்த்தரி யோகம்', 'named', 'good',
                       'Benefics on both sides of the Lagna: protection, health and a comfortable life.',
                       'லக்னத்தின் இருபுறமும் சுப கிரகங்கள்: பாதுகாப்பு, உடல்நலம், சுகமான வாழ்க்கை.'),
    'papa_kartari': ('Papa Kartari Yoga', 'பாப கர்த்தரி யோகம்', 'challenge', 'bad',
                     'Malefics on both sides of the Lagna: the self feels hemmed in; health and confidence need care.',
                     'லக்னத்தின் இருபுறமும் பாப கிரகங்கள்: நெருக்கடியான சூழல்; உடல்நலத்திலும் தன்னம்பிக்கையிலும் கவனம் தேவை.'),
    'maha_parivartana': ('Maha Parivartana Yoga', 'மகா பரிவர்த்தனை யோகம்', 'parivartana', 'good',
                         'Two good-house lords exchange signs: both houses gain strength; wealth and status follow.',
                         'இரு நல்ல பாவ அதிபதிகள் ராசி மாற்றம்: இரு பாவங்களும் வலுப்பெறும்; செல்வமும் அந்தஸ்தும் கிட்டும்.'),
    'khala_parivartana': ('Khala Parivartana Yoga', 'கல பரிவர்த்தனை யோகம்', 'parivartana', 'mixed',
                          'The 3rd lord exchanges signs with another lord: success comes through bold effort, with ups and downs.',
                          '3-ஆம் அதிபதியுடன் ராசி மாற்றம்: துணிச்சலான முயற்சியால் வெற்றி, ஏற்ற இறக்கங்களுடன்.'),
    'dainya_parivartana': ('Dainya Parivartana Yoga', 'தைன்ய பரிவர்த்தனை யோகம்', 'parivartana', 'mixed',
                           'A dusthana lord (6th, 8th or 12th) exchanges signs with another lord: struggles that turn into strength over time.',
                           'மறைவு ஸ்தான அதிபதியுடன் (6, 8, 12) ராசி மாற்றம்: போராட்டங்கள் காலப்போக்கில் பலமாக மாறும்.'),
    'harsha': ('Harsha Vipareeta Raja Yoga', 'ஹர்ஷ விபரீத ராஜ யோகம்', 'vipareeta', 'good',
               'The 6th lord in a dusthana: protection from enemies, good health and victory in hardship.',
               '6-ஆம் அதிபதி மறைவு ஸ்தானத்தில்: எதிரிகளிடமிருந்து பாதுகாப்பு, நல்ல உடல்நலம், துன்பத்தில் வெற்றி.'),
    'sarala': ('Sarala Vipareeta Raja Yoga', 'சரள விபரீத ராஜ யோகம்', 'vipareeta', 'good',
               'The 8th lord in a dusthana: long life, fearlessness and sudden gains.',
               '8-ஆம் அதிபதி மறைவு ஸ்தானத்தில்: நீண்ட ஆயுள், அச்சமின்மை, திடீர் லாபம்.'),
    'vimala': ('Vimala Vipareeta Raja Yoga', 'விமல விபரீத ராஜ யோகம்', 'vipareeta', 'good',
               'The 12th lord in a dusthana: thrift, independence and peace of mind.',
               '12-ஆம் அதிபதி மறைவு ஸ்தானத்தில்: சிக்கனம், சுதந்திரம், மன அமைதி.'),
    'neechabhanga': ('Neechabhanga Raja Yoga', 'நீசபங்க ராஜ யோகம்', 'raja', 'good',
                     'A debilitated graha has its debilitation cancelled: early setbacks turn into a rise.',
                     'நீசமான கிரகத்தின் நீசம் பங்கமடைகிறது: ஆரம்பத் தடைகள் உயர்வாக மாறும்.'),

    'guru_chandala': ('Guru Chandala Yoga', 'குரு சண்டாள யோகம்', 'challenge', 'bad',
                      'Jupiter with Rahu: unconventional beliefs; guard against poor advice and shortcuts.',
                      'குருவுடன் ராகு: வழக்கத்திற்கு மாறான நம்பிக்கைகள்; தவறான ஆலோசனைகளையும் குறுக்குவழிகளையும் தவிர்க்கவும்.'),
    'grahana': ('Grahana Yoga', 'கிரகண யோகம்', 'challenge', 'bad',
                'The Sun or Moon with Rahu or Ketu: an eclipsed luminary; confidence or peace of mind needs nurturing.',
                'சூரியன் அல்லது சந்திரனுடன் ராகு/கேது: கிரகணமான ஒளிக்கிரகம்; தன்னம்பிக்கை அல்லது மன அமைதியைப் பேண வேண்டும்.'),
    'angaraka': ('Angaraka Yoga', 'அங்காரக யோகம்', 'challenge', 'bad',
                 'Mars with Rahu or Ketu: intense energy and a quick temper; channel it into disciplined work.',
                 'செவ்வாயுடன் ராகு/கேது: தீவிர ஆற்றல், முன்கோபம்; ஒழுக்கமான உழைப்பில் செலுத்த வேண்டும்.'),
    'punarphoo': ('Punarphoo Dosham (Saturn-Moon)', 'புனர்பூ தோஷம் (சனி-சந்திரன்)', 'challenge', 'bad',
                  'Saturn with the Moon: a serious, cautious mind; delays in marriage talks are common, as Tamil tradition notes.',
                  'சனியுடன் சந்திரன்: கவனமான, கனமான மனம்; திருமணப் பேச்சுகளில் தாமதம் ஏற்படலாம் என தமிழ் மரபு கூறுகிறது.'),
    'daridra': ('Daridra Yoga', 'தரித்திர யோகம்', 'challenge', 'bad',
                'The 11th lord in the 6th, 8th or 12th: income meets obstacles; careful saving protects wealth.',
                '11-ஆம் அதிபதி 6, 8, 12-இல்: வருமானத்தில் தடைகள்; கவனமான சேமிப்பு செல்வத்தைக் காக்கும்.'),

    # Nabhasa yogas (BPHS ch. 35): the pattern the seven grahas make
    'rajju': ('Rajju Yoga', 'ரஜ்ஜு யோகம்', 'nabhasa', 'mixed',
              'All grahas in movable signs: fond of travel, and fortune found away from home.',
              'எல்லா கிரகங்களும் சர ராசிகளில்: பயண விருப்பம்; வெளியூரில் அதிர்ஷ்டம்.'),
    'musala': ('Musala Yoga', 'முசல யோகம்', 'nabhasa', 'good',
               'All grahas in fixed signs: steady, proud, learned and wealthy.',
               'எல்லா கிரகங்களும் ஸ்திர ராசிகளில்: உறுதி, கௌரவம், கல்வி, செல்வம்.'),
    'nala': ('Nala Yoga', 'நள யோகம்', 'nabhasa', 'mixed',
             'All grahas in dual signs: clever and resourceful, with a hand in many fields.',
             'எல்லா கிரகங்களும் உபய ராசிகளில்: சாமர்த்தியம், பல துறைகளில் திறமை.'),
    'mala': ('Mala Yoga', 'மாலா யோகம்', 'nabhasa', 'good',
             'Benefics in three kendras: comforts, vehicles, wealth and enjoyment.',
             'மூன்று கேந்திரங்களில் சுப கிரகங்கள்: சுகம், வாகனம், செல்வம், இன்பம்.'),
    'sarpa': ('Sarpa Yoga', 'சர்ப்ப யோகம்', 'nabhasa', 'bad',
              'Malefics in three kendras: hardships and dependence on others; resilience wins over time.',
              'மூன்று கேந்திரங்களில் பாப கிரகங்கள்: சிரமங்கள், பிறரைச் சார்ந்திருத்தல்; மன உறுதி காலப்போக்கில் வெல்லும்.'),
    'gada': ('Gada Yoga', 'கதா யோகம்', 'nabhasa', 'good',
             'All grahas in two successive kendras: wealth, learning and devotion.',
             'அடுத்தடுத்த இரு கேந்திரங்களில் எல்லா கிரகங்களும்: செல்வம், கல்வி, பக்தி.'),
    'sakata_nabhasa': ('Sakata Yoga (Nabhasa)', 'சகட யோகம் (நாபசம்)', 'nabhasa', 'mixed',
                       'All grahas in the 1st and 7th: livelihood through vehicles or transport, with changing fortunes.',
                       '1, 7-இல் எல்லா கிரகங்களும்: வாகனம் அல்லது போக்குவரத்து வழியே ஜீவனம்; மாறும் அதிர்ஷ்டம்.'),
    'vihaga': ('Vihaga Yoga', 'விஹக யோகம்', 'nabhasa', 'mixed',
               'All grahas in the 4th and 10th: a life of travel and communication, often as a go-between.',
               '4, 10-இல் எல்லா கிரகங்களும்: பயணமும் தகவல் தொடர்பும் நிறைந்த வாழ்க்கை.'),
    'sringataka': ('Sringataka Yoga', 'சிருங்காடக யோகம்', 'nabhasa', 'good',
                   'All grahas in the trines 1, 5 and 9: fortunate, especially later in life.',
                   '1, 5, 9 திரிகோணங்களில் எல்லா கிரகங்களும்: அதிர்ஷ்டம், குறிப்பாகப் பிற்கால வாழ்க்கையில்.'),
    'hala': ('Hala Yoga', 'ஹல யோகம்', 'nabhasa', 'mixed',
             'All grahas in trines other than the Lagna\'s: hard-working, with a livelihood from land or farming.',
             'லக்னம் அல்லாத திரிகோணங்களில் எல்லா கிரகங்களும்: கடின உழைப்பு, நிலம் அல்லது விவசாயம் வழி ஜீவனம்.'),
    'vajra': ('Vajra Yoga', 'வஜ்ர யோகம்', 'nabhasa', 'good',
              'Benefics in the 1st and 7th, malefics in the 4th and 10th: happy in youth and old age.',
              '1, 7-இல் சுபர், 4, 10-இல் பாபர்: இளமையிலும் முதுமையிலும் மகிழ்ச்சி.'),
    'yava': ('Yava Yoga', 'யவ யோகம்', 'nabhasa', 'good',
             'Malefics in the 1st and 7th, benefics in the 4th and 10th: happiest in middle life; charitable.',
             '1, 7-இல் பாபர், 4, 10-இல் சுபர்: நடுத்தர வயதில் மிகுந்த மகிழ்ச்சி; தான குணம்.'),
    'kamala': ('Kamala Yoga', 'கமல யோகம்', 'nabhasa', 'good',
               'All grahas in the four kendras: fame, virtue and long life.',
               'நான்கு கேந்திரங்களில் எல்லா கிரகங்களும்: புகழ், அறநெறி, நீண்ட ஆயுள்.'),
    'vapi': ('Vapi Yoga', 'வாபி யோகம்', 'nabhasa', 'good',
             'All grahas outside the kendras: wealth quietly accumulated and enjoyed.',
             'கேந்திரங்களுக்கு வெளியே எல்லா கிரகங்களும்: அமைதியாகச் சேர்த்து அனுபவிக்கும் செல்வம்.'),
    'yupa': ('Yupa Yoga', 'யூப யோகம்', 'nabhasa', 'good',
             'All grahas in the 1st to 4th: generous, devout and self-controlled.',
             '1 முதல் 4 வரை எல்லா கிரகங்களும்: தாராள மனம், பக்தி, சுயக்கட்டுப்பாடு.'),
    'ishu': ('Ishu Yoga', 'இஷு யோகம்', 'nabhasa', 'mixed',
             'All grahas in the 4th to 7th: bold and skilled with tools or weapons.',
             '4 முதல் 7 வரை எல்லா கிரகங்களும்: துணிச்சல், கருவிகளில் திறமை.'),
    'shakti': ('Shakti Yoga', 'சக்தி யோகம்', 'nabhasa', 'mixed',
               'All grahas in the 7th to 10th: early struggles, then success through persistence.',
               '7 முதல் 10 வரை எல்லா கிரகங்களும்: ஆரம்பப் போராட்டம், பின் விடாமுயற்சியால் வெற்றி.'),
    'danda': ('Danda Yoga', 'தண்ட யோகம்', 'nabhasa', 'mixed',
              'All grahas in the 10th to the 1st: a life of service; distance from loved ones at times.',
              '10 முதல் 1 வரை எல்லா கிரகங்களும்: சேவை வாழ்க்கை; சில நேரம் அன்புக்குரியவர்களிடமிருந்து பிரிவு.'),
    'nauka': ('Nauka Yoga', 'நௌகா யோகம்', 'nabhasa', 'mixed',
              'The grahas fill the seven houses from the Lagna: fame and earnings through water, travel or trade.',
              'லக்னம் முதல் ஏழு பாவங்களிலும் கிரகங்கள்: நீர், பயணம் அல்லது வணிகம் வழியே புகழும் வருமானமும்.'),
    'koota': ('Koota Yoga', 'கூட யோகம்', 'nabhasa', 'mixed',
              'The grahas fill the seven houses from the 4th: work in remote places, forts or guarded settings.',
              '4 முதல் ஏழு பாவங்களிலும் கிரகங்கள்: தொலைதூர அல்லது பாதுகாப்பான இடங்களில் பணி.'),
    'chatra': ('Chatra Yoga', 'சத்ர யோகம்', 'nabhasa', 'good',
               'The grahas fill the seven houses from the 7th: helpful to family, happy and long-lived.',
               '7 முதல் ஏழு பாவங்களிலும் கிரகங்கள்: குடும்பத்திற்கு உதவி, மகிழ்ச்சி, நீண்ட ஆயுள்.'),
    'chapa': ('Chapa Yoga', 'சாப யோகம்', 'nabhasa', 'mixed',
              'The grahas fill the seven houses from the 10th: brave, happiest in the first and last parts of life.',
              '10 முதல் ஏழு பாவங்களிலும் கிரகங்கள்: துணிச்சல்; வாழ்வின் தொடக்கத்திலும் இறுதியிலும் மகிழ்ச்சி.'),
    'ardha_chandra': ('Ardha Chandra Yoga', 'அர்த்த சந்திர யோகம்', 'nabhasa', 'good',
                      'The grahas fill seven houses starting away from a kendra: handsome, honoured and a leader of others.',
                      'கேந்திரமல்லாத பாவம் முதல் ஏழு பாவங்களிலும் கிரகங்கள்: அழகு, கௌரவம், தலைமைப் பொறுப்பு.'),
    'chakra': ('Chakra Yoga', 'சக்ர யோகம்', 'nabhasa', 'good',
               'The grahas occupy the six odd houses from the Lagna: prestige and authority like a ruler.',
               'லக்னம் முதல் ஒற்றைப்படை ஆறு பாவங்களிலும் கிரகங்கள்: அரசனைப் போன்ற மதிப்பும் அதிகாரமும்.'),
    'samudra': ('Samudra Yoga', 'சமுத்திர யோகம்', 'nabhasa', 'good',
                'The grahas occupy the six even houses from the 2nd: wealth and enjoyments like a king.',
                '2 முதல் இரட்டைப்படை ஆறு பாவங்களிலும் கிரகங்கள்: அரசனைப் போன்ற செல்வமும் இன்பமும்.'),
    'vallaki': ('Vallaki (Veena) Yoga', 'வல்லகி (வீணை) யோகம்', 'nabhasa', 'good',
                'The grahas spread over seven signs: fond of music and the arts, with many friends.',
                'ஏழு ராசிகளில் கிரகங்கள்: இசை, கலைகளில் ஆர்வம், பல நண்பர்கள்.'),
    'dama': ('Dama Yoga', 'தாம யோகம்', 'nabhasa', 'good',
             'The grahas spread over six signs: generous, helpful and well off.',
             'ஆறு ராசிகளில் கிரகங்கள்: தாராள மனம், உதவும் குணம், வசதி.'),
    'pasa': ('Pasa Yoga', 'பாச யோகம்', 'nabhasa', 'mixed',
             'The grahas spread over five signs: good earnings, many dependants and ties of duty.',
             'ஐந்து ராசிகளில் கிரகங்கள்: நல்ல வருமானம், பல பொறுப்புகள், கடமைப் பிணைப்புகள்.'),
    'kedara': ('Kedara Yoga', 'கேதார யோகம்', 'nabhasa', 'good',
               'The grahas spread over four signs: useful to many, truthful, often linked with land or farming.',
               'நான்கு ராசிகளில் கிரகங்கள்: பலருக்குப் பயன், வாய்மை; நிலம் அல்லது விவசாயத் தொடர்பு.'),
    'shula': ('Shula Yoga', 'சூல யோகம்', 'nabhasa', 'mixed',
              'The grahas spread over three signs: sharp and courageous, but prone to conflict.',
              'மூன்று ராசிகளில் கிரகங்கள்: கூர்மை, துணிச்சல், ஆனால் மோதல்களுக்கு வாய்ப்பு.'),
    'yuga': ('Yuga Yoga', 'யுக யோகம்', 'nabhasa', 'mixed',
             'The grahas in only two signs: an unconventional path with financial ups and downs.',
             'இரண்டு ராசிகளில் மட்டும் கிரகங்கள்: வழக்கத்திற்கு மாறான பாதை; பொருளாதார ஏற்ற இறக்கங்கள்.'),
    'gola': ('Gola Yoga', 'கோள யோகம்', 'nabhasa', 'mixed',
             'All grahas in one sign: an intensely focused life that must build stability through effort.',
             'ஒரே ராசியில் எல்லா கிரகங்களும்: ஒருமுகப்பட்ட வாழ்க்கை; முயற்சியால் நிலைத்தன்மை பெற வேண்டும்.')
}
SANKHYA = {7: 'vallaki', 6: 'dama', 5: 'pasa', 4: 'kedara', 3: 'shula', 2: 'yuga', 1: 'gola'}


class Chart:
    """Sign and house arithmetic over the engine's planet dicts."""

    def __init__(self, planets):
        self.p = planets
        self.asc = planets['Ascendant']['sign_index']
        lon = {g: planets[g]['longitude'] for g in SEVEN}
        signs = {g: planets[g]['sign_index'] for g in SEVEN}
        self.benefics = _benefics(lon, signs, (lon['Moon'] - lon['Sun']) % 360 < 180)
        self.malefics = set(SEVEN) - self.benefics

    def sign(self, g):
        return self.p[g]['sign_index']

    def house(self, g):
        return (self.sign(g) - self.asc) % 12 + 1

    def from_(self, ref, g):
        """Position of g counted from graha ref (1 = same sign)."""
        return (self.sign(g) - self.sign(ref)) % 12 + 1

    def lord(self, house):
        return SIGN_LORDS[(self.asc + house - 1) % 12]

    def in_house(self, house, pool=SEVEN):
        return [g for g in pool if self.house(g) == house]

    def dignified(self, g):
        return self.p[g].get('dignity') in DIGNIFIED

    def aspects(self, g, target_sign):
        d = (target_sign - self.sign(g)) % 12 + 1
        return d == 7 or (g == 'Mars' and d in (4, 8)) or (g == 'Jupiter' and d in (5, 9)) or (g == 'Saturn' and d in (3, 10))

    def associated(self, a, b):
        """Conjunction, sign exchange or mutual aspect of two grahas."""
        exchange = SIGN_LORDS[self.sign(a)] == b and SIGN_LORDS[self.sign(b)] == a
        return self.sign(a) == self.sign(b) or exchange or (self.aspects(a, self.sign(b)) and self.aspects(b, self.sign(a)))


def _found(key, planets, note_en='', note_ta=''):
    en, ta, category, nature, desc_en, desc_ta = YOGAS[key]
    cat_en, cat_ta = CATEGORIES[category]
    nat_en, nat_ta = NATURES[nature]
    suffix_en = f" ({', '.join(planets)})" if key in ('raja', 'dhana', 'yogakaraka', 'neechabhanga', 'maha_parivartana',
                                                    'khala_parivartana', 'dainya_parivartana', 'dharma_karmadhipati') else ''
    suffix_ta = f" ({', '.join(PLANET_TAMIL[g] for g in planets)})" if suffix_en else ''
    return dict(key=key, name=en + suffix_en, name_ta=ta + suffix_ta, category=cat_en, category_ta=cat_ta,
                auspiciousness=nat_en, auspiciousness_ta=nat_ta, nature=nature,
                description=desc_en + (f' {note_en}' if note_en else ''),
                description_ta=desc_ta + (f' {note_ta}' if note_ta else ''), planets=list(planets))


def detect(planets):
    """Every yoga present in the chart, auspicious ones first."""
    c = Chart(planets)
    found = []
    add = lambda key, grahas, note_en='', note_ta='': found.append(_found(key, grahas, note_en, note_ta))

    # --- Pancha Mahapurusha: Mars to Saturn in own, exaltation or moolatrikona sign in a kendra ---
    for g, key in (('Mars', 'ruchaka'), ('Mercury', 'bhadra'), ('Jupiter', 'hamsa'), ('Venus', 'malavya'), ('Saturn', 'sasa')):
        if c.house(g) in KENDRA and c.dignified(g):
            add(key, [g])

    # --- Chandra yogas ---
    second = [g for g in FIVE if c.from_('Moon', g) == 2]
    twelfth = [g for g in FIVE if c.from_('Moon', g) == 12]
    if second and twelfth:
        add('durudhara', ['Moon'] + second + twelfth)
    elif second:
        add('sunapha', ['Moon'] + second)
    elif twelfth:
        add('anapha', ['Moon'] + twelfth)
    else:
        with_moon = [g for g in FIVE if c.sign(g) == c.sign('Moon')]
        in_kendras = [g for g in SEVEN if g != 'Moon' and (c.house(g) in KENDRA or c.from_('Moon', g) in KENDRA)]
        if with_moon or in_kendras:
            add('kemadruma_bhanga', ['Moon'] + sorted(set(with_moon + in_kendras), key=SEVEN.index))
        else:
            add('kemadruma', ['Moon'])
    if all(c.from_('Moon', g) in (6, 7, 8) for g in TRIO):
        add('adhi', list(TRIO))
    harsh = list(c.malefics) + ['Rahu', 'Ketu']
    if all(c.house(g) in (6, 7, 8) for g in TRIO) and not any(
            c.sign(m) == c.sign(g) or (m in SEVEN and c.aspects(m, c.sign(g))) for m in harsh for g in TRIO):
        add('lagnadhi', list(TRIO))
    # Gaja Kesari (Raman #1): Jupiter in a kendra from the Moon, joined or aspected by a benefic,
    # and not debilitated, combust or in an enemy's sign
    helpers = [g for g in c.benefics if g != 'Jupiter' and (c.sign(g) == c.sign('Jupiter') or c.aspects(g, c.sign('Jupiter')))]
    if c.from_('Moon', 'Jupiter') in KENDRA and helpers and not planets['Jupiter'].get('combust') and \
            planets['Jupiter'].get('dignity') not in ('Debilitated', 'Enemy', 'Great Enemy'):
        add('gaja_kesari', ['Moon', 'Jupiter'] + [g for g in helpers if g != 'Moon'])
    if c.from_('Moon', 'Mars') in (1, 7):
        add('chandra_mangala', ['Moon', 'Mars'])
    if c.from_('Moon', 'Jupiter') in (6, 8, 12) and c.house('Moon') not in KENDRA:
        add('sakata', ['Moon', 'Jupiter'])
    if all(c.house(g) in UPACHAYA or c.from_('Moon', g) in UPACHAYA for g in TRIO):
        add('vasumati', list(TRIO))

    # --- Surya yogas ---
    before = [g for g in FIVE if c.from_('Sun', g) == 2]
    after = [g for g in FIVE if c.from_('Sun', g) == 12]
    if before and after:
        add('ubhayachari', ['Sun'] + before + after)
    elif before:
        add('vesi', ['Sun'] + before)
    elif after:
        add('vasi', ['Sun'] + after)
    if c.sign('Sun') == c.sign('Mercury'):
        combust = planets['Mercury'].get('combust')
        add('budhaditya', ['Sun', 'Mercury'],
            'Mercury is combust, so the yoga works only partly.' if combust else '',
            'புதன் அஸ்தங்கம் என்பதால் இந்த யோகம் பகுதியாகவே பலன் தரும்.' if combust else '')

    # --- Raja and Dhana yogas by lordship ---
    kendra_lords = {h: c.lord(h) for h in KENDRA}
    trikona_lords = {h: c.lord(h) for h in (5, 9)}
    pairs = set()
    for kh, kl in kendra_lords.items():
        for th, tl in trikona_lords.items():
            if kl != tl and c.associated(kl, tl):
                pairs.add(tuple(sorted((kl, tl), key=SEVEN.index)))
    for a, b in sorted(pairs, key=lambda x: (SEVEN.index(x[0]), SEVEN.index(x[1]))):
        add('raja', [a, b])
    for g in SEVEN:
        owned = {h for h in range(1, 13) if c.lord(h) == g}
        if owned & {4, 7, 10} and owned & {5, 9}:
            add('yogakaraka', [g])
    l9, l10 = c.lord(9), c.lord(10)
    if l9 != l10 and c.associated(l9, l10):
        add('dharma_karmadhipati', sorted({l9, l10}, key=SEVEN.index))
    dhana_pairs = set()
    for wh in (2, 11):
        for fh in (1, 5, 9):
            a, b = c.lord(wh), c.lord(fh)
            exchange = SIGN_LORDS[c.sign(a)] == b and SIGN_LORDS[c.sign(b)] == a
            if a != b and (c.sign(a) == c.sign(b) or exchange):
                dhana_pairs.add(tuple(sorted((a, b), key=SEVEN.index)))
    for a, b in sorted(dhana_pairs):
        add('dhana', [a, b])

    # --- Named yogas ---
    l1, l4, l5, l6 = c.lord(1), c.lord(4), c.lord(5), c.lord(6)
    lagna_lord_strong = (c.dignified(l1) or planets[l1].get('dignity') in ('Friend', 'Great Friend')) and c.house(l1) not in DUSTHANA
    if c.dignified(l9) and c.house(l9) in KENDRA + TRIKONA and lagna_lord_strong:
        add('lakshmi', sorted({l1, l9}, key=SEVEN.index))
    jupiter_lord = SIGN_LORDS[c.sign('Jupiter')]
    if all(c.house(g) in KENDRA + TRIKONA + (2,) for g in TRIO) and \
            (c.dignified('Jupiter') or planets['Jupiter'].get('dignity') == 'Exalted' or jupiter_lord in ('Sun', 'Moon', 'Mars')):
        add('saraswati', list(TRIO))
    # Parvata (Raman #14): the kendras hold only benefics, the 6th and 8th are empty or benefic
    harsh = list(c.malefics) + ['Rahu', 'Ketu']
    kendra_benefics = [g for g in c.benefics if c.house(g) in KENDRA]
    if kendra_benefics and not any(c.house(g) in KENDRA + (6, 8) for g in harsh):
        add('parvata', sorted(kendra_benefics, key=SEVEN.index))
    mutual_kendra = lambda a, b: (c.sign(b) - c.sign(a)) % 12 in (0, 3, 6, 9)
    if l4 != l9 and mutual_kendra(l4, l9) and c.dignified(l1):
        add('kahala', sorted({l4, l9, l1}, key=SEVEN.index))
    if planets[l1].get('dignity') == 'Exalted' and c.house(l1) in KENDRA and c.aspects('Jupiter', c.sign(l1)):
        add('chamara', [l1, 'Jupiter'] if l1 != 'Jupiter' else [l1])
    else:
        paired = next((h for h in (1, 7, 9, 10) if len([g for g in c.benefics if c.house(g) == h]) >= 2), None)
        if paired:
            add('chamara', [g for g in SEVEN if g in c.benefics and c.house(g) == paired])
    # Sankha (Raman #12): 5th and 6th lords in mutual kendras with a strong Lagna lord, or the Lagna
    # and 10th lords together in a movable sign with a strong 9th lord
    l10 = c.lord(10)
    if (l5 != l6 and mutual_kendra(l5, l6) and c.dignified(l1)) or \
            (l1 != l10 and c.sign(l1) == c.sign(l10) and c.sign(l1) % 3 == 0 and c.dignified(l9)):
        add('sankha', sorted({l5, l6, l1} if mutual_kendra(l5, l6) else {l1, l10, l9}, key=SEVEN.index))
    # Bheri (Raman #45): a strong 9th lord with the 1st, 2nd, 7th and 12th all occupied, or with
    # Venus, Jupiter and the Lagna lord in mutual kendras
    if c.dignified(l9) and (all(c.in_house(h) for h in (1, 2, 7, 12)) or
                            (mutual_kendra('Venus', 'Jupiter') and mutual_kendra('Venus', l1) and mutual_kendra('Jupiter', l1))):
        add('bheri', sorted({'Venus', 'Jupiter', l1, l9}, key=SEVEN.index))
    if c.from_('Jupiter', 'Mars') in (1, 7):
        add('guru_mangala', ['Jupiter', 'Mars'])
    # Amala (Raman #13): only benefics in the 10th from the Lagna or from the Moon
    for ref in (None, 'Moon'):
        occupants = [g for g in SEVEN + ('Rahu', 'Ketu') if (c.house(g) if ref is None else c.from_(ref, g)) == 10]
        if occupants and all(g in c.benefics for g in occupants):
            add('amala', occupants)
            break
    around = [g for g in SEVEN if c.house(g) in (2, 12)]
    if any(c.house(g) == 2 for g in c.benefics) and any(c.house(g) == 12 for g in c.benefics) and \
            all(g in c.benefics for g in around) and not any(c.house(n) in (2, 12) for n in ('Rahu', 'Ketu')):
        add('shubha_kartari', around)
    harsh = list(c.malefics) + ['Rahu', 'Ketu']
    if any(c.house(g) == 2 for g in harsh) and any(c.house(g) == 12 for g in harsh) and not any(g in c.benefics for g in around):
        add('papa_kartari', [g for g in SEVEN + ('Rahu', 'Ketu') if g in harsh and c.house(g) in (2, 12)])

    # --- Parivartana: two lords in each other's signs ---
    seen = set()
    for h1 in range(1, 13):
        for h2 in range(h1 + 1, 13):
            a, b = c.lord(h1), c.lord(h2)
            if a == b or (a, b) in seen or c.house(a) != h2 or c.house(b) != h1:
                continue
            seen.add((a, b))
            kind = 'dainya_parivartana' if {h1, h2} & set(DUSTHANA) else ('khala_parivartana' if 3 in (h1, h2) else 'maha_parivartana')
            add(kind, [a, b], f"Lords of houses {h1} and {h2}.", f"{h1}, {h2}-ஆம் பாவ அதிபதிகள்.")

    # --- Vipareeta Raja yogas ---
    for house, key in ((6, 'harsha'), (8, 'sarala'), (12, 'vimala')):
        lord = c.lord(house)
        if c.house(lord) in DUSTHANA:
            add(key, [lord])

    # --- Neechabhanga: the classical cancellations of debilitation ---
    for g in SEVEN:
        if planets[g].get('dignity') != 'Debilitated':
            continue
        deb = c.sign(g)
        dispositor = SIGN_LORDS[deb]
        exalt_lord = SIGN_LORDS[EXALTATION_SIGN[g]]
        exalted_here = [q for q in SEVEN if EXALTATION_SIGN[q] == deb]
        in_kendra = lambda q: c.house(q) in KENDRA or c.from_('Moon', q) in KENDRA
        reasons = []
        if in_kendra(dispositor):
            reasons.append((f'{dispositor}, lord of the sign, is in a kendra', f'ராசி அதிபதி {PLANET_TAMIL[dispositor]} கேந்திரத்தில்'))
        if exalt_lord != dispositor and in_kendra(exalt_lord):
            reasons.append((f'{exalt_lord}, lord of its exaltation sign, is in a kendra', f'உச்ச வீட்டு அதிபதி {PLANET_TAMIL[exalt_lord]} கேந்திரத்தில்'))
        for q in exalted_here:
            if in_kendra(q):
                reasons.append((f'{q}, exalted in that sign, is in a kendra', f'அந்த ராசியில் உச்சம் பெறும் {PLANET_TAMIL[q]} கேந்திரத்தில்'))
        if dispositor != g and c.aspects(dispositor, deb):
            reasons.append((f'{dispositor} aspects it', f'{PLANET_TAMIL[dispositor]} பார்வை'))
        if planets[g]['vargas']['D9'] == EXALTATION_SIGN[g]:
            reasons.append(('it is exalted in the Navamsa', 'நவாம்சத்தில் உச்சம்'))
        if reasons:
            add('neechabhanga', [g], 'Cancelled because ' + '; '.join(r[0] for r in reasons) + '.',
                'பங்கக் காரணம்: ' + '; '.join(r[1] for r in reasons) + '.')

    # --- Challenging combinations ---
    same = lambda a, b: c.sign(a) == c.sign(b)
    if same('Jupiter', 'Rahu'):
        add('guru_chandala', ['Jupiter', 'Rahu'])
    eclipsed = [(lum, node) for lum in ('Sun', 'Moon') for node in ('Rahu', 'Ketu') if same(lum, node)]
    if eclipsed:
        add('grahana', sorted({g for pair in eclipsed for g in pair}, key=lambda g: (SEVEN + ('Rahu', 'Ketu')).index(g)))
    fiery = [node for node in ('Rahu', 'Ketu') if same('Mars', node)]
    if fiery:
        add('angaraka', ['Mars'] + fiery)
    if same('Saturn', 'Moon'):
        add('punarphoo', ['Saturn', 'Moon'])
    l11 = c.lord(11)
    if c.house(l11) in DUSTHANA:
        add('daridra', [l11])

    # --- Nabhasa yogas: the pattern of the seven grahas ---
    signs = [c.sign(g) for g in SEVEN]
    houses = {c.house(g) for g in SEVEN}
    nabhasa = []
    if all(s % 3 == 0 for s in signs):
        nabhasa.append('rajju')
    elif all(s % 3 == 1 for s in signs):
        nabhasa.append('musala')
    elif all(s % 3 == 2 for s in signs):
        nabhasa.append('nala')
    benefic_kendras = sum(1 for h in KENDRA if any(c.house(g) == h for g in c.benefics))
    malefic_kendras = sum(1 for h in KENDRA if any(c.house(g) == h for g in c.malefics))
    if benefic_kendras == 3:
        nabhasa.append('mala')
    if malefic_kendras == 3:
        nabhasa.append('sarpa')
    # Akriti yogas: the shape the seven grahas make. One shape per chart, most specific first;
    # exact = the grahas occupy exactly these houses, within = they all fall inside them.
    span = lambda start: {(start + i - 1) % 12 + 1 for i in range(7)}
    good_in = lambda hs: all(c.house(g) in hs for g in c.benefics) and hs <= {c.house(g) for g in c.benefics}
    bad_in = lambda hs: all(c.house(g) in hs for g in c.malefics) and hs <= {c.house(g) for g in c.malefics}
    akriti = [
        ('sakata_nabhasa', 'exact', [{1, 7}]), ('vihaga', 'exact', [{4, 10}]),
        ('gada', 'exact', [{1, 4}, {4, 7}, {7, 10}, {10, 1}]), ('sringataka', 'exact', [{1, 5, 9}]),
        ('hala', 'exact', [{2, 6, 10}, {3, 7, 11}, {4, 8, 12}]), ('kamala', 'exact', [set(KENDRA)]),
        ('vapi', 'within', [{2, 5, 8, 11}, {3, 6, 9, 12}]),
        ('yupa', 'within', [{1, 2, 3, 4}]), ('ishu', 'within', [{4, 5, 6, 7}]),
        ('shakti', 'within', [{7, 8, 9, 10}]), ('danda', 'within', [{10, 11, 12, 1}]),
        ('nauka', 'exact', [span(1)]), ('koota', 'exact', [span(4)]), ('chatra', 'exact', [span(7)]),
        ('chapa', 'exact', [span(10)]), ('ardha_chandra', 'exact', [span(s) for s in (2, 3, 5, 6, 8, 9, 11, 12)]),
        ('chakra', 'exact', [{1, 3, 5, 7, 9, 11}]), ('samudra', 'exact', [{2, 4, 6, 8, 10, 12}])
    ]
    shape = None
    if good_in({1, 7}) and bad_in({4, 10}):
        shape = 'vajra'
    elif bad_in({1, 7}) and good_in({4, 10}):
        shape = 'yava'
    for key, mode, options in akriti:
        if shape:
            break
        for option in options:
            if (houses == option) if mode == 'exact' else houses <= option:
                shape = key
                break
    if shape:
        nabhasa.append(shape)
    if not nabhasa:  # the Sankhya yogas stand only when no other Nabhasa yoga forms
        nabhasa.append(SANKHYA[len(set(signs))])
    for key in nabhasa:
        add(key, list(SEVEN))

    order = {'good': 0, 'mixed': 1, 'cancelled': 2, 'bad': 3}
    found.sort(key=lambda y: order[y['nature']])
    return found
