"""Life readings: the birth star and Lagna, the twelve bhavas, grahas in houses, the running
Dasa-Bhukti, transits (Sade Sati, Jupiter, Rahu-Ketu), and lucky factors and gemstones.
"""

from datetime import datetime
from zoneinfo import ZoneInfo

from .common import (
    DIGNITY_PHRASE, DIGNITY_PHRASE_ML, DIGNITY_SCORE, DIG_BALA_HOUSE, DUSTHANAS, HOUSE_THEMES, HOUSE_THEMES_ML, KENDRAS,
    MALAYALAM_SIGNS, NATURAL_BENEFICS, PLANET_ML, PLANET_ML_CASE, PLANET_TAMIL, SIGNS, SIGN_LORDS, TRIKONAS, UPACHAYAS, VERDICT_ML, VERDICT_TAMIL,
    _functional_role, _house_list, _ordinal, _owned_houses, _verdict
)


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

# 3. 12 Bhavas (House-by-House) Detailed Predictions Engine
BHAVA_TITLES_ML = [
    'ഒന്നാം ഭാവം (തനു / ലഗ്നം)', 'രണ്ടാം ഭാവം (ധനം / വാക്ക്)', 'മൂന്നാം ഭാവം (സഹജം / ധൈര്യം)', 'നാലാം ഭാവം (സുഖം / മാതാവ്)',
    'അഞ്ചാം ഭാവം (പുത്രൻ / പൂർവ്വപുണ്യം)', 'ആറാം ഭാവം (ശത്രു / രോഗം / കടം)', 'ഏഴാം ഭാവം (കളത്രം / വിവാഹം)',
    'എട്ടാം ഭാവം (ആയുസ്സ്)', 'ഒൻപതാം ഭാവം (ഭാഗ്യം / ധർമ്മം)', 'പത്താം ഭാവം (കർമ്മം / തൊഴിൽ)', 'പതിനൊന്നാം ഭാവം (ലാഭം)',
    'പന്ത്രണ്ടാം ഭാവം (വ്യയം / മോക്ഷം)'
]
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

        themes_ml = HOUSE_THEMES_ML[h_num]
        lord_themes_ml = HOUSE_THEMES_ML[lord_house]
        lord_ml = PLANET_ML.get(lord, lord)

        # Each factor: (English, Tamil, effect on the house, Malayalam)
        factors = []
        dig_en, dig_ta = DIGNITY_PHRASE.get(lord_dignity, DIGNITY_PHRASE['Neutral'])
        dig_ml = DIGNITY_PHRASE_ML.get(lord_dignity, DIGNITY_PHRASE_ML['Neutral'])
        dig_score = DIGNITY_SCORE.get(lord_dignity, 0)
        factors.append((f"Lord {lord} is in {dig_en}", f"அதிபதி {lord_ta} {dig_ta} உள்ளார்", dig_score,
                        f"ഭാവാധിപൻ {lord_ml} {dig_ml}"))
        if lord_house in DUSTHANAS:
            if h_num in DUSTHANAS:
                factors.append((f"A dusthana lord hidden in the {_ordinal(lord_house)} house weakens this house's troubles (Vipareeta)",
                                f"மறைவு ஸ்தான அதிபதி {lord_house}-ம் பாவத்தில் மறைந்ததால் இப்பாவத்தின் தீமைகள் குறையும் (விபரீதம்)", 1,
                                f"ദുഃസ്ഥാനാധിപൻ {lord_house}-ാം ഭാവത്തിൽ മറഞ്ഞതിനാൽ ഈ ഭാവത്തിന്റെ ദോഷങ്ങൾ കുറയും (വിപരീതം)"))
            else:
                factors.append((f"Lord placed in the {_ordinal(lord_house)} house, a dusthana",
                                f"அதிபதி {lord_house}-ம் பாவம் எனும் மறைவு ஸ்தானத்தில்", -1,
                                f"ഭാവാധിപൻ ദുഃസ്ഥാനമായ {lord_house}-ാം ഭാവത്തിൽ"))
        elif lord_house in KENDRAS + TRIKONAS:
            factors.append((f"Lord well placed in the {_ordinal(lord_house)} house (kendra/trikona)",
                            f"அதிபதி {lord_house}-ம் பாவம் எனும் கேந்திர/திரிகோண ஸ்தானத்தில்", 1,
                            f"ഭാവാധിപൻ കേന്ദ്ര/ത്രികോണമായ {lord_house}-ാം ഭാവത്തിൽ നല്ല നിലയിൽ"))
        if lord_data.get('combust'):
            factors.append((f"Lord {lord} is combust", f"அதிபதி {lord_ta} அஸ்தங்கம்", -1, f"ഭാവാധിപൻ {lord_ml} മൗഢ്യത്തിൽ"))
        for occ in occupants:
            occ_ta = PLANET_TAMIL[occ]
            occ_ml = PLANET_ML[occ]
            if occ in NATURAL_BENEFICS:
                if h_num in DUSTHANAS:
                    factors.append((f"Benefic {occ} here spends its goodness on {themes_en}",
                                    f"சுபர் {occ_ta} இங்கு இருப்பதால் நற்பலன் குறைவாகவே கிடைக்கும்", 0,
                                    f"ശുഭനായ {occ_ml} ഇവിടെ നിൽക്കുന്നതിനാൽ നല്ല ഫലം കുറവായേ ലഭിക്കൂ"))
                else:
                    factors.append((f"Benefic {occ} occupies the house", f"சுபர் {occ_ta} இப்பாவத்தில் உள்ளார்", 1,
                                    f"ശുഭനായ {occ_ml} ഈ ഭാവത്തിൽ നിൽക്കുന്നു"))
            elif h_num in UPACHAYAS:
                factors.append((f"Malefic {occ} thrives in this upachaya house", f"பாவர் {occ_ta} உபசய ஸ்தானத்தில் வலுப்பெறுகிறார்", 1,
                                f"പാപനായ {occ_ml} ഉപചയ ഭാവത്തിൽ ബലം നേടുന്നു"))
            else:
                factors.append((f"Malefic {occ} occupies the house", f"பாவர் {occ_ta} இப்பாவத்தில் உள்ளார்", -1,
                                f"പാപനായ {occ_ml} ഈ ഭാവത്തിൽ നിൽക്കുന്നു"))
        if 'Jupiter' in aspected_by:
            factors.append(("Jupiter's aspect protects the house", 'குருவின் பார்வை இப்பாவத்தைக் காக்கிறது', 1,
                            'വ്യാഴത്തിന്റെ ദൃഷ്ടി ഈ ഭാവത്തെ സംരക്ഷിക്കുന്നു'))
        for mal in ('Saturn', 'Mars'):
            if mal in aspected_by and h_num not in UPACHAYAS:
                factors.append((f"{mal}'s aspect brings pressure and delays", f"{PLANET_TAMIL[mal]} பார்வை தடைகளையும் அழுத்தத்தையும் தரும்", -1,
                                f"{PLANET_ML_CASE['gen'][mal]} ദൃഷ്ടി തടസ്സങ്ങളും സമ്മർദ്ദവും നൽകും"))
        rupas = round(bhava_bala[h_num - 1]['rupas'], 2) if bhava_bala else None
        if rupas is not None and rupas >= 9:
            factors.append((f"Bhava Bala of {rupas} rupas, well above the minimum of 7",
                            f"பாவ பலம் {rupas} ரூபம், குறைந்தபட்ச அளவான 7-ஐ விட நன்கு அதிகம்", 1,
                            f"ഭാവബലം {rupas} രൂപ, കുറഞ്ഞ അളവായ 7-നേക്കാൾ ഏറെ കൂടുതൽ"))
        elif rupas is not None and rupas < 7:
            factors.append((f"Bhava Bala of only {rupas} rupas, below the minimum of 7",
                            f"பாவ பலம் {rupas} ரூபம் மட்டுமே, குறைந்தபட்ச அளவான 7-க்குக் கீழ்", -1,
                            f"ഭാവബലം {rupas} രൂപ മാത്രം, കുറഞ്ഞ അളവായ 7-ൽ താഴെ"))
        if sav >= 30:
            factors.append((f"{sav} Ashtakavarga bindus, above the average of 28", f"{sav} அஷ்டகவர்க்கப் பரல்கள் (சராசரி 28-க்கு மேல்)", 1,
                            f"{sav} അഷ്ടകവർഗ്ഗ ബിന്ദുക്കൾ (ശരാശരി 28-ൽ കൂടുതൽ)"))
        elif sav < 25:
            factors.append((f"Only {sav} Ashtakavarga bindus, below the average of 28", f"{sav} அஷ்டகவர்க்கப் பரல்கள் மட்டுமே (சராசரி 28-க்குக் கீழ்)", -1,
                            f"{sav} അഷ്ടകവർഗ്ഗ ബിന്ദുക്കൾ മാത്രം (ശരാശരി 28-ൽ താഴെ)"))

        score = sum(f[2] for f in factors)
        verdict = _verdict(score)
        occ_en = ', '.join(occupants) if occupants else ''
        occ_ta = ', '.join(PLANET_TAMIL[o] for o in occupants)
        occ_ml = ', '.join(PLANET_ML[o] for o in occupants)

        if verdict == 'strong':
            close_en = f"Overall this is a strong house: {themes_en} flourish with steady support."
            close_ta = f"மொத்தத்தில் இது பலம் வாய்ந்த பாவம்: {themes_ta} ஆகியவை சிறப்பாக அமையும்."
            close_ml = f"മൊത്തത്തിൽ ഇത് ബലമുള്ള ഭാവമാണ്: {themes_ml} എന്നിവ നന്നായി അഭിവൃദ്ധിപ്പെടും."
        elif verdict == 'weak':
            close_en = f"Overall this house needs care: {themes_en} may meet delays, and strengthening {lord} through its remedies helps."
            close_ta = f"மொத்தத்தில் இப்பாவம் கவனம் தேவைப்படுவது: {themes_ta} ஆகியவற்றில் தாமதங்கள் வரலாம்; {lord_ta} கிரகத்திற்கான பரிகாரங்கள் நலம் தரும்."
            close_ml = f"മൊത്തത്തിൽ ഈ ഭാവത്തിന് ശ്രദ്ധ വേണം: {themes_ml} എന്നിവയിൽ കാലതാമസം ഉണ്ടാകാം; {PLANET_ML_CASE['dat'].get(lord, lord_ml)} വേണ്ടിയുള്ള പരിഹാരങ്ങൾ ഗുണം ചെയ്യും."
        else:
            close_en = f"Overall a moderate house: {themes_en} give mixed results that improve with effort."
            close_ta = f"மொத்தத்தில் மத்திமமான பாவம்: {themes_ta} ஆகியவை முயற்சிக்கேற்ப மேம்படும்."
            close_ml = f"മൊത്തത്തിൽ മധ്യമമായ ഭാവം: {themes_ml} എന്നിവ പ്രയത്നത്തിനനുസരിച്ച് മെച്ചപ്പെടും."

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
        sign_ml = MALAYALAM_SIGNS[SIGNS.index(h_info['sign'])] if h_info['sign'] in SIGNS else h_info['sign']
        lord_state_ml = ('മൗഢ്യത്തിലും ' if lord_data.get('combust') else '') + \
            ('വക്രത്തിലും ' if lord_data.get('retrograde') and lord not in ('Rahu', 'Ketu') else '')
        pred_ml = (
            f"{themes_ml} എന്നിവ സൂചിപ്പിക്കുന്ന {h_num}-ാം ഭാവം {sign_ml} രാശിയിലാണ്. ഇതിന്റെ അധിപൻ {lord_ml} "
            f"{lord_state_ml}{lord_house}-ാം ഭാവത്തിൽ {dig_ml} നിൽക്കുന്നു"
            + (f"; അതിനാൽ ഈ ഫലങ്ങൾ {lord_themes_ml} എന്നിവയുമായി ബന്ധപ്പെടുന്നു. " if lord_house != h_num else '; സ്വന്തം ഭാവത്തെ സംരക്ഷിക്കുന്നു. ')
            + (f"ഈ ഭാവത്തിൽ {occ_ml} നിൽക്കുന്നു. " if occupants
               else 'ഈ ഭാവത്തിൽ ഗ്രഹങ്ങളില്ല; ഭാവാധിപന്റെ നിലയാണ് ഫലം നിശ്ചയിക്കുന്നത്. ')
            + f"ഇതിന് {sav} അഷ്ടകവർഗ്ഗ ബിന്ദുക്കളുണ്ട്. {close_ml}"
        )

        predictions.append({
            'house': h_num,
            'title_en': title_en,
            'title_ta': title_ta,
            'title_ml': BHAVA_TITLES_ML[h_num - 1],
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
            'strength_ml': VERDICT_ML[verdict],
            'score': score,
            'factors': [{'en': en, 'ta': ta, 'ml': ml, 'effect': effect} for en, ta, effect, ml in factors],
            'prediction_en': pred_en,
            'prediction_ta': pred_ta,
            'prediction_ml': pred_ml
        })

    return predictions

# 4. Planets in Houses Predictions (Sun to Ketu in 12 Houses)
P_ROLES_ML = {
    'Sun': 'ആത്മബലം, അച്ഛൻ, സർക്കാർ', 'Moon': 'മനസ്സ്, മാതൃസ്നേഹം, ഭാവന', 'Mars': 'ധൈര്യം, ഭൂമി, വീര്യം',
    'Mercury': 'ബുദ്ധി, വിദ്യ, വ്യാപാരം', 'Jupiter': 'ജ്ഞാനം, ധനം, സന്താനഭാഗ്യം', 'Venus': 'കല, ഐശ്വര്യം, ദാമ്പത്യസുഖം',
    'Saturn': 'ആയുസ്സ്, അധ്വാനം, നീതി', 'Rahu': 'ഭോഗം, വിദേശയോഗം, ആധുനിക മേഖലകൾ', 'Ketu': 'മോക്ഷം, ജ്ഞാനം, ആത്മീയത'
}
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
                       'இந்த லக்னத்திற்கு யோககாரகன்; கேந்திரமும் திரிகோணமும் ஆள்வதால் ஜாதகத்தின் மிகச் சிறந்த கிரகங்களில் ஒன்று',
                       'ഈ ലഗ്നത്തിന് യോഗകാരകൻ; കേന്ദ്രവും ത്രികോണവും ഭരിക്കുന്നതിനാൽ ജാതകത്തിലെ ഏറ്റവും ഗുണകരമായ ഗ്രഹങ്ങളിൽ ഒന്ന്'),
        'benefic': ('a functional benefic for this Lagna', 'இந்த லக்னத்திற்குச் சுப பலன் தரும் கிரகம்', 'ഈ ലഗ്നത്തിന് ശുഭഫലം നൽകുന്ന ഗ്രഹം'),
        'malefic': ('a functional malefic for this Lagna, as it rules a dusthana', 'மறைவு ஸ்தானம் ஆள்வதால் இந்த லக்னத்திற்குப் பாவ பலன் தரும் கிரகம்',
                    'ദുഃസ്ഥാനം ഭരിക്കുന്നതിനാൽ ഈ ലഗ്നത്തിന് പാപഫലം നൽകുന്ന ഗ്രഹം'),
        'neutral': ('functionally neutral for this Lagna', 'இந்த லக்னத்திற்குச் சம பலன் தரும் கிரகம்', 'ഈ ലഗ്നത്തിന് സമഫലം നൽകുന്ന ഗ്രഹം')
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
        themes_ml = HOUSE_THEMES_ML[h]
        name_ml = PLANET_ML[p_name]
        dig_en, dig_ta = DIGNITY_PHRASE.get(dignity, DIGNITY_PHRASE['Neutral'])
        dig_ml = DIGNITY_PHRASE_ML.get(dignity, DIGNITY_PHRASE_ML['Neutral'])
        is_benefic = p_name in NATURAL_BENEFICS

        score = DIGNITY_SCORE.get(dignity, 0)
        notes_en, notes_ta, notes_ml = [], [], []
        if is_benefic:
            if h in DUSTHANAS:
                score -= 1
                notes_en.append(f"As a natural benefic in the {_ordinal(h)} house, a dusthana, its kindness is spent on struggles and expenses.")
                notes_ta.append(f"இயற்கைச் சுபர் {h}-ம் பாவம் எனும் மறைவு ஸ்தானத்தில் இருப்பதால் அதன் நற்பலன் போராட்டங்களிலும் செலவுகளிலும் கரைகிறது.")
                notes_ml.append(f"സ്വാഭാവിക ശുഭൻ ദുഃസ്ഥാനമായ {h}-ാം ഭാവത്തിൽ നിൽക്കുന്നതിനാൽ അതിന്റെ നന്മ പോരാട്ടങ്ങളിലും ചെലവുകളിലും അലിയുന്നു.")
            elif h in KENDRAS + TRIKONAS:
                score += 1
                notes_en.append(f"A natural benefic in a kendra or trikona is one of the best placements, uplifting {themes_en}.")
                notes_ta.append(f"இயற்கைச் சுபர் கேந்திர/திரிகோணத்தில் இருப்பது சிறந்த அமைப்பு; {themes_ta} மேன்மை பெறும்.")
                notes_ml.append(f"സ്വാഭാവിക ശുഭൻ കേന്ദ്ര/ത്രികോണത്തിൽ നിൽക്കുന്നത് ഏറ്റവും നല്ല സ്ഥിതി; {themes_ml} ഉയർച്ച നേടും.")
        elif h in UPACHAYAS:
            score += 1
            notes_en.append(f"Natural malefics do well in upachaya houses; it builds strength and wins over {themes_en} with time.")
            notes_ta.append(f"பாவ கிரகங்கள் உபசய ஸ்தானத்தில் வலுப்பெறும்; காலப்போக்கில் {themes_ta} ஆகியவற்றில் வெற்றி தரும்.")
            notes_ml.append(f"പാപഗ്രഹങ്ങൾ ഉപചയ ഭാവങ്ങളിൽ ബലം നേടും; കാലക്രമേണ {themes_ml} എന്നിവയിൽ വിജയം നൽകും.")
        elif h in (1, 4, 5, 7, 9) and DIGNITY_SCORE.get(dignity, 0) < 2:
            score -= 1
            notes_en.append(f"As a natural malefic here it can strain {themes_en}, calling for patience.")
            notes_ta.append(f"இங்குள்ள பாவ கிரகம் {themes_ta} ஆகியவற்றில் சிரமம் தரலாம்; பொறுமை தேவை.")
            notes_ml.append(f"ഇവിടെയുള്ള പാപഗ്രഹം {themes_ml} എന്നിവയിൽ ബുദ്ധിമുട്ട് നൽകാം; ക്ഷമ വേണം.")
        if DIG_BALA_HOUSE.get(p_name) == h:
            score += 1
            notes_en.append("It enjoys directional strength (Dig Bala) in this house.")
            notes_ta.append("இப்பாவத்தில் திக் பலம் பெறுகிறது.")
            notes_ml.append("ഈ ഭാവത്തിൽ ദിഗ്ബലം നേടുന്നു.")
        if combust:
            score -= 1
            notes_en.append("Being combust, close to the Sun, its independent results are weakened.")
            notes_ta.append("சூரியனுக்கு அருகில் அஸ்தங்கம் பெற்றதால் தனித்த பலன்கள் குறையும்.")
            notes_ml.append("സൂര്യനോട് അടുത്ത് മൗഢ്യത്തിലായതിനാൽ സ്വതന്ത്ര ഫലങ്ങൾ കുറയും.")
        if retro:
            notes_en.append("Retrograde motion turns its energy inward: results come after reflection and second attempts.")
            notes_ta.append("வக்ர கதியால் அதன் சக்தி உள்நோக்கித் திரும்பும்; மறுமுயற்சிக்குப் பின் பலன் கிடைக்கும்.")
            notes_ml.append("വക്രഗതിയാൽ അതിന്റെ ഊർജ്ജം ഉള്ളിലേക്ക് തിരിയും; വീണ്ടും ശ്രമിച്ചശേഷം ഫലം ലഭിക്കും.")
        if 'Jupiter' in p_data.get('aspects_received', []) and p_name != 'Jupiter':
            score += 1
            notes_en.append("Jupiter's aspect adds protection and wisdom.")
            notes_ta.append("குருவின் பார்வை பாதுகாப்பையும் ஞானத்தையும் சேர்க்கிறது.")
            notes_ml.append("വ്യാഴത്തിന്റെ ദൃഷ്ടി സംരക്ഷണവും ജ്ഞാനവും നൽകുന്നു.")

        role, owned = _functional_role(p_name, asc_sign)
        if owned:
            owned_themes_en = '; '.join(HOUSE_THEMES[o][0] for o in owned)
            owned_themes_ta = '; '.join(HOUSE_THEMES[o][1] for o in owned)
            rp_en, rp_ta, rp_ml = role_phrases[role]
            owned_themes_ml = '; '.join(HOUSE_THEMES_ML[o] for o in owned)
            lord_en = (f"As lord of the {_house_list(owned, 'en')} ({owned_themes_en}), it is {rp_en}; "
                       f"it carries those matters into {themes_en}.")
            lord_ta = (f"{_house_list(owned, 'ta')} ({owned_themes_ta}) அதிபதியாக இது {rp_ta}; "
                       f"அவ்விஷயங்களை {themes_ta} ஆகியவற்றுடன் இணைக்கிறது.")
            lord_ml = (f"{_house_list(owned, 'ml')} ({owned_themes_ml}) എന്നിവയുടെ അധിപനായ ഇത് {rp_ml}; "
                       f"ആ കാര്യങ്ങളെ {themes_ml} എന്നിവയുമായി ബന്ധിപ്പിക്കുന്നു.")
            score += {'yogakaraka': 1, 'benefic': 1, 'malefic': 0, 'neutral': 0}[role]
        else:
            dispositor = SIGN_LORDS[p_data['sign_index']]
            lord_en = f"As a shadow planet it acts through its sign lord {dispositor}, amplifying {themes_en}."
            lord_ta = f"சாயா கிரகமான இது தன் ராசி அதிபதி {PLANET_TAMIL[dispositor]} மூலம் செயல்பட்டு {themes_ta} ஆகியவற்றைத் தீவிரப்படுத்தும்."
            lord_ml = f"ഛായാഗ്രഹമായ ഇത് രാശ്യധിപനായ {PLANET_ML[dispositor]} വഴി പ്രവർത്തിച്ച് {themes_ml} എന്നിവയെ തീവ്രമാക്കും."

        verdict = _verdict(score)
        if verdict == 'strong':
            close_en = "Expect its significations to deliver well, especially during its dasa and bhukti."
            close_ta = "இதன் காரகத்துவங்கள் சிறப்பாகப் பலன் தரும்; குறிப்பாக இதன் தசை, புக்தி காலங்களில்."
            close_ml = "ഇതിന്റെ കാരകത്വങ്ങൾ നല്ല ഫലം നൽകും; പ്രത്യേകിച്ച് ഇതിന്റെ ദശയിലും അപഹാരത്തിലും."
        elif verdict == 'weak':
            close_en = "Its results come through effort; its dasa or bhukti calls for patience and its remedies."
            close_ta = "இதன் பலன்கள் முயற்சியால் கிடைக்கும்; இதன் தசை அல்லது புக்தியில் பொறுமையும் பரிகாரமும் தேவை."
            close_ml = "ഇതിന്റെ ഫലങ്ങൾ പ്രയത്നത്താൽ ലഭിക്കും; ഇതിന്റെ ദശയിലോ അപഹാരത്തിലോ ക്ഷമയും പരിഹാരവും വേണം."
        else:
            close_en = "Its results are mixed and grow steadily with conscious effort."
            close_ta = "இதன் பலன்கள் கலவையானவை; முயற்சியுடன் படிப்படியாக வளரும்."
            close_ml = "ഇതിന്റെ ഫലങ്ങൾ സമ്മിശ്രമാണ്; ബോധപൂർവ്വമായ പ്രയത്നത്തോടെ ക്രമേണ വളരും."

        pred_en = (
            f"{p_name}, significator of {role_en.lower()}, occupies the {_ordinal(h)} house of {themes_en} in {sign}, in {dig_en}. "
            f"{lord_en} {' '.join(notes_en)} {close_en}"
        ).replace('  ', ' ')
        pred_ta = (
            f"{role_ta} ஆகியவற்றின் காரகனான {name_ta}, {themes_ta} ஆகியவற்றைக் குறிக்கும் {h}-ம் பாவத்தில் {tamil_sign} ராசியில் {dig_ta} அமர்ந்துள்ளார். "
            f"{lord_ta} {' '.join(notes_ta)} {close_ta}"
        ).replace('  ', ' ')
        pred_ml = (
            f"{P_ROLES_ML[p_name]} എന്നിവയുടെ കാരകനായ {name_ml}, {themes_ml} എന്നിവ സൂചിപ്പിക്കുന്ന {h}-ാം ഭാവത്തിൽ "
            f"{MALAYALAM_SIGNS[p_data['sign_index']]} രാശിയിൽ {dig_ml} നിൽക്കുന്നു. {lord_ml} {' '.join(notes_ml)} {close_ml}"
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
            'strength_ml': VERDICT_ML[verdict],
            'score': score,
            'prediction_en': pred_en,
            'prediction_ta': pred_ta,
            'prediction_ml': pred_ml
        })

    return planet_insights

# 5. Dasa-Bhukti Comprehensive Forecast
MAHA_GENERAL_ML = {
    "Sun": "സൂര്യ മഹാദശ (6 വർഷം): സർക്കാർ അംഗീകാരം, നേതൃപദവി, അച്ഛന്റെ പിന്തുണ, ആത്മബലം എന്നിവ ഉയരും. അഹംഭാവം ഒഴിവാക്കുന്നത് നല്ലത്.",
    "Moon": "ചന്ദ്ര മഹാദശ (10 വർഷം): മനസ്സമാധാനം, ജനപ്രീതി, മാതൃസ്നേഹം, വ്യാപാരലാഭം, ദൂരയാത്രകൾ എന്നിവ നന്നായി ലഭിക്കും.",
    "Mars": "ചൊവ്വ മഹാദശ (7 വർഷം): ഭൂമി, വീട് വാങ്ങാനുള്ള യോഗം, പുതിയ സംരംഭങ്ങളിൽ വിജയം, ധൈര്യം എന്നിവ ഉയരും.",
    "Rahu": "രാഹു മഹാദശ (18 വർഷം): വിദേശയോഗം, പെട്ടെന്നുള്ള ധനലാഭം, പുതിയ തൊഴിൽ സംരംഭങ്ങൾ, ആധുനിക മേഖലകളിൽ വൻ വളർച്ച.",
    "Jupiter": "വ്യാഴ മഹാദശ (16 വർഷം): സുവർണ്ണകാലം. സന്താനഭാഗ്യം, ധർമ്മചിന്ത, വിദ്യ, ധനം, സമൂഹത്തിൽ ഉയർന്ന ആദരവ്.",
    "Saturn": "ശനി മഹാദശ (19 വർഷം): കഠിനാധ്വാനത്തിനൊത്ത സ്ഥിരമായ സമ്പത്ത്, പക്വമായ ചിന്ത, ദീർഘായുസ്സ് എന്നീ നല്ല ഫലങ്ങൾ.",
    "Mercury": "ബുധ മഹാദശ (17 വർഷം): വിദ്യാഭ്യാസ ഉന്നതി, വ്യാപാര വളർച്ച, മികച്ച സംസാരശേഷി, കണക്ക്, ആശയവിനിമയ മേഖലകളിൽ ഉന്നതി.",
    "Ketu": "കേതു മഹാദശ (7 വർഷം): ജ്ഞാനം, ആത്മീയതാൽപ്പര്യം, ധ്യാനം, മനസ്സമാധാനം, അപ്രതീക്ഷിത നേട്ടങ്ങൾ.",
    "Venus": "ശുക്ര മഹാദശ (20 വർഷം): സർവ്വ സൗഭാഗ്യങ്ങൾ, വസ്ത്രാഭരണ ശേഖരം, വാഹനസൗകര്യം, കുടുംബത്തിൽ ശുഭകാര്യങ്ങൾ.",
}

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

    for lord, text in MAHA_GENERAL_ML.items():
        maha_general[lord]['ml'] = text

    active_reading_en = "Active Dasa calculation in progress."
    active_reading_ml = 'ദശാ കണക്കുകൂട്ടൽ നടക്കുന്നു.'
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
            dig_ml = DIGNITY_PHRASE_ML.get(data.get('dignity', 'Neutral'), DIGNITY_PHRASE_ML['Neutral'])
            ml = (f"{PLANET_ML[name]} {_house_list(owned, 'ml')} എന്നിവയുടെ അധിപനായി {data['house']}-ാം ഭാവത്തിൽ {dig_ml} നിൽക്കുന്നു"
                  if owned else f"{PLANET_ML[name]} {data['house']}-ാം ഭാവത്തിൽ {dig_ml} നിൽക്കുന്നു")
            return (en, ta, '; '.join(HOUSE_THEMES[h][0] for h in themes), '; '.join(HOUSE_THEMES[h][1] for h in themes),
                    DIGNITY_SCORE.get(data.get('dignity', 'Neutral'), 0), ml, '; '.join(HOUSE_THEMES_ML[h] for h in themes))

        d_en, d_ta, d_themes_en, d_themes_ta, d_score, d_ml, d_themes_ml = lord_profile(d)
        b_en, b_ta, b_themes_en, b_themes_ta, b_score, b_ml, b_themes_ml = lord_profile(b)
        # Position of the Bhukti lord counted from the Dasa lord
        rel = (planets[b]['sign_index'] - planets[d]['sign_index']) % 12 + 1
        if rel == 1:
            rel_en, rel_ta = 'conjoined in the same sign, blending their results closely', 'ஒரே ராசியில் இணைந்திருப்பதால் இருவரின் பலன்களும் நெருக்கமாகக் கலக்கும்'
            rel_ml = 'ഒരേ രാശിയിൽ യോഗം ചെയ്യുന്നതിനാൽ ഇരുവരുടെയും ഫലങ്ങൾ അടുത്ത് കലരും'
        elif rel in (5, 9):
            rel_en, rel_ta = 'in trine to each other, so the period flows harmoniously', 'ஒருவருக்கொருவர் திரிகோணத்தில் இருப்பதால் இக்காலம் இணக்கமாக நகரும்'
            rel_ml = 'പരസ്പരം ത്രികോണത്തിലായതിനാൽ ഈ കാലം ഇണക്കത്തോടെ നീങ്ങും'
        elif rel in (4, 7, 10):
            rel_en, rel_ta = 'in kendra to each other, bringing activity and visible change', 'ஒருவருக்கொருவர் கேந்திரத்தில் இருப்பதால் செயல்பாடும் வெளிப்படையான மாற்றங்களும் வரும்'
            rel_ml = 'പരസ്പരം കേന്ദ്രത്തിലായതിനാൽ പ്രവർത്തനവും പ്രകടമായ മാറ്റങ്ങളും വരും'
        elif rel in (3, 11):
            rel_en, rel_ta = 'in the 3-11 relationship, which favours effort and gains', '3-11 நிலையில் இருப்பதால் முயற்சிக்கு ஏற்ற லாபம் கிடைக்கும்'
            rel_ml = '3-11 ബന്ധത്തിലായതിനാൽ പ്രയത്നത്തിനൊത്ത ലാഭം ലഭിക്കും'
        else:
            rel_en, rel_ta = ('in the 2-12 or 6-8 relationship, which can bring friction; steady, careful decisions help',
                              '2-12 அல்லது 6-8 நிலையில் இருப்பதால் சில உரசல்கள் வரலாம்; நிதானமான முடிவுகள் நலம் தரும்')
            rel_ml = '2-12 അല്ലെങ്കിൽ 6-8 ബന്ധത്തിലായതിനാൽ ചില ഉരസലുകൾ വരാം; സമചിത്തതയുള്ള തീരുമാനങ്ങൾ ഗുണം ചെയ്യും'
        tone = d_score + b_score
        if tone >= 2:
            tone_en, tone_ta = 'Both lords are well placed, so this is a productive period.', 'இரு அதிபதிகளும் நல்ல நிலையில் உள்ளதால் இது பலன் தரும் காலம்.'
            tone_ml = 'രണ്ട് നാഥന്മാരും നല്ല നിലയിലായതിനാൽ ഇത് ഫലപ്രദമായ കാലമാണ്.'
        elif tone <= -2:
            tone_en, tone_ta = 'The lords are under strain, so progress needs patience and remedies.', 'அதிபதிகள் பலவீனமாக உள்ளதால் முன்னேற்றத்திற்குப் பொறுமையும் பரிகாரமும் தேவை.'
            tone_ml = 'നാഥന്മാർ ദുർബലരായതിനാൽ പുരോഗതിക്ക് ക്ഷമയും പരിഹാരവും വേണം.'
        else:
            tone_en, tone_ta = 'The period gives mixed results that respond well to effort.', 'இக்காலம் கலவையான பலன்களைத் தரும்; முயற்சிக்கு நல்ல பலன் உண்டு.'
            tone_ml = 'ഈ കാലം സമ്മിശ്ര ഫലങ്ങൾ നൽകും; പ്രയത്നത്തിന് നല്ല ഫലമുണ്ട്.'
        until = datetime.fromisoformat(active_dasa['bhukti_end']).astimezone(ZoneInfo(tz_name)).date().isoformat()

        if d == b:  # the Maha Dasa's own bhukti
            bhukti_en = f"In its own bhukti {d} gives these results in their purest form."
            bhukti_ta = f"சுய புக்தியில் {PLANET_TAMIL[d]} இப்பலன்களை முழுமையாக வழங்குவார்."
            bhukti_ml = f"സ്വന്തം അപഹാരത്തിൽ {PLANET_ML[d]} ഈ ഫലങ്ങൾ പൂർണ്ണമായി നൽകും."
        else:
            bhukti_en = f"{b_en}, bringing {b_themes_en} to the foreground now. The two lords are {rel_en}."
            bhukti_ta = f"{b_ta}; இப்போது {b_themes_ta} முன்னிலை பெறும். இரு அதிபதிகளும் {rel_ta}."
            bhukti_ml = f"{b_ml}; ഇപ്പോൾ {b_themes_ml} മുന്നിലെത്തും. രണ്ട് നാഥന്മാരും {rel_ml}."

        active_reading_en = (
            f"You are running {d} Maha Dasa, {b} Bhukti and {p} Pratyantardasa; this bhukti lasts until {until}. "
            f"{d_en}, so the Maha Dasa centres on {d_themes_en}. {bhukti_en} {tone_en} {maha_general.get(d, {}).get('en', '')}"
        )
        active_reading_ta = (
            f"தற்போது {PLANET_TAMIL[d]} மகா தசையில் {PLANET_TAMIL[b]} புக்தி, {PLANET_TAMIL[p]} அந்தரம் நடைபெறுகிறது; இப்புக்தி {until} வரை நீடிக்கும். "
            f"{d_ta}; எனவே இந்த மகா தசை {d_themes_ta} ஆகியவற்றை மையமாகக் கொண்டது. {bhukti_ta} {tone_ta} {maha_general.get(d, {}).get('ta', '')}"
        )
        active_reading_ml = (
            f"ഇപ്പോൾ {PLANET_ML[d]} മഹാദശയിൽ {PLANET_ML[b]} അപഹാരവും {PLANET_ML[p]} ഛിദ്രവും നടക്കുന്നു; ഈ അപഹാരം {until} വരെ. "
            f"{d_ml}; അതിനാൽ ഈ മഹാദശ {d_themes_ml} എന്നിവയെ കേന്ദ്രീകരിക്കുന്നു. {bhukti_ml} {tone_ml} {maha_general.get(d, {}).get('ml', '')}"
        )

    return {
        'active_period': active_dasa,
        'active_forecast_en': active_reading_en,
        'active_forecast_ta': active_reading_ta,
        'active_forecast_ml': active_reading_ml,
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
    saturn_title_ml = "അനുകൂലമായ ശനി ഗോചാരം"
    phase = 1 if saturn_diff == 12 else (2 if saturn_diff == 1 else 3)
    if is_sade_sati:
        saturn_title_en = f"Sade Sati (Ezharai Sani, phase {phase})"
        saturn_title_ta = f"ஏழரை நாட்டுச் சனி (கட்டம் {phase})"
        saturn_title_ml = f"ഏഴരശ്ശനി (ഘട്ടം {phase})"
    elif is_ashtama:
        saturn_title_en = "Ashtama Sani (8th House Saturn Transit)"
        saturn_title_ta = "அஷ்டமத்துச் சனி (8-ஆம் இடத்துச் சனி)"
        saturn_title_ml = "അഷ്ടമശ്ശനി (എട്ടിലെ ശനി)"
    elif is_ardhashtama:
        saturn_title_en = "Ardhashtama Sani (4th House Saturn Transit)"
        saturn_title_ta = "அர்த்தாஷ்டமச் சனி (4-ஆம் இடத்துச் சனி)"
        saturn_title_ml = "കണ്ടകശ്ശനി (നാലിലെ ശനി)"

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

    saturn_pred_ml = (
        f"ശനി നിങ്ങളുടെ കൂറിൽ നിന്ന് {saturn_diff}-ാം ഭാവത്തിൽ സഞ്ചരിക്കുന്നു. "
        + ('ഇത് ഏഴരശ്ശനിയുടെ കാലമാണ്; വിവേകവും ക്ഷമയും കഠിനാധ്വാനവും നിങ്ങളെ ഉയർത്തും.' if is_sade_sati else '')
        + ('ഇത് അഷ്ടമശ്ശനിയാണ്; യാത്രകളിൽ ശ്രദ്ധയും ആരോഗ്യ പരിപാലനവും ധർമ്മചിന്തയും ഗുണം ചെയ്യും.' if is_ashtama else '')
        + ('ഇത് കണ്ടകശ്ശനിയാണ്; വീട്, സ്വത്ത്, അമ്മയുടെ ആരോഗ്യം എന്നിവയിൽ ക്ഷമയോടെ ശ്രദ്ധ വേണം.' if is_ardhashtama else '')
        + ('ശനി അനുകൂല ഭാവത്തിൽ സഞ്ചരിക്കുന്നതിനാൽ തൊഴിൽ വളർച്ച, ധനാഗമം, സ്ഥിരമായ പുരോഗതി എന്നിവ ലഭിക്കും.'
           if not (is_sade_sati or is_ashtama or is_ardhashtama) else '')
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

    jupiter_pred_ml = (
        f"വ്യാഴം നിങ്ങളുടെ കൂറിൽ നിന്ന് {jupiter_diff}-ാം ഭാവത്തിൽ സഞ്ചരിക്കുന്നു. "
        + ('ഗുരുബലം നല്ലതാണ്; ധനലാഭം, ശുഭകാര്യങ്ങൾ, മംഗളസംഭവങ്ങൾ, ദൈവാനുഗ്രഹം എന്നിവ ലഭിക്കും.' if is_guru_favorable
           else 'വ്യാഴത്തിന്റെ ഈ സഞ്ചാരം പുതിയ പദ്ധതികൾക്ക് അടിത്തറയിടുന്ന കാലമാണ്.')
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

    rahu_ketu_pred_ml = (
        f"രാഹു നിങ്ങളുടെ കൂറിൽ നിന്ന് {rahu_diff}-ാം ഭാവത്തിലും കേതു {ketu_diff}-ാം ഭാവത്തിലും സഞ്ചരിക്കുന്നു. "
        + ('ധൈര്യം, ശത്രുജയം, അപ്രതീക്ഷിത ലാഭം എന്നിവ ലഭിക്കും.' if rk_favorable
           else 'പുതിയ സംരംഭങ്ങൾ, ആരോഗ്യം, തിടുക്കത്തിലുള്ള തീരുമാനങ്ങൾ എന്നിവയിൽ ശ്രദ്ധ വേണം.')
    )

    return {
        'saturn': {
            'house_from_moon': saturn_diff,
            'sign': transit['Saturn']['sign'],
            'tamil_sign': transit['Saturn']['tamil'],
            'title_en': saturn_title_en,
            'title_ta': saturn_title_ta,
            'title_ml': saturn_title_ml,
            'prediction_en': saturn_pred_en,
            'prediction_ta': saturn_pred_ta,
            'prediction_ml': saturn_pred_ml
        },
        'jupiter': {
            'house_from_moon': jupiter_diff,
            'sign': transit['Jupiter']['sign'],
            'tamil_sign': transit['Jupiter']['tamil'],
            'favorable': is_guru_favorable,
            'prediction_en': jupiter_pred_en,
            'prediction_ta': jupiter_pred_ta,
            'prediction_ml': jupiter_pred_ml
        },
        'rahu_ketu': {
            'rahu_house_from_moon': rahu_diff,
            'ketu_house_from_moon': ketu_diff,
            'favorable': rk_favorable,
            'prediction_en': rahu_ketu_pred_en,
            'prediction_ta': rahu_ketu_pred_ta,
            'prediction_ml': rahu_ketu_pred_ml
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
        'gem_basis_ml': (f"ജീവരത്നം: ലഗ്നാധിപൻ {PLANET_ML[SIGN_LORDS[asc_sign_idx]]}; ഭാഗ്യരത്നം: ഒൻപതാം ഭാവാധിപൻ "
                         f"{PLANET_ML[SIGN_LORDS[(asc_sign_idx + 8) % 12]]}. ജാതകത്തിൽ ഈ നാഥന്മാരുടെ ബലം പരിശോധിച്ച ശേഷം മാത്രം "
                         f"ധരിക്കുക; 6, 8, 12 ഭാവാധിപന്മാരുടെ രത്നങ്ങൾ ഒഴിവാക്കുന്നതാണ് നല്ലത്."),
        'deity_worship_en': 'Lord Ganesha, Lord Shiva, and Goddess Mahalakshmi',
        'deity_worship_ta': 'விநாயகர், சிவபெருமான் மற்றும் மஹாலக்ஷ்மி தாயார்',
        'deity_worship_ml': 'ഗണപതി, പരമശിവൻ, മഹാലക്ഷ്മി'
    }
