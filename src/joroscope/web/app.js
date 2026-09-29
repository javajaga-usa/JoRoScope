/**
 * JoRoScope — Modern Precision Vedic Astrology
 * Core of the page: shared helpers and constants, state, event wiring, theme and language,
 * the birth form and chart calculation. The other views are classic scripts sharing this global
 * scope, loaded after it (index.html): chart-views, dasa, readings, panchangam, matching,
 * profiles-ui and print; i18n.js and profiles.js load before it.
 */

// Helper utilities
const $ = s => document.querySelector(s);
const $$ = s => document.querySelectorAll(s);
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

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
  D27: ['Saptavimsamsa', 'சப்தவிம்சாம்சம்'], D30: ['Trimsamsa', 'திரிம்சாம்சம்'], D40: ['Khavedamsa', 'கவேதாம்சம்'],
  D45: ['Akshavedamsa', 'அக்ஷவேதாம்சம்'], D60: ['Shashtiamsa', 'ஷஷ்டியாம்சம்'],
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

// The text for the page language: Malayalam falls back to its term dictionary, then English
const txt = (en, ta, ml) => {
  if (currentLang === 'ta') return ta;
  if (currentLang === 'ml') return ml !== undefined ? ml : mlTerm(en);
  return en;
};
const LANGUAGES = ['en', 'ta', 'ml'];
const LANGUAGE_NAMES = { en: 'English', ta: 'தமிழ்', ml: 'മലയാളം' };
const nextLanguage = lang => LANGUAGES[(LANGUAGES.indexOf(lang) + 1) % LANGUAGES.length];
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
let currentChartPayload = null;  // the birth details behind currentChart, for /api/timeline
let timelineDetailsLoad = null;   // pending or finished fetch of the deferred period readings
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
  if (pageName === 'tools') fillPrasnaQuestions();
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
  // Printing: the report dialog (print.js) for charts, the Porutham report for matches
  $('#print-btn').addEventListener('click', () => printCurrentView());
  $('#quick-print-btn').addEventListener('click', () => openPrintDialog('detailed'));
  $('#print-jathagam-btn').addEventListener('click', () => openPrintDialog('jathagam'));
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
  $('#btn-srilanka-style').addEventListener('click', () => setChartStyle('srilanka'));
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
  $('#btn-mode-ashtottari')?.addEventListener('click', () => setDasaViewMode('ashtottari'));
  $('#btn-mode-chara')?.addEventListener('click', () => setDasaViewMode('chara'));

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
  $('#muhurtham-ics-btn')?.addEventListener('click', exportMuhurthamsIcs);
  $('#prasna-btn')?.addEventListener('click', askPrasna);
  $('#rect-add')?.addEventListener('click', () => { if (rectEvents.length < 12) { rectEvents.push({ date: '', type: 'career' }); renderRectEvents(); } });
  $('#rect-run')?.addEventListener('click', runRectification);
  renderRectEvents();
  fillPrasnaQuestions();
  $('#month-ics-btn')?.addEventListener('click', exportMonthIcs);
  $('#chandrashtamam-ics-btn')?.addEventListener('click', exportChandrashtamamIcs);
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
  $('#muhurtham-btn')?.addEventListener('click', loadMuhurthams);
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
    const saved = localStorage.getItem('joroscope_lang');
    if (LANGUAGES.includes(saved)) currentLang = saved;
  } catch (e) {}
  $('#lang-label').textContent = LANGUAGE_NAMES[nextLanguage(currentLang)];
  renderRectEvents();  // drawn at setup, possibly before the saved language was known
  fillPrasnaQuestions();
  // In Malayalam, terms that renderers write in English (signs, stars, labels) are translated in place
  new MutationObserver(records => {
    if (currentLang !== 'ml') return;
    records.forEach(r => r.addedNodes.forEach(node => {
      if (node.nodeType === Node.TEXT_NODE) translateTree(node.parentNode);
      else if (node.nodeType === Node.ELEMENT_NODE) translateTree(node);
    }));
  }).observe(document.body, { childList: true, subtree: true });
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
  currentLang = nextLanguage(currentLang);
  // A chart fetched in English or Tamil has no Malayalam readings: fetch it again
  if (currentLang === 'ml' && currentChart && currentChartPayload?.lang !== 'ml') $('#birth-form').requestSubmit();
  try {
    localStorage.setItem('joroscope_lang', currentLang);
  } catch (e) {}
  $('#lang-label').textContent = LANGUAGE_NAMES[nextLanguage(currentLang)];
  applyLanguage();
  if (currentChart) {
    renderCurrentChart();
    renderPlanetsTable();
    renderQuickStats();
    renderAshtakavarga();
    renderYogasAndDoshas();
    renderDashaAccordion();
    renderYoginiAccordion();
    renderExtraDasas();
    renderUpagrahas();
    renderJathagaKurippu();
    renderNavamsaTable();
    renderLifeReadings();
    renderDasaTimelineView();
  }
  if (lastDailyPanchangam) populatePanchangamView(lastDailyPanchangam);
  if (lastCalendar) renderMonthCalendar(lastCalendar);
  if (lastMuhurthams) renderMuhurthams(lastMuhurthams);
  if (lastMatch) renderMatchResult(lastMatch);
  fillPrasnaQuestions();
  if (lastPrasna) renderChapterInto($('#prasna-result'), lastPrasna);
  renderRectEvents();
  if (lastRectification) renderChapterInto($('#rect-result'), lastRectification);
  populateQuickProfileDropdown();
  renderProfilesList();
  populateMatchDropdowns();
}

function applyLanguage() {
  const dict = { ...I18N.en, ...I18N[currentLang] };
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
  if (currentLang === 'ml') translateTree(document.body);
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
    payload.lang = currentLang;  // the server sends Malayalam readings only when asked
    const resp = await fetch('/api/chart', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const result = await resp.json();
    if (!resp.ok) throw new Error(result.error || 'Calculation failed.');

    currentChart = result;
    learnMalayalam(result);
    currentChartPayload = payload;
    timelineDetailsLoad = null;
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
    renderExtraDasas();
    renderDasaTimelineView();
    renderLifeReadings();
    renderJathagaKurippu();
    renderNavamsaTable();
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
  $('#stat-lagna-tamil').textContent = currentLang === 'en' ? p.Ascendant.tamil : p.Ascendant.sign;

  $('#stat-moon').textContent = currentLang === 'ta' ? p.Moon.tamil : p.Moon.sign;
  $('#stat-moon-tamil').textContent = currentLang === 'en' ? p.Moon.tamil : p.Moon.sign;

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
  if (currentLang === 'ml') return paksha.startsWith('Shukla') ? 'വെളുത്ത പക്ഷം' : 'കറുത്ത പക്ഷം';
  if (currentLang !== 'ta') return paksha;
  return paksha.startsWith('Shukla') ? 'வளர்பிறை' : 'தேய்பிறை';
}

// Tamil Jathaga Kurippu: the birth notes block of a Tamil horoscope
// Navamsa (D9) table and the full Shodasavarga table
const SHODASAVARGA_KEYS = ['D1', 'D2', 'D3', 'D4', 'D7', 'D9', 'D10', 'D12', 'D16', 'D20', 'D24', 'D27', 'D30', 'D40', 'D45', 'D60'];
const VARGA_BODIES = ['Ascendant', 'Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu'];

function renderNavamsaTable() {
  const rows = currentChart?.navamsa_table;
  const body = $('#navamsa-tbody');
  if (!body) return;
  $('#navamsa-table-card').hidden = !rows;
  if (!rows) return;
  body.innerHTML = rows.map(r => {
    const notes = [];
    if (r.vargottama) notes.push(txt('Vargottama', 'வர்கோத்தமம்'));
    if (r.pushkara) notes.push(txt('Pushkara Navamsa', 'புஷ்கர நவாம்சம்'));
    return `<tr>
      <td><strong>${esc(grahaName(r.body))}</strong></td>
      <td>${esc(txt(r.rasi, r.rasi_ta))}</td>
      <td><strong style="color:var(--gold)">${esc(txt(r.navamsa, r.navamsa_ta))}</strong></td>
      <td>${r.navamsa_part}/9</td>
      <td>${esc(grahaName(r.lord))}</td>
      <td>${r.dignity ? dignityLabel(r.dignity) : '—'}</td>
      <td>${esc(notes.join(', ')) || '—'}</td>
    </tr>`;
  }).join('');

  const vargas = currentChart.vargas || {};
  $('#shodasavarga-head').innerHTML = `<th>${txt('Planet', 'கிரகம்')}</th>` + SHODASAVARGA_KEYS.map(k => {
    const [en, ta] = VARGA_NAMES[k] || [k, k];
    return `<th title="${esc(txt(en, ta))}">${k}</th>`;
  }).join('');
  $('#shodasavarga-tbody').innerHTML = VARGA_BODIES.filter(b => vargas.D1 && b in vargas.D1).map(b => `<tr>
      <td><strong>${esc(grahaName(b))}</strong></td>
      ${SHODASAVARGA_KEYS.map(k => {
        const s = vargas[k]?.[b];
        if (s == null) return '<td>—</td>';
        const same = k !== 'D1' && s === vargas.D1[b];
        return `<td${same ? ' class="varga-same"' : ''}>${esc(currentLang === 'ta' ? SIGNS_TA[s] : SIGNS_EN[s].slice(0, 3))}</td>`;
      }).join('')}
    </tr>`).join('');
}

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
  const withTa = (en, ta) => currentLang === 'en' ? `${en} (${ta})` : en;  // the Tamil name beside English only
  const starIdx = STARS_EN.indexOf(p.Moon.nakshatra);

  const rows = [
    [pick('Tamil Year', 'வருடம்'), pick(withTa(tc.year, tc.year_ta), `${tc.year_ta} வருடம்`)],
    [pick('Tamil Month & Date', 'மாதம் & தேதி'), pick(withTa(`${tc.month} ${tc.day}`, tc.month_ta), `${tc.month_ta} ${tc.day}`)],
    [pick('Vaaram (Vedic day)', 'கிழமை'), pick(withTa(si.vaaram.en, si.vaaram.ta), si.vaaram.ta)],
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
  const ex = si.extras;
  if (ex) {
    const none = pick('None', 'இல்லை');
    rows.push(
      [pick('Yogi · Duplicate Yogi', 'யோகி · இரண்டாம் யோகி'),
        `${grahaName(ex.yogi.planet)} (${pick(ex.yogi.star, ex.yogi.star_ta)}) · ${grahaName(ex.yogi.duplicate)}`],
      [pick('Avayogi', 'அவயோகி'), `${grahaName(ex.avayogi.planet)} (${pick(ex.avayogi.star, ex.avayogi.star_ta)})`],
      [pick('Dagdha Rasi', 'தக்த ராசி'), ex.dagdha_rasis.map(r => pick(r.en, r.ta)).join(', ') || none],
      [pick('Chandra Avastha · Vela · Kriya', 'சந்திர அவஸ்தை · வேளை · கிரியை'),
        `${ex.chandra.avastha}/12 · ${ex.chandra.vela}/36 · ${ex.chandra.kriya}/60`],
      [pick('Moudhyam (combust)', 'மௌட்யம் (அஸ்தங்கம்)'), ex.moudhyam.map(m => `${grahaName(m.planet)} ${m.distance}°`).join(', ') || none],
      [pick('Graha Yuddha', 'கிரக யுத்தம்'),
        (ex.graha_yuddha || []).map(w => pick(`${w.winner} defeats ${w.loser}`, `${grahaName(w.winner)} வெற்றி, ${grahaName(w.loser)} தோல்வி`)).join('; ') || none]
    );
  }
  return rows;
}
