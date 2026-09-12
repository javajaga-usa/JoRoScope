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

const PLANET_NAMES = {
  Sun: { en: 'Sun', ta: 'சூரியன்', short: 'Su', color: '#f39c12' },
  Moon: { en: 'Moon', ta: 'சந்திரன்', short: 'Mo', color: '#ecf0f1' },
  Mars: { en: 'Mars', ta: 'செவ்வாய்', short: 'Ma', color: '#e74c3c' },
  Mercury: { en: 'Mercury', ta: 'புதன்', short: 'Me', color: '#2ecc71' },
  Jupiter: { en: 'Jupiter', ta: 'குரு', short: 'Ju', color: '#f1c40f' },
  Venus: { en: 'Venus', ta: 'சுக்கிரன்', short: 'Ve', color: '#e056fd' },
  Saturn: { en: 'Saturn', ta: 'சனி', short: 'Sa', color: '#3498db' },
  Rahu: { en: 'Rahu', ta: 'ராகு', short: 'Ra', color: '#95a5a6' },
  Ketu: { en: 'Ketu', ta: 'கேது', short: 'Ke', color: '#bdc3c7' },
  Ascendant: { en: 'Ascendant', ta: 'லக்னம்', short: 'Asc', color: '#e5c378' }
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
    nakshatra: 'Shatabhisha',
    nakshatra_ta: 'சதயம்',
    nakshatra_idx: 23,
    sign_idx: 10,
    pada: 1,
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
    moon_sign: 'Leo',
    moon_sign_ta: 'சிம்மம்',
    nakshatra: 'Magha',
    nakshatra_ta: 'மகம்',
    nakshatra_idx: 9,
    sign_idx: 4,
    pada: 2,
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
    pada: 4,
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
    open_timeline_studio: 'Open Interactive 81-Period Timeline Studio →'
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
    latitude: 'அட்சரேகை (Lat)',
    longitude: 'தீர்க்கரேகை (Lon)',
    timezone: 'நேர வலயம் (Timezone)',
    ayanamsa: 'அயனாம்சம்',
    dst_clock: 'கடிகார மாற்றம் (DST)',
    generate_chart: 'ஜாதகம் கணிக்கவும்',
    ready_to_reveal: 'வான மண்டலம் கணிக்கத் தயார்',
    enter_details_prompt: 'பிறப்பு விவரங்களை உள்ளிட்டு "ஜாதகம் கணிக்கவும்" பொத்தானை அழுத்தவும்.',
    save_profile: 'ஜாதகத்தை சேமி',
    export_pdf: 'பிடிஎஃப் ஆக எடு',
    ascendant: 'லக்னம் (ASCENDANT)',
    moon_sign: 'சந்திர ராசி (MOON SIGN)',
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
    timeline_predictions_mode: 'காலவரிசை பலன்கள் (Timeline)',
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
    open_timeline_studio: '81 தசா-புக்தி காலவரிசை ஸ்டுடியோவைக் காண்க →'
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
  if (pageName === 'panchangam' && currentChart) populatePanchangamView(currentChart.panchanga);

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
  $('#lang-label').textContent = currentLang === 'en' ? 'தமிழ்' : 'English';
  applyLanguage();
  if (currentChart) {
    renderCurrentChart();
    renderPlanetsTable();
    renderQuickStats();
    renderAshtakavarga();
    renderLifeReadings();
    renderDasaTimelineView();
  }
  populateQuickProfileDropdown();
  renderProfilesList();
  populateMatchDropdowns();
}

function applyLanguage() {
  const dict = I18N[currentLang];
  $$('[data-i18n]').forEach(el => {
    const key = el.dataset.i18n;
    if (dict[key]) el.textContent = dict[key];
  });
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
    notify('Geolocation is not supported by your browser.');
    return;
  }
  notify('Querying coordinates...');
  navigator.geolocation.getCurrentPosition(
    pos => {
      const lat = pos.coords.latitude.toFixed(4);
      const lon = pos.coords.longitude.toFixed(4);
      $('#input-lat').value = lat;
      $('#input-lon').value = lon;
      $('#city-search').value = `Current Location (${lat}, ${lon})`;
      // Try to auto-guess timezone
      try {
        const guessedTz = Intl.DateTimeFormat().resolvedOptions().timeZone;
        if (guessedTz) $('#input-timezone').value = guessedTz;
      } catch (e) {}
      notify(`Coordinates updated: ${lat}, ${lon}`);
    },
    err => {
      notify('Could not retrieve location. Please enter coordinates manually.');
    },
    { timeout: 8000 }
  );
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

        // Auto-suggest timezone if Indian city or known
        const n = c.name.toLowerCase();
        if (n.includes('india') || c.longitude > 68 && c.longitude < 97 && c.latitude > 8 && c.latitude < 37) {
          $('#input-timezone').value = 'Asia/Kolkata';
        } else if (n.includes('colombo') || n.includes('sri lanka')) {
          $('#input-timezone').value = 'Asia/Colombo';
        } else if (n.includes('singapore')) {
          $('#input-timezone').value = 'Asia/Singapore';
        } else if (n.includes('dubai') || n.includes('uae')) {
          $('#input-timezone').value = 'Asia/Dubai';
        } else if (n.includes('london') || n.includes('uk')) {
          $('#input-timezone').value = 'Europe/London';
        } else if (n.includes('new york') || n.includes('usa')) {
          $('#input-timezone').value = 'America/New_York';
        }
        notify(`Selected ${c.name}`);
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
    renderAshtakavarga();
    renderYogasAndDoshas();
    renderDashaAccordion();
    renderDasaTimelineView();
    renderLifeReadings();
    populatePanchangamView(result.panchanga);

    // Sync calculated astrological attributes with saved profiles if already stored
    syncCalculatedProfileWithStorage(result);

    notify(`Chart generated for ${result.profile.name}`);
  } catch (err) {
    errorEl.textContent = err.message;
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

  $('#res-name').textContent = prof.name || 'Unnamed Chart';
  $('#res-details').textContent = `${prof.date} · ${prof.time} · ${prof.city} · ${prof.timezone} · ${prof.ayanamsa} Ayanamsa`;

  const ascSignIdx = p.Ascendant.sign_index;
  $('#res-zodiac-icon').textContent = ZODIAC_SYMBOLS[ascSignIdx];

  $('#stat-lagna').textContent = currentLang === 'ta' ? p.Ascendant.tamil : p.Ascendant.sign;
  $('#stat-lagna-tamil').textContent = currentLang === 'ta' ? p.Ascendant.sign : p.Ascendant.tamil;

  $('#stat-moon').textContent = currentLang === 'ta' ? p.Moon.tamil : p.Moon.sign;
  $('#stat-moon-tamil').textContent = currentLang === 'ta' ? p.Moon.sign : p.Moon.tamil;

  $('#stat-star').textContent = currentLang === 'ta' ? p.Moon.tamil_nakshatra : p.Moon.nakshatra;
  $('#stat-star-pada').textContent = `Pada ${p.Moon.pada} · Ruler: ${p.Moon.nakshatra_lord}`;

  if (currentChart.active_dasha) {
    const ad = currentChart.active_dasha;
    $('#stat-dasa').textContent = `${ad.dasa} · ${ad.bhukti}`;
    $('#stat-dasa-sub').textContent = `Pratyantar: ${ad.pratyantar}`;
    $('#hero-dasa-names').textContent = `${ad.dasa} Maha Dasa → ${ad.bhukti} Bhukti → ${ad.pratyantar} Pratyantar`;
    $('#hero-dasa-dates').textContent = `Active through ${ad.end.slice(0, 10)} (Maha Dasa ends ${ad.dasa_end.slice(0, 10)})`;
  } else {
    $('#stat-dasa').textContent = '—';
  }

  $('#calc-engine-desc').textContent = `${currentChart.method.engine} (${currentChart.method.ephemeris}). Houses: ${currentChart.method.houses}. Nodes: ${currentChart.method.nodes}.`;
  $('#calc-jd').textContent = currentChart.julian_day.toFixed(6);
  $('#calc-ayanamsa-val').textContent = formatDegrees(currentChart.ayanamsa_degrees);
}

// Chart Style & Varga Switching
function setChartStyle(style) {
  currentStyle = style;
  $('#btn-south-style').classList.toggle('active', style === 'south');
  $('#btn-north-style').classList.toggle('active', style === 'north');
  $('#btn-east-style').classList.toggle('active', style === 'east');

  $('#south-chart-container').hidden = (style !== 'south');
  $('#north-chart-container').hidden = (style !== 'north');
  $('#east-chart-container').hidden = (style !== 'east');

  renderCurrentChart();
}

function setVarga(varga) {
  currentVarga = varga;
  $$('.varga-pill').forEach(b => b.classList.toggle('active', b.dataset.varga === varga));
  $('#current-varga-display').textContent = `${varga} Chart`;
  renderCurrentChart();
}

function renderCurrentChart() {
  if (!currentChart) return;
  if (currentStyle === 'south') {
    renderSouthChart();
  } else if (currentStyle === 'north') {
    renderNorthChart();
  } else if (currentStyle === 'east') {
    renderEastChart();
  }
}

// 1. South Indian Layout (Traditional 4x4 Grid with Fixed Signs)
function renderSouthChart() {
  const container = $('#south-chart-container');
  container.replaceChildren();

  // South Indian Sign positions [row, col] (1-indexed)
  // 0: Aries (1,2), 1: Taurus (1,3), 2: Gemini (1,4), 3: Cancer (2,4), 4: Leo (3,4), 5: Virgo (4,4),
  // 6: Libra (4,3), 7: Scorpio (4,2), 8: Sagittarius (4,1), 9: Capricorn (3,1), 10: Aquarius (2,1), 11: Pisces (1,1)
  const pos = [
    [1, 2], [1, 3], [1, 4], [2, 4],
    [3, 4], [4, 4], [4, 3], [4, 2],
    [4, 1], [3, 1], [2, 1], [1, 1]
  ];

  const ascSign = currentChart.planets.Ascendant.sign_index;

  // Render 12 houses
  for (let s = 0; s < 12; s++) {
    const cell = document.createElement('div');
    cell.className = 'house-cell';
    cell.style.gridArea = `${pos[s][0]} / ${pos[s][1]}`;

    // Relative house number from Lagna
    const houseNum = (s - ascSign + 12) % 12 + 1;

    // Header
    const header = document.createElement('div');
    header.className = 'house-header';
    header.innerHTML = `
      <div>
        <span class="sign-label">${currentLang === 'ta' ? SIGNS_TA[s] : SIGNS_EN[s]}</span>
        <span class="tamil-sign-label">${currentLang === 'ta' ? SIGNS_EN[s] : SIGNS_TA[s]}</span>
      </div>
      <span class="house-num-badge">H${houseNum}</span>
    `;
    cell.append(header);

    // Planets inside this sign for the current Varga
    const flow = document.createElement('div');
    flow.className = 'house-planets-flow';

    Object.entries(currentChart.planets).forEach(([pName, pData]) => {
      const vargaSign = pData.vargas[currentVarga];
      if (vargaSign === s) {
        const badge = document.createElement('span');
        const isAsc = (pName === 'Ascendant');
        const isBenefic = ['Jupiter', 'Venus', 'Moon', 'Mercury'].includes(pName);
        badge.className = `planet-badge ${isAsc ? 'asc' : (isBenefic ? 'benefic' : 'malefic')} ${pData.retrograde ? 'retro' : ''} ${pData.combust ? 'combust' : ''}`;
        badge.title = `${pName} (${formatDegrees(pData.degree)})`;
        badge.textContent = PLANET_NAMES[pName].short;
        flow.append(badge);
      }
    });

    cell.append(flow);

    // Click handler for house inspector
    cell.onclick = () => openHouseInspector(houseNum, s);

    container.append(cell);
  }

  // Center Box
  const center = document.createElement('div');
  center.className = 'chart-center-box';
  center.innerHTML = `
    <span class="center-star">✦</span>
    <h3 class="center-title">${currentVarga} ${currentVarga === 'D1' ? 'Rasi' : (currentVarga === 'D9' ? 'Navamsa' : 'Varga')}</h3>
    <p class="center-sub">${esc(currentChart.profile.name || 'JoRoScope')}</p>
    <span class="center-meta">${currentChart.profile.date} · ${currentChart.method.ayanamsa}</span>
  `;
  container.append(center);
}

// 2. North Indian Diamond Layout (SVG Renderer)
function renderNorthChart() {
  const svg = $('#north-svg');
  svg.innerHTML = '';

  const ascSign = currentChart.planets.Ascendant.sign_index;
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
    g.onclick = () => openHouseInspector(hItem.num, signIdx);

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
    const planetsInHouse = Object.entries(currentChart.planets).filter(([pName, pData]) => {
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

      const names = planetsInHouse.map(([n, p]) => `${PLANET_NAMES[n].short}${p.retrograde ? 'ᴿ' : ''}`).join(' ');
      planText.textContent = names;
      g.append(planText);
    }

    svg.append(g);
  });
}

// 3. East Indian Layout (SVG Renderer)
function renderEastChart() {
  const svg = $('#east-svg');
  svg.innerHTML = '';
  // East Indian grid
  renderNorthChart(); // Fallback elegant SVG display with shared geometric harmony
}

// House Inspector Drawer
function openHouseInspector(houseNum, signIdx) {
  if (!currentChart) return;
  const inspector = $('#house-inspector-card');
  inspector.hidden = false;

  const signName = currentLang === 'ta' ? SIGNS_TA[signIdx] : SIGNS_EN[signIdx];
  const signLord = currentChart.house_details[houseNum - 1].lord;

  $('#inspect-title').textContent = `House ${houseNum} (${signName}) Inspector`;
  $('#inspect-sign').textContent = `Sign: ${signName} · Lord: ${signLord} · House ${houseNum} from Lagna`;

  // Occupants in D1
  const occupants = Object.entries(currentChart.planets).filter(([n, p]) => p.house === houseNum);
  const occEl = $('#inspect-occupants');
  occEl.replaceChildren();
  if (occupants.length) {
    occupants.forEach(([n, p]) => {
      const pill = document.createElement('span');
      pill.className = 'planet-badge';
      pill.textContent = `${PLANET_NAMES[n].en} (${formatDegrees(p.degree)})`;
      occEl.append(pill);
    });
  } else {
    occEl.innerHTML = '<span class="muted">No occupant planets</span>';
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
      pill.textContent = `${PLANET_NAMES[n].en} (from H${p.house})`;
      aspEl.append(pill);
    });
  } else {
    aspEl.innerHTML = '<span class="muted">No direct major aspects</span>';
  }

  // Ashtakavarga SAV points
  const sav = currentChart.ashtakavarga.SAV[signIdx];
  $('#inspect-sav').textContent = `${sav} Bindus`;

  // Significations
  $('#inspect-significations').textContent = HOUSE_BHAVAS[houseNum] || 'Auspicious celestial node.';

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
      <td>${starName} (Pada ${p.pada})</td>
      <td><strong>House ${p.house}</strong></td>
      <td><span class="dignity-badge ${dignityClass}">${p.dignity || 'Neutral'}</span></td>
      <td>${p.retrograde ? '<span class="legend-badge retro">Retrograde (Rx)</span>' : 'Direct'} ${p.combust ? '<span class="legend-badge combust">🔥 Combust</span>' : ''}</td>
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
      <span class="muted">${isStrong ? 'Auspicious' : 'Average'}</span>
    `;
    grid.append(card);
  });

  // Render BAV Table
  const thead = $('#bav-header');
  thead.innerHTML = '<th>Planet</th>' + SIGNS_EN.map((s, i) => `<th>${currentLang === 'ta' ? SIGNS_TA[i] : s.slice(0, 3)}</th>`).join('') + '<th>Total</th>';

  const tbody = $('#bav-tbody');
  tbody.replaceChildren();

  Object.entries(bav).forEach(([pName, row]) => {
    const tr = document.createElement('tr');
    const rowSum = row.reduce((a, b) => a + b, 0);
    tr.innerHTML = `<td><strong>${pName}</strong></td>` + row.map(v => `<td>${v}</td>`).join('') + `<td><strong>${rowSum}</strong></td>`;
    tbody.append(tr);
  });
}

// Yogas & Doshas Rendering
function renderYogasAndDoshas() {
  if (!currentChart) return;
  const yogas = currentChart.yogas || [];
  const doshas = currentChart.doshas || {};

  // Kuja / Manglik
  const m = doshas.manglik;
  const mCard = $('#manglik-card');
  if (m) {
    if (m.present && !m.cancelled) {
      mCard.className = 'cosmic-card dosha-card active-dosha';
      $('#manglik-status').className = 'status-pill danger';
      $('#manglik-status').textContent = 'Present (Active)';
      $('#manglik-desc').textContent = `Mars is placed in House ${m.house}. Encourages vigorous ambition and strong independence in relationships.`;
    } else if (m.present && m.cancelled) {
      mCard.className = 'cosmic-card dosha-card cancelled-dosha';
      $('#manglik-status').className = 'status-pill success';
      $('#manglik-status').textContent = 'Present but Cancelled (Bhanga)';
      $('#manglik-desc').textContent = `Mars resides in House ${m.house}, but Kuja Dosha is neutralized by protective astrological alignments.`;
      $('#manglik-reasons').innerHTML = (m.reasons || []).map(r => `<div>✔ ${r}</div>`).join('');
    } else {
      mCard.className = 'cosmic-card dosha-card';
      $('#manglik-status').className = 'status-pill neutral';
      $('#manglik-status').textContent = 'Not Present';
      $('#manglik-desc').textContent = 'Mars occupies an auspicious non-afflicting house position.';
      $('#manglik-reasons').innerHTML = '';
    }
  }

  // Kaal Sarp
  const ks = doshas.kaal_sarp;
  const ksCard = $('#kaalsarp-card');
  if (ks) {
    if (ks.present) {
      ksCard.className = 'cosmic-card dosha-card active-dosha';
      $('#kaalsarp-status').className = 'status-pill danger';
      $('#kaalsarp-status').textContent = ks.type;
      $('#kaalsarp-desc').textContent = ks.description;
    } else {
      ksCard.className = 'cosmic-card dosha-card';
      $('#kaalsarp-status').className = 'status-pill neutral';
      $('#kaalsarp-status').textContent = 'Not Present';
      $('#kaalsarp-desc').textContent = ks.description;
    }
  }

  // Detected Yogas Grid
  $('#yogas-count').textContent = `${yogas.length} Detected`;
  const grid = $('#yogas-grid');
  grid.replaceChildren();

  if (yogas.length) {
    yogas.forEach(y => {
      const card = document.createElement('div');
      card.className = 'yoga-card';
      card.innerHTML = `
        <h3>${y.name}</h3>
        <div class="yoga-meta">${y.category} · <span style="color:var(--emerald)">${y.auspiciousness}</span></div>
        <p class="yoga-desc">${y.description}</p>
        <div class="pill-list" style="margin-top:8px">
          ${(y.planets || []).map(p => `<span class="planet-badge benefic">${p}</span>`).join('')}
        </div>
      `;
      grid.append(card);
    });
  } else {
    grid.innerHTML = '<p class="muted">No major classical yogas triggered under primary rules.</p>';
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
        <span class="dasa-name">${d.lord} Maha Dasa</span>
        ${d.is_active ? '<span class="status-pill success" style="margin-left:8px">ACTIVE</span>' : ''}
      </div>
      <span class="dasa-dates">${d.start.slice(0, 10)} → ${d.end.slice(0, 10)}</span>
    `;
    details.append(summary);

    // Subperiods table
    const table = document.createElement('table');
    table.className = 'luxury-table bhukti-table';
    table.innerHTML = `
      <thead>
        <tr>
          <th>Bhukti</th>
          <th>Pratyantardasa Details</th>
          <th>Start (UTC)</th>
          <th>End (UTC)</th>
        </tr>
      </thead>
      <tbody>
        ${d.subperiods.map(b => `
          <tr class="${b.is_active ? 'active-period' : ''}">
            <td><strong>${b.lord}</strong> ${b.is_active ? '<span class="status-pill success">Active</span>' : ''}</td>
            <td>${(b.pratyantars || []).map(p => `<span class="planet-badge ${p.is_active ? 'asc' : ''}" style="margin:2px">${p.lord}</span>`).join('')}</td>
            <td>${b.start.slice(0, 10)}</td>
            <td>${b.end.slice(0, 10)}</td>
          </tr>
        `).join('')}
      </tbody>
    `;
    details.append(table);
    container.append(details);
  });
}

// Dasa View Switcher & Timeline Predictions Engine
function setDasaViewMode(mode) {
  currentDasaMode = mode;
  $('#btn-mode-timeline')?.classList.toggle('active', mode === 'timeline');
  $('#btn-mode-cycles')?.classList.toggle('active', mode === 'cycles');
  const tView = $('#dasa-timeline-view');
  const cView = $('#dasa-tabular-view');
  if (tView) tView.hidden = (mode !== 'timeline');
  if (cView) cView.hidden = (mode !== 'cycles');
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

      <button type="button" class="timeline-details-toggle">
        <span>▶</span> <span>${isTa ? 'விரிவான பலாபலன்கள் (தொழில், தனம், நலம், குடும்பம், பரிகாரம்)' : 'Detailed Breakdown (Career, Wealth, Health, Family, Remedies)'}</span>
      </button>

      <div class="timeline-details-panel" hidden>
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
      toggleBtn.addEventListener('click', () => {
        const isClosed = panel.hidden;
        panel.hidden = !isClosed;
        toggleBtn.querySelector('span:first-child').textContent = isClosed ? '▼' : '▶';
      });
      if (p.is_active) {
        panel.hidden = false;
        toggleBtn.querySelector('span:first-child').textContent = '▼';
      }
    }

    container.append(card);
  });
}

// Life Predictions Multi-Chapter Comprehensive Renderer
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
      ? `சூரியன் & திதி: ${ov.tithi_name} (யோகம்: ${ov.yoga_name})`
      : `Sun & Tithi: ${ov.tithi_name} (${ov.yoga_name} Yoga)`;
    $('#pred-sun-sub').textContent = isTa
      ? 'ஆன்ம பலம், கௌரவம் மற்றும் நித்திய சுப யோகம்'
      : 'Soul Vitality, Integrity & Auspicious Alignment';
    $('#pred-sun-text').textContent = isTa
      ? `நீங்கள் ${ov.tithi_name} திதியிலும், ${ov.yoga_name} யோகத்திலும் அவதரித்துள்ளீர்கள். ஆன்ம காரகனான சூரியனின் ஆதிக்கத்தால் சமூக அந்தஸ்து, கடமை உணர்வு, தர்ம சிந்தனை மற்றும் அசைக்க முடியாத தன்னம்பிக்கை உங்களை முன்னிறுத்தும்.`
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
      const occStr = b.occupants && b.occupants.length ? b.occupants.join(', ') : (isTa ? 'கிரகங்கள் இல்லை' : 'None');
      const aspStr = b.aspected_by && b.aspected_by.length ? b.aspected_by.join(', ') : (isTa ? 'நேரடி பார்வைகள் இல்லை' : 'None');
      const title = isTa ? b.title_ta : b.title_en;
      const narrative = isTa ? b.prediction_ta : b.prediction_en;

      card.innerHTML = `
        <div class="bhava-header">
          <div class="bhava-title-group">
            <span class="bhava-num-badge">${b.house}</span>
            <div>
              <h3>${esc(title)}</h3>
              <small class="muted">${isTa ? b.tamil_sign : b.sign} · ${isTa ? 'அதிபதி' : 'Lord'}: ${b.lord} (${isTa ? 'பாவம்' : 'H'}${b.lord_house})</small>
            </div>
          </div>
          <span class="bhava-meta-pill ${isSavStrong ? 'highlight' : ''}">${b.sav_points} SAV Bindus</span>
        </div>
        <div class="bhava-meta-strip">
          <span class="bhava-meta-pill">${isTa ? 'அதிபதி நிலை' : 'Lord Dignity'}: <strong>${b.lord_dignity}</strong></span>
          <span class="bhava-meta-pill">${isTa ? 'அமர்ந்த கிரகங்கள்' : 'Occupants'}: <strong>${esc(occStr)}</strong></span>
          <span class="bhava-meta-pill">${isTa ? 'பார்வை கிரகங்கள்' : 'Aspects'}: <strong>${esc(aspStr)}</strong></span>
        </div>
        <p class="reading-body">${esc(narrative)}</p>
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
          <span class="dignity-badge ${dignityClass}">${p.dignity || 'Neutral'}</span>
        </div>
        <div class="planet-meta-strip">
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
        ? `தற்போதைய இயங்கும் தசா-புக்தி: ${ad.dasa} தசை — ${ad.bhukti} புக்தி`
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
        ? 'குருப் பெயர்ச்சி பலன் (Guru Peyarchi)'
        : 'Jupiter Transit (Guru Peyarchi)';
      $('#jupiter-transit-badge').textContent = j.favorable
        ? (isTa ? 'சுப பலன் (Auspicious)' : 'Auspicious')
        : (isTa ? 'மத்திம பலன் (Moderate)' : 'Moderate');
      $('#jupiter-transit-badge').className = `status-pill ${j.favorable ? 'success' : 'neutral'}`;
      $('#jupiter-transit-desc').textContent = isTa ? j.prediction_ta : j.prediction_en;
    }
  }

  // Chapter 6: Lucky Gemstones & Remedies
  const luck = pred.lucky_factors;
  if (luck) {
    $('#gem-primary').textContent = luck.primary_gem || '—';
    $('#gem-fortune').textContent = luck.fortune_gem || '—';
    $('#gem-metal').textContent = luck.metal || '—';
    $('#gem-finger').textContent = luck.finger || '—';
    $('#gem-day').textContent = luck.wearing_day || '—';

    $('#luck-numbers').textContent = luck.lucky_numbers ? luck.lucky_numbers.join(', ') : '—';
    $('#luck-days').textContent = luck.lucky_days ? luck.lucky_days.join(', ') : '—';
    $('#luck-colors').textContent = luck.lucky_colors ? luck.lucky_colors.join(', ') : '—';
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
            <span class="bhava-meta-pill">${isTa ? 'நிலை' : 'Dignity'}: <strong>${k.dignity}</strong></span>
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
      $('#timing-calc-date').textContent = `Live: ${dt.calculation_date_utc.slice(0, 10)}`;
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
          <td><strong>${row.kakshya_num}</strong> ${row.is_current ? '<span class="status-pill success" style="font-size:9px">Active</span>' : ''}</td>
          <td>${row.range_str}</td>
          <td><strong>${isTa ? row.lord_ta : row.lord}</strong></td>
          <td>${row.has_bindu ? '<span style="color:#2ecc71; font-weight:700">1 Bindu</span>' : '<span style="color:#e63946">0 Bindu</span>'}</td>
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
          <td><strong>${row.kakshya_num}</strong> ${row.is_current ? '<span class="status-pill success" style="font-size:9px">Active</span>' : ''}</td>
          <td>${row.range_str}</td>
          <td><strong>${isTa ? row.lord_ta : row.lord}</strong></td>
          <td>${row.has_bindu ? '<span style="color:#2ecc71; font-weight:700">1 Bindu</span>' : '<span style="color:#e63946">0 Bindu</span>'}</td>
          <td><span class="dignity-badge ${row.has_bindu ? 'exalted' : 'neutral'}">${isTa ? row.status_ta : row.status_en}</span></td>
        `;
        jBody.append(tr);
      });
    }
  }

  // Chapter 12: Shadbala Planetary Strengths & Potency
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
              <h3>${esc(label)} — ${p.total_rupas} Rupas (${p.total_virupas} Virupas)</h3>
              <small class="muted">${isTa ? 'தேவை' : 'Required'}: ${p.min_required_rupas} Rupas · Rank ${p.rank} of 7</small>
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
            <span class="bhava-meta-pill">Sthana: <strong>${p.sthana_bala}</strong></span>
            <span class="bhava-meta-pill">Dig: <strong>${p.dig_bala}</strong></span>
            <span class="bhava-meta-pill">Kaala: <strong>${p.kaala_bala}</strong></span>
            <span class="bhava-meta-pill">Chesta: <strong>${p.chesta_bala}</strong></span>
            <span class="bhava-meta-pill">Naisargika: <strong>${p.naisargika_bala}</strong></span>
            <span class="bhava-meta-pill">Drik: <strong>${p.drik_bala}</strong></span>
          </div>
          <p class="reading-body" style="font-size:12.5px; margin-top:8px;">${esc(reading)}</p>
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
          <td>${c.star_name} (${isTa ? c.star_lord_ta : c.star_lord})</td>
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
          <td>${p.star_name} (${isTa ? p.star_lord_ta : p.star_lord})</td>
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
              <small class="muted">${isTa ? 'இணைந்த கிரகங்கள்' : 'Associated Grahas'}: ${s.planets.join(' + ')}</small>
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

// Panchangam View
function populatePanchangamView(panch) {
  if (!panch) return;
  $('#panch-tithi').textContent = `${panch.tithi_name} (${panch.tithi})`;
  $('#panch-paksha').textContent = `${panch.paksha} · ${panch.tithi_percent_remaining}% left`;

  $('#panch-nakshatra').textContent = `${panch.nakshatra} (${panch.tamil_nakshatra})`;
  $('#panch-pada').textContent = `Pada ${panch.pada} · Gana: ${panch.nakshatra_gana} · Yoni: ${panch.nakshatra_yoni}`;

  $('#panch-yoga').textContent = `${panch.yoga_name} (Yoga ${panch.yoga_number})`;
  $('#panch-yoga-nature').textContent = panch.yoga_auspiciousness;

  $('#panch-karana').textContent = panch.karana_name;
  $('#panch-karana-type').textContent = `Half-tithi ${panch.karana_half_number}`;

  $('#panch-abhijit').textContent = panch.abhijit_muhurtham_utc;
  $('#panch-rahu').textContent = panch.rahu_kalam_utc;
  $('#panch-yama').textContent = panch.yamagandam_utc;
  $('#panch-gulika').textContent = panch.gulika_kalam_utc;
  $('#panch-sun-times').textContent = `Rise: ${panch.sunrise_utc} | Set: ${panch.sunset_utc} (${panch.day_length_hours}h)`;
}

// Horoscope Matching Tool
function populateMatchDropdowns() {
  const gStar = $('#match-girl-star');
  const bStar = $('#match-boy-star');
  const gSign = $('#match-girl-sign');
  const bSign = $('#match-boy-sign');

  if (gStar && !gStar.options.length) {
    STARS_EN.forEach((s, i) => {
      gStar.add(new Option(`${i + 1}. ${s} (${STARS_TA[i]})`, i));
      bStar.add(new Option(`${i + 1}. ${s} (${STARS_TA[i]})`, i));
    });
    SIGNS_EN.forEach((s, i) => {
      gSign.add(new Option(`${s} (${SIGNS_TA[i]})`, i));
      bSign.add(new Option(`${s} (${SIGNS_TA[i]})`, i));
    });
  }

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

async function runHoroscopeMatch() {
  const gStar = parseInt($('#match-girl-star').value, 10);
  const gSign = parseInt($('#match-girl-sign').value, 10);
  const bStar = parseInt($('#match-boy-star').value, 10);
  const bSign = parseInt($('#match-boy-sign').value, 10);

  const payload = {
    girl: { nakshatra_index: gStar, sign_index: gSign },
    boy: { nakshatra_index: bStar, sign_index: bSign }
  };

  try {
    const resp = await fetch('/api/match', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const match = await resp.json();
    if (!resp.ok) throw new Error(match.error);

    $('#match-results-container').hidden = false;
    $('#match-score-num').textContent = match.guna_milan.total_score;
    $('#match-verdict-title').textContent = match.verdict;
    $('#match-verdict-desc').textContent = `${match.passed_count} of 10 Poruthams passed. Guna score: ${match.guna_milan.total_score} of 36.`;

    const rajjuBadge = $('#match-rajju-badge');
    rajjuBadge.textContent = match.rajju_agreement ? 'Rajju Match: Harmonious (Passed)' : 'Rajju Dosha: Inauspicious (Same Rajju)';
    rajjuBadge.className = `badge ${match.rajju_agreement ? 'status-pill success' : 'status-pill danger'}`;

    $('#match-porutham-count').textContent = `${match.passed_count} of 10 Passed`;

    // 10 Poruthams table
    const tbody = $('#poruthams-tbody');
    tbody.replaceChildren();
    match.poruthams.forEach(p => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><strong>${p.name}</strong> <small style="display:block;color:var(--gold-dim)">${p.tamil}</small></td>
        <td>${p.description}</td>
        <td><span class="status-pill ${p.passed ? 'success' : 'danger'}">${p.passed ? 'Passed ✔' : 'Not Matched ✖'}</span></td>
        <td>${p.points} / ${p.max_points}</td>
      `;
      tbody.append(tr);
    });

    // 8 Gunas Grid
    const gunasGrid = $('#gunas-grid');
    gunasGrid.replaceChildren();
    const gObj = match.guna_milan;
    const gLabels = [
      ['Varna (Work & Spiritual Nature)', gObj.varna, 1],
      ['Vashya (Mutual Magnetism)', gObj.vashya, 2],
      ['Tara (Health & Longevity)', gObj.tara, 3],
      ['Yoni (Physical Harmony)', gObj.yoni, 4],
      ['Graha Maitri (Mental Friendship)', gObj.graha_maitri, 5],
      ['Gana (Temperament Alignment)', gObj.gana, 6],
      ['Bhakoot (Family Fortune)', gObj.bhakoot, 7],
      ['Nadi (Genetic / Health Affinity)', gObj.nadi, 8]
    ];
    gLabels.forEach(([label, pts, max]) => {
      const card = document.createElement('div');
      card.className = 'guna-card';
      card.innerHTML = `
        <small style="font-size:10px;color:var(--text-muted)">${label}</small>
        <div style="font-size:18px;font-weight:700;color:var(--gold);margin:4px 0">${pts} / ${max}</div>
      `;
      gunasGrid.append(card);
    });

    notify('Horoscope compatibility calculated');
  } catch (err) {
    notify('Matching error: ' + err.message);
  }
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
    notify('Storage error: please export profiles backup.');
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
          <span class="pill-badge" style="font-size:10px;padding:2px 8px;">${esc(p.city || 'Custom Location')}</span>
        </div>
      </div>

      <p class="muted" style="font-size:11.5px;margin:6px 0 8px;line-height:1.5;">
        📅 ${esc(p.date)} · ⏰ ${esc(p.time)}<br>
        🌐 ${esc(p.timezone || 'Asia/Kolkata')} · ${esc(p.ayanamsa || 'Lahiri')}
      </p>

      <div class="profile-astro-badges">
        <span class="mini-astro-tag lagna-tag" title="Ascendant">
          <span>🌌</span> <strong>${isTa ? 'லக்னம்' : 'Asc'}:</strong> ${esc(lagnaStr)}
        </span>
        <span class="mini-astro-tag moon-tag" title="Moon Sign / Rasi">
          <span>🌙</span> <strong>${isTa ? 'ராசி' : 'Rasi'}:</strong> ${esc(moonStr)}
        </span>
        <span class="mini-astro-tag star-tag" title="Birth Star / Nakshatra">
          <span>⭐</span> <strong>${isTa ? 'நட்சத்திரம்' : 'Star'}:</strong> ${esc(starStr)} ${padaStr}
        </span>
      </div>

      <div class="profile-card-actions">
        <button class="action-btn btn-full" data-load="${originalIdx}">
          <span>🪐</span> <span>${isTa ? 'ஜாதகம் திறக்க ↗' : 'Open Chart ↗'}</span>
        </button>
        <button class="action-btn" data-match-boy="${originalIdx}" title="Use as Boy in Horoscope Compatibility">
          <span>👦</span> <span>${isTa ? 'மணமகன்' : 'Boy'}</span>
        </button>
        <button class="action-btn" data-match-girl="${originalIdx}" title="Use as Girl in Horoscope Compatibility">
          <span>👧</span> <span>${isTa ? 'மணமகள்' : 'Girl'}</span>
        </button>
        <button class="action-btn" data-delete="${originalIdx}" style="color:var(--ruby);grid-column:1/-1;" title="Delete this person's record">
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
  notify('Exported profiles backup');
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
    notify(`Imported ${addedCount} new profiles successfully.`);
  } catch (err) {
    notify('Import error: ' + err.message);
  } finally {
    e.target.value = '';
  }
}
