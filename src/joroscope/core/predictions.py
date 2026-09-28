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
def generate_bhava_predictions(house_details, planets, lang='en'):
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
    'Little / Ring Finger': 'சுண்டு / மோதிர விரல்'
}

def generate_lucky_factors(asc_sign_idx):
    gem_map = {
        0: ('Red Coral (சிவப்பு பவளம்)', 'Yellow Sapphire (மஞ்சள் புஷ்பராகம்)', 'Tuesday / Thursday', 'Gold / Copper', 'Ring Finger'),
        1: ('Diamond (வைரம்)', 'Blue Sapphire (நீலக்கல்)', 'Friday / Saturday', 'Platinum / Silver', 'Middle / Little Finger'),
        2: ('Emerald (மரகதப் பச்சை)', 'Blue Sapphire (நீலக்கல்)', 'Wednesday / Saturday', 'Gold / Silver', 'Little Finger'),
        3: ('Natural Pearl (முத்து)', 'Red Coral (சிவப்பு பவளம்)', 'Monday / Tuesday', 'Silver / Gold', 'Little / Ring Finger'),
        4: ('Ruby (மாணிக்கம்)', 'Yellow Sapphire (மஞ்சள் புஷ்பராகம்)', 'Sunday / Thursday', 'Gold / Copper', 'Ring Finger'),
        5: ('Emerald (மரகதப் பச்சை)', 'Diamond (வைரம்)', 'Wednesday / Friday', 'Gold / Silver', 'Little Finger'),
        6: ('Diamond (வைரம்)', 'Emerald (மரகதப் பச்சை)', 'Friday / Wednesday', 'Platinum / Silver', 'Middle / Little Finger'),
        7: ('Red Coral (சிவப்பு பவளம்)', 'Natural Pearl (முத்து)', 'Tuesday / Monday', 'Gold / Copper', 'Ring Finger'),
        8: ('Yellow Sapphire (மஞ்சள் புஷ்பராகம்)', 'Ruby (மாணிக்கம்)', 'Thursday / Sunday', 'Gold', 'Index Finger'),
        9: ('Blue Sapphire (நீலக்கல்)', 'Emerald (மரகதப் பச்சை)', 'Saturday / Wednesday', 'Silver / Iron', 'Middle Finger'),
        10: ('Blue Sapphire (நீலக்கல்)', 'Diamond (வைரம்)', 'Saturday / Friday', 'Silver / Iron', 'Middle Finger'),
        11: ('Yellow Sapphire (மஞ்சள் புஷ்பராகம்)', 'Natural Pearl (முத்து)', 'Thursday / Monday', 'Gold', 'Index Finger')
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
        'deity_worship_en': 'Lord Ganesha, Lord Shiva, and Goddess Mahalakshmi',
        'deity_worship_ta': 'விநாயகர், சிவபெருமான் மற்றும் மஹாலக்ஷ்மி தாயார்'
    }

# 8. Jaimini 7 Chara Karakas & Karakamsha System
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
        ('GK', 'Gnatikaraka', 'ஞானாதி காரகன்', 'Karmic Obstacles, Resilience & Competitive Victory'),
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

    return {
        'karakas': karakas_list,
        'atmakaraka': ak_planet,
        'amatyakaraka': amk_planet,
        'karakamsha': {
            'sign': karakamsha_sign,
            'tamil_sign': karakamsha_tamil,
            'interpretation_en': kk_en,
            'interpretation_ta': kk_ta
        }
    }

# 9. K.N. Rao & BVB Double Transit (Dwi-Gochara) Engine
def calculate_double_transit(chart):
    transit = chart['gochara']['planets']
    sat_lon = transit['Saturn']['longitude']
    jup_lon = transit['Jupiter']['longitude']

    sat_sign = int(sat_lon // 30)
    sat_deg = sat_lon % 30
    jup_sign = int(jup_lon // 30)
    jup_deg = jup_lon % 30

    sat_aspects = [sat_sign, (sat_sign + 2) % 12, (sat_sign + 6) % 12, (sat_sign + 9) % 12]
    jup_aspects = [jup_sign, (jup_sign + 4) % 12, (jup_sign + 6) % 12, (jup_sign + 8) % 12]

    planets = chart['planets']
    asc_sign = planets['Ascendant']['sign_index']

    # 1. Marriage / Partnership (H7, Lord 7, Lagna)
    h7_sign = (asc_sign + 6) % 12
    h7_lord = SIGN_LORDS[h7_sign]
    h7_lord_sign = planets.get(h7_lord, {}).get('sign_index', h7_sign)

    marr_sat = (h7_sign in sat_aspects) or (h7_lord_sign in sat_aspects) or (asc_sign in sat_aspects)
    marr_jup = (h7_sign in jup_aspects) or (h7_lord_sign in jup_aspects) or (asc_sign in jup_aspects)
    marr_active = marr_sat and marr_jup

    # 2. Career Elevation & Promotion (H10, Lord 10, Lagna)
    h10_sign = (asc_sign + 9) % 12
    h10_lord = SIGN_LORDS[h10_sign]
    h10_lord_sign = planets.get(h10_lord, {}).get('sign_index', h10_sign)

    career_sat = (h10_sign in sat_aspects) or (h10_lord_sign in sat_aspects) or (asc_sign in sat_aspects)
    career_jup = (h10_sign in jup_aspects) or (h10_lord_sign in jup_aspects) or (asc_sign in jup_aspects)
    career_active = career_sat and career_jup

    # 3. Childbirth / Progeny / Intellect (H5, Lord 5, Jupiter natal)
    h5_sign = (asc_sign + 4) % 12
    h5_lord = SIGN_LORDS[h5_sign]
    h5_lord_sign = planets.get(h5_lord, {}).get('sign_index', h5_sign)
    natal_jup_sign = planets.get('Jupiter', {}).get('sign_index', 0)

    child_sat = (h5_sign in sat_aspects) or (h5_lord_sign in sat_aspects) or (natal_jup_sign in sat_aspects)
    child_jup = (h5_sign in jup_aspects) or (h5_lord_sign in jup_aspects) or (natal_jup_sign in jup_aspects)
    child_active = child_sat and child_jup

    # 4. Property, Vehicle & Relocation (H4, Lord 4, H12)
    h4_sign = (asc_sign + 3) % 12
    h4_lord = SIGN_LORDS[h4_sign]
    h4_lord_sign = planets.get(h4_lord, {}).get('sign_index', h4_sign)
    h12_sign = (asc_sign + 11) % 12

    prop_sat = (h4_sign in sat_aspects) or (h4_lord_sign in sat_aspects) or (h12_sign in sat_aspects)
    prop_jup = (h4_sign in jup_aspects) or (h4_lord_sign in jup_aspects) or (h12_sign in jup_aspects)
    prop_active = prop_sat and prop_jup

    milestones = [
        {
            'key': 'marriage',
            'title_en': 'Marriage & Relationship Alignment',
            'title_ta': 'திருமண பிராப்தி & தாம்பத்திய சேர்க்கை',
            'target_house': '7th House & 7th Lord',
            'target_house_ta': '7-ஆம் பாவம் & களத்திர காரகன்',
            'is_active': marr_active,
            'score': 88 if marr_active else (60 if (marr_sat or marr_jup) else 35),
            'status_en': 'High-Probability Active Window' if marr_active else ('Emerging Alignment' if (marr_sat or marr_jup) else 'Neutral Period'),
            'status_ta': 'தீவிர சாதகமான காலகட்டம்' if marr_active else ('வளர்ந்து வரும் காலகட்டம்' if (marr_sat or marr_jup) else 'அமைதியான காலம்'),
            'desc_en': (
                f"K.N. Rao's Double Transit Law is {'ACTIVATED' if marr_active else 'PARTIALLY ACTIVE'}. "
                f"Transit Saturn in {SIGNS[sat_sign]} casts aspect on target houses, while Transit Jupiter in {SIGNS[jup_sign]} lends divine benefic sanction. "
                f"{'Conditions are primed for alliance finalization, marriage ceremonies, or harmonious relationship deepening over the ongoing cycle.' if marr_active else 'Groundwork and prospective meetings are favored; formal commitment matures in upcoming phase.'}"
            ),
            'desc_ta': (
                f"கே.என். ராவ் அவர்களின் இரட்டைப் பெயர்ச்சி விதி {'முழுமையாக இயங்குகிறது' if marr_active else 'பகுதியாக இயங்குகிறது'}. "
                f"சனி பகவான் {TAMIL_SIGNS[sat_sign]} ராசியிலிருந்தும், குரு பகவான் {TAMIL_SIGNS[jup_sign]} ராசியிலிருந்தும் 7-ஆம் பாவகத்தை ஆசீர்வதிக்கின்றனர். "
                f"{'திருமணம், புதிய கூட்டாண்மை மற்றும் இல்லற மகிழ்ச்சிக்குரிய அரிய சுப காலகட்டமாகும்.' if marr_active else 'திருமணப் பேச்சுவார்த்தைகள் மற்றும் நல்லுறவுக்கான தயாரிப்புகள் தொடங்கலாம்.'}"
            )
        },
        {
            'key': 'career',
            'title_en': 'Career Elevation, Authority & Promotion',
            'title_ta': 'தொழில் முன்னேற்றம், பதவி உயர்வு & அந்தஸ்து',
            'target_house': '10th House & 10th Lord',
            'target_house_ta': '10-ஆம் பாவம் & ஜீவன ஸ்தானம்',
            'is_active': career_active,
            'score': 92 if career_active else (65 if (career_sat or career_jup) else 40),
            'status_en': 'High-Probability Active Window' if career_active else ('Emerging Alignment' if (career_sat or career_jup) else 'Neutral Period'),
            'status_ta': 'தீவிர சாதகமான காலகட்டம்' if career_active else ('வளர்ந்து வரும் காலகட்டம்' if (career_sat or career_jup) else 'அமைதியான காலம்'),
            'desc_en': (
                f"Professional karma is energized. Transit Saturn (Labor & Permanence) and Transit Jupiter (Expansion & Honor) simultaneously touch your career axis. "
                f"{'A major vocational breakthrough, leadership promotion, or lucrative business expansion is strongly signaled.' if career_active else 'Career foundations are strengthening steadily; focus on skill mastery and strategic networking.'}"
            ),
            'desc_ta': (
                f"தொழில் ஜீவன ஸ்தானம் சுப பலம் பெறுகிறது. சனி (கடின உழைப்பு) மற்றும் குரு (வளர்ச்சி & கௌரவம்) இணைந்து உங்கள் 10-ஆம் பாவத்தை இயக்குகின்றனர். "
                f"{'பதவி உயர்வு, புதிய பொறுப்புகள், நிறுவன வளர்ச்சி மற்றும் சமுதாய அந்தஸ்து கூடும் அற்புத காலம்.' if career_active else 'தொழில் முயற்சிகள் படிப்படியாக நல்ல முன்னேற்றத்தை நோக்கி நகரும்.'}"
            )
        },
        {
            'key': 'children',
            'title_en': 'Progeny, Children & Intellectual Breakthroughs',
            'title_ta': 'புத்திர பாக்கியம், கல்வி & படைப்பாற்றல்',
            'target_house': '5th House & Jupiter',
            'target_house_ta': '5-ஆம் பாவம் & குரு பகவான்',
            'is_active': child_active,
            'score': 85 if child_active else (55 if (child_sat or child_jup) else 30),
            'status_en': 'High-Probability Active Window' if child_active else ('Emerging Alignment' if (child_sat or child_jup) else 'Neutral Period'),
            'status_ta': 'தீவிர சாதகமான காலகட்டம்' if child_active else ('வளர்ந்து வரும் காலகட்டம்' if (child_sat or child_jup) else 'அமைதியான காலம்'),
            'desc_en': (
                f"Purva Punya and 5th house significations are activated. "
                f"{'Highly fertile and auspicious window for conception, birth of children, competitive examination triumph, and creative breakthroughs.' if child_active else 'Scholarly intellectual pursuits and artistic cultivation yield steady satisfaction.'}"
            ),
            'desc_ta': (
                f"பூர்வ புண்ணிய ஸ்தானம் குரு மற்றும் சனியின் பார்வையால் புத்துயிர் பெறுகிறது. "
                f"{'குழந்தைப் பேறு, குழந்தைகளின் கல்வி மேன்மை, போட்டித் தேர்வுகளில் வெற்றி பெற அருமையான காலம்.' if child_active else 'அறிவுசார் பணிகள் மற்றும் புதிய பயிற்சிகளுக்கு நற்பலன் தரும் காலம்.'}"
            )
        },
        {
            'key': 'property',
            'title_en': 'Real Estate, Vehicle & Relocation Timing',
            'title_ta': 'பூமி, வீடு, வாகன யோகம் & இடமாற்றம்',
            'target_house': '4th House & 4th Lord',
            'target_house_ta': '4-ஆம் பாவம் & சுக ஸ்தானம்',
            'is_active': prop_active,
            'score': 84 if prop_active else (58 if (prop_sat or prop_jup) else 35),
            'status_en': 'High-Probability Active Window' if prop_active else ('Emerging Alignment' if (prop_sat or prop_jup) else 'Neutral Period'),
            'status_ta': 'தீவிர சாதகமான காலகட்டம்' if prop_active else ('வளர்ந்து வரும் காலகட்டம்' if (prop_sat or prop_jup) else 'அமைதியான காலம்'),
            'desc_en': (
                f"Fixed assets and domestic foundation are under transit focus. "
                f"{'Strong probability of acquiring real estate, upgrading personal vehicles, home renovation, or favorable long-distance relocation.' if prop_active else 'Property investments require careful document verification and prudent budget planning.'}"
            ),
            'desc_ta': (
                f"நிலம், மனை, வீடு மற்றும் வாகன சுகத்திற்கான 4-ஆம் பாவம் தூண்டப்படுகிறது. "
                f"{'புதிய சொத்து வாங்குதல், வீடு புதுப்பித்தல், புது வாகனம் அமைதல் அல்லது அனுகூலமான இடமாற்றம் ஏற்படும் காலம்.' if prop_active else 'சொத்து விவகாரங்களில் ஆவணங்களை சரிபார்த்து நிதானமாக முடிவெடுப்பது நல்லது.'}"
            )
        }
    ]

    return {
        'calculation_date_utc': chart['gochara']['computed_at'].replace('T', ' ').replace('+00:00', ' UTC'),
        'transit_saturn': {
            'sign': SIGNS[sat_sign],
            'tamil_sign': TAMIL_SIGNS[sat_sign],
            'degree_str': f"{int(sat_deg)}° {int((sat_deg*60)%60):02d}′",
            'aspects_houses': sat_aspects
        },
        'transit_jupiter': {
            'sign': SIGNS[jup_sign],
            'tamil_sign': TAMIL_SIGNS[jup_sign],
            'degree_str': f"{int(jup_deg)}° {int((jup_deg*60)%60):02d}′",
            'aspects_houses': jup_aspects
        },
        'milestones': milestones
    }

# 10. D-10 Dasamsa & Career Vocation Aptitude Engine
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
            'sectors_ta': 'அரசுப் பணிகள், ஐ.ஏ.எஸ் / ஐ.பி.எஸ், தலைமை அதிகாரி, பாதுகாப்பு, நீதித்துறை',
            'base_score': 60
        },
        {
            'id': 'technology',
            'title_en': 'Engineering, Software, Data & Technology',
            'title_ta': 'பொறியியல், மென்பொருள் & நவீன தொழில்நுட்பம்',
            'planets': ['Mars', 'Rahu', 'Mercury', 'Saturn'],
            'sectors_en': 'Software Engineering, AI/Data Science, Hardware, Civil Construction, Aerospace',
            'sectors_ta': 'கணினி மென்பொருள், செயற்கை நுண்ணறிவு, கட்டடப் பொறியியல், விண்வெளி, மின்னணு',
            'base_score': 55
        },
        {
            'id': 'commerce',
            'title_en': 'Commerce, Finance, Enterprise & Banking',
            'title_ta': 'வணிகம், வங்கி, முதலீடு & நிதித்துறை',
            'planets': ['Mercury', 'Venus', 'Jupiter'],
            'sectors_en': 'Investment Banking, Wealth Management, FinTech, Retail Empire, Corporate Trade',
            'sectors_ta': 'வங்கி, நிதி மேலாண்மை, பங்குச் சந்தை, ஏற்றுமதி இறக்குமதி, பெரு வர்த்தகம்',
            'base_score': 58
        },
        {
            'id': 'medicine',
            'title_en': 'Medicine, Healthcare, Pharmacology & Healing',
            'title_ta': 'மருத்துவம், அறுவை சிகிச்சை & மக்கள் நல்வாழ்வு',
            'planets': ['Sun', 'Mars', 'Moon', 'Jupiter', 'Ketu'],
            'sectors_en': 'Physician, Surgery, Biotechnology, Pharmaceuticals, Holistic Wellness, Nursing',
            'sectors_ta': 'மருத்துவர், அறுவை சிகிச்சை, மருந்தியல், உயிரி தொழில்நுட்பம், இயற்கை மருத்துவம்',
            'base_score': 50
        },
        {
            'id': 'creative',
            'title_en': 'Law, Advisory, Academia, Creative Arts & Media',
            'title_ta': 'சட்டம், நீதி, கல்வி, கலை & ஊடகம்',
            'planets': ['Jupiter', 'Venus', 'Mercury', 'Moon'],
            'sectors_en': 'Legal Counsel, Higher Education, Film & Media, Journalism, Architecture, Creative Direction',
            'sectors_ta': 'சட்ட ஆலோசகர், பேராசிரியர், திரைப்படம், இதழியல், கட்டடக்கலை, படைப்புக் கலைகள்',
            'base_score': 52
        }
    ]

    scored = []
    for arch in archetypes:
        score = arch['base_score']
        for p_name in arch['planets']:
            p_data = planets.get(p_name)
            if not p_data: continue
            dig = p_data.get('dignity', 'Neutral')
            if 'Exalted' in dig or 'Moolatrikona' in dig or 'Own' in dig:
                score += 7
            elif 'Friend' in dig:
                score += 4
            if p_data['house'] in (1, 4, 7, 10, 5, 9):
                score += 5
            if p_name in d10:
                d10_sign = d10[p_name]
                if d10_sign in (0, 3, 4, 6, 8, 9, 10):
                    score += 4

        if h10_lord in arch['planets']:
            score += 10

        score = min(score, 98)
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

    narrative_en = (
        f"Your D-1 (Rasi) and D-10 (Dasamsa) charts indicate supreme aptitude for {top_arch['title_en']} ({top_arch['score']}% fit). "
        f"Governed on the professional axis by 10th Lord {h10_lord} in alignment with powerful karakas. "
        f"Key recommended industry sectors include: {top_arch['key_sectors_en']}."
    )
    narrative_ta = (
        f"உங்கள் ராசி (D-1) மற்றும் தசாம்சம் (D-10) அமைப்பின்படி, {top_arch['title_ta']} ({top_arch['score']}% பொருத்தம்) முதன்மை யோகமாக அமைகிறது. "
        f"10-ஆம் அதிபதியான {PLANET_TAMIL[h10_lord]} மற்றும் சாதகமான கிரக இணைவுகள் உங்களை இத்துறையில் உயர்த்தும். "
        f"பரிந்துரைக்கப்படும் முக்கிய துறைகள்: {top_arch['key_sectors_ta']}."
    )

    return {
        'top_archetype': top_arch,
        'all_archetypes': scored,
        'tenth_lord': h10_lord,
        'tenth_sign': SIGNS[h10_sign],
        'tamil_tenth_sign': TAMIL_SIGNS[h10_sign],
        'narrative_en': narrative_en,
        'narrative_ta': narrative_ta
    }

# 11. Ayur-Jyotish & Tridosha Medical Wellness
def calculate_ayur_jyotish(chart):
    planets = chart['planets']
    asc = planets['Ascendant']
    asc_sign = asc['sign_index']
    moon_sign = planets['Moon']['sign_index']
    sun_sign = planets['Sun']['sign_index']
    h6_sign = (asc_sign + 5) % 12
    h6_lord = SIGN_LORDS[h6_sign]

    vata_pts = 5.0
    pitta_pts = 5.0
    kapha_pts = 5.0

    # Ascendant sign element
    if asc_sign in (0, 4, 8): pitta_pts += 12
    elif asc_sign in (2, 6, 10): vata_pts += 12
    elif asc_sign in (3, 7, 11): kapha_pts += 12
    else: kapha_pts += 6; vata_pts += 6

    # Moon sign element
    if moon_sign in (0, 4, 8): pitta_pts += 9
    elif moon_sign in (2, 6, 10): vata_pts += 9
    elif moon_sign in (3, 7, 11): kapha_pts += 10
    else: kapha_pts += 5; vata_pts += 5

    # Sun sign element
    if sun_sign in (0, 4, 8): pitta_pts += 10
    elif sun_sign in (2, 6, 10): vata_pts += 7
    elif sun_sign in (3, 7, 11): kapha_pts += 7
    else: pitta_pts += 4; vata_pts += 4

    # Planetary natural doshas
    vata_pts += 10 if not planets.get('Saturn', {}).get('combust') else 6
    vata_pts += 8 # Rahu
    vata_pts += 6 # Mercury

    pitta_pts += 10 # Mars
    pitta_pts += 10 # Sun
    pitta_pts += 8  # Ketu

    kapha_pts += 10 # Jupiter
    kapha_pts += 8  # Venus
    kapha_pts += 8  # Moon

    # 6th lord influence
    if h6_lord in ('Mars', 'Sun'): pitta_pts += 6
    elif h6_lord in ('Saturn', 'Mercury'): vata_pts += 6
    elif h6_lord in ('Jupiter', 'Venus', 'Moon'): kapha_pts += 6

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
        'lifestyle_guidance_ta': lifestyle_ta
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

    bav = chart.get('ashtakavarga', {}).get('BAV', {})
    kakshya_deg_step = 30.0 / 8.0 # 3.75 deg per Kakshya

    def build_kakshya_table(p_name, sign_idx, current_deg):
        current_k_idx = min(int(current_deg / kakshya_deg_step), 7)
        rows = []
        p_bav = bav.get(p_name, [0]*12)
        sign_pts = p_bav[sign_idx] if len(p_bav) > sign_idx else 4

        for k in range(8):
            start_d = k * kakshya_deg_step
            end_d = (k + 1) * kakshya_deg_step
            k_lord = KAKSHYA_LORDS[k]
            k_lord_ta = KAKSHYA_LORDS_TA[k]
            has_bindu = (k < sign_pts)
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
            'summary_en': f"Saturn transits Kakshya {sat_k_idx + 1} ({sat_curr['lord']}) in {SIGNS[sat_sign]}. Status: {sat_curr['status_en']}.",
            'summary_ta': f"சனி பகவான் {TAMIL_SIGNS[sat_sign]} ராசியில் {sat_k_idx + 1}-வது கக்ஷியாவில் ({sat_curr['lord_ta']}) சஞ்சரிக்கிறார். பலன்: {sat_curr['status_ta']}."
        },
        'jupiter': {
            'sign': SIGNS[jup_sign],
            'tamil_sign': TAMIL_SIGNS[jup_sign],
            'current_degree': f"{int(jup_deg)}°{int((jup_deg*60)%60):02d}′",
            'current_kakshya': jup_curr,
            'kakshya_timeline': jup_table,
            'summary_en': f"Jupiter transits Kakshya {jup_k_idx + 1} ({jup_curr['lord']}) in {SIGNS[jup_sign]}. Status: {jup_curr['status_en']}.",
            'summary_ta': f"குரு பகவான் {TAMIL_SIGNS[jup_sign]} ராசியில் {jup_k_idx + 1}-வது கக்ஷியாவில் ({jup_curr['lord_ta']}) சஞ்சரிக்கிறார். பலன்: {jup_curr['status_ta']}."
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
    lon = lon % 360
    sign_idx = int(lon // 30)
    sign_lord = SIGN_LORDS[sign_idx]
    
    star_span = 360.0 / 27.0
    star_idx = int(lon // star_span)
    star_name = STARS[star_idx % 27]
    star_lord = DASA_LORDS[star_idx % 9]
    
    arc_in_star = lon - (star_idx * star_span)
    start_lord_idx = DASA_LORDS.index(star_lord)
    accum = 0.0
    sub_lord = star_lord
    for i in range(9):
        curr_lord = DASA_LORDS[(start_lord_idx + i) % 9]
        sub_span = (star_span * VIMSHOTTARI_YEARS[curr_lord]) / 120.0
        if accum <= arc_in_star < (accum + sub_span + 1e-9):
            sub_lord = curr_lord
            break
        accum += sub_span
    return sign_idx, SIGNS[sign_idx], TAMIL_SIGNS[sign_idx], sign_lord, star_name, star_lord, sub_lord

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

    return {
        'dominant_planet': dominant,
        'vulnerable_planet': vulnerable,
        'adequate_count': len(adequate),
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
def calculate_kp_system(chart):
    planets = chart['planets']
    kp_cusps = chart.get('kp_cusps', [])
    if not kp_cusps or len(kp_cusps) < 12:
        asc_lon = planets['Ascendant']['longitude']
        kp_cusps = [(asc_lon + i * 30) % 360 for i in range(12)]

    cusp_rows = []
    for idx, lon in enumerate(kp_cusps):
        sign_idx, sign_name, sign_ta, sign_lord, star_name, star_lord, sub_lord = get_kp_sublord(lon)
        deg_in_sign = lon % 30
        d = int(deg_in_sign); m = int((deg_in_sign * 60) % 60); s = int((deg_in_sign * 3600) % 60)
        cusp_rows.append({
            'cusp': idx + 1,
            'longitude': round(lon, 4),
            'degree_str': f"{d}° {m:02d}′ {s:02d}″",
            'sign': sign_name,
            'sign_ta': sign_ta,
            'sign_lord': sign_lord,
            'sign_lord_ta': PLANET_TAMIL.get(sign_lord, sign_lord),
            'star_name': star_name,
            'star_lord': star_lord,
            'star_lord_ta': PLANET_TAMIL.get(star_lord, star_lord),
            'sub_lord': sub_lord,
            'sub_lord_ta': PLANET_TAMIL.get(sub_lord, sub_lord)
        })

    planet_rows = []
    for p_name in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']:
        lon = planets[p_name]['longitude']
        sign_idx, sign_name, sign_ta, sign_lord, star_name, star_lord, sub_lord = get_kp_sublord(lon)
        deg_in_sign = lon % 30
        d = int(deg_in_sign); m = int((deg_in_sign * 60) % 60); s = int((deg_in_sign * 3600) % 60)
        planet_rows.append({
            'planet': p_name,
            'planet_ta': PLANET_TAMIL[p_name],
            'degree_str': f"{d}° {m:02d}′ {s:02d}″",
            'sign': sign_name,
            'sign_ta': sign_ta,
            'sign_lord': sign_lord,
            'sign_lord_ta': PLANET_TAMIL.get(sign_lord, sign_lord),
            'star_name': star_name,
            'star_lord': star_lord,
            'star_lord_ta': PLANET_TAMIL.get(star_lord, star_lord),
            'sub_lord': sub_lord,
            'sub_lord_ta': PLANET_TAMIL.get(sub_lord, sub_lord)
        })

    c1_sub = cusp_rows[0]['sub_lord']
    c2_sub = cusp_rows[1]['sub_lord']
    c5_sub = cusp_rows[4]['sub_lord']
    c7_sub = cusp_rows[6]['sub_lord']
    c10_sub = cusp_rows[9]['sub_lord']
    c11_sub = cusp_rows[10]['sub_lord']

    kp_interpretations = {
        'cusp_1': {
            'cusp_num': 1,
            'title_en': '1st Cusp Sub-Lord (Physical Constitution & Self-Agency)',
            'title_ta': '1-ஆம் பாவ உப-அதிபதி (உடல் நலம், சுய கௌரவம் & ஆயுள் பலம்)',
            'sub_lord': c1_sub,
            'sub_lord_ta': PLANET_TAMIL.get(c1_sub, c1_sub),
            'reading_en': f"1st Cusp sub-lord is {c1_sub}. In KP astrology, this sub-lord governs physical vitality, innate inclinations, and health resilience. {c1_sub}'s connection with auspicious houses grants strong recovery power and dignified self-direction.",
            'reading_ta': f"லக்ன பாவத்தின் உப-அதிபதி {PLANET_TAMIL.get(c1_sub, c1_sub)} ஆகும். கே.பி. விதிகளின்படி இது உடல் ஆரோக்கியம், தனித்துவமான செயல் திறன் மற்றும் நோய்களை எதிர்க்கும் ஆற்றலை நிர்ணயிக்கிறது. சுப ஸ்தான தொடர்புகளால் நீண்ட ஆயுளும் நற்புகழும் கிட்டும்."
        },
        'cusp_2': {
            'cusp_num': 2,
            'title_en': '2nd Cusp Sub-Lord (Financial Inflow & Family Wealth)',
            'title_ta': '2-ஆம் பாவ உப-அதிபதி (தன வரவு, வாக்கு வன்மை & குடும்ப செல்வம்)',
            'sub_lord': c2_sub,
            'sub_lord_ta': PLANET_TAMIL.get(c2_sub, c2_sub),
            'reading_en': f"2nd Cusp sub-lord is {c2_sub}. Controls liquid assets, speech eloquence, and monetary accumulation. As {c2_sub} signifies wealth channels, earnings grow steadily through systematic investments and credible partnerships.",
            'reading_ta': f"2-ஆம் பாவத்தின் உப-அதிபதி {PLANET_TAMIL.get(c2_sub, c2_sub)} ஆகும். இது நிதி திரட்டுதல், வாக்குப் பலம் மற்றும் குடும்ப பொருளாதார ஸ்திரத்தன்மையை வழிநடத்துகிறது. வங்கி இருப்பு மற்றும் சேமிப்பு படிப்படியாக உயரும்."
        },
        'cusp_5': {
            'cusp_num': 5,
            'title_en': '5th Cusp Sub-Lord (Creative Intellect & Speculative Wisdom)',
            'title_ta': '5-ஆம் பாவ உப-அதிபதி (பூர்வ புண்ணியம், புத்தி கூர்மை & புத்திர யோகம்)',
            'sub_lord': c5_sub,
            'sub_lord_ta': PLANET_TAMIL.get(c5_sub, c5_sub),
            'reading_en': f"5th Cusp sub-lord is {c5_sub}. Determines creative breakthroughs, artistic intuition, and speculative intelligence. Inspires fruitful intellectual pursuits and harmonious progeny relations.",
            'reading_ta': f"5-ஆம் பாவ உப-அதிபதி {PLANET_TAMIL.get(c5_sub, c5_sub)} ஆகும். இது பூர்வ புண்ணியம், ஆக்கப்பூர்வமான சிந்தனை, கலை ஆர்வம் மற்றும் பிள்ளைகளின் மேன்மையை குறிக்கிறது. கற்பனை ஆற்றலும் புதிய திட்டங்களை வகுக்கும் திறனும் சிறக்கும்."
        },
        'cusp_7': {
            'cusp_num': 7,
            'title_en': '7th Cusp Sub-Lord (Spouse Nature & Partnership Harmony)',
            'title_ta': '7-ஆம் பாவ உப-அதிபதி (களத்திர பாக்கியம், துணைவரின் குணம் & கூட்டுத் தொழில்)',
            'sub_lord': c7_sub,
            'sub_lord_ta': PLANET_TAMIL.get(c7_sub, c7_sub),
            'reading_en': f"7th Cusp sub-lord is {c7_sub}. In KP doctrine, this sub-lord governs marital timing, spouse temperament, and commercial alliances. Bestows a loyal, supportive partner with compatible values.",
            'reading_ta': f"7-ஆம் பாவ உப-அதிபதி {PLANET_TAMIL.get(c7_sub, c7_sub)} ஆகும். இது திருமண வாழ்க்கை, துணைவரின் குணாதிசயம் மற்றும் வணிகக் கூட்டாளிகளைத் தீர்மானிக்கிறது. அன்பான, குடும்ப நலனில் அக்கறை கொண்ட துணைவர் அமைவார்."
        },
        'cusp_10': {
            'cusp_num': 10,
            'title_en': '10th Cusp Sub-Lord (Professional Eminence & Social Status)',
            'title_ta': '10-ஆம் பாவ உப-அதிபதி (தொழில் வெற்றி, சமூக அந்தஸ்து & அதிகார யோகம்)',
            'sub_lord': c10_sub,
            'sub_lord_ta': PLANET_TAMIL.get(c10_sub, c10_sub),
            'reading_en': f"10th Cusp sub-lord is {c10_sub}. Determines career zenith, authority in enterprise, and societal reputation. Endows focused execution, leading to commanding recognition in your field.",
            'reading_ta': f"10-ஆம் பாவ உப-அதிபதி {PLANET_TAMIL.get(c10_sub, c10_sub)} ஆகும். இது தொழில் மேன்மை, அரசு மற்றும் உயர்மட்ட நிர்வாகத்தில் செல்வாக்கு, மற்றும் சமூக நற்பெயரைத் தரும். விடாமுயற்சியால் உயர்பதவிகளை அடைவீர்கள்."
        },
        'cusp_11': {
            'cusp_num': 11,
            'title_en': '11th Cusp Sub-Lord (Fulfillment of Desires & Profitability)',
            'title_ta': '11-ஆம் பாவ உப-அதிபதி (லாப ஸ்தானம், விருப்பங்கள் நிறைவேறுதல் & நண்பர்கள்)',
            'sub_lord': c11_sub,
            'sub_lord_ta': PLANET_TAMIL.get(c11_sub, c11_sub),
            'reading_en': f"11th Cusp sub-lord is {c11_sub}. In KP principles, the 11th cusp is the crown of fulfillment. Confirms that ambitious life aspirations and financial milestones will manifest successfully.",
            'reading_ta': f"11-ஆம் பாவ உப-அதிபதி {PLANET_TAMIL.get(c11_sub, c11_sub)} ஆகும். இது அனைத்து ஆசைகளும் ஈடேறுவதையும், தொழில் லாபம் மற்றும் விசுவாசமான நண்பர்களின் ஆதரவையும் உறுதி செய்கிறது."
        }
    }

    return {
        'cusps': cusp_rows,
        'planets': planet_rows,
        'cuspal_predictions': kp_interpretations
    }

# 3. BHRIGU NANDI NADI (BNN)
def calculate_bhrigu_nandi_nadi(chart):
    planets = chart['planets']
    trine_map = {
        'dharma_fire': {'name_en': 'Dharma Trine (Fire: Aries, Leo, Sagittarius)', 'name_ta': 'தர்ம திரிகோணம் (நெருப்பு: மேஷம், சிம்மம், தனுசு)', 'planets': []},
        'artha_earth': {'name_en': 'Artha Trine (Earth: Taurus, Virgo, Capricorn)', 'name_ta': 'அர்த்த திரிகோணம் (நிலம்: ரிஷபம், கன்னி, மகரம்)', 'planets': []},
        'kama_air': {'name_en': 'Kama Trine (Air: Gemini, Libra, Aquarius)', 'name_ta': 'காம திரிகோணம் (காற்று: மிதுனம், துலாம், கும்பம்)', 'planets': []},
        'moksha_water': {'name_en': 'Moksha Trine (Water: Cancer, Scorpio, Pisces)', 'name_ta': 'மோட்ச திரிகோணம் (நீர்: கடகம், விருச்சிகம், மீனம்)', 'planets': []}
    }

    p_names = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
    p_trine = {}
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
        p_trine[p_name] = t_key

    sutras = []
    def in_same_trine(p1, p2):
        return p_trine[p1] == p_trine[p2]

    if in_same_trine('Jupiter', 'Saturn'):
        sutras.append({
            'title_en': 'Dharma-Karma Adhipati Yoga (Guru + Shani)',
            'title_ta': 'தர்ம-கர்மாதிபதி யோகம் (குரு + சனி சேர்க்கை)',
            'planets': ['Jupiter', 'Saturn'],
            'significance_en': 'The Divine Worker Sutra. Conjoins Jeeva Karaka (Soul) with Karma Karaka (Duty). Bestows deep sense of social duty, ethical professional standing, steady perseverance through initial delays, and celebrated eminence after age 32.',
            'significance_ta': 'ஜீவகாரகன் குருவும் கர்மகாரகன் சனியும் திரிகோணத்தில் இணைவதால் உண்டாகும் உன்னத யோகம். தொடக்கத்தில் உழைப்புக்கேற்ற அங்கீகாரம் சற்றே தாமதமானாலும், 32 வயதிற்குப் பின் அழியாத நற்பெயரும், உயர்ந்த பதவியும், சமூக மரியாதையும் கிட்டும்.'
        })

    if in_same_trine('Jupiter', 'Mars'):
        sutras.append({
            'title_en': 'Deva-Senapati Yoga (Guru + Mangala)',
            'title_ta': 'தேவ-சேனாதிபதி யோகம் (குரு + செவ்வாய் சேர்க்கை)',
            'planets': ['Jupiter', 'Mars'],
            'significance_en': 'Courageous Leader Sutra. Melds divine wisdom with energetic vigor. Bestows commanding executive power, technical/engineering acumen, real estate prosperity, and protective championship of family interests.',
            'significance_ta': 'குருவும் செவ்வாயும் இணைவதால் அஞ்சாத தைரியம், பூமி-மனை யோகம், பொறியியல்/தொழில்நுட்ப ஆளுமை மற்றும் தலைமை நிர்வாகப் பொறுப்புகள் அமையும்.'
        })

    if in_same_trine('Jupiter', 'Venus'):
        sutras.append({
            'title_en': 'Bhrigu-Guru Yoga (Jupiter + Venus)',
            'title_ta': 'பிருகு-குரு யோகம் (குரு + சுக்கிரன் சேர்க்கை)',
            'planets': ['Jupiter', 'Venus'],
            'significance_en': 'Abundant Fortune Sutra. Harmonizes the two supreme benefics (Deva Guru & Asura Guru). Bestows immense material affluence, refined aesthetic taste, virtuous life companion, and peaceful family prosperity.',
            'significance_ta': 'இரு பெரும் சுப கிரகங்களான குருவும் சுக்கிரனும் இணையும் மகா சுப யோகம். பொன், பொருள் சேர்க்கை, வாகன யோகம், குடும்ப மகிழ்ச்சி மற்றும் ஆடம்பர வசதிகள் இயல்பாகவே அமையும்.'
        })

    if in_same_trine('Jupiter', 'Mercury'):
        sutras.append({
            'title_en': 'Saraswati Yoga (Guru + Budha)',
            'title_ta': 'சரஸ்வதி யோகம் (குரு + புதன் சேர்க்கை)',
            'planets': ['Jupiter', 'Mercury'],
            'significance_en': 'Master of Wisdom & Commerce. Fosters multifaceted intellectual depth, teaching mastery, linguistic wit, successful business enterprise, and diplomatic counsel.',
            'significance_ta': 'குருவும் புதனும் இணைவதால் வாக்கு வன்மை, எழுத்து, கணிதம், ஜோதிடம், மற்றும் வர்த்தகத் துறைகளில் தனி முத்திரை பதிக்கும் கல்வி ஞானம் உண்டாகும்.'
        })

    if in_same_trine('Jupiter', 'Sun'):
        sutras.append({
            'title_en': 'Shiva-Raja Yoga (Guru + Surya)',
            'title_ta': 'சிவ-ராஜ யோகம் (குரு + சூரியன் சேர்க்கை)',
            'planets': ['Jupiter', 'Sun'],
            'significance_en': 'Honor & Regal Dignity. Grants divine protection, paternal blessings, ethical leadership, and honors from governmental or high corporate bodies.',
            'significance_ta': 'சூரியனும் குருவும் இணைவதால் தந்தை வழியில் பெருமை, அரசு வழியில் ஆதரவு, கம்பீரமான தோற்றம் மற்றும் நேர்மையான வழியில் உயர்ந்த கௌரவம் கிட்டும்.'
        })

    if in_same_trine('Jupiter', 'Rahu'):
        sutras.append({
            'title_en': 'Guru-Chandal / Revolutionary Mind (Guru + Rahu)',
            'title_ta': 'விஞ்ஞான புத்தி யோகம் (குரு + ராகு சேர்க்கை)',
            'planets': ['Jupiter', 'Rahu'],
            'significance_en': 'Unconventional Innovator. Drives revolutionary thinking that challenges traditional dogmas. Strongly favors overseas travels, cutting-edge technology, foreign networks, and unconventional success.',
            'significance_ta': 'குருவும் ராகுவும் இணைவதால் பழமைவாதத்தைத் தாண்டி நவீன அறிவியல், கணினி மற்றும் வெளிநாட்டு தொடர்புகளால் பெரிய முன்னேற்றத்தை அடையும் ஆற்றல் உண்டு.'
        })

    if in_same_trine('Jupiter', 'Ketu'):
        sutras.append({
            'title_en': 'Gnana Mukti Yoga (Guru + Ketu)',
            'title_ta': 'ஞான முக்தி யோகம் (குரு + கேது சேர்க்கை)',
            'planets': ['Jupiter', 'Ketu'],
            'significance_en': 'Spiritual Seeker & Mystic. Bestows philosophical detachment, profound intuitive faculties, natural healing talents, and attraction to meditation, astrology, or higher metaphysics.',
            'significance_ta': 'ஞானகாரகன் கேதுவும் குருவும் இணைவதால் இறை பக்தி, உள்ளுணர்வு, ஜோதிடம் மற்றும் ஆன்மீக ஆராய்ச்சியில் அதீத ஞானம் உண்டாகும்.'
        })

    if in_same_trine('Saturn', 'Venus'):
        sutras.append({
            'title_en': 'Lakshmi-Karma Yoga (Shani + Shukra)',
            'title_ta': 'லட்சுமி-கர்ம யோகம் (சனி + சுக்கிரன் சேர்க்கை)',
            'planets': ['Saturn', 'Venus'],
            'significance_en': 'Prosperity through Enterprise. Karma Karaka meets Dhanakaraka. Bestows steady accumulation of durable assets, success in corporate/luxury industries, and a supportive partner.',
            'significance_ta': 'சனி மற்றும் சுக்கிரன் இணைவதால் கடின உழைப்பு பெரும் செல்வமாக மாறும். நிலையான அசையாச் சொத்துக்கள் மற்றும் தொழில் மூலமாக நிரந்தர வருமானம் பெருகும்.'
        })

    if in_same_trine('Saturn', 'Mercury'):
        sutras.append({
            'title_en': 'Vyapara Yoga (Shani + Budha)',
            'title_ta': 'வியாபார யோகம் (சனி + புதன் சேர்க்கை)',
            'planets': ['Saturn', 'Mercury'],
            'significance_en': 'Master of Commerce & Logistics. Combines patient discipline with analytical calculation. Highly favored for auditing, legal trade, software development, and large-scale commerce.',
            'significance_ta': 'சனி மற்றும் புதன் இணைவதால் கணக்கு, தணிக்கை, மென்பொருள் மற்றும் வணிக மேலாண்மையில் நுட்பமான நிபுணத்துவம் பெற்று தொழிலில் வெற்றி பெறுவீர்கள்.'
        })

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
    nav_sign = moon.get('navamsa', 'Aries')
    nav_idx = SIGNS.index(nav_sign) if nav_sign in SIGNS else 0
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
def calculate_sahams(chart):
    planets = chart['planets']
    asc_lon = planets['Ascendant']['longitude']
    sun_lon = planets['Sun']['longitude']
    moon_lon = planets['Moon']['longitude']
    sat_lon = planets['Saturn']['longitude']
    ven_lon = planets['Venus']['longitude']
    is_day = planets['Sun']['house'] in (7, 8, 9, 10, 11, 12)

    punya_lon = (asc_lon + moon_lon - sun_lon) % 360 if is_day else (asc_lon + sun_lon - moon_lon) % 360
    vidya_lon = (asc_lon + sun_lon - moon_lon) % 360 if is_day else (asc_lon + moon_lon - sun_lon) % 360
    vivaha_lon = (asc_lon + ven_lon - sat_lon) % 360
    karma_lon = (asc_lon + sun_lon - sat_lon) % 360 if is_day else (asc_lon + sat_lon - sun_lon) % 360
    roga_lon = (asc_lon + moon_lon - sat_lon) % 360

    sahams_data = [
        ('Punya Saham', 'புண்ணிய சஹாம்', punya_lon, 'Fortune & Divine Merit', 'அதிர்ஷ்டம் & பூர்வ புண்ணியம்',
         'Point of divine grace and fortune. Signifies sudden favorable turns of fate, spiritual merit, and virtuous prosperity.',
         'தெய்வ அனுகூலம் மற்றும் பூர்வ புண்ணியப் புள்ளி. எதிர்பாராத அதிர்ஷ்ட வாய்ப்புகள் மற்றும் தர்ம காரியங்களால் வாழ்வில் உயர்வு தரும்.'),
        ('Vidya Saham', 'வித்யா சஹாம்', vidya_lon, 'Intellect & Higher Learning', 'கல்வி ஞானம் & ஆராய்ச்சி அறிவு',
         'Point of deep intellect and scholarship. Enhances analytical perception, academic laurels, and quick comprehension.',
         'உயர்ந்த அறிவு மற்றும் கல்வித் திறன் புள்ளி. கூரிய புத்தி, ஆராய்ச்சி ஆர்வம் மற்றும் நிபுணத்துவத்தை வளர்க்கும்.'),
        ('Vivaha Saham', 'விவாக சஹாம்', vivaha_lon, 'Sacred Marriage & Partnerships', 'திருமண யோகம் & தாம்பத்தியம்',
         'Point of marital harmony and contracts. Dictates emotional compatibility, wedding timing, and lasting mutual devotion.',
         'தாம்பத்திய சுகம் மற்றும் திருமணப் புள்ளி. துணைவருடன் நல்லிணக்கம், குடும்பப் பொறுப்பு மற்றும் விசுவாசமான உறவை உறுதி செய்யும்.'),
        ('Karma Saham', 'கர்மா சஹாம்', karma_lon, 'Career Eminence & Authority', 'தொழில் மேன்மை & சமூக அந்தஸ்து',
         'Point of worldly action and social legacy. Signals career zenith, authority over teams, and lasting societal respect.',
         'சமூக அந்தஸ்து மற்றும் அதிகாரப் புள்ளி. தொழிலில் உயர்ந்த தலைமைப் பொறுப்பு, சமூக கௌரவம் மற்றும் நிலைத்த புகழைத் தரும்.'),
        ('Roga Saham', 'ரோக சஹாம்', roga_lon, 'Physical Resilience & Healing', 'உடல் எதிர்ப்பு சக்தி & ஆரோக்கியம்',
         'Point of health sensitivity and bodily immunity. Advises balanced lifestyle rhythms to preserve enduring vitality.',
         'உடல் ஆரோக்கியம் மற்றும் நோய் எதிர்ப்பு சக்திப் புள்ளி. முறையான உணவுப் பழக்கம் மற்றும் தியானத்தால் பூரண நல்வாழ்வு பெறலாம்.')
    ]

    sahams_list = []
    for en_title, ta_title, lon, kw_en, kw_ta, r_en, r_ta in sahams_data:
        s_idx = int(lon // 30)
        deg = lon % 30
        h_from_asc = (s_idx - planets['Ascendant']['sign_index']) % 12 + 1
        d = int(deg); m = int((deg * 60) % 60)
        sahams_list.append({
            'name_en': en_title,
            'name_ta': ta_title,
            'longitude': round(lon, 2),
            'degree_str': f"{d}° {m:02d}′",
            'sign': SIGNS[s_idx],
            'tamil_sign': TAMIL_SIGNS[s_idx],
            'house': h_from_asc,
            'keyword_en': kw_en,
            'keyword_ta': kw_ta,
            'reading_en': r_en,
            'reading_ta': r_ta
        })

    return {
        'is_day_birth': is_day,
        'birth_type_en': 'Diurnal (Day Birth)' if is_day else 'Nocturnal (Night Birth)',
        'birth_type_ta': 'பகல் பிறப்பு' if is_day else 'இரவு பிறப்பு',
        'sahams': sahams_list
    }

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
    bhavas = generate_bhava_predictions(house_details, planets)
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
