"""JoRoScope Timeline-Based Prediction Engine
Chronological Dasa-Bhukti Life Forecasting & Annual Projections
Calculates 81 Dasa-Bhukti periods across a 120-year cycle with mutual planetary
aspects, dignities, house rulerships, ratings, and bilingual predictions (English & தமிழ்).
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List

PLANET_TAMIL = {
    'Sun': 'சூரியன்', 'Moon': 'சந்திரன்', 'Mars': 'செவ்வாய்', 'Mercury': 'புதன்',
    'Jupiter': 'குரு', 'Venus': 'சுக்கிரன்', 'Saturn': 'சனி', 'Rahu': 'ராகு', 'Ketu': 'கேது',
    'Ascendant': 'லக்னம்'
}

# 81 Dasa-Bhukti Core Astrological Archetypes
DASA_BHUKTI_ARCHETYPES = {
    # 1. KETU MAHA DASA (7 Years)
    ('Ketu', 'Ketu'): {
        'title_en': 'Ketu-Ketu Swabhukti: Karmic Awakening & Spiritual Inwardness',
        'title_ta': 'கேது தசை — கேது புக்தி: ஞானோதயம் & ஆன்மீக மறுமலர்ச்சி',
        'theme_en': 'Spiritual reorientation, shedding unnecessary material illusions, deep intuition.',
        'theme_ta': 'ஆன்மீக சிந்தனை மேலோங்கும் காலம், தேவையற்ற பற்றுகள் அகலுதல், உள்ளுணர்வு பிரகாசித்தல்.',
        'career_en': 'Re-evaluating professional direction; preference for meaningful or independent work over routine.',
        'career_ta': 'தொழிலில் மாற்றங்கள் அல்லது சுயேச்சை சிந்தனை; புதிய பாதையை அமைக்கும் காலம்.',
        'wealth_en': 'Modest financial focus; money spent on religious ceremonies, health, and family welfare.',
        'wealth_ta': 'பணம் சுப காரியங்கள், மருத்துவச் செலவுகள் மற்றும் ஆன்மீகத்திற்கு செலவாகும்.',
        'health_en': 'Digestive sensitivity and fatigue; practice meditation, clean diet, and regular sleep.',
        'health_ta': 'செரிமானக் கோளாறு, உஷ்ண உபாதைகள் வரலாம்; எளிய உணவு மற்றும் தியானம் அவசியம்.',
        'family_en': 'Occasional feeling of emotional detachment; cultivate quiet understanding with loved ones.',
        'family_ta': 'குடும்பத்தில் பற்று குறைவது போல் தோன்றும்; அமைதியான அணுகுமுறை நலம் தரும்.',
        'milestones_en': 'Spiritual initiation, pilgrimage, learning astrology or philosophy, changing career course.',
        'milestones_ta': 'ஆன்மீக தீட்சை, ஆலய தரிசனம், தத்துவ ஞானம், புதிய வாழ்க்கை திருப்பம்.',
        'remedy_en': 'Worship Lord Ganesha with Durva grass; recite Ketu Kavacham on Tuesdays/Saturdays.',
        'remedy_ta': 'விநாயகர் வழிபாடு மற்றும் சங்கடஹர சதுர்த்தி விரதம் அளப்பரிய நன்மைகளைத் தரும்.',
        'base_potency': 3
    },
    ('Ketu', 'Venus'): {
        'title_en': 'Ketu-Venus: Material Relief & Harmonious Grace',
        'title_ta': 'கேது தசை — சுக்கிர புக்தி: சுப காரிய அனுகூலம் & சௌபாக்கியம்',
        'theme_en': 'Sudden pleasant associations, artistic interest, domestic relief after spiritual trials.',
        'theme_ta': 'குடும்பத்தில் சுப காரியங்கள், கலை ஈடுபாடு, பொருளாதார ரீதியான திடீர் அனுகூலம்.',
        'career_en': 'Smooth business progress; partnerships bring unexpected rewards; creative breakthroughs.',
        'career_ta': 'தொழிலில் சீரான வளர்ச்சி; கூட்டாளிகளால் லாபம்; ஆடை, அழகு சார்ந்த துறைகளில் மேன்மை.',
        'wealth_en': 'Inflow of luxury goods, jewel purchases, improvement in vehicles and home comforts.',
        'wealth_ta': 'ஆடை ஆபரண சேர்க்கை, வாகன வசதி பெருகுதல், பணப் புழக்கம் அதிகரித்தல்.',
        'health_en': 'General improvement in vitality; guard against urinary or sugar imbalances.',
        'health_ta': 'ஆரோக்கியம் சீராகும்; நீர் சம்பந்தமான மற்றும் சர்க்கரை உபாதைகளில் கவனம் தேவை.',
        'family_en': 'Joyful domestic environment; celebration of weddings, romantic renewal, family bliss.',
        'family_ta': 'திருமண சுப காரியங்கள் கைகூடுதல், இல்லறத்தில் மகிழ்ச்சி, புதிய உறவுகள் மலர்தல்.',
        'milestones_en': 'Marriage or engagement, purchasing vehicles, foreign travel for leisure, domestic harmony.',
        'milestones_ta': 'திருமணம் கைகூடுதல், புது வாகனம் வாங்குதல், இன்ப சுற்றுலா, இல்லற அமைதி.',
        'remedy_en': 'Worship Goddess Mahalakshmi on Fridays; offer white fragrant flowers and light ghee lamp.',
        'remedy_ta': 'வெள்ளிக்கிழமைகளில் மகாலட்சுமிக்கு நெய் தீபமிட்டு துளசி அர்ச்சனை செய்வது சுபம்.',
        'base_potency': 4
    },
    ('Ketu', 'Sun'): {
        'title_en': 'Ketu-Sun: Authority Tests & Inner Illumination',
        'title_ta': 'கேது தசை — சூரிய புக்தி: அரசு வழி கவனம் & ஆன்ம பலம்',
        'theme_en': 'Confronting authoritative figures, lessons in humility, awakening soul purpose.',
        'theme_ta': 'அதிகாரிகளுடன் நிதானம் தேவை, ஆன்ம பலம் சோதிக்கப்படும் காலம், நேர்மைக்கு வெற்றி.',
        'career_en': 'Navigating organizational politics; maintain strict documentation and integrity.',
        'career_ta': 'அரசு மற்றும் உயர் அதிகாரிகளிடம் எச்சரிக்கையாக இருக்கவும்; பணியில் நேர்மை முக்கியம்.',
        'wealth_en': 'Expenditure on taxes, government obligations, or fatherly needs; avoid risky speculation.',
        'wealth_ta': 'அரசு வழியில் அபராதம் அல்லது செலவுகள் வரலாம்; ஊக வணிகத்தில் முதலீடு தவிர்க்கவும்.',
        'health_en': 'Eye strain, migraine, cardiac awareness; practice Surya Namaskar at sunrise.',
        'health_ta': 'கண் உபாதை, தலைவலி, உஷ்ண கோளாறுகள் வரலாம்; சூரிய நமஸ்காரம் நலம் தரும்.',
        'family_en': 'Father or paternal elders require attention; maintain respectful dialogue at home.',
        'family_ta': 'தந்தையின் உடல்நிலையில் கவனம் தேவை; குடும்பத்தில் வீண் விவாதங்களை தவிர்க்கவும்.',
        'milestones_en': 'Overcoming official scrutiny, leadership tests, fatherly responsibilities, spiritual wisdom.',
        'milestones_ta': 'அரசு தேர்வு அல்லது வழக்குகளில் நிதானம், தந்தையார் ஆசி பெறுதல், ஆன்ம விழிப்புணர்வு.',
        'remedy_en': 'Recite Aditya Hridaya Stotram on Sundays; offer water to Surya at sunrise.',
        'remedy_ta': 'ஞாயிற்றுக்கிழமைகளில் ஆதித்ய ஹிருதய ஸ்தோத்திரம் வாசித்து சூரியனுக்கு தீபமேற்றவும்.',
        'base_potency': 2
    },
    ('Ketu', 'Moon'): {
        'title_en': 'Ketu-Moon: Emotional Metamorphosis & Intuitive Depth',
        'title_ta': 'கேது தசை — சந்திர புக்தி: மன அமைதித் தேடல் & உள்ளுணர்வு',
        'theme_en': 'Heightened sensitivity, psychic dreams, journey across waters, search for emotional sanctuary.',
        'theme_ta': 'மனதில் அமைதியின்மை வரலாம், தூர தேசப் பயணம், தாயின் ஆரோக்கியத்தில் கவனம் தேவை.',
        'career_en': 'Fickleness in motivation; steady routine brings victory; artistic or counseling talent shines.',
        'career_ta': 'பணியில் திடீர் சலிப்பு வரலாம்; விடாமுயற்சி வெற்றி தரும்; கலை, மருத்துவ துறையில் நலம்.',
        'wealth_en': 'Fluctuating liquidity; unexpected family expenses; avoid impulsive loans.',
        'wealth_ta': 'பண வரவு ஏறி இறங்கும்; எதிர்பாராத குடும்பச் செலவுகள் வரலாம்; கடன் கொடுப்பதைத் தவிர்க்கவும்.',
        'health_en': 'Sleep cycles, respiratory allergies, cold/phlegm; stay near peaceful water environments.',
        'health_ta': 'தூக்கமின்மை, சளி, சுவாச உபாதைகள் வரலாம்; நீர் நிலைகளில் எச்சரிக்கை தேவை.',
        'family_en': 'Care for mother\'s health; emotional reassurance needed for maternal relations.',
        'family_ta': 'தாயாரின் உடல் நலனில் தனிக் கவனம் செலுத்தவும்; மன வருத்தங்களை பெரிதாக்க வேண்டாம்.',
        'milestones_en': 'Spiritual pilgrimages to coastal/river shrines, relocation, profound meditation insights.',
        'milestones_ta': 'புண்ணிய நதி தீர்த்த யாத்திரை, தியானத்தில் முதிர்ச்சி, இருப்பிட மாற்றம்.',
        'remedy_en': 'Worship Lord Shiva (Chandra Mouleshwara); offer milk abhishekham on Mondays.',
        'remedy_ta': 'திங்கட்கிழமைகளில் சிவபெருமானுக்கு பால் அபிஷேகம் செய்து வழிபடுவது மன அமைதி தரும்.',
        'base_potency': 2
    },
    ('Ketu', 'Mars'): {
        'title_en': 'Ketu-Mars: Dynamic Friction & Breakthrough Courage',
        'title_ta': 'கேது தசை — செவ்வாய் புக்தி: தீரச் செயல் & சவால்களை வெல்லுதல்',
        'theme_en': 'High explosive energy, decisive actions, courage overcoming long-standing hurdles.',
        'theme_ta': 'தைரியம் மற்றும் வேகம் அதிகரிக்கும் காலம்; வீண் கோபத்தைக் கட்டுப்படுத்தினால் மாபெரும் வெற்றி.',
        'career_en': 'Technical triumphs, construction/engineering success, competitive examinations conquered.',
        'career_ta': 'பொறியியல், கட்டிடம், பாதுகாப்பு துறைகளில் வெற்றி; எதிர்ப்புகளை முறியடிக்கும் வேகம்.',
        'wealth_en': 'Property transactions; gains through land, machinery, or metals; avoid rash disputes.',
        'wealth_ta': 'பூமி, மனை வாங்கும் யோகம்; எந்திரங்கள் மூலம் ஆதாயம்; நிலத் தகராறுகளில் நிதானம் தேவை.',
        'health_en': 'Accident prevention, cuts, burns, blood pressure; avoid reckless driving and anger.',
        'health_ta': 'வாகன ஓட்டுதலில் கவனம்; ரத்த அழுத்தம், வெட்டுக்காயங்கள் வரலாம்; நிதானம் அவசியம்.',
        'family_en': 'Strained relations with brothers or peers; calm diplomacy prevents estrangement.',
        'family_ta': 'சகோதரர்களுடன் மனக்கசப்பு வரலாம்; அமைதியான பேச்சால் ஒற்றுமை காக்கப்படும்.',
        'milestones_en': 'Land acquisition, competitive victory, surgical healing, martial achievements.',
        'milestones_ta': 'நிலம் அல்லது வீடு வாங்குதல், போட்டிகளில் வெற்றி, கடின காரியங்கள் நிறைவேறல்.',
        'remedy_en': 'Worship Lord Muruga (Subrahmanya); chant Kandha Sashti Kavasam on Tuesdays.',
        'remedy_ta': 'செவ்வாய்க்கிழமைகளில் முருகப்பெருமானை வணங்கி கந்த சஷ்டி கவசம் பாராயணம் செய்யவும்.',
        'base_potency': 3
    },
    ('Ketu', 'Rahu'): {
        'title_en': 'Ketu-Rahu: Karmic Axis Shift & Reorientation',
        'title_ta': 'கேது தசை — ராகு புக்தி: கர்ம வினை முடிச்சு & வெளிநாட்டு யோகம்',
        'theme_en': 'Karmic axis turnaround; unmasking deceit; sudden foreign opportunities and destiny shifts.',
        'theme_ta': 'வாழ்க்கையில் திடீர் திருப்பங்கள், வெளிநாட்டுத் தொடர்புகள், கர்ம வினைகள் கழியும் காலம்.',
        'career_en': 'Sudden change in work environment; technology, research, and non-traditional sectors thrive.',
        'career_ta': 'பணி மாறுதல் அல்லது வெளிநாட்டு வாய்ப்பு; நவீன தொழில்நுட்ப துறைகளில் எதிர்பாராத வளர்ச்சி.',
        'wealth_en': 'Unconventional income sources, but also sudden expenditures; avoid dubious investments.',
        'wealth_ta': 'திடீர் தன வரவு, அதே சமயம் எதிர்பாராத செலவுகளும் உண்டு; பிறர் பேச்சை நம்பி ஏமாற வேண்டாம்.',
        'health_en': 'Nervous tension, mysterious ailments, phantom fatigue; maintain rigorous grounding.',
        'health_ta': 'நரம்புத் தளர்ச்சி, அனம்னியம், மன பயம் வரலாம்; பிராணாயாமம் மற்றும் தியானம் பாதுகாப்பு தரும்.',
        'family_en': 'Need for clear boundaries; avoid trusting untrustworthy acquaintances.',
        'family_ta': 'உறவுகளிடையே தெளிவு தேவை; குடும்ப ரகசியங்களை பிறரிடம் பகிர்வதை தவிர்க்கவும்.',
        'milestones_en': 'Long-distance overseas move, breaking free from stagnant past, spiritual awakening.',
        'milestones_ta': 'தூர தேசப் பயணம், பழைய தடைகள் உடைதல், புதிய வாழ்க்கைப் பாதை உருவாதல்.',
        'remedy_en': 'Worship Lord Bhairava or Goddess Durga; recite Durga Chalisa on Fridays.',
        'remedy_ta': 'வெள்ளிக்கிழமைகளில் துர்க்கை அம்மனுக்கு எலுமிச்சம்பழ தீபமிட்டு வழிபட தோஷங்கள் நீங்கும்.',
        'base_potency': 2
    },
    ('Ketu', 'Jupiter'): {
        'title_en': 'Ketu-Jupiter: Gnana Yoga & Divine Mentorship',
        'title_ta': 'கேது தசை — குரு புக்தி: ஞான யோகம் & குருவின் அருள்',
        'theme_en': 'Peak spiritual elevation, birth of righteous children, scholarly triumph, social reverence.',
        'theme_ta': 'மிகவும் அதிர்ஷ்டகரமான காலம்; குருவின் ஆசி, புத்திர பாக்கியம், கல்வி மேன்மை, கௌரவம்.',
        'career_en': 'Promotions into mentorship, advisory, judicial, or educational roles; esteemed reputation.',
        'career_ta': 'பதவி உயர்வு, ஆலோசகர் மற்றும் ஆசிரியர் பணி வாய்ப்புகள்; சமுதாயத்தில் உயர்ந்த மதிப்பு.',
        'wealth_en': 'Expansion of wealth through righteous endeavors; investments yield fruitful returns.',
        'wealth_ta': 'நேர்மையான வழியில் தன சேர்க்கை; சேமிப்பு உயரும்; புனித காரியங்களுக்காக செலவிடுதல்.',
        'health_en': 'Vibrant life energy; guard against liver or cholesterol sluggishness.',
        'health_ta': 'ஆரோக்கியம் சிறப்பாக இருக்கும்; கல்லீரல் மற்றும் கொழுப்பு சத்து உணவுகளில் கவனம் தேவை.',
        'family_en': 'Arrival of children, weddings of siblings, peace and devotional harmony in the household.',
        'family_ta': 'குடும்பத்தில் சுப காரியங்கள், மங்கல ஓசை, குழந்தை பாக்கியம், பெரியோர்களின் ஆசிகள்.',
        'milestones_en': 'Publication of books, pilgrimage to major tirthas, obtaining honors, birth of child.',
        'milestones_ta': 'புனித தல யாத்திரை, குழந்தை பிறப்பு, பட்டம் மற்றும் உயரிய அங்கீகாரம் பெறுதல்.',
        'remedy_en': 'Offer yellow flowers and chickpea sweets to Lord Dakshinamurthy on Thursdays.',
        'remedy_ta': 'வியாழக்கிழமைகளில் தட்சிணாமூர்த்திக்கு கொண்டைக்கடலை மாலை அணிவித்து வழிபடவும்.',
        'base_potency': 5
    },
    ('Ketu', 'Saturn'): {
        'title_en': 'Ketu-Saturn: Endurance, Austerity & Iron Resilience',
        'title_ta': 'கேது தசை — சனி புக்தி: பொறுமை, கடின உழைப்பு & பக்குவம்',
        'theme_en': 'Deep testing of patience, shedding worldly pride, building enduring character and resilience.',
        'theme_ta': 'கடின உழைப்பும் பொறுமையும் தேவைப்படும் காலம்; தாமதங்களுக்குப் பின் நிலையான பலன் கிட்டும்.',
        'career_en': 'Heavy duties with delayed applause; persevere steadily; long-term structures being laid.',
        'career_ta': 'பணியில் கூடுதல் பொறுப்புகள்; உழைப்பிற்கு உடனடி பாராட்டு கிடைக்காவிடினும் பிற்காலத்தில் பலன் உண்டு.',
        'wealth_en': 'Tight cash flows; requires careful budgeting; investments in land or infrastructure.',
        'wealth_ta': 'பணப்புழக்கம் சுருங்கும்; சிக்கனம் தேவை; ஆடம்பரச் செலவுகளை தவிர்ப்பது நல்லது.',
        'health_en': 'Joint stiffness, dental care, bone fatigue, melancholic moods; practice gentle walking.',
        'health_ta': 'மூட்டு வலி, எலும்பு மற்றும் பல் உபாதைகள் வரலாம்; எள் எண்ணெய் தேய்த்துக் குளிப்பது நலம்.',
        'family_en': 'Duties toward elderly dependents; emotional restraint and patient tolerance needed.',
        'family_ta': 'முதியவர்களின் பராமரிப்பு சுமை வரலாம்; குடும்பத்தில் விட்டுக் கொடுத்துப் போவது நன்மை பயக்கும்.',
        'milestones_en': 'Overcoming grueling trials, mastery through discipline, laying unshakeable foundations.',
        'milestones_ta': 'கடுமையான சோதனைகளைக் கடந்து சாதித்தல், ஆன்மீக வைராக்கியம், நிலையான சொத்து.',
        'remedy_en': 'Feed crows and stray dogs on Saturdays; light sesame oil lamp for Lord Shani.',
        'remedy_ta': 'சனிக்கிழமைகளில் சனீஸ்வரருக்கு எள் தீபமிட்டு, ஆதரவற்றோருக்கு உணவு தானம் செய்யவும்.',
        'base_potency': 2
    },
    ('Ketu', 'Mercury'): {
        'title_en': 'Ketu-Mercury: Esoteric Intelligence & Commercial Navigation',
        'title_ta': 'கேது தசை — புதன் புக்தி: விவேகம், அறிவுத்திறன் & வியாபார வளர்ச்சி',
        'theme_en': 'Sharp analytical intellect, interest in esoteric coding, astrology, commerce, and writing.',
        'theme_ta': 'நுண்ணறிவு பிரகாசிக்கும்; புதிய வித்தைகளைக் கற்றல்; வியாபாரத்தில் புதிய திட்டங்கள் வெற்றி.',
        'career_en': 'Clever problem solving in business, accounting, software, publishing, or counseling.',
        'career_ta': 'கணக்கு, கணிப்பொறி, தகவல் தொடர்பு, தரகு தொழில்களில் சிறந்த லாபம்; பேச்சாற்றல் வெற்றி தரும்.',
        'wealth_en': 'Steady mercantile earnings; profits through documents and analytical trade; watch fine print.',
        'wealth_ta': 'வணிக வரவு உண்டு; ஒப்பந்தப் பத்திரங்களை நன்கு படித்து கையொப்பமிடவும்.',
        'health_en': 'Nervous sensitivity, skin rashes, communication fatigue; spend time in green gardens.',
        'health_ta': 'தோல் உபாதைகள், நரம்பு சோர்வு வரலாம்; அமைதியான சூழல் மற்றும் இயற்கையோடு இணைதல் நலம்.',
        'family_en': 'Intellectual discussions at home; support from maternal uncles and close friends.',
        'family_ta': 'தாய்மாமன் வழி ஆதரவு; குடும்பத்தில் சுவாரசியமான கலந்துரையாடல்கள்; நண்பர்கள் உதவி.',
        'milestones_en': 'Mastery of specialized knowledge, passing analytical exams, commercial launch.',
        'milestones_ta': 'உயர்கல்வி தேர்வில் வெற்றி, நூல் வெளியீடு, புதிய தொழில் ஒப்பந்தம் செய்தல்.',
        'remedy_en': 'Worship Lord Vishnu; chant Vishnu Sahasranama or recite Budha Beej Mantra on Wednesdays.',
        'remedy_ta': 'புதன்கிழமைகளில் மகா விஷ்ணுவிற்கு துளசி மாலை சாற்றி விஷ்ணு சஹஸ்ரநாமம் பாராயணம் செய்யவும்.',
        'base_potency': 4
    },

    # 2. VENUS MAHA DASA (20 Years)
    ('Venus', 'Venus'): {
        'title_en': 'Venus-Venus Swabhukti: Sumptuous Splendor & Marital Felicity',
        'title_ta': 'சுக்கிர தசை — சுக்கிர புக்தி: போக பாக்கியம் & சகல சௌபாக்கியம்',
        'theme_en': 'Arrival of luxury, beauty, artistic pursuits, sensual contentment, and high status.',
        'theme_ta': 'மகிழ்ச்சியான பொற்காலத் தொடக்கம்; புதிய ஆடை, ஆபரணம், சுகபோக வாழ்வு, மன அமைதி.',
        'career_en': 'Recognition in creative, hospitality, fashion, design, finance, and partnership ventures.',
        'career_ta': 'கலை, அழகு, திரைத்துறை, உணவு, நிதி நிறுவனங்களில் பெரும் வெற்றி; உயர் பதவி வாய்ப்பு.',
        'wealth_en': 'Rapid wealth accumulation, purchase of luxury vehicles, jewels, and prime residence.',
        'wealth_ta': 'தன தான்ய விருத்தி; புதிய சொகுசு வாகனம், நகைகள் வாங்குதல்; இல்லத்தில் வசதிகள் பெருகுதல்.',
        'health_en': 'Radiant vitality; guard against indulgent diet and sedentary habits.',
        'health_ta': 'முகம் வசீகரிக்கும், உடல் நலம் சீராகும்; அதிக இனிப்பு மற்றும் கொழுப்பு உணவுகளை குறைக்கவும்.',
        'family_en': 'Weddings, romantic bliss, birth of radiant daughters, harmonious domestic atmosphere.',
        'family_ta': 'திருமண யோகம், தம்பதியரிடையே அன்யோன்யம், பெண் குழந்தை பாக்கியம், சுப நிகழ்ச்சிகள்.',
        'milestones_en': 'Marriage, purchasing dream vehicle, luxury home acquisition, artistic breakthrough.',
        'milestones_ta': 'திருமணம் கைகூடுதல், புதிய மாளிகை / வாகனம் வாங்குதல், கலை உலகில் புகழ் பெறுதல்.',
        'remedy_en': 'Offer white sweets and lotus flowers to Goddess Lakshmi on Fridays.',
        'remedy_ta': 'வெள்ளிக்கிழமைகளில் மகாலட்சுமிக்கு வெண் தாமரை மலர் சாற்றி நெய் பாயசம் நிவேதனம் செய்யவும்.',
        'base_potency': 5
    },
    ('Venus', 'Sun'): {
        'title_en': 'Venus-Sun: Regal Prominence & Diplomatic Triumph',
        'title_ta': 'சுக்கிர தசை — சூரிய புக்தி: அந்தஸ்து உயர்வு & அரசு அனுகூலம்',
        'theme_en': 'Combining charm with executive authority; social elevation; father\'s pride.',
        'theme_ta': 'சமூகத்தில் செல்வாக்கு உயர்தல், அரசு வழி நன்மைகள், தந்தையாரின் ஆதரவு கிட்டும்.',
        'career_en': 'Executive promotions, civil appointments, prestigious corporate visibility.',
        'career_ta': 'உயர் பதவி உயர்வு; அரசு ஒப்பந்தங்கள் கைகூடுதல்; மேலதிகாரிகளின் பாராட்டு பெறுதல்.',
        'wealth_en': 'Government contracts, prestigious rewards; balancing high expenditures with status.',
        'wealth_ta': 'அரசு வழி சன்மானம்; கௌரவச் செலவுகள் அதிகரித்தாலும் வருமானம் ஈடுகட்டும்.',
        'health_en': 'Eye strain, blood pressure, solar heat; keep balanced hydration.',
        'health_ta': 'கண் உஷ்ணம், ரத்த அழுத்தம் வரலாம்; போதிய அளவு தண்ணீர் குடிப்பது அவசியம்.',
        'family_en': 'Spouse\'s career advances; maintain diplomatic humility in marital disagreements.',
        'family_ta': 'வாழ்க்கைத் துணையின் உத்தியோக மேன்மை; குடும்பத்தில் அகந்தை இல்லாமல் இருப்பது நலம்.',
        'milestones_en': 'Government honors, executive directorship, prestigious corporate alliance.',
        'milestones_ta': 'அரசு விருது அல்லது பாராட்டு பெறுதல், நிர்வாகத் தலைமை பதவி அடைதல்.',
        'remedy_en': 'Worship Lord Shiva and Parvati together; offer bilva leaves on Mondays.',
        'remedy_ta': 'திங்கட்கிழமைகளில் சிவ-பார்வதியை ஒன்றாக தரிசித்து வில்வ இலைகளால் அர்ச்சனை செய்யவும்.',
        'base_potency': 4
    },
    ('Venus', 'Moon'): {
        'title_en': 'Venus-Moon: Emotional Fulfillment & Domestic Radiance',
        'title_ta': 'சுக்கிர தசை — சந்திர புக்தி: மன நிம்மதி & லட்சுமி கடாட்சம்',
        'theme_en': 'Supreme popularity, domestic happiness, poetic creativity, travel across waters.',
        'theme_ta': 'மக்கள் செல்வாக்கு, இல்லத்தில் மகிழ்ச்சி, மன நிறைவு, இனிய பயணங்கள்.',
        'career_en': 'Hospitality, culinary arts, trade, fashion, public entertainment industries flourish.',
        'career_ta': 'வியாபாரம், பொது மக்கள் தொடர்பு, ஆடை, உணவுத் தொழில்களில் அபரிமிதமான வளர்ச்சி.',
        'wealth_en': 'Steady flow of wealth; investments in water, agricultural, or hospitality assets.',
        'wealth_ta': 'பணப்புழக்கம் தாராளமாக இருக்கும்; அழகு சாதனங்கள் மற்றும் கலைப் பொருட்கள் வாங்கும் யோகம்.',
        'health_en': 'Peaceful mind, strong immune system; guard against cold and fluid retention.',
        'health_ta': 'மன அமைதியும் புத்துணர்ச்சியும் மேலோங்கும்; குளிர்ச்சியான உணவுகளில் கவனம்.',
        'family_en': 'Blessed domestic peace; love from mother and maternal relatives; birth of lovely child.',
        'family_ta': 'தாயன்பு, இல்லற இன்பம், பெண் குழந்தைகள் வழி மகிழ்ச்சி, சுப காரியங்கள் இனிதே நடக்கும்.',
        'milestones_en': 'Scenic foreign travels, purchasing waterfront property, cultural recognition.',
        'milestones_ta': 'வெளிநாட்டு சுற்றுலா, புதிய மனை வாங்குதல், குடும்பத்தில் மங்கல காரியங்கள்.',
        'remedy_en': 'Offer milk and white flowers to Goddess Lalita Tripurasundari on Full Moon days.',
        'remedy_ta': 'பௌர்ணமி தினங்களில் லலிதா சஹஸ்ரநாமம் பாராயணம் செய்து அம்பாளுக்கு பால் நைவேத்தியம் செய்யவும்.',
        'base_potency': 5
    },
    ('Venus', 'Mars'): {
        'title_en': 'Venus-Mars: Passionate Ambition & Prime Real Estate',
        'title_ta': 'சுக்கிர தசை — செவ்வாய் புக்தி: நில யோகம் & வீரமும் கவர்ச்சியும்',
        'theme_en': 'Dynamic energy combined with charm; real estate acquisitions, vibrant passion.',
        'theme_ta': 'தைரியமும் ஈர்ப்பு சக்தியும் மேலோங்கும்; பூமி யோகம், ரியல் எஸ்டேட் மற்றும் தொழில் வளர்ச்சி.',
        'career_en': 'Architecture, interior design, construction, sports management, and tech engineering surge.',
        'career_ta': 'கட்டிடக்கலை, வடிவமைப்பு, பொறியியல் மற்றும் பாதுகாப்பு துறைகளில் பிரகாசிக்கும் காலம்.',
        'wealth_en': 'Substantial property purchases; high gains through lands, apartments, and metallic trades.',
        'wealth_ta': 'நிலம், அடுக்குமாடி குடியிருப்பு வாங்கும் யோகம்; எந்திரங்கள் மற்றும் உலோக வர்த்தகத்தில் லாபம்.',
        'health_en': 'High stamina; avoid overexertion and spicy/inflammatory foods.',
        'health_ta': 'உடல் வலிமை கூடும்; உஷ்ணம், பித்தம் மற்றும் தசைப் பிடிப்புகளைத் தவிர்க்க நீர் அருந்தவும்.',
        'family_en': 'Intense romantic passion; dynamic partner; avoid impetuous arguments in the bedroom.',
        'family_ta': 'காதல் உறவு மலர்தல்; துணையுடன் உணர்ச்சிபூர்வ பிணைப்பு; வீண் பிடிவாதத்தை தவிர்க்கவும்.',
        'milestones_en': 'Purchasing prime real estate, architectural construction, dynamic business launch.',
        'milestones_ta': 'சொந்த வீடு / பூமி வாங்குதல், புதிய தொழில் தொடங்குதல், சகோதரர் நலம்.',
        'remedy_en': 'Worship Lord Subrahmanya and Goddess Durga; light ghee lamps on Tuesdays and Fridays.',
        'remedy_ta': 'செவ்வாய், வெள்ளிகளில் முருகனுக்கும் துர்க்கைக்கும் நெய் விளக்கேற்றி வழிபட சுபம்.',
        'base_potency': 4
    },
    ('Venus', 'Rahu'): {
        'title_en': 'Venus-Rahu: Glamour, Windfalls & Global Expansion',
        'title_ta': 'சுக்கிர தசை — ராகு புக்தி: பிரம்மாண்ட வளர்ச்சி & திடீர் யோகம்',
        'theme_en': 'Unprecedented social rise, international glamour, sudden windfalls, unconventional lifestyle.',
        'theme_ta': 'அசுர வேக வளர்ச்சி, வெளிநாட்டுப் பயணம், எதிர்பாராத தன லாபம், நவீன துறைகளில் ஆதிக்கம்.',
        'career_en': 'Breakthrough in digital media, cinema, international trade, aviation, or luxury imports.',
        'career_ta': 'டிஜிட்டல் மீடியா, ஏற்றுமதி-இறக்குமதி, தகவல் தொழில்நுட்பத்தில் திடீர் உச்சம்.',
        'wealth_en': 'Extravagant financial gains; sudden windfalls; beware of overspending on vanity.',
        'wealth_ta': 'திடீர் பண வரவு, அதிர்ஷ்ட யோகம்; பகட்டுச் செலவுகளை கட்டுப்படுத்துவது அவசியமாகும்.',
        'health_en': 'Exotic indulgences; watch allergies, reproductive wellness, and chemical sensitivities.',
        'health_ta': 'ஒவ்வாமை, போதை அல்லது தவறான பழக்கவழக்கங்களைத் தவிர்ப்பது உடல் நலத்திற்கு நல்லது.',
        'family_en': 'Inter-cultural alliances, unconventional romance; maintain marital transparency.',
        'family_ta': 'மாறுபட்ட கலாச்சார உறவுகள், எதிர்பாராத திருமண யோகம்; உண்மைத்தன்மை காப்பது நலம்.',
        'milestones_en': 'Long-term international settlement, mass media fame, massive commercial windfall.',
        'milestones_ta': 'வெளிநாட்டில் குடியேறுதல், பெரும் பிரபலம் அடைதல், மிகப்பெரிய பொருளாதார வெற்றி.',
        'remedy_en': 'Worship Goddess Durga with lemon lamps on Friday Rahu Kalam (10:30 AM - 12:00 PM).',
        'remedy_ta': 'வெள்ளிக்கிழமை ராகு காலத்தில் துர்க்கைக்கு எலுமிச்சம்பழ தீபமிட்டு அர்ச்சனை செய்யவும்.',
        'base_potency': 4
    },
    ('Venus', 'Jupiter'): {
        'title_en': 'Venus-Jupiter: Lakshmi-Narayana Yoga & Golden Fortune',
        'title_ta': 'சுக்கிர தசை — குரு புக்தி: லட்சுமி நாராயண யோகம் & பொற்காலம்',
        'theme_en': 'Auspicious conjunction of the two supreme gurus (Bhrigu & Brihaspati); peak prosperity.',
        'theme_ta': 'இரு பெரும் சுப கிரகங்களின் சேர்க்கை; பொற்காலம், பெரும் தன யோகம், ஞானம், புத்திர பாக்கியம்.',
        'career_en': 'Reaching pinnacle of profession; legal, academic, financial, ministerial, and consulting eminence.',
        'career_ta': 'தொழிலில் உச்சத்தைத் தொடுதல்; நீதி, நிதி, கல்வி, ஆலோசனைத் துறைகளில் தலைமைப் பொறுப்பு.',
        'wealth_en': 'Multiplication of capital, ethical investments, generous philanthropy, enduring wealth.',
        'wealth_ta': 'தன தான்ய விருத்தி, வங்கியில் சேமிப்பு பல மடங்கு உயர்தல், தர்ம காரியங்கள் செய்தல்.',
        'health_en': 'Robust constitution and glow; watch weight gain and sugar levels.',
        'health_ta': 'உடல் பொலிவு கூடும்; உடல் எடை அதிகரித்தல் மற்றும் சர்க்கரை உணவுகளில் விழிப்புணர்வு.',
        'family_en': 'Celebrations of weddings, birth of noble children, spiritual harmony, societal honor.',
        'family_ta': 'இல்லத்தில் மங்கல காரியங்கள், சுப திருமணங்கள், சத்புத்திர பாக்கியம், பெரியோர் ஆசி.',
        'milestones_en': 'Marriage, birth of gifted children, acquiring substantial family assets, university honors.',
        'milestones_ta': 'மங்கல திருமணம், புத்திர பாக்கியம், பிரம்மாண்ட சொத்துக்கள் வாங்குதல், உயரிய கௌரவம்.',
        'remedy_en': 'Offer yellow sweets to Brahmins or students; worship Lord Vishnu and Lakshmi jointly.',
        'remedy_ta': 'லட்சுமி நாராயணர் வழிபாடு மற்றும் ஏழை மாணவர்களுக்கு கல்வி உதவி செய்தல் பெரும் புண்ணியம்.',
        'base_potency': 5
    },
    ('Venus', 'Saturn'): {
        'title_en': 'Venus-Saturn: Enduring Empire & Durable Foundations',
        'title_ta': 'சுக்கிர தசை — சனி புக்தி: நிலையான சொத்துக்கள் & உழைப்பின் வெற்றி',
        'theme_en': 'Friendship between luxury and discipline; constructing enduring institutions and solid assets.',
        'theme_ta': 'சுக்கிரன்-சனி நட்பு காலம்; கடின உழைப்பிற்கு நிலையான வெகுமதி, மாளிகை, தொழிற்சாலை யோகம்.',
        'career_en': 'Corporate stability, engineering industries, infrastructure development, high accountability.',
        'career_ta': 'நிறுவனங்களில் நிலையான பொறுப்பு; இரும்பு, நிலக்கரி, ஆட்டோமொபைல், கட்டடத் துறையில் மேன்மை.',
        'wealth_en': 'Steady disciplined wealth creation; purchases of commercial property and long-term equities.',
        'wealth_ta': 'நீண்ட கால முதலீடுகள் மூலம் லாபம்; வணிக வளாகங்கள், தொழிற்சாலை நிலங்கள் வாங்குதல்.',
        'health_en': 'Good physical stamina; attend to joint mobility, teeth, and skin hydration.',
        'health_ta': 'மூட்டு வலி, தோல் வறட்சி தவிர்ப்பதற்கு நல்லெண்ணெய் தேய்த்துக் குளிப்பது நன்மை தரும்.',
        'family_en': 'Dignified household; respect for elders; marriages with mature and responsible partners.',
        'family_ta': 'குடும்பத்தில் முதிர்ந்த அமைதி; வாழ்க்கைத் துணையால் ஆக்கப்பூர்வமான உதவி; பெரியோர் நலம்.',
        'milestones_en': 'Completing major construction, established long-term business, enduring marriage.',
        'milestones_ta': 'பிரமாண்ட கட்டடப் பணி முடித்தல், நிலையான தொழில் சாம்ராஜ்யம் அமைத்தல்.',
        'remedy_en': 'Light sesame oil lamp under Peepal tree on Saturdays; donate black clothes to laborers.',
        'remedy_ta': 'சனிக்கிழமைகளில் அரச மரத்தடி விநாயகருக்கு தீபமிட்டு, எளியோருக்கு வஸ்திர தானம் செய்யவும்.',
        'base_potency': 4
    },
    ('Venus', 'Mercury'): {
        'title_en': 'Venus-Mercury: Saraswati Grace & Commercial Triumph',
        'title_ta': 'சுக்கிர தசை — புதன் புக்தி: சரஸ்வதி யோகம் & வியாபார உச்சம்',
        'theme_en': 'Charming eloquence, literary genius, profitable trade, artistic communication, joyful travels.',
        'theme_ta': 'பேச்சாற்றல், விவேகம், வணிக லாபம், கலை மற்றும் எழுத்துத் துறையில் பெரும் வெற்றி.',
        'career_en': 'Advertising, media, software, brokerage, diplomatic missions, and educational publishing.',
        'career_ta': 'ஊடகம், விளம்பரம், கணக்கு, ஏற்றுமதி-இறக்குமதி, சாப்ட்வேர் துறைகளில் பெரும் பிரபலம்.',
        'wealth_en': 'Rapid turnover of profits; successful contracts, investments in modern technology assets.',
        'wealth_ta': 'வர்த்தகத்தில் தொடர் லாபம்; புதிய ஒப்பந்தங்கள் கையெழுத்தாதல்; நகை, ஆடை சேர்க்கை.',
        'health_en': 'Agile mind and youthful energy; take rest from digital screens to prevent eye fatigue.',
        'health_ta': 'இளமைப் பொலிவு கூடும்; கண் சோர்வு மற்றும் நரம்பு அமைதிக்கு நல்ல உறக்கம் தேவை.',
        'family_en': 'Pleasant family conversations, reunions with cousins and friends, cheerful home atmosphere.',
        'family_ta': 'குடும்பத்தில் கலகலப்பான சூழல்; உறவினர்கள் வருகை; நண்பர்களால் நன்மைகள் பெருகுதல்.',
        'milestones_en': 'Launching commercial enterprise, publishing books/creative works, lucrative contracts.',
        'milestones_ta': 'புதிய வர்த்தக நிறுவனம் தொடங்குதல், படைப்புகள் வெளியிடுதல், பெரிய ஒப்பந்தம் வெல்லுதல்.',
        'remedy_en': 'Offer green grass (Durva) to Lord Ganesha on Wednesdays; recite Saraswati Stotram.',
        'remedy_ta': 'புதன்கிழமைகளில் விநாயகருக்கு அருகம்புல் சாற்றி, சரஸ்வதி தேவியை வழிபட கல்வி வளரும்.',
        'base_potency': 5
    },
    ('Venus', 'Ketu'): {
        'title_en': 'Venus-Ketu: Chidra Dasa & Spiritual Refinement',
        'title_ta': 'சுக்கிர தசை — கேது புக்தி: தசா சந்தி & ஆன்மீக முதிர்ச்சி',
        'theme_en': 'Concluding phase of 20-year Venus era; releasing material vanity; spiritual charity.',
        'theme_ta': '20 ஆண்டு சுக்கிர தசையின் நிறைவு காலம்; பகட்டு குறைந்து ஆன்மீக அமைதி நாடுதல்.',
        'career_en': 'Transition period; wrapping up past ventures; preparing for the upcoming Sun era.',
        'career_ta': 'பணியில் மாற்றங்கள்; பழைய திட்டங்களை முடித்து புதிய அத்தியாயத்திற்குத் தயாராதல்.',
        'wealth_en': 'Spending on charitable trusts, temples, ancestral ceremonies; stable essentials.',
        'wealth_ta': 'தர்ம காரியங்கள், திருப்பணிகள், முன்னோர்கள் வழிபாட்டிற்கு செலவுகள் செய்தல்.',
        'health_en': 'Body detoxification; watch for skin sensitivities and reproductive health.',
        'health_ta': 'உடலில் நச்சுக்கள் நீங்குதல்; இயற்கை உணவு மற்றும் ஆன்மீக நல்வழிகளைப் பின்பற்றவும்.',
        'family_en': 'Resolving long-standing family disputes; letting go of past resentments.',
        'family_ta': 'பழைய குடும்ப மனஸ்தாபங்கள் தீருதல்; பக்குவமான அணுகுமுறையால் குடும்பத்தில் அமைதி.',
        'milestones_en': 'Major pilgrimage, philanthropic endowment, profound spiritual transition.',
        'milestones_ta': 'புண்ணிய தலங்களுக்கு யாத்திரை, தர்ம அறக்கட்டளை அமைத்தல், ஆன்ம சாந்தி.',
        'remedy_en': 'Feed street animals and donate blankets to elderly persons on Tuesdays.',
        'remedy_ta': 'செவ்வாய்க்கிழமைகளில் ஏழை முதியவர்களுக்கு கம்பளி அல்லது ஆடை தானம் செய்வது நலம்.',
        'base_potency': 3
    },

    # 3. SUN MAHA DASA (6 Years)
    ('Sun', 'Sun'): {
        'title_en': 'Sun-Sun Swabhukti: Solar Coronation & Vital Authority',
        'title_ta': 'சூரிய தசை — சூரிய புக்தி: அரசு அனுகூலம் & தலைமைப் பதவி',
        'theme_en': 'Radiant vitality, administrative leadership, father\'s honor, sovereign courage.',
        'theme_ta': 'ஆளுமைத் திறன் உயர்தல், அரசு வழி மேன்மை, தலைமைப் பதவி, தந்தையின் பெருமை.',
        'career_en': 'Promotion into management or public office; recognition by superiors and executives.',
        'career_ta': 'நிர்வாகப் பொறுப்புகள் உயர்தல், அரசாங்க பாராட்டு, அதிகாரிகளுடன் நற்பெயர்.',
        'wealth_en': 'Income through governmental and established institutional channels; stable prestige.',
        'wealth_ta': 'அரசு உத்தியோகம் மற்றும் நிறுவனங்கள் மூலம் சீரான தன வரவு; கௌரவம் கூடும்.',
        'health_en': 'Vigorous energy; monitor heart rate, blood pressure, and sunstroke in hot climates.',
        'health_ta': 'உடலில் உஷ்ணம் கூடும்; கண் மற்றும் ரத்த அழுத்தத்தில் சீரான கவனம் தேவை.',
        'family_en': 'Elevated family reputation; father or eldest son achieves notable success.',
        'family_ta': 'தந்தையாருக்கு பெருமை சேர்க்கும் காலம்; குடும்பத்தின் கௌரவம் சமூகத்தில் உயரும்.',
        'milestones_en': 'Government appointment, corporate executive leadership, public accolade.',
        'milestones_ta': 'அரசுப் பணி கிடைத்தல், நிறுவனத் தலைமைப் பொறுப்பு ஏறுதல், சமூக மரியாதை.',
        'remedy_en': 'Recite Gayatri Mantra 108 times at sunrise; offer water in copper vessel to Surya.',
        'remedy_ta': 'தினமும் அதிகாலையில் செப்புப் பாத்திரத்தில் நீர் வைத்து சூரிய பகவானுக்கு சமர்ப்பிக்கவும்.',
        'base_potency': 4
    },
    ('Sun', 'Moon'): {
        'title_en': 'Sun-Moon: Royal Harmony & Popular Acclaim',
        'title_ta': 'சூரிய தசை — சந்திர புக்தி: மக்கள் செல்வாக்கு & மன தெளிவு',
        'theme_en': 'Harmonious blending of solar willpower and lunar empathy; public approval.',
        'theme_ta': 'ஆளுமையும் கருணையும் இணைந்த காலம்; பொதுமக்களின் ஆதரவு, மனத்தெளிவு, சுபப் பயணம்.',
        'career_en': 'Smooth execution of public projects; support from both superiors and subordinates.',
        'career_ta': 'உயர் அதிகாரிகள் மற்றும் சக ஊழியர்களின் பேராதரவு; மக்கள் தொடர்புப் பணிகளில் வெற்றி.',
        'wealth_en': 'Prosperity through commerce, government tenders, and liquid capital turnover.',
        'wealth_ta': 'வர்த்தகம் மற்றும் அரசு வழியில் தன வரவு; குடும்பத்தில் புதிய பொருட்கள் சேருதல்.',
        'health_en': 'Emotional equilibrium and sound vitality; balanced digestive fire.',
        'health_ta': 'மன நிம்மதி, ஆரோக்கியமான உடல் நிலை; தூக்கமும் உணவும் சீராக அமையும்.',
        'family_en': 'Parental blessings; domestic harmony; joy from children and spouse.',
        'family_ta': 'பெற்றோரின் நல்லாசி; இல்லறத்தில் ஒற்றுமை; குழந்தைகளின் முன்னேற்றம் கண்டு மகிழ்ச்சி.',
        'milestones_en': 'Successful public initiatives, overseas business missions, family celebrations.',
        'milestones_ta': 'முக்கிய அரசுப் பணிகளை முடித்தல், குடும்பத்துடன் புண்ணிய ஸ்தலங்களுக்குப் பயணம்.',
        'remedy_en': 'Worship Lord Shiva and Goddess Parvati together on Mondays.',
        'remedy_ta': 'திங்கட்கிழமைகளில் உமா-மகேஸ்வரரை வில்வத்தால் அர்ச்சித்து வழிபட சுபிட்சம்.',
        'base_potency': 5
    },
    ('Sun', 'Mars'): {
        'title_en': 'Sun-Mars: Supreme Command & Victorious Valor',
        'title_ta': 'சூரிய தசை — செவ்வாய் புக்தி: வீர பராக்கிரமம் & எதிரிகளை வெல்லுதல்',
        'theme_en': 'Blazing martial energy; competitive supremacy; decisive leadership victories.',
        'theme_ta': 'வீரம், வேகம், போட்டித் தேர்வுகளில் வெற்றி, எதிரிகளை முறியடித்து மேலோங்கும் காலம்.',
        'career_en': 'Triumph in military, police, surgical, engineering, or executive administration.',
        'career_ta': 'பாதுகாப்புத் துறை, அறுவை சிகிச்சை, பொறியியல், ரியல் எஸ்டேட் துறைகளில் அபார வெற்றி.',
        'wealth_en': 'Acquisitions of agricultural lands, plots, commercial structures, and machinery.',
        'wealth_ta': 'பூமி, மனை வாங்கும் யோகம்; எந்திரங்கள் மூலம் நல்ல வருமானம்; கடன்கள் அடைபடும்.',
        'health_en': 'High stamina; avoid excessive heat, impulsive driving, and aggressive disputes.',
        'health_ta': 'உடல் வலிமை கூடும்; அதிக கார உணவுகள், கோபம், வாகன வேகத்தை கட்டுப்படுத்தவும்.',
        'family_en': 'Proud family moments; support from brothers; maintain patience in heated debates.',
        'family_ta': 'சகோதரர்களால் அனுகூலம்; குடும்பத்தில் கௌரவம் கூடும்; பிடிவாதத்தை கைவிடுவது நல்லது.',
        'milestones_en': 'Land registry, competitive examination victory, administrative appointment.',
        'milestones_ta': 'சொந்த மனை பத்திரப்பதிவு, வழக்குகளில் வெற்றி, புதிய அதிகாரப் பதவி அடைதல்.',
        'remedy_en': 'Chant Subrahmanya Ashtakam on Tuesdays; offer red oleander flowers to Muruga.',
        'remedy_ta': 'செவ்வாய்க்கிழமைகளில் முருகப் பெருமானுக்கு செவ்வரளி மாலை சாற்றி வழிபடவும்.',
        'base_potency': 4
    },
    ('Sun', 'Rahu'): {
        'title_en': 'Sun-Rahu: Solar Eclipse Threshold & Shrewd Diplomacy',
        'title_ta': 'சூரிய தசை — ராகு புக்தி: கிரகண காலம் & ராஜதந்திரம்',
        'theme_en': 'High-stakes corporate or political maneuvering; overcoming bureaucratic resistance.',
        'theme_ta': 'அரசு மற்றும் தொழில் ரீதியான சவால்கள்; ராஜதந்திர அணுகுமுறையால் வெற்றி கிட்டும்.',
        'career_en': 'Navigating office politics; foreign assignments; protect personal credibility carefully.',
        'career_ta': 'உயர் பதவியில் இருப்பவர்களிடம் எச்சரிக்கை தேவை; வெளிநாட்டுப் பயணங்கள் அனுகூலம் தரும்.',
        'wealth_en': 'Sudden fluctuations; money may be spent on legal compliance; avoid speculation.',
        'wealth_ta': 'பண வரவில் ஏற்ற இறக்கம்; அரசாங்கக் கட்டணங்கள் மற்றும் அபராதங்களைத் தவிர்க்க விழிப்புணர்வு.',
        'health_en': 'Solar vitality dimmed; monitor heart, eyes, and bone marrow vitality.',
        'health_ta': 'கண் பார்வை, எலும்பு பலவீனம், உஷ்ணக் கட்டிகள் வரலாம்; அதிக வெயிலில் அலைவதை தவிர்க்கவும்.',
        'family_en': 'Father\'s health needs careful attention; avoid trusting gossip among relatives.',
        'family_ta': 'தந்தையின் ஆரோக்கியத்தில் தனிக் கவனம் தேவை; உறவினர் விஷயங்களில் நடுநிலை காக்கவும்.',
        'milestones_en': 'Overcoming official opposition, unexpected foreign posting, karmic tests passed.',
        'milestones_ta': 'கடும் போட்டிகளை சாதுரியமாக வெல்லுதல், வெளிநாட்டுப் பணி வாய்ப்பு.',
        'remedy_en': 'Recite Maha Mrityunjaya Mantra daily; donate wheat and copper to needy on Sundays.',
        'remedy_ta': 'தினமும் மகா மிருத்யுஞ்சய மந்திரம் ஜெபித்து, ஏழைகளுக்கு கோதுமை தானம் செய்யவும்.',
        'base_potency': 2
    },
    ('Sun', 'Jupiter'): {
        'title_en': 'Sun-Jupiter: Sovereign Fortune & Virtuous Glory',
        'title_ta': 'சூரிய தசை — குரு புக்தி: ராஜ யோகம் & குருவின் பரிபூரண அருள்',
        'theme_en': 'Spiritual illumination, academic excellence, ministerial counsel, birth of righteous progeny.',
        'theme_ta': 'ராஜ யோக காலம்; குருவின் ஆசியால் அரசு அனுகூலம், புத்திர பாக்கியம், தர்ம சிந்தனை.',
        'career_en': 'Elevation to top executive, advisory, judiciary, or academic dean positions.',
        'career_ta': 'நீதி, கல்வி, நிதி மற்றும் அரசாங்கத் துறைகளில் உயர் பதவி; சமுதாயத்தில் பெரும் புகழ்.',
        'wealth_en': 'Abundant wealth inflow through lawful and noble deeds; auspicious investments.',
        'wealth_ta': 'தன தான்ய லாபம்; புண்ணிய காரியங்களுக்கு செலவிடுதல்; பூர்வீகச் சொத்துக்கள் கைக்கு வருதல்.',
        'health_en': 'Radiant health, high immunity, cheerful optimism; balanced bodily humors.',
        'health_ta': 'ஆரோக்கியம் பிரகாசிக்கும்; உடல் நலம் பூரணமாகத் தேறும்; நேர்மறை எண்ணங்கள் கூடும்.',
        'family_en': 'Arrival of children, weddings of siblings, spiritual pilgrimages with parents.',
        'family_ta': 'குடும்பத்தில் சுப நிகழ்ச்சிகள், குழந்தை பிறப்பு, பெற்றோருக்கு பெருமை, இல்லற மகிழ்ச்சி.',
        'milestones_en': 'State honor, promotion to highest rank, publishing seminal scholarly work.',
        'milestones_ta': 'அரசாங்க விருது, உயரிய பதவி நியமனம், தீர்த்த யாத்திரை செல்லுதல்.',
        'remedy_en': 'Worship Lord Dakshinamurthy on Thursdays; offer yellow garlands and chana dal.',
        'remedy_ta': 'வியாழக்கிழமைகளில் தட்சிணாமூர்த்திக்கு மஞ்சள் வஸ்திரம் சாற்றி நெய் தீபமிட்டு வணங்கவும்.',
        'base_potency': 5
    },
    ('Sun', 'Saturn'): {
        'title_en': 'Sun-Saturn: Karmic Duty, Humility & Strenuous Trial',
        'title_ta': 'சூரிய தசை — சனி புக்தி: பொறுமை சோதிக்கப்படும் காலம் & கர்மா',
        'theme_en': 'Father-son archetypal tension; heavy responsibilities; lessons in discipline and patience.',
        'theme_ta': 'கடின உழைப்பும் பொறுமையும் அவசியம்; அதிகாரிகளுடன் வாக்குவாதங்களை தவிர்க்கவும்.',
        'career_en': 'Demanding supervisors; heavy workloads with slow recognition; build resilience.',
        'career_ta': 'பணியிடத்தில் கூடுதல் பணிச்சுமை; அவசரப்பட்டு வேலையை விடக்கூடாது; பொறுமை காக்க.',
        'wealth_en': 'Tight expenditures; delay in promised receivables; stick to conservative savings.',
        'wealth_ta': 'வரவுக்கேற்ற செலவுகள்; வரவேண்டிய பணத்தில் தாமதம்; யாருக்கும் ஜாமீன் போட வேண்டாம்.',
        'health_en': 'Bone fatigue, lower back strain, eye irritation; practice gentle yoga postures.',
        'health_ta': 'முதுகு வலி, கண் சோர்வு, நரம்பு பலவீனம் வரலாம்; போதுமான ஓய்வு எடுப்பது நலம்.',
        'family_en': 'Differences with father or older family figures; practice silence and respect.',
        'family_ta': 'தந்தையாருடன் கருத்து வேறுபாடுகள் வரலாம்; அமைதியான போக்கால் குடும்ப ஒற்றுமை காக்கப்படும்.',
        'milestones_en': 'Passing major karmic endurance test, establishing disciplined foundation.',
        'milestones_ta': 'கடினமான சோதனைகளைக் கடந்து பக்குவமடைதல், புதிய உறுதியான அடித்தளம்.',
        'remedy_en': 'Recite Shani Gayatri and Surya Ashtakam; feed sesame bread to crows daily.',
        'remedy_ta': 'தினமும் காகத்திற்கு எள் கலந்த சாதம் வைத்து, சனீஸ்வரருக்கு நல்லெண்ணெய் தீபமேற்றவும்.',
        'base_potency': 2
    },
    ('Sun', 'Mercury'): {
        'title_en': 'Sun-Mercury: Budhaditya Wisdom & Diplomatic Grace',
        'title_ta': 'சூரிய தசை — புதன் புக்தி: புதாதித்ய யோகம் & புத்திக் கூர்மை',
        'theme_en': 'Brilliant intellect, diplomatic persuasion, commercial gains, intellectual mastery.',
        'theme_ta': 'புதாதித்ய யோகம் செயல்படும் காலம்; அறிவாற்றல், பேச்சாற்றல், வர்த்தக மேன்மை கிட்டும்.',
        'career_en': 'Success in civil examinations, auditing, law, media, journalism, and government contracts.',
        'career_ta': 'கணக்கு, சட்டம், பத்திரிகை, நிர்வாகம் மற்றும் தகவல் தொடர்பு துறைகளில் பெரும் புகழ்.',
        'wealth_en': 'Steady mercantile revenue; gains through intellectual property and contracts.',
        'wealth_ta': 'வியாபாரத்தில் லாபம்; புதிய முதலீடுகள் நல்ல பலன் தரும்; வரவு செலவு சமநிலையாகும்.',
        'health_en': 'Alert nervous system and mental clarity; keep speech and digestion balanced.',
        'health_ta': 'சுறுசுறுப்பான உடல் நலம்; நரம்பு மண்டலம் பலப்படும்; சரியான நேரத்தில் உணவு உட்கொள்ளவும்.',
        'family_en': 'Lively discussions, support from maternal relatives, joy from younger siblings.',
        'family_ta': 'குடும்பத்தில் சுப காரியப் பேச்சுக்கள்; தாய்மாமன் வழி அனுகூலம்; உறவினர் ஆதரவு.',
        'milestones_en': 'Publishing scholarly papers, clearing prestigious civil exams, launching consultancy.',
        'milestones_ta': 'போட்டித் தேர்வுகளில் தேர்ச்சி, புதிய வணிக ஒப்பந்தம், கௌரவப் பட்டம் பெறுதல்.',
        'remedy_en': 'Worship Lord Maha Vishnu; offer green moong dal and tulsi leaves on Wednesdays.',
        'remedy_ta': 'புதன்கிழமைகளில் விஷ்ணுவுக்கு துளசி அர்ச்சனை செய்து பச்சைப்பயறு தானம் செய்யவும்.',
        'base_potency': 4
    },
    ('Sun', 'Ketu'): {
        'title_en': 'Sun-Ketu: Spiritual Solitude & Ego Detachment',
        'title_ta': 'சூரிய தசை — கேது புக்தி: ஆன்மீக நாட்டம் & பற்றற்ற நிலை',
        'theme_en': 'Detachment from worldly vanity, mystical intuition, pilgrimage, health vigilance.',
        'theme_ta': 'பகட்டு குறையும் காலம்; ஆன்மீக ஈடுபாடு கூடும்; உடல் நலனில் எச்சரிக்கை தேவை.',
        'career_en': 'Feeling uninspired by routine corporate ladder; seeking autonomy or ethical vocations.',
        'career_ta': 'பணியில் திடீர் சலிப்பு ஏற்படலாம்; சுயேச்சை மற்றும் ஆன்மீகப் பணிகள் மன நிம்மதி தரும்.',
        'wealth_en': 'Expenditures on charitable causes and medical check-ups; avoid speculative bets.',
        'wealth_ta': 'மருத்துவச் செலவுகள் மற்றும் தான தர்மங்கள் உண்டாகும்; பண முதலீடுகளில் விழிப்புணர்வு.',
        'health_en': 'Vitality needs care; watch fever, sunstroke, and inflammatory ailments.',
        'health_ta': 'காய்ச்சல், உஷ்ணக் கட்டிகள் வரலாம்; சுத்தமான குடிநீர் மற்றும் எளிய உணவு அவசியம்.',
        'family_en': 'Spiritual sanctuary at home; cultivate compassionate patience with elders.',
        'family_ta': 'தந்தையின் உடல் நலம் பேணவும்; அமைதியான முறையில் குடும்ப விஷயங்களை அணுகவும்.',
        'milestones_en': 'Pilgrimage to mountain or solar shrines, profound meditation breakthrough.',
        'milestones_ta': 'சூரிய தலங்களுக்கு யாத்திரை செல்லுதல், ஆன்ம அமைதி அடைதல், தியானப் பழக்கம்.',
        'remedy_en': 'Worship Lord Ganesha and Surya; offer red flowers to Ganapati on Tuesdays.',
        'remedy_ta': 'செவ்வாய்க்கிழமைகளில் விநாயகருக்கு செவ்வரளி பூ சாற்றி மோதகம் நைவேத்தியம் செய்யவும்.',
        'base_potency': 2
    },
    ('Sun', 'Venus'): {
        'title_en': 'Sun-Venus: Diplomatic Alliances & Royal Hospitality',
        'title_ta': 'சூரிய தசை — சுக்கிர புக்தி: தசா சந்தி & அரசு-கலை நற்பலன்',
        'theme_en': 'Combining prestige with aesthetics; concluding phase of 6-year Sun cycle.',
        'theme_ta': 'கௌரவமும் கலை நயமும் இணைந்த காலம்; சூரிய தசையின் நிறைவு புக்தி; சுப அனுகூலம்.',
        'career_en': 'Public relations, luxury government projects, diplomatic protocol, cultural missions.',
        'career_ta': 'பொது மக்கள் தொடர்பு, கலை மற்றும் அழகு சாதனத் துறைகளில் புதிய வாய்ப்புகள்.',
        'wealth_en': 'Expenditure on high-status celebrations and hospitality; balanced financial inflows.',
        'wealth_ta': 'அந்தஸ்துக்கான செலவுகள் கூடும்; அதே சமயம் வரவும் சீராக இருக்கும்; நகைகள் வாங்கும் யோகம்.',
        'health_en': 'Watch hormonal balance, hydration, and eye strain; avoid excessive rich foods.',
        'health_ta': 'நீர் சம்பந்தமான உபாதைகள், கண் எரிச்சல் வரலாம்; பழங்கள் மற்றும் இளநீர் உட்கொள்ளவும்.',
        'family_en': 'Spouse achieves recognition; maintain mutual respect and avoid subtle ego clashes.',
        'family_ta': 'வாழ்க்கைத் துணையின் முன்னேற்றம்; இல்லத்தில் மங்கல காரியப் பேச்சுக்கள் சுபமாகும்.',
        'milestones_en': 'Diplomatic honors, high-profile social wedding, major acquisition of luxury assets.',
        'milestones_ta': 'சமூகத்தில் முக்கியஸ்தர்களின் நட்பு, இல்லத்தில் மங்கல விழாக்கள் இனிதே முடிதல்.',
        'remedy_en': 'Worship Goddess Mahalakshmi with white lotus; donate food to cows on Fridays.',
        'remedy_ta': 'வெள்ளிக்கிழமைகளில் பசுவிற்கு அகத்திக்கீரை வழங்கி மகாலட்சுமியை வழிபடவும்.',
        'base_potency': 3
    }
}

# Generic fallback builder for remaining Dasa-Bhukti pairs
def get_dasa_bhukti_reading(d_lord: str, b_lord: str, mutual_kendra: int, d_dignity: str, b_dignity: str) -> Dict[str, Any]:
    key = (d_lord, b_lord)
    if key in DASA_BHUKTI_ARCHETYPES:
        arch = dict(DASA_BHUKTI_ARCHETYPES[key])
    else:
        # Generate astrological reading based on planetary nature & mutual house distance
        d_ta = PLANET_TAMIL.get(d_lord, d_lord)
        b_ta = PLANET_TAMIL.get(b_lord, b_lord)

        is_trikone = mutual_kendra in (1, 5, 9)
        is_upachaya = mutual_kendra in (3, 11)
        is_kendra = mutual_kendra in (4, 7, 10)
        is_dusthana = mutual_kendra in (6, 8, 12)

        if is_trikone:
            axis_en = f"Harmonious {mutual_kendra}-Trikona Alignment"
            axis_ta = "திரிகோண சுப அமைப்பு"
            potency = 5
            trend_en = f"Brings auspicious expansion, spiritual merit fruition, and creative success under {d_lord}-{b_lord}."
            trend_ta = f"{d_ta} தசையில் {b_ta} புக்தி நற்பலன்களை வாரி வழங்கும் திரிகோண சுப காலம்."
            career_en = f"Promotions and favorable transitions; {b_lord} enhances professional reputation."
            career_ta = "பதவி உயர்வு, பாராட்டுகள்; தொழிலில் புதிய உயரங்களை எட்டும் காலம்."
            wealth_en = "Smooth financial liquidity and gains through legitimate efforts."
            wealth_ta = "தன வரவு திருப்திகரமாக இருக்கும்; சுப காரியங்களுக்கு முதலீடுகள் உதவும்."
            health_en = "Vibrant health and peaceful mental disposition."
            health_ta = "ஆரோக்கியம் சிறப்பாக இருக்கும்; மன அமைதி கூடும்."
        elif is_upachaya:
            axis_en = f"Progressive {mutual_kendra}-Upachaya Growth"
            axis_ta = "உபசெய ஸ்தான வளர்ச்சி"
            potency = 4
            trend_en = f"Steady effort yields tangible material gains and victory over past delays."
            trend_ta = f"கடின உழைப்பிற்கு ஏற்ற நிலையான வெற்றி மற்றும் பொருளாதார வளர்ச்சி கிட்டும் காலம்."
            career_en = f"Expansion of enterprise and network; {b_lord} channels practical achievements."
            career_ta = "புதிய தொழில் முயற்சிகளில் லாபம்; நண்பர்கள் மற்றும் கூட்டாளிகள் ஆதரவு."
            wealth_en = "Progressive increase in earnings, recovery of pending debts."
            wealth_ta = "பண வரவு படிப்படியாக உயரும்; நிலுவைத் தொகைகள் வசூலாகும்."
            health_en = "Strong stamina and resilience overcoming minor seasonal ailments."
            health_ta = "உடல் வலிமை கூடும்; சோர்வு நீங்கி சுறுசுறுப்பு மேலோங்கும்."
        elif is_dusthana:
            axis_en = f"Transformational {mutual_kendra}-House Karmic Transition"
            axis_ta = "மறைவு ஸ்தான எச்சரிக்கை & கர்ம காலம்"
            potency = 2
            trend_en = f"Calls for patient vigilance, spiritual surrender, and avoidance of hasty risks."
            trend_ta = f"நிதானமும் விவேகமும் தேவைப்படும் காலம்; அவசர முடிவுகளைத் தவிர்ப்பது நல்லது."
            career_en = f"Patience required in workplace interactions; safeguard documents and maintain ethics."
            career_ta = "பணியிடத்தில் பொறுமை அவசியம்; உயர் அதிகாரிகளிடம் வீண் வாக்குவாதங்களை தவிர்க்கவும்."
            wealth_en = "Controlled spending is essential; avoid speculative investments and lending."
            wealth_ta = "சிக்கனம் தேவை; புதிய கடன் வாங்குவதையோ கொடுப்பதையோ தவிர்க்கவும்."
            health_en = "Prioritize preventative wellness, stress management, and nutritious diet."
            health_ta = "உடல் நலம் மற்றும் மன உளைச்சலில் கவனம்; தியானம் மற்றும் நடைப்பயிற்சி நலம் தரும்."
        else:
            axis_en = f"Dynamic {mutual_kendra}-Kendra Action"
            axis_ta = "கேந்திர ஸ்தான செயல் காலம்"
            potency = 4
            trend_en = f"Worldly activity and major domestic and career developments."
            trend_ta = f"வாழ்வியல் திருப்பங்கள் மற்றும் புதிய பொறுப்புகள் உருவாகும் காலம்."
            career_en = f"Direct authority and visible leadership accomplishments."
            career_ta = "புதிய பொறுப்புகள், தலைமைப் பண்பு வெளிப்படுதல், நிர்வாக வெற்றி."
            wealth_en = "Investments in fixed assets, vehicles, or home enhancements."
            wealth_ta = "நிலம், வீடு, வாகனங்கள் சார்ந்த சுபச் செலவுகள் உண்டாகும்."
            health_en = "Energetic constitution; maintain adequate rest during busy schedules."
            health_ta = "சுறுசுறுப்பான உடல் நிலை; உரிய ஓய்வு எடுப்பது நலம்."

        arch = {
            'title_en': f"{d_lord} Maha Dasa — {b_lord} Bhukti ({axis_en})",
            'title_ta': f"{d_ta} தசை — {b_ta} புக்தி ({axis_ta})",
            'theme_en': trend_en,
            'theme_ta': trend_ta,
            'career_en': career_en,
            'career_ta': career_ta,
            'wealth_en': wealth_en,
            'wealth_ta': wealth_ta,
            'health_en': health_en,
            'health_ta': health_ta,
            'family_en': f"Family events guided by {b_lord}; fostering cooperative dialogue and domestic stability.",
            'family_ta': f"குடும்பத்தில் அமைதி; உறவினர்களிடையே ஒற்றுமை பேணுவது நலம் பயக்கும்.",
            'milestones_en': f"Key milestone in {b_lord}'s domain; progress through deliberate dedication.",
            'milestones_ta': f"முக்கிய சுப காரியங்கள், கல்வி / தொழில் முன்னேற்றம், சமூக மதிப்பு.",
            'remedy_en': f"Propitiate {b_lord} through dedicated mantras and charitable food distribution.",
            'remedy_ta': f"{b_ta} பகவானுக்குரிய வழிபாடுகள் செய்து, எளியோருக்கு அன்னதானம் செய்வது சுபம்.",
            'base_potency': potency
        }

    return arch


def calculate_timeline_predictions(chart: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate 81 chronological Dasa-Bhukti periods and annual forecast projections."""
    dasha_rows = chart.get('dasha', [])
    planets = chart.get('planets', {})
    now_dt = datetime.now(timezone.utc)

    utc_val = chart.get('utc')
    if isinstance(utc_val, datetime):
        birth_dt = utc_val
        if birth_dt.tzinfo is None:
            birth_dt = birth_dt.replace(tzinfo=timezone.utc)
    elif isinstance(utc_val, str) and utc_val:
        try:
            birth_dt = datetime.fromisoformat(utc_val)
            if birth_dt.tzinfo is None:
                birth_dt = birth_dt.replace(tzinfo=timezone.utc)
        except Exception:
            birth_dt = now_dt
    else:
        # Fallback to first dasha subperiod start if available
        if dasha_rows and dasha_rows[0].get('subperiods'):
            try:
                s_iso = dasha_rows[0]['subperiods'][0]['start']
                birth_dt = datetime.fromisoformat(s_iso)
                if birth_dt.tzinfo is None:
                    birth_dt = birth_dt.replace(tzinfo=timezone.utc)
            except Exception:
                birth_dt = now_dt
        else:
            birth_dt = now_dt

    timeline_periods = []
    active_spotlight = None

    for d_idx, d_row in enumerate(dasha_rows):
        d_lord = d_row['lord']
        d_lord_ta = PLANET_TAMIL.get(d_lord, d_lord)

        subperiods = d_row.get('subperiods', [])
        for b_idx, b_row in enumerate(subperiods):
            b_lord = b_row['lord']
            b_lord_ta = PLANET_TAMIL.get(b_lord, b_lord)

            start_iso = b_row['start']
            end_iso = b_row['end']

            try:
                start_dt = datetime.fromisoformat(start_iso)
                end_dt = datetime.fromisoformat(end_iso)
            except Exception:
                start_dt = birth_dt
                end_dt = birth_dt

            # Age at start & end
            age_start = max(0.0, round((start_dt - birth_dt).total_seconds() / (365.2425 * 86400), 1))
            age_end = max(0.0, round((end_dt - birth_dt).total_seconds() / (365.2425 * 86400), 1))
            duration_days = max(1, int((end_dt - start_dt).total_seconds() / 86400))

            is_active = (start_dt <= now_dt < end_dt)
            is_past = (end_dt <= now_dt)
            is_future = (start_dt > now_dt)

            # Mutual Kendra/House calculation
            d_house = planets.get(d_lord, {}).get('house', 1)
            b_house = planets.get(b_lord, {}).get('house', 1)
            mutual_dist = ((b_house - d_house) % 12) + 1

            # Mutual classification & aspect labels
            if mutual_dist in (1, 5, 9):
                mutual_class = 'trine'
                mutual_rel = '1-5-9 Auspicious Trine' if mutual_dist in (5, 9) else '1-1 Swabhukti Alignment'
                mutual_rel_ta = '1-5-9 திரிகோண சுப அமைப்பு' if mutual_dist in (5, 9) else '1-1 சுய புக்தி அமைப்பு'
            elif mutual_dist in (4, 7, 10):
                mutual_class = 'kendra'
                mutual_rel = '1-7 Full Mutual Aspect' if mutual_dist == 7 else f'{mutual_dist}-Kendra Dynamic Action'
                mutual_rel_ta = '1-7 நேரடி சம சப்தம பார்வை' if mutual_dist == 7 else f'{mutual_dist}-ஆம் கேந்திர செயல் அமைப்பு'
            elif mutual_dist in (3, 11):
                mutual_class = 'growth'
                mutual_rel = f'{mutual_dist}-11 Upachaya Growth'
                mutual_rel_ta = f'{mutual_dist}-11 உபஜெய வளர்ச்சி அமைப்பு'
            elif mutual_dist in (6, 8):
                mutual_class = 'friction'
                mutual_rel = '6-8 Shadashtaka Friction'
                mutual_rel_ta = '6-8 சஷ்டாஷ்டக கவன அமைப்பு'
            else:  # 2, 12
                mutual_class = 'transition'
                mutual_rel = '2-12 Dwirdwadasa Transition'
                mutual_rel_ta = '2-12 துவித்வாதச சுபவிரய அமைப்பு'

            d_dignity = planets.get(d_lord, {}).get('dignity', 'Neutral')
            b_dignity = planets.get(b_lord, {}).get('dignity', 'Neutral')

            reading = get_dasa_bhukti_reading(d_lord, b_lord, mutual_dist, d_dignity, b_dignity)

            # Potency classification
            potency = reading.get('base_potency', 3)
            if 'Exalted' in (d_dignity, b_dignity):
                potency = min(5, potency + 1)
            elif 'Debilitated' in (d_dignity, b_dignity):
                potency = max(1, potency - 1)

            status_class = 'auspicious' if potency >= 4 else ('moderate' if potency == 3 else 'challenging')
            status_text_en = 'Auspicious ★★★' if potency >= 4 else ('Moderate ★★' if potency == 3 else 'Caution ★')
            status_text_ta = 'சுப காலம் ★★★' if potency >= 4 else ('மத்தியம பலன் ★★' if potency == 3 else 'கவனமான காலம் ★')

            period_obj = {
                'id': f"timeline-{d_idx}-{b_idx}",
                'dasa_lord': d_lord,
                'dasa_lord_ta': d_lord_ta,
                'bhukti_lord': b_lord,
                'bhukti_lord_ta': b_lord_ta,
                'start_iso': start_iso,
                'end_iso': end_iso,
                'start_date': start_iso[:10],
                'end_date': end_iso[:10],
                'age_start': age_start,
                'age_end': age_end,
                'duration_days': duration_days,
                'duration_months': round(duration_days / 30.4375, 1),
                'is_active': is_active,
                'is_past': is_past,
                'is_future': is_future,
                'potency': potency,
                'stars': '★' * potency,
                'status_class': status_class,
                'status_text_en': status_text_en,
                'status_text_ta': status_text_ta,
                'mutual_house': mutual_dist,
                'mutual_class': mutual_class,
                'mutual_rel': mutual_rel,
                'mutual_rel_ta': mutual_rel_ta,
                'title_en': reading['title_en'],
                'title_ta': reading['title_ta'],
                'theme_en': reading['theme_en'],
                'theme_ta': reading['theme_ta'],
                'career_en': reading['career_en'],
                'career_ta': reading['career_ta'],
                'wealth_en': reading['wealth_en'],
                'wealth_ta': reading['wealth_ta'],
                'health_en': reading['health_en'],
                'health_ta': reading['health_ta'],
                'family_en': reading['family_en'],
                'family_ta': reading['family_ta'],
                'milestones_en': reading['milestones_en'],
                'milestones_ta': reading['milestones_ta'],
                'remedy_en': reading['remedy_en'],
                'remedy_ta': reading['remedy_ta']
            }

            timeline_periods.append(period_obj)

            if is_active:
                elapsed_days = max(0, int((now_dt - start_dt).total_seconds() / 86400))
                remaining_days = max(0, int((end_dt - now_dt).total_seconds() / 86400))
                percent = min(100, max(0, int(elapsed_days / duration_days * 100)))

                active_spotlight = {
                    'dasa_lord': d_lord,
                    'dasa_lord_ta': d_lord_ta,
                    'bhukti_lord': b_lord,
                    'bhukti_lord_ta': b_lord_ta,
                    'start_date': start_iso[:10],
                    'end_date': end_iso[:10],
                    'elapsed_days': elapsed_days,
                    'remaining_days': remaining_days,
                    'percent': percent,
                    'age': round((now_dt - birth_dt).total_seconds() / (365.2425 * 86400), 1),
                    'potency': potency,
                    'status_class': status_class,
                    'title_en': reading['title_en'],
                    'title_ta': reading['title_ta'],
                    'strategic_advice_en': reading['theme_en'],
                    'strategic_advice_ta': reading['theme_ta'],
                    'primary_remedy_en': reading['remedy_en'],
                    'primary_remedy_ta': reading['remedy_ta']
                }

    # 10-Year Annual Projections (Current Year - 1 to Current Year + 9)
    current_year = now_dt.year
    annual_projections = []

    for yr in range(current_year - 1, current_year + 10):
        yr_dt = datetime(yr, 7, 1, tzinfo=timezone.utc)
        age = max(0, int((yr_dt - birth_dt).total_seconds() / (365.2425 * 86400)))

        # Find active Dasa & Bhukti in this year
        matched_period = None
        for p in timeline_periods:
            try:
                s_dt = datetime.fromisoformat(p['start_iso'])
                e_dt = datetime.fromisoformat(p['end_iso'])
                if s_dt <= yr_dt < e_dt:
                    matched_period = p
                    break
            except Exception:
                continue

        if not matched_period and timeline_periods:
            matched_period = timeline_periods[0]

        d_lord = matched_period['dasa_lord'] if matched_period else 'Jupiter'
        b_lord = matched_period['bhukti_lord'] if matched_period else 'Venus'
        potency = matched_period['potency'] if matched_period else 4

        icons = ['🌟', '💼', '🏡', '💍', '🎓', '✈️', '🧘', '🏆', '📈', '🕊️']
        chosen_icon = icons[(yr + age) % len(icons)]
        score = 65 + (potency * 6) + ((yr * 7) % 8)

        annual_projections.append({
            'year': yr,
            'age': age,
            'dasa_lord': d_lord,
            'dasa_lord_ta': PLANET_TAMIL.get(d_lord, d_lord),
            'bhukti_lord': b_lord,
            'bhukti_lord_ta': PLANET_TAMIL.get(b_lord, b_lord),
            'dasa_bhukti_str_en': f"{d_lord} / {b_lord}",
            'dasa_bhukti_str_ta': f"{PLANET_TAMIL.get(d_lord, d_lord)} / {PLANET_TAMIL.get(b_lord, b_lord)}",
            'theme_en': matched_period['theme_en'] if matched_period else 'Progressive life milestones.',
            'theme_ta': matched_period['theme_ta'] if matched_period else 'வாழ்வியல் முன்னேற்ற காலம்.',
            'icon': chosen_icon,
            'score': min(98, score),
            'is_current_year': (yr == current_year)
        })

    return {
        'total_periods': len(timeline_periods),
        'periods': timeline_periods,
        'active_spotlight': active_spotlight,
        'annual_projections': annual_projections
    }
