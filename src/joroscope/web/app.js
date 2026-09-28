/**
 * JoRoScope — Modern Precision Vedic Astrology
 * Interactive Application Engine & Multi-Chart Renderer
 */

// Helper utilities
const $ = s => document.querySelector(s);
const $$ = s => document.querySelectorAll(s);
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&gt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

// Constants
const SIGNS_EN = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'];
const SIGNS_TA = ['மேஷம்', 'ரிஷபம்', 'மிதுனம்', 'கடகம்', 'சிம்மம்', 'கன்னி', 'துலாம்', 'விருச்சிகம்', 'தனுசு', 'மகரம்', 'கும்பம்', 'மீனம்'];

const STARS_EN = [
  'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
  'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
  'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha',
  'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishtha', 'Shatabhisha',
  'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
];
const STARS_TA = [
  'அசுவினி', 'பரணி', 'கிருத்திகை', 'ரோகிணி', 'மிருகசீரிஷம்', 'திருவாதிரை',
  'புனர்பூசம்', 'பூசம்', 'ஆயில்யம்', 'மகம்', 'பூரம்', 'உத்திரம்',
  'அஸ்தம்', 'சித்திரை', 'சுவாதி', 'விசாகம்', 'அனுஷம்', 'கேட்டை',
  'மூலம்', 'பூராடம்', 'உத்திராடம்', 'திருவோணம்', 'அவிட்டம்', 'சதயம்',
  'பூரட்டாதி', 'உத்திரட்டாதி', 'ரேவதி'
];

// ta_short: the abbreviations written inside a traditional Tamil jathaga kattam
const PLANET_NAMES = {
  Sun: { en: 'Sun', ta: 'சூரியன்', short: 'Su', ta_short: 'சூ', color: '#f39c12' },
  Moon: { en: 'Moon', ta: 'சந்திரன்', short: 'Mo', ta_short: 'சந்', color: '#ecf0f1' },
  Mars: { en: 'Mars', ta: 'செவ்வாய்', short: 'Ma', ta_short: 'செ', color: '#e74c3c' },
  Mercury: { en: 'Mercury', ta: 'புதன்', short: 'Me', ta_short: 'பு', color: '#2ecc71' },
  Jupiter: { en: 'Jupiter', ta: 'குரு', short: 'Ju', ta_short: 'கு', color: '#f1c40f' },
  Venus: { en: 'Venus', ta: 'சுக்கிரன்', short: 'Ve', ta_short: 'சு', color: '#e056fd' },
  Saturn: { en: 'Saturn', ta: 'சனி', short: 'Sa', ta_short: 'ச', color: '#3498db' },
  Rahu: { en: 'Rahu', ta: 'ராகு', short: 'Ra', ta_short: 'ரா', color: '#95a5a6' },
  Ketu: { en: 'Ketu', ta: 'கேது', short: 'Ke', ta_short: 'கே', color: '#bdc3c7' },
  Ascendant: { en: 'Ascendant', ta: 'லக்னம்', short: 'Asc', ta_short: 'ல', color: '#e5c378' },
  Mandi: { en: 'Mandi', ta: 'மாந்தி', short: 'Md', ta_short: 'மா', color: '#7f8c8d' }
};

const VARGA_NAMES = {
  D1: ['Rasi', 'இராசி'], D2: ['Hora', 'ஹோரை'], D3: ['Drekkana', 'திரேக்காணம்'],
  D4: ['Chaturthamsa', 'சதுர்த்தாம்சம்'], D7: ['Saptamsa', 'சப்தாம்சம்'], D9: ['Navamsa', 'நவாம்சம்'],
  D10: ['Dasamsa', 'தசாம்சம்'], D12: ['Dwadasamsa', 'துவாதசாம்சம்'], D16: ['Shodasamsa', 'ஷோடசாம்சம்'],
  D20: ['Vimsamsa', 'விம்சாம்சம்'], D24: ['Chaturvimsamsa', 'சதுர்விம்சாம்சம்'],
  D27: ['Saptavimsamsa', 'சப்தவிம்சாம்சம்'], D30: ['Trimsamsa', 'திரிம்சாம்சம்'], D60: ['Shashtiamsa', 'ஷஷ்டியாம்சம்'],
  Bhava: ['Bhava Chakra', 'பாவ சக்கரம்']
};

const DIGNITY_TA = {
  Exalted: 'உச்சம்', Debilitated: 'நீசம்', 'Own Sign': 'ஆட்சி', Moolatrikona: 'மூலத்திரிகோணம்',
  'Great Friend': 'அதி நட்பு', Friend: 'நட்பு', Neutral: 'சமம்', Enemy: 'பகை', 'Great Enemy': 'அதி பகை',
  Ascendant: 'லக்னம்'
};

const NITYA_YOGA_TA = {
  Vishkambha: 'விஷ்கம்பம்', Priti: 'ப்ரீதி', Ayushman: 'ஆயுஷ்மான்', Saubhagya: 'சௌபாக்கியம்', Shobhana: 'சோபனம்',
  Atiganda: 'அதிகண்டம்', Sukarma: 'சுகர்மம்', Dhriti: 'திருதி', Shula: 'சூலம்', Ganda: 'கண்டம்', Vriddhi: 'விருத்தி',
  Dhruva: 'துருவம்', Vyaghata: 'வியாகாதம்', Harshana: 'ஹர்ஷணம்', Vajra: 'வஜ்ரம்', Siddhi: 'சித்தி',
  Vyatipata: 'வியதீபாதம்', Variyan: 'வரியான்', Parigha: 'பரிகம்', Shiva: 'சிவம்', Siddha: 'சித்தம்', Sadhya: 'சாத்தியம்',
  Shubha: 'சுபம்', Shukla: 'சுக்லம்', Brahma: 'பிரம்மம்', Indra: 'ஐந்திரம்', Vaidhriti: 'வைதிருதி'
};

const KARANA_TA = {
  Bava: 'பவம்', Balava: 'பாலவம்', Kaulava: 'கௌலவம்', Taitila: 'தைதுலம்', Gara: 'கரசை', Vanija: 'வணிசை',
  Vishti: 'பத்திரை (விஷ்டி)', Shakuni: 'சகுனி', Chatushpada: 'சதுஷ்பாதம்', Naga: 'நாகவம்', Kimstughna: 'கிம்ஸ்துக்னம்'
};

const AYANAMSA_TA = { Lahiri: 'லாஹிரி', Raman: 'ராமன்', Krishnamurti: 'கிருஷ்ணமூர்த்தி (KP)', 'Fagan-Bradley': 'ஃபேகன்-பிராட்லி' };

const HOUSE_BHAVAS_TA = {
  1: 'தனு பாவம் (சுயம்): உடல் வலிமை, மனநிலை, தோற்றம், வாழ்க்கைப் பாதை மற்றும் இயல்பான குணம்.',
  2: 'தன பாவம் (செல்வம்): கையிருப்புச் செல்வம், குடும்பம், பேச்சு, பார்வை, உணவு மற்றும் ஆரம்பக் கல்வி.',
  3: 'சகஜ பாவம் (தைரியம்): உடன்பிறப்புகள், வீரம், படைப்பாற்றல், தகவல் தொடர்பு, முயற்சி மற்றும் குறும் பயணங்கள்.',
  4: 'சுக பாவம் (சுகம்): தாய், நிலம், வாகனம், கல்வி, மன நிறைவு மற்றும் இல்லற அமைதி.',
  5: 'புத்திர பாவம் (சந்ததி & அறிவு): பூர்வ புண்ணியம், ஞானம், குழந்தைகள், முதலீடுகள் மற்றும் மந்திரம்.',
  6: 'ருண ரோக சத்ரு பாவம்: அன்றாடக் கடமைகள், கடன், நோய், சேவை மற்றும் வழக்குகளை வெல்லுதல்.',
  7: 'களத்திர பாவம் (வாழ்க்கைத் துணை): திருமணம், கூட்டுத் தொழில், பொது உறவுகள் மற்றும் ஒப்பந்தங்கள்.',
  8: 'ஆயுள் பாவம் (ஆயுள் & மாற்றம்): ஆயுட்காலம், மறைஞானம், எதிர்பாராத பரம்பரைச் சொத்து, ஆழ்ந்த மாற்றம், ஆராய்ச்சி.',
  9: 'பாக்ய பாவம் (அதிர்ஷ்டம் & ஞானம்): குரு, தர்மம், உயர் தத்துவம், புனித யாத்திரை, தந்தை, ஆன்மீகப் புண்ணியம்.',
  10: 'கர்ம பாவம் (தொழில் & அதிகாரம்): உலக சாதனைகள், சமூக அந்தஸ்து, தொழில் அதிகாரம் மற்றும் கௌரவம்.',
  11: 'லாப பாவம் (லாபம் & ஆசைகள்): ஆசைகள் நிறைவேறுதல், வருமான வளர்ச்சி, மூத்த உடன்பிறப்புகள், செல்வாக்குள்ள நண்பர்கள்.',
  12: 'விரய பாவம் (மோட்சம் & தனிமை): மோட்சம், ஆன்மீகத் தனிமை, தானச் செலவுகள், வெளிநாடு மற்றும் நிம்மதியான உறக்கம்.'
};

// Server validation messages, so errors read in Tamil too
const ERROR_TA = {
  'Choose a date between 1800 and 2200.': '1800 முதல் 2200 வரையிலான தேதியைத் தேர்ந்தெடுக்கவும்.',
  'Enter a valid IANA timezone, such as Asia/Kolkata.': 'சரியான IANA நேர வலயத்தை உள்ளிடவும் (எ.கா. Asia/Kolkata).',
  'This local time did not exist because of a clock change. Correct the birth time.': 'கடிகார மாற்றத்தால் இந்த நேரம் நிகழவில்லை. பிறந்த நேரத்தைச் சரிசெய்யவும்.',
  'This time occurred twice during a clock change. Select the first or second occurrence.': 'கடிகார மாற்றத்தால் இந்த நேரம் இருமுறை நிகழ்ந்தது. முதல் அல்லது இரண்டாம் நிகழ்வைத் தேர்ந்தெடுக்கவும்.',
  'Latitude must be between 66° south and 66° north in this version.': 'அட்சரேகை 66° தெற்கு முதல் 66° வடக்கு வரை இருக்க வேண்டும்.',
  'Longitude must be between -180 and 180.': 'தீர்க்கரேகை -180 முதல் 180 வரை இருக்க வேண்டும்.',
  'Unsupported ayanamsa.': 'இந்த அயனாம்சம் ஆதரிக்கப்படவில்லை.',
  'The Sun does not rise or set at this latitude on this date.': 'இந்த அட்சரேகையில் இன்று சூரியன் உதிப்பதோ மறைவதோ இல்லை.',
  'Both boy and girl data are required for matchmaking.': 'பொருத்தம் பார்க்க ஆண், பெண் இருவரின் விவரங்களும் தேவை.',
  'Invalid request size.': 'கோரிக்கையின் அளவு தவறானது.'
};

const txt = (en, ta) => (currentLang === 'ta' ? ta : en);
const VAARAM_SHORT = [['Sun', 'ஞா'], ['Mon', 'தி'], ['Tue', 'செ'], ['Wed', 'பு'], ['Thu', 'வி'], ['Fri', 'வெ'], ['Sat', 'ச']];
const grahaName = name => PLANET_NAMES[name] ? txt(PLANET_NAMES[name].en, PLANET_NAMES[name].ta) : name;
const grahaNames = (list, sep = ', ') => (list || []).map(grahaName).join(sep);
const dignityLabel = d => txt(d || 'Neutral', DIGNITY_TA[d || 'Neutral'] || d);
const nityaYogaLabel = n => txt(n, NITYA_YOGA_TA[n] || n);
const karanaLabel = n => txt(n, KARANA_TA[n] || n);
const ayanamsaLabel = a => txt(a, AYANAMSA_TA[a] || a);
const errorText = msg => txt(msg, ERROR_TA[msg] || msg);

function signName(sign) {
  const i = typeof sign === 'number' ? sign : SIGNS_EN.indexOf(sign);
  return i < 0 ? sign : txt(SIGNS_EN[i], SIGNS_TA[i]);
}

function starName(star) {
  const i = STARS_EN.indexOf(star);
  return i < 0 ? star : txt(STARS_EN[i], STARS_TA[i]);
}

const TITHI_TA = {
  Prathama: 'பிரதமை', Dwitiya: 'துவிதியை', Tritiya: 'திருதியை', Chaturthi: 'சதுர்த்தி', Panchami: 'பஞ்சமி',
  Shashthi: 'சஷ்டி', Saptami: 'சப்தமி', Ashtami: 'அஷ்டமி', Navami: 'நவமி', Dashami: 'தசமி',
  Ekadashi: 'ஏகாதசி', Dwadashi: 'துவாதசி', Trayodashi: 'திரயோதசி', Chaturdashi: 'சதுர்த்தசி',
  Purnima: 'பௌர்ணமி', Amavasya: 'அமாவாசை'
};

const HOUSE_BHAVAS = {
  1: 'Tanu Bhava (The Self): Physical vitality, mental constitution, appearance, life path, and innate character.',
  2: 'Dhana Bhava (Wealth): Liquid capital, family heritage, eloquence, vision, food, and early learning.',
  3: 'Sahaja Bhava (Courage): Siblings, bravery, creative self-expression, communications, enterprise, short travels.',
  4: 'Sukha Bhava (Happiness): Mother, fixed property, vehicles, education, inner contentment, emotional anchor.',
  5: 'Putra Bhava (Progeny & Intellect): Purva Punya (past life merit), creative wisdom, children, investments, mantras.',
  6: 'Ari Bhava (Adversaries & Health): Daily duties, resilience over debts and disease, service, overcoming disputes.',
  7: 'Kalatra Bhava (Partnership): Marriage, life partner, business associations, public relations, contracts.',
  8: 'Ayur Bhava (Longevity & Transformation): Lifespan, occult wisdom, sudden inheritances, deep transformation, research.',
  9: 'Dharma Bhava (Fortune & Wisdom): Guru, righteous conduct, higher philosophy, pilgrimages, father, spiritual merit.',
  10: 'Karma Bhava (Profession & Authority): Worldly achievements, social standing, career authority, public karma, honor.',
  11: 'Labha Bhava (Gains & Aspirations): Realization of ambitions, capital expansion, elder siblings, influential allies.',
  12: 'Vyaya Bhava (Liberation & Solitude): Moksha, spiritual seclusion, philanthropic expenses, foreign lands, sleep peace.'
};

const ZODIAC_SYMBOLS = ['♈', '♉', '♊', '♋', '♌', '♍', '♎', '♏', '♐', '♑', '♒', '♓'];

// State
let currentChart = null;
let currentVarga = 'D1';
let currentStyle = 'south';
let currentLang = 'en';
let currentTheme = 'dark';
let citiesList = [];
let currentDasaMode = 'timeline';
let currentTimelineFilter = 'active';
let currentTimelinePlanet = 'all';
let timelineSearchYear = null;
let lastDailyPanchangam = null;
let lastMatch = null;
let calendarMonth = null;  // {year, month} shown in the monthly Tamil calendar
let lastCalendar = null;
const STORAGE_KEY = 'joroscope_profiles_v2';
const LEGACY_STORAGE_KEY = 'astrology-reborn-profiles-v1';

// Seed sample profiles for multi-person demonstration
const DEFAULT_SEED_PROFILES = [
  {
    id: 'seed-raman-1990',
    name: 'Sri Raman',
    date: '1990-01-01',
    time: '12:00:00',
    city: 'Chennai (Madras)',
    latitude: 13.0827,
    longitude: 80.2707,
    timezone: 'Asia/Kolkata',
    ayanamsa: 'Lahiri',
    fold: '',
    lagna: 'Pisces',
    lagna_ta: 'மீனம்',
    moon_sign: 'Aquarius',
    moon_sign_ta: 'கும்பம்',
    nakshatra: 'Dhanishtha',
    nakshatra_ta: 'அவிட்டம்',
    nakshatra_idx: 22,
    sign_idx: 10,
    pada: 4,
    created_at: '2026-01-01T12:00:00.000Z'
  },
  {
    id: 'seed-kalyani-1994',
    name: 'Kalyani Devi',
    date: '1994-05-18',
    time: '08:30:00',
    city: 'Madurai, India',
    latitude: 9.9252,
    longitude: 78.1198,
    timezone: 'Asia/Kolkata',
    ayanamsa: 'Lahiri',
    fold: '',
    lagna: 'Gemini',
    lagna_ta: 'மிதுனம்',
    moon_sign: 'Cancer',
    moon_sign_ta: 'கடகம்',
    nakshatra: 'Ashlesha',
    nakshatra_ta: 'ஆயில்யம்',
    nakshatra_idx: 8,
    sign_idx: 3,
    pada: 4,
    created_at: '2026-01-02T08:30:00.000Z'
  },
  {
    id: 'seed-vikram-1988',
    name: 'Vikramaditya',
    date: '1988-11-22',
    time: '18:45:00',
    city: 'Coimbatore, India',
    latitude: 11.0168,
    longitude: 76.9558,
    timezone: 'Asia/Kolkata',
    ayanamsa: 'Lahiri',
    fold: '',
    lagna: 'Taurus',
    lagna_ta: 'ரிஷபம்',
    moon_sign: 'Aries',
    moon_sign_ta: 'மேஷம்',
    nakshatra: 'Bharani',
    nakshatra_ta: 'பரணி',
    nakshatra_idx: 1,
    sign_idx: 0,
    pada: 3,
    created_at: '2026-01-03T18:45:00.000Z'
  }
];

// Internationalization dictionary
const I18N = {
  en: {
    workspace: 'WORKSPACE',
    birth_chart: 'Birth Chart & Vargas',
    planets_strengths: 'Planets & Dignity',
    ashtakavarga: 'Ashtakavarga',
    yogas_doshas: 'Yogas & Doshas',
    vimshottari_dasa: 'Vimshottari Dasa',
    life_readings: 'Life Predictions',
    matching: 'Horoscope Matching',
    daily_panchangam: 'Daily Panchangam',
    saved_profiles: 'Saved Profiles',
    local_engine: 'Swiss Ephemeris Local',
    private_data: 'Zero cloud tracking · 100% Private',
    my_location: 'My Location',
    print_pdf: 'Print / PDF',
    birth_details: 'Birth Details',
    enter_natal: 'Enter natal moment & location',
    full_name: 'Full Name',
    birth_date: 'Date',
    birth_time: 'Time (24h)',
    birthplace: 'Birthplace',
    latitude: 'Latitude (°N/S)',
    longitude: 'Longitude (°E/W)',
    timezone: 'IANA Timezone',
    ayanamsa: 'Ayanamsa',
    dst_clock: 'Clock Fold (DST)',
    generate_chart: 'Generate Birth Chart',
    ready_to_reveal: 'Ready to Reveal the Sky',
    enter_details_prompt: 'Enter birth details and click Generate to view South Indian, North Indian, and 14 Divisional Vargas with deep planetary analysis.',
    save_profile: 'Save Profile',
    export_pdf: 'Export PDF',
    ascendant: 'ASCENDANT (LAGNA)',
    moon_sign: 'MOON SIGN (RASI)',
    birth_star: 'BIRTH STAR (NAKSHATRA)',
    active_dasa: 'ACTIVE DASA TODAY',
    south_indian: 'South Indian',
    north_diamond: 'North Indian (Diamond)',
    east_indian: 'East Indian',
    click_house: 'Click any house',
    occupant_planets: 'Occupant Planets',
    aspects_received: 'Aspects Received From',
    ashtakavarga_sav: 'Sarvashtakavarga Points',
    house_significations: 'House Significations (Bhavas)',
    astronomical_engine: 'ENGINE & METHOD',
    julian_day: 'JULIAN DAY',
    ayanamsa_value: 'AYANAMSA OFFSET',
    graha: 'Graha',
    sign: 'Sign',
    degrees: 'Degree',
    star_pada: 'Star / Pada',
    house: 'House',
    dignity: 'Dignity',
    motion_status: 'Status',
    aspects_cast: 'Aspects Cast (Houses)',
    sav_title: 'Sarvashtakavarga (SAV) Points',
    bav_title: 'Bhinnashtakavarga (BAV) Table',
    detected_yogas: 'Detected Planetary Yogas',
    current_running_period: 'CURRENT ACTIVE PERIOD TODAY',
    lagna_path: 'Ascendant & Life Path',
    moon_mind: 'Moon & Emotional Blueprint',
    sun_vitality: 'Surya & Soul Purpose',
    career_karma: 'Career & 10th House Karma',
    wealth_gains: 'Wealth & Financial Fortune',
    relationships_7th: 'Marriage & Partnerships',
    active_dasa_focus: 'Current Dasa Period Focus',
    tithi: 'TITHI (LUNAR DAY)',
    nakshatra: 'NAKSHATRA (CONSTELLATION)',
    nitya_yoga: 'YOGA (SOLI-LUNAR)',
    karana: 'KARANA (HALF-TITHI)',
    export_json: 'Export JSON Backup',
    import_json: 'Import JSON Backup',
    save_person: 'Save',
    new_person: 'New Person',
    clear_all: 'Clear All',
    load_saved_profile: 'Select Saved Person',
    quick_load_person: '👤 -- Quick Load Person --',
    timeline_predictions_mode: 'Timeline Predictions',
    tabular_cycles_mode: 'Tabular Date Cycles (3 Tiers)',
    live_active_period: 'ACTIVE LIFE PERIOD TODAY',
    running_dates: 'DATES & SPAN',
    current_age: 'CURRENT AGE',
    elapsed_time: 'DAYS ELAPSED',
    remaining_time: 'DAYS REMAINING',
    strategic_focus: 'Period Focus & Strategy',
    primary_remedy: 'Prescribed Vedic Remedy & Mantra',
    filter_active: 'Active Today',
    filter_next5: 'Next 5 Years',
    filter_annual: 'Annual Milestones',
    filter_all: 'Full Life (81 Periods)',
    filter_auspicious: 'Auspicious (3+ ★)',
    filter_caution: 'Caution Periods',
    filter_by_lord: 'Maha Dasa Lord:',
    jump: 'Go',
    annual_projections_title: '10-Year Rolling Annual Projections',
    annual_projections_sub: 'Milestones and astrological favorability score for current era',
    open_timeline_studio: 'Open Interactive 81-Period Timeline Studio →',
    city_helper: 'Search historical database or use coordinates below.',
    print_jathagam: 'Print Jathagam',
    title_print_jathagam: 'Print a traditional horoscope sheet: birth notes, Rasi and Navamsa, planets and Dasa-Bhukti',
    bhava_col: 'Bhava (Sripati)',
    gowri_title: 'Gowri Panchangam (Nalla Neram)',
    gowri_sub: 'Amirdham, Uthi, Laabam, Dhanam and Sugam are good times; Rogam, Soram and Visham are avoided.',
    saturn_cycles_title: 'Saturn Cycles Through Life',
    saturn_cycles_sub: 'Ezharai (Sade Sati), Ardhashtama, Kandaka and Ashtama Sani, counted from your Moon sign, from first entry to final exit.',
    th_cycle: 'Cycle',
    th_period: 'Period',
    th_age: 'Age',
    th_phases: 'Phases',
    print_porutham: 'Print Porutham Report',
    title_print_porutham: 'Print the compatibility report',
    upagrahas_title: 'Upagrahas (Sub-planets)',
    upagrahas_sub: "Kaala, Mrityu, Artha Praharaka and Yama Ghantaka rise mid-way through their lord's part of the day or night, Gulika at the start of Saturn's; the Dhuma group is derived from the Sun.",
    th_upagraha: 'Upagraha',
    yogini_mode: 'Yogini Dasa',
    yogini_title: 'Yogini Dasa (36-Year Cycle)',
    yogini_sub: 'Eight yoginis ruled by the Moon, Sun, Jupiter, Mars, Mercury, Saturn, Venus and Rahu; the birth star fixes the first.',
    month_cal_title: 'Tamil Monthly Calendar',
    month_cal_sub: 'Tithi and star at sunrise with Amavasai, Pournami, Ekadasi, Pradosham, Sashti, Sankatahara Chaturthi, Masa Shivaratri and Karthigai.',
    rasi_navamsa: 'Rasi + Navamsa',
    jathaga_kurippu: 'Tamil Jathaga Kurippu',
    jathaga_kurippu_sub: 'Birth notes in the Tamil almanac tradition',
    chevvai_dosham: 'Chevvai Dosham (Kuja / Manglik)',
    rahu_ketu_dosham: 'Rahu-Ketu Dosham',
    dosha_samyam: 'Dosha Samyam (Chevvai & Papa Balance)',
    dosha: 'Dosha',
    bride: 'Bride',
    groom: 'Groom',
    samyam: 'Samyam',
    panch_date: 'Date',
    panch_now: 'Now',
    panch_location: 'LOCATION',
    panch_location_hint: 'From the birth form. Use 📍 My Location to switch.',
    tamil_calendar: 'TAMIL CALENDAR',
    soolam: 'SOOLAM (AVOID TRAVEL)',
    chandrashtamam: 'CHANDRASHTAMAM',
    personal_balam: 'Your Day: Tara & Chandra Balam',
    tara_balam: 'TARA BALAM',
    chandra_balam: 'CHANDRA BALAM',
    five_limbs: 'Five Limbs of Time (Pancha-Anga)',
    vaaram: 'VAARAM (WEEKDAY)',
    muhurtha_local: 'Muhurtha Windows (Local Time)',
    sunrise_sunset: 'Sunrise & Sunset',
    abhijit: 'Abhijit Muhurtham',
    abhijit_sub: 'Most auspicious daytime window',
    rahu_kalam: 'Rahu Kalam',
    rahu_kalam_sub: 'Inauspicious period ruled by Rahu',
    yamagandam: 'Yamagandam',
    yamagandam_sub: 'Inauspicious period ruled by Yama',
    kuligai: 'Kuligai (Gulika Kalam)',
    kuligai_sub: "Saturn's segment: avoid beginnings that should not repeat",
    peyarchi_title: 'Upcoming Peyarchi (Sign Changes)',
    peyarchi_date: 'Date',
    peyarchi_from_to: 'From → To',
    house_from_moon: 'House from Moon',
    gochara_table_title: 'Gochara Today with Ashtakavarga',
    bindus: 'Bindus',
    transit_result: 'Result',
    next_chandrashtamam: 'NEXT CHANDRASHTAMAM',
    star_birthday: 'NAKSHATRA BIRTHDAY',
    hora_title: 'Hora (Orai) Timings',
    hora_sub: 'Twelve day and twelve night horas from sunrise; Moon, Mercury, Jupiter and Venus horas are auspicious.',
    sacred_geometry: "ASTRONOMICAL PRECISION & VEDIC TRADITION",
    birth_chart_heading: "Your Celestial Blueprint",
    birth_chart_sub: "Explore planetary alignments across Rasi, Navamsa, and 14 Parashara divisional vargas.",
    planetary_status: "GRAHA AVASTHAS & DRISHTI",
    planets_sub: "Detailed degrees, nakshatra padas, dignities, combustion, speed, and Vedic aspects.",
    parashara_system: "PARASHARA ASHTAKAVARGA SYSTEM",
    ashtakavarga_sub: "Sarvashtakavarga (337 total points) and Bhinnashtakavarga bindu distribution across all 12 signs.",
    karmic_combinations: "VEDIC COMBINATIONS & DOSHAS",
    yogas_sub: "Automatic detection of Pancha Mahapurusha, Raja, Dhana, and Vipareeta Yogas plus Kuja and Kaal Sarp analysis.",
    planetary_cycles: "120-YEAR VIMSHOTTARI CYCLE & LIFE TIMELINE",
    dasa_sub: "Chronological life forecasting across all 9 Maha Dasas & 81 Bhukti periods, mutual planetary alignments, and 10-year annual projections.",
    astrological_synthesis: "COMPREHENSIVE HOROSCOPE PREDICTION REPORT",
    predictions_sub: "Traditional Parashara and Tamil astrological readings: Nakshatra, Lagna, 12 Bhavas, Planets in Houses, Dasa-Bhukti, Transits & Lucky Gemstones.",
    marital_compatibility: "KUNDALI MILAN & 10 PORUTHAMS",
    matching_sub: "Compute traditional South Indian 10 Poruthams and North Indian 36 Guna Milan with precision.",
    celestial_calendar: "NITYA PANCHANGA & TIMINGS",
    panchangam_sub: "Five elements of time: Tithi, Vaara, Nakshatra, Yoga, and Karana with auspicious Muhurtham windows.",
    browser_vault: "LOCAL BROWSER VAULT",
    profiles_sub: "Manage your family and client charts locally in this browser. Backup and restore anytime.",
    brand_sub: "VEDIC HOROSCOPE",
    engine_status: "Swiss Ephemeris 2.10",
    title_geo: "Use current GPS location",
    title_lang: "Switch Language",
    title_theme: "Toggle Light/Dark Theme",
    title_print: "Print or Save PDF",
    title_quick_load: "Choose a saved person to instantly load and calculate their horoscope",
    title_save_person: "Save this person's details to local vault",
    title_new_person: "Clear form for a new person",
    ph_name: "Name for this chart",
    city_count: "5,481 cities",
    ph_city: "Type city name (e.g. Chennai, Madurai, London)...",
    ayan_lahiri: "Lahiri (Chitra Paksha - Standard)",
    ayan_raman: "B.V. Raman",
    ayan_kp: "KP (Krishnamurti)",
    ayan_fagan: "Fagan-Bradley (Western Sidereal)",
    fold_auto: "Automatic",
    fold_first: "1st occurrence (Standard)",
    fold_second: "2nd occurrence (Repeated)",
    pill_vargas: "✦ 14 Divisional Vargas",
    pill_ashtaka: "✦ Parashara Ashtakavarga",
    pill_dasa: "✦ 3-Tier Dasa",
    pill_yoga: "✦ Yoga Engine",
    pill_porutham: "✦ 10 Poruthams",
    title_save_local: "Save to local browser storage",
    title_export_pdf: "Export as PDF / Print",
    legend_benefic: "Benefic",
    legend_malefic: "Malefic",
    legend_combust: "🔥 Combust",
    click_house_rest: "to inspect lord, occupants, aspects received, and house significations.",
    sav_note: "Auspicious houses (>28 points) cultivate strength and ease; houses under 28 require mindful attention.",
    sav_total: "Total: 337 Bindus",
    th_planet: "Planet",
    kaal_sarp_title: "Kaal Sarp Dosha",
    spotlight_calc_note: "Calculated via Swiss Ephemeris Vimshottari Balance",
    tl_all: "🪐 All 9 Maha Dasas",
    tl_sun: "☀️ Sun (சூரியன்)",
    tl_moon: "🌙 Moon (சந்திரன்)",
    tl_mars: "♂️ Mars (செவ்வாய்)",
    tl_rahu: "☊ Rahu (ராகு)",
    tl_jupiter: "♃ Jupiter (குரு)",
    tl_saturn: "♄ Saturn (சனி)",
    tl_mercury: "☿ Mercury (புதன்)",
    tl_ketu: "☋ Ketu (கேது)",
    tl_venus: "♀️ Venus (சுக்கிரன்)",
    ph_jump_year: "Jump Year (e.g. 2026)",
    title_jump_year: "Jump to year",
    year_by_year: "Year-by-Year Forecast",
    jump_active_dasa: "Jump to Active Dasa",
    pt_natal: "🌟 Natal & Personality",
    pt_bhavas: "🏛️ 12 Bhavas (Houses)",
    pt_planets: "🪐 Planets in Houses",
    pt_dasa: "⏳ Dasa-Bhukti Forecast",
    pt_transits: "🌌 Transits (Gochara)",
    pt_remedies: "💎 Lucky Gems & Remedies",
    pt_jaimini: "🪷 Jaimini Karakas",
    pt_timing: "⏱️ Double Transit (BVB)",
    pt_career: "💼 D-10 Career & Vocation",
    pt_ayur: "🌿 Ayur-Jyotish Wellness",
    pt_kakshya: "📐 Ashtakavarga Kakshyas",
    pt_shadbala: "⚖️ Shadbala Strengths",
    pt_kp: "🔍 KP System Sub-Lords",
    pt_bnn: "📜 Bhrigu Nandi Nadi",
    pt_avasthas: "✨ Planetary Avasthas",
    pt_pada: "🎯 Nakshatra Pada Reading",
    pt_sahams: "🔮 Sensitive Sahams",
    h_bhavas: "12 Bhavas Comprehensive Life Path",
    pill_all_houses: "All 12 Houses",
    p_bhavas: "Detailed astrological life readings for each house based on house lord placement, occupants, aspects, and Sarvashtakavarga strength.",
    h_planet_positions: "Planetary Positions & Influence",
    pill_9_grahas: "9 Grahas",
    p_planets: "Specific effects of Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, and Ketu in their respective natal houses.",
    active_dasa_forecast: "ACTIVE DASA-BHUKTI FORECAST",
    h_maha_dasas: "9 Maha Dasas Life Cycles",
    pill_120_years: "120 Years",
    h_transits: "Planetary Transits (Gochara)",
    pill_current_weather: "Current Astrological Weather",
    p_transits: "Transit analysis calculated from your Janma Rasi (Moon Sign).",
    h_remedies: "Auspicious Factors, Gemstones & Remedies",
    pill_guidance: "Astrological Guidance",
    p_remedies: "Prescribed gemstones, auspicious numbers, days, colors, and protective deities calculated for your Lagna.",
    h_gems: "Recommended Gemstones",
    sub_gems: "Life & Fortune Stones",
    h_lucky: "Lucky Numbers, Days & Colors",
    sub_lucky: "Favorable Cosmic Alignments",
    pill_upadesha: "Upadesha Sutras",
    p_jaimini: "Degree-based variable significators revealing the soul's karmic evolution (Atmakaraka), career path (Amatyakaraka), mentors, mother, progeny, challenges, and life partner (Darakaraka).",
    soul_purpose: "SOUL'S SUPREME PURPOSE (KARAKAMSHA IN NAVAMSA D-9)",
    p_double_transit: "Empirically validated law: Major milestones eventuate only when Saturn (Discipline & Karma) and Jupiter (Grace & Expansion) simultaneously cast their aspects on designated natal houses.",
    transit_saturn_today: "TRANSIT SATURN TODAY",
    transit_jupiter_today: "TRANSIT JUPITER TODAY",
    h_career: "D-10 Dasamsa & Vocation Aptitude Analysis",
    pill_bvb: "BVB Tested Framework",
    p_career: "Cross-analysis of Rasi (D-1), Dasamsa (D-10), and Amatyakaraka (AmK) calculating objective aptitude scores across 5 proven career archetypes.",
    h_ayur: "Ayur-Jyotish & Tridosha Wellness Framework",
    pill_charaka: "Charaka & Prashna Marga",
    p_ayur: "Classical Ayurvedic constitutional analysis evaluating Vata, Pitta, and Kapha balances, metabolic tendencies, and organ system resilience.",
    prakriti: "NATAL PRAKRITI CONSTITUTION",
    vata_label: "Vata (வாதம் - Air/Ether)",
    pitta_label: "Pitta (பித்தம் - Fire)",
    kapha_label: "Kapha (கபம் - Water/Earth)",
    h_vulnerabilities: "Anatomical Vulnerabilities",
    sub_6th: "6th House (Roga Bhava) & 6th Lord",
    h_lifestyle: "Ayurvedic Preventative Lifestyle",
    sub_lifestyle: "Dietary & Yogic Recommendations",
    h_kakshya: "Ashtakavarga Kakshya Micro-Transit System",
    pill_raman_patel: "Dr. B.V. Raman & C.S. Patel",
    p_kakshya: "Precision timing dividing each zodiac sign into 8 Kakshyas (3°45' each). A transit planet yields fruitful results (Phala-Prada) only when passing through Kakshyas where it contributed a bindu in its BAV.",
    h_sat_kakshya: "Saturn Transit Kakshyas",
    h_jup_kakshya: "Jupiter Transit Kakshyas",
    th_degree_range: "Degree Range",
    th_lord: "Lord",
    th_bav_bindu: "BAV Bindu",
    th_result: "Result",
    h_shadbala: "Shadbala Six-Fold Planetary Potency Engine",
    pill_shadbala: "Classical Vedic Mathematical Strength",
    dominant_planet: "DOMINANT GUIDING PLANET (ATMA BALA)",
    karmic_vulnerability: "KARMIC VULNERABILITY (GROWTH FOCUS)",
    h_kp: "Krishnamurti Paddhati (KP System) Sub-Lord Analysis",
    pill_kp: "Prof. K.S. Krishnamurti 249 Divisions",
    p_kp: "The KP System subdivides each of the 27 nakshatras into 9 unequal sub-divisions based on Vimshottari Dasa proportions, pin-pointing life results with extraordinary mathematical precision.",
    h_kp_cuspal: "Core Cuspal Sub-Lord Predictions",
    h_kp_cusps: "12 KP Placidus Cusps (Bhava Sandhis)",
    th_cusp: "Cusp",
    th_degree: "Degree",
    th_sign: "Sign",
    th_sign_lord: "Sign Lord",
    th_star_lord: "Star Lord",
    th_sub_lord: "Sub-Lord",
    h_kp_planets: "9 Planets KP Coordinates",
    h_bnn: "Bhrigu Nandi Nadi (BNN) Karmic Planetary Sutras",
    pill_bnn: "Classical Sage Bhrigu Tradition",
    h_bnn_combos: "Detected Nadi Karmic Combinations & Life Lessons",
    h_avasthas: "Planetary Avasthas & Consciousness States",
    pill_avasthas: "Baladi & Jagradadi Avasthas",
    p_avasthas: "Planets deliver results depending on their age state (Bala, Kumara, Yuva, Vriddha, Mrita) and state of consciousness (Jagrat/Awake, Swapna/Dreaming, Sushupti/Sleeping). This reveals the actual percentage of promised results that materialize in physical reality.",
    h_pada: "Birth Star Quarter (Nakshatra Pada) Destiny Reading",
    birth_star_pada: "BIRTH STAR & PADA",
    navamsa_sign_lord: "NAVAMSA SIGN & LORD",
    h_sahams: "Sensitive Sahams (Tajika Cosmic Lots)",
    p_sahams: "Mathematical sensitive points synthesized from Ascendant, Sun, Moon, and planetary distances, revealing focal vortexes of fortune, wisdom, marriage, career, and physical resilience.",
    h_match_candidates: "Select Match Candidates",
    h_bride: "Bride (Girl's Star & Sign)",
    h_groom: "Groom (Boy's Star & Sign)",
    label_saved_profile: "Saved Profile (Optional)",
    label_nakshatra: "Nakshatra (Birth Star)",
    label_rasi: "Rasi (Moon Sign)",
    btn_calc_match: "Calculate Compatibility Match",
    of_36_gunas: "/ 36 Gunas",
    final_verdict: "FINAL VERDICT",
    h_10_poruthams: "10 South Indian Poruthams",
    th_porutham: "Porutham",
    th_significance: "Significance",
    th_status: "Status",
    th_points: "Points",
    h_ashta_koota: "North Indian Ashta Koota (36 Gunas)",
    footer_calc: "Calculated with Swiss Ephemeris AGPL",
    footer_private: "Private & Offline Capable · Your charts remain on your machine",
    gem_primary_label: "Primary Life Stone (Lagna Lord):",
    gem_fortune_label: "Fortune Stone (9th Lord):",
    gem_metal_label: "Recommended Metal:",
    gem_finger_label: "Finger to Wear:",
    gem_day_label: "Auspicious Day:",
    luck_numbers_label: "Lucky Numbers:",
    luck_days_label: "Lucky Days:",
    luck_colors_label: "Favorable Colors:",
    luck_deities_label: "Auspicious Deities:",
    h_jaimini: "Maharshi Jaimini’s 7 Chara Karakas & Karakamsha",
    h_double_transit: "K.N. Rao & BVB Double Transit (Dwi-Gochara) Timing Engine",
    ph_profile_search: "Search profiles by name, city, rasi, or star...",
    title_profiles_new: "Enter a new person on the birth chart form",
    title_export_json: "Export all profiles as JSON file",
    title_import_json: "Import profiles from a JSON backup file",
    title_clear_all: "Clear all saved profiles",
    footer_tagline: "Modern Precision Vedic Astrology"
  },
  ta: {
    workspace: 'பணிப் பகுதி',
    birth_chart: 'ஜாதகம் & வர்க்கங்கள்',
    planets_strengths: 'கிரக பலம் & ஆதிபத்தியம்',
    ashtakavarga: 'அஷ்டகவர்க்கம்',
    yogas_doshas: 'யோகங்கள் & தோஷங்கள்',
    vimshottari_dasa: 'விம்சோத்தரி தசை & காலவரிசை பலன்கள்',
    life_readings: 'வாழ்க்கைப் பலன்கள்',
    matching: 'திருமணப் பொருத்தம்',
    daily_panchangam: 'தினசரி பஞ்சாங்கம்',
    saved_profiles: 'சேமித்த ஜாதகங்கள்',
    local_engine: 'சுவிஸ் எபிமெரிஸ் கணிதம்',
    private_data: 'முழுமையான தனிஉரிமை · உள்ளூர் கணிதம்',
    my_location: 'என் இருப்பிடம்',
    print_pdf: 'அச்சு / பிடிஎஃப்',
    birth_details: 'பிறப்பு விவரங்கள்',
    enter_natal: 'பிறந்த நேரம் மற்றும் இருப்பிடம்',
    full_name: 'முழுப் பெயர்',
    birth_date: 'பிறந்த தேதி',
    birth_time: 'பிறந்த நேரம் (24 மணி)',
    birthplace: 'பிறந்த ஊர்',
    latitude: 'அட்சரேகை',
    longitude: 'தீர்க்கரேகை',
    timezone: 'IANA நேர வலயம்',
    ayanamsa: 'அயனாம்சம்',
    dst_clock: 'கடிகார மாற்றம்',
    generate_chart: 'ஜாதகம் கணிக்கவும்',
    ready_to_reveal: 'வான மண்டலம் கணிக்கத் தயார்',
    enter_details_prompt: 'பிறப்பு விவரங்களை உள்ளிட்டு "ஜாதகம் கணிக்கவும்" பொத்தானை அழுத்தவும்.',
    save_profile: 'ஜாதகத்தை சேமி',
    export_pdf: 'பிடிஎஃப் ஆக எடு',
    ascendant: 'லக்னம்',
    moon_sign: 'சந்திர ராசி',
    birth_star: 'பிறந்த நட்சத்திரம்',
    active_dasa: 'இன்றைய தசை இருப்பு',
    south_indian: 'தென்னிந்திய கட்டம்',
    north_diamond: 'வடஇந்திய வைரம்',
    east_indian: 'கிழக்கிந்திய கட்டம்',
    click_house: 'கட்டத்தை சொடுக்கவும்',
    occupant_planets: 'இருக்கும் கிரகங்கள்',
    aspects_received: 'பார்வை தரும் கிரகங்கள்',
    ashtakavarga_sav: 'அஷ்டகவர்க்கப் பரல்கள்',
    house_significations: 'பாவகப் பலன்கள்',
    astronomical_engine: 'கணித எஞ்சின்',
    julian_day: 'ஜூலியன் நாள்',
    ayanamsa_value: 'அயனாம்சம் அளவு',
    graha: 'கிரகம்',
    sign: 'ராசி',
    degrees: 'பாகை / கலை',
    star_pada: 'நட்சத்திரம் / பாதம்',
    house: 'பாவகம்',
    dignity: 'ஆதிபத்திய நிலை',
    motion_status: 'இயக்கம்',
    aspects_cast: 'பார்க்கும் வீடுகள்',
    sav_title: 'சர்வாஷ்டகவர்க்கப் பரல்கள்',
    bav_title: 'பின்னாஷ்டகவர்க்க அட்டவணை',
    detected_yogas: 'அமைந்துள்ள சுப யோகங்கள்',
    current_running_period: 'தற்போதைய தசா-புக்தி-அந்தரம்',
    lagna_path: 'லக்னம் & உடல் அமைப்பு',
    moon_mind: 'சந்திரன் & மன இயல்பு',
    sun_vitality: 'சூரியன் & ஆன்ம பலம்',
    career_karma: 'தொழில் & பத்தாம் பாவம்',
    wealth_gains: 'தனம் & பதினொன்றாம் பாவம்',
    relationships_7th: 'களத்திரம் & ஏழாம் பாவம்',
    active_dasa_focus: 'தசா புக்தி வழிகாட்டல்',
    tithi: 'திதி',
    nakshatra: 'நட்சத்திரம்',
    nitya_yoga: 'நித்திய யோகம்',
    karana: 'கரணம்',
    export_json: 'பேக்கப் ஏற்றுமதி',
    import_json: 'பேக்கப் இறக்குமதி',
    save_person: 'சேமிக்க',
    new_person: 'புதிய நபர்',
    clear_all: 'அனைத்தும் நீக்கு',
    load_saved_profile: 'சேமிக்கப்பட்ட நபர்',
    quick_load_person: '👤 -- நபரைத் தேர்வு செய்க --',
    timeline_predictions_mode: 'காலவரிசை பலன்கள்',
    tabular_cycles_mode: 'அட்டவணை சுழற்சிகள் (3 அடுக்குகள்)',
    live_active_period: 'இன்று இயங்கும் தசா-புக்தி பலன்',
    running_dates: 'காலம் & தேதிகள்',
    current_age: 'தற்போதைய வயது',
    elapsed_time: 'கடந்த நாட்கள்',
    remaining_time: 'மீதமுள்ள நாட்கள்',
    strategic_focus: 'இக்காலத்திற்கான முக்கிய வழிகாட்டல்',
    primary_remedy: 'பரிகாரம் & வழிபட வேண்டிய தெய்வம்',
    filter_active: 'இன்றைய புக்தி',
    filter_next5: 'அடுத்த 5 ஆண்டுகள்',
    filter_annual: 'வருடாந்திர மைல்கற்கள்',
    filter_all: 'முழு வாழ்க்கை (81 காலங்கள்)',
    filter_auspicious: 'சுப காலங்கள் (3+ ★)',
    filter_caution: 'கவனக் காலங்கள்',
    filter_by_lord: 'மகா தசா நாதன்:',
    jump: 'செல்க',
    annual_projections_title: '10 ஆண்டுக்கான வருடாந்திர மைல்கல் பலன்கள்',
    annual_projections_sub: 'ஒவ்வொரு ஆண்டின் வயது, இயங்கும் தசை மற்றும் சாதக சுட்டெண்',
    open_timeline_studio: '81 தசா-புக்தி காலவரிசை ஸ்டுடியோவைக் காண்க →',
    city_helper: 'நகரத் தரவுத்தளத்தில் தேடவும் அல்லது கீழே அட்சரேகை, தீர்க்கரேகையை உள்ளிடவும்.',
    print_jathagam: 'ஜாதகம் அச்சிடு',
    title_print_jathagam: 'பிறப்புக் குறிப்பு, இராசி, அம்சம், கிரக நிலை, தசா புக்தி அடங்கிய ஜாதகத் தாளை அச்சிடவும்',
    bhava_col: 'பாவம் (ஸ்ரீபதி)',
    gowri_title: 'கௌரி பஞ்சாங்கம் (நல்ல நேரம்)',
    gowri_sub: 'அமிர்தம், உத்தி, லாபம், தனம், சுகம் நல்ல நேரங்கள்; ரோகம், சோரம், விஷம் தவிர்க்க வேண்டியவை.',
    saturn_cycles_title: 'வாழ்நாள் சனி சஞ்சார காலங்கள்',
    saturn_cycles_sub: 'உங்கள் சந்திர ராசியிலிருந்து ஏழரை, அர்த்தாஷ்டம, கண்ட, அஷ்டமச் சனி காலங்கள், முதல் நுழைவு முதல் இறுதி வெளியேற்றம் வரை.',
    th_cycle: 'சுழற்சி',
    th_period: 'காலம்',
    th_age: 'வயது',
    th_phases: 'கட்டங்கள்',
    print_porutham: 'பொருத்த அறிக்கை அச்சிடு',
    title_print_porutham: 'திருமணப் பொருத்த அறிக்கையை அச்சிடவும்',
    upagrahas_title: 'உபகிரகங்கள்',
    upagrahas_sub: 'காலன், மிருத்யு, அர்த்தப்பிரகரன், எமகண்டன் தங்கள் அதிபதியின் பகல்/இரவுப் பகுதியின் நடுவிலும், குளிகன் சனியின் பகுதியின் தொடக்கத்திலும் உதிக்கின்றனர்; தூமம் முதலியவை சூரியனிலிருந்து கணிக்கப்படுகின்றன.',
    th_upagraha: 'உபகிரகம்',
    yogini_mode: 'யோகினி தசை',
    yogini_title: 'யோகினி தசை (36 ஆண்டு சுழற்சி)',
    yogini_sub: 'சந்திரன், சூரியன், குரு, செவ்வாய், புதன், சனி, சுக்கிரன், ராகு ஆளும் எட்டு யோகினிகள்; ஜென்ம நட்சத்திரமே முதல் யோகினியைத் தீர்மானிக்கிறது.',
    month_cal_title: 'தமிழ் மாத நாட்காட்டி',
    month_cal_sub: 'சூரிய உதய திதி, நட்சத்திரம் மற்றும் அமாவாசை, பௌர்ணமி, ஏகாதசி, பிரதோஷம், சஷ்டி, சங்கடஹர சதுர்த்தி, மாத சிவராத்திரி, கார்த்திகை.',
    rasi_navamsa: 'இராசி + அம்சம்',
    jathaga_kurippu: 'ஜாதகக் குறிப்பு',
    jathaga_kurippu_sub: 'பஞ்சாங்க முறைப்படி பிறப்புக் குறிப்புகள்',
    chevvai_dosham: 'செவ்வாய் தோஷம்',
    rahu_ketu_dosham: 'ராகு-கேது தோஷம்',
    dosha_samyam: 'தோஷ சாம்யம் (செவ்வாய் & பாப சாம்யம்)',
    dosha: 'தோஷம்',
    bride: 'பெண்',
    groom: 'ஆண்',
    samyam: 'சாம்யம்',
    panch_date: 'தேதி',
    panch_now: 'இப்போது',
    panch_location: 'இடம்',
    panch_location_hint: 'பிறப்பு படிவத்திலிருந்து. மாற்ற 📍 என் இருப்பிடம் பயன்படுத்தவும்.',
    tamil_calendar: 'தமிழ் நாட்காட்டி',
    soolam: 'சூலம்',
    chandrashtamam: 'சந்திராஷ்டமம்',
    personal_balam: 'உங்கள் நாள்: தாரா & சந்திர பலம்',
    tara_balam: 'தாரா பலம்',
    chandra_balam: 'சந்திர பலம்',
    five_limbs: 'பஞ்ச அங்கங்கள்',
    vaaram: 'வாரம் (கிழமை)',
    muhurtha_local: 'முகூர்த்த நேரங்கள் (உள்ளூர் நேரம்)',
    sunrise_sunset: 'சூரிய உதயம் & அஸ்தமனம்',
    abhijit: 'அபிஜித் முகூர்த்தம்',
    abhijit_sub: 'பகலின் மிகச் சிறந்த நேரம்',
    rahu_kalam: 'இராகு காலம்',
    rahu_kalam_sub: 'ராகுவின் அசுப நேரம்',
    yamagandam: 'எமகண்டம்',
    yamagandam_sub: 'எமனின் அசுப நேரம்',
    kuligai: 'குளிகை',
    kuligai_sub: 'மீண்டும் நிகழக் கூடாத காரியங்களைத் தவிர்க்கவும்',
    peyarchi_title: 'வரவிருக்கும் கிரகப் பெயர்ச்சிகள்',
    peyarchi_date: 'தேதி',
    peyarchi_from_to: 'ராசி மாற்றம்',
    house_from_moon: 'சந்திரனிலிருந்து',
    gochara_table_title: 'இன்றைய கோச்சாரம் & அஷ்டகவர்க்கப் பரல்கள்',
    bindus: 'பரல்கள்',
    transit_result: 'பலன்',
    next_chandrashtamam: 'அடுத்த சந்திராஷ்டமம்',
    star_birthday: 'நட்சத்திரப் பிறந்தநாள்',
    hora_title: 'ஓரை நேரங்கள்',
    hora_sub: 'சூரிய உதயம் முதல் 12 பகல், 12 இரவு ஓரைகள்; சந்திரன், புதன், குரு, சுக்கிர ஓரைகள் சுபம்.',
    sacred_geometry: "வானியல் துல்லியம் & வேத மரபு",
    birth_chart_heading: "உங்கள் ஜாதக வரைபடம்",
    birth_chart_sub: "இராசி, நவாம்சம் மற்றும் 14 பராசர வர்க்கங்களில் கிரக அமைப்புகளை ஆராயுங்கள்.",
    planetary_status: "கிரக நிலைகள் & பார்வைகள்",
    planets_sub: "பாகைகள், நட்சத்திரப் பாதங்கள், கிரக நிலைகள், அஸ்தங்கம், வேகம் மற்றும் வேதப் பார்வைகள்.",
    parashara_system: "பராசர அஷ்டகவர்க்க முறை",
    ashtakavarga_sub: "சர்வாஷ்டகவர்க்கம் (மொத்தம் 337 பரல்கள்) மற்றும் 12 ராசிகளிலும் பின்னாஷ்டகவர்க்கப் பரல் பரவல்.",
    karmic_combinations: "யோகங்கள் & தோஷங்கள்",
    yogas_sub: "பஞ்ச மகாபுருஷ, ராஜ, தன, விபரீத யோகங்கள் மற்றும் செவ்வாய், கால சர்ப்ப தோஷ ஆய்வு.",
    planetary_cycles: "120 ஆண்டு விம்சோத்தரி சுழற்சி & வாழ்க்கைக் காலவரிசை",
    dasa_sub: "9 மகா தசைகள், 81 புக்திகள், கிரகங்களின் பரஸ்பர அமைப்பு மற்றும் 10 ஆண்டு வருடாந்திரப் பலன்கள்.",
    astrological_synthesis: "முழுமையான ஜாதகப் பலன் அறிக்கை",
    predictions_sub: "பராசர மற்றும் தமிழ் ஜோதிடப் பலன்கள்: நட்சத்திரம், லக்னம், 12 பாவங்கள், கிரக அமர்வு, தசா-புக்தி, கோச்சாரம் & அதிர்ஷ்டக் கற்கள்.",
    marital_compatibility: "ஜாதகப் பொருத்தம் & 10 பொருத்தங்கள்",
    matching_sub: "தென்னிந்திய 10 பொருத்தங்கள் மற்றும் வடஇந்திய 36 குண மிலனைத் துல்லியமாகக் கணிக்கவும்.",
    celestial_calendar: "நித்திய பஞ்சாங்கம் & நேரங்கள்",
    panchangam_sub: "காலத்தின் ஐந்து அங்கங்கள்: திதி, வாரம், நட்சத்திரம், யோகம், கரணம் மற்றும் முகூர்த்த நேரங்கள்.",
    browser_vault: "உலாவிச் சேமிப்பகம்",
    profiles_sub: "குடும்பத்தினர் மற்றும் வாடிக்கையாளர் ஜாதகங்களை இந்த உலாவியிலேயே நிர்வகிக்கவும். எப்போது வேண்டுமானாலும் பேக்கப் எடுக்கலாம்.",
    brand_sub: "வேத ஜாதகம்",
    engine_status: "சுவிஸ் எபிமெரிஸ் 2.10",
    title_geo: "தற்போதைய GPS இருப்பிடத்தைப் பயன்படுத்து",
    title_lang: "மொழி மாற்று",
    title_theme: "ஒளி/இருள் தோற்றம்",
    title_print: "அச்சிடு அல்லது PDF ஆகச் சேமி",
    title_quick_load: "சேமித்த நபரைத் தேர்ந்தெடுத்து உடனே ஜாதகம் கணிக்கவும்",
    title_save_person: "இந்த நபரின் விவரங்களைச் சேமிக்கவும்",
    title_new_person: "புதிய நபருக்காகப் படிவத்தை அழி",
    ph_name: "இந்த ஜாதகத்தின் பெயர்",
    city_count: "5,481 நகரங்கள்",
    ph_city: "நகரப் பெயரைத் தட்டச்சு செய்க (எ.கா. Chennai, Madurai)...",
    ayan_lahiri: "லாஹிரி (சித்ரா பக்ஷம் - நிலையானது)",
    ayan_raman: "பி.வி. ராமன்",
    ayan_kp: "கே.பி (கிருஷ்ணமூர்த்தி)",
    ayan_fagan: "ஃபேகன்-பிராட்லி (மேற்கத்திய சாயன)",
    fold_auto: "தானியங்கி",
    fold_first: "முதல் நிகழ்வு (நிலையான நேரம்)",
    fold_second: "இரண்டாம் நிகழ்வு (மீண்டும் வந்த நேரம்)",
    pill_vargas: "✦ 14 வர்க்கச் சக்கரங்கள்",
    pill_ashtaka: "✦ பராசர அஷ்டகவர்க்கம்",
    pill_dasa: "✦ 3 அடுக்கு தசை",
    pill_yoga: "✦ யோகக் கணிப்பு",
    pill_porutham: "✦ 10 பொருத்தங்கள்",
    title_save_local: "உலாவியில் சேமிக்கவும்",
    title_export_pdf: "PDF ஆக எடு / அச்சிடு",
    legend_benefic: "சுபர்",
    legend_malefic: "பாவர்",
    legend_combust: "🔥 அஸ்தங்கம்",
    click_house_rest: "அதிபதி, அமர்ந்த கிரகங்கள், பார்வைகள் மற்றும் பாவப் பலன்களைக் காணலாம்.",
    sav_note: "28-க்கு மேல் பரல்கள் உள்ள வீடுகள் பலமும் எளிமையும் தரும்; 28-க்குக் குறைவானவை கவனம் தேவைப்படுபவை.",
    sav_total: "மொத்தம்: 337 பரல்கள்",
    th_planet: "கிரகம்",
    kaal_sarp_title: "கால சர்ப்ப தோஷம்",
    spotlight_calc_note: "சுவிஸ் எபிமெரிஸ் விம்சோத்தரி இருப்பின்படி கணிக்கப்பட்டது",
    tl_all: "🪐 அனைத்து 9 மகா தசைகள்",
    tl_sun: "☀️ சூரியன்",
    tl_moon: "🌙 சந்திரன்",
    tl_mars: "♂️ செவ்வாய்",
    tl_rahu: "☊ ராகு",
    tl_jupiter: "♃ குரு",
    tl_saturn: "♄ சனி",
    tl_mercury: "☿ புதன்",
    tl_ketu: "☋ கேது",
    tl_venus: "♀️ சுக்கிரன்",
    ph_jump_year: "ஆண்டுக்குச் செல் (எ.கா. 2026)",
    title_jump_year: "ஆண்டுக்குச் செல்",
    year_by_year: "ஆண்டுவாரிப் பலன்கள்",
    jump_active_dasa: "நடப்புத் தசைக்குச் செல்",
    pt_natal: "🌟 ஜென்ம இயல்பு",
    pt_bhavas: "🏛️ 12 பாவங்கள்",
    pt_planets: "🪐 பாவங்களில் கிரகங்கள்",
    pt_dasa: "⏳ தசா-புக்தி பலன்கள்",
    pt_transits: "🌌 கோச்சாரம்",
    pt_remedies: "💎 அதிர்ஷ்டக் கற்கள் & பரிகாரம்",
    pt_jaimini: "🪷 ஜைமினி காரகங்கள்",
    pt_timing: "⏱️ இரட்டைக் கோச்சாரம்",
    pt_career: "💼 தசாம்சம்: தொழில்",
    pt_ayur: "🌿 ஆயுர்-ஜோதிட நலம்",
    pt_kakshya: "📐 அஷ்டகவர்க்கக் கக்ஷ்யைகள்",
    pt_shadbala: "⚖️ ஷட்பலம்",
    pt_kp: "🔍 கே.பி உப-அதிபதிகள்",
    pt_bnn: "📜 பிருகு நந்தி நாடி",
    pt_avasthas: "✨ கிரக அவஸ்தைகள்",
    pt_pada: "🎯 நட்சத்திரப் பாத பலன்",
    pt_sahams: "🔮 சகமங்கள்",
    h_bhavas: "12 பாவங்களின் முழுமையான வாழ்க்கைப் பலன்கள்",
    pill_all_houses: "அனைத்து 12 பாவங்கள்",
    p_bhavas: "பாவாதிபதியின் அமர்வு, அமர்ந்த கிரகங்கள், பார்வைகள் மற்றும் சர்வாஷ்டகவர்க்கப் பலத்தின் அடிப்படையில் ஒவ்வொரு பாவத்தின் பலன்.",
    h_planet_positions: "கிரக நிலைகள் & தாக்கம்",
    pill_9_grahas: "9 கிரகங்கள்",
    p_planets: "சூரியன் முதல் கேது வரை ஒன்பது கிரகங்களும் ஜாதகத்தில் அமர்ந்த பாவங்களில் தரும் பலன்கள்.",
    active_dasa_forecast: "நடப்புத் தசா-புக்தி பலன்",
    h_maha_dasas: "9 மகா தசைகளின் வாழ்க்கைச் சுழற்சி",
    pill_120_years: "120 ஆண்டுகள்",
    h_transits: "கிரகக் கோச்சாரம்",
    pill_current_weather: "தற்போதைய கிரக நிலவரம்",
    p_transits: "உங்கள் ஜென்ம ராசியிலிருந்து கணிக்கப்பட்ட கோச்சாரப் பலன்கள்.",
    h_remedies: "அதிர்ஷ்டக் காரணிகள், ரத்தினங்கள் & பரிகாரங்கள்",
    pill_guidance: "ஜோதிட வழிகாட்டல்",
    p_remedies: "உங்கள் லக்னத்திற்கு ஏற்ற ரத்தினங்கள், அதிர்ஷ்ட எண்கள், கிழமைகள், நிறங்கள் மற்றும் வழிபட வேண்டிய தெய்வங்கள்.",
    h_gems: "பரிந்துரைக்கப்படும் ரத்தினங்கள்",
    sub_gems: "ஜீவ ரத்தினம் & பாக்ய ரத்தினம்",
    h_lucky: "அதிர்ஷ்ட எண்கள், கிழமைகள் & நிறங்கள்",
    sub_lucky: "சாதகமான கிரக அமைப்புகள்",
    pill_upadesha: "உபதேச சூத்திரங்கள்",
    p_jaimini: "பாகை அடிப்படையிலான சர காரகங்கள்: ஆன்ம வளர்ச்சி (ஆத்மகாரகன்), தொழில் (அமாத்யகாரகன்), குரு, தாய், சந்ததி, சவால்கள் மற்றும் வாழ்க்கைத் துணை (தாரகாரகன்).",
    soul_purpose: "ஆன்மாவின் உயர் நோக்கம் (நவாம்சத்தில் காரகாம்சம்)",
    p_double_transit: "சனியும் (ஒழுக்கம் & கர்மா) குருவும் (அருள் & வளர்ச்சி) ஒரே நேரத்தில் குறிப்பிட்ட ஜாதக பாவங்களைப் பார்க்கும் போதே முக்கிய நிகழ்வுகள் நடைபெறும்.",
    transit_saturn_today: "இன்றைய சனி கோச்சாரம்",
    transit_jupiter_today: "இன்றைய குரு கோச்சாரம்",
    h_career: "தசாம்சம் (D-10) & தொழில் திறன் ஆய்வு",
    pill_bvb: "பாரதிய வித்யா பவன் முறை",
    p_career: "இராசி (D-1), தசாம்சம் (D-10) மற்றும் அமாத்யகாரகன் அடிப்படையில் 5 தொழில் வகைகளுக்கான திறன் மதிப்பீடு.",
    h_ayur: "ஆயுர்-ஜோதிடம் & திரிதோஷ நல ஆய்வு",
    pill_charaka: "சரகர் & பிரசன்ன மார்க்கம்",
    p_ayur: "வாதம், பித்தம், கபம் சமநிலை, செரிமானப் போக்கு மற்றும் உறுப்புகளின் வலிமையை மதிப்பிடும் ஆயுர்வேத உடலமைப்பு ஆய்வு.",
    prakriti: "பிறவிப் பிரகிருதி",
    vata_label: "வாதம் (காற்று/ஆகாயம்)",
    pitta_label: "பித்தம் (நெருப்பு)",
    kapha_label: "கபம் (நீர்/நிலம்)",
    h_vulnerabilities: "உடல் பலவீனங்கள்",
    sub_6th: "6-ம் பாவம் (ரோக பாவம்) & 6-ம் அதிபதி",
    h_lifestyle: "ஆயுர்வேத நோய்த்தடுப்பு வாழ்க்கை முறை",
    sub_lifestyle: "உணவு & யோகப் பரிந்துரைகள்",
    h_kakshya: "அஷ்டகவர்க்கக் கக்ஷ்யா நுண் கோச்சார முறை",
    pill_raman_patel: "டாக்டர் பி.வி. ராமன் & சி.எஸ். படேல்",
    p_kakshya: "ஒவ்வொரு ராசியும் 8 கக்ஷ்யைகளாக (தலா 3°45′) பிரிக்கப்படுகிறது. கோச்சார கிரகம் தன் அஷ்டகவர்க்கத்தில் பரல் அளித்த கக்ஷ்யையில் செல்லும் போதே பலன் தரும்.",
    h_sat_kakshya: "சனி கோச்சாரக் கக்ஷ்யைகள்",
    h_jup_kakshya: "குரு கோச்சாரக் கக்ஷ்யைகள்",
    th_degree_range: "பாகை வரம்பு",
    th_lord: "அதிபதி",
    th_bav_bindu: "அஷ்டகவர்க்கப் பரல்",
    th_result: "பலன்",
    h_shadbala: "ஷட்பலம்: அறுவகைக் கிரக பலம்",
    pill_shadbala: "பாரம்பரிய வேதக் கணித பலம்",
    dominant_planet: "ஆதிக்க கிரகம் (ஆத்ம பலம்)",
    karmic_vulnerability: "கர்ம பலவீனம் (வளர்ச்சிக் கவனம்)",
    h_kp: "கிருஷ்ணமூர்த்தி பத்ததி (கே.பி) உப-அதிபதி ஆய்வு",
    pill_kp: "பேரா. கே.எஸ். கிருஷ்ணமூர்த்தி 249 பிரிவுகள்",
    p_kp: "கே.பி முறை ஒவ்வொரு நட்சத்திரத்தையும் விம்சோத்தரி விகிதப்படி 9 சமமற்ற உப பிரிவுகளாகப் பிரித்து பலன்களைத் துல்லியமாகக் கணிக்கிறது.",
    h_kp_cuspal: "முக்கிய பாவ ஆரம்ப உப-அதிபதி பலன்கள்",
    h_kp_cusps: "12 கே.பி பிளாசிடஸ் பாவ ஆரம்பங்கள்",
    th_cusp: "பாவம்",
    th_degree: "பாகை",
    th_sign: "ராசி",
    th_sign_lord: "ராசி அதிபதி",
    th_star_lord: "நட்சத்திர அதிபதி",
    th_sub_lord: "உப-அதிபதி",
    h_kp_planets: "9 கிரகங்களின் கே.பி நிலைகள்",
    h_bnn: "பிருகு நந்தி நாடி கர்ம சூத்திரங்கள்",
    pill_bnn: "பிருகு முனிவர் மரபு",
    h_bnn_combos: "நாடி கர்ம சேர்க்கைகள் & வாழ்க்கைப் பாடங்கள்",
    h_avasthas: "கிரக அவஸ்தைகள் & விழிப்பு நிலைகள்",
    pill_avasthas: "பாலாதி & ஜாக்ரதாதி அவஸ்தைகள்",
    p_avasthas: "கிரகங்கள் தங்கள் வயது நிலை (பால, குமார, யுவ, விருத்த, மிருத) மற்றும் விழிப்பு நிலைக்கு (ஜாக்ரத், ஸ்வப்ன, சுஷுப்தி) ஏற்ப பலன் தருகின்றன; வாக்களிக்கப்பட்ட பலனில் எத்தனை சதவீதம் நடைமுறையில் கிடைக்கும் என்பதைக் காட்டுகிறது.",
    h_pada: "நட்சத்திரப் பாத விதிப் பலன்",
    birth_star_pada: "ஜென்ம நட்சத்திரம் & பாதம்",
    navamsa_sign_lord: "நவாம்ச ராசி & அதிபதி",
    h_sahams: "சகமங்கள் (தாஜிக உணர்வுப் புள்ளிகள்)",
    p_sahams: "லக்னம், சூரியன், சந்திரன் மற்றும் கிரக இடைவெளிகளிலிருந்து கணிக்கப்படும் புள்ளிகள்: அதிர்ஷ்டம், ஞானம், திருமணம், தொழில், உடல் வலிமை.",
    h_match_candidates: "பொருத்தம் பார்க்க வேண்டியவர்கள்",
    h_bride: "மணமகள் (நட்சத்திரம் & ராசி)",
    h_groom: "மணமகன் (நட்சத்திரம் & ராசி)",
    label_saved_profile: "சேமித்த ஜாதகம் (விருப்பத்தேர்வு)",
    label_nakshatra: "நட்சத்திரம்",
    label_rasi: "ராசி",
    btn_calc_match: "பொருத்தம் கணிக்கவும்",
    of_36_gunas: "/ 36 குணங்கள்",
    final_verdict: "இறுதி முடிவு",
    h_10_poruthams: "தென்னிந்திய 10 பொருத்தங்கள்",
    th_porutham: "பொருத்தம்",
    th_significance: "பலன்",
    th_status: "நிலை",
    th_points: "மதிப்பெண்",
    h_ashta_koota: "வடஇந்திய அஷ்ட கூடம் (36 குணங்கள்)",
    footer_calc: "சுவிஸ் எபிமெரிஸ் AGPL மூலம் கணிக்கப்பட்டது",
    footer_private: "தனிப்பட்டது & இணையமின்றி இயங்கும் · உங்கள் ஜாதகங்கள் உங்கள் கணினியிலேயே இருக்கும்",
    gem_primary_label: "ஜீவ ரத்தினம் (லக்னாதிபதி):",
    gem_fortune_label: "பாக்ய ரத்தினம் (9-ம் அதிபதி):",
    gem_metal_label: "உலோகம்:",
    gem_finger_label: "அணிய வேண்டிய விரல்:",
    gem_day_label: "அணிய உகந்த கிழமை:",
    luck_numbers_label: "அதிர்ஷ்ட எண்கள்:",
    luck_days_label: "அதிர்ஷ்டக் கிழமைகள்:",
    luck_colors_label: "உகந்த நிறங்கள்:",
    luck_deities_label: "வழிபட வேண்டிய தெய்வங்கள்:",
    h_jaimini: "மகரிஷி ஜைமினியின் 7 சர காரகங்கள் & காரகாம்சம்",
    h_double_transit: "கே.என். ராவ் & பாரதிய வித்யா பவன் இரட்டைக் கோச்சாரக் கணிப்பு",
    ph_profile_search: "பெயர், ஊர், ராசி அல்லது நட்சத்திரம் மூலம் தேடுக...",
    title_profiles_new: "புதிய நபரின் விவரங்களை உள்ளிடவும்",
    title_export_json: "அனைத்து ஜாதகங்களையும் JSON கோப்பாக ஏற்றுமதி செய்",
    title_import_json: "JSON பேக்கப் கோப்பிலிருந்து இறக்குமதி செய்",
    title_clear_all: "அனைத்து ஜாதகங்களையும் நீக்கு",
    footer_tagline: "நவீன துல்லிய வேத ஜோதிடம்"
  }
};

// Toast notification
function notify(msg) {
  const toast = $('#toast');
  toast.textContent = msg;
  toast.hidden = false;
  setTimeout(() => { toast.hidden = true; }, 3800);
}

// Degrees to D° M′ S″
function formatDegrees(val) {
  const totalSec = Math.round(val * 3600);
  const deg = Math.floor(totalSec / 3600);
  const min = Math.floor((totalSec % 3600) / 60);
  const sec = totalSec % 60;
  return `${deg}° ${String(min).padStart(2, '0')}′ ${String(sec).padStart(2, '0')}″`;
}

// Page Navigation
function navigatePage(pageName) {
  $$('.app-page').forEach(p => p.hidden = p.id !== `page-${pageName}`);
  $$('.nav-item').forEach(b => b.classList.toggle('active', b.dataset.page === pageName));
  const activeBtn = $(`#nav-${pageName}`);
  if (activeBtn) {
    $('#current-page-badge').textContent = activeBtn.querySelector('.nav-text').textContent;
  }
  // If opening matching or panchangam or profiles, trigger their renders
  if (pageName === 'profiles') renderProfilesList();
  if (pageName === 'matching') populateMatchDropdowns();
  if (pageName === 'panchangam') {
    loadDailyPanchangam();
    loadMonthCalendar();
  }

  // Close mobile sidebar if open
  $('.sidebar').classList.remove('open');
}

// Setup Event Listeners
document.addEventListener('DOMContentLoaded', () => {
  // Navigation clicks
  $$('.nav-item').forEach(btn => {
    btn.addEventListener('click', () => navigatePage(btn.dataset.page));
  });

  // Mobile menu toggle
  $('#mobile-menu-toggle').addEventListener('click', () => {
    $('.sidebar').classList.toggle('open');
  });

  // Theme toggle
  $('#theme-btn').addEventListener('click', toggleTheme);

  // Language toggle
  $('#lang-btn').addEventListener('click', toggleLanguage);

  // Geolocation button
  $('#geo-btn').addEventListener('click', detectCurrentLocation);

  // Print buttons
  $('#print-btn').addEventListener('click', () => window.print());
  $('#quick-print-btn').addEventListener('click', () => window.print());
  $('#print-jathagam-btn').addEventListener('click', printJathagam);
  $('#print-porutham-btn').addEventListener('click', printPorutham);
  window.addEventListener('afterprint', () => document.body.classList.remove('printing-jathagam'));

  // Save profile button (results banner & form)
  $('#save-profile-btn')?.addEventListener('click', saveCurrentProfile);
  $('#form-save-profile-btn')?.addEventListener('click', saveCurrentProfile);
  $('#form-new-profile-btn')?.addEventListener('click', clearFormForNewPerson);
  $('#quick-profile-select')?.addEventListener('change', handleQuickProfileChange);

  // Close inspector button
  $('#close-inspector-btn').addEventListener('click', () => {
    $('#house-inspector-card').hidden = true;
  });

  // Chart style toggles
  $('#btn-south-style').addEventListener('click', () => setChartStyle('south'));
  $('#btn-north-style').addEventListener('click', () => setChartStyle('north'));
  $('#btn-east-style').addEventListener('click', () => setChartStyle('east'));
  $('#btn-dual-style').addEventListener('click', () => setChartStyle('dual'));

  // Varga selector pills
  $$('.varga-pill').forEach(btn => {
    btn.addEventListener('click', () => setVarga(btn.dataset.varga));
  });

  // Jump to active dasa
  $('#jump-active-dasa').addEventListener('click', () => {
    const activeEl = $('.dasa-summary.active-period');
    if (activeEl) {
      activeEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
      const details = activeEl.closest('details');
      if (details) details.open = true;
    }
  });

  // Timeline View Mode Switcher (Timeline Predictions vs Tabular Date Cycles)
  $('#btn-mode-timeline')?.addEventListener('click', () => setDasaViewMode('timeline'));
  $('#btn-mode-cycles')?.addEventListener('click', () => setDasaViewMode('cycles'));
  $('#btn-mode-yogini')?.addEventListener('click', () => setDasaViewMode('yogini'));

  // Timeline Filter Buttons
  $$('.timeline-filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      $$('.timeline-filter-btn').forEach(b => b.classList.toggle('active', b === btn));
      currentTimelineFilter = btn.dataset.tfilter;
      renderDasaTimelineView();
    });
  });

  // Timeline Planet Selector
  $('#timeline-planet-select')?.addEventListener('change', e => {
    currentTimelinePlanet = e.target.value;
    renderDasaTimelineView();
  });

  // Timeline Year Jump
  $('#timeline-jump-btn')?.addEventListener('click', handleTimelineYearJump);
  $('#timeline-jump-year')?.addEventListener('keydown', e => {
    if (e.key === 'Enter') handleTimelineYearJump();
  });

  // Jump to Timeline Studio from Predictions tab
  $('#btn-jump-to-timeline')?.addEventListener('click', () => {
    navigatePage('dasha');
    setDasaViewMode('timeline');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  // Prediction Chapters Tab Switcher
  $$('.pred-tab').forEach(btn => {
    btn.addEventListener('click', () => switchPredictionTab(btn.dataset.ptab));
  });

  // Birth Form Submit
  $('#birth-form').addEventListener('submit', handleFormSubmit);

  // City Search
  setupCityAutocomplete();

  // Profiles toolbar buttons
  $('#export-profiles-btn')?.addEventListener('click', exportProfilesJSON);
  $('#import-profiles-input')?.addEventListener('change', importProfilesJSON);
  $('#profile-search')?.addEventListener('input', renderProfilesList);
  $('#profiles-add-new-btn')?.addEventListener('click', () => {
    navigatePage('chart');
    clearFormForNewPerson();
  });
  $('#profiles-clear-all-btn')?.addEventListener('click', clearAllProfiles);

  // Match Button
  $('#run-match-btn').addEventListener('click', runHoroscopeMatch);

  // Daily Panchangam: a picked date shows that day at sunrise; "Now" shows this moment
  $('#panch-date')?.addEventListener('change', loadDailyPanchangam);
  $('#month-prev-btn')?.addEventListener('click', () => shiftCalendarMonth(-1));
  $('#month-next-btn')?.addEventListener('click', () => shiftCalendarMonth(1));
  $('#panch-today-btn')?.addEventListener('click', () => {
    $('#panch-date').value = '';
    loadDailyPanchangam();
  });

  // Initialize theme from persistence or system preference
  let initialTheme = 'dark';
  try {
    const saved = localStorage.getItem('joroscope_theme');
    if (saved === 'light' || saved === 'dark') {
      initialTheme = saved;
    } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) {
      initialTheme = 'light';
    }
  } catch (e) {}
  applyTheme(initialTheme);

  // Restore the language choice before anything renders
  try {
    if (localStorage.getItem('joroscope_lang') === 'ta') currentLang = 'ta';
  } catch (e) {}
  $('#lang-label').textContent = currentLang === 'en' ? 'தமிழ்' : 'English';
  applyLanguage();

  // Load cities
  loadInitialData();
});

// Theme Management
function toggleTheme() {
  const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
  applyTheme(nextTheme);
}

function applyTheme(theme) {
  currentTheme = theme;
  document.documentElement.setAttribute('data-theme', theme);
  try {
    localStorage.setItem('joroscope_theme', theme);
  } catch (e) {}

  const themeIcon = $('#theme-icon');
  const themeText = $('#theme-text');
  if (themeIcon) themeIcon.textContent = theme === 'dark' ? '🌙' : '☀️';
  if (themeText) {
    themeText.textContent = currentLang === 'ta'
      ? (theme === 'dark' ? 'இருள்' : 'ஒளி')
      : (theme === 'dark' ? 'Dark' : 'Light');
  }

  // Reactive re-render of SVG chart & timeline
  if (currentChart) {
    renderCurrentChart();
    renderDasaTimelineView();
  }
}

// Prediction Chapter Switcher
function switchPredictionTab(ptab) {
  $$('.pred-tab').forEach(b => b.classList.toggle('active', b.dataset.ptab === ptab));
  $$('.pred-panel').forEach(p => p.hidden = p.id !== `ppanel-${ptab}`);
}

// Language Management
function toggleLanguage() {
  currentLang = currentLang === 'en' ? 'ta' : 'en';
  try {
    localStorage.setItem('joroscope_lang', currentLang);
  } catch (e) {}
  $('#lang-label').textContent = currentLang === 'en' ? 'தமிழ்' : 'English';
  applyLanguage();
  if (currentChart) {
    renderCurrentChart();
    renderPlanetsTable();
    renderQuickStats();
    renderAshtakavarga();
    renderYogasAndDoshas();
    renderDashaAccordion();
    renderYoginiAccordion();
    renderUpagrahas();
    renderJathagaKurippu();
    renderLifeReadings();
    renderDasaTimelineView();
  }
  if (lastDailyPanchangam) populatePanchangamView(lastDailyPanchangam);
  if (lastCalendar) renderMonthCalendar(lastCalendar);
  if (lastMatch) renderMatchResult(lastMatch);
  populateQuickProfileDropdown();
  renderProfilesList();
  populateMatchDropdowns();
}

function applyLanguage() {
  const dict = I18N[currentLang];
  document.documentElement.lang = currentLang;
  $$('[data-i18n]').forEach(el => {
    const key = el.dataset.i18n;
    if (dict[key]) el.textContent = dict[key];
  });
  $$('[data-i18n-placeholder]').forEach(el => {
    const text = dict[el.dataset.i18nPlaceholder];
    if (text) el.placeholder = text;
  });
  $$('[data-i18n-title]').forEach(el => {
    const text = dict[el.dataset.i18nTitle];
    if (text) el.title = text;
  });
  $$('.varga-pill').forEach(btn => {
    const [en, ta] = VARGA_NAMES[btn.dataset.varga];
    btn.textContent = btn.dataset.varga === 'Bhava' ? txt(en, ta) : `${btn.dataset.varga} ${txt(en, ta)}`;
  });
  const activeNav = $('.nav-item.active .nav-text');
  if (activeNav) $('#current-page-badge').textContent = activeNav.textContent;
  const themeText = $('#theme-text');
  if (themeText) {
    themeText.textContent = currentLang === 'ta'
      ? (currentTheme === 'dark' ? 'இருள்' : 'ஒளி')
      : (currentTheme === 'dark' ? 'Dark' : 'Light');
  }
}

// Geolocation
function detectCurrentLocation() {
  if (!navigator.geolocation) {
    notify(txt('Geolocation is not supported by your browser.', 'உங்கள் உலாவி இருப்பிட வசதியை ஆதரிக்கவில்லை.'));
    return;
  }
  notify(txt('Querying coordinates...', 'இருப்பிடம் கண்டறியப்படுகிறது...'));
  navigator.geolocation.getCurrentPosition(
    pos => {
      const lat = pos.coords.latitude.toFixed(4);
      const lon = pos.coords.longitude.toFixed(4);
      $('#input-lat').value = lat;
      $('#input-lon').value = lon;
      $('#city-search').value = txt(`Current Location (${lat}, ${lon})`, `தற்போதைய இருப்பிடம் (${lat}, ${lon})`);
      // Try to auto-guess timezone
      try {
        const guessedTz = Intl.DateTimeFormat().resolvedOptions().timeZone;
        if (guessedTz) $('#input-timezone').value = guessedTz;
      } catch (e) {}
      notify(txt(`Coordinates updated: ${lat}, ${lon}`, `இருப்பிடம் புதுப்பிக்கப்பட்டது: ${lat}, ${lon}`));
    },
    err => {
      notify(txt('Could not retrieve location. Please enter coordinates manually.', 'இருப்பிடத்தைப் பெற முடியவில்லை. அட்சரேகை, தீர்க்கரேகையை உள்ளிடவும்.'));
    },
    { timeout: 8000 }
  );
}

// Single-timezone countries named in the city database's "(country)" suffixes
const COUNTRY_ZONES = {
  'sl': 'Asia/Colombo', 'sri lanka': 'Asia/Colombo', 'ceylon': 'Asia/Colombo', 'colombo': 'Asia/Colombo',
  'singapore': 'Asia/Singapore', 'malaysia': 'Asia/Kuala_Lumpur', 'uae': 'Asia/Dubai', 'dubai': 'Asia/Dubai',
  'saudi arab': 'Asia/Riyadh', 'saudia': 'Asia/Riyadh', 'saudi arabia': 'Asia/Riyadh', 'iraq': 'Asia/Baghdad',
  'iran': 'Asia/Tehran', 'yemen': 'Asia/Aden', 'jordan': 'Asia/Amman', 'syria': 'Asia/Damascus',
  'turkey': 'Europe/Istanbul', 'egypt': 'Africa/Cairo', 'nigeria': 'Africa/Lagos', 'ghana': 'Africa/Accra',
  'uganda': 'Africa/Kampala', 'burma': 'Asia/Yangon', 'china': 'Asia/Shanghai', 'japan': 'Asia/Tokyo',
  'mangolia': 'Asia/Ulaanbaatar', 'nepal': 'Asia/Kathmandu', 'pakistan': 'Asia/Karachi',
  'bangladesh': 'Asia/Dhaka', 'afghanistan': 'Asia/Kabul', 'thailand': 'Asia/Bangkok',
  'germany': 'Europe/Berlin', 'italy': 'Europe/Rome', 'france': 'Europe/Paris', 'switzerland': 'Europe/Zurich',
  'poland': 'Europe/Warsaw', 'sweden': 'Europe/Stockholm', 'finland': 'Europe/Helsinki',
  'holland': 'Europe/Amsterdam', 'ireland': 'Europe/Dublin', 'uk': 'Europe/London', 'england': 'Europe/London',
  'london': 'Europe/London', 'scotland': 'Europe/London', 'hawai': 'Pacific/Honolulu', 'alaska': 'America/Anchorage',
  'new york': 'America/New_York'
};
// A representative zone for each standard offset in the database, used when nothing better is known
const OFFSET_ZONES = {
  '00.00W': 'Europe/London', '01.00E': 'Europe/Paris', '02.00E': 'Africa/Cairo', '03.00E': 'Asia/Riyadh',
  '03.30E': 'Asia/Tehran', '04.00E': 'Asia/Dubai', '04.30E': 'Asia/Kabul', '05.00E': 'Asia/Karachi',
  '05.30E': 'Asia/Kolkata', '06.00E': 'Asia/Dhaka', '06.30E': 'Asia/Yangon', '07.00E': 'Asia/Bangkok',
  '08.00E': 'Asia/Shanghai', '09.00E': 'Asia/Tokyo', '10.00E': 'Australia/Sydney', '12.00E': 'Pacific/Auckland',
  '03.00W': 'America/Sao_Paulo', '04.00W': 'America/Halifax', '05.00W': 'America/New_York',
  '06.00W': 'America/Chicago', '08.00W': 'America/Los_Angeles', '09.00W': 'America/Anchorage',
  '10.00W': 'Pacific/Honolulu'
};

function guessTimezone(city) {
  const name = city.name.toLowerCase();
  const suffix = (name.match(/\(([^)]*)\)?\s*$/) || [])[1]?.trim();
  if (suffix && COUNTRY_ZONES[suffix]) return { zone: COUNTRY_ZONES[suffix], confident: true };
  const named = Object.keys(COUNTRY_ZONES).find(k => k.length > 3 && name.includes(k));
  if (named) return { zone: COUNTRY_ZONES[named], confident: true };
  const inIndia = city.longitude > 68 && city.longitude < 97 && city.latitude > 8 && city.latitude < 37;
  if (name.includes('india') || (inIndia && city.legacy_offset !== '06.00E')) return { zone: 'Asia/Kolkata', confident: true };
  return { zone: OFFSET_ZONES[city.legacy_offset] || null, confident: false };
}

// City Search Autocomplete
function setupCityAutocomplete() {
  const cityInput = $('#city-search');
  const dropdown = $('#city-dropdown');

  cityInput.addEventListener('input', () => {
    const q = cityInput.value.toLowerCase().trim();
    dropdown.replaceChildren();
    if (q.length < 2) {
      dropdown.hidden = true;
      return;
    }
    const matches = citiesList.filter(c => c.name.toLowerCase().includes(q)).slice(0, 15);
    if (!matches.length) {
      dropdown.hidden = true;
      return;
    }
    matches.forEach(c => {
      const b = document.createElement('button');
      b.type = 'button';
      b.textContent = `${c.name} (${c.latitude.toFixed(2)}°, ${c.longitude.toFixed(2)}°)`;
      b.onclick = () => {
        cityInput.value = c.name;
        $('#input-lat').value = c.latitude;
        $('#input-lon').value = c.longitude;
        dropdown.hidden = true;

        const guess = guessTimezone(c);
        if (guess.zone) $('#input-timezone').value = guess.zone;
        $('#city-helper').textContent = guess.confident ? I18N[currentLang].city_helper : (currentLang === 'ta'
          ? `நேர வலயம் நகரின் நிலையான நேர வேறுபாட்டிலிருந்து (${c.legacy_offset}) ஊகிக்கப்பட்டது; பிறந்த இடத்தின் சரியான IANA வலயத்தை உறுதிசெய்யவும்.`
          : `Timezone guessed from the city's standard offset (${c.legacy_offset}); confirm the birthplace's IANA zone.`);
        $('#city-helper').classList.toggle('field-warning', !guess.confident);
        notify(txt(`Selected ${c.name}`, `${c.name} தேர்ந்தெடுக்கப்பட்டது`));
      };
      dropdown.append(b);
    });
    dropdown.hidden = false;
  });

  document.addEventListener('click', e => {
    if (!dropdown.contains(e.target) && e.target !== cityInput) {
      dropdown.hidden = true;
    }
  });
}

// Load initial static JSON files
async function loadInitialData() {
  try {
    const rCities = await fetch('cities.json');
    if (rCities.ok) citiesList = await rCities.json();
  } catch (e) {
    console.warn('Could not load cities.json', e);
  }

  // Initialize multi-person profiles and quick loader
  populateQuickProfileDropdown();
  renderProfilesList();

  // Pre-load default chart
  $('#birth-form').requestSubmit();
}

// Form Submission Handler
async function handleFormSubmit(e) {
  e.preventDefault();
  const errorEl = $('#form-error');
  const btn = $('#calculate-btn');
  errorEl.hidden = true;
  errorEl.textContent = '';
  btn.disabled = true;

  try {
    const formData = new FormData(e.target);
    const payload = Object.fromEntries(formData);
    const resp = await fetch('/api/chart', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const result = await resp.json();
    if (!resp.ok) throw new Error(result.error || 'Calculation failed.');

    currentChart = result;
    $('#chart-empty').hidden = true;
    $('#chart-results').hidden = false;

    // Render all result views
    renderQuickStats();
    renderCurrentChart();
    renderPlanetsTable();
    renderUpagrahas();
    renderAshtakavarga();
    renderYogasAndDoshas();
    renderDashaAccordion();
    renderYoginiAccordion();
    renderDasaTimelineView();
    renderLifeReadings();
    renderJathagaKurippu();
    if (!$('#page-panchangam').hidden) loadDailyPanchangam();

    // Sync calculated astrological attributes with saved profiles if already stored
    syncCalculatedProfileWithStorage(result);

    notify(txt(`Chart generated for ${result.profile.name}`, `${result.profile.name} ஜாதகம் கணிக்கப்பட்டது`));
  } catch (err) {
    errorEl.textContent = errorText(err.message);
    errorEl.hidden = false;
  } finally {
    btn.disabled = false;
  }
}

// Quick Stats Rendering
function renderQuickStats() {
  if (!currentChart) return;
  const p = currentChart.planets;
  const prof = currentChart.profile;

  $('#res-name').textContent = prof.name || txt('Unnamed Chart', 'பெயரிடப்படாத ஜாதகம்');
  $('#res-details').textContent = `${prof.date} · ${prof.time} · ${prof.city} · ${prof.timezone} · ${ayanamsaLabel(prof.ayanamsa)} ${txt('Ayanamsa', 'அயனாம்சம்')}`;

  const ascSignIdx = p.Ascendant.sign_index;
  $('#res-zodiac-icon').textContent = ZODIAC_SYMBOLS[ascSignIdx];

  $('#stat-lagna').textContent = currentLang === 'ta' ? p.Ascendant.tamil : p.Ascendant.sign;
  $('#stat-lagna-tamil').textContent = currentLang === 'ta' ? p.Ascendant.sign : p.Ascendant.tamil;

  $('#stat-moon').textContent = currentLang === 'ta' ? p.Moon.tamil : p.Moon.sign;
  $('#stat-moon-tamil').textContent = currentLang === 'ta' ? p.Moon.sign : p.Moon.tamil;

  $('#stat-star').textContent = currentLang === 'ta' ? p.Moon.tamil_nakshatra : p.Moon.nakshatra;
  $('#stat-star-pada').textContent = txt(
    `Pada ${p.Moon.pada} · Ruler: ${p.Moon.nakshatra_lord}`,
    `பாதம் ${p.Moon.pada} · அதிபதி: ${grahaName(p.Moon.nakshatra_lord)}`);

  if (currentChart.active_dasha) {
    const ad = currentChart.active_dasha;
    $('#stat-dasa').textContent = `${grahaName(ad.dasa)} · ${grahaName(ad.bhukti)}`;
    $('#stat-dasa-sub').textContent = txt(`Pratyantar: ${ad.pratyantar}`, `அந்தரம்: ${grahaName(ad.pratyantar)}`);
    $('#hero-dasa-names').textContent = txt(
      `${ad.dasa} Maha Dasa → ${ad.bhukti} Bhukti → ${ad.pratyantar} Pratyantar`,
      `${grahaName(ad.dasa)} மகா தசை → ${grahaName(ad.bhukti)} புக்தி → ${grahaName(ad.pratyantar)} அந்தரம்`);
    $('#hero-dasa-dates').textContent = txt(
      `Active through ${localDate(ad.end)} (Maha Dasa ends ${localDate(ad.dasa_end)})`,
      `${localDate(ad.end)} வரை நடைமுறையில் (மகா தசை ${localDate(ad.dasa_end)} அன்று முடிகிறது)`);
  } else {
    $('#stat-dasa').textContent = '—';
  }

  const m = currentChart.method;
  $('#calc-engine-desc').textContent = txt(
    `${m.engine} (${m.ephemeris}). Houses: ${m.houses}. Nodes: ${m.nodes}.`,
    `${m.engine} (மோஷியர் பகுப்பாய்வு எபிமெரிஸ்). பாவங்கள்: முழு ராசி முறை. ராகு-கேது: சராசரி கணு.`);
  $('#calc-jd').textContent = currentChart.julian_day.toFixed(6);
  $('#calc-ayanamsa-val').textContent = formatDegrees(currentChart.ayanamsa_degrees);
}

// Calendar date (YYYY-MM-DD) of a UTC timestamp at the chart's birthplace
const localDate = iso => new Date(iso).toLocaleDateString('en-CA', { timeZone: currentChart?.profile?.timezone || undefined });

// "HH:MM" from an ISO timestamp that carries its own UTC offset
const clockTime = iso => (iso || '').slice(11, 16);

function tithiLabel(name) {
  return currentLang === 'ta' ? (TITHI_TA[name] || name) : name;
}

function pakshaLabel(paksha) {
  if (currentLang !== 'ta') return paksha;
  return paksha.startsWith('Shukla') ? 'வளர்பிறை' : 'தேய்பிறை';
}

// Tamil Jathaga Kurippu: the birth notes block of a Tamil horoscope
function renderJathagaKurippu() {
  const si = currentChart?.south_indian;
  const grid = $('#kurippu-grid');
  if (!grid) return;
  $('#jathaga-kurippu-card').hidden = !si;
  if (!si) return;

  grid.innerHTML = kurippuRows().map(([label, value]) => `
    <div class="kurippu-item">
      <small>${esc(label)}</small>
      <strong>${esc(value)}</strong>
    </div>
  `).join('');
}

// [label, value] rows of the Tamil birth notes, shared by the card and the printed Jathagam
function kurippuRows() {
  const si = currentChart.south_indian;
  const isTa = currentLang === 'ta';
  const p = currentChart.planets;
  const panch = currentChart.panchanga;
  const tc = si.tamil_calendar;
  const nz = si.nazhigai;
  const star = si.birth_star;
  const mandi = si.mandi;
  const pick = (en, ta) => isTa ? ta : en;
  const starIdx = STARS_EN.indexOf(p.Moon.nakshatra);

  const rows = [
    [pick('Tamil Year', 'வருடம்'), pick(`${tc.year} (${tc.year_ta})`, `${tc.year_ta} வருடம்`)],
    [pick('Tamil Month & Date', 'மாதம் & தேதி'), pick(`${tc.month} ${tc.day} (${tc.month_ta})`, `${tc.month_ta} ${tc.day}`)],
    [pick('Vaaram (Vedic day)', 'கிழமை'), pick(`${si.vaaram.en} (${si.vaaram.ta})`, si.vaaram.ta)],
    [pick('Sunrise', 'சூரிய உதயம்'), clockTime(si.sunrise_local)],
    [pick('Udayadi Nazhigai', 'உதயாதி நாழிகை'), pick(`${nz.nazhigai} nazhigai ${nz.vinadi} vinadi`, `${nz.nazhigai} நாழிகை ${nz.vinadi} விநாடி`)],
    [pick('Dinamanam (day length)', 'தினமானம்'), pick(`${nz.dinamanam} nazhigai`, `${nz.dinamanam} நாழிகை`)],
    [pick('Tithi', 'திதி'), `${tithiLabel(panch.tithi_name)} · ${pakshaLabel(panch.paksha)}`],
    [pick('Nakshatra & Pada', 'நட்சத்திரம் & பாதம்'), `${isTa ? STARS_TA[starIdx] : p.Moon.nakshatra} · ${pick('Pada', 'பாதம்')} ${p.Moon.pada}`],
    [pick('Nitya Yoga · Karana', 'யோகம் · கரணம்'), `${nityaYogaLabel(panch.yoga_name)} · ${karanaLabel(panch.karana_name)}`],
    [pick('Lagna', 'லக்னம்'), pick(p.Ascendant.sign, p.Ascendant.tamil)],
    [pick('Rasi', 'ராசி'), pick(p.Moon.sign, p.Moon.tamil)],
    [pick('Gana · Yoni', 'கணம் · யோனி'), pick(`${star.gana} · ${star.yoni}`, `${star.gana_ta} · ${star.yoni_ta}`)],
    [pick('Rajju · Nadi', 'ரஜ்ஜு · நாடி'), pick(`${star.rajju} · ${star.nadi}`, `${star.rajju_ta} · ${star.nadi_ta}`)],
    [pick('Dasa Irruppu (balance at birth)', 'தசா இருப்பு'),
      `${pick(si.dasa_irruppu.lord, si.dasa_irruppu.lord_ta)} · ${irruppuSpan(si.dasa_irruppu)}`],
    [pick('Mandi (Maandhi)', 'மாந்தி'), `${pick(mandi.sign, mandi.tamil)} ${formatDegrees(mandi.degree)} · ${pick(`H${mandi.house}`, `${mandi.house}-ம் வீடு`)}`],
    [pick('Papa Points (L / C / S)', 'பாப புள்ளிகள் (ல / ச / சு)'),
      `${si.papa_points.total} (${si.papa_points.breakdown.map(b => b.points).join(' / ')})`]
  ];
  return rows;
}

// Printable Jathagam: the sheet a Tamil family prints and shares for marriage matching
function buildJathagamSheet() {
  const c = currentChart;
  const prof = c.profile;
  const d = c.doshas;
  const bodies = chartBodies();

  const details = [
    [txt('Name', 'பெயர்'), prof.name || '—'],
    [txt('Date & Time of Birth', 'பிறந்த தேதி & நேரம்'), `${prof.date} · ${prof.time}`],
    [txt('Place', 'பிறந்த ஊர்'), `${prof.city || '—'} (${Number(prof.latitude).toFixed(2)}°, ${Number(prof.longitude).toFixed(2)}°)`],
    [txt('Timezone · Ayanamsa', 'நேர வலயம் · அயனாம்சம்'), `${prof.timezone} · ${ayanamsaLabel(prof.ayanamsa)} (${formatDegrees(c.ayanamsa_degrees)})`],
    ...kurippuRows()
  ];

  const planetRows = bodies.map(([name, pl]) => {
    const flags = [
      pl.retrograde && !['Rahu', 'Ketu'].includes(name) ? txt('Retrograde', 'வக்ரம்') : '',
      pl.combust ? txt('Combust', 'அஸ்தங்கம்') : ''
    ].filter(Boolean).join(', ');
    return `<tr>
      <td><strong>${esc(grahaName(name))}</strong></td>
      <td>${esc(signName(pl.sign_index))}</td>
      <td>${formatDegrees(pl.degree)}</td>
      <td>${esc(starName(pl.nakshatra))} · ${pl.pada}</td>
      <td>${esc(grahaName(pl.nakshatra_lord))}</td>
      <td>${pl.dignity ? esc(dignityLabel(pl.dignity)) : '—'}</td>
      <td>${esc(flags || '—')}</td>
    </tr>`;
  }).join('');

  const status = (present, cancelled) => !present ? txt('Not present', 'இல்லை')
    : (cancelled ? txt('Present, cancelled', 'உண்டு, நிவர்த்தி') : txt('Present', 'உண்டு'));
  const doshaRows = [
    [txt('Chevvai Dosham', 'செவ்வாய் தோஷம்'), status(d.chevvai.present, d.chevvai.cancelled)],
    [txt('Rahu-Ketu Dosham', 'ராகு-கேது தோஷம்'), status(d.rahu_ketu.present, false)],
    [txt('Kaal Sarp Dosham', 'கால சர்ப்ப தோஷம்'), d.kaal_sarp.present ? txt(d.kaal_sarp.type, d.kaal_sarp.type_ta) : txt('Not present', 'இல்லை')],
    [txt('Yogas', 'யோகங்கள்'), (c.yogas || []).map(y => txt(y.name, y.name_ta)).join(', ') || '—']
  ];

  const dasaBlocks = c.dasha.map(md => `
    <div class="pj-dasa-block${md.is_active ? ' active' : ''}">
      <strong>${esc(txt(`${md.lord} Dasa`, `${grahaName(md.lord)} தசை`))}</strong>
      <span>${localDate(md.start)} → ${localDate(md.end)}</span>
      <ul>${md.subperiods.map(b => `<li class="${b.is_active ? 'active' : ''}">${esc(grahaName(b.lord))} <em>${localDate(b.start)}</em></li>`).join('')}</ul>
    </div>`).join('');

  const kv = rows => rows.map(([k, v]) => `<div class="pj-kv"><span>${esc(k)}</span><strong>${esc(v)}</strong></div>`).join('');
  $('#print-jathagam').innerHTML = `
    <header class="pj-header">
      <span class="pj-om">ௐ</span>
      <h1>${txt('Horoscope', 'ஜாதகம்')}</h1>
      <p>${esc(prof.name || '')}</p>
    </header>
    <section class="pj-section"><h2>${txt('Birth Details', 'பிறப்பு விவரங்கள்')}</h2><div class="pj-grid">${kv(details)}</div></section>
    <section class="pj-charts">
      <div id="pj-rasi" class="south-chart-grid compact"></div>
      <div id="pj-amsa" class="south-chart-grid compact"></div>
    </section>
    <section class="pj-section">
      <h2>${txt('Planetary Positions', 'கிரக நிலைகள்')}</h2>
      <table class="pj-table">
        <thead><tr>
          <th>${txt('Graha', 'கிரகம்')}</th><th>${txt('Rasi', 'ராசி')}</th><th>${txt('Degree', 'பாகை')}</th>
          <th>${txt('Star · Pada', 'நட்சத்திரம் · பாதம்')}</th><th>${txt('Star Lord', 'நட்சத்திர அதிபதி')}</th>
          <th>${txt('Dignity', 'நிலை')}</th><th>${txt('Motion', 'கதி')}</th>
        </tr></thead>
        <tbody>${planetRows}</tbody>
      </table>
    </section>
    <section class="pj-section"><h2>${txt('Doshas & Yogas', 'தோஷங்கள் & யோகங்கள்')}</h2><div class="pj-grid">${kv(doshaRows)}</div></section>
    <section class="pj-section pj-dasa">
      <h2>${txt('Vimshottari Dasa-Bhukti Periods (local dates)', 'விம்சோத்தரி தசா புக்தி காலங்கள்')}</h2>
      <div class="pj-dasa-grid">${dasaBlocks}</div>
    </section>
    <footer class="pj-footer">${esc(txt(
      `Calculated by JoRoScope with the Swiss Ephemeris · ${ayanamsaLabel(prof.ayanamsa)} ayanamsa · printed ${new Date().toLocaleDateString('en-GB')}`,
      `ஜோரோஸ்கோப் சுவிஸ் எபிமெரிஸ் கணிதம் · ${ayanamsaLabel(prof.ayanamsa)} அயனாம்சம் · அச்சிட்ட நாள் ${new Date().toLocaleDateString('ta-IN')}`))}</footer>
  `;
  renderSouthChart($('#pj-rasi'), 'D1', true);
  renderSouthChart($('#pj-amsa'), 'D9', true);
}

function printJathagam() {
  if (!currentChart) {
    notify(txt('Generate a chart first.', 'முதலில் ஜாதகம் கணிக்கவும்.'));
    return;
  }
  buildJathagamSheet();
  document.body.classList.add('printing-jathagam');
  window.print();
}

// Printable Porutham report: both stars, the 10 Poruthams, Guna Milan and Dosha Samyam
function buildPoruthamSheet(match) {
  const kv = rows => rows.map(([k, v]) => `<div class="pj-kv"><span>${esc(k)}</span><strong>${v}</strong></div>`).join('');
  const person = p => [
    [txt('Name', 'பெயர்'), esc(p.name || '—')],
    [txt('Nakshatra', 'நட்சத்திரம்'), esc(txt(p.nakshatra, p.nakshatra_ta) + (p.pada ? ` · ${txt('Pada', 'பாதம்')} ${p.pada}` : ''))],
    [txt('Rasi', 'ராசி'), esc(txt(p.sign, p.sign_ta))],
    [txt('Lagna', 'லக்னம்'), esc(p.lagna ? txt(p.lagna, p.lagna_ta) : '—')],
    [txt('Gana · Yoni', 'கணம் · யோனி'), esc(`${txt(p.gana, p.gana_ta)} · ${txt(p.yoni, p.yoni_ta)}`)],
    [txt('Rajju · Nadi', 'ரஜ்ஜு · நாடி'), esc(`${txt(p.rajju, p.rajju_ta)} · ${txt(p.nadi, p.nadi_ta)}`)]
  ];
  const poruthams = match.poruthams.map(p => `
    <tr>
      <td><strong>${esc(txt(p.name, p.tamil))}</strong></td>
      <td>${esc(txt(p.description, p.description_ta))}</td>
      <td>${p.passed ? txt('Yes ✔', 'உண்டு ✔') : txt('No ✖', 'இல்லை ✖')}</td>
      <td>${p.points} / ${p.max_points}</td>
    </tr>`).join('');
  const g = match.guna_milan;
  const gunas = GUNA_LABELS.map(([key, max, en, ta]) => [txt(en, ta), `${g[key]} / ${max}`]);
  const ds = match.dosha_samyam;
  const samyam = ds ? `
    <section class="pj-section"><h2>${txt('Dosha Samyam', 'தோஷ சாம்யம்')}</h2>
      <table class="pj-table">
        <thead><tr><th>${txt('Dosha', 'தோஷம்')}</th><th>${txt('Bride', 'பெண்')}</th><th>${txt('Groom', 'ஆண்')}</th><th>${txt('Samyam', 'சாம்யம்')}</th></tr></thead>
        <tbody>${$('#dosha-samyam-tbody').innerHTML}</tbody>
      </table>
    </section>` : '';

  $('#print-jathagam').innerHTML = `
    <header class="pj-header">
      <span class="pj-om">ௐ</span>
      <h1>${txt('Marriage Compatibility Report', 'திருமணப் பொருத்த அறிக்கை')}</h1>
      <p>${esc(txt(match.verdict, match.verdict_ta))} · ${txt(`${match.passed_count} of 10 Poruthams`, `10-ல் ${match.passed_count} பொருத்தங்கள்`)} · ${txt('Guna', 'குணம்')} ${g.total_score} / 36</p>
      ${(match.verdict_notes || []).map(n => `<p><small>⚠ ${esc(txt(n.en, n.ta))}</small></p>`).join('')}
    </header>
    <section class="pj-charts">
      <div><h2>${txt('Bride', 'மணமகள்')}</h2>${kv(person(match.bride))}</div>
      <div><h2>${txt('Groom', 'மணமகன்')}</h2>${kv(person(match.groom))}</div>
    </section>
    <section class="pj-section"><h2>${txt('10 Poruthams', '10 பொருத்தங்கள்')}</h2>
      <table class="pj-table">
        <thead><tr><th>${txt('Porutham', 'பொருத்தம்')}</th><th>${txt('Significance', 'பலன்')}</th><th>${txt('Result', 'முடிவு')}</th><th>${txt('Points', 'மதிப்பெண்')}</th></tr></thead>
        <tbody>${poruthams}</tbody>
      </table>
    </section>
    ${samyam}
    <section class="pj-section"><h2>${txt('Ashta Koota (36 Gunas)', 'அஷ்ட கூடம் (36 குணங்கள்)')}</h2><div class="pj-grid">${kv(gunas)}</div></section>
    <footer class="pj-footer">${esc(txt(
      `Calculated by JoRoScope · printed ${new Date().toLocaleDateString('en-GB')} · Rules differ between traditions; consult an astrologer before deciding.`,
      `ஜோரோஸ்கோப் கணிதம் · அச்சிட்ட நாள் ${new Date().toLocaleDateString('ta-IN')} · மரபுக்கு மரபு விதிகள் வேறுபடும்; முடிவெடுக்கும் முன் ஜோதிடரை அணுகவும்.`))}</footer>
  `;
}

function printPorutham() {
  if (!lastMatch) return;
  buildPoruthamSheet(lastMatch);
  document.body.classList.add('printing-jathagam');
  window.print();
}

// Chart Style & Varga Switching
function setChartStyle(style) {
  currentStyle = style;
  ['south', 'north', 'east', 'dual'].forEach(st => {
    $(`#btn-${st}-style`).classList.toggle('active', style === st);
    $(`#${st}-chart-container`).hidden = (style !== st);
  });

  renderCurrentChart();
}

function setVarga(varga) {
  currentVarga = varga;
  $$('.varga-pill').forEach(b => b.classList.toggle('active', b.dataset.varga === varga));
  renderCurrentChart();
}

function vargaTitle(varga) {
  const [en, ta] = VARGA_NAMES[varga] || [varga, varga];
  return currentLang === 'ta' ? ta : (varga === 'Bhava' ? `${en} (Sripati)` : `${en} (${varga})`);
}

function renderCurrentChart() {
  if (!currentChart) return;
  // Rasi + Navamsa always shows D1 on the left; the right panel follows the varga pills (D9 by default).
  const amsa = currentVarga === 'D1' ? 'D9' : currentVarga;
  $('#current-varga-display').textContent = currentStyle === 'dual'
    ? `${vargaTitle('D1')} + ${vargaTitle(amsa)}`
    : vargaTitle(currentVarga);
  $('#legend-retro').textContent = currentLang === 'ta' ? '(வ) வக்ரம்' : 'Rx Retro';
  $('#legend-lagna').textContent = currentLang === 'ta' ? '╱ லக்னம்' : '╱ Lagna';

  if (currentStyle === 'south') {
    renderSouthChart($('#south-chart-container'), currentVarga);
  } else if (currentStyle === 'dual') {
    renderSouthChart($('#dual-rasi-grid'), 'D1', true);
    renderSouthChart($('#dual-amsa-grid'), amsa, true);
  } else if (currentStyle === 'north') {
    renderNorthChart();
  } else if (currentStyle === 'east') {
    renderEastChart();
  }
}

// Grahas plus Mandi (Maandhi), which Tamil and Kerala charts always show
function chartBodies() {
  const bodies = Object.entries(currentChart.planets);
  const mandi = currentChart.south_indian?.mandi;
  if (mandi) bodies.push(['Mandi', mandi]);
  return bodies;
}

function grahaAbbrev(pName) {
  const meta = PLANET_NAMES[pName];
  return currentLang === 'ta' ? meta.ta_short : meta.short;
}

// Balance of the birth Maha Dasa as years / months / days (வருடம் / மாதம் / நாள்)
function irruppuSpan(irr) {
  return currentLang === 'ta'
    ? `${irr.years} வ ${irr.months} மா ${irr.days} நா`
    : `${irr.years}y ${irr.months}m ${irr.days}d`;
}

function dasaIrruppuText(irr) {
  if (!irr) return '';
  return currentLang === 'ta'
    ? `${irr.lord_ta} தசை இருப்பு: ${irruppuSpan(irr)}`
    : `${irr.lord} Dasa balance: ${irruppuSpan(irr)}`;
}

// 1. South Indian Layout (Traditional 4x4 Grid with Fixed Signs)
function renderSouthChart(container, varga, compact = false) {
  container.replaceChildren();
  const isTa = currentLang === 'ta';

  // South Indian Sign positions [row, col] (1-indexed)
  // 0: Aries (1,2), 1: Taurus (1,3), 2: Gemini (1,4), 3: Cancer (2,4), 4: Leo (3,4), 5: Virgo (4,4),
  // 6: Libra (4,3), 7: Scorpio (4,2), 8: Sagittarius (4,1), 9: Capricorn (3,1), 10: Aquarius (2,1), 11: Pisces (1,1)
  const pos = [
    [1, 2], [1, 3], [1, 4], [2, 4],
    [3, 4], [4, 4], [4, 3], [4, 2],
    [4, 1], [3, 1], [2, 1], [1, 1]
  ];

  // Houses count from this varga's own Lagna; the inspector describes the Rasi (D1) house.
  const vargaAsc = currentChart.planets.Ascendant.vargas[varga];
  const rasiAsc = currentChart.planets.Ascendant.sign_index;
  const bodies = chartBodies();

  for (let s = 0; s < 12; s++) {
    const cell = document.createElement('div');
    cell.className = `house-cell${s === vargaAsc ? ' lagna-cell' : ''}`;
    cell.style.gridArea = `${pos[s][0]} / ${pos[s][1]}`;

    const houseNum = (s - vargaAsc + 12) % 12 + 1;

    const header = document.createElement('div');
    header.className = 'house-header';
    header.innerHTML = `
      <div>
        <span class="sign-label">${isTa ? SIGNS_TA[s] : SIGNS_EN[s]}</span>
        ${compact ? '' : `<span class="tamil-sign-label">${isTa ? SIGNS_EN[s] : SIGNS_TA[s]}</span>`}
      </div>
      <span class="house-num-badge">${isTa ? houseNum : `H${houseNum}`}</span>
    `;
    cell.append(header);

    const flow = document.createElement('div');
    flow.className = 'house-planets-flow';

    bodies.forEach(([pName, pData]) => {
      if (pData.vargas[varga] !== s) return;
      const badge = document.createElement('span');
      const isAsc = pName === 'Ascendant';
      const isBenefic = ['Jupiter', 'Venus', 'Moon', 'Mercury'].includes(pName);
      const kind = isAsc ? 'asc' : (pName === 'Mandi' ? 'upagraha' : (isBenefic ? 'benefic' : 'malefic'));
      badge.className = `planet-badge ${kind} ${pData.retrograde && !['Rahu', 'Ketu'].includes(pName) ? 'retro' : ''} ${pData.combust ? 'combust' : ''}`;
      badge.dataset.retro = isTa ? '(வ)' : 'ᴿ';
      badge.title = `${isTa ? PLANET_NAMES[pName].ta : PLANET_NAMES[pName].en} ${formatDegrees(pData.degree)}`;
      badge.textContent = grahaAbbrev(pName);
      if (varga === 'D1' && !compact) {
        const deg = document.createElement('small');
        deg.className = 'badge-deg';
        deg.textContent = `${Math.floor(pData.degree)}°`;
        badge.append(deg);
      }
      flow.append(badge);
    });

    cell.append(flow);
    cell.onclick = () => openHouseInspector((s - rasiAsc + 12) % 12 + 1, s);
    container.append(cell);
  }

  // Center box: the birth details a Tamil jathagam writes between the houses
  const prof = currentChart.profile;
  const center = document.createElement('div');
  center.className = 'chart-center-box';
  const irruppu = varga === 'D1' ? dasaIrruppuText(currentChart.south_indian?.dasa_irruppu) : '';
  center.innerHTML = `
    ${compact ? '' : '<span class="center-star">✦</span>'}
    <h3 class="center-title">${esc(isTa ? VARGA_NAMES[varga]?.[1] : VARGA_NAMES[varga]?.[0] || varga)}</h3>
    <p class="center-sub">${esc(prof.name || 'JoRoScope')}</p>
    <span class="center-meta">${esc(prof.date)} · ${esc(prof.time)}${prof.city ? ` · ${esc(prof.city)}` : ''}</span>
    ${irruppu ? `<span class="center-irruppu">${esc(irruppu)}</span>` : ''}
  `;
  container.append(center);
}

// 2. North Indian Diamond Layout (SVG Renderer)
function renderNorthChart() {
  const svg = $('#north-svg');
  svg.innerHTML = '';

  const ascSign = currentChart.planets.Ascendant.vargas[currentVarga];
  const w = 600, h = 600;

  const isLight = document.documentElement.getAttribute('data-theme') === 'light';
  const houseFill = isLight ? '#fafbf7' : 'rgba(15, 20, 42, 0.6)';
  const houseStroke = isLight ? '#b38628' : '#e5c378';
  const signColor = isLight ? '#b38628' : '#e5c378';
  const planetColor = isLight ? '#15221b' : '#ffffff';

  const houses = [
    { num: 1, path: 'M 300,0 L 450,150 L 300,300 L 150,150 Z', textPos: [300, 160], numPos: [300, 50] },
    { num: 2, path: 'M 300,0 L 150,150 L 0,0 Z', textPos: [150, 65], numPos: [210, 45] },
    { num: 3, path: 'M 0,0 L 150,150 L 0,300 Z', textPos: [50, 150], numPos: [45, 90] },
    { num: 4, path: 'M 0,300 L 150,150 L 300,300 L 150,450 Z', textPos: [150, 300], numPos: [65, 300] },
    { num: 5, path: 'M 0,300 L 150,450 L 0,600 Z', textPos: [50, 450], numPos: [45, 510] },
    { num: 6, path: 'M 0,600 L 150,450 L 300,600 Z', textPos: [150, 535], numPos: [210, 555] },
    { num: 7, path: 'M 300,600 L 150,450 L 300,300 L 450,450 Z', textPos: [300, 440], numPos: [300, 550] },
    { num: 8, path: 'M 300,600 L 450,450 L 600,600 Z', textPos: [450, 535], numPos: [390, 555] },
    { num: 9, path: 'M 600,600 L 450,450 L 600,300 Z', textPos: [550, 450], numPos: [555, 510] },
    { num: 10, path: 'M 600,300 L 450,450 L 300,300 L 450,150 Z', textPos: [450, 300], numPos: [535, 300] },
    { num: 11, path: 'M 600,300 L 450,150 L 600,0 Z', textPos: [550, 150], numPos: [555, 90] },
    { num: 12, path: 'M 600,0 L 450,150 L 300,0 Z', textPos: [450, 65], numPos: [390, 45] }
  ];

  // Draw house segments
  houses.forEach(hItem => {
    // In North Indian chart: House numbers are fixed (1-12). Sign rotating starts at House 1 = ascSign
    const signIdx = (ascSign + hItem.num - 1) % 12;

    const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    g.style.cursor = 'pointer';
    // The inspector describes the Rasi (D1) house of this sign
    g.onclick = () => openHouseInspector((signIdx - currentChart.planets.Ascendant.sign_index + 12) % 12 + 1, signIdx);

    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('d', hItem.path);
    path.setAttribute('fill', houseFill);
    path.setAttribute('stroke', houseStroke);
    path.setAttribute('stroke-width', '1.2');
    g.append(path);

    // Sign number text (1 = Aries, 12 = Pisces)
    const signText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    signText.setAttribute('x', hItem.numPos[0]);
    signText.setAttribute('y', hItem.numPos[1]);
    signText.setAttribute('fill', signColor);
    signText.setAttribute('font-size', '13');
    signText.setAttribute('font-weight', '700');
    signText.setAttribute('text-anchor', 'middle');
    signText.textContent = signIdx + 1;
    g.append(signText);

    // Planet labels in this house
    const planetsInHouse = chartBodies().filter(([pName, pData]) => {
      return pData.vargas[currentVarga] === signIdx;
    });

    if (planetsInHouse.length) {
      const planText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      planText.setAttribute('x', hItem.textPos[0]);
      planText.setAttribute('y', hItem.textPos[1]);
      planText.setAttribute('fill', planetColor);
      planText.setAttribute('font-size', '12');
      planText.setAttribute('font-weight', '700');
      planText.setAttribute('text-anchor', 'middle');

      const names = planetsInHouse.map(([n, p]) => `${grahaAbbrev(n)}${p.retrograde && !['Rahu', 'Ketu'].includes(n) ? 'ᴿ' : ''}`).join(' ');
      planText.textContent = names;
      g.append(planText);
    }

    svg.append(g);
  });
}

// 3. East Indian Layout (SVG Renderer): signs are fixed with Aries at the top centre,
// running anticlockwise; each corner square is split diagonally toward the centre.
const EAST_CELLS = [
  { pts: '200,0 400,0 400,200 200,200', at: [300, 100] },    // Aries
  { pts: '0,0 200,0 200,200', at: [133, 62] },               // Taurus
  { pts: '0,0 0,200 200,200', at: [67, 138] },               // Gemini
  { pts: '0,200 200,200 200,400 0,400', at: [100, 300] },    // Cancer
  { pts: '0,400 200,400 0,600', at: [67, 462] },             // Leo
  { pts: '200,400 200,600 0,600', at: [133, 538] },          // Virgo
  { pts: '200,400 400,400 400,600 200,600', at: [300, 500] }, // Libra
  { pts: '400,400 400,600 600,600', at: [467, 538] },        // Scorpio
  { pts: '400,400 600,400 600,600', at: [533, 462] },        // Sagittarius
  { pts: '400,200 600,200 600,400 400,400', at: [500, 300] }, // Capricorn
  { pts: '400,200 600,200 600,0', at: [533, 138] },          // Aquarius
  { pts: '400,0 600,0 400,200', at: [467, 62] }              // Pisces
];

function renderEastChart() {
  const svg = $('#east-svg');
  svg.innerHTML = '';
  const NS = 'http://www.w3.org/2000/svg';
  const isTa = currentLang === 'ta';
  const light = document.documentElement.getAttribute('data-theme') === 'light';
  const fill = light ? '#fafbf7' : 'rgba(15, 20, 42, 0.6)';
  const lagnaFill = light ? '#f3ead2' : 'rgba(229, 195, 120, 0.14)';
  const stroke = light ? '#b38628' : '#e5c378';
  const textColor = light ? '#15221b' : '#ffffff';

  const vargaAsc = currentChart.planets.Ascendant.vargas[currentVarga];
  const rasiAsc = currentChart.planets.Ascendant.sign_index;
  const bodies = chartBodies();

  const text = (x, y, content, size, color, weight = 700) => {
    const t = document.createElementNS(NS, 'text');
    t.setAttribute('x', x);
    t.setAttribute('y', y);
    t.setAttribute('fill', color);
    t.setAttribute('font-size', size);
    t.setAttribute('font-weight', weight);
    t.setAttribute('text-anchor', 'middle');
    t.textContent = content;
    return t;
  };

  EAST_CELLS.forEach((cell, s) => {
    const g = document.createElementNS(NS, 'g');
    g.style.cursor = 'pointer';
    g.onclick = () => openHouseInspector((s - rasiAsc + 12) % 12 + 1, s);

    const poly = document.createElementNS(NS, 'polygon');
    poly.setAttribute('points', cell.pts);
    poly.setAttribute('fill', s === vargaAsc ? lagnaFill : fill);
    poly.setAttribute('stroke', stroke);
    poly.setAttribute('stroke-width', s === vargaAsc ? '2.4' : '1.2');
    g.append(poly);

    const [x, y] = cell.at;
    const houseNum = (s - vargaAsc + 12) % 12 + 1;
    const signName = isTa ? SIGNS_TA[s] : SIGNS_EN[s].slice(0, 3);
    g.append(text(x, y - 22, `${signName} · ${isTa ? houseNum : `H${houseNum}`}`, 11, stroke));

    // Up to three grahas per line so the corner triangles stay legible
    const names = bodies
      .filter(([, pData]) => pData.vargas[currentVarga] === s)
      .map(([n, pData]) => `${grahaAbbrev(n)}${pData.retrograde && !['Rahu', 'Ketu'].includes(n) ? (isTa ? '(வ)' : 'ᴿ') : ''}`);
    for (let i = 0; i < names.length; i += 3) {
      g.append(text(x, y + (i / 3) * 16, names.slice(i, i + 3).join(' '), 12, textColor));
    }
    svg.append(g);
  });

  const title = VARGA_NAMES[currentVarga] || [currentVarga, currentVarga];
  svg.append(text(300, 292, isTa ? title[1] : title[0], 18, stroke));
  svg.append(text(300, 316, currentChart.profile.name || 'JoRoScope', 12, textColor, 500));
}

// House Inspector Drawer
function openHouseInspector(houseNum, signIdx) {
  if (!currentChart) return;
  const inspector = $('#house-inspector-card');
  inspector.hidden = false;

  const sign = signName(signIdx);
  const signLord = grahaName(currentChart.house_details[houseNum - 1].lord);

  $('#inspect-title').textContent = txt(`House ${houseNum} (${sign}) Inspector`, `${houseNum}-ம் பாவம் (${sign}) விவரம்`);
  $('#inspect-sign').textContent = txt(
    `Sign: ${sign} · Lord: ${signLord} · House ${houseNum} from Lagna`,
    `ராசி: ${sign} · அதிபதி: ${signLord} · லக்னத்திலிருந்து ${houseNum}-ம் பாவம்`);

  // Occupants in D1
  const occupants = Object.entries(currentChart.planets).filter(([n, p]) => p.house === houseNum);
  const occEl = $('#inspect-occupants');
  occEl.replaceChildren();
  if (occupants.length) {
    occupants.forEach(([n, p]) => {
      const pill = document.createElement('span');
      pill.className = 'planet-badge';
      pill.textContent = `${grahaName(n)} (${formatDegrees(p.degree)})`;
      occEl.append(pill);
    });
  } else {
    occEl.innerHTML = `<span class="muted">${txt('No occupant planets', 'கிரகங்கள் இல்லை')}</span>`;
  }

  // Aspects received
  const aspecting = Object.entries(currentChart.planets).filter(([n, p]) => {
    return n !== 'Ascendant' && p.aspects_cast && p.aspects_cast.includes(houseNum);
  });
  const aspEl = $('#inspect-aspects');
  aspEl.replaceChildren();
  if (aspecting.length) {
    aspecting.forEach(([n, p]) => {
      const pill = document.createElement('span');
      pill.className = 'planet-badge benefic';
      pill.textContent = txt(`${grahaName(n)} (from H${p.house})`, `${grahaName(n)} (${p.house}-ம் பாவத்திலிருந்து)`);
      aspEl.append(pill);
    });
  } else {
    aspEl.innerHTML = `<span class="muted">${txt('No direct major aspects', 'நேரடிப் பார்வைகள் இல்லை')}</span>`;
  }

  // Ashtakavarga SAV points
  const sav = currentChart.ashtakavarga.SAV[signIdx];
  $('#inspect-sav').textContent = txt(`${sav} Bindus`, `${sav} பரல்கள்`);

  // Significations
  $('#inspect-significations').textContent = txt(HOUSE_BHAVAS[houseNum], HOUSE_BHAVAS_TA[houseNum]);

  inspector.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Planets Table Rendering
function renderPlanetsTable() {
  if (!currentChart) return;
  const tbody = $('#planets-tbody');
  tbody.replaceChildren();

  Object.entries(currentChart.planets).forEach(([pName, p]) => {
    const tr = document.createElement('tr');
    const signName = currentLang === 'ta' ? p.tamil : p.sign;
    const starName = currentLang === 'ta' ? p.tamil_nakshatra : p.nakshatra;
    const pLabel = currentLang === 'ta' ? PLANET_NAMES[pName].ta : PLANET_NAMES[pName].en;

    const dignityClass = (p.dignity || '').toLowerCase().replace(/\s+/g, '-');
    const aspectsCastStr = (p.aspects_cast || []).join(', ') || '—';

    tr.innerHTML = `
      <td><strong>${pLabel}</strong></td>
      <td>${signName}</td>
      <td>${formatDegrees(p.degree)}</td>
      <td>${starName} (${txt('Pada', 'பாதம்')} ${p.pada})</td>
      <td><strong>${txt(`House ${p.house}`, `${p.house}-ம் பாவம்`)}</strong></td>
      <td>${p.bhava ? txt(`Bhava ${p.bhava}`, `${p.bhava}-ம் பாவம்`) : '—'}${p.bhava && p.bhava !== p.house ? ' ⇄' : ''}</td>
      <td><span class="dignity-badge ${dignityClass}">${dignityLabel(p.dignity)}</span></td>
      <td>${p.retrograde ? `<span class="legend-badge retro">${txt('Retrograde (Rx)', 'வக்ரம் (வ)')}</span>` : txt('Direct', 'நேர்கதி')} ${p.combust ? `<span class="legend-badge combust">🔥 ${txt('Combust', 'அஸ்தங்கம்')}</span>` : ''}</td>
      <td>${aspectsCastStr}</td>
    `;
    tbody.append(tr);
  });
}

// Ashtakavarga Rendering
function renderAshtakavarga() {
  if (!currentChart || !currentChart.ashtakavarga) return;
  const sav = currentChart.ashtakavarga.SAV;
  const bav = currentChart.ashtakavarga.BAV;

  // Render 12 SAV Cards
  const grid = $('#sav-signs-grid');
  grid.replaceChildren();

  sav.forEach((pts, idx) => {
    const card = document.createElement('div');
    const isStrong = pts >= 28;
    card.className = `sav-sign-card ${isStrong ? 'strong' : 'moderate'}`;
    card.innerHTML = `
      <small>${currentLang === 'ta' ? SIGNS_TA[idx] : SIGNS_EN[idx]}</small>
      <div class="sav-points">${pts}</div>
      <span class="muted">${isStrong ? txt('Auspicious', 'சுபம்') : txt('Average', 'சராசரி')}</span>
    `;
    grid.append(card);
  });

  // Render BAV Table
  const thead = $('#bav-header');
  thead.innerHTML = `<th>${txt('Planet', 'கிரகம்')}</th>` + SIGNS_EN.map((s, i) => `<th>${currentLang === 'ta' ? SIGNS_TA[i] : s.slice(0, 3)}</th>`).join('') + `<th>${txt('Total', 'மொத்தம்')}</th>`;

  const tbody = $('#bav-tbody');
  tbody.replaceChildren();

  Object.entries(bav).forEach(([pName, row]) => {
    const tr = document.createElement('tr');
    const rowSum = row.reduce((a, b) => a + b, 0);
    tr.innerHTML = `<td><strong>${grahaName(pName)}</strong></td>` + row.map(v => `<td>${v}</td>`).join('') + `<td><strong>${rowSum}</strong></td>`;
    tbody.append(tr);
  });
}

// Yogas & Doshas Rendering
function renderYogasAndDoshas() {
  if (!currentChart) return;
  const yogas = currentChart.yogas || [];
  const doshas = currentChart.doshas || {};

  const isTa = currentLang === 'ta';
  const houseWord = h => isTa ? `${h}-ம் வீடு` : `house ${h}`;

  // Chevvai Dosham: Tamil rule from Lagna, Moon and Venus
  const cv = doshas.chevvai;
  const mCard = $('#manglik-card');
  if (cv) {
    const status = $('#manglik-status');
    if (cv.effective) {
      mCard.className = 'cosmic-card dosha-card active-dosha';
      status.className = 'status-pill danger';
      status.textContent = isTa ? `உள்ளது (${cv.severity}/3)` : `Present (${cv.severity} of 3)`;
    } else if (cv.present) {
      mCard.className = 'cosmic-card dosha-card cancelled-dosha';
      status.className = 'status-pill success';
      status.textContent = isTa ? 'உள்ளது, ஆனால் நிவர்த்தி' : 'Present but Cancelled';
    } else {
      mCard.className = 'cosmic-card dosha-card';
      status.className = 'status-pill neutral';
      status.textContent = isTa ? 'இல்லை' : 'Not Present';
    }
    $('#manglik-desc').textContent = isTa
      ? `செவ்வாய் ${cv.mars_sign_ta} ராசியில் உள்ளது. லக்னம், சந்திரன், சுக்கிரனிலிருந்து 2, 4, 7, 8, 12-ம் வீடுகளில் செவ்வாய் இருந்தால் தோஷம்.`
      : `Mars is in ${cv.mars_sign}. The dosha arises when Mars occupies houses 2, 4, 7, 8 or 12 counted from Lagna, Moon or Venus.`;
    $('#chevvai-references').innerHTML = cv.references.map(r => {
      const state = r.afflicting ? (isTa ? 'தோஷம்' : 'afflicts') : (r.exempt ? (isTa ? 'விதிவிலக்கு' : 'exempt by sign') : (isTa ? 'தோஷமில்லை' : 'clear'));
      const cls = r.afflicting ? 'danger' : (r.exempt ? 'success' : 'neutral');
      return `<div class="dosha-ref"><span>${esc(isTa ? r.reference_ta : r.reference)}</span><span>${houseWord(r.house)}</span><span class="status-pill ${cls}">${state}</span></div>`;
    }).join('');
    $('#manglik-reasons').innerHTML = cv.cancellations.map(c => `<div>✔ ${esc(isTa ? c.ta : c.en)}</div>`).join('');
  }
  const m = doshas.manglik;
  if (m) {
    const northState = !m.present ? (isTa ? 'இல்லை' : 'not present')
      : (m.cancelled ? (isTa ? 'நிவர்த்தி' : 'cancelled') : (isTa ? 'உள்ளது' : 'present'));
    $('#manglik-north-note').textContent = isTa
      ? `வட இந்திய மாங்கலிக் விதி (லக்னத்திலிருந்து 1, 2, 4, 7, 8, 12): ${northState}.`
      : `North Indian Manglik rule (1, 2, 4, 7, 8, 12 from Lagna only): ${northState}.`;
  }

  // Rahu-Ketu Dosham
  const rk = doshas.rahu_ketu;
  const rkCard = $('#rahuketu-card');
  if (rk) {
    const status = $('#rahuketu-status');
    rkCard.className = `cosmic-card dosha-card${rk.present ? ' active-dosha' : ''}`;
    status.className = `status-pill ${rk.present ? 'danger' : 'neutral'}`;
    status.textContent = rk.present ? (isTa ? 'உள்ளது' : 'Present') : (isTa ? 'இல்லை' : 'Not Present');
    $('#rahuketu-desc').textContent = isTa
      ? 'லக்னம் அல்லது சந்திரனிலிருந்து 1, 2, 7, 8-ம் வீடுகளில் ராகு அல்லது கேது இருந்தால் தோஷம்; திருமணப் பொருத்தத்தில் இருவருக்கும் சமமாக இருப்பது நல்லது.'
      : 'Arises when Rahu or Ketu occupies houses 1, 2, 7 or 8 from Lagna or Moon. In matching, it is best balanced by a similar dosha in the partner.';
    $('#rahuketu-references').innerHTML = rk.references.map(r => {
      const nodes = isTa ? `ராகு ${r.rahu_house} · கேது ${r.ketu_house}` : `Rahu ${r.rahu_house} · Ketu ${r.ketu_house}`;
      const cls = r.afflicting ? 'danger' : 'neutral';
      const state = r.afflicting ? (isTa ? 'தோஷம்' : 'afflicts') : (isTa ? 'தோஷமில்லை' : 'clear');
      return `<div class="dosha-ref"><span>${esc(isTa ? r.reference_ta : r.reference)}</span><span>${nodes}</span><span class="status-pill ${cls}">${state}</span></div>`;
    }).join('');
  }

  // Kaal Sarp
  const ks = doshas.kaal_sarp;
  const ksCard = $('#kaalsarp-card');
  if (ks) {
    if (ks.present) {
      ksCard.className = 'cosmic-card dosha-card active-dosha';
      $('#kaalsarp-status').className = 'status-pill danger';
      $('#kaalsarp-status').textContent = txt(ks.type, ks.type_ta);
      $('#kaalsarp-desc').textContent = txt(ks.description, ks.description_ta);
    } else {
      ksCard.className = 'cosmic-card dosha-card';
      $('#kaalsarp-status').className = 'status-pill neutral';
      $('#kaalsarp-status').textContent = txt('Not Present', 'இல்லை');
      $('#kaalsarp-desc').textContent = txt(ks.description, ks.description_ta);
    }
  }

  // Detected Yogas Grid
  $('#yogas-count').textContent = txt(`${yogas.length} Detected`, `${yogas.length} யோகங்கள்`);
  const grid = $('#yogas-grid');
  grid.replaceChildren();

  if (yogas.length) {
    yogas.forEach(y => {
      const card = document.createElement('div');
      card.className = 'yoga-card';
      card.innerHTML = `
        <h3>${esc(txt(y.name, y.name_ta))}</h3>
        <div class="yoga-meta">${esc(txt(y.category, y.category_ta))} · <span style="color:var(--emerald)">${esc(txt(y.auspiciousness, y.auspiciousness_ta))}</span></div>
        <p class="yoga-desc">${esc(txt(y.description, y.description_ta))}</p>
        <div class="pill-list" style="margin-top:8px">
          ${(y.planets || []).map(p => `<span class="planet-badge benefic">${grahaName(p)}</span>`).join('')}
        </div>
      `;
      grid.append(card);
    });
  } else {
    grid.innerHTML = `<p class="muted">${txt('No major classical yogas triggered under primary rules.', 'முதன்மை விதிகளின்படி முக்கிய யோகங்கள் எதுவும் அமையவில்லை.')}</p>`;
  }
}

// 3-Tier Vimshottari Dasa Accordion
function renderDashaAccordion() {
  if (!currentChart || !currentChart.dasha) return;
  const container = $('#dasa-accordion');
  container.replaceChildren();

  currentChart.dasha.forEach(d => {
    const details = document.createElement('details');
    details.className = 'dasa-item';
    if (d.is_active) details.open = true;

    const summary = document.createElement('summary');
    summary.className = `dasa-summary ${d.is_active ? 'active-period' : ''}`;
    summary.innerHTML = `
      <div>
        <span class="dasa-name">${txt(`${d.lord} Maha Dasa`, `${grahaName(d.lord)} மகா தசை`)}</span>
        ${d.is_active ? `<span class="status-pill success" style="margin-left:8px">${txt('ACTIVE', 'நடப்பில்')}</span>` : ''}
      </div>
      <span class="dasa-dates">${localDate(d.start)} → ${localDate(d.end)}</span>
    `;
    details.append(summary);

    // Subperiods table
    const table = document.createElement('table');
    table.className = 'luxury-table bhukti-table';
    table.innerHTML = `
      <thead>
        <tr>
          <th>${txt('Bhukti', 'புக்தி')}</th>
          <th>${txt('Pratyantardasa Details', 'அந்தர விவரங்கள்')}</th>
          <th>${txt('Start', 'தொடக்கம்')}</th>
          <th>${txt('End', 'முடிவு')}</th>
        </tr>
      </thead>
      <tbody>
        ${d.subperiods.map(b => `
          <tr class="${b.is_active ? 'active-period' : ''}">
            <td><strong>${grahaName(b.lord)}</strong> ${b.is_active ? `<span class="status-pill success">${txt('Active', 'நடப்பில்')}</span>` : ''}</td>
            <td>${(b.pratyantars || []).map(p => `<span class="planet-badge ${p.is_active ? 'asc' : ''}" style="margin:2px">${grahaName(p.lord)}</span>`).join('')}</td>
            <td>${localDate(b.start)}</td>
            <td>${localDate(b.end)}</td>
          </tr>
        `).join('')}
      </tbody>
    `;
    details.append(table);
    container.append(details);
  });
}

// Yogini Dasa accordion: each yogini with its ruling graha, then its eight bhuktis
function renderYoginiAccordion() {
  const container = $('#yogini-accordion');
  const rows = currentChart?.yogini_dasha;
  if (!container || !rows) return;
  const yName = y => txt(`${y.yogini} (${grahaName(y.lord)})`, `${y.yogini_ta} (${grahaName(y.lord)})`);
  container.innerHTML = rows.map(d => `
    <details class="dasa-item"${d.is_active ? ' open' : ''}>
      <summary class="dasa-summary ${d.is_active ? 'active-period' : ''}">
        <div>
          <span class="dasa-name">${esc(yName(d))} · ${d.years} ${txt(d.years === 1 ? 'year' : 'years', 'ஆண்டு')}</span>
          ${d.is_active ? `<span class="status-pill success" style="margin-left:8px">${txt('ACTIVE', 'நடப்பில்')}</span>` : ''}
        </div>
        <span class="dasa-dates">${localDate(d.start)} → ${localDate(d.end)}</span>
      </summary>
      <table class="luxury-table bhukti-table">
        <thead><tr><th>${txt('Bhukti', 'புக்தி')}</th><th>${txt('Start', 'தொடக்கம்')}</th><th>${txt('End', 'முடிவு')}</th></tr></thead>
        <tbody>${d.subperiods.map(b => `
          <tr class="${b.is_active ? 'active-period' : ''}">
            <td><strong>${esc(yName(b))}</strong>${b.is_active ? ` <span class="status-pill success">${txt('Active', 'நடப்பில்')}</span>` : ''}</td>
            <td>${localDate(b.start)}</td><td>${localDate(b.end)}</td>
          </tr>`).join('')}
        </tbody>
      </table>
    </details>`).join('');
}

function renderUpagrahas() {
  const tbody = $('#upagrahas-tbody');
  const rows = currentChart?.south_indian?.upagrahas;
  if (!tbody || !rows) return;
  tbody.innerHTML = rows.map(u => `
    <tr>
      <td><strong>${esc(txt(u.name, u.name_ta))}</strong></td>
      <td>${esc(signName(u.sign_index))}</td>
      <td>${formatDegrees(u.degree)}</td>
      <td>${esc(starName(u.nakshatra))} (${txt('Pada', 'பாதம்')} ${u.pada})</td>
      <td>${txt(`House ${u.house}`, `${u.house}-ம் பாவம்`)}</td>
    </tr>`).join('');
}

// Dasa View Switcher & Timeline Predictions Engine
function setDasaViewMode(mode) {
  currentDasaMode = mode;
  $('#btn-mode-timeline')?.classList.toggle('active', mode === 'timeline');
  $('#btn-mode-cycles')?.classList.toggle('active', mode === 'cycles');
  $('#btn-mode-yogini')?.classList.toggle('active', mode === 'yogini');
  const tView = $('#dasa-timeline-view');
  const cView = $('#dasa-tabular-view');
  const yView = $('#dasa-yogini-view');
  if (tView) tView.hidden = (mode !== 'timeline');
  if (cView) cView.hidden = (mode !== 'cycles');
  if (yView) yView.hidden = (mode !== 'yogini');
}

function handleTimelineYearJump() {
  const yrVal = parseInt($('#timeline-jump-year')?.value, 10);
  if (!yrVal || isNaN(yrVal)) {
    timelineSearchYear = null;
  } else {
    timelineSearchYear = yrVal;
    currentTimelineFilter = 'all';
    $$('.timeline-filter-btn').forEach(b => b.classList.toggle('active', b.dataset.tfilter === 'all'));
  }
  renderDasaTimelineView();
}

function renderDasaTimelineView() {
  if (!currentChart || !currentChart.predictions) return;
  const tp = currentChart.predictions.timeline_predictions;
  if (!tp) return;
  const isTa = currentLang === 'ta';

  // 1. Active Period Spotlight Card
  const sp = tp.active_spotlight;
  const spotCard = $('#timeline-spotlight-card');
  if (sp && spotCard) {
    const dLordName = isTa ? (sp.dasa_lord_ta || sp.dasa_lord) : sp.dasa_lord;
    const bLordName = isTa ? (sp.bhukti_lord_ta || sp.bhukti_lord) : sp.bhukti_lord;

    $('#spotlight-lords-title').textContent = isTa
      ? `${dLordName} மகா தசை — ${bLordName} புக்தி`
      : `${dLordName} Maha Dasa — ${bLordName} Bhukti`;

    $('#spotlight-period-theme').textContent = isTa ? (sp.title_ta || sp.strategic_advice_ta) : (sp.title_en || sp.strategic_advice_en);
    $('#spotlight-dates').textContent = `${sp.start_date} → ${sp.end_date}`;
    $('#spotlight-age').textContent = `${sp.age} ${isTa ? 'வயது' : 'Years'}`;
    $('#spotlight-elapsed').textContent = `${sp.elapsed_days} ${isTa ? 'நாட்கள்' : 'Days'}`;
    $('#spotlight-remaining').textContent = `${sp.remaining_days} ${isTa ? 'நாட்கள்' : 'Days'}`;

    const starIcons = '★'.repeat(sp.potency) + '☆'.repeat(Math.max(0, 5 - sp.potency));
    const potencyBadge = $('#spotlight-potency-badge');
    if (potencyBadge) {
      potencyBadge.textContent = `${starIcons} ${sp.potency >= 4 ? (isTa ? 'அதி உத்தமம்' : 'High Potency') : (sp.potency >= 3 ? (isTa ? 'மத்திமம்' : 'Moderate') : (isTa ? 'கவனம் தேவை' : 'Caution Required'))}`;
    }

    const progBar = $('#spotlight-progress-bar');
    if (progBar) progBar.style.width = `${sp.percent}%`;
    const progText = $('#spotlight-progress-text');
    if (progText) {
      progText.textContent = isTa
        ? `${sp.percent}% காலம் முடிவடைந்தது (${sp.elapsed_days} நாட்கள் நிறைவு · ${sp.remaining_days} நாட்கள் மீதம்)`
        : `${sp.percent}% Elapsed (${sp.elapsed_days} days passed · ${sp.remaining_days} days remaining)`;
    }

    $('#spotlight-advice-text').textContent = isTa ? sp.strategic_advice_ta : sp.strategic_advice_en;
    $('#spotlight-remedy-text').textContent = isTa ? sp.primary_remedy_ta : sp.primary_remedy_en;
  }

  // 2. 10-Year Annual Projections Grid
  const annualGrid = $('#annual-projections-grid');
  const annualSec = $('#annual-milestones-section');
  if (annualGrid && tp.annual_projections) {
    annualGrid.replaceChildren();
    tp.annual_projections.forEach(ap => {
      const aCard = document.createElement('div');
      aCard.className = `annual-card ${ap.is_current_year ? 'current-year' : ''}`;

      const dStr = isTa ? (ap.dasa_lord_ta || ap.dasa_lord) : ap.dasa_lord;
      const bStr = isTa ? (ap.bhukti_lord_ta || ap.bhukti_lord) : ap.bhukti_lord;
      const theme = isTa ? ap.theme_ta : ap.theme_en;

      aCard.innerHTML = `
        <div class="annual-card-top">
          <span class="annual-year-badge">${ap.icon} ${ap.year}</span>
          <span class="annual-age-pill">${isTa ? 'வயது' : 'Age'} ${ap.age}</span>
        </div>
        <div class="annual-lords">${esc(dStr)} / ${esc(bStr)}</div>
        <p class="annual-theme-text">${esc(theme)}</p>
        <div class="annual-score-wrap">
          <span>${isTa ? 'சுப பலம்' : 'Astro Score'}: ${ap.score}/100</span>
          <div class="annual-score-bar-track">
            <div class="annual-score-bar-fill" style="width: ${ap.score}%"></div>
          </div>
        </div>
      `;
      annualGrid.append(aCard);
    });
  }

  if (annualSec) {
    annualSec.hidden = (currentTimelineFilter !== 'annual' && currentTimelineFilter !== 'all');
  }

  // 3. Chronological Periods Stream Filtered
  renderTimelineStream(tp.periods, isTa);
}

function renderTimelineStream(periods, isTa) {
  const container = $('#timeline-periods-stream');
  if (!container) return;
  container.replaceChildren();

  if (!periods || !periods.length) {
    container.innerHTML = `<p class="muted">${isTa ? 'காலவரிசை விவரங்கள் கிடைக்கவில்லை.' : 'No timeline periods available.'}</p>`;
    return;
  }

  const nowYear = new Date().getFullYear();

  const filtered = periods.filter(p => {
    // Planet filter
    if (currentTimelinePlanet !== 'all') {
      if (p.dasa_lord.toLowerCase() !== currentTimelinePlanet.toLowerCase()) {
        return false;
      }
    }

    // Specific Year Search filter
    if (timelineSearchYear !== null) {
      try {
        const sYr = parseInt(p.start_date.slice(0, 4), 10);
        const eYr = parseInt(p.end_date.slice(0, 4), 10);
        if (timelineSearchYear < sYr || timelineSearchYear > eYr) {
          return false;
        }
      } catch (e) {
        return false;
      }
    }

    // Category button filter
    if (currentTimelineFilter === 'active') {
      return p.is_active;
    } else if (currentTimelineFilter === 'next5') {
      try {
        const sYr = parseInt(p.start_date.slice(0, 4), 10);
        const eYr = parseInt(p.end_date.slice(0, 4), 10);
        return p.is_active || (p.is_future && sYr <= nowYear + 5);
      } catch (e) {
        return p.is_active;
      }
    } else if (currentTimelineFilter === 'annual') {
      return false; // Annual view displays the annual grid prominently
    } else if (currentTimelineFilter === 'auspicious') {
      return p.potency >= 3;
    } else if (currentTimelineFilter === 'caution') {
      return p.potency <= 2;
    }

    return true; // 'all'
  });

  const countBadge = $('#timeline-count-badge');
  if (countBadge) {
    countBadge.textContent = isTa
      ? `${filtered.length} / ${periods.length} காலங்கள்`
      : `Showing ${filtered.length} of ${periods.length} Periods`;
  }

  if (filtered.length === 0) {
    container.innerHTML = `<div class="cosmic-card" style="text-align:center;padding:30px;"><p class="muted">${isTa ? 'தேர்ந்தெடுக்கப்பட்ட வடிகட்டியில் காலங்கள் எதுவும் அமையவில்லை.' : 'No periods matched the selected filter criteria.'}</p></div>`;
    return;
  }

  filtered.forEach(p => {
    const card = document.createElement('div');
    card.className = `timeline-card ${p.is_active ? 'active-period' : (p.is_past ? 'past-period' : '')}`;

    const dLordStr = isTa ? (p.dasa_lord_ta || p.dasa_lord) : p.dasa_lord;
    const bLordStr = isTa ? (p.bhukti_lord_ta || p.bhukti_lord) : p.bhukti_lord;
    const titleStr = isTa ? (p.title_ta || p.theme_ta) : (p.title_en || p.theme_en);
    const themeStr = isTa ? p.theme_ta : p.theme_en;

    let statusLabel = '';
    if (p.is_active) {
      statusLabel = `<span class="status-pill success">${isTa ? '🔴 நடைமுறையில் உள்ள காலம்' : '🔴 LIVE ACTIVE'}</span>`;
    } else if (p.is_future) {
      statusLabel = `<span class="status-pill info">${isTa ? 'எதிர்காலம்' : 'UPCOMING'}</span>`;
    } else {
      statusLabel = `<span class="status-pill neutral">${isTa ? 'முடிந்த காலம்' : 'PAST'}</span>`;
    }

    const starIcons = '★'.repeat(p.potency) + '☆'.repeat(Math.max(0, 5 - p.potency));

    card.innerHTML = `
      <div class="timeline-card-header">
        <div class="timeline-title-wrap">
          <h3>
            <span>${esc(dLordStr)} — ${esc(bLordStr)}</span>
            ${statusLabel}
          </h3>
          <div class="timeline-timing-pill">
            📅 ${p.start_date} → ${p.end_date} · <strong>${isTa ? 'வயது' : 'Age'} ${p.age_start} – ${p.age_end}</strong> (${p.duration_months} ${isTa ? 'மாதங்கள்' : 'months'})
          </div>
        </div>
      </div>

      <div class="timeline-badges-row">
        <span class="mutual-badge ${p.mutual_class}">${esc(isTa ? (p.mutual_rel_ta || p.mutual_rel) : p.mutual_rel)}</span>
        <span class="potency-pill">${starIcons} (${isTa ? (p.potency >= 4 ? 'உத்தமம்' : (p.potency >= 3 ? 'மத்திமம்' : 'எச்சரிக்கை')) : (p.potency >= 4 ? 'Favorable' : (p.potency >= 3 ? 'Moderate' : 'Caution'))})</span>
      </div>

      <div class="timeline-theme-narrative">
        <strong>${esc(titleStr)}:</strong> ${esc(themeStr)}
      </div>

      <button type="button" class="timeline-details-toggle ${p.is_active ? 'expanded' : ''}" aria-expanded="${p.is_active ? 'true' : 'false'}">
        <span class="toggle-icon">${p.is_active ? '▼' : '▶'}</span>
        <span class="toggle-label">${isTa
          ? (p.is_active ? 'விரிவான பலாபலன்கள் (திறக்கப்பட்டுள்ளது - மூட கிளிக் செய்யவும்)' : 'விரிவான பலாபலன்கள் (தொழில், தனம், நலம், குடும்பம், பரிகாரம்)')
          : (p.is_active ? 'Detailed Breakdown (Expanded - Click to Collapse)' : 'Detailed Breakdown (Career, Wealth, Health, Family, Remedies)')}</span>
      </button>

      <div class="timeline-details-panel" ${p.is_active ? '' : 'hidden'} style="display: ${p.is_active ? 'grid' : 'none'};">
        <div class="timeline-dim-card">
          <h4>💼 ${isTa ? 'தொழில் & உத்தியோகம்' : 'Career & Profession'}</h4>
          <p>${esc(isTa ? p.career_ta : p.career_en)}</p>
        </div>
        <div class="timeline-dim-card">
          <h4>💰 ${isTa ? 'தனம் & முதலீடு' : 'Wealth & Assets'}</h4>
          <p>${esc(isTa ? p.wealth_ta : p.wealth_en)}</p>
        </div>
        <div class="timeline-dim-card">
          <h4>🌿 ${isTa ? 'உடல்நலம் & உணவு' : 'Health & Vitality'}</h4>
          <p>${esc(isTa ? p.health_ta : p.health_en)}</p>
        </div>
        <div class="timeline-dim-card">
          <h4>🏡 ${isTa ? 'குடும்பம் & இல்லறம்' : 'Family & Relationships'}</h4>
          <p>${esc(isTa ? p.family_ta : p.family_en)}</p>
        </div>
        <div class="timeline-dim-card">
          <h4>🎯 ${isTa ? 'முக்கிய மைல்கல்' : 'Key Milestones'}</h4>
          <p>${esc(isTa ? p.milestones_ta : p.milestones_en)}</p>
        </div>
        <div class="timeline-dim-card">
          <h4>🕉️ ${isTa ? 'வேத பரிகாரம் & வழிபாடு' : 'Remedy & Mantra'}</h4>
          <p>${esc(isTa ? p.remedy_ta : p.remedy_en)}</p>
        </div>
      </div>
    `;

    const toggleBtn = card.querySelector('.timeline-details-toggle');
    const panel = card.querySelector('.timeline-details-panel');
    if (toggleBtn && panel) {
      toggleBtn.addEventListener('click', (e) => {
        e.preventDefault();
        const willOpen = panel.hidden || panel.style.display === 'none' || panel.hasAttribute('hidden');
        if (willOpen) {
          panel.hidden = false;
          panel.removeAttribute('hidden');
          panel.style.display = 'grid';
          toggleBtn.classList.add('expanded');
          toggleBtn.setAttribute('aria-expanded', 'true');
          toggleBtn.querySelector('.toggle-icon').textContent = '▼';
          toggleBtn.querySelector('.toggle-label').textContent = isTa
            ? 'விரிவான பலாபலன்கள் (திறக்கப்பட்டுள்ளது - மூட கிளிக் செய்யவும்)'
            : 'Detailed Breakdown (Expanded - Click to Collapse)';
        } else {
          panel.hidden = true;
          panel.setAttribute('hidden', '');
          panel.style.display = 'none';
          toggleBtn.classList.remove('expanded');
          toggleBtn.setAttribute('aria-expanded', 'false');
          toggleBtn.querySelector('.toggle-icon').textContent = '▶';
          toggleBtn.querySelector('.toggle-label').textContent = isTa
            ? 'விரிவான பலாபலன்கள் (தொழில், தனம், நலம், குடும்பம், பரிகாரம்)'
            : 'Detailed Breakdown (Career, Wealth, Health, Family, Remedies)';
        }
      });
    }

    container.append(card);
  });
}

// Life Predictions Multi-Chapter Comprehensive Renderer
// Verdict pill for a house or planet reading: strong / moderate / weak
function strengthPill(item) {
  if (!item.strength) return '';
  const cls = { strong: 'success', moderate: 'neutral', weak: 'danger' }[item.strength];
  const en = { strong: 'Strong', moderate: 'Moderate', weak: 'Needs care' }[item.strength];
  return `<span class="status-pill ${cls}">${txt(en, item.strength_ta)}</span>`;
}

function renderLifeReadings() {
  if (!currentChart) return;
  const pred = currentChart.predictions;
  if (!pred) return;
  const isTa = currentLang === 'ta';

  // Chapter 1: Natal Elements & Personality
  const ov = pred.overview;
  if (ov) {
    // Star
    $('#pred-star-title').textContent = isTa
      ? `ஜென்ம நட்சத்திரம்: ${ov.tamil_nakshatra} (${ov.nakshatra})`
      : `Birth Star: ${ov.nakshatra} (${ov.tamil_nakshatra})`;
    $('#pred-star-sub').textContent = isTa
      ? 'குணம், மனோபாவம் மற்றும் விதியின் தாக்கம்'
      : 'Core Character, Temperament & Destiny';
    $('#pred-star-text').textContent = isTa ? ov.nakshatra_pred_ta : ov.nakshatra_pred_en;

    // Lagna
    $('#pred-lagna-title').textContent = isTa
      ? `லக்னம் (உதய ராசி): ${ov.tamil_lagna} (${ov.lagna})`
      : `Ascendant (Lagna): ${ov.lagna} (${ov.tamil_lagna})`;
    $('#pred-lagna-sub').textContent = isTa
      ? 'உடல்வாகு, தலைமைப் பண்பு மற்றும் வாழ்க்கை திசை'
      : 'Body Constitution, Leadership & Life Path';
    $('#pred-lagna-text').textContent = isTa ? ov.lagna_pred_ta : ov.lagna_pred_en;

    // Moon Sign
    $('#pred-moon-title').textContent = isTa
      ? `சந்திர ராசி: ${ov.tamil_moon_sign} (${ov.moon_sign})`
      : `Moon Sign (Rasi): ${ov.moon_sign} (${ov.tamil_moon_sign})`;
    $('#pred-moon-sub').textContent = isTa
      ? 'உள்மன உணர்வுகள், சிந்தனை ஓட்டம் மற்றும் கற்பனை வளம்'
      : 'Emotional Landscape, Instincts & Mental Equanimity';
    $('#pred-moon-text').textContent = isTa
      ? `சந்திர பகவான் உங்கள் மனோகாரகனாக ${ov.tamil_moon_sign} ராசியில் அமைந்து, சிந்தனைத் தெளிவையும் உணர்ச்சிப் பெருக்கையும் நிர்வகிக்கிறார். கற்பனை வளம், தாய்வழி ஆசிகள், சூழலுக்கு ஏற்ப பொருந்தும் நெகிழ்வுத்தன்மை இயல்பாகவே அமையும்.`
      : `The Moon placed in ${ov.moon_sign} governs your subconscious temperament, empathy, and intuitive reactions. It provides emotional adaptability, imaginative clarity, maternal grace, and domestic prosperity.`;

    // Sun & Tithi
    $('#pred-sun-title').textContent = isTa
      ? `சூரியன் & திதி: ${tithiLabel(ov.tithi_name)} (யோகம்: ${nityaYogaLabel(ov.yoga_name)})`
      : `Sun & Tithi: ${ov.tithi_name} (${ov.yoga_name} Yoga)`;
    $('#pred-sun-sub').textContent = isTa
      ? 'ஆன்ம பலம், கௌரவம் மற்றும் நித்திய சுப யோகம்'
      : 'Soul Vitality, Integrity & Auspicious Alignment';
    $('#pred-sun-text').textContent = isTa
      ? `நீங்கள் ${tithiLabel(ov.tithi_name)} திதியிலும், ${nityaYogaLabel(ov.yoga_name)} யோகத்திலும் அவதரித்துள்ளீர்கள். ஆன்ம காரகனான சூரியனின் ஆதிக்கத்தால் சமூக அந்தஸ்து, கடமை உணர்வு, தர்ம சிந்தனை மற்றும் அசைக்க முடியாத தன்னம்பிக்கை உங்களை முன்னிறுத்தும்.`
      : `Born under the sacred lunar day ${ov.tithi_name} and soli-lunar combination ${ov.yoga_name}. Sun governs your core vital spark and moral resolve, bestowing natural authority, honorable ambition, and perseverance in duty.`;
  }

  // Chapter 2: 12 Bhavas Comprehensive Life Path
  const bhavasContainer = $('#bhavas-cards-container');
  bhavasContainer.replaceChildren();
  if (pred.bhavas && pred.bhavas.length) {
    pred.bhavas.forEach(b => {
      const card = document.createElement('div');
      card.className = 'bhava-card';
      const isSavStrong = b.sav_points >= 28;
      const occStr = b.occupants && b.occupants.length ? grahaNames(b.occupants) : (isTa ? 'கிரகங்கள் இல்லை' : 'None');
      const aspStr = b.aspected_by && b.aspected_by.length ? grahaNames(b.aspected_by) : (isTa ? 'நேரடி பார்வைகள் இல்லை' : 'None');
      const title = isTa ? b.title_ta : b.title_en;
      const narrative = isTa ? b.prediction_ta : b.prediction_en;

      card.innerHTML = `
        <div class="bhava-header">
          <div class="bhava-title-group">
            <span class="bhava-num-badge">${b.house}</span>
            <div>
              <h3>${esc(title)}</h3>
              <small class="muted">${isTa ? b.tamil_sign : b.sign} · ${isTa ? 'அதிபதி' : 'Lord'}: ${grahaName(b.lord)} (${isTa ? `${b.lord_house}-ம் பாவம்` : `H${b.lord_house}`})</small>
            </div>
          </div>
          <span class="bhava-meta-pill ${isSavStrong ? 'highlight' : ''}">${b.sav_points} ${txt('SAV Bindus', 'சர்வாஷ்டக பரல்கள்')}</span>
        </div>
        <div class="bhava-meta-strip">
          ${strengthPill(b)}
          <span class="bhava-meta-pill">${isTa ? 'அதிபதி நிலை' : 'Lord Dignity'}: <strong>${dignityLabel(b.lord_dignity)}</strong></span>
          <span class="bhava-meta-pill">${isTa ? 'அமர்ந்த கிரகங்கள்' : 'Occupants'}: <strong>${esc(occStr)}</strong></span>
          <span class="bhava-meta-pill">${isTa ? 'பார்வை கிரகங்கள்' : 'Aspects'}: <strong>${esc(aspStr)}</strong></span>
        </div>
        <p class="reading-body">${esc(narrative)}</p>
        ${(b.factors || []).length ? `<ul class="bhava-factors">${b.factors.map(f => `
          <li class="${f.effect > 0 ? 'plus' : (f.effect < 0 ? 'minus' : 'neutral')}">${esc(txt(f.en, f.ta))}</li>`).join('')}
        </ul>` : ''}
      `;
      bhavasContainer.append(card);
    });
  }

  // Chapter 3: Planets in Houses
  const planetsContainer = $('#planets-cards-container');
  planetsContainer.replaceChildren();
  if (pred.planets_in_houses && pred.planets_in_houses.length) {
    pred.planets_in_houses.forEach(p => {
      const card = document.createElement('div');
      card.className = 'planet-pred-card';
      const pInfo = PLANET_NAMES[p.planet] || { en: p.planet, ta: p.planet, color: '#e5c378' };
      const pLabel = isTa ? pInfo.ta : pInfo.en;
      const narrative = isTa ? p.prediction_ta : p.prediction_en;
      const dignityClass = (p.dignity || '').toLowerCase().replace(/\s+/g, '-');

      card.innerHTML = `
        <div class="planet-pred-header">
          <div class="planet-title-group">
            <span class="bhava-num-badge" style="border-color:${pInfo.color}; color:${pInfo.color}">${pInfo.short || p.planet.slice(0, 2)}</span>
            <div>
              <h3>${esc(pLabel)}</h3>
              <small class="muted">${isTa ? 'பாவம்' : 'House'} ${p.house} · ${isTa ? p.tamil_sign : p.sign}</small>
            </div>
          </div>
          <span class="dignity-badge ${dignityClass}">${dignityLabel(p.dignity)}</span>
        </div>
        <div class="planet-meta-strip">
          ${strengthPill(p)}
          ${p.retrograde ? `<span class="legend-badge retro">${isTa ? 'வக்ரம் (Rx)' : 'Retrograde (Rx)'}</span>` : ''}
          ${p.combust ? `<span class="legend-badge combust">${isTa ? '🔥 அஸ்தமனம்' : '🔥 Combust'}</span>` : ''}
          <span class="bhava-meta-pill">${isTa ? 'ராசி' : 'Rasi'}: <strong>${isTa ? p.tamil_sign : p.sign}</strong></span>
        </div>
        <p class="reading-body">${esc(narrative)}</p>
      `;
      planetsContainer.append(card);
    });
  }

  // Chapter 4: Dasa-Bhukti Life Phases
  const dasaForecast = pred.dasa_forecast;
  if (dasaForecast) {
    if (dasaForecast.active_period) {
      const ad = dasaForecast.active_period;
      $('#pred-dasa-active-title').textContent = isTa
        ? `தற்போதைய இயங்கும் தசா-புக்தி: ${grahaName(ad.dasa)} தசை — ${grahaName(ad.bhukti)} புக்தி`
        : `Active Running Period: ${ad.dasa} Maha Dasa — ${ad.bhukti} Bhukti`;
      $('#pred-dasa-active-desc').textContent = isTa ? dasaForecast.active_forecast_ta : dasaForecast.active_forecast_en;
    }

    const dasasList = $('#maha-dasas-list');
    dasasList.replaceChildren();
    if (dasaForecast.all_dasas) {
      const activeLord = dasaForecast.active_period ? dasaForecast.active_period.dasa : '';
      Object.entries(dasaForecast.all_dasas).forEach(([pLord, texts]) => {
        const dCard = document.createElement('div');
        const isActive = pLord.toLowerCase() === activeLord.toLowerCase();
        dCard.className = `maha-dasa-card ${isActive ? 'active-period' : ''}`;
        const pInfo = PLANET_NAMES[pLord] || { en: pLord, ta: pLord };
        const label = isTa ? pInfo.ta : pInfo.en;
        const text = isTa ? texts.ta : texts.en;

        dCard.innerHTML = `
          <h4>
            <span>${esc(label)} ${isTa ? 'மகா தசை' : 'Maha Dasa'}</span>
            ${isActive ? `<span class="status-pill success">${isTa ? 'நடைமுறையில் உள்ளது' : 'ACTIVE'}</span>` : ''}
          </h4>
          <p class="reading-body" style="font-size:12px">${esc(text)}</p>
        `;
        dasasList.append(dCard);
      });
    }
  }

  // Chapter 5: Transits (Gochara)
  const transits = pred.transits;
  if (transits) {
    const s = transits.saturn;
    if (s) {
      $('#saturn-transit-title').textContent = isTa ? s.title_ta : s.title_en;
      $('#saturn-transit-badge').textContent = isTa
        ? `சந்திரனிலிருந்து ${s.house_from_moon}-ஆம் இடம்`
        : `House ${s.house_from_moon} from Moon`;
      $('#saturn-transit-badge').className = `status-pill ${[12, 1, 2, 8].includes(s.house_from_moon) ? 'danger' : 'success'}`;
      $('#saturn-transit-desc').textContent = isTa ? s.prediction_ta : s.prediction_en;
    }

    const j = transits.jupiter;
    if (j) {
      $('#jupiter-transit-title').textContent = isTa
        ? 'குருப் பெயர்ச்சி பலன்'
        : 'Jupiter Transit (Guru Peyarchi)';
      $('#jupiter-transit-badge').textContent = j.favorable
        ? (isTa ? 'சுப பலன்' : 'Auspicious')
        : (isTa ? 'மத்திம பலன்' : 'Moderate');
      $('#jupiter-transit-badge').className = `status-pill ${j.favorable ? 'success' : 'neutral'}`;
      $('#jupiter-transit-desc').textContent = isTa ? j.prediction_ta : j.prediction_en;
    }

    const rk = transits.rahu_ketu;
    if (rk) {
      $('#rahuketu-transit-title').textContent = isTa ? 'ராகு-கேது பெயர்ச்சி பலன்' : 'Rahu-Ketu Transit';
      $('#rahuketu-transit-badge').textContent = rk.favorable
        ? (isTa ? 'சுப பலன்' : 'Favourable')
        : (isTa ? 'கவனம் தேவை' : 'Caution');
      $('#rahuketu-transit-badge').className = `status-pill ${rk.favorable ? 'success' : 'neutral'}`;
      $('#rahuketu-transit-desc').textContent = isTa ? rk.prediction_ta : rk.prediction_en;
    }
  }
  renderGochara();

  // Chapter 6: Lucky Gemstones & Remedies
  const luck = pred.lucky_factors;
  if (luck) {
    $('#gem-primary').textContent = txt(luck.primary_gem, luck.primary_gem_ta) || '—';
    $('#gem-fortune').textContent = txt(luck.fortune_gem, luck.fortune_gem_ta) || '—';
    $('#gem-metal').textContent = txt(luck.metal, luck.metal_ta) || '—';
    $('#gem-finger').textContent = txt(luck.finger, luck.finger_ta) || '—';
    $('#gem-day').textContent = txt(luck.wearing_day, luck.wearing_day_ta) || '—';

    $('#luck-numbers').textContent = luck.lucky_numbers ? luck.lucky_numbers.join(', ') : '—';
    $('#luck-days').textContent = (txt(luck.lucky_days, luck.lucky_days_ta) || []).join(', ') || '—';
    $('#luck-colors').textContent = (txt(luck.lucky_colors, luck.lucky_colors_ta) || []).join(', ') || '—';
    $('#luck-deities').textContent = isTa ? luck.deity_worship_ta : luck.deity_worship_en;
  }

  // Chapter 7: Jaimini Chara Karakas & Karakamsha
  const jk = pred.jaimini_karakas;
  if (jk) {
    if (jk.karakamsha) {
      $('#jaimini-karakamsha-title').textContent = isTa
        ? `காரகாம்சம்: ${jk.karakamsha.tamil_sign} (${jk.karakamsha.sign})`
        : `Karakamsha Lagna: ${jk.karakamsha.sign} (${jk.karakamsha.tamil_sign})`;
      $('#jaimini-karakamsha-desc').textContent = isTa
        ? jk.karakamsha.interpretation_ta
        : jk.karakamsha.interpretation_en;
    }

    const jGrid = $('#jaimini-karakas-grid');
    jGrid.replaceChildren();
    if (jk.karakas) {
      jk.karakas.forEach(k => {
        const card = document.createElement('div');
        const isAk = k.code === 'AK';
        card.className = `karaka-card ${isAk ? 'ak-card' : ''}`;
        card.innerHTML = `
          <div class="karaka-card-header">
            <div>
              <span class="karaka-code-badge">${k.code}</span>
              <strong style="margin-left:8px; font-family:var(--font-serif); font-size:15px; color:var(--gold);">
                ${isTa ? k.title_ta : k.title_en}
              </strong>
            </div>
            <small class="muted">${k.degree_str}</small>
          </div>
          <div class="bhava-meta-strip">
            <span class="bhava-meta-pill">${isTa ? 'கிரகம்' : 'Planet'}: <strong>${isTa ? k.tamil_planet : k.planet}</strong></span>
            <span class="bhava-meta-pill">${isTa ? 'ராசி' : 'Sign'}: <strong>${isTa ? k.tamil_sign : k.sign}</strong></span>
            <span class="bhava-meta-pill">${isTa ? 'பாவம்' : 'House'}: <strong>${k.house}</strong></span>
            <span class="bhava-meta-pill">${isTa ? 'நிலை' : 'Dignity'}: <strong>${dignityLabel(k.dignity)}</strong></span>
          </div>
          <p class="reading-body" style="font-size:12.5px">${esc(isTa ? k.reading_ta : k.reading_en)}</p>
        `;
        jGrid.append(card);
      });
    }
  }

  // Chapter 8: Double Transit (Dwi-Gochara) Timing Engine
  const dt = pred.double_transit;
  if (dt) {
    if (dt.calculation_date_utc) {
      $('#timing-calc-date').textContent = `${txt('Live', 'நேரலை')}: ${dt.calculation_date_utc.slice(0, 10)}`;
    }
    if (dt.transit_saturn) {
      $('#timing-saturn-pos').textContent = `${isTa ? dt.transit_saturn.tamil_sign : dt.transit_saturn.sign} (${dt.transit_saturn.degree_str})`;
    }
    if (dt.transit_jupiter) {
      $('#timing-jupiter-pos').textContent = `${isTa ? dt.transit_jupiter.tamil_sign : dt.transit_jupiter.sign} (${dt.transit_jupiter.degree_str})`;
    }

    const tGrid = $('#timing-milestones-grid');
    tGrid.replaceChildren();
    if (dt.milestones) {
      dt.milestones.forEach(m => {
        const card = document.createElement('div');
        card.className = `timing-event-card ${m.is_active ? 'active-window' : ''}`;
        card.innerHTML = `
          <div class="timing-card-header">
            <div>
              <h3 style="font-family:var(--font-serif); font-size:16px; color:var(--gold); margin:0 0 4px;">
                ${esc(isTa ? m.title_ta : m.title_en)}
              </h3>
              <small class="muted">${isTa ? m.target_house_ta : m.target_house}</small>
            </div>
            <span class="status-pill ${m.is_active ? 'success' : 'neutral'}">
              ${esc(isTa ? m.status_ta : m.status_en)}
            </span>
          </div>
          <div class="timing-score-bar">
            <small class="muted">${isTa ? 'சாதக சதவீதம்' : 'Probability Score'}:</small>
            <div class="timing-track">
              <div class="timing-fill" style="width:${m.score}%"></div>
            </div>
            <strong style="color:var(--gold); font-size:12px">${m.score}%</strong>
          </div>
          <p class="reading-body" style="font-size:12.5px">${esc(isTa ? m.desc_ta : m.desc_en)}</p>
        `;
        tGrid.append(card);
      });
    }
  }

  // Chapter 9: D-10 Dasamsa Career & Vocation
  const c10 = pred.career_d10;
  if (c10) {
    if (c10.top_archetype) {
      $('#career-top-title').textContent = `${isTa ? 'முதன்மை யோகம்' : 'Prime Calling'}: ${isTa ? c10.top_archetype.title_ta : c10.top_archetype.title_en}`;
      $('#career-top-badge').textContent = `${c10.top_archetype.score}% ${isTa ? 'பொருத்தம்' : 'Aptitude Match'}`;
      $('#career-top-narrative').textContent = isTa ? c10.narrative_ta : c10.narrative_en;
    }

    const cContainer = $('#career-archetypes-container');
    cContainer.replaceChildren();
    if (c10.all_archetypes) {
      c10.all_archetypes.forEach((arch, idx) => {
        const card = document.createElement('div');
        const isTop = idx === 0;
        card.className = `career-arch-card ${isTop ? 'top-calling' : ''}`;
        card.innerHTML = `
          <div class="career-arch-header">
            <div>
              <strong style="font-size:15px; font-family:var(--font-serif); color:var(--gold);">
                ${esc(isTa ? arch.title_ta : arch.title_en)}
              </strong>
              <div style="font-size:11.5px; color:var(--text-muted); margin-top:2px">
                ${isTa ? arch.suitability_ta : arch.suitability}
              </div>
            </div>
            <span class="status-pill ${arch.score >= 80 ? 'success' : 'neutral'}">${arch.score}%</span>
          </div>
          <div class="career-progress-track">
            <div class="career-progress-fill" style="width:${arch.score}%"></div>
          </div>
          <div style="font-size:12px; color:var(--text-secondary); margin-top:4px">
            <strong>${isTa ? 'முக்கிய துறைகள்' : 'Industry Sectors'}:</strong> ${esc(isTa ? arch.key_sectors_ta : arch.key_sectors_en)}
          </div>
        `;
        cContainer.append(card);
      });
    }
  }

  // Chapter 10: Ayur-Jyotish & Tridosha Wellness
  const ayur = pred.ayur_jyotish;
  if (ayur) {
    $('#ayur-prakriti-title').textContent = isTa ? ayur.prakriti_ta : ayur.prakriti_en;
    $('#vata-pct').textContent = `${ayur.vata_percentage}%`;
    $('#vata-fill').style.width = `${ayur.vata_percentage}%`;

    $('#pitta-pct').textContent = `${ayur.pitta_percentage}%`;
    $('#pitta-fill').style.width = `${ayur.pitta_percentage}%`;

    $('#kapha-pct').textContent = `${ayur.kapha_percentage}%`;
    $('#kapha-fill').style.width = `${ayur.kapha_percentage}%`;

    $('#ayur-vulnerabilities-text').textContent = isTa ? ayur.anatomical_vulnerabilities_ta : ayur.anatomical_vulnerabilities_en;
    $('#ayur-lifestyle-text').textContent = isTa ? ayur.lifestyle_guidance_ta : ayur.lifestyle_guidance_en;
  }

  // Chapter 11: Ashtakavarga Kakshya Precision Transits
  const kt = pred.kakshya_transits;
  if (kt) {
    if (kt.saturn) {
      const sat = kt.saturn;
      $('#kakshya-sat-badge').textContent = sat.current_degree;
      $('#kakshya-sat-badge').className = `status-pill ${sat.current_kakshya.has_bindu ? 'success' : 'danger'}`;
      $('#kakshya-sat-summary').textContent = isTa ? sat.summary_ta : sat.summary_en;

      const sBody = $('#kakshya-sat-tbody');
      sBody.replaceChildren();
      (sat.kakshya_timeline || []).forEach(row => {
        const tr = document.createElement('tr');
        if (row.is_current) tr.className = 'active-period';
        tr.innerHTML = `
          <td><strong>${row.kakshya_num}</strong> ${row.is_current ? `<span class="status-pill success" style="font-size:9px">${txt('Active', 'நடப்பில்')}</span>` : ''}</td>
          <td>${row.range_str}</td>
          <td><strong>${isTa ? row.lord_ta : row.lord}</strong></td>
          <td>${row.has_bindu ? `<span style="color:#2ecc71; font-weight:700">${txt('1 Bindu', '1 பரல்')}</span>` : `<span style="color:#e63946">${txt('0 Bindu', '0 பரல்')}</span>`}</td>
          <td><span class="dignity-badge ${row.has_bindu ? 'own-sign' : 'enemy'}">${isTa ? row.status_ta : row.status_en}</span></td>
        `;
        sBody.append(tr);
      });
    }

    if (kt.jupiter) {
      const jup = kt.jupiter;
      $('#kakshya-jup-badge').textContent = jup.current_degree;
      $('#kakshya-jup-badge').className = `status-pill ${jup.current_kakshya.has_bindu ? 'success' : 'neutral'}`;
      $('#kakshya-jup-summary').textContent = isTa ? jup.summary_ta : jup.summary_en;

      const jBody = $('#kakshya-jup-tbody');
      jBody.replaceChildren();
      (jup.kakshya_timeline || []).forEach(row => {
        const tr = document.createElement('tr');
        if (row.is_current) tr.className = 'active-period';
        tr.innerHTML = `
          <td><strong>${row.kakshya_num}</strong> ${row.is_current ? `<span class="status-pill success" style="font-size:9px">${txt('Active', 'நடப்பில்')}</span>` : ''}</td>
          <td>${row.range_str}</td>
          <td><strong>${isTa ? row.lord_ta : row.lord}</strong></td>
          <td>${row.has_bindu ? `<span style="color:#2ecc71; font-weight:700">${txt('1 Bindu', '1 பரல்')}</span>` : `<span style="color:#e63946">${txt('0 Bindu', '0 பரல்')}</span>`}</td>
          <td><span class="dignity-badge ${row.has_bindu ? 'exalted' : 'neutral'}">${isTa ? row.status_ta : row.status_en}</span></td>
        `;
        jBody.append(tr);
      });
    }
  }

  // Chapter 12: Shadbala Planetary Strengths & Potency
  const SHADBALA_PARTS = [
    ['uchcha', 'Uchcha', 'உச்ச'], ['saptavargaja', 'Saptavargaja', 'சப்தவர்க்கஜ'], ['ojayugma', 'Ojayugma', 'ஓஜயுக்ம'],
    ['kendra', 'Kendradi', 'கேந்திராதி'], ['drekkana', 'Drekkana', 'திரேக்காண'], ['nathonnatha', 'Nathonnatha', 'நதோன்னத'],
    ['paksha', 'Paksha', 'பக்ஷ'], ['tribhaga', 'Tribhaga', 'திரிபாக'], ['abda', 'Abda', 'அப்த'], ['masa', 'Masa', 'மாச'],
    ['vara', 'Vara', 'வார'], ['hora', 'Hora', 'ஹோரா'], ['ayana', 'Ayana', 'அயன'], ['yuddha', 'Yuddha', 'யுத்த'],
    ['cheshta', 'Cheshta', 'சேஷ்டா'], ['drik', 'Drik', 'திருக்']
  ];
  const sb = pred.shadbala;
  if (sb) {
    $('#shadbala-master-summary').textContent = isTa ? sb.summary_ta : sb.summary_en;
    if (sb.dominant_planet) {
      const dp = sb.dominant_planet;
      $('#shadbala-dom-planet').textContent = `${isTa ? dp.planet_ta : dp.planet} (${dp.strength_ratio}x)`;
      $('#shadbala-dom-sub').textContent = isTa ? dp.theme_ta : dp.theme_en;
    }
    if (sb.vulnerable_planet) {
      const vp = sb.vulnerable_planet;
      $('#shadbala-vuln-planet').textContent = `${isTa ? vp.planet_ta : vp.planet} (${vp.strength_ratio}x)`;
      $('#shadbala-vuln-sub').textContent = isTa ? vp.theme_ta : vp.theme_en;
    }

    const sbGrid = $('#shadbala-cards-grid');
    if (sbGrid && sb.planets) {
      sbGrid.replaceChildren();
      sb.planets.forEach(p => {
        const card = document.createElement('div');
        card.className = 'cosmic-card reading-card';
        const pInfo = PLANET_NAMES[p.planet] || { en: p.planet, ta: p.planet, color: '#e5c378' };
        const label = isTa ? p.planet_ta : p.planet;
        const reading = isTa ? p.reading_ta : p.reading_en;
        const statusBadge = p.is_adequate
          ? `<span class="status-pill success">${isTa ? 'சுப பலம் வாய்ந்தது' : 'Adequate'} (${p.strength_ratio}x)</span>`
          : `<span class="status-pill neutral">${isTa ? 'வளர்ச்சி தேவை' : 'Growth Area'} (${p.strength_ratio}x)</span>`;

        card.innerHTML = `
          <div class="reading-header">
            <span class="bhava-num-badge" style="border-color:${pInfo.color}; color:${pInfo.color}">#${p.rank}</span>
            <div>
              <h3>${esc(label)} — ${p.total_rupas} ${txt('Rupas', 'ரூபம்')} (${p.total_virupas} ${txt('Virupas', 'விரூபம்')})</h3>
              <small class="muted">${isTa ? 'தேவை' : 'Required'}: ${p.min_required_rupas} ${txt('Rupas', 'ரூபம்')} · ${txt(`Rank ${p.rank} of 7`, `7-ல் ${p.rank}-வது இடம்`)}</small>
            </div>
          </div>
          <div class="timing-score-bar" style="margin:8px 0;">
            <small class="muted">${isTa ? 'பலம் விகிதம்' : 'Strength Ratio'}:</small>
            <div class="timing-track" style="flex:1; margin:0 8px;">
              <div class="timing-fill" style="width:${Math.min(100, p.strength_ratio * 70)}%; background:${p.is_adequate ? 'var(--gold)' : '#e63946'}"></div>
            </div>
            ${statusBadge}
          </div>
          <div class="bhava-meta-strip" style="font-size:11px;">
            <span class="bhava-meta-pill">${txt('Sthana', 'ஸ்தான')}: <strong>${p.sthana_bala}</strong></span>
            <span class="bhava-meta-pill">${txt('Dig', 'திக்')}: <strong>${p.dig_bala}</strong></span>
            <span class="bhava-meta-pill">${txt('Kaala', 'கால')}: <strong>${p.kaala_bala}</strong></span>
            <span class="bhava-meta-pill">${txt('Chesta', 'சேஷ்டா')}: <strong>${p.chesta_bala}</strong></span>
            <span class="bhava-meta-pill">${txt('Naisargika', 'நைசர்கிக')}: <strong>${p.naisargika_bala}</strong></span>
            <span class="bhava-meta-pill">${txt('Drik', 'திருக்')}: <strong>${p.drik_bala}</strong></span>
          </div>
          <p class="reading-body" style="font-size:12.5px; margin-top:8px;">${esc(reading)}</p>
          ${(p.factors || []).length ? `<ul class="bhava-factors">${p.factors.map(f => `
            <li class="${f.effect > 0 ? 'plus' : 'minus'}">${esc(txt(f.en, f.ta))}</li>`).join('')}
          </ul>` : ''}
          <div class="bhava-meta-strip" style="font-size:11px; margin-top:8px;">
            <span class="bhava-meta-pill">${txt('Ishta Phala', 'இஷ்ட பலன்')}: <strong>${p.ishta_phala}</strong></span>
            <span class="bhava-meta-pill">${txt('Kashta Phala', 'கஷ்ட பலன்')}: <strong>${p.kashta_phala}</strong></span>
          </div>
          ${p.components ? `<details class="shadbala-breakdown">
            <summary>${txt('Component breakdown (virupas)', 'உட்கூறு பலங்கள் (விரூபம்)')}</summary>
            <div class="shadbala-components">${SHADBALA_PARTS.map(([key, en, ta]) => `
              <div><span>${esc(txt(en, ta))}</span><strong>${p.components[key]}</strong></div>`).join('')}
            </div>
          </details>` : ''}
        `;
        sbGrid.append(card);
      });
    }
  }

  // Chapter 13: Krishnamurti Paddhati (KP System) Sub-Lord Analysis
  const kp = pred.kp_system;
  if (kp) {
    const kpGrid = $('#kp-cusp-preds-grid');
    if (kpGrid && kp.cuspal_predictions) {
      kpGrid.replaceChildren();
      Object.values(kp.cuspal_predictions).forEach(cp => {
        const card = document.createElement('div');
        card.className = 'cosmic-card reading-card';
        const title = isTa ? cp.title_ta : cp.title_en;
        const subLord = isTa ? cp.sub_lord_ta : cp.sub_lord;
        const reading = isTa ? cp.reading_ta : cp.reading_en;
        card.innerHTML = `
          <div class="reading-header">
            <span class="reading-icon">🔍</span>
            <div>
              <h3>${esc(title)}</h3>
              <small class="muted">${isTa ? 'உப-அதிபதி' : 'Sub-Lord'}: <strong style="color:var(--gold);">${esc(subLord)}</strong></small>
            </div>
          </div>
          <p class="reading-body" style="font-size:12.5px">${esc(reading)}</p>
        `;
        kpGrid.append(card);
      });
    }

    const cBody = $('#kp-cusps-tbody');
    if (cBody && kp.cusps) {
      cBody.replaceChildren();
      kp.cusps.forEach(c => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><strong>${c.cusp}</strong></td>
          <td>${c.degree_str}</td>
          <td>${isTa ? c.sign_ta : c.sign}</td>
          <td>${isTa ? c.sign_lord_ta : c.sign_lord}</td>
          <td>${starName(c.star_name)} (${isTa ? c.star_lord_ta : c.star_lord})</td>
          <td><strong style="color:var(--gold)">${isTa ? c.sub_lord_ta : c.sub_lord}</strong></td>
        `;
        cBody.append(tr);
      });
    }

    const pBody = $('#kp-planets-tbody');
    if (pBody && kp.planets) {
      pBody.replaceChildren();
      kp.planets.forEach(p => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><strong>${isTa ? p.planet_ta : p.planet}</strong></td>
          <td>${p.degree_str}</td>
          <td>${isTa ? p.sign_ta : p.sign}</td>
          <td>${isTa ? p.sign_lord_ta : p.sign_lord}</td>
          <td>${starName(p.star_name)} (${isTa ? p.star_lord_ta : p.star_lord})</td>
          <td><strong style="color:var(--gold)">${isTa ? p.sub_lord_ta : p.sub_lord}</strong></td>
        `;
        pBody.append(tr);
      });
    }
  }

  // Chapter 14: Bhrigu Nandi Nadi (BNN) Karmic Sutras
  const bnn = pred.bhrigu_nandi_nadi;
  if (bnn) {
    $('#bnn-summary-text').textContent = isTa ? bnn.summary_ta : bnn.summary_en;
    const tRow = $('#bnn-trines-row');
    if (tRow && bnn.trines) {
      tRow.replaceChildren();
      Object.entries(bnn.trines).forEach(([tKey, tData]) => {
        const item = document.createElement('div');
        item.className = 'timing-meta-item';
        const pNames = tData.planets.map(p => isTa ? p.tamil : p.name).join(', ') || (isTa ? 'கிரகங்கள் இல்லை' : 'Empty');
        item.innerHTML = `
          <small>${esc(isTa ? tData.name_ta : tData.name_en)}</small>
          <strong style="font-size:13px; color:var(--text-primary)">${esc(pNames)}</strong>
        `;
        tRow.append(item);
      });
    }

    const sGrid = $('#bnn-sutras-grid');
    if (sGrid && bnn.sutras) {
      sGrid.replaceChildren();
      bnn.sutras.forEach(s => {
        const card = document.createElement('div');
        card.className = 'cosmic-card reading-card';
        const title = isTa ? s.title_ta : s.title_en;
        const desc = isTa ? s.significance_ta : s.significance_en;
        card.innerHTML = `
          <div class="reading-header">
            <span class="reading-icon">📜</span>
            <div>
              <h3 style="color:var(--gold);">${esc(title)}</h3>
              <small class="muted">${isTa ? 'இணைந்த கிரகங்கள்' : 'Associated Grahas'}: ${grahaNames(s.planets, ' + ')}</small>
            </div>
          </div>
          <p class="reading-body" style="font-size:12.5px">${esc(desc)}</p>
        `;
        sGrid.append(card);
      });
    }
  }

  // Chapter 15: Planetary Avasthas & Consciousness States
  const av = pred.avasthas;
  if (av && av.avasthas) {
    const aGrid = $('#avasthas-cards-grid');
    if (aGrid) {
      aGrid.replaceChildren();
      av.avasthas.forEach(a => {
        const card = document.createElement('div');
        card.className = 'cosmic-card reading-card';
        const pInfo = PLANET_NAMES[a.planet] || { en: a.planet, ta: a.planet, color: '#e5c378' };
        const label = isTa ? a.planet_ta : a.planet;
        const bLabel = isTa ? a.baladi_ta : a.baladi;
        const jLabel = isTa ? a.jagradadi_ta : a.jagradadi;
        const interp = isTa ? a.interpretation_ta : a.interpretation_en;

        card.innerHTML = `
          <div class="reading-header">
            <span class="bhava-num-badge" style="border-color:${pInfo.color}; color:${pInfo.color}">${pInfo.short || a.planet.slice(0, 2)}</span>
            <div>
              <h3>${esc(label)} — ${a.degree_str}</h3>
              <small class="muted">${esc(bLabel)} · ${esc(jLabel)}</small>
            </div>
          </div>
          <div class="timing-score-bar" style="margin:8px 0;">
            <small class="muted">${isTa ? 'நடைமுறை பலன் கொடுக்கும் விகிதம்' : 'Fruit Potency'}:</small>
            <div class="timing-track" style="flex:1; margin:0 8px;">
              <div class="timing-fill" style="width:${a.fruit_potency}%; background:${a.fruit_potency >= 75 ? '#2ecc71' : (a.fruit_potency >= 40 ? 'var(--gold)' : '#e63946')}"></div>
            </div>
            <strong style="color:var(--gold); font-size:12px">${a.fruit_potency}%</strong>
          </div>
          <p class="reading-body" style="font-size:12.5px">${esc(interp)}</p>
        `;
        aGrid.append(card);
      });
    }
  }

  // Chapter 16: Birth Nakshatra Pada Reading
  const pada = pred.pada_reading;
  if (pada) {
    $('#pada-element-badge').textContent = isTa ? pada.element_ta : pada.element;
    $('#pada-star-name').textContent = isTa ? pada.tamil_nakshatra : pada.nakshatra;
    $('#pada-num-display').textContent = `${isTa ? 'பாதம்' : 'Pada'} ${pada.pada} (${isTa ? pada.element_ta : pada.element})`;
    $('#pada-nav-sign').textContent = isTa ? pada.navamsa_ta : pada.navamsa_sign;
    $('#pada-nav-lord').textContent = `${isTa ? 'அதிபதி' : 'Lord'}: ${isTa ? pada.pada_lord_ta : pada.pada_lord}`;
    $('#pada-reading-title').textContent = isTa
      ? `${pada.tamil_nakshatra} பாதம் ${pada.pada} வாழ்க்கைப் பலன்கள்`
      : `${pada.nakshatra} Pada ${pada.pada} Destiny Analysis`;
    $('#pada-reading-sub').textContent = isTa
      ? `நவாம்சம்: ${pada.navamsa_ta} · பூத தத்துவம்: ${pada.element_ta}`
      : `Navamsa: ${pada.navamsa_sign} · Element: ${pada.element}`;
    $('#pada-reading-body').textContent = isTa ? pada.reading_ta : pada.reading_en;
  }

  // Chapter 17: Sensitive Sahams
  const sh = pred.sahams;
  if (sh) {
    $('#sahams-birth-type-badge').textContent = isTa ? sh.birth_type_ta : sh.birth_type_en;
    const sGrid = $('#sahams-cards-grid');
    if (sGrid && sh.sahams) {
      sGrid.replaceChildren();
      sh.sahams.forEach(s => {
        const card = document.createElement('div');
        card.className = 'cosmic-card reading-card';
        const name = isTa ? s.name_ta : s.name_en;
        const sign = isTa ? s.tamil_sign : s.sign;
        const kw = isTa ? s.keyword_ta : s.keyword_en;
        const reading = isTa ? s.reading_ta : s.reading_en;

        card.innerHTML = `
          <div class="reading-header">
            <span class="reading-icon">🔮</span>
            <div>
              <h3>${esc(name)}</h3>
              <small class="muted">${sign} ${s.degree_str} · ${isTa ? 'பாவம்' : 'House'} ${s.house} (${esc(kw)})</small>
            </div>
          </div>
          <p class="reading-body" style="font-size:12.5px">${esc(reading)}</p>
        `;
        sGrid.append(card);
      });
    }
  }
}

// Daily Panchangam: fetch the Tamil panchangam for the birth form's location
async function loadDailyPanchangam() {
  const form = $('#birth-form');
  const errorEl = $('#panch-error');
  errorEl.hidden = true;
  const city = form.elements['city']?.value || '';
  const lat = form.elements['latitude']?.value;
  const lon = form.elements['longitude']?.value;
  const tz = form.elements['timezone']?.value || 'Asia/Kolkata';
  $('#panch-location').textContent = `${city || `${lat}, ${lon}`} · ${tz}`;

  const payload = { latitude: lat, longitude: lon, timezone: tz };
  const picked = $('#panch-date').value;
  if (picked) payload.date = picked;
  if (currentChart) {
    payload.natal_nakshatra_index = STARS_EN.indexOf(currentChart.planets.Moon.nakshatra);
    payload.natal_sign_index = currentChart.planets.Moon.sign_index;
  }

  try {
    const resp = await fetch('/api/panchangam', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const panch = await resp.json();
    if (!resp.ok) throw new Error(panch.error || 'Panchangam calculation failed.');
    lastDailyPanchangam = panch;
    populatePanchangamView(panch);
  } catch (err) {
    errorEl.textContent = errorText(err.message);
    errorEl.hidden = false;
  }
}

// Monthly Tamil calendar for the birth form's location
function shiftCalendarMonth(step) {
  const m = calendarMonth.month - 1 + step;
  calendarMonth = { year: calendarMonth.year + Math.floor(m / 12), month: ((m % 12) + 12) % 12 + 1 };
  loadMonthCalendar();
}

async function loadMonthCalendar() {
  const form = $('#birth-form');
  if (!calendarMonth) {
    const picked = $('#panch-date').value;
    const base = picked ? new Date(`${picked}T12:00:00`) : new Date();
    calendarMonth = { year: base.getFullYear(), month: base.getMonth() + 1 };
  }
  try {
    const resp = await fetch('/api/calendar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...calendarMonth,
        latitude: form.elements['latitude']?.value,
        longitude: form.elements['longitude']?.value,
        timezone: form.elements['timezone']?.value || 'Asia/Kolkata'
      })
    });
    const cal = await resp.json();
    if (!resp.ok) throw new Error(cal.error || 'Calendar calculation failed.');
    lastCalendar = cal;
    renderMonthCalendar(cal);
  } catch (err) {
    notify(errorText(err.message));
  }
}

const OBSERVANCE_ICONS = {
  amavasai: '🌑', pournami: '🌕', ekadasi: '🙏', pradosham: '🔱', sashti: '🦚',
  sankatahara: '🐘', shivaratri: '🕉', karthigai: '🪔', month_start: '🗓'
};

function renderMonthCalendar(cal) {
  const isTa = currentLang === 'ta';
  const first = new Date(`${cal.days[0].date}T12:00:00`);
  $('#month-cal-label').textContent = first.toLocaleDateString(isTa ? 'ta-IN' : 'en-GB', { month: 'long', year: 'numeric' });
  const headers = VAARAM_SHORT.map(([en, ta]) => `<div class="month-head">${txt(en, ta)}</div>`).join('');
  const blanks = '<div class="month-cell empty"></div>'.repeat(first.getDay());
  const today = new Date().toLocaleDateString('en-CA');
  const cells = cal.days.map(d => `
    <div class="month-cell${d.date === today ? ' today' : ''}${d.observances.length ? ' has-obs' : ''}">
      <div class="month-cell-top">
        <strong>${Number(d.date.slice(8))}</strong>
        <small>${esc(txt(`${d.tamil_month.slice(0, 3)} ${d.tamil_day}`, `${d.tamil_month_ta} ${d.tamil_day}`))}</small>
      </div>
      <small class="month-cell-anga">${esc(txt(d.tithi_name, d.tithi_ta))} · ${esc(txt(d.nakshatra, d.nakshatra_ta))}</small>
      <div class="month-cell-obs">${d.observances.map(o => `<span title="${esc(txt(o.en, o.ta))}">${OBSERVANCE_ICONS[o.key]}</span>`).join('')}</div>
    </div>`).join('');
  $('#month-grid').innerHTML = headers + blanks + cells;

  const listed = cal.days.flatMap(d => d.observances.map(o => ({ d, o })));
  $('#month-observances').innerHTML = listed.map(({ d, o }) => `
    <div class="month-obs-row">
      <span>${OBSERVANCE_ICONS[o.key]} ${esc(txt(o.en, o.ta))}</span>
      <span>${new Date(`${d.date}T12:00:00`).toLocaleDateString(isTa ? 'ta-IN' : 'en-GB', { weekday: 'short', day: 'numeric', month: 'short' })}</span>
    </div>`).join('') || `<p class="muted">${txt('No observances this month.', 'இம்மாதம் விரத நாட்கள் இல்லை.')}</p>`;
}

// "until HH:MM", with the date when the anga runs past the panchangam's day
function untilLabel(endIso, dayIso) {
  if (!endIso) return '';
  const time = clockTime(endIso);
  const sameDay = endIso.slice(0, 10) === dayIso;
  const date = new Date(`${endIso.slice(0, 10)}T00:00:00`);
  const dayText = date.toLocaleDateString(currentLang === 'ta' ? 'ta-IN' : 'en-GB', { day: 'numeric', month: 'short' });
  if (currentLang === 'ta') return sameDay ? `${time} வரை` : `${dayText} ${time} வரை`;
  return sameDay ? `until ${time}` : `until ${time}, ${dayText}`;
}

function populatePanchangamView(panch) {
  if (!panch) return;
  const isTa = currentLang === 'ta';
  const ends = panch.ends_local || {};
  const day = panch.local_date;
  const tc = panch.tamil_calendar;

  if (tc) {
    $('#panch-tamil-date').textContent = isTa
      ? `${tc.month_ta} ${tc.day}, ${panch.vaaram.ta}`
      : `${tc.month} ${tc.day} (${tc.month_ta} ${tc.day}), ${panch.vaaram.en}`;
    $('#panch-tamil-year').textContent = isTa
      ? `${tc.year_ta} வருடம் · ${day}`
      : `${tc.year} year (${tc.year_ta}), #${tc.year_number} of the 60-year cycle · ${day}`;
  }
  if (panch.soolam) {
    const sl = panch.soolam;
    $('#panch-soolam').textContent = isTa ? sl.direction_ta : sl.direction;
    $('#panch-parigaram').textContent = isTa ? `பரிகாரம்: ${sl.parigaram_ta}` : `Parigaram (remedy): ${sl.parigaram}`;
  }
  if (panch.chandrashtamam) {
    const ch = panch.chandrashtamam;
    $('#panch-chandrashtamam').textContent = isTa ? `${ch.sign_ta} ராசி` : `${ch.sign} (${ch.sign_ta}) Rasi`;
    $('#panch-chandrashtamam-stars').textContent = ch.stars.map(st => isTa ? st.ta : st.en).join(', ');
  }

  const when = panch.moment_local ? `${panch.moment_local.slice(0, 10)} ${clockTime(panch.moment_local)}` : day;
  $('#panch-moment').textContent = isTa
    ? `${when} நிலவரப்படி அங்கங்களும் அவை முடியும் நேரமும்`
    : `Angas prevailing at ${when}, with the local time each one ends`;

  if (panch.vaaram) {
    $('#panch-vaaram').textContent = isTa ? panch.vaaram.ta : panch.vaaram.en;
    $('#panch-vaaram-sub').textContent = isTa ? panch.vaaram.en : panch.vaaram.ta;
  }
  $('#panch-tithi').textContent = `${tithiLabel(panch.tithi_name)} (${panch.tithi})`;
  $('#panch-paksha').textContent = `${pakshaLabel(panch.paksha)} · ${untilLabel(ends.tithi, day)}`;

  $('#panch-nakshatra').textContent = isTa ? panch.tamil_nakshatra : `${panch.nakshatra} (${panch.tamil_nakshatra})`;
  $('#panch-pada').textContent = `${isTa ? 'பாதம்' : 'Pada'} ${panch.pada} · ${untilLabel(ends.nakshatra, day)}`;

  $('#panch-yoga').textContent = `${nityaYogaLabel(panch.yoga_name)} (${panch.yoga_number})`;
  $('#panch-yoga-nature').textContent = `${panch.yoga_auspiciousness === 'Auspicious' ? txt('Auspicious', 'சுபம்') : txt('Inauspicious', 'அசுபம்')} · ${untilLabel(ends.yoga, day)}`;

  $('#panch-karana').textContent = karanaLabel(panch.karana_name);
  $('#panch-karana-type').textContent = untilLabel(ends.karana, day);

  // Older payloads (a chart's birth panchanga) only carry UTC timings
  const local = key => panch[`${key}_local`] || `${panch[`${key}_utc`]} UTC`;
  $('#panch-abhijit').textContent = local('abhijit_muhurtham');
  $('#panch-rahu').textContent = local('rahu_kalam');
  $('#panch-yama').textContent = local('yamagandam');
  $('#panch-gulika').textContent = local('gulika_kalam');
  $('#panch-sun-times').textContent = `${local('sunrise')} – ${local('sunset')}`;
  $('#panch-tz').textContent = isTa
    ? `${panch.timezone} · பகல் ${panch.day_length_hours} மணி`
    : `${panch.timezone} · day length ${panch.day_length_hours} h`;

  renderHoraTable(panch.horas);
  renderGowriTable(panch.gowri);
  renderPersonalBalam(panch.personal);
}

// Date and clock time of an ISO timestamp in the chart location's timezone, e.g. "3 Jun 2027, 05:28"
function formatLocalDateTime(iso) {
  return new Date(iso).toLocaleString(currentLang === 'ta' ? 'ta-IN' : 'en-GB', {
    timeZone: currentChart?.profile?.timezone || undefined,
    day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit', hour12: false
  });
}

// Gochara (transits today) and upcoming Peyarchi, on the Predictions transit tab
function renderGochara() {
  const g = currentChart?.gochara;
  if (!g) return;
  const isTa = currentLang === 'ta';
  const houseLabel = h => isTa ? `${h}-ம் இடம்` : `House ${h}`;
  const planetLabel = n => isTa ? PLANET_NAMES[n].ta : PLANET_NAMES[n].en;

  $('#peyarchi-tbody').innerHTML = g.peyarchi.map(pe => `
    <tr>
      <td><strong>${planetLabel(pe.planet)}</strong></td>
      <td>${esc(formatLocalDateTime(pe.date))}</td>
      <td>${esc(isTa ? `${pe.from_tamil} → ${pe.to_tamil}` : `${pe.from_sign} → ${pe.to_sign}`)}</td>
      <td>${houseLabel(pe.house_from_moon)}</td>
    </tr>
  `).join('');

  renderSaturnCycles(g.saturn_cycles);
  $('#gochara-computed-at').textContent = isTa
    ? `${formatLocalDateTime(g.computed_at)} நிலவரப்படி · சந்திர ராசியிலிருந்து`
    : `As of ${formatLocalDateTime(g.computed_at)} · counted from the Moon sign`;
  $('#gochara-tbody').innerHTML = Object.entries(g.planets).map(([name, t]) => {
    const bindus = t.bindus === null ? '—'
      : `<span class="status-pill ${t.bindus >= 5 ? 'success' : (t.bindus >= 4 ? 'neutral' : 'danger')}">${t.bindus} / 8</span>`;
    const result = t.favourable ? (isTa ? 'சுபம்' : 'Favourable') : (isTa ? 'அசுபம்' : 'Unfavourable');
    const retro = t.retrograde ? (isTa ? ' (வ)' : ' ᴿ') : '';
    return `
      <tr>
        <td><strong>${planetLabel(name)}${retro}</strong></td>
        <td>${esc(isTa ? t.tamil : t.sign)}</td>
        <td>${formatDegrees(t.degree)}</td>
        <td>${houseLabel(t.house_from_moon)}</td>
        <td>${bindus}</td>
        <td><span class="status-pill ${t.favourable ? 'success' : 'neutral'}">${result}</span></td>
      </tr>`;
  }).join('');
}

const SATURN_CYCLE_LABELS = {
  sade_sati: ['Ezharai Sani (Sade Sati)', 'ஏழரைச் சனி'],
  ardhashtama: ['Ardhashtama Sani (4th)', 'அர்த்தாஷ்டமச் சனி (4-ம் இடம்)'],
  kandaka: ['Kandaka Sani (7th)', 'கண்டச் சனி (7-ம் இடம்)'],
  ashtama: ['Ashtama Sani (8th)', 'அஷ்டமச் சனி (8-ம் இடம்)']
};
const SADE_SATI_PHASES = {
  1: ['Rising (12th)', 'விரயச் சனி (12)'],
  2: ['Janma (1st)', 'ஜென்மச் சனி (1)'],
  3: ['Setting (2nd)', 'பாதச் சனி (2)']
};

function renderSaturnCycles(cycles) {
  const tbody = $('#saturn-cycles-tbody');
  if (!tbody || !cycles) return;
  tbody.innerHTML = cycles.map(c => {
    const [en, ta] = SATURN_CYCLE_LABELS[c.kind];
    const phases = c.phases.map(ph => {
      const [pen, pta] = SADE_SATI_PHASES[ph.phase];
      return `<div><small>${txt(pen, pta)}: ${localDate(ph.start)} → ${localDate(ph.end)}</small></div>`;
    }).join('') || '—';
    return `
      <tr class="${c.active ? 'active-period' : ''}">
        <td><strong>${txt(en, ta)}</strong>${c.active ? ` <span class="status-pill danger">${txt('Now', 'நடப்பில்')}</span>` : ''}</td>
        <td>${c.from_birth ? txt('from birth', 'பிறப்பு முதல்') : localDate(c.start)} → ${localDate(c.end)}</td>
        <td>${c.age_start < 0 ? 0 : c.age_start}</td>
        <td>${phases}</td>
      </tr>`;
  }).join('');
}

function renderHoraTable(horas) {
  const grid = $('#hora-grid');
  if (!grid || !horas) return;
  const isTa = currentLang === 'ta';
  grid.innerHTML = horas.map(h => `
    <div class="hora-item ${h.auspicious ? 'auspicious' : 'inauspicious'}${h.current ? ' current' : ''}">
      <span class="hora-time">${clockTime(h.start_local)}–${clockTime(h.end_local)}</span>
      <strong>${esc(isTa ? `${h.lord_ta} ஓரை` : `${h.lord} Hora`)}</strong>
      <small>${h.daytime ? (isTa ? 'பகல்' : 'Day') : (isTa ? 'இரவு' : 'Night')}${h.current ? (isTa ? ' · இப்போது' : ' · now') : ''}</small>
    </div>
  `).join('');
}

function renderGowriTable(gowri) {
  const grid = $('#gowri-grid');
  if (!grid || !gowri) return;
  grid.innerHTML = gowri.map(g => `
    <div class="hora-item ${g.good ? 'auspicious' : 'inauspicious'}${g.current ? ' current' : ''}">
      <span class="hora-time">${clockTime(g.start_local)}–${clockTime(g.end_local)}</span>
      <strong>${esc(txt(g.name, g.name_ta))}</strong>
      <small>${g.daytime ? txt('Day', 'பகல்') : txt('Night', 'இரவு')} · ${g.good ? txt('Nalla Neram', 'நல்ல நேரம்') : txt('Avoid', 'தவிர்க்கவும்')}${g.current ? txt(' · now', ' · இப்போது') : ''}</small>
    </div>
  `).join('');
}

// Upcoming Chandrashtamam periods and the Nakshatra birthday from the loaded chart
function renderUpcomingDates() {
  const up = currentChart?.south_indian?.upcoming;
  const isTa = currentLang === 'ta';
  if (!up) return;
  const ch = up.chandrashtamam;
  $('#panch-next-chandrashtamam').innerHTML = ch.periods.map(pr => `
    <div class="${pr.active ? 'upcoming-active' : ''}">${esc(formatLocalDateTime(pr.start_local))} → ${esc(formatLocalDateTime(pr.end_local))}</div>
  `).join('');

  const sb = up.star_birthday;
  if (sb) {
    $('#panch-star-birthday').textContent = sb.dates
      .map(d => new Date(`${d}T00:00:00`).toLocaleDateString(isTa ? 'ta-IN' : 'en-GB', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' }))
      .join(isTa ? ' மற்றும் ' : ' and ');
    $('#panch-star-birthday-sub').textContent = isTa
      ? `${sb.month_ta} மாதம், ${sb.star_ta} நட்சத்திரம் சூரிய உதயத்தில்`
      : `${sb.star} at sunrise in the Tamil month of ${sb.month}`;
  } else {
    $('#panch-star-birthday').textContent = '—';
    $('#panch-star-birthday-sub').textContent = '';
  }
}

function renderPersonalBalam(personal) {
  const card = $('#panch-personal-card');
  card.hidden = !(personal && currentChart);
  if (card.hidden) return;
  const isTa = currentLang === 'ta';
  const tara = personal.tara;
  const cb = personal.chandra_balam;
  const moon = currentChart.planets.Moon;
  $('#panch-personal-for').textContent = isTa
    ? `${currentChart.profile.name} · ${moon.tamil_nakshatra} · ${moon.tamil} ராசி`
    : `${currentChart.profile.name} · ${moon.nakshatra} · ${moon.sign} Rasi`;

  $('#panch-tara').textContent = isTa ? `${tara.name_ta} தாரை` : `${tara.name} Tara`;
  $('#panch-tara-sub').textContent = isTa
    ? `ஜன்ம நட்சத்திரத்திலிருந்து ${tara.count}-வது நட்சத்திரம்`
    : `Today's star is ${tara.count} from the birth star · ${tara.quality === 'good' ? 'favourable' : (tara.quality === 'bad' ? 'unfavourable' : 'mixed')}`;

  $('#panch-chandra').textContent = isTa ? `${cb.house}-ம் இடத்தில் சந்திரன்` : `Moon in house ${cb.house}`;
  $('#panch-chandra-sub').textContent = personal.chandrashtamam
    ? (isTa ? 'சந்திராஷ்டமம்: முக்கிய முடிவுகளைத் தவிர்க்கவும்' : 'Chandrashtamam: postpone important decisions')
    : (cb.favourable ? (isTa ? 'சந்திர பலம் உண்டு' : 'Favourable Chandra Balam') : (isTa ? 'சந்திர பலம் குறைவு' : 'Weak Chandra Balam'));

  const good = tara.quality === 'good' && cb.favourable;
  const bad = personal.chandrashtamam || (tara.quality === 'bad' && !cb.favourable);
  const status = $('#panch-personal-status');
  status.className = `status-pill ${good ? 'success' : (bad ? 'danger' : 'neutral')}`;
  status.textContent = good ? (isTa ? 'சாதகமான நாள்' : 'Favourable day')
    : (bad ? (isTa ? 'கவனம் தேவை' : 'Take care') : (isTa ? 'கலப்பு' : 'Mixed'));
  renderUpcomingDates();
}

// Horoscope Matching Tool
function populateMatchDropdowns() {
  const gStar = $('#match-girl-star');
  const bStar = $('#match-boy-star');
  const gSign = $('#match-girl-sign');
  const bSign = $('#match-boy-sign');

  if (gStar && !gStar.options.length) {
    STARS_EN.forEach((s, i) => {
      gStar.add(new Option('', i));
      bStar.add(new Option('', i));
    });
    SIGNS_EN.forEach((s, i) => {
      gSign.add(new Option('', i));
      bSign.add(new Option('', i));
    });
  }
  [gStar, bStar].forEach(sel => [...(sel?.options || [])].forEach((o, i) => {
    o.textContent = txt(`${i + 1}. ${STARS_EN[i]} (${STARS_TA[i]})`, `${i + 1}. ${STARS_TA[i]} (${STARS_EN[i]})`);
  }));
  [gSign, bSign].forEach(sel => [...(sel?.options || [])].forEach((o, i) => {
    o.textContent = txt(`${SIGNS_EN[i]} (${SIGNS_TA[i]})`, `${SIGNS_TA[i]} (${SIGNS_EN[i]})`);
  }));

  // Populate profiles
  const profiles = getSavedProfiles();
  const gProf = $('#match-girl-profile');
  const bProf = $('#match-boy-profile');
  const isTa = currentLang === 'ta';

  if (gProf && bProf) {
    const defaultText = isTa ? '-- நபர் அல்லது கைமுறை தேர்வு --' : '-- Choose Profile or Manual --';
    gProf.innerHTML = `<option value="">${defaultText}</option>`;
    bProf.innerHTML = `<option value="">${defaultText}</option>`;

    profiles.forEach((p, idx) => {
      const starText = isTa ? (p.nakshatra_ta || p.nakshatra || '') : (p.nakshatra || '');
      const signText = isTa ? (p.moon_sign_ta || p.moon_sign || '') : (p.moon_sign || '');
      const astroLabel = starText && signText ? ` (${starText} · ${signText})` : (starText ? ` (${starText})` : '');
      const optText = `${p.name}${astroLabel}`;

      gProf.add(new Option(optText, idx));
      bProf.add(new Option(optText, idx));
    });

    gProf.onchange = () => {
      if (gProf.value === '') return;
      const p = profiles[gProf.value];
      if (p && p.nakshatra_idx !== undefined && p.sign_idx !== undefined) {
        gStar.value = p.nakshatra_idx;
        gSign.value = p.sign_idx;
      }
    };
    bProf.onchange = () => {
      if (bProf.value === '') return;
      const p = profiles[bProf.value];
      if (p && p.nakshatra_idx !== undefined && p.sign_idx !== undefined) {
        bStar.value = p.nakshatra_idx;
        bSign.value = p.sign_idx;
      }
    };
  }
}

// Full birth details let the server compare Chevvai Dosham and Papa Samyam;
// fall back to star and sign when no profile is chosen or the selects were changed by hand.
function matchCandidate(side) {
  const star = parseInt($(`#match-${side}-star`).value, 10);
  const sign = parseInt($(`#match-${side}-sign`).value, 10);
  const profIdx = $(`#match-${side}-profile`).value;
  const prof = profIdx === '' ? null : getSavedProfiles()[profIdx];
  if (prof && prof.date && prof.time && prof.nakshatra_idx === star && prof.sign_idx === sign) {
    const { name, date, time, timezone, latitude, longitude, ayanamsa, fold, city } = prof;
    return { name, date, time, timezone, latitude, longitude, ayanamsa, fold, city };
  }
  return { nakshatra_index: star, sign_index: sign };
}

async function runHoroscopeMatch() {
  const payload = {
    girl: matchCandidate('girl'),
    boy: matchCandidate('boy')
  };

  try {
    const resp = await fetch('/api/match', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const match = await resp.json();
    if (!resp.ok) throw new Error(match.error);
    lastMatch = match;
    syncProfilesFromMatch(match);
    renderMatchResult(match);
    notify(txt('Horoscope compatibility calculated', 'திருமணப் பொருத்தம் கணிக்கப்பட்டது'));
  } catch (err) {
    notify(`${txt('Matching error', 'பொருத்தப் பிழை')}: ${errorText(err.message)}`);
  }
}

// A full-chart match computes each partner's true star and sign; store them on the
// matching saved profile and selects so older or hand-entered values are corrected.
function syncProfilesFromMatch(match) {
  const list = getSavedProfiles();
  let changed = false;
  [['bride', 'girl'], ['groom', 'boy']].forEach(([side, prefix]) => {
    const info = match[side];
    if (!info?.name) return;
    const prof = list.find(p => p.name.toLowerCase() === info.name.toLowerCase());
    if (prof && (prof.nakshatra_idx !== info.nakshatra_index || prof.sign_idx !== info.sign_index || prof.pada !== info.pada)) {
      Object.assign(prof, {
        nakshatra: info.nakshatra, nakshatra_ta: info.nakshatra_ta, nakshatra_idx: info.nakshatra_index,
        moon_sign: info.sign, moon_sign_ta: info.sign_ta, sign_idx: info.sign_index, pada: info.pada,
        lagna: info.lagna, lagna_ta: info.lagna_ta
      });
      changed = true;
    }
    $(`#match-${prefix}-star`).value = info.nakshatra_index;
    $(`#match-${prefix}-sign`).value = info.sign_index;
  });
  if (!changed) return;
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(list));
  } catch (e) {}
  const [gSel, bSel] = [$('#match-girl-profile').value, $('#match-boy-profile').value];
  populateMatchDropdowns();
  $('#match-girl-profile').value = gSel;
  $('#match-boy-profile').value = bSel;
  renderProfilesList();
}

const GUNA_LABELS = [
  ['varna', 1, 'Varna (Work & Spiritual Nature)', 'வர்ணம் (தொழில் & ஆன்மீக இயல்பு)'],
  ['vashya', 2, 'Vashya (Mutual Magnetism)', 'வசியம் (பரஸ்பர ஈர்ப்பு)'],
  ['tara', 3, 'Tara (Health & Longevity)', 'தாரை (ஆரோக்கியம் & ஆயுள்)'],
  ['yoni', 4, 'Yoni (Physical Harmony)', 'யோனி (உடல் ஒற்றுமை)'],
  ['graha_maitri', 5, 'Graha Maitri (Mental Friendship)', 'கிரக மைத்ரி (மன நட்பு)'],
  ['gana', 6, 'Gana (Temperament Alignment)', 'கணம் (குண ஒற்றுமை)'],
  ['bhakoot', 7, 'Bhakoot (Family Fortune)', 'பகூட் (குடும்ப அதிர்ஷ்டம்)'],
  ['nadi', 8, 'Nadi (Genetic / Health Affinity)', 'நாடி (மரபு & ஆரோக்கிய ஒற்றுமை)']
];

function renderMatchResult(match) {
  const g = match.guna_milan;
  $('#match-results-container').hidden = false;
  $('#match-score-num').textContent = g.total_score;
  $('#match-verdict-title').textContent = txt(match.verdict, match.verdict_ta);
  const notes = (match.verdict_notes || []).map(n => txt(n.en, n.ta)).join('; ');
  $('#match-verdict-desc').textContent = txt(
    `${match.passed_count} of 10 Poruthams passed. Guna score: ${g.total_score} of 36.`,
    `10-ல் ${match.passed_count} பொருத்தங்கள் உள்ளன. குண மதிப்பெண்: 36-ல் ${g.total_score}.`) +
    (notes ? txt(` Verdict lowered: ${notes}.`, ` முடிவு குறைக்கப்பட்டது: ${notes}.`) : '');

  const rajjuBadge = $('#match-rajju-badge');
  rajjuBadge.textContent = match.rajju_agreement
    ? txt('Rajju Match: Harmonious (Passed)', 'ரஜ்ஜு பொருத்தம் உண்டு')
    : txt('Rajju Dosha: Inauspicious (Same Rajju)', 'ரஜ்ஜு தோஷம்: ஒரே ரஜ்ஜு');
  rajjuBadge.className = `badge ${match.rajju_agreement ? 'status-pill success' : 'status-pill danger'}`;
  $('#match-porutham-count').textContent = txt(`${match.passed_count} of 10 Passed`, `10-ல் ${match.passed_count} பொருத்தம்`);

  // 10 Poruthams table: the other language's name sits underneath
  const tbody = $('#poruthams-tbody');
  tbody.replaceChildren();
  match.poruthams.forEach(p => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><strong>${txt(p.name, p.tamil)}</strong> <small style="display:block;color:var(--gold-dim)">${txt(p.tamil, p.name)}</small></td>
      <td>${esc(txt(p.description, p.description_ta))}</td>
      <td><span class="status-pill ${p.passed ? 'success' : 'danger'}">${p.passed ? txt('Passed ✔', 'உண்டு ✔') : txt('Not Matched ✖', 'இல்லை ✖')}</span></td>
      <td>${p.points} / ${p.max_points}</td>
    `;
    tbody.append(tr);
  });

  // 8 Gunas Grid
  const gunasGrid = $('#gunas-grid');
  gunasGrid.replaceChildren();
  GUNA_LABELS.forEach(([key, max, en, ta]) => {
    const card = document.createElement('div');
    card.className = 'guna-card';
    card.innerHTML = `
      <small style="font-size:10px;color:var(--text-muted)">${txt(en, ta)}</small>
      <div style="font-size:18px;font-weight:700;color:var(--gold);margin:4px 0">${g[key]} / ${max}</div>
    `;
    gunasGrid.append(card);
  });
  renderDoshaSamyam(match);
}

// Dasa Sandhi: both Maha Dasas changing within about six months of each other
function dasaSandhiRows(sandhi) {
  if (!sandhi) return [];
  const label = txt('Dasa Sandhi', 'தசா சந்தி');
  if (!sandhi.present) {
    return [[label, '—', '—', `<span class="status-pill success">${txt(`None in the next ${sandhi.horizon_years} years ✔`, `அடுத்த ${sandhi.horizon_years} ஆண்டுகளில் இல்லை ✔`)}</span>`]];
  }
  return sandhi.conflicts.map(c => [
    label,
    `${grahaName(c.bride_from)} → ${grahaName(c.bride_to)}<br><small>${localDate(c.bride_date)}</small>`,
    `${grahaName(c.groom_from)} → ${grahaName(c.groom_to)}<br><small>${localDate(c.groom_date)}</small>`,
    `<span class="status-pill danger">${txt(`${c.gap_days} days apart ✖`, `${c.gap_days} நாள் இடைவெளி ✖`)}</span>`
  ]);
}

function renderDoshaSamyam(match) {
  const card = $('#dosha-samyam-card');
  const hint = $('#dosha-samyam-hint');
  const ds = match.dosha_samyam;
  const isTa = currentLang === 'ta';
  card.hidden = !ds;
  hint.hidden = !!ds;
  if (!ds) {
    hint.textContent = isTa
      ? 'செவ்வாய் தோஷ சாம்யம் மற்றும் பாப சாம்யம் ஒப்பிட, முழு பிறப்பு விவரங்களுடன் சேமிக்கப்பட்ட ஜாதகங்களைத் தேர்வு செய்யவும்.'
      : 'Choose saved profiles with full birth details to compare Chevvai Dosham and Papa Samyam as well.';
    return;
  }

  const chevvaiText = c => !c.present ? (isTa ? 'இல்லை' : 'None')
    : (c.cancelled ? (isTa ? 'நிவர்த்தி' : 'Cancelled') : (isTa ? `உள்ளது (${c.severity}/3)` : `Present (${c.severity}/3)`));
  const rkText = r => r.present ? (isTa ? 'உள்ளது' : 'Present') : (isTa ? 'இல்லை' : 'None');
  const papaText = pp => `${pp.total} (${pp.breakdown.map(b => b.points).join(' / ')})`;
  const pill = ok => `<span class="status-pill ${ok ? 'success' : 'danger'}">${ok ? (isTa ? 'சமம் ✔' : 'Balanced ✔') : (isTa ? 'சமமில்லை ✖' : 'Unbalanced ✖')}</span>`;
  const rkBalanced = ds.boy.rahu_ketu.present === ds.girl.rahu_ketu.present;

  $('#dosha-samyam-tbody').innerHTML = [
    [isTa ? 'செவ்வாய் தோஷம்' : 'Chevvai Dosham', chevvaiText(ds.girl.chevvai), chevvaiText(ds.boy.chevvai), pill(ds.chevvai_balanced)],
    [isTa ? 'ராகு-கேது தோஷம்' : 'Rahu-Ketu Dosham', rkText(ds.girl.rahu_ketu), rkText(ds.boy.rahu_ketu), pill(rkBalanced)],
    [isTa ? 'பாப புள்ளிகள் (ல / ச / சு)' : 'Papa Points (L / C / S)', papaText(ds.girl.papa), papaText(ds.boy.papa), pill(ds.papa_balanced)],
    ...dasaSandhiRows(ds.dasa_sandhi)
  ].map(([label, girl, boy, state]) => `<tr><td><strong>${label}</strong></td><td>${girl}</td><td>${boy}</td><td>${state}</td></tr>`).join('');

  const status = $('#dosha-samyam-status');
  status.className = `status-pill ${ds.balanced ? 'success' : 'danger'}`;
  status.textContent = ds.balanced ? (isTa ? 'தோஷ சாம்யம் உண்டு' : 'Doshas Balanced') : (isTa ? 'ஜோதிடரை அணுகவும்' : 'Needs Review');
  $('#dosha-samyam-summary').textContent = isTa
    ? 'செவ்வாய் தோஷம் இருவருக்கும் இருக்க வேண்டும் அல்லது இருவருக்கும் இல்லாமல் இருக்க வேண்டும்; பெண்ணின் பாப புள்ளிகள் ஆணின் புள்ளிகளை விட அதிகமாக இருக்கக் கூடாது.'
    : "Chevvai Dosham should be present in both charts or neither, and the bride's Papa points should not exceed the groom's.";
}

// Saved Profiles Vault & Multi-Person Management
function getSavedProfiles() {
  try {
    let p = JSON.parse(localStorage.getItem(STORAGE_KEY));
    if (!p || !Array.isArray(p) || p.length === 0) {
      // Check for legacy migration
      const legacy = JSON.parse(localStorage.getItem(LEGACY_STORAGE_KEY) || 'null');
      if (Array.isArray(legacy) && legacy.length) {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(legacy));
        return legacy;
      }
      // Seed default profiles for immediate out-of-the-box multi-person testing
      localStorage.setItem(STORAGE_KEY, JSON.stringify(DEFAULT_SEED_PROFILES));
      return [...DEFAULT_SEED_PROFILES];
    }
    return p;
  } catch (e) {
    console.warn('LocalStorage access issue:', e);
    return [...DEFAULT_SEED_PROFILES];
  }
}

function populateQuickProfileDropdown(selectedId = null) {
  const select = $('#quick-profile-select');
  if (!select) return;
  const profiles = getSavedProfiles();
  const isTa = currentLang === 'ta';

  select.innerHTML = `<option value="">👤 ${isTa ? '-- நபரைத் தேர்வு செய்க --' : '-- Quick Load Person --'}</option>`;

  profiles.forEach(p => {
    const opt = document.createElement('option');
    opt.value = p.id || p.name;
    const starStr = isTa ? (p.nakshatra_ta || p.nakshatra || '') : (p.nakshatra || '');
    const astroStr = starStr ? ` — ${starStr}` : (p.city ? ` (${p.city})` : '');
    opt.textContent = `${p.name}${astroStr}`;
    select.appendChild(opt);
  });

  if (selectedId) {
    select.value = selectedId;
  }
}

function handleQuickProfileChange(e) {
  const val = e.target.value;
  if (!val) return;
  const profiles = getSavedProfiles();
  const profile = profiles.find(p => (p.id === val || p.name === val));
  if (profile) {
    loadProfileIntoForm(profile);
  }
}

function loadProfileIntoForm(p) {
  if (!p) return;
  const form = $('#birth-form');
  if (!form) return;

  if (form.elements['name']) form.elements['name'].value = p.name || '';
  if (form.elements['date']) form.elements['date'].value = p.date || '';
  if (form.elements['time']) form.elements['time'].value = p.time || '';
  if (form.elements['city']) form.elements['city'].value = p.city || '';
  if (form.elements['latitude']) form.elements['latitude'].value = p.latitude ?? '';
  if (form.elements['longitude']) form.elements['longitude'].value = p.longitude ?? '';
  if (form.elements['timezone']) form.elements['timezone'].value = p.timezone || 'Asia/Kolkata';
  if (form.elements['ayanamsa']) form.elements['ayanamsa'].value = p.ayanamsa || 'Lahiri';
  if (form.elements['fold']) form.elements['fold'].value = p.fold ?? '';

  const qSelect = $('#quick-profile-select');
  if (qSelect) qSelect.value = p.id || p.name;

  // Auto-submit to compute chart immediately
  form.requestSubmit();
  notify(currentLang === 'ta' ? `${p.name} ஜாதகம் கணிக்கப்படுகிறது...` : `Loaded chart for ${p.name}`);
}

function saveCurrentProfile() {
  const form = $('#birth-form');
  if (!form) return;

  const nameInput = form.elements['name'];
  const name = (nameInput ? nameInput.value : '').trim();
  if (!name) {
    notify(currentLang === 'ta' ? 'தயவுசெய்து பெயரை உள்ளிடவும்' : 'Please enter a name first.');
    if (nameInput) nameInput.focus();
    return;
  }

  const date = form.elements['date']?.value || '';
  const time = form.elements['time']?.value || '';
  const city = form.elements['city']?.value || '';
  const lat = parseFloat(form.elements['latitude']?.value || '0');
  const lon = parseFloat(form.elements['longitude']?.value || '0');
  const timezone = form.elements['timezone']?.value || 'Asia/Kolkata';
  const ayanamsa = form.elements['ayanamsa']?.value || 'Lahiri';
  const fold = form.elements['fold']?.value || '';

  const list = getSavedProfiles();
  const existingIndex = list.findIndex(p => p.name.toLowerCase() === name.toLowerCase());

  let nakshatra = '';
  let nakshatra_ta = '';
  let nakshatra_idx = undefined;
  let moon_sign = '';
  let moon_sign_ta = '';
  let sign_idx = undefined;
  let lagna = '';
  let lagna_ta = '';
  let pada = undefined;

  if (currentChart && currentChart.planets && currentChart.profile && currentChart.profile.name === name) {
    const pMoon = currentChart.planets.Moon;
    const pAsc = currentChart.planets.Ascendant;
    if (pMoon) {
      nakshatra = pMoon.nakshatra || '';
      nakshatra_idx = STARS_EN.indexOf(pMoon.nakshatra);
      if (nakshatra_idx >= 0) nakshatra_ta = STARS_TA[nakshatra_idx];
      moon_sign = pMoon.sign || '';
      sign_idx = pMoon.sign_index;
      if (sign_idx !== undefined && sign_idx >= 0) moon_sign_ta = SIGNS_TA[sign_idx];
      pada = pMoon.pada;
    }
    if (pAsc) {
      lagna = pAsc.sign || '';
      if (pAsc.sign_index !== undefined && pAsc.sign_index >= 0) lagna_ta = SIGNS_TA[pAsc.sign_index];
    }
  }

  const profileId = existingIndex >= 0 ? (list[existingIndex].id || crypto.randomUUID()) : crypto.randomUUID();

  const item = {
    id: profileId,
    name,
    date,
    time,
    city,
    latitude: lat,
    longitude: lon,
    timezone,
    ayanamsa,
    fold,
    lagna: lagna || (existingIndex >= 0 ? list[existingIndex].lagna : ''),
    lagna_ta: lagna_ta || (existingIndex >= 0 ? list[existingIndex].lagna_ta : ''),
    moon_sign: moon_sign || (existingIndex >= 0 ? list[existingIndex].moon_sign : ''),
    moon_sign_ta: moon_sign_ta || (existingIndex >= 0 ? list[existingIndex].moon_sign_ta : ''),
    nakshatra: nakshatra || (existingIndex >= 0 ? list[existingIndex].nakshatra : ''),
    nakshatra_ta: nakshatra_ta || (existingIndex >= 0 ? list[existingIndex].nakshatra_ta : ''),
    nakshatra_idx: nakshatra_idx !== undefined ? nakshatra_idx : (existingIndex >= 0 ? list[existingIndex].nakshatra_idx : undefined),
    sign_idx: sign_idx !== undefined ? sign_idx : (existingIndex >= 0 ? list[existingIndex].sign_idx : undefined),
    pada: pada !== undefined ? pada : (existingIndex >= 0 ? list[existingIndex].pada : undefined),
    created_at: existingIndex >= 0 ? (list[existingIndex].created_at || new Date().toISOString()) : new Date().toISOString(),
    updated_at: new Date().toISOString()
  };

  if (existingIndex >= 0) {
    list[existingIndex] = item;
  } else {
    list.unshift(item);
  }

  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(list));
    populateQuickProfileDropdown(item.id);
    renderProfilesList();
    populateMatchDropdowns();
    const msg = currentLang === 'ta'
      ? `'${item.name}' ஜாதகம் வெற்றிகரமாக சேமிக்கப்பட்டது!`
      : `Profile '${item.name}' saved successfully!`;
    notify(msg);
  } catch (err) {
    console.error(err);
    notify(txt('Storage error: please export profiles backup.', 'சேமிப்புப் பிழை: ஜாதகங்களை பேக்கப் எடுக்கவும்.'));
  }
}

function syncCalculatedProfileWithStorage(chartResult) {
  if (!chartResult || !chartResult.profile || !chartResult.planets) return;
  const name = (chartResult.profile.name || '').trim();
  if (!name) return;

  const list = getSavedProfiles();
  const idx = list.findIndex(p => p.name.toLowerCase() === name.toLowerCase());
  if (idx < 0) return;

  const pMoon = chartResult.planets.Moon;
  const pAsc = chartResult.planets.Ascendant;

  if (pMoon) {
    list[idx].nakshatra = pMoon.nakshatra || '';
    const starIdx = STARS_EN.indexOf(pMoon.nakshatra);
    list[idx].nakshatra_idx = starIdx >= 0 ? starIdx : undefined;
    if (starIdx >= 0) list[idx].nakshatra_ta = STARS_TA[starIdx];
    list[idx].moon_sign = pMoon.sign || '';
    list[idx].sign_idx = pMoon.sign_index;
    if (pMoon.sign_index !== undefined && pMoon.sign_index >= 0) list[idx].moon_sign_ta = SIGNS_TA[pMoon.sign_index];
    list[idx].pada = pMoon.pada;
  }

  if (pAsc) {
    list[idx].lagna = pAsc.sign || '';
    if (pAsc.sign_index !== undefined && pAsc.sign_index >= 0) list[idx].lagna_ta = SIGNS_TA[pAsc.sign_index];
  }

  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(list));
    populateQuickProfileDropdown(list[idx].id);
    renderProfilesList();
    populateMatchDropdowns();
  } catch (e) {
    console.warn('Auto-sync profile storage failed:', e);
  }
}

function clearFormForNewPerson() {
  const form = $('#birth-form');
  if (!form) return;

  const nameInput = form.elements['name'];
  if (nameInput) {
    nameInput.value = '';
    nameInput.focus();
  }

  // Set default date to today
  const today = new Date().toISOString().slice(0, 10);
  if (form.elements['date']) form.elements['date'].value = today;
  if (form.elements['time']) form.elements['time'].value = '12:00:00';

  const qSelect = $('#quick-profile-select');
  if (qSelect) qSelect.value = '';

  const msg = currentLang === 'ta'
    ? 'புதிய நபரின் விவரங்களை உள்ளிட தயார்.'
    : 'Form ready for new person details.';
  notify(msg);
}

function clearAllProfiles() {
  const isTa = currentLang === 'ta';
  const confirmMsg = isTa
    ? 'அனைத்து சேமிக்கப்பட்ட ஜாதகங்களையும் நீக்க விரும்புகிறீர்களா? இதை மீண்டும் பெற இயலாது.'
    : 'Are you sure you want to delete all saved profiles? This cannot be undone.';
  if (!window.confirm(confirmMsg)) return;

  localStorage.setItem(STORAGE_KEY, JSON.stringify([]));
  populateQuickProfileDropdown();
  renderProfilesList();
  populateMatchDropdowns();
  notify(isTa ? 'அனைத்து ஜாதகங்களும் நீக்கப்பட்டன.' : 'All profiles cleared.');
}

function deleteProfile(idx) {
  const list = getSavedProfiles();
  if (idx < 0 || idx >= list.length) return;
  const p = list[idx];
  const isTa = currentLang === 'ta';
  if (!window.confirm(`${isTa ? 'இந்த ஜாதகத்தை நீக்க வேண்டுமா:' : 'Delete profile for'} ${p.name}?`)) return;

  list.splice(idx, 1);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(list));
  populateQuickProfileDropdown();
  renderProfilesList();
  populateMatchDropdowns();
  notify(isTa ? `'${p.name}' நீக்கப்பட்டது` : `Deleted '${p.name}'`);
}

function renderProfilesList() {
  const list = getSavedProfiles();
  const q = ($('#profile-search')?.value || '').toLowerCase().trim();
  const grid = $('#profiles-grid');
  const countBadge = $('#profiles-count-badge');
  const isTa = currentLang === 'ta';

  if (countBadge) {
    countBadge.textContent = isTa ? `${list.length} சேமிக்கப்பட்டது` : `${list.length} saved`;
  }

  if (!grid) return;
  grid.replaceChildren();

  const filtered = list.filter(p => {
    if (!q) return true;
    const nameMatch = (p.name || '').toLowerCase().includes(q);
    const cityMatch = (p.city || '').toLowerCase().includes(q);
    const starMatch = (p.nakshatra || '').toLowerCase().includes(q) || (p.nakshatra_ta || '').toLowerCase().includes(q);
    const signMatch = (p.moon_sign || '').toLowerCase().includes(q) || (p.moon_sign_ta || '').toLowerCase().includes(q);
    return nameMatch || cityMatch || starMatch || signMatch;
  });

  if (!filtered.length) {
    grid.innerHTML = `
      <div class="empty-state" style="grid-column:1/-1;min-height:220px;padding:30px;">
        <span style="font-size:36px;margin-bottom:12px;">📁</span>
        <h3 style="margin-bottom:6px;color:var(--text-primary);">${isTa ? 'ஜாதகங்கள் எதுவும் இல்லை' : 'No Profiles Found'}</h3>
        <p class="muted">${isTa ? 'புதிய நபரை சேர்க்க "புதிய நபர்" பொத்தானை அழுத்தவும்.' : 'Click "New Person" to enter birth details and save a chart.'}</p>
      </div>
    `;
    return;
  }

  filtered.forEach(p => {
    const originalIdx = list.indexOf(p);
    const card = document.createElement('div');
    card.className = 'profile-card';

    const initial = (p.name || 'J').charAt(0).toUpperCase();
    const lagnaStr = isTa ? (p.lagna_ta || p.lagna || '—') : (p.lagna || '—');
    const moonStr = isTa ? (p.moon_sign_ta || p.moon_sign || '—') : (p.moon_sign || '—');
    const starStr = isTa ? (p.nakshatra_ta || p.nakshatra || '—') : (p.nakshatra || '—');
    const padaStr = p.pada ? (isTa ? `பாதம் ${p.pada}` : `P${p.pada}`) : '';

    card.innerHTML = `
      <div class="profile-card-header">
        <div class="profile-avatar-initial">${initial}</div>
        <div class="profile-header-meta">
          <h3>${esc(p.name)}</h3>
          <span class="pill-badge" style="font-size:10px;padding:2px 8px;">${esc(p.city || txt('Custom Location', 'தனிப்பயன் இருப்பிடம்'))}</span>
        </div>
      </div>

      <p class="muted" style="font-size:11.5px;margin:6px 0 8px;line-height:1.5;">
        📅 ${esc(p.date)} · ⏰ ${esc(p.time)}<br>
        🌐 ${esc(p.timezone || 'Asia/Kolkata')} · ${esc(ayanamsaLabel(p.ayanamsa || 'Lahiri'))}
      </p>

      <div class="profile-astro-badges">
        <span class="mini-astro-tag lagna-tag" title="${txt('Ascendant', 'லக்னம்')}">
          <span>🌌</span> <strong>${isTa ? 'லக்னம்' : 'Asc'}:</strong> ${esc(lagnaStr)}
        </span>
        <span class="mini-astro-tag moon-tag" title="${txt('Moon Sign / Rasi', 'சந்திர ராசி')}">
          <span>🌙</span> <strong>${isTa ? 'ராசி' : 'Rasi'}:</strong> ${esc(moonStr)}
        </span>
        <span class="mini-astro-tag star-tag" title="${txt('Birth Star / Nakshatra', 'ஜென்ம நட்சத்திரம்')}">
          <span>⭐</span> <strong>${isTa ? 'நட்சத்திரம்' : 'Star'}:</strong> ${esc(starStr)} ${padaStr}
        </span>
      </div>

      <div class="profile-card-actions">
        <button class="action-btn btn-full" data-load="${originalIdx}">
          <span>🪐</span> <span>${isTa ? 'ஜாதகம் திறக்க ↗' : 'Open Chart ↗'}</span>
        </button>
        <button class="action-btn" data-match-boy="${originalIdx}" title="${txt('Use as Boy in Horoscope Compatibility', 'திருமணப் பொருத்தத்தில் மணமகனாகப் பயன்படுத்து')}">
          <span>👦</span> <span>${isTa ? 'மணமகன்' : 'Boy'}</span>
        </button>
        <button class="action-btn" data-match-girl="${originalIdx}" title="${txt('Use as Girl in Horoscope Compatibility', 'திருமணப் பொருத்தத்தில் மணமகளாகப் பயன்படுத்து')}">
          <span>👧</span> <span>${isTa ? 'மணமகள்' : 'Girl'}</span>
        </button>
        <button class="action-btn" data-delete="${originalIdx}" style="color:var(--ruby);grid-column:1/-1;" title="${txt("Delete this person's record", 'இந்த நபரின் ஜாதகத்தை நீக்கு')}">
          <span>🗑️</span> <span>${isTa ? 'நீக்கு' : 'Delete'}</span>
        </button>
      </div>
    `;

    // Open Chart
    card.querySelector('[data-load]').onclick = () => {
      loadProfileIntoForm(p);
      navigatePage('chart');
    };

    // Use as Boy in Matcher
    card.querySelector('[data-match-boy]').onclick = () => {
      navigatePage('matching');
      const bProf = $('#match-boy-profile');
      if (bProf) {
        bProf.value = originalIdx;
        bProf.dispatchEvent(new Event('change'));
      }
      notify(isTa ? `${p.name} மணமகனாக தேர்வு செய்யப்பட்டார்` : `Selected ${p.name} as Boy`);
    };

    // Use as Girl in Matcher
    card.querySelector('[data-match-girl]').onclick = () => {
      navigatePage('matching');
      const gProf = $('#match-girl-profile');
      if (gProf) {
        gProf.value = originalIdx;
        gProf.dispatchEvent(new Event('change'));
      }
      notify(isTa ? `${p.name} மணமகளாக தேர்வு செய்யப்பட்டார்` : `Selected ${p.name} as Girl`);
    };

    // Delete
    card.querySelector('[data-delete]').onclick = () => {
      deleteProfile(originalIdx);
    };

    grid.append(card);
  });
}

function exportProfilesJSON() {
  const profiles = getSavedProfiles();
  const blob = new Blob([JSON.stringify({ version: 2, app: 'JoRoScope', profiles }, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `JoRoScope-Profiles-${new Date().toISOString().slice(0, 10)}.json`;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1500);
  notify(txt('Exported profiles backup', 'ஜாதகங்கள் பேக்கப் எடுக்கப்பட்டது'));
}

async function importProfilesJSON(e) {
  try {
    const file = e.target.files[0];
    if (!file) return;
    const text = await file.text();
    const data = JSON.parse(text);
    if (!Array.isArray(data.profiles)) throw new Error('Invalid JoRoScope backup format.');
    const existing = getSavedProfiles();
    // Merge avoiding duplicate IDs or exact name+date+time matches
    const merged = [...existing];
    let addedCount = 0;

    data.profiles.forEach(newP => {
      const match = merged.some(ep => (ep.id && ep.id === newP.id) || (ep.name.toLowerCase() === (newP.name || '').toLowerCase() && ep.date === newP.date && ep.time === newP.time));
      if (!match) {
        merged.unshift(newP);
        addedCount++;
      }
    });

    localStorage.setItem(STORAGE_KEY, JSON.stringify(merged));
    populateQuickProfileDropdown();
    renderProfilesList();
    populateMatchDropdowns();
    notify(txt(`Imported ${addedCount} new profiles successfully.`, `${addedCount} புதிய ஜாதகங்கள் இறக்குமதி செய்யப்பட்டன.`));
  } catch (err) {
    notify(`${txt('Import error', 'இறக்குமதிப் பிழை')}: ${err.message}`);
  } finally {
    e.target.value = '';
  }
}
