"""JoRoScope Comprehensive Life Prediction Engine
Authoritative Vedic & Tamil astrological prediction generator providing:
1. Birth Star (Nakshatra) & Lagna Detailed Characteristics
2. 12 Bhavas (House-by-House) In-Depth Life Readings
3. Planetary Placements in 12 Houses
4. 9 Maha Dasas & Current Dasa-Bhukti Forecast
5. Gochara (Transit) Predictions (Sade Sati, Jupiter, Rahu-Ketu)
6. Lucky Gemstone, Colors, Numbers, Deities & Remedial Guidance
Available in both English and authentic Tamil (தமிழ்).
"""

from datetime import datetime
from zoneinfo import ZoneInfo

try:
    from .timeline import calculate_timeline_predictions
except ImportError:
    from timeline import calculate_timeline_predictions

SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
TAMIL_SIGNS = ['மேஷம்', 'ரிஷபம்', 'மிதுனம்', 'கடகம்', 'சிம்மம்', 'கன்னி', 'துலாம்', 'விருச்சிகம்', 'தனுசு', 'மகரம்', 'கும்பம்', 'மீனம்']
SIGN_LORDS = ['Mars', 'Venus', 'Mercury', 'Moon', 'Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Saturn', 'Jupiter']
PLANET_TAMIL = {
    'Sun': 'சூரியன்', 'Moon': 'சந்திரன்', 'Mars': 'செவ்வாய்', 'Mercury': 'புதன்',
    'Jupiter': 'குரு', 'Venus': 'சுக்கிரன்', 'Saturn': 'சனி', 'Rahu': 'ராகு', 'Ketu': 'கேது',
    'Ascendant': 'லக்னம்'
}
KAKSHYA_LORDS = ['Saturn', 'Jupiter', 'Mars', 'Sun', 'Venus', 'Mercury', 'Moon', 'Ascendant']
KAKSHYA_LORDS_TA = ['சனி', 'குரு', 'செவ்வாய்', 'சூரியன்', 'சுக்கிரன்', 'புதன்', 'சந்திரன்', 'லக்னம்']

# 1. 27 Nakshatras Life Predictions (English & Tamil)
NAKSHATRA_PREDICTIONS = {
    'Ashwini': {
        'en': 'Governed by Ketu and symbolized by the Horse Head. Bestows swift intellect, youthful vitality, spontaneous courage, and natural healing abilities. You excel in pioneering new ventures, sports, or medicine. You value autonomy and direct action, though cultivating patience will help you finish long-term endeavors.',
        'ta': 'அசுவினி நட்சத்திரத்தில் பிறந்த நீங்கள் சுறுசுறுப்பும், கூரிய மதியும், தளராத தைரியமும் கொண்டவர்கள். குதிரை முகக் குறியீடு போல் எதிலும் வேகம் காட்டி முதலிடம் பெறுவீர்கள். மருத்துவம், நிர்வாகம், புதிய முயற்சிகளில் சிறந்து விளங்குவீர்கள். சுதந்திர உணர்வும் உதவும் குணமும் உண்டு. அவசர முடிவுகளைத் தவிர்ப்பது பெரும் வெற்றியைத் தரும்.'
    },
    'Bharani': {
        'en': 'Governed by Venus and symbolized by the Yoni. Bestows strong willpower, intense determination, creative magnetism, and loyalty to loved ones. You are unafraid of transformation and difficult challenges. You possess exquisite aesthetic taste, though avoiding impulsive arguments ensures enduring peace.',
        'ta': 'பரணி நட்சத்திரத்தில் பிறந்த நீங்கள் அசைக்க முடியாத மன உறுதி, விடாமுயற்சி, கவர்ச்சியான ஆளுமை கொண்டவர்கள். எத்தகைய கடினமான சூழ்நிலையையும் எதிர்கொள்ளும் துணிச்சல் உண்டு. கலை ஆர்வம், நேர்மை, ரசனை மிக்கவர்கள். பிடிவாத குணத்தைக் குறைத்து நிதானத்தைக் கடைப்பிடித்தால் வாழ்வில் உயர்ந்த நிலையை அடைவீர்கள்.'
    },
    'Krittika': {
        'en': 'Governed by Sun and symbolized by the Flame/Razor. Bestows brilliant intellect, commanding dignity, fiery protective instinct, and radiant ambition. You cut through hypocrisy with sharp clarity. In business or leadership you rise steadily through discipline.',
        'ta': 'கிருத்திகை நட்சத்திரத்தில் பிறந்த நீங்கள் சூரியனின் ஆதிக்கத்தால் கம்பீரமும், தலைமை தாங்கும் ஆற்றலும், கூர்மையான அறிவாற்றலும் பெற்றவர்கள். அக்னி போன்ற சுடர்விடும் உறுதி உண்டு. தர்ம சிந்தனையும், நேர்மையும் உங்கள் பலம். முன்கோபத்தைக் குறைத்துக் கொண்டால் சமூகத்தில் பெரும் செல்வாக்கு பெறுவீர்கள்.'
    },
    'Rohini': {
        'en': 'Governed by Moon and symbolized by the Chariot. Bestows artistic charm, emotional magnetism, commercial acumen, and refined eloquence. You attract beauty, material prosperity, and genuine admirers. Blessed with a fertile imagination and stable home life.',
        'ta': 'ரோகிணி நட்சத்திரத்தில் பிறந்த நீங்கள் வசீகரத் தோற்றமும், கனிவான பேச்சும், ரசனை உணர்வும் கொண்டவர்கள். சந்திரனின் ஆசியால் கலை, வியாபாரம், பொதுத் தொடர்புகளில் பெரும் வெற்றி பெறுவீர்கள். செல்வம், வாகன சுகம், குடும்ப மகிழ்ச்சி இயல்பாகவே அமையும். உணர்ச்சிவசப்படுவதைக் கட்டுப்படுத்துவது நல்லது.'
    },
    'Mrigashira': {
        'en': 'Governed by Mars and symbolized by the Deer Head. Bestows curious intellect, inquiring nature, gentle speech, and sharp investigative instinct. You are an eternal seeker of knowledge and love exploring new horizons.',
        'ta': 'மிருகசீரிஷம் நட்சத்திரத்தில் பிறந்த நீங்கள் அறிவுத் தேடலும், சாதுரியமான பேச்சும், மென்மையான குணமும் கொண்டவர்கள். மான் போன்ற சுறுசுறுப்பும் எச்சரிக்கை உணர்வும் உண்டு. ஆராய்ச்சி, எழுத்து, தகவல் தொடர்புத் துறைகளில் மிளிர்வீர்கள். சந்தேகக் குணத்தை தவிர்த்து உறுதியான முடிவுகளை எடுப்பது நலம்.'
    },
    'Ardra': {
        'en': 'Governed by Rahu and symbolized by the Teardrop. Bestows razor-sharp analytical faculty, transformative brilliance, and resilience through life trials. You overcome obstacles and achieve hard-won breakthroughs in modern technology, research, or enterprise.',
        'ta': 'திருவாதிரை நட்சத்திரத்தில் பிறந்த நீங்கள் தீவிர சிந்தனையும், கூர்மையான பகுத்தறிவும், எதையும் ஆழமாக உணரும் ஆற்றலும் கொண்டவர்கள். ருத்ரனின் அம்சத்தால் சோதனைகளைக் கடந்து சாதனைகளைப் படைப்பீர்கள். நவீன அறிவியல், தொழில்நுட்பம், ஆராய்ச்சியில் உயர்நிலை அடைவீர்கள்.'
    },
    'Punarvasu': {
        'en': 'Governed by Jupiter and symbolized by the Quiver of Arrows. Bestows deep righteousness, benevolent optimism, spiritual grace, and recovery of lost fortune. You inspire others with wisdom, forgiveness, and moral integrity.',
        'ta': 'புனர்பூசம் நட்சத்திரத்தில் பிறந்த நீங்கள் அமைதியான சுபாவமும், தர்ம சிந்தனையும், சிறந்த குணமும் கொண்டவர்கள். இழந்ததை மீண்டும் பெறும் அற்புத பாக்கியம் உண்டு. குருவின் அருளால் கல்வி, ஆன்மீகம், ஆசிரியர், ஆலோசகர் பணிகளில் பெரும் புகழ் பெறுவீர்கள்.'
    },
    'Pushya': {
        'en': 'Governed by Saturn and ruled by Brihaspati, symbolized by the Cow Udder. Considered the most nourishing of all nakshatras. Bestows steadfast wisdom, ethical wealth, patience, and community leadership.',
        'ta': 'பூசம் நட்சத்திரத்தில் பிறந்த நீங்கள் தியாக மனப்பான்மை, நேர்மை, ஆன்மீக பக்தி கொண்டவர்கள். அனைத்து நட்சத்திரங்களிலும் மிக உன்னதமான சுப நட்சத்திரமாகும். உழைப்பால் படிப்படியாக முன்னேறி நிரந்தர சொத்துக்களையும், மக்கள் நன்மதிப்பையும் பெறுவீர்கள்.'
    },
    'Ashlesha': {
        'en': 'Governed by Mercury and symbolized by the Coiled Serpent. Bestows intuitive psychology, diplomatic finesse, strategic intellect, and protective shrewdness. You excel in finance, psychology, and executive management.',
        'ta': 'ஆயில்யம் நட்சத்திரத்தில் பிறந்த நீங்கள் மதிநுட்பமும், ராஜதந்திர பேச்சாற்றலும், எதையும் முன்கூட்டியே அறியும் உள்ளுணர்வும் கொண்டவர்கள். சர்ப்பக் குறியீடு போல் சமயோசித புத்தியால் எத்தகைய சவால்களையும் வெல்வீர்கள். வியாபாரம், பொருளாதாரம், அரசியலில் செல்வாக்கு பெறுவீர்கள்.'
    },
    'Magha': {
        'en': 'Governed by Ketu and symbolized by the Royal Throne. Bestows noble lineage consciousness, regal presence, leadership authority, and respect for tradition. You naturally assume positions of authority and command respect.',
        'ta': 'மகம் நட்சத்திரத்தில் பிறந்த நீங்கள் கம்பீரமான தோற்றமும், நிர்வாகத் திறமையும், முன்னோர்களின் ஆசியும் பெற்றவர்கள். சிம்மாசனக் குறியீடு போல் தலைமைப் பதவிகளை வகிப்பீர்கள். தாராள மனமும், கௌரவமான வாழ்க்கையும் அமையும்.'
    },
    'Purva Phalguni': {
        'en': 'Governed by Venus and symbolized by the Hammock/Bed. Bestows vibrant charisma, romantic elegance, artistic creativity, and love of luxury and social celebration. You bring joy and harmony to your surroundings.',
        'ta': 'பூரம் நட்சத்திரத்தில் பிறந்த நீங்கள் இன்முகமும், கலை ரசனையும், கவர்ச்சிகரமான பேச்சும் கொண்டவர்கள். சுக்கிரனின் அருளால் சுகபோக வாழ்க்கை, நண்பர்களின் ஆதரவு, மகிழ்ச்சியான குடும்பம் அமையும். ஆடம்பரச் செலவுகளைக் குறைப்பது சேமிப்பை உயர்த்தும்.'
    },
    'Uttara Phalguni': {
        'en': 'Governed by Sun and symbolized by the Four Legs of Bed. Bestows generous patronage, reliable friendship, philanthropic nature, and civic responsibility. You excel in diplomacy, statecraft, and executive leadership.',
        'ta': 'உத்திரம் நட்சத்திரத்தில் பிறந்த நீங்கள் கொடுத்த வாக்கைக் காப்பாற்றும் உத்தம குணம் கொண்டவர்கள். சூரியனின் ஆதிக்கத்தால் தலைமைப் பண்பும், நற்பெயரும் உண்டு. அரசாங்க அனுகூலம், பொதுநல ஈடுபாடு, சமுதாய கௌரவம் எளிதில் கிட்டும்.'
    },
    'Hasta': {
        'en': 'Governed by Moon and symbolized by the Open Hand. Bestows dexterity, craft skills, commercial versatility, witty humor, and healing touch. You are an expert organizer and persuasive communicator.',
        'ta': 'அஸ்தம் நட்சத்திரத்தில் பிறந்த நீங்கள் கைத்தொழில் வல்லமை, புத்தி சாதுரியம், நகைச்சுவை உணர்வு கொண்டவர்கள். கைரேகை போன்ற கை ராசி மிக்கவர்கள். வியாபாரம், கணக்கு, எழுத்து, கலைகளில் கொடிகட்டிப் பறப்பீர்கள்.'
    },
    'Chitra': {
        'en': 'Governed by Mars and symbolized by the Bright Jewel. Bestows dazzling creativity, architectural precision, visual aesthetics, and independent spirit. You love design, structure, and perfection.',
        'ta': 'சித்திரை நட்சத்திரத்தில் பிறந்த நீங்கள் நவரத்தினம் போன்ற வசீகரமும், கலை நுணுக்கமும், தனித்துவமான சிந்தனையும் கொண்டவர்கள். விஸ்வகர்மாவின் அம்சம் பெற்றதால் வடிவமைப்பு, பொறியியல், கட்டடக் கலைகளில் முத்திரை பதிப்பீர்கள்.'
    },
    'Swati': {
        'en': 'Governed by Rahu and symbolized by the Young Shoot in the Wind. Bestows flexible diplomacy, mercantile independence, fair-minded justice, and commercial agility. You rise high like the wind through adaptable enterprise.',
        'ta': 'சுவாதி நட்சத்திரத்தில் பிறந்த நீங்கள் சுதந்திர சிந்தனையும், சமரசப் போக்கும், எதிலும் நேர்மையும் கொண்டவர்கள். காற்றில் ஆடும் இளம் பயிர் போல் நெளிவு சுளிவுடன் காரியம் சாதிப்பீர்கள். வியாபாரம், சட்டம், வெளிநாட்டுத் தொடர்புகளில் மேன்மை பெறுவீர்கள்.'
    },
    'Vishakha': {
        'en': 'Governed by Jupiter and symbolized by the Triumphal Arch. Bestows intense focus, burning ambition, competitive stamina, and triumphant conquest of goals. You do not stop until your mission is complete.',
        'ta': 'விசாகம் நட்சத்திரத்தில் பிறந்த நீங்கள் வைராக்கியமும், விடாமுயற்சியும், குறிக்கோளை அடையும் தீவிரமும் கொண்டவர்கள். வெற்றித் தோரணம் போல் எத்துறையிலும் முன்னணியில் நிற்பீர்கள். தலைமைப் பொறுப்புகளும், சாதனைகளும் உங்களை வந்தடையும்.'
    },
    'Anuradha': {
        'en': 'Governed by Saturn and symbolized by the Lotus. Bestows devotion, loyalty, enduring friendships, foreign travel, and grace under pressure. Like the lotus blooming through mud, you rise gracefully above early adversities.',
        'ta': 'அனுஷம் நட்சத்திரத்தில் பிறந்த நீங்கள் தாமரை மலர் போன்ற மென்மையான உள்ளமும், கடின உழைப்பும், நட்புக்கு இலக்கணமான குணமும் கொண்டவர்கள். வெளியூர் மற்றும் வெளிநாட்டுப் பயணங்களால் அதிக யோகம் பெறுவீர்கள்.'
    },
    'Jyeshtha': {
        'en': 'Governed by Mercury and symbolized by the Circular Amulet/Earring. Bestows protective seniority, mental sharpness, defensive courage, and elder responsibility. You command deference and protect your clan.',
        'ta': 'கேட்டை நட்சத்திரத்தில் பிறந்த நீங்கள் மூத்தவர் போன்ற அனுபவ அறிவும், சமயோசித புத்தியும், பிறருக்கு வழிகாட்டும் ஆற்றலும் கொண்டவர்கள். குடும்பத்திலும் சமுதாயத்திலும் முக்கியஸ்தராக விளங்குவீர்கள்.'
    },
    'Mula': {
        'en': 'Governed by Ketu and symbolized by Tied Roots. Bestows profound investigative curiosity, philosophical depth, courage to uproot falsity, and spiritual transformation. You get to the core root of every matter.',
        'ta': 'மூலம் நட்சத்திரத்தில் பிறந்த நீங்கள் ஆழமான சிந்தனையும், துணிச்சலும், எதன் உண்மை வேரையும் ஆராயும் திறனும் கொண்டவர்கள். ஆன்மீகம், ஆராய்ச்சி, தத்துவம், அரசியலில் பெரும் திருப்புமுனைகளை ஏற்படுத்துவீர்கள்.'
    },
    'Purva Ashadha': {
        'en': 'Governed by Venus and symbolized by the Elephant Tusk / Winnowing Fan. Bestows invincible confidence, magnetic oratory, victory over rivals, and popularity. Your faith in your capabilities inspires everyone.',
        'ta': 'பூராடம் நட்சத்திரத்தில் பிறந்த நீங்கள் தன்னம்பிக்கையும், பேச்சாற்றலும், எதிலும் தோல்வி காணாத வெற்றி மனப்பான்மையும் கொண்டவர்கள். நீர் போன்ற தூய்மையான குணமும், அனைவரையும் கவரும் ஆளுமையும் உண்டு.'
    },
    'Uttara Ashadha': {
        'en': 'Governed by Sun and symbolized by the Small Bed / Elephant Tusk. Bestows enduring integrity, unshakeable virtue, steadfast leadership, and universal respect. You complete what you begin with total honor.',
        'ta': 'உத்திராடம் நட்சத்திரத்தில் பிறந்த நீங்கள் சாந்த குணமும், சத்திய நேர்மையும், கடமை உணர்வும் கொண்டவர்கள். சூரியனின் ஆசியால் நிலைத்த வெற்றியும், அரசு வழி கௌரவமும், அனைவராலும் மதிக்கப்படும் நிலையும் பெறுவீர்கள்.'
    },
    'Shravana': {
        'en': 'Governed by Moon and symbolized by the Ear. Bestows receptive listening, scholarly learning, oral tradition mastery, and fame through communication. You absorb knowledge like a sponge and advise with tact.',
        'ta': 'திருவோணம் நட்சத்திரத்தில் பிறந்த நீங்கள் சிறந்த கல்விமான்களாகவும், நல்ல ஆலோசகர்களாகவும், பொறுமை மிக்கவர்களாகவும் விளங்குவீர்கள். மகாவிஷ்ணுவின் ஆசி பெற்றதால் பேரும் புகழும், சமூகத்தில் உயர்ந்த மரியாதையும் பெறுவீர்கள்.'
    },
    'Dhanishtha': {
        'en': 'Governed by Mars and symbolized by the Drum / Flute. Bestows rhythmic timing, financial wealth, musical affinity, and organizational command. You possess an innate sense of harmony and resource management.',
        'ta': 'அவிட்டம் நட்சத்திரத்தில் பிறந்த நீங்கள் தாராள குணமும், இசை மற்றும் கலை ஆர்வமும், செல்வாக்கும் கொண்டவர்கள். உடுக்கை போன்ற சுப சப்தம் போல் உங்கள் பெயர் பரவும். பூமி யோகமும், வீடு வாகன யோகமும் சிறப்பாக அமையும்.'
    },
    'Shatabhisha': {
        'en': 'Governed by Rahu and symbolized by 100 Physicians / Empty Circle. Bestows mystical vision, healing acumen, independent solitude, and secretive problem-solving depth. You see beyond ordinary surface appearances.',
        'ta': 'சதயம் நட்சத்திரத்தில் பிறந்த நீங்கள் மர்மங்களை அறியும் ஆற்றலும், மருத்துவ ஞானமும், தனித்துவமான சிந்தனையும் கொண்டவர்கள். நூறு மருத்துவர்கள் குணப்படுத்தும் ஆற்றல் கொண்டவர் என்பதால் ஆலோசனை, ஜோதிடம், மருத்துவத்தில் ஜொலிப்பீர்கள்.'
    },
    'Purva Bhadrapada': {
        'en': 'Governed by Jupiter and symbolized by the Front of Funeral Cot / Two-Faced Man. Bestows intense idealism, transformative passion, philanthropic sacrifice, and deep esoteric intellect.',
        'ta': 'பூரட்டாதி நட்சத்திரத்தில் பிறந்த நீங்கள் ஆன்மீக தாகமும், கொள்கைப் பிடிப்பும், சிறந்த பேச்சாற்றலும் கொண்டவர்கள். குருவின் அருளால் நியாய உணர்வும், சமூக நல ஈடுபாடும் உண்டு. பொருளாதாரத்தில் சிறந்த நிலை காண்பீர்கள்.'
    },
    'Uttara Bhadrapada': {
        'en': 'Governed by Saturn and symbolized by the Back of Cot / Deep Sea Serpent. Bestows serene wisdom, emotional equanimity, benevolent charity, and spiritual enlightenment. You remain tranquil in all conditions.',
        'ta': 'உத்திரட்டாதி நட்சத்திரத்தில் பிறந்த நீங்கள் ஆழ்ந்த சாந்தமும், விவேகமும், பொறுமையும் கொண்டவர்கள். அமைதியான சமுத்திரம் போன்ற ஞானம் உண்டு. தான தர்மங்கள் செய்து நற்பெயரையும், நிலையான சொத்துக்களையும் ஈட்டுவீர்கள்.'
    },
    'Revati': {
        'en': 'Governed by Mercury and symbolized by the Fish Swimming in Water. Bestows compassionate empathy, sweet eloquence, traveler fortune, and divine protection. The final nakshatra of fulfillment and universal love.',
        'ta': 'ரேவதி நட்சத்திரத்தில் பிறந்த நீங்கள் கனிவான சுபாவமும், இனிமையான பேச்சும், உதவும் மனமும் கொண்டவர்கள். 27 நட்சத்திரங்களின் நிறைவு நட்சத்திரமாக விளங்குவதால் தெய்வீக அருளும், பயணங்களால் நன்மையும், நிறைவான வாழ்க்கையும் அமையும்.'
    }
}

# 2. 12 Ascendants (Lagnas) Physical Body, Mind & Vitality
LAGNA_PREDICTIONS = {
    'Aries': {
        'en': 'Aries (Mesha) Lagna is a fiery cardinal sign ruled by Mars. You possess an athletic build, energetic gait, expressive eyes, and natural initiative. You are quick to start ventures, courageous in competition, and direct in communication. You thrive when given autonomy and leadership.',
        'ta': 'மேஷ லக்னத்தில் பிறந்த நீங்கள் செவ்வாயின் ஆதிக்கத்தால் சுறுசுறுப்பான உடலமைப்பும், பிரகாசமான முகமும், தன்னம்பிக்கையும் கொண்டவர்கள். வேகமான நடை, நேரடியான பேச்சு, பிறரை வழிநடத்தும் ஆற்றல் உண்டு. எதிலும் முதன்மையாக நிற்க விரும்புவீர்கள்.'
    },
    'Taurus': {
        'en': 'Taurus (Rishabha) Lagna is an earthy fixed sign ruled by Venus. You possess a sturdy physical constitution, handsome/graceful features, melodious voice, and calm endurance. You build wealth through steady patience, artistic appreciation, and practical enterprise.',
        'ta': 'ரிஷப லக்னத்தில் பிறந்த நீங்கள் சுக்கிரனின் அருளால் கவர்ச்சியான தோற்றமும், கம்பீரமான உடலும், இனிமையான குரலும் பெற்றவர்கள். பொறுமையும் நிதானமும் உங்கள் பலம். கலை ரசனை, நிலம் மற்றும் ஆடை ஆபரண சேர்க்கை சிறப்பாக அமையும்.'
    },
    'Gemini': {
        'en': 'Gemini (Mithuna) Lagna is an airy dual sign ruled by Mercury. You possess a tall, nimble physique, quick gestures, youthful appearance, and sparkling wit. You excel in communication, writing, commerce, multi-tasking, and intellectual analysis.',
        'ta': 'மிதுன லக்னத்தில் பிறந்த நீங்கள் புதனின் ஆதிக்கத்தால் இளமையான தோற்றமும், வசீகரப் பார்வையும், பன்முகத் திறமையும் கொண்டவர்கள். நகைச்சுவை உணர்வும், பேச்சாற்றலும், எழுத்துத் திறனும் உண்டு. வணிகம் மற்றும் தகவல்தொடர்பில் கொடிகட்டிப் பறப்பீர்கள்.'
    },
    'Cancer': {
        'en': 'Cancer (Kataka) Lagna is a watery cardinal sign ruled by the Moon. You possess round, gentle features, soulful eyes, deep emotional sensitivity, and strong attachment to family. You are naturally protective, empathetic, and intuitive.',
        'ta': 'கடக லக்னத்தில் பிறந்த நீங்கள் சந்திரனின் அம்சத்தால் சாந்தமான முகமும், கருணை உள்ளமும், ஆழமான பாசமும் கொண்டவர்கள். தாயன்பும், குடும்பப் பற்றும் அதிகம். கற்பனைத் திறனும், உள்ளுணர்வும் உங்களை வழிநடத்தும்.'
    },
    'Leo': {
        'en': 'Leo (Simha) Lagna is a fiery fixed sign ruled by the Sun. You possess a regal posture, broad shoulders, commanding voice, and magnetic presence. You possess natural dignity, generous magnanimity, leadership pride, and public authority.',
        'ta': 'சிம்ம லக்னத்தில் பிறந்த நீங்கள் சூரியனின் ஆதிக்கத்தால் கம்பீரமான நடையும், சிங்கத்தைப் போன்ற பெருந்தன்மையும், தலைமைப் பண்பும் கொண்டவர்கள். அநீதியைக் கண்டு பொங்குவீர்கள். சமுதாயத்தில் உயர்ந்த அந்தஸ்தையும் கௌரவத்தையும் பெறுவீர்கள்.'
    },
    'Virgo': {
        'en': 'Virgo (Kanya) Lagna is an earthy dual sign ruled by Mercury. You possess refined facial symmetry, modest demeanor, sharp analytical eyes, and methodical hygiene. You excel in critical analysis, financial precision, administration, and service.',
        'ta': 'கன்னி லக்னத்தில் பிறந்த நீங்கள் புதனின் அருளால் அமைதியான தோற்றமும், கூர்மையான அறிவாற்றலும், நுணுக்கமான வேலைப்பாடும் கொண்டவர்கள். எதையும் திட்டமிட்டு நேர்த்தியாகச் செய்வீர்கள். கணக்கு, நிர்வாகம், மருத்துவத்தில் சிறப்பு காண்பீர்கள்.'
    },
    'Libra': {
        'en': 'Libra (Thula) Lagna is an airy cardinal sign ruled by Venus. You possess attractive proportions, balanced demeanor, dimpled smile, and natural charm. You are driven by justice, harmonious partnership, diplomacy, and exquisite cultural taste.',
        'ta': 'துலாம் லக்னத்தில் பிறந்த நீங்கள் சுக்கிரனின் ஆதிக்கத்தால் அழகான தோற்றமும், வசீகர சிரிப்பும், நடுநிலையான சிந்தனையும் கொண்டவர்கள். தராசு போல் நியாய உணர்வும், சட்டம், வணிகம், பொதுவாழ்வில் நற்பெயரும் பெறுவீர்கள்.'
    },
    'Scorpio': {
        'en': 'Scorpio (Vrischika) Lagna is a watery fixed sign ruled by Mars. You possess penetrating, magnetic eyes, commanding presence, emotional depth, and unshakeable resilience. You are deeply loyal, perceptive of hidden truths, and secretive.',
        'ta': 'விருச்சிக லக்னத்தில் பிறந்த நீங்கள் செவ்வாயின் ஆதிக்கத்தால் ஊடுருவிப் பார்க்கும் காந்தக் கண்களும், ஆழ்ந்த மன உறுதியும் கொண்டவர்கள். எத்தகைய ரகசியங்களையும் அறிவீர்கள். சோதனைகளை சாதனைகளாக மாற்றும் அசாத்திய வலிமை உண்டு.'
    },
    'Sagittarius': {
        'en': 'Sagittarius (Dhanus) Lagna is a fiery dual sign ruled by Jupiter. You possess a tall, athletic stature, jovial expression, expansive forehead, and optimistic vitality. You are guided by higher truth, philosophy, justice, sports, and outdoor exploration.',
        'ta': 'தனுசு லக்னத்தில் பிறந்த நீங்கள் குருவின் அருளால் உயரமான தோற்றமும், பரந்த நெற்றியும், ஆன்மீக அறிவும் கொண்டவர்கள். வில்லின் அம்பு போன்ற நேர்மையும், தர்ம சிந்தனையும், தத்துவ நாட்டமும் உங்களை உயர்த்தும்.'
    },
    'Capricorn': {
        'en': 'Capricorn (Makara) Lagna is an earthy cardinal sign ruled by Saturn. You possess a wiry constitution, serious thoughtful gaze, youthful aging process, and pragmatic endurance. You rise steadily through discipline, duty, and relentless ambition.',
        'ta': 'மகர லக்னத்தில் பிறந்த நீங்கள் சனியின் ஆதிக்கத்தால் உறுதியான உடலமைப்பும், விடாமுயற்சியும், கடமை உணர்வும் கொண்டவர்கள். இளமையில் போராட்டங்கள் இருந்தாலும், படிப்படியாக முன்னேறி முதுமையில் உச்ச நிலையை அடைவீர்கள்.'
    },
    'Aquarius': {
        'en': 'Aquarius (Kumbha) Lagna is an airy fixed sign ruled by Saturn. You possess a tall/proportionate build, intellectual aura, visionary eyes, and egalitarian mindset. You are deeply progressive, humanitarian, innovative, and loyal in friendship.',
        'ta': 'கும்ப லக்னத்தில் பிறந்த நீங்கள் சனியின் ஆதிக்கத்தால் பரந்த மனப்பான்மையும், விஞ்ஞான சிந்தனையும், பொதுநலப் பண்பும் கொண்டவர்கள். குடம் போன்ற ஞானப் பொக்கிஷம். புதிய கண்டுபிடிப்புகள், சமுதாய மாற்றங்களில் முன்னிற்பீர்கள்.'
    },
    'Pisces': {
        'en': 'Pisces (Meena) Lagna is a watery dual sign ruled by Jupiter. You possess soft soulful eyes, gentle romantic constitution, imaginative mind, and spiritual empathy. You love music, meditation, ocean horizons, and universal compassion.',
        'ta': 'மீன லக்னத்தில் பிறந்த நீங்கள் குருவின் ஆசியால் கருணை ததும்பும் கண்களும், மென்மையான இதயமும், தெய்வீக பக்தியும் கொண்டவர்கள். கலை, சங்கீதம், தியானம், ஆன்மீகத்தில் ஈடுபாடும், மற்றவர்களின் துயர் துடைக்கும் நல்லெண்ணமும் உண்டு.'
    }
}

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


def _ordinal(n):
    return f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


def _house_list(houses, lang):
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


# 3. 12 Bhavas (House-by-House) Detailed Predictions Engine
def generate_bhava_predictions(house_details, planets, lang='en', bhava_bala=None):
    predictions = []
    bhava_titles = [
        ('1st House (Tanu / Self)', 'முதலாம் பாவம் (தனு / லக்ன பாவம்)', 'Physical vitality, temperament, self-realization, and life path.'),
        ('2nd House (Dhana / Wealth)', 'இரண்டாம் பாவம் (தன / வாக்கு பாவம்)', 'Financial reserves, family roots, speech persuasiveness, and vision.'),
        ('3rd House (Sahaja / Courage)', 'மூன்றாம் பாவம் (சகஜ / தைரிய பாவம்)', 'Enterprise, younger siblings, communications, writing, short travels.'),
        ('4th House (Sukha / Domestic)', 'நான்காம் பாவம் (சுக / மாத்ரு பாவம்)', 'Motherly bond, real estate, vehicles, education, and emotional peace.'),
        ('5th House (Putra / Progeny)', 'ஐந்தாம் பாவம் (புத்திர / பூர்வ புண்ணிய பாவம்)', 'Intelligence, children, creative wisdom, intuition, and speculative gains.'),
        ('6th House (Ari / Health & Debts)', 'ஆறாம் பாவம் (ருண / ரோக / சத்ரு பாவம்)', 'Resistance to illness, triumph over rivals, employment service, and litigations.'),
        ('7th House (Kalatra / Marriage)', 'ஏழாம் பாவம் (களத்திர / திருமண பாவம்)', 'Marriage partner, conjugal harmony, business alliances, and public charisma.'),
        ('8th House (Ayur / Longevity)', 'எட்டாம் பாவம் (ஆயுள் / மரண பாவம்)', 'Lifespan vitality, sudden transformations, occult insight, and inheritances.'),
        ('9th House (Bhagya / Fortune)', 'ஒன்பதாம் பாவம் (பாக்கிய / தர்ம பாவம்)', 'Higher wisdom, father, pilgrimages, divine fortune, and dharmic merit.'),
        ('10th House (Karma / Career)', 'பத்தாம் பாவம் (கர்ம / ஜீவன பாவம்)', 'Professional calling, executive authority, social reputation, and public status.'),
        ('11th House (Labha / Gains)', 'பதினொன்றாம் பாவம் (லாப பாவம்)', 'Accumulation of profits, realization of ambitions, elder siblings, and allies.'),
        ('12th House (Vyaya / Liberation)', 'பன்னிரண்டாம் பாவம் (விரய / மோட்ச பாவம்)', 'Spiritual liberation, expenditures, foreign travels, and dream subconscious.')
    ]

    for h_info in house_details:
        h_num = h_info['house']
        title_en, title_ta, _ = bhava_titles[h_num - 1]
        lord = h_info['lord']
        lord_data = planets.get(lord, {})
        lord_house = lord_data.get('house', h_num)
        lord_dignity = lord_data.get('dignity', 'Neutral')
        occupants = [o for o in h_info['occupants'] if o in PLANET_TAMIL and o != 'Ascendant']
        aspected_by = h_info['aspected_by']
        sav = h_info['sav_points']
        themes_en, themes_ta = HOUSE_THEMES[h_num]
        lord_themes_en, lord_themes_ta = HOUSE_THEMES[lord_house]
        lord_ta = PLANET_TAMIL.get(lord, lord)

        # Each factor: (English, Tamil, effect on the house)
        factors = []
        dig_en, dig_ta = DIGNITY_PHRASE.get(lord_dignity, DIGNITY_PHRASE['Neutral'])
        dig_score = DIGNITY_SCORE.get(lord_dignity, 0)
        factors.append((f"Lord {lord} is in {dig_en}", f"அதிபதி {lord_ta} {dig_ta} உள்ளார்", dig_score))
        if lord_house in DUSTHANAS:
            if h_num in DUSTHANAS:
                factors.append((f"A dusthana lord hidden in the {_ordinal(lord_house)} house weakens this house's troubles (Vipareeta)",
                                f"மறைவு ஸ்தான அதிபதி {lord_house}-ம் பாவத்தில் மறைந்ததால் இப்பாவத்தின் தீமைகள் குறையும் (விபரீதம்)", 1))
            else:
                factors.append((f"Lord placed in the {_ordinal(lord_house)} house, a dusthana",
                                f"அதிபதி {lord_house}-ம் பாவம் எனும் மறைவு ஸ்தானத்தில்", -1))
        elif lord_house in KENDRAS + TRIKONAS:
            factors.append((f"Lord well placed in the {_ordinal(lord_house)} house (kendra/trikona)",
                            f"அதிபதி {lord_house}-ம் பாவம் எனும் கேந்திர/திரிகோண ஸ்தானத்தில்", 1))
        if lord_data.get('combust'):
            factors.append((f"Lord {lord} is combust", f"அதிபதி {lord_ta} அஸ்தங்கம்", -1))
        for occ in occupants:
            occ_ta = PLANET_TAMIL[occ]
            if occ in NATURAL_BENEFICS:
                if h_num in DUSTHANAS:
                    factors.append((f"Benefic {occ} here spends its goodness on {themes_en}",
                                    f"சுபர் {occ_ta} இங்கு இருப்பதால் நற்பலன் குறைவாகவே கிடைக்கும்", 0))
                else:
                    factors.append((f"Benefic {occ} occupies the house", f"சுபர் {occ_ta} இப்பாவத்தில் உள்ளார்", 1))
            elif h_num in UPACHAYAS:
                factors.append((f"Malefic {occ} thrives in this upachaya house", f"பாவர் {occ_ta} உபசய ஸ்தானத்தில் வலுப்பெறுகிறார்", 1))
            else:
                factors.append((f"Malefic {occ} occupies the house", f"பாவர் {occ_ta} இப்பாவத்தில் உள்ளார்", -1))
        if 'Jupiter' in aspected_by:
            factors.append(("Jupiter's aspect protects the house", 'குருவின் பார்வை இப்பாவத்தைக் காக்கிறது', 1))
        for mal in ('Saturn', 'Mars'):
            if mal in aspected_by and h_num not in UPACHAYAS:
                factors.append((f"{mal}'s aspect brings pressure and delays", f"{PLANET_TAMIL[mal]} பார்வை தடைகளையும் அழுத்தத்தையும் தரும்", -1))
        rupas = round(bhava_bala[h_num - 1]['rupas'], 2) if bhava_bala else None
        if rupas is not None and rupas >= 9:
            factors.append((f"Bhava Bala of {rupas} rupas, well above the minimum of 7",
                            f"பாவ பலம் {rupas} ரூபம், குறைந்தபட்ச அளவான 7-ஐ விட நன்கு அதிகம்", 1))
        elif rupas is not None and rupas < 7:
            factors.append((f"Bhava Bala of only {rupas} rupas, below the minimum of 7",
                            f"பாவ பலம் {rupas} ரூபம் மட்டுமே, குறைந்தபட்ச அளவான 7-க்குக் கீழ்", -1))
        if sav >= 30:
            factors.append((f"{sav} Ashtakavarga bindus, above the average of 28", f"{sav} அஷ்டகவர்க்கப் பரல்கள் (சராசரி 28-க்கு மேல்)", 1))
        elif sav < 25:
            factors.append((f"Only {sav} Ashtakavarga bindus, below the average of 28", f"{sav} அஷ்டகவர்க்கப் பரல்கள் மட்டுமே (சராசரி 28-க்குக் கீழ்)", -1))

        score = sum(f[2] for f in factors)
        verdict = _verdict(score)
        occ_en = ', '.join(occupants) if occupants else ''
        occ_ta = ', '.join(PLANET_TAMIL[o] for o in occupants)

        if verdict == 'strong':
            close_en = f"Overall this is a strong house: {themes_en} flourish with steady support."
            close_ta = f"மொத்தத்தில் இது பலம் வாய்ந்த பாவம்: {themes_ta} ஆகியவை சிறப்பாக அமையும்."
        elif verdict == 'weak':
            close_en = f"Overall this house needs care: {themes_en} may meet delays, and strengthening {lord} through its remedies helps."
            close_ta = f"மொத்தத்தில் இப்பாவம் கவனம் தேவைப்படுவது: {themes_ta} ஆகியவற்றில் தாமதங்கள் வரலாம்; {lord_ta} கிரகத்திற்கான பரிகாரங்கள் நலம் தரும்."
        else:
            close_en = f"Overall a moderate house: {themes_en} give mixed results that improve with effort."
            close_ta = f"மொத்தத்தில் மத்திமமான பாவம்: {themes_ta} ஆகியவை முயற்சிக்கேற்ப மேம்படும்."

        pred_en = (
            f"The {_ordinal(h_num)} house of {themes_en} rises in {h_info['sign']}. Its lord {lord} sits in the "
            f"{_ordinal(lord_house)} house in {dig_en}"
            + (', combust' if lord_data.get('combust') else '')
            + (', retrograde' if lord_data.get('retrograde') and lord not in ('Rahu', 'Ketu') else '')
            + (f", so these matters are tied to {lord_themes_en}. " if lord_house != h_num else ', guarding its own house. ')
            + (f"{occ_en} {'occupies' if len(occupants) == 1 else 'occupy'} the house. " if occupants
               else "No planet occupies it, so the lord's condition decides the results. ")
            + f"It holds {sav} Ashtakavarga bindus. {close_en}"
        )
        lord_state_ta = ('அஸ்தங்கம் பெற்று ' if lord_data.get('combust') else '') + \
            ('வக்ரம் பெற்று ' if lord_data.get('retrograde') and lord not in ('Rahu', 'Ketu') else '')
        pred_ta = (
            f"{themes_ta} ஆகியவற்றைக் குறிக்கும் {h_num}-ம் பாவம் {h_info['tamil']} ராசியில் அமைகிறது. இதன் அதிபதி {lord_ta} "
            f"{lord_state_ta}{lord_house}-ம் பாவத்தில் {dig_ta} உள்ளார்"
            + (f"; எனவே இப்பலன்கள் {lord_themes_ta} ஆகியவற்றுடன் இணைகின்றன. " if lord_house != h_num else '; தன் பாவத்தையே காக்கிறார். ')
            + (f"இப்பாவத்தில் {occ_ta} உள்ளனர். " if len(occupants) > 1 else (f"இப்பாவத்தில் {occ_ta} உள்ளார். " if occupants
               else 'இப்பாவத்தில் கிரகங்கள் இல்லை; அதிபதியின் நிலையே பலனைத் தீர்மானிக்கும். '))
            + f"இதற்கு {sav} அஷ்டகவர்க்கப் பரல்கள் உள்ளன. {close_ta}"
        )

        predictions.append({
            'house': h_num,
            'title_en': title_en,
            'title_ta': title_ta,
            'sign': h_info['sign'],
            'tamil_sign': h_info['tamil'],
            'lord': lord,
            'lord_house': lord_house,
            'lord_dignity': lord_dignity,
            'sav_points': sav,
            'bhava_bala_rupas': rupas,
            'occupants': occupants,
            'aspected_by': aspected_by,
            'strength': verdict,
            'strength_ta': VERDICT_TAMIL[verdict],
            'score': score,
            'factors': [{'en': en, 'ta': ta, 'effect': effect} for en, ta, effect in factors],
            'prediction_en': pred_en,
            'prediction_ta': pred_ta
        })

    return predictions

# 4. Planets in Houses Predictions (Sun to Ketu in 12 Houses)
def generate_planet_house_predictions(planets):
    planet_insights = []
    p_roles = {
        'Sun': ('Soul, Vitality, Authority', 'ஆன்ம பலம், தந்தை, அரசாங்கம்'),
        'Moon': ('Mind, Emotions, Mental Peace', 'மனம், தாயன்பு, கற்பனை'),
        'Mars': ('Courage, Vital Force, Property', 'தைரியம், பூமி, வீரம்'),
        'Mercury': ('Intellect, Commerce, Eloquence', 'அறிவு, கல்வி, வணிகம்'),
        'Jupiter': ('Wisdom, Fortune, Progeny', 'ஞானம், செல்வம், புத்திர பாக்கியம்'),
        'Venus': ('Art, Luxuries, Marriage Bliss', 'கலை, செல்வம், தாம்பத்திய சுகம்'),
        'Saturn': ('Discipline, Longevity, Career', 'ஆயுள், உழைப்பு, நீதி'),
        'Rahu': ('Ambition, Foreign Links, Modern Fields', 'போக காரகன், வெளிநாட்டு யோகம்'),
        'Ketu': ('Intuition, Liberation, Spiritual Wisdom', 'மோட்ச காரகன், ஞானம், ஆன்மீகம்')
    }

    asc_sign = planets['Ascendant']['sign_index']
    role_phrases = {
        'yogakaraka': ('a Yogakaraka for this Lagna, ruling both a kendra and a trikona, so it is one of the most beneficial planets in the chart',
                       'இந்த லக்னத்திற்கு யோககாரகன்; கேந்திரமும் திரிகோணமும் ஆள்வதால் ஜாதகத்தின் மிகச் சிறந்த கிரகங்களில் ஒன்று'),
        'benefic': ('a functional benefic for this Lagna', 'இந்த லக்னத்திற்குச் சுப பலன் தரும் கிரகம்'),
        'malefic': ('a functional malefic for this Lagna, as it rules a dusthana', 'மறைவு ஸ்தானம் ஆள்வதால் இந்த லக்னத்திற்குப் பாவ பலன் தரும் கிரகம்'),
        'neutral': ('functionally neutral for this Lagna', 'இந்த லக்னத்திற்குச் சம பலன் தரும் கிரகம்')
    }

    for p_name, (role_en, role_ta) in p_roles.items():
        p_data = planets.get(p_name)
        if not p_data: continue
        h = p_data['house']
        sign = p_data['sign']
        tamil_sign = p_data['tamil']
        dignity = p_data.get('dignity', 'Neutral')
        retro = p_data.get('retrograde', False) and p_name not in ('Rahu', 'Ketu')
        combust = p_data.get('combust', False)
        name_ta = PLANET_TAMIL[p_name]
        themes_en, themes_ta = HOUSE_THEMES[h]
        dig_en, dig_ta = DIGNITY_PHRASE.get(dignity, DIGNITY_PHRASE['Neutral'])
        is_benefic = p_name in NATURAL_BENEFICS

        score = DIGNITY_SCORE.get(dignity, 0)
        notes_en, notes_ta = [], []
        if is_benefic:
            if h in DUSTHANAS:
                score -= 1
                notes_en.append(f"As a natural benefic in the {_ordinal(h)} house, a dusthana, its kindness is spent on struggles and expenses.")
                notes_ta.append(f"இயற்கைச் சுபர் {h}-ம் பாவம் எனும் மறைவு ஸ்தானத்தில் இருப்பதால் அதன் நற்பலன் போராட்டங்களிலும் செலவுகளிலும் கரைகிறது.")
            elif h in KENDRAS + TRIKONAS:
                score += 1
                notes_en.append(f"A natural benefic in a kendra or trikona is one of the best placements, uplifting {themes_en}.")
                notes_ta.append(f"இயற்கைச் சுபர் கேந்திர/திரிகோணத்தில் இருப்பது சிறந்த அமைப்பு; {themes_ta} மேன்மை பெறும்.")
        elif h in UPACHAYAS:
            score += 1
            notes_en.append(f"Natural malefics do well in upachaya houses; it builds strength and wins over {themes_en} with time.")
            notes_ta.append(f"பாவ கிரகங்கள் உபசய ஸ்தானத்தில் வலுப்பெறும்; காலப்போக்கில் {themes_ta} ஆகியவற்றில் வெற்றி தரும்.")
        elif h in (1, 4, 5, 7, 9) and DIGNITY_SCORE.get(dignity, 0) < 2:
            score -= 1
            notes_en.append(f"As a natural malefic here it can strain {themes_en}, calling for patience.")
            notes_ta.append(f"இங்குள்ள பாவ கிரகம் {themes_ta} ஆகியவற்றில் சிரமம் தரலாம்; பொறுமை தேவை.")
        if DIG_BALA_HOUSE.get(p_name) == h:
            score += 1
            notes_en.append("It enjoys directional strength (Dig Bala) in this house.")
            notes_ta.append("இப்பாவத்தில் திக் பலம் பெறுகிறது.")
        if combust:
            score -= 1
            notes_en.append("Being combust, close to the Sun, its independent results are weakened.")
            notes_ta.append("சூரியனுக்கு அருகில் அஸ்தங்கம் பெற்றதால் தனித்த பலன்கள் குறையும்.")
        if retro:
            notes_en.append("Retrograde motion turns its energy inward: results come after reflection and second attempts.")
            notes_ta.append("வக்ர கதியால் அதன் சக்தி உள்நோக்கித் திரும்பும்; மறுமுயற்சிக்குப் பின் பலன் கிடைக்கும்.")
        if 'Jupiter' in p_data.get('aspects_received', []) and p_name != 'Jupiter':
            score += 1
            notes_en.append("Jupiter's aspect adds protection and wisdom.")
            notes_ta.append("குருவின் பார்வை பாதுகாப்பையும் ஞானத்தையும் சேர்க்கிறது.")

        role, owned = _functional_role(p_name, asc_sign)
        if owned:
            owned_themes_en = '; '.join(HOUSE_THEMES[o][0] for o in owned)
            owned_themes_ta = '; '.join(HOUSE_THEMES[o][1] for o in owned)
            rp_en, rp_ta = role_phrases[role]
            lord_en = (f"As lord of the {_house_list(owned, 'en')} ({owned_themes_en}), it is {rp_en}; "
                       f"it carries those matters into {themes_en}.")
            lord_ta = (f"{_house_list(owned, 'ta')} ({owned_themes_ta}) அதிபதியாக இது {rp_ta}; "
                       f"அவ்விஷயங்களை {themes_ta} ஆகியவற்றுடன் இணைக்கிறது.")
            score += {'yogakaraka': 1, 'benefic': 1, 'malefic': 0, 'neutral': 0}[role]
        else:
            dispositor = SIGN_LORDS[p_data['sign_index']]
            lord_en = f"As a shadow planet it acts through its sign lord {dispositor}, amplifying {themes_en}."
            lord_ta = f"சாயா கிரகமான இது தன் ராசி அதிபதி {PLANET_TAMIL[dispositor]} மூலம் செயல்பட்டு {themes_ta} ஆகியவற்றைத் தீவிரப்படுத்தும்."

        verdict = _verdict(score)
        if verdict == 'strong':
            close_en = "Expect its significations to deliver well, especially during its dasa and bhukti."
            close_ta = "இதன் காரகத்துவங்கள் சிறப்பாகப் பலன் தரும்; குறிப்பாக இதன் தசை, புக்தி காலங்களில்."
        elif verdict == 'weak':
            close_en = "Its results come through effort; its dasa or bhukti calls for patience and its remedies."
            close_ta = "இதன் பலன்கள் முயற்சியால் கிடைக்கும்; இதன் தசை அல்லது புக்தியில் பொறுமையும் பரிகாரமும் தேவை."
        else:
            close_en = "Its results are mixed and grow steadily with conscious effort."
            close_ta = "இதன் பலன்கள் கலவையானவை; முயற்சியுடன் படிப்படியாக வளரும்."

        pred_en = (
            f"{p_name}, significator of {role_en.lower()}, occupies the {_ordinal(h)} house of {themes_en} in {sign}, in {dig_en}. "
            f"{lord_en} {' '.join(notes_en)} {close_en}"
        ).replace('  ', ' ')
        pred_ta = (
            f"{role_ta} ஆகியவற்றின் காரகனான {name_ta}, {themes_ta} ஆகியவற்றைக் குறிக்கும் {h}-ம் பாவத்தில் {tamil_sign} ராசியில் {dig_ta} அமர்ந்துள்ளார். "
            f"{lord_ta} {' '.join(notes_ta)} {close_ta}"
        ).replace('  ', ' ')

        planet_insights.append({
            'planet': p_name,
            'house': h,
            'sign': sign,
            'tamil_sign': tamil_sign,
            'dignity': dignity,
            'retrograde': retro,
            'combust': combust,
            'owned_houses': owned,
            'functional_role': role,
            'strength': verdict,
            'strength_ta': VERDICT_TAMIL[verdict],
            'score': score,
            'prediction_en': pred_en,
            'prediction_ta': pred_ta
        })

    return planet_insights

# 5. Dasa-Bhukti Comprehensive Forecast
def generate_dasa_forecast(active_dasa, dasha_rows, planets, tz_name='UTC'):
    maha_general = {
        'Sun': {
            'en': 'Sun (Surya) Maha Dasa (6 Years): Fosters government recognition, leadership promotion, fatherly connections, and inner vitality. Maintain ego balance.',
            'ta': 'சூரிய மகா தசை (6 ஆண்டுகள்): அரசு வழி நன்மைகள், தலைமைப் பதவிகள், தந்தையின் ஆதரவு, ஆன்ம பலம் மேலோங்கும். அகந்தையைத் தவிர்ப்பது நல்லது.'
        },
        'Moon': {
            'en': 'Moon (Chandra) Maha Dasa (10 Years): Cultivates public popularity, emotional fulfillment, travel, water/commercial trade, and domestic comfort.',
            'ta': 'சந்திர மகா தசை (10 ஆண்டுகள்): மன அமைதி, மக்கள் செல்வாக்கு, தாயன்பு, வியாபார லாபம், தூர தேசப் பயணங்கள் சிறப்பாக அமையும்.'
        },
        'Mars': {
            'en': 'Mars (Chevvai) Maha Dasa (7 Years): Ignites bold courage, real estate acquisitions, athletic vitality, technical achievements, and decisive leadership.',
            'ta': 'செவ்வாய் மகா தசை (7 ஆண்டுகள்): பூமி, நிலம், வீடு வாங்கும் யோகம், புதிய முயற்சிகளில் வெற்றி, தைரியம் மேலோங்கும்.'
        },
        'Rahu': {
            'en': 'Rahu Maha Dasa (18 Years): Unleashes rapid worldly ambition, technological breakthroughs, foreign travels, unconventional expansion, and sudden windfalls.',
            'ta': 'ராகு மகா தசை (18 ஆண்டுகள்): வெளிநாட்டு யோகம், திடீர் பண வரவு, புதிய தொழில் முயற்சிகள், நவீன துறைகளில் அசுர வளர்ச்சி கிட்டும்.'
        },
        'Jupiter': {
            'en': 'Jupiter (Guru) Maha Dasa (16 Years): Golden era of wisdom, progeny birth, wealth expansion, spiritual pilgrimage, social honor, and benevolent guidance.',
            'ta': 'குரு மகா தசை (16 ஆண்டுகள்): பொற்காலம். புத்திர பாக்கியம், தர்ம சிந்தனை, கல்வி, செல்வம், சமுதாயத்தில் உயர்ந்த மரியாதை கிட்டும்.'
        },
        'Saturn': {
            'en': 'Saturn (Sani) Maha Dasa (19 Years): Rewards enduring perseverance, builds stable empire through discipline, brings philosophical maturity and justice.',
            'ta': 'சனி மகா தசை (19 ஆண்டுகள்): கடின உழைப்பிற்கு ஏற்ற நிலையான சொத்துக்கள், பக்குவமான சிந்தனை, நீண்ட ஆயுள் நற்பலன்கள் அமையும்.'
        },
        'Mercury': {
            'en': 'Mercury (Budha) Maha Dasa (17 Years): Sharpened intellect, profitable commerce, academic excellence, publishing/writing success, and diplomatic triumph.',
            'ta': 'புதன் மகா தசை (17 ஆண்டுகள்): கல்வி மேன்மை, வியாபார வளர்ச்சி, சிறந்த பேச்சாற்றல், கணக்கு மற்றும் தகவல் தொடர்புத் துறையில் உச்சம்.'
        },
        'Ketu': {
            'en': 'Ketu Maha Dasa (7 Years): Spiritual awakening, liberation, intuitive breakthroughs, occult interest, and shedding of unnecessary material burdens.',
            'ta': 'கேது மகா தசை (7 ஆண்டுகள்): ஞானம், ஆன்மீக ஈடுபாடு, தியானம், மன அமைதி மற்றும் எதிர்பாராத நன்மைகள் உண்டாகும்.'
        },
        'Venus': {
            'en': 'Venus (Sukra) Maha Dasa (20 Years): Sumptuous luxury, artistic mastery, marital joy, acquisition of vehicles/gems, and harmonious domestic bliss.',
            'ta': 'சுக்கிர மகா தசை (20 ஆண்டுகள்): சகல சௌபாக்கியங்கள், ஆடை ஆபரண சேர்க்கை, வாகன வசதி, குடும்பத்தில் சுப காரியங்கள் சிறப்பாக நடக்கும்.'
        }
    }

    active_reading_en = "Active Dasa calculation in progress."
    active_reading_ta = "தசா கணக்கீடு நடைபெறுகிறது."

    if active_dasa:
        d = active_dasa['dasa']
        b = active_dasa['bhukti']
        p = active_dasa['pratyantar']
        asc_sign = planets['Ascendant']['sign_index']

        def lord_profile(name):
            data = planets[name]
            owned = _owned_houses(name, asc_sign)
            dig_en, dig_ta = DIGNITY_PHRASE.get(data.get('dignity', 'Neutral'), DIGNITY_PHRASE['Neutral'])
            themes = sorted(set(owned + [data['house']]))
            en = (f"{name} rules the {_house_list(owned, 'en')} and sits in the {_ordinal(data['house'])} house in {dig_en}"
                  if owned else f"{name} sits in the {_ordinal(data['house'])} house in {dig_en}")
            ta = (f"{PLANET_TAMIL[name]} {_house_list(owned, 'ta')} அதிபதியாக {data['house']}-ம் பாவத்தில் {dig_ta} உள்ளார்"
                  if owned else f"{PLANET_TAMIL[name]} {data['house']}-ம் பாவத்தில் {dig_ta} உள்ளார்")
            return en, ta, '; '.join(HOUSE_THEMES[h][0] for h in themes), '; '.join(HOUSE_THEMES[h][1] for h in themes), DIGNITY_SCORE.get(data.get('dignity', 'Neutral'), 0)

        d_en, d_ta, d_themes_en, d_themes_ta, d_score = lord_profile(d)
        b_en, b_ta, b_themes_en, b_themes_ta, b_score = lord_profile(b)
        # Position of the Bhukti lord counted from the Dasa lord
        rel = (planets[b]['sign_index'] - planets[d]['sign_index']) % 12 + 1
        if rel == 1:
            rel_en, rel_ta = 'conjoined in the same sign, blending their results closely', 'ஒரே ராசியில் இணைந்திருப்பதால் இருவரின் பலன்களும் நெருக்கமாகக் கலக்கும்'
        elif rel in (5, 9):
            rel_en, rel_ta = 'in trine to each other, so the period flows harmoniously', 'ஒருவருக்கொருவர் திரிகோணத்தில் இருப்பதால் இக்காலம் இணக்கமாக நகரும்'
        elif rel in (4, 7, 10):
            rel_en, rel_ta = 'in kendra to each other, bringing activity and visible change', 'ஒருவருக்கொருவர் கேந்திரத்தில் இருப்பதால் செயல்பாடும் வெளிப்படையான மாற்றங்களும் வரும்'
        elif rel in (3, 11):
            rel_en, rel_ta = 'in the 3-11 relationship, which favours effort and gains', '3-11 நிலையில் இருப்பதால் முயற்சிக்கு ஏற்ற லாபம் கிடைக்கும்'
        else:
            rel_en, rel_ta = ('in the 2-12 or 6-8 relationship, which can bring friction; steady, careful decisions help',
                              '2-12 அல்லது 6-8 நிலையில் இருப்பதால் சில உரசல்கள் வரலாம்; நிதானமான முடிவுகள் நலம் தரும்')
        tone = d_score + b_score
        if tone >= 2:
            tone_en, tone_ta = 'Both lords are well placed, so this is a productive period.', 'இரு அதிபதிகளும் நல்ல நிலையில் உள்ளதால் இது பலன் தரும் காலம்.'
        elif tone <= -2:
            tone_en, tone_ta = 'The lords are under strain, so progress needs patience and remedies.', 'அதிபதிகள் பலவீனமாக உள்ளதால் முன்னேற்றத்திற்குப் பொறுமையும் பரிகாரமும் தேவை.'
        else:
            tone_en, tone_ta = 'The period gives mixed results that respond well to effort.', 'இக்காலம் கலவையான பலன்களைத் தரும்; முயற்சிக்கு நல்ல பலன் உண்டு.'
        until = datetime.fromisoformat(active_dasa['bhukti_end']).astimezone(ZoneInfo(tz_name)).date().isoformat()

        if d == b:  # the Maha Dasa's own bhukti
            bhukti_en = f"In its own bhukti {d} gives these results in their purest form."
            bhukti_ta = f"சுய புக்தியில் {PLANET_TAMIL[d]} இப்பலன்களை முழுமையாக வழங்குவார்."
        else:
            bhukti_en = f"{b_en}, bringing {b_themes_en} to the foreground now. The two lords are {rel_en}."
            bhukti_ta = f"{b_ta}; இப்போது {b_themes_ta} முன்னிலை பெறும். இரு அதிபதிகளும் {rel_ta}."

        active_reading_en = (
            f"You are running {d} Maha Dasa, {b} Bhukti and {p} Pratyantardasa; this bhukti lasts until {until}. "
            f"{d_en}, so the Maha Dasa centres on {d_themes_en}. {bhukti_en} {tone_en} {maha_general.get(d, {}).get('en', '')}"
        )
        active_reading_ta = (
            f"தற்போது {PLANET_TAMIL[d]} மகா தசையில் {PLANET_TAMIL[b]} புக்தி, {PLANET_TAMIL[p]} அந்தரம் நடைபெறுகிறது; இப்புக்தி {until} வரை நீடிக்கும். "
            f"{d_ta}; எனவே இந்த மகா தசை {d_themes_ta} ஆகியவற்றை மையமாகக் கொண்டது. {bhukti_ta} {tone_ta} {maha_general.get(d, {}).get('ta', '')}"
        )

    return {
        'active_period': active_dasa,
        'active_forecast_en': active_reading_en,
        'active_forecast_ta': active_reading_ta,
        'all_dasas': maha_general
    }

# 6. Gochara (Transit) Predictions (Saturn, Jupiter, Rahu-Ketu)
def generate_transit_forecast(moon_sign_idx, gochara):
    # Sade Sati occurs when Saturn is in 12th, 1st, 2nd from Janma Rasi
    # Ashtama Sani is 8th from Janma Rasi; Kantaka Sani is 4th, 7th, 10th
    transit = gochara['planets']
    saturn_diff = (transit['Saturn']['sign_index'] - moon_sign_idx) % 12 + 1
    jupiter_diff = (transit['Jupiter']['sign_index'] - moon_sign_idx) % 12 + 1
    rahu_diff = (transit['Rahu']['sign_index'] - moon_sign_idx) % 12 + 1
    ketu_diff = (transit['Ketu']['sign_index'] - moon_sign_idx) % 12 + 1

    # Sade Sati check
    is_sade_sati = saturn_diff in (12, 1, 2)
    is_ashtama = saturn_diff == 8
    is_ardhashtama = saturn_diff == 4

    saturn_title_en = "Favorable Saturn Transit"
    saturn_title_ta = "அனுகூலமான சனிப் பெயர்ச்சி"
    if is_sade_sati:
        saturn_title_en = f"Sade Sati (ஏழரை சனி - Phase {1 if saturn_diff == 12 else (2 if saturn_diff == 1 else 3)})"
        saturn_title_ta = f"ஏழரை நாட்டுச் சனி (கட்டம் {1 if saturn_diff == 12 else (2 if saturn_diff == 1 else 3)})"
    elif is_ashtama:
        saturn_title_en = "Ashtama Sani (8th House Saturn Transit)"
        saturn_title_ta = "அஷ்டமத்துச் சனி (8-ஆம் இடத்துச் சனி)"
    elif is_ardhashtama:
        saturn_title_en = "Ardhashtama Sani (4th House Saturn Transit)"
        saturn_title_ta = "அர்த்தாஷ்டமச் சனி (4-ஆம் இடத்துச் சனி)"

    saturn_pred_en = (
        f"Saturn currently transits House {saturn_diff} from your Moon sign. "
        f"{'This marks the transformative period of Sade Sati; focus on disciplined labor, patience, and humility.' if is_sade_sati else ''}"
        f"{'This is Ashtama Sani; drive carefully, maintain health routines, and avoid speculative risks.' if is_ashtama else ''}"
        f"{'This is Ardhashtama Sani; domestic matters, property and mother’s health need patient attention.' if is_ardhashtama else ''}"
        f"{'Saturn in an auspicious house brings career stability, solid professional foundations, and sustained growth.' if not (is_sade_sati or is_ashtama or is_ardhashtama) else ''}"
    )

    saturn_pred_ta = (
        f"சனி பகவான் உங்கள் சந்திர ராசிக்கு {saturn_diff}-ஆம் இடத்தில் சஞ்சரிக்கிறார். "
        f"{'இது ஏழரை நாட்டுச் சனியின் காலமாகும்; விவேகமும், பொறுமையும், கடுமையான உழைப்பும் உங்களை உயர்த்தும்.' if is_sade_sati else ''}"
        f"{'இது அஷ்டமத்துச் சனியாகும்; பயணங்களில் கவனமும், ஆரோக்கிய பராமரிப்பும், தர்ம சிந்தனையும் நலம் தரும்.' if is_ashtama else ''}"
        f"{'இது அர்த்தாஷ்டமச் சனியாகும்; வீடு, சொத்து, தாயாரின் உடல்நலம் ஆகியவற்றில் பொறுமையான கவனம் தேவை.' if is_ardhashtama else ''}"
        f"{'சனி பகவான் அனுகூலமான இடத்தில் சஞ்சரிப்பதால் தொழில் வளர்ச்சி, பண வரவு, நிலையான முன்னேற்றம் கிட்டும்.' if not (is_sade_sati or is_ashtama or is_ardhashtama) else ''}"
    )

    # Jupiter Transit check
    is_guru_favorable = jupiter_diff in (2, 5, 7, 9, 11)
    jupiter_pred_en = (
        f"Jupiter transits House {jupiter_diff} from your Moon sign. "
        f"{'Guru is highly auspicious (Guru Bala); brings financial prosperity, auspicious celebrations, and divine luck.' if is_guru_favorable else 'Guru prompts introspection, learning, and steady preparation for upcoming expansions.'}"
    )
    jupiter_pred_ta = (
        f"குரு பகவான் உங்கள் சந்திர ராசிக்கு {jupiter_diff}-ஆம் இடத்தில் சஞ்சரிக்கிறார். "
        f"{'குரு பலம் சிறப்பாக உள்ளது; தன லாபம், சுப காரியங்கள், மங்கல நிகழ்வுகள், ஆன்மீக அருள் பூரணமாகக் கிட்டும்.' if is_guru_favorable else 'குருவின் சஞ்சாரம் புதிய திட்டங்களுக்கு அடித்தளம் அமைக்கும் காலமாகும்.'}"
    )

    # Rahu-Ketu: favourable in the 3rd, 6th and 11th from the Moon
    rk_favorable = rahu_diff in (3, 6, 11) or ketu_diff in (3, 6, 11)
    rahu_ketu_pred_en = (
        f"Rahu transits House {rahu_diff} and Ketu House {ketu_diff} from your Moon sign. "
        f"{'The nodes support courage, victory over rivals and unexpected gains.' if rk_favorable else 'The nodes ask for caution with new ventures, health and hasty decisions.'}"
    )
    rahu_ketu_pred_ta = (
        f"ராகு உங்கள் சந்திர ராசிக்கு {rahu_diff}-ஆம் இடத்திலும், கேது {ketu_diff}-ஆம் இடத்திலும் சஞ்சரிக்கின்றனர். "
        f"{'துணிவு, எதிரிகளை வெல்லும் திறன், எதிர்பாராத லாபம் கிட்டும்.' if rk_favorable else 'புதிய முயற்சிகள், உடல்நலம், அவசர முடிவுகளில் கவனம் தேவை.'}"
    )

    return {
        'saturn': {
            'house_from_moon': saturn_diff,
            'sign': transit['Saturn']['sign'],
            'tamil_sign': transit['Saturn']['tamil'],
            'title_en': saturn_title_en,
            'title_ta': saturn_title_ta,
            'prediction_en': saturn_pred_en,
            'prediction_ta': saturn_pred_ta
        },
        'jupiter': {
            'house_from_moon': jupiter_diff,
            'sign': transit['Jupiter']['sign'],
            'tamil_sign': transit['Jupiter']['tamil'],
            'favorable': is_guru_favorable,
            'prediction_en': jupiter_pred_en,
            'prediction_ta': jupiter_pred_ta
        },
        'rahu_ketu': {
            'rahu_house_from_moon': rahu_diff,
            'ketu_house_from_moon': ketu_diff,
            'favorable': rk_favorable,
            'prediction_en': rahu_ketu_pred_en,
            'prediction_ta': rahu_ketu_pred_ta
        },
        'peyarchi': gochara.get('peyarchi', [])
    }

# 7. Lucky Factors & Gemstones
LUCKY_TAMIL = {
    'Sunday': 'ஞாயிறு', 'Monday': 'திங்கள்', 'Tuesday': 'செவ்வாய்', 'Wednesday': 'புதன்',
    'Thursday': 'வியாழன்', 'Friday': 'வெள்ளி', 'Saturday': 'சனி',
    'Gold': 'தங்கம்', 'Copper': 'செம்பு', 'Platinum': 'பிளாட்டினம்', 'Silver': 'வெள்ளி', 'Iron': 'இரும்பு',
    'Bright Red': 'பிரகாசமான சிவப்பு', 'Crimson': 'அடர் சிவப்பு', 'Golden Yellow': 'பொன் மஞ்சள்',
    'Diamond White': 'வைர வெண்மை', 'Pale Pink': 'வெளிர் இளஞ்சிவப்பு', 'Cream': 'இளம் மஞ்சள்',
    'Emerald Green': 'மரகதப் பச்சை', 'Pastel Shades': 'மென்மையான வண்ணங்கள்', 'Pearl White': 'முத்து வெண்மை',
    'Deep Gold': 'அடர் பொன்னிறம்', 'Orange': 'ஆரஞ்சு', 'Ruby Red': 'மாணிக்கச் சிவப்பு',
    'Parrot Green': 'கிளிப் பச்சை', 'Turquoise': 'நீலப் பச்சை', 'Pure White': 'தூய வெண்மை',
    'Rose Pink': 'ரோஜா நிறம்', 'Silk Blue': 'பட்டு நீலம்', 'Scarlet Red': 'செஞ்சிவப்பு', 'Rust': 'துரு நிறம்',
    'Amber': 'அம்பர் மஞ்சள்', 'Bright Yellow': 'பிரகாசமான மஞ்சள்', 'Saffron': 'காவி',
    'Royal Blue': 'அரச நீலம்', 'Navy': 'கடற்படை நீலம்', 'Steel Grey': 'எஃகு சாம்பல்',
    'Electric Blue': 'மின் நீலம்', 'Violet': 'ஊதா', 'Indigo': 'கருநீலம்', 'Pale Yellow': 'வெளிர் மஞ்சள்',
    'Golden Amber': 'பொன் அம்பர்', 'Sea Green': 'கடல் பச்சை'
}
FINGER_TAMIL = {
    'Ring Finger': 'மோதிர விரல்', 'Middle Finger': 'நடு விரல்', 'Little Finger': 'சுண்டு விரல்',
    'Index Finger': 'ஆள்காட்டி விரல்', 'Middle / Little Finger': 'நடு / சுண்டு விரல்',
    'Little / Ring Finger': 'சுண்டு / மோதிர விரல்', 'Little / Index Finger': 'சுண்டு / ஆள்காட்டி விரல்',
    'Index / Ring Finger': 'ஆள்காட்டி / மோதிர விரல்'
}

def generate_lucky_factors(asc_sign_idx):
    gem_map = {
        0: ('Red Coral (சிவப்பு பவளம்)', 'Yellow Sapphire (மஞ்சள் புஷ்பராகம்)', 'Tuesday / Thursday', 'Gold / Copper', 'Ring Finger'),
        1: ('Diamond (வைரம்)', 'Blue Sapphire (நீலக்கல்)', 'Friday / Saturday', 'Platinum / Silver', 'Middle / Little Finger'),
        2: ('Emerald (மரகதப் பச்சை)', 'Blue Sapphire (நீலக்கல்)', 'Wednesday / Saturday', 'Gold / Silver', 'Little Finger'),
        3: ('Natural Pearl (முத்து)', 'Yellow Sapphire (மஞ்சள் புஷ்பராகம்)', 'Monday / Thursday', 'Silver / Gold', 'Little / Index Finger'),
        4: ('Ruby (மாணிக்கம்)', 'Red Coral (சிவப்பு பவளம்)', 'Sunday / Tuesday', 'Gold / Copper', 'Ring Finger'),
        5: ('Emerald (மரகதப் பச்சை)', 'Diamond (வைரம்)', 'Wednesday / Friday', 'Gold / Silver', 'Little Finger'),
        6: ('Diamond (வைரம்)', 'Emerald (மரகதப் பச்சை)', 'Friday / Wednesday', 'Platinum / Silver', 'Middle / Little Finger'),
        7: ('Red Coral (சிவப்பு பவளம்)', 'Natural Pearl (முத்து)', 'Tuesday / Monday', 'Gold / Copper', 'Ring Finger'),
        8: ('Yellow Sapphire (மஞ்சள் புஷ்பராகம்)', 'Ruby (மாணிக்கம்)', 'Thursday / Sunday', 'Gold', 'Index Finger'),
        9: ('Blue Sapphire (நீலக்கல்)', 'Emerald (மரகதப் பச்சை)', 'Saturday / Wednesday', 'Silver / Iron', 'Middle Finger'),
        10: ('Blue Sapphire (நீலக்கல்)', 'Diamond (வைரம்)', 'Saturday / Friday', 'Silver / Iron', 'Middle Finger'),
        11: ('Yellow Sapphire (மஞ்சள் புஷ்பராகம்)', 'Red Coral (சிவப்பு பவளம்)', 'Thursday / Tuesday', 'Gold / Copper', 'Index / Ring Finger')
    }

    lucky_days_map = {
        0: ['Tuesday', 'Sunday', 'Thursday'],
        1: ['Friday', 'Saturday', 'Wednesday'],
        2: ['Wednesday', 'Friday', 'Saturday'],
        3: ['Monday', 'Tuesday', 'Thursday'],
        4: ['Sunday', 'Tuesday', 'Thursday'],
        5: ['Wednesday', 'Friday', 'Saturday'],
        6: ['Friday', 'Saturday', 'Wednesday'],
        7: ['Tuesday', 'Sunday', 'Monday'],
        8: ['Thursday', 'Sunday', 'Tuesday'],
        9: ['Saturday', 'Friday', 'Wednesday'],
        10: ['Saturday', 'Friday', 'Wednesday'],
        11: ['Thursday', 'Monday', 'Tuesday']
    }

    lucky_numbers_map = {
        0: [1, 9, 3], 1: [6, 5, 8], 2: [5, 6, 8], 3: [2, 7, 9],
        4: [1, 9, 3], 5: [5, 6, 8], 6: [6, 5, 8], 7: [9, 1, 2],
        8: [3, 1, 9], 9: [8, 5, 6], 10: [8, 6, 5], 11: [3, 2, 9]
    }

    lucky_colors_map = {
        0: ['Bright Red', 'Crimson', 'Golden Yellow'],
        1: ['Diamond White', 'Pale Pink', 'Cream'],
        2: ['Emerald Green', 'Pastel Shades'],
        3: ['Pearl White', 'Silver', 'Cream'],
        4: ['Deep Gold', 'Orange', 'Ruby Red'],
        5: ['Parrot Green', 'Turquoise'],
        6: ['Pure White', 'Rose Pink', 'Silk Blue'],
        7: ['Scarlet Red', 'Rust', 'Amber'],
        8: ['Bright Yellow', 'Saffron', 'Golden Yellow'],
        9: ['Royal Blue', 'Navy', 'Steel Grey'],
        10: ['Electric Blue', 'Violet', 'Indigo'],
        11: ['Pale Yellow', 'Golden Amber', 'Sea Green']
    }

    primary_gem, fortune_gem, best_day, metal, finger = gem_map[asc_sign_idx]
    # Gem names carry their Tamil name in brackets: "Ruby (மாணிக்கம்)"
    gem_en = lambda g: g.split(' (')[0]
    gem_ta = lambda g: g.split(' (')[1].rstrip(')')
    in_tamil = lambda text: ' / '.join(LUCKY_TAMIL[part] for part in text.split(' / '))

    return {
        'primary_gem': gem_en(primary_gem),
        'primary_gem_ta': gem_ta(primary_gem),
        'fortune_gem': gem_en(fortune_gem),
        'fortune_gem_ta': gem_ta(fortune_gem),
        'wearing_day': best_day,
        'wearing_day_ta': in_tamil(best_day),
        'metal': metal,
        'metal_ta': in_tamil(metal),
        'finger': finger,
        'finger_ta': FINGER_TAMIL[finger],
        'lucky_days': lucky_days_map[asc_sign_idx],
        'lucky_days_ta': [LUCKY_TAMIL[d] for d in lucky_days_map[asc_sign_idx]],
        'lucky_numbers': lucky_numbers_map[asc_sign_idx],
        'lucky_colors': lucky_colors_map[asc_sign_idx],
        'lucky_colors_ta': [LUCKY_TAMIL[c] for c in lucky_colors_map[asc_sign_idx]],
        'gem_basis_en': (f"Life stone for the Lagna lord {SIGN_LORDS[asc_sign_idx]}; fortune stone for the 9th lord "
                         f"{SIGN_LORDS[(asc_sign_idx + 8) % 12]}. Wear a gem only after checking these lords' strength in your chart; "
                         f"stones of the 6th, 8th and 12th lords are best avoided."),
        'gem_basis_ta': (f"ஜீவ ரத்தினம்: லக்னாதிபதி {PLANET_TAMIL[SIGN_LORDS[asc_sign_idx]]}; பாக்கிய ரத்தினம்: 9-ஆம் அதிபதி "
                         f"{PLANET_TAMIL[SIGN_LORDS[(asc_sign_idx + 8) % 12]]}. ஜாதகத்தில் இந்த அதிபதிகளின் பலத்தைச் "
                         f"சரிபார்த்த பின்னரே அணியவும்; 6, 8, 12-ஆம் அதிபதிகளின் ரத்தினங்களைத் தவிர்ப்பது நலம்."),
        'deity_worship_en': 'Lord Ganesha, Lord Shiva, and Goddess Mahalakshmi',
        'deity_worship_ta': 'விநாயகர், சிவபெருமான் மற்றும் மஹாலக்ஷ்மி தாயார்'
    }

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


# 9. K.N. Rao & BVB Double Transit (Dwi-Gochara) Engine
# An event needs transit Saturn and Jupiter both to influence (occupy or aspect) the house or
# its lord, and a running Maha or Antar dasa connected with the matter (K.N. Rao).
SATURN_ASPECTS, JUPITER_ASPECTS = (0, 2, 6, 9), (0, 4, 6, 8)
DOUBLE_TRANSIT_EVENTS = [
    ('marriage', 7, ('Venus',), 'Marriage & Relationship', 'திருமணம் & இல்லறம்'),
    ('career', 10, ('Sun', 'Saturn'), 'Career Rise & Promotion', 'தொழில் முன்னேற்றம் & பதவி உயர்வு'),
    ('children', 5, ('Jupiter',), 'Progeny & Children', 'புத்திர பாக்கியம்'),
    ('property', 4, ('Mars', 'Venus'), 'Property, Home & Vehicle', 'பூமி, வீடு & வாகனம்')
]
DT_STATUS = {
    'active': (90, 'Active window: double transit with dasa support', 'செயல்படும் காலம்: இரட்டைப் பெயர்ச்சியுடன் தசா ஆதரவு'),
    'transit': (65, 'Transit ready, awaiting a supporting dasa', 'பெயர்ச்சி சாதகம்; ஆதரவான தசைக்காகக் காத்திருக்கிறது'),
    'building': (50, 'Building: dasa supports, one transit in place', 'உருவாகிறது: தசா ஆதரவு, ஒரு பெயர்ச்சி மட்டும் சாதகம்'),
    'quiet': (25, 'Quiet period', 'அமைதியான காலம்')
}


def _dasa_at(dasha_rows, moment):
    for d in dasha_rows:
        if datetime.fromisoformat(d['start']) <= moment < datetime.fromisoformat(d['end']):
            for b in d.get('subperiods', []):
                if datetime.fromisoformat(b['start']) <= moment < datetime.fromisoformat(b['end']):
                    return d['lord'], b['lord']
            return d['lord'], None
    return None, None


def calculate_double_transit(chart):
    gochara = chart['gochara']
    transit = gochara['planets']
    planets = chart['planets']
    asc_sign = planets['Ascendant']['sign_index']
    tz = ZoneInfo(chart.get('timezone') or 'UTC')
    now = datetime.fromisoformat(gochara['computed_at'])
    sat_sign, jup_sign = transit['Saturn']['sign_index'], transit['Jupiter']['sign_index']
    periods = gochara.get('slow_transits', {})

    def influences(aspects, from_sign, targets):
        return any((t - from_sign) % 12 in aspects for t in targets)

    milestones = []
    for key, house, karakas, title_en, title_ta in DOUBLE_TRANSIT_EVENTS:
        house_sign = (asc_sign + house - 1) % 12
        lord = SIGN_LORDS[house_sign]
        targets = {house_sign, planets[lord]['sign_index']}

        def connected(dasa_lord):
            if dasa_lord is None:
                return False
            ruler = SIGN_LORDS[planets[dasa_lord]['sign_index']] if dasa_lord in ('Rahu', 'Ketu') else dasa_lord
            return (dasa_lord in (lord,) + karakas or ruler == lord or planets[dasa_lord]['house'] == house
                    or planets[dasa_lord]['sign_index'] == planets[lord]['sign_index'])

        sat_now = influences(SATURN_ASPECTS, sat_sign, targets)
        jup_now = influences(JUPITER_ASPECTS, jup_sign, targets)
        maha, antar = _dasa_at(chart.get('dasha', []), now)
        dasa_now = connected(maha) or connected(antar)
        status = ('active' if sat_now and jup_now and dasa_now else 'transit' if sat_now and jup_now
                  else 'building' if dasa_now and (sat_now or jup_now) else 'quiet')

        # Upcoming double-transit windows, each checked against the dasa running when it opens
        windows = []
        for sp in periods.get('Saturn', []):
            if not influences(SATURN_ASPECTS, sp['sign_index'], targets):
                continue
            for jp in periods.get('Jupiter', []):
                start, end = max(sp['start'], jp['start']), min(sp['end'], jp['end'])
                if start < end and influences(JUPITER_ASPECTS, jp['sign_index'], targets):
                    if windows and windows[-1]['_end'] == start:
                        windows[-1]['_end'] = end
                    else:
                        windows.append(dict(_start=start, _end=end))
        windows.sort(key=lambda w: w['_start'])
        window_rows = []
        for w in windows[:4]:
            opens = datetime.fromisoformat(w['_start'])
            w_maha, w_antar = _dasa_at(chart.get('dasha', []), opens)
            window_rows.append(dict(
                start=opens.astimezone(tz).date().isoformat(),
                end=datetime.fromisoformat(w['_end']).astimezone(tz).date().isoformat(),
                dasa=w_maha, bhukti=w_antar, dasa_support=connected(w_maha) or connected(w_antar)))
        supported = [w for w in window_rows if w['dasa_support']]
        best = supported[0] if supported else (window_rows[0] if window_rows else None)

        score, status_en, status_ta = DT_STATUS[status]
        lord_ta = PLANET_TAMIL[lord]
        transit_en = (f"Transit Saturn in {SIGNS[sat_sign]} {'influences' if sat_now else 'does not influence'} your "
                      f"{_ordinal(house)} house ({SIGNS[house_sign]}) or its lord {lord}; transit Jupiter in "
                      f"{SIGNS[jup_sign]} {'influences it' if jup_now else 'does not'}.")
        transit_ta = (f"கோச்சார சனி ({TAMIL_SIGNS[sat_sign]}) உங்கள் {house}-ஆம் பாவம் ({TAMIL_SIGNS[house_sign]}) அல்லது "
                      f"அதன் அதிபதி {lord_ta} மீது {'தொடர்பு கொள்கிறார்' if sat_now else 'தொடர்பு கொள்ளவில்லை'}; "
                      f"கோச்சார குரு ({TAMIL_SIGNS[jup_sign]}) {'தொடர்பு கொள்கிறார்' if jup_now else 'தொடர்பு கொள்ளவில்லை'}.")
        if maha:
            dasa_en = (f" The running {maha}{'–' + antar if antar else ''} dasa is "
                       f"{'connected' if dasa_now else 'not connected'} with this matter.")
            dasa_ta = (f" நடப்பு {PLANET_TAMIL[maha]}{'–' + PLANET_TAMIL[antar] if antar else ''} தசை இந்த விஷயத்துடன் "
                       f"{'தொடர்பு கொண்டுள்ளது' if dasa_now else 'தொடர்பில்லை'}.")
        else:
            dasa_en = dasa_ta = ''
        if best:
            next_en = (f" Next {'dasa-supported ' if best['dasa_support'] else ''}double-transit window: "
                       f"{best['start']} to {best['end']} ({best['dasa']}–{best['bhukti']} dasa).")
            next_ta = (f" அடுத்த {'தசா ஆதரவுள்ள ' if best['dasa_support'] else ''}இரட்டைப் பெயர்ச்சி காலம்: "
                       f"{best['start']} முதல் {best['end']} வரை ({PLANET_TAMIL[best['dasa']]}–{PLANET_TAMIL[best['bhukti']]} தசை).")
        else:
            next_en = " No double-transit window opens in the next 6 years."
            next_ta = " அடுத்த 6 ஆண்டுகளில் இரட்டைப் பெயர்ச்சி காலம் இல்லை."
        milestones.append({
            'key': key,
            'title_en': title_en,
            'title_ta': title_ta,
            'target_house': f"{_ordinal(house)} house ({SIGNS[house_sign]}) & its lord {lord}",
            'target_house_ta': f"{house}-ஆம் பாவம் ({TAMIL_SIGNS[house_sign]}) & அதிபதி {lord_ta}",
            'is_active': status == 'active',
            'status': status,
            'score': score,
            'status_en': status_en,
            'status_ta': status_ta,
            'saturn_influence': sat_now,
            'jupiter_influence': jup_now,
            'dasa_support': dasa_now,
            'windows': window_rows,
            'desc_en': transit_en + dasa_en + next_en,
            'desc_ta': transit_ta + dasa_ta + next_ta
        })

    def position(name, sign, aspects):
        lon = transit[name]['longitude']
        deg = lon % 30
        return {
            'sign': SIGNS[sign],
            'tamil_sign': TAMIL_SIGNS[sign],
            'degree_str': f"{int(deg)}° {int((deg * 60) % 60):02d}′",
            'aspects_houses': sorted(((sign + a) - asc_sign) % 12 + 1 for a in aspects)
        }

    return {
        'calculation_date_utc': gochara['computed_at'].replace('T', ' ').replace('+00:00', ' UTC'),
        'transit_saturn': position('Saturn', sat_sign, SATURN_ASPECTS),
        'transit_jupiter': position('Jupiter', jup_sign, JUPITER_ASPECTS),
        'milestones': milestones
    }

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

# 12. Ashtakavarga Kakshya Precision Transit System
def calculate_kakshya_transits(chart):
    transit = chart['gochara']['planets']
    sat_lon = transit['Saturn']['longitude']
    jup_lon = transit['Jupiter']['longitude']

    sat_sign = int(sat_lon // 30)
    sat_deg = sat_lon % 30
    jup_sign = int(jup_lon // 30)
    jup_deg = jup_lon % 30

    bav = chart['ashtakavarga']['BAV']
    prastara = chart['ashtakavarga']['prastara']
    kakshya_deg_step = 30.0 / 8.0 # 3.75 deg per Kakshya

    def build_kakshya_table(p_name, sign_idx, current_deg):
        # A kakshya bears fruit only if its lord contributed a bindu to this sign in the
        # transiting planet's own Ashtakavarga (the prastara table).
        current_k_idx = min(int(current_deg / kakshya_deg_step), 7)
        rows = []
        for k in range(8):
            start_d = k * kakshya_deg_step
            end_d = (k + 1) * kakshya_deg_step
            k_lord = KAKSHYA_LORDS[k]
            k_lord_ta = KAKSHYA_LORDS_TA[k]
            has_bindu = bool(prastara[p_name][k_lord][sign_idx])
            is_current = (k == current_k_idx)

            rows.append({
                'kakshya_num': k + 1,
                'range_str': f"{int(start_d)}°{int((start_d*60)%60):02d}′ – {int(end_d)}°{int((end_d*60)%60):02d}′",
                'lord': k_lord,
                'lord_ta': k_lord_ta,
                'has_bindu': has_bindu,
                'status_en': 'Fruitful (Phala-Prada)' if has_bindu else 'Caution (Nishphala)',
                'status_ta': 'சுப பலன் (பலப்பிரதம்)' if has_bindu else 'கவனம் (நிஷ்பலம்)',
                'is_current': is_current
            })
        return current_k_idx, rows

    sat_k_idx, sat_table = build_kakshya_table('Saturn', sat_sign, sat_deg)
    jup_k_idx, jup_table = build_kakshya_table('Jupiter', jup_sign, jup_deg)

    sat_curr = sat_table[sat_k_idx]
    jup_curr = jup_table[jup_k_idx]

    return {
        'saturn': {
            'sign': SIGNS[sat_sign],
            'tamil_sign': TAMIL_SIGNS[sat_sign],
            'current_degree': f"{int(sat_deg)}°{int((sat_deg*60)%60):02d}′",
            'current_kakshya': sat_curr,
            'kakshya_timeline': sat_table,
            'bindus': bav['Saturn'][sat_sign],
            'summary_en': f"Saturn transits Kakshya {sat_k_idx + 1} ({sat_curr['lord']}) of {SIGNS[sat_sign]}, where it holds {bav['Saturn'][sat_sign]} of 8 bindus. Status: {sat_curr['status_en']}.",
            'summary_ta': f"சனி பகவான் {TAMIL_SIGNS[sat_sign]} ராசியின் {sat_k_idx + 1}-வது கக்ஷ்யையில் ({sat_curr['lord_ta']}) சஞ்சரிக்கிறார்; இந்த ராசியில் சனிக்கு 8-ல் {bav['Saturn'][sat_sign]} பரல்கள் உள்ளன. பலன்: {sat_curr['status_ta']}."
        },
        'jupiter': {
            'sign': SIGNS[jup_sign],
            'tamil_sign': TAMIL_SIGNS[jup_sign],
            'current_degree': f"{int(jup_deg)}°{int((jup_deg*60)%60):02d}′",
            'current_kakshya': jup_curr,
            'kakshya_timeline': jup_table,
            'bindus': bav['Jupiter'][jup_sign],
            'summary_en': f"Jupiter transits Kakshya {jup_k_idx + 1} ({jup_curr['lord']}) of {SIGNS[jup_sign]}, where it holds {bav['Jupiter'][jup_sign]} of 8 bindus. Status: {jup_curr['status_en']}.",
            'summary_ta': f"குரு பகவான் {TAMIL_SIGNS[jup_sign]} ராசியின் {jup_k_idx + 1}-வது கக்ஷ்யையில் ({jup_curr['lord_ta']}) சஞ்சரிக்கிறார்; இந்த ராசியில் குருவுக்கு 8-ல் {bav['Jupiter'][jup_sign]} பரல்கள் உள்ளன. பலன்: {jup_curr['status_ta']}."
        }
    }


# ==============================================================================
# 6 ADVANCED ASTROLOGICAL SYSTEMS & DEEP PREDICTIONS (TAMIL & ENGLISH)
# ==============================================================================

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


def get_kp_sublord(lon):
    """Sign, star and KP sub of a longitude. Worked in arc-minutes, where a nakshatra is
    exactly 800', so boundaries such as 280° (the start of Shravana) fall the right way."""
    minutes = round((lon % 360) * 60, 6)
    sign_idx = int(minutes // 1800) % 12
    star_idx = int(minutes // 800) % 27
    star_lord = DASA_LORDS[star_idx % 9]
    offset = minutes - (minutes // 800) * 800
    start = DASA_LORDS.index(star_lord)
    sub_lord = DASA_LORDS[(start + 8) % 9]
    accum = 0.0
    for i in range(9):
        lord = DASA_LORDS[(start + i) % 9]
        accum += 800 * VIMSHOTTARI_YEARS[lord] / 120
        if offset < accum:
            sub_lord = lord
            break
    return sign_idx, SIGNS[sign_idx], TAMIL_SIGNS[sign_idx], SIGN_LORDS[sign_idx], STARS[star_idx], star_lord, sub_lord

# 1. SHADBALA ENGINE & PREDICTIONS
SHADBALA_READINGS = {
    'Sun': {
        'theme_en': 'executive authority, vitality, leadership, and public recognition',
        'theme_ta': 'அதிகார ஆளுமை, உடல் நலம், தலைமைத்துவம் மற்றும் சமூக புகழ்',
        'strong_en': 'Endows radiant confidence, dignified integrity, natural leadership charisma, and strong support from government or senior authorities.',
        'strong_ta': 'சூரியன் உயர் பலம் பெற்றுள்ளதால் அசைக்க முடியாத தன்னம்பிக்கை, கம்பீரமான ஆளுமை, அரசு வழியில் நன்மைகள் மற்றும் தலைமைப் பொறுப்புகள் அமையும்.',
        'weak_en': 'May induce occasional self-doubt or struggle with organizational superiors. Daily Surya Namaskar and honoring father figures strengthen solar vigor.',
        'weak_ta': 'சூரியன் குறைந்த பலம் உள்ளதால் சில சமயங்களில் தயக்கமும், அதிகாரிகளுடன் பிணக்குகளும் நேரலாம். ஆதித்ய ஹிருதய ஸ்தோத்திரம் மற்றும் தந்தையிடம் ஆசி பெறுதல் நலம்.'
    },
    'Moon': {
        'theme_en': 'emotional equanimity, intuitive perception, mental tranquility, and public popularity',
        'theme_ta': 'மன அமைதி, உள்ளுணர்வுத் தெளிவு, பொதுஜன ஆதரவு மற்றும் கற்பனைத் திறன்',
        'strong_en': 'Bestows serene emotional balance, maternal grace, fertile creative instincts, and wide social affection.',
        'strong_ta': 'சந்திரன் உன்னத பலம் பெற்றுள்ளதால் மன அமைதி, தெளிவான உள்ளுணர்வு, கற்பனை ஆற்றல் மற்றும் மக்கள் மத்தியில் நன்மதிப்பு கூடும்.',
        'weak_en': 'Indicates mood sensitivity or over-thinking during stressful periods. Meditation and honoring mother energies cultivate inner stability.',
        'weak_ta': 'சந்திரன் குறைந்த பலம் பெற்றுள்ளதால் மன அமைதியின்மை அல்லது அதீத சிந்தனை ஏற்படலாம். தியானம் மற்றும் தாய்க்கு பணிவிடை செய்வது அமைதி தரும்.'
    },
    'Mars': {
        'theme_en': 'courage, real estate prowess, physical stamina, engineering acumen, and fearlessness',
        'theme_ta': 'துணிச்சல், பூமி யோகம், பொறியியல்/தொழில்நுட்பத் திறன் மற்றும் எதிரிகளை வெல்லும் வலிமை',
        'strong_en': 'Commands heroic willpower, strategic fearlessness, property success, and razor-sharp executive decisiveness.',
        'strong_ta': 'செவ்வாய் மிகுந்த பலம் பெற்றுள்ளதால் அஞ்சாத நெஞ்சம், பூமி-மனை வாங்கும் யோகம், தொழில்நுட்பம் மற்றும் நிர்வாகத்தில் அபார வெற்றி கிட்டும்.',
        'weak_en': 'Can prompt impulsive haste or friction. Channeling fire into sports, yoga, or methodical engineering maintains harmonious energy.',
        'weak_ta': 'செவ்வாய் பலம் குறைவாக இருந்தால் அவசர முடிவுகளும், கோபமும் வரலாம். உடற்பயிற்சி மற்றும் சுப்ரமணியர் வழிபாடு செய்வது ஆற்றலை சமப்படுத்தும்.'
    },
    'Mercury': {
        'theme_en': 'commercial acumen, analytical intellect, communication flair, and diplomatic wit',
        'theme_ta': 'வணிக சாதுரியம், கூர்மையான புத்தி, தகவல் தொடர்புத் திறன் மற்றும் கணக்கியல் விவேகம்',
        'strong_en': 'Fosters multifaceted intellectual brilliance, linguistic elegance, swift mathematical intuition, and prosperous trade associations.',
        'strong_ta': 'புதன் மிகச் சிறந்த பலம் பெற்றுள்ளதால் பேச்சுத் திறமை, எழுத்து, கணிதம், வியாபாரம் மற்றும் கணினித் துறைகளில் அசாத்திய சாதனை புரியலாம்.',
        'weak_en': 'May result in scattered multitasking or mental restlessness. Grounding routines and green color alignments enhance focus.',
        'weak_ta': 'புதன் பலம் குறைவாக உள்ளதால் கவனச்சிதறல் ஏற்படலாம். புதன்கிழமை விஷ்ணு சஹஸ்ரநாமம் பாராயணம் செய்வது அறிவாற்றலை கூர்மையாக்கும்.'
    },
    'Jupiter': {
        'theme_en': 'divine grace, moral wisdom, financial expansion, mentorship, and progeny blessings',
        'theme_ta': 'தெய்வ அனுகூலம், தர்ம சிந்தனை, பொருளாதார வளர்ச்சி, புத்திர பாக்கியம் மற்றும் வழிகாட்டும் பெருமை',
        'strong_en': 'Radiates magnanimous benevolence, deep philosophical comprehension, ethical prosperity, and revered advisor standing.',
        'strong_ta': 'குரு பகவான் பரிபூரண பலம் பெற்றுள்ளதால் நற்குணங்கள், பொருளாதார பெருக்கம், ஆன்மீக அறிவு மற்றும் பெரியோர்களின் ஆசிகள் நிறைவாகக் கிட்டும்.',
        'weak_en': 'Suggests vigilance against financial complacency or over-promising. Honoring preceptors and engaging in philanthropic teaching elevates Jupiter.',
        'weak_ta': 'குரு பலம் குறைவாக இருந்தால் விரயச் செலவுகள் வரலாம். வியாழக்கிழமை தட்சிணாமூர்த்தி வழிபாடு மற்றும் குருமார்களுக்கு மரியாதை செய்தல் சிறப்பு.'
    },
    'Venus': {
        'theme_en': 'artistic refinement, marital harmony, aesthetic luxury, and relational elegance',
        'theme_ta': 'கலை ரசனை, தாம்பத்திய மகிழ்ச்சி, ஆடம்பர சுகபோகம் மற்றும் கவர்ச்சியான தோற்றம்',
        'strong_en': 'Confers exquisite aesthetic discernment, magnetic charm, sensual fulfillment, and enduring joy in matrimonial companionship.',
        'strong_ta': 'சுக்கிரன் நிறைந்த பலம் பெற்றுள்ளதால் கலை, வாகனம், ஆடை ஆபரண சேர்க்கை, வசதியான வாழ்க்கை மற்றும் இனிமையான தாம்பத்தியம் அமையும்.',
        'weak_en': 'May indicate relationship compromises or indulgence. Cultivating devotion to Mahalakshmi and refined artistic discipline brings balance.',
        'weak_ta': 'சுக்கிரன் பலம் குறைவாக இருந்தால் உறவுகளில் சமரசம் தேவைப்படலாம். வெள்ளிக்கிழமை மகாலட்சுமி வழிபாடு செய்வது வாழ்வில் சுப யோகங்களை சேர்க்கும்.'
    },
    'Saturn': {
        'theme_en': 'monumental endurance, career longevity, discipline, organization, and karmic resilience',
        'theme_ta': 'தளராத உழைப்பு, நீண்ட ஆயுள், நிர்வாக ஒழுக்கம் மற்றும் கர்ம வினைகளை வெல்லும் மன உறுதி',
        'strong_en': 'Instills unshakeable stoicism, structural organizing mastery, deep humility, and a career that rises steadily to legendary permanence.',
        'strong_ta': 'சனி பகவான் மிகுந்த பலம் பெற்றுள்ளதால் இரும்பைப் போன்ற மன உறுதி, கடின உழைப்பால் படிப்படியான உயர்ந்த பதவி மற்றும் நிலைத்த செல்வம் கிட்டும்.',
        'weak_en': 'May bring experiences of delay or emotional gravity. Serving underprivileged communities and disciplined consistency transform Saturnian karma.',
        'weak_ta': 'சனி பலம் குறைவாக இருந்தால் காரியத் தடைகளும், தாமதங்களும் வரலாம். ஏழை எளியவர்களுக்கு அன்னதானம் செய்வதும், அனுமன் வழிபாடும் தடைகளை நீக்கும்.'
    }
}
# Why a graha is strong or weak, read from its Shadbala components (virupas)
SHADBALA_FACTORS = [
    ('uchcha', lambda v: v >= 45, 1, 'Close to its exaltation point', 'உச்ச நிலைக்கு அருகில் உள்ளது'),
    ('uchcha', lambda v: v <= 15, -1, 'Close to its debilitation point', 'நீச நிலைக்கு அருகில் உள்ளது'),
    ('saptavargaja', lambda v: v >= 150, 1, 'Dignified across the seven vargas', 'சப்த வர்க்கங்களில் நல்ல கௌரவம் பெற்றது'),
    ('saptavargaja', lambda v: v <= 60, -1, 'With unfriendly lords in most vargas', 'பெரும்பாலான வர்க்கங்களில் பகை வீடுகளில் உள்ளது'),
    ('dig', lambda v: v >= 45, 1, 'Near its direction of strength', 'திக் பலம் நிறைந்த நிலையில் உள்ளது'),
    ('dig', lambda v: v <= 15, -1, 'Far from its direction of strength', 'திக் பலம் குறைந்த நிலையில் உள்ளது'),
    ('cheshta', lambda v: v >= 45, 1, 'Strong in motion (retrograde or slowing)', 'வக்ர/மந்த கதியால் சேஷ்டா பலம் பெற்றது'),
    ('drik', lambda v: v >= 10, 1, 'Aspected mainly by benefics', 'சுப கிரகப் பார்வை பெற்றது'),
    ('drik', lambda v: v <= -10, -1, 'Aspected mainly by malefics', 'பாப கிரகப் பார்வை பெற்றது'),
    ('yuddha', lambda v: v > 0, 1, 'Victorious in a planetary war', 'கிரக யுத்தத்தில் வெற்றி பெற்றது'),
    ('yuddha', lambda v: v < 0, -1, 'Defeated in a planetary war', 'கிரக யுத்தத்தில் தோல்வியுற்றது')
]
# Vimsopaka Bala grades out of 20 (BPHS ch. 7)
VIMSOPAKA_GRADES = [(15, ('Excellent', 'மிகச் சிறப்பு')), (10, ('Good', 'நன்று')), (5, ('Average', 'சராசரி')),
                    (0, ('Poor', 'பலவீனம்'))]
SHADBALA_COMPONENTS = ('uchcha', 'saptavargaja', 'ojayugma', 'kendra', 'drekkana', 'nathonnatha', 'paksha', 'tribhaga',
                       'abda', 'masa', 'vara', 'hora', 'ayana', 'yuddha', 'cheshta', 'drik')


def calculate_shadbala(chart):
    """Interpret the engine's Shadbala (BPHS, as worked in B.V. Raman's Graha and Bhava Balas)."""
    raw = chart['shadbala']
    shadbala_list = []
    for p_name in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']:
        r = raw[p_name]
        ratio = round(r['ratio'], 2)
        is_adequate = ratio >= 1.0
        factors = [dict(en=en, ta=ta, effect=effect) for key, test, effect, en, ta in SHADBALA_FACTORS if test(r[key])]
        if p_name == 'Moon':
            bright = r['paksha'] >= 60
            factors.insert(0, dict(en='A bright Moon' if bright else 'A dim Moon near Amavasai',
                                   ta='ஒளி மிகுந்த சந்திரன்' if bright else 'அமாவாசைக்கு அருகில் ஒளி குறைந்த சந்திரன்',
                                   effect=1 if bright else -1))
        ishta, kashta = r['ishta'], r['kashta']
        favourable = ishta >= kashta
        phala_en = (f"Ishta Phala {ishta:.1f} against Kashta Phala {kashta:.1f}: its dasa and bhukti lean towards "
                    + ('favourable results.' if favourable else 'testing results that reward patience.'))
        phala_ta = (f"இஷ்ட பலன் {ishta:.1f}, கஷ்ட பலன் {kashta:.1f}: இதன் தசா புக்திகள் பெரும்பாலும் "
                    + ('நற்பலன்களைத் தரும்.' if favourable else 'பொறுமையைச் சோதிக்கும் பலன்களைத் தரும்.'))
        interp = SHADBALA_READINGS[p_name]
        shadbala_list.append({
            'planet': p_name,
            'planet_ta': PLANET_TAMIL[p_name],
            'sthana_bala': round(r['sthana'], 2),
            'dig_bala': round(r['dig'], 2),
            'kaala_bala': round(r['kaala'], 2),
            'chesta_bala': round(r['cheshta'], 2),
            'naisargika_bala': round(r['naisargika'], 2),
            'drik_bala': round(r['drik'], 2),
            'components': {k: round(r[k], 2) for k in SHADBALA_COMPONENTS},
            'total_virupas': round(r['total'], 2),
            'total_rupas': round(r['rupas'], 2),
            'min_required_rupas': r['required_rupas'],
            'strength_ratio': ratio,
            'is_adequate': is_adequate,
            'ishta_phala': round(ishta, 2),
            'kashta_phala': round(kashta, 2),
            'factors': factors,
            'theme_en': interp['theme_en'],
            'theme_ta': interp['theme_ta'],
            'reading_en': (interp['strong_en'] if is_adequate else interp['weak_en']) + ' ' + phala_en,
            'reading_ta': (interp['strong_ta'] if is_adequate else interp['weak_ta']) + ' ' + phala_ta
        })

    shadbala_list.sort(key=lambda x: x['strength_ratio'], reverse=True)
    for idx, item in enumerate(shadbala_list):
        item['rank'] = idx + 1

    dominant = shadbala_list[0]
    vulnerable = shadbala_list[-1]
    adequate = [x for x in shadbala_list if x['is_adequate']]

    bhava_rows = []
    for row in chart.get('bhava_bala', []):
        bhava_rows.append(dict(bhava=row['bhava'], lord=row['lord'], lord_ta=PLANET_TAMIL[row['lord']],
                               adhipati=round(row['adhipati'], 2), dig=round(row['dig'], 2), drishti=round(row['drishti'], 2),
                               total_virupas=round(row['total'], 2), rupas=round(row['rupas'], 2), is_strong=row['strong']))
    for rank, row in enumerate(sorted(bhava_rows, key=lambda r: -r['rupas']), 1):
        row['rank'] = rank

    vimsopaka_rows = []
    for p_name, schemes in chart.get('vimsopaka', {}).items():
        row = dict(planet=p_name, planet_ta=PLANET_TAMIL[p_name])
        for scheme, v in schemes.items():
            score = round(v['score'], 2)
            grade = next(g for limit, g in VIMSOPAKA_GRADES if score >= limit)
            row[scheme] = dict(score=score, dignified=v['dignified'], grade_en=grade[0], grade_ta=grade[1],
                               bheda_en=v['bheda'][0] if v['bheda'] else None,
                               bheda_ta=v['bheda'][1] if v['bheda'] else None)
        vimsopaka_rows.append(row)

    return {
        'dominant_planet': dominant,
        'vulnerable_planet': vulnerable,
        'adequate_count': len(adequate),
        'bhavas': bhava_rows,
        'vimsopaka': vimsopaka_rows,
        'method_en': 'Brihat Parashara Hora Shastra, as worked in B.V. Raman\'s Graha and Bhava Balas; minimum strengths per BPHS.',
        'method_ta': 'பிருஹத் பராசர ஹோரா சாஸ்திரம் (பி.வி. ராமனின் கிரக-பாவ பலம் நூல் வழி); குறைந்தபட்ச பலம் பராசரர் வகுத்தபடி.',
        'summary_en': (f"{dominant['planet']} is the strongest graha at {dominant['strength_ratio']}x its required Shadbala, "
                       f"fuelling your {dominant['theme_en']}. {len(adequate)} of 7 grahas meet their classical minimum; "
                       f"{vulnerable['planet']} ({vulnerable['strength_ratio']}x) is the one to strengthen."),
        'summary_ta': (f"உங்கள் ஜாதகத்தில் அதிக பலம் பெற்ற கிரகம் {dominant['planet_ta']} (தேவையான ஷட்பலத்தின் "
                       f"{dominant['strength_ratio']} மடங்கு); இது உங்கள் {dominant['theme_ta']}-க்கு வலு சேர்க்கும். "
                       f"7 கிரகங்களில் {len(adequate)} கிரகங்கள் குறைந்தபட்ச பலத்தைப் பெற்றுள்ளன; "
                       f"பலம் கூட்ட வேண்டிய கிரகம் {vulnerable['planet_ta']} ({vulnerable['strength_ratio']} மடங்கு)."),
        'planets': shadbala_list
    }

# 2. KRISHNAMURTI PADDHATI (KP SYSTEM)
# Cusps judged by their sub-lord, with the houses that promise each matter and the houses
# (12th from them) that negate it (K.S. Krishnamurti, KP Readers).
KP_MATTERS = [
    (1, 'Health & Personality', 'உடல் நலம் & சுய ஆளுமை', (1, 5, 11), (6, 8, 12)),
    (2, 'Wealth & Family', 'தனம் & குடும்பம்', (2, 6, 11), (5, 8, 12)),
    (5, 'Children & Intellect', 'புத்திர பாக்கியம் & புத்தி', (2, 5, 11), (1, 4, 10)),
    (7, 'Marriage & Partnership', 'திருமணம் & கூட்டாண்மை', (2, 7, 11), (1, 6, 10)),
    (10, 'Profession & Status', 'தொழில் & அந்தஸ்து', (2, 6, 10, 11), (1, 5, 9)),
    (11, 'Gains & Fulfilment of Desires', 'லாபம் & விருப்பங்கள் நிறைவேறுதல்', (2, 6, 11), (5, 8, 12))
]
KP_VERDICTS = {
    'promised': ('Promised', 'உறுதி'),
    'mixed': ('Promised with delays', 'தாமதத்துடன் உறுதி'),
    'weak': ('Weakly supported', 'பலம் குறைவு'),
    'denied': ('Obstructed', 'தடை'),
    'neutral': ('Not clearly indicated', 'தெளிவில்லை')
}


def _kp_house(lon, cusps):
    """Placidus bhava (1-12) holding a longitude: from its cusp up to the next cusp."""
    for n in range(12):
        if (lon - cusps[n]) % 360 < (cusps[(n + 1) % 12] - cusps[n]) % 360:
            return n + 1
    return 1


def _houses_en(houses):
    hs = sorted(houses)
    if len(hs) < 2:
        return f"house {hs[0]}" if hs else 'no house'
    return 'houses ' + ', '.join(map(str, hs[:-1])) + f' and {hs[-1]}'


def _houses_ta(houses, case):
    """Tamil house list in the accusative ('acc', before a verb) or genitive ('gen')."""
    hs = sorted(houses)
    if len(hs) == 1:
        return f"{hs[0]}-ஆம் பாவத்தைக்" if case == 'acc' else f"{hs[0]}-ஆம் பாவத்"
    joined = ', '.join(map(str, hs))
    return f"{joined} ஆகிய பாவங்களைக்" if case == 'acc' else f"{joined} ஆகிய பாவங்களின்"


def calculate_kp_system(chart):
    kp = chart.get('kp')
    if kp:
        cusps, longitudes = kp['cusps'], kp['planets']
    else:  # a chart built without the engine's KP block: equal houses in the chart's ayanamsa
        asc_lon = chart['planets']['Ascendant']['longitude']
        cusps = [(asc_lon + i * 30) % 360 for i in range(12)]
        longitudes = {p: chart['planets'][p]['longitude'] for p in DASA_LORDS}
    grahas = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
    info = {p: get_kp_sublord(longitudes[p]) for p in grahas}
    occupied = {p: {_kp_house(longitudes[p], cusps)} for p in grahas}
    owned = {p: {n + 1 for n, c in enumerate(cusps) if SIGN_LORDS[int(c // 30) % 12] == p} for p in grahas}
    for node in ('Rahu', 'Ketu'):
        # A node acts as an agent of the lord of the sign it occupies
        agent = info[node][3]
        occupied[node] |= occupied[agent]
        owned[node] = set(owned[agent])

    def signified(p):
        star_lord = info[p][5]
        return dict(star_lord_occupies=sorted(occupied[star_lord]), occupies=sorted(occupied[p]),
                    star_lord_owns=sorted(owned[star_lord]), owns=sorted(owned[p]))

    def row(label, lon, extra):
        sign_idx, sign_name, sign_ta, sign_lord, star_name, star_lord, sub_lord = get_kp_sublord(lon)
        deg_in_sign = lon % 30
        d = int(deg_in_sign); m = int((deg_in_sign * 60) % 60); sec = int((deg_in_sign * 3600) % 60)
        return dict(label, longitude=round(lon, 4), degree_str=f"{d}° {m:02d}′ {sec:02d}″",
                    sign=sign_name, sign_ta=sign_ta, sign_lord=sign_lord, sign_lord_ta=PLANET_TAMIL[sign_lord],
                    star_name=star_name, star_lord=star_lord, star_lord_ta=PLANET_TAMIL[star_lord],
                    sub_lord=sub_lord, sub_lord_ta=PLANET_TAMIL[sub_lord], **extra)

    cusp_rows = [row(dict(cusp=i + 1), lon, {}) for i, lon in enumerate(cusps)]
    planet_rows = []
    for p in grahas:
        levels = signified(p)
        houses = sorted(set().union(*levels.values()))
        planet_rows.append(row(dict(planet=p, planet_ta=PLANET_TAMIL[p]), longitudes[p],
                               dict(kp_house=_kp_house(longitudes[p], cusps),
                                    significations=houses, signification_levels=levels)))

    interpretations = {}
    for cusp, title_en, title_ta, favourable, negating in KP_MATTERS:
        sub = cusp_rows[cusp - 1]['sub_lord']
        star_lord = info[sub][5]
        primary = occupied[star_lord] | owned[star_lord]
        secondary = occupied[sub] | owned[sub]
        good, bad, own_good = primary & set(favourable), primary & set(negating), secondary & set(favourable)
        if good and not bad:
            verdict = 'promised'
        elif good:
            verdict = 'mixed'
        elif own_good:
            verdict = 'weak'
        elif bad:
            verdict = 'denied'
        else:
            verdict = 'neutral'
        sub_ta, star_ta = PLANET_TAMIL[sub], PLANET_TAMIL[star_lord]
        basis_en = (f"The {_ordinal(cusp)} cusp sub-lord is {sub}, in the star of {star_lord}, which signifies "
                    f"{_houses_en(primary)}; {sub} itself signifies {_houses_en(secondary)}.")
        basis_ta = (f"{cusp}-ஆம் பாவ ஆரம்பத்தின் உப-அதிபதி {sub_ta}; அது {star_ta} நட்சத்திரத்தில் உள்ளது. "
                    f"{star_ta} {_houses_ta(primary, 'acc')} குறிக்கிறது; {sub_ta} தானாக {_houses_ta(secondary, 'acc')} குறிக்கிறது.")
        outcome = {
            'promised': (f"{title_en} is clearly promised through {_houses_en(good)}.",
                         f"{title_ta} {_houses_ta(good, 'gen')} தொடர்பால் உறுதியாக வாக்களிக்கப்பட்டுள்ளது."),
            'mixed': (f"{title_en} is promised through {_houses_en(good)}, but the link to {_houses_en(bad)} brings delays or struggle.",
                      f"{title_ta} {_houses_ta(good, 'gen')} தொடர்பால் உறுதி; ஆனால் {_houses_ta(bad, 'gen')} தொடர்பால் தாமதமோ போராட்டமோ இருக்கும்."),
            'weak': (f"{title_en} is possible but only modestly supported, through the sub-lord's own {_houses_en(own_good)}.",
                     f"{title_ta} சாத்தியம்; ஆனால் உப-அதிபதியின் சொந்த {_houses_ta(own_good, 'gen')} தொடர்பு வழியே மட்டுமே குறைந்த ஆதரவு உள்ளது."),
            'denied': (f"{title_en} meets obstruction from {_houses_en(bad)}, so only a supporting dasa can deliver it.",
                       f"{title_ta} தடைகளைச் சந்திக்கும்: {_houses_ta(bad, 'gen')} தொடர்பு இதற்கு எதிராக உள்ளது; சாதகமான தசையில் மட்டுமே பலன் கிட்டும்."),
            'neutral': (f"{title_en} is not clearly indicated either way by this sub-lord; the dasa lords decide.",
                        f"{title_ta} இந்த உப-அதிபதியால் தெளிவாகச் சுட்டப்படவில்லை; நடப்பு தசா நாதர்களே தீர்மானிப்பர்.")
        }[verdict]
        interpretations[f'cusp_{cusp}'] = dict(
            cusp_num=cusp,
            title_en=f"{_ordinal(cusp)} Cusp Sub-Lord ({title_en})",
            title_ta=f"{cusp}-ஆம் பாவ உப-அதிபதி ({title_ta})",
            sub_lord=sub, sub_lord_ta=sub_ta, star_lord=star_lord, star_lord_ta=star_ta,
            signified_houses=sorted(primary), favourable_houses=list(favourable), negating_houses=list(negating),
            verdict=verdict, verdict_en=KP_VERDICTS[verdict][0], verdict_ta=KP_VERDICTS[verdict][1],
            reading_en=f"{basis_en} {outcome[0]}", reading_ta=f"{basis_ta} {outcome[1]}"
        )

    # Ruling planets at birth: Lagna sign, star and sub lords, Moon sign and star lords, and the day lord
    asc = cusp_rows[0]
    moon = next(r for r in planet_rows if r['planet'] == 'Moon')
    weekday = chart.get('vedic_weekday')
    ruling = [('Lagna sign lord', 'லக்ன ராசி அதிபதி', asc['sign_lord']), ('Lagna star lord', 'லக்ன நட்சத்திர அதிபதி', asc['star_lord']),
              ('Lagna sub-lord', 'லக்ன உப-அதிபதி', asc['sub_lord']), ('Moon sign lord', 'சந்திர ராசி அதிபதி', moon['sign_lord']),
              ('Moon star lord', 'சந்திர நட்சத்திர அதிபதி', moon['star_lord'])]
    if weekday is not None:
        day_lord = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'][weekday]
        ruling.append(('Day lord', 'கிழமை அதிபதி', day_lord))
    ruling_planets = [dict(role_en=en, role_ta=ta, planet=p, planet_ta=PLANET_TAMIL[p]) for en, ta, p in ruling]

    return {
        'ayanamsa': 'Krishnamurti' if kp else None,
        'ayanamsa_degrees': round(kp['ayanamsa'], 4) if kp else None,
        'cusps': cusp_rows,
        'planets': planet_rows,
        'cuspal_predictions': interpretations,
        'ruling_planets': ruling_planets
    }

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
        'dharma_fire': {'name_en': 'Dharma Trine (Fire: Aries, Leo, Sagittarius)', 'name_ta': 'தர்ம திரிகோணம் (நெருப்பு: மேஷம், சிம்மம், தனுசு)', 'planets': []},
        'artha_earth': {'name_en': 'Artha Trine (Earth: Taurus, Virgo, Capricorn)', 'name_ta': 'அர்த்த திரிகோணம் (நிலம்: ரிஷபம், கன்னி, மகரம்)', 'planets': []},
        'kama_air': {'name_en': 'Kama Trine (Air: Gemini, Libra, Aquarius)', 'name_ta': 'காம திரிகோணம் (காற்று: மிதுனம், துலாம், கும்பம்)', 'planets': []},
        'moksha_water': {'name_en': 'Moksha Trine (Water: Cancer, Scorpio, Pisces)', 'name_ta': 'மோட்ச திரிகோணம் (நீர்: கடகம், விருச்சிகம், மீனம்)', 'planets': []}
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
    for a, b, title_en, title_ta, sig_en, sig_ta in BNN_SUTRAS:
        link = _bnn_link(planets, a, b)
        if link:
            rank, link_en, link_ta = link
            sutras.append({
                'title_en': title_en,
                'title_ta': title_ta,
                'planets': [a, b],
                'link_rank': rank,
                'link_en': link_en,
                'link_ta': link_ta,
                'significance_en': f"{a} and {b} are {link_en}. {sig_en}",
                'significance_ta': f"{PLANET_TAMIL[a]}, {PLANET_TAMIL[b]} {link_ta} உள்ளனர். {sig_ta}"
            })
    sutras.sort(key=lambda x: x['link_rank'])  # conjunctions first, adjacent signs last

    if not sutras:
        sutras.append({
            'title_en': 'Pancha-Bhuta Balance (Nadi Alignment)',
            'title_ta': 'பஞ்சபூத சமநிலை (நாடி யோகம்)',
            'planets': ['Jupiter', 'Ascendant'],
            'significance_en': 'Planetary energies are evenly distributed across Dharma, Artha, Kama, and Moksha trines, bestowing a versatile life orientation that adapts skillfully across all worldly stages.',
            'significance_ta': 'கிரகங்கள் தர்ம, அர்த்த, காம, மோட்ச திரிகோணங்களில் சமச்சீராகப் பரவியுள்ளதால் வாழ்வின் அனைத்து நிலைகளிலும் எளிதில் பழகி முன்னேறும் சமநிலை வாய்க்கும்.'
        })

    return {
        'trines': trine_map,
        'sutras': sutras,
        'summary_en': f"Bhrigu Nandi Nadi reveals {len(sutras)} core karmic sutras anchored by Jeeva Karaka (Jupiter) and Karma Karaka (Saturn). Your primary life lessons and breakthroughs unfold through purposeful service and ethical expansion.",
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
WATERY_SIGNS = (3, 7, 11)


def lajjitadi_avasthas(p_name, planets):
    """The Lajjitadi states of a graha, judged by rasi (sign) conjunction and Parashari aspect."""
    from .engine import NATURAL_FRIENDS
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
                 reading_en=LAJJITADI[k][3], reading_ta=LAJJITADI[k][4]) for k in states]


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
            'fruit_potency': fruit_potency,
            'lajjitadi': moods,
            'interpretation_en': f"Operating in {b_en} and {j_en}. Manifests approximately {fruit_potency}% of its innate planetary potential in physical life events.",
            'interpretation_ta': f"{b_ta} மற்றும் {j_ta} நிலையில் உள்ளதால், தனது இயற்கை காரகத்துவங்களில் சுமார் {fruit_potency}% முழு பலன்களை நடைமுறை வாழ்வில் வழங்கும்."
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
        'reading_en': f['en'],
        'reading_ta': f['ta']
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
            strength, note_en, note_ta = 'weak', 'needs strengthening', 'பலப்படுத்த வேண்டியது'
        elif lord_house in KENDRAS + TRIKONAS + (11,) and DIGNITY_SCORE.get(lord_dignity, 0) >= 0:
            strength, note_en, note_ta = 'strong', 'well supported', 'நல்ல ஆதரவுடன் உள்ளது'
        else:
            strength, note_en, note_ta = 'moderate', 'moderately supported', 'மிதமான ஆதரவுடன் உள்ளது'
        malefics = [q for q in ('Saturn', 'Mars', 'Rahu', 'Ketu') if planets[q]['sign_index'] == s_idx]
        affliction_en = f" {', '.join(malefics)} in the same sign afflicts it." if malefics else ''
        affliction_ta = f" அதே ராசியில் உள்ள {', '.join(PLANET_TAMIL[q] for q in malefics)} இதைப் பாதிக்கிறது." if malefics else ''
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
            'reading_en': (f"{r_en} It falls in {SIGNS[s_idx]}, the {_ordinal(house)} house; its lord {lord} sits in the "
                           f"{_ordinal(lord_house)} house, so this area of life is {note_en}.{affliction_en}"),
            'reading_ta': (f"{r_ta} இது {house}-ஆம் பாவமான {TAMIL_SIGNS[s_idx]} ராசியில் விழுகிறது; அதன் அதிபதி "
                           f"{PLANET_TAMIL[lord]} {lord_house}-ஆம் பாவத்தில் இருப்பதால் இந்த வாழ்க்கைத் துறை {note_ta}.{affliction_ta}")
        })

    return {
        'is_day_birth': is_day,
        'birth_type_en': 'Diurnal (Day Birth)' if is_day else 'Nocturnal (Night Birth)',
        'birth_type_ta': 'பகல் பிறப்பு' if is_day else 'இரவு பிறப்பு',
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
    items.append(dict(key='vaara', title_en='Weekday (Vaara)', title_ta='கிழமை (வாரம்)', reading_en=en, reading_ta=ta))

    tithi = panch['tithi']
    in_paksha = (tithi - 1) % 15 + 1
    class_en, class_ta, trait_en, trait_ta = TITHI_CLASSES[(in_paksha - 1) % 5]
    if in_paksha == 15:
        deity_en, deity_ta = ('the Moon', 'சந்திரன்') if tithi == 15 else ('the ancestors (Pitrs)', 'பித்ருக்கள்')
    else:
        deity_en, deity_ta = TITHI_DEITIES[in_paksha - 1]
    from .south_indian import TITHI_TA
    tithi_ta = TITHI_TA[in_paksha - 1] if in_paksha < 15 else ('பௌர்ணமி' if tithi == 15 else 'அமாவாசை')
    observance = TITHI_OBSERVANCE.get(30 if tithi == 30 else in_paksha, (
        f"Worshipping {deity_en} on this tithi each month is traditionally recommended.",
        f"ஒவ்வொரு மாதமும் இத்திதியில் {deity_ta} வழிபாடு பாரம்பரியமாகப் பரிந்துரைக்கப்படுகிறது.")) or ('', '')
    paksha_en = 'waxing (Shukla)' if tithi <= 15 else 'waning (Krishna)'
    paksha_ta = 'வளர்பிறை' if tithi <= 15 else 'தேய்பிறை'
    items.append(dict(
        key='tithi', title_en='Tithi', title_ta='திதி',
        reading_en=(f"Born on {panch['tithi_name']} of the {paksha_en} fortnight, a {class_en} tithi: {trait_en}. "
                    f"Presiding deity: {deity_en}. {observance[0]}".rstrip()),
        reading_ta=(f"{paksha_ta} {tithi_ta} திதியில் பிறந்தவர்; இது {class_ta} திதி: {trait_ta}. "
                    f"இதன் அதிதேவதை {deity_ta}. {observance[1]}".rstrip())))

    yoga = panch['yoga_name']
    meaning_en, yoga_ta, meaning_ta = NITYA_YOGA_MEANINGS.get(yoga, (yoga, yoga, yoga))
    if panch.get('yoga_auspiciousness') == 'Auspicious':
        yoga_en_text = f"Born in {yoga} yoga ('{meaning_en}'), an auspicious nitya yoga that supports well-being and success in undertakings."
        yoga_ta_text = f"{yoga_ta} யோகத்தில் ('{meaning_ta}') பிறந்தவர்; இது சுப நித்ய யோகம் என்பதால் நலமும் காரிய வெற்றியும் உண்டு."
    else:
        yoga_en_text = (f"Born in {yoga} yoga ('{meaning_en}'), one of the nine difficult nitya yogas: obstacles are overcome through "
                        f"patience, and prayer on the birth star day is traditionally advised.")
        yoga_ta_text = (f"{yoga_ta} யோகத்தில் ('{meaning_ta}') பிறந்தவர்; இது ஒன்பது கடினமான நித்ய யோகங்களில் ஒன்று: பொறுமையால் "
                        f"தடைகள் நீங்கும்; ஜன்ம நட்சத்திர நாளில் இறை வழிபாடு செய்வது பாரம்பரியமாகப் பரிந்துரைக்கப்படுகிறது.")
    items.append(dict(key='yoga', title_en='Nitya Yoga', title_ta='நித்ய யோகம்', reading_en=yoga_en_text, reading_ta=yoga_ta_text))

    karana = panch['karana_name']
    karana_ta = KARANA_TAMIL.get(karana, karana)
    if karana == 'Vishti':
        k_en = ("Born in Vishti (Bhadra) karana, traditionally a difficult karana: energy is strong but needs direction; "
                "worship of Ganapati is advised.")
        k_ta = "பத்திரை (விஷ்டி) கரணத்தில் பிறந்தவர்; இது கடினமான கரணம்: ஆற்றல் அதிகம், அதை நல்வழியில் செலுத்த வேண்டும்; விநாயகர் வழிபாடு நலம்."
    elif karana in ('Shakuni', 'Chatushpada', 'Naga', 'Kimstughna'):
        k_en = f"Born in {karana} karana, one of the four fixed karanas: a steady, determined temperament that prefers stability to change."
        k_ta = f"{karana_ta} கரணத்தில் பிறந்தவர்; இது நான்கு ஸ்திர கரணங்களில் ஒன்று: மாற்றத்தை விட நிலைத்தன்மையை விரும்பும் உறுதியான இயல்பு."
    else:
        k_en = f"Born in {karana} karana, a movable karana: an active, adaptable temperament that does well with travel and new ventures."
        k_ta = f"{karana_ta} கரணத்தில் பிறந்தவர்; இது சர கரணம்: சுறுசுறுப்பான, எந்தச் சூழலுக்கும் ஏற்றுக்கொள்ளும் இயல்பு; பயணங்களும் புதிய முயற்சிகளும் நலம் தரும்."
    items.append(dict(key='karana', title_en='Karana', title_ta='கரணம்', reading_en=k_en, reading_ta=k_ta))
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
            row[name.lower()] = dict(sign=SIGNS[sign], sign_ta=TAMIL_SIGNS[sign],
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
                    f"இயக்குகிறது: இந்த ஆண்டு {themes_ta} தொடர்பான விஷயங்கள் முன்னிலை பெறும்.")
    )


# Master Generator
def generate_comprehensive_predictions(chart):
    planets = chart['planets']
    asc = planets['Ascendant']
    moon = planets['Moon']
    panch = chart['panchanga']
    active_dasa = chart.get('active_dasha')
    dasha_rows = chart.get('dasha', [])
    house_details = chart.get('house_details', [])
    vargas = chart.get('vargas', {})

    star_pred = NAKSHATRA_PREDICTIONS.get(moon['nakshatra'], NAKSHATRA_PREDICTIONS['Ashwini'])
    lagna_pred = LAGNA_PREDICTIONS.get(asc['sign'], LAGNA_PREDICTIONS['Aries'])
    bhavas = generate_bhava_predictions(house_details, planets, bhava_bala=chart.get('bhava_bala'))
    planets_in_houses = generate_planet_house_predictions(planets)
    dasa_forecast = generate_dasa_forecast(active_dasa, dasha_rows, planets, chart.get('timezone') or 'UTC')
    transits = generate_transit_forecast(moon['sign_index'], chart['gochara'])
    luck = generate_lucky_factors(asc['sign_index'])

    # 5 Advanced Approved Astrological Research Modules
    jaimini_karakas = calculate_jaimini_karakas(planets, vargas)
    double_transit = calculate_double_transit(chart)
    career_d10 = calculate_career_vocation_d10(chart)
    ayur_jyotish = calculate_ayur_jyotish(chart)
    kakshya_transits = calculate_kakshya_transits(chart)

    # 6 New Advanced Calculation & Predictive Modules
    shadbala = calculate_shadbala(chart)
    kp_system = calculate_kp_system(chart)
    bnn = calculate_bhrigu_nandi_nadi(chart)
    avasthas = calculate_planetary_avasthas(chart)
    pada_reading = calculate_nakshatra_pada_reading(chart)
    sahams = calculate_sahams(chart)

    # 7 Chronological Life Timeline & 10-Year Projections (81 Dasa-Bhukti periods)
    timeline_predictions = calculate_timeline_predictions(chart)

    return {
        'overview': {
            'nakshatra': moon['nakshatra'],
            'tamil_nakshatra': moon['tamil_nakshatra'],
            'nakshatra_pred_en': star_pred['en'],
            'nakshatra_pred_ta': star_pred['ta'],
            'lagna': asc['sign'],
            'tamil_lagna': asc['tamil'],
            'lagna_pred_en': lagna_pred['en'],
            'lagna_pred_ta': lagna_pred['ta'],
            'moon_sign': moon['sign'],
            'tamil_moon_sign': moon['tamil'],
            'tithi_name': panch['tithi_name'],
            'yoga_name': panch['yoga_name']
        },
        'panchanga_phala': generate_panchanga_phala(chart),
        'sudarshana': calculate_sudarshana_chakra(chart),
        'bhavas': bhavas,
        'planets_in_houses': planets_in_houses,
        'dasa_forecast': dasa_forecast,
        'transits': transits,
        'lucky_factors': luck,
        'jaimini_karakas': jaimini_karakas,
        'double_transit': double_transit,
        'career_d10': career_d10,
        'ayur_jyotish': ayur_jyotish,
        'kakshya_transits': kakshya_transits,
        'shadbala': shadbala,
        'kp_system': kp_system,
        'bhrigu_nandi_nadi': bnn,
        'avasthas': avasthas,
        'pada_reading': pada_reading,
        'sahams': sahams,
        'timeline_predictions': timeline_predictions
    }
