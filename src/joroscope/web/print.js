/**
 * JoRoScope print reports
 * Three presets, modelled on what horoscope software prints today: a traditional Tamil
 * Jathagam (the family sheet, like Prokerala's basic report), a Detailed Horoscope with the
 * tables AstroSage's PDF carries (Shodasavarga, Bhava, Shadbala, Ashtakavarga, KP), and a
 * Complete Report that adds the readings, as Astro-Vision's reports do. Every section can be
 * switched on or off. The sheet prints on A4 with a running header and page numbers; "Save as
 * PDF" in the print window makes the PDF.
 */

const PRINT_SECTIONS = [
  { key: 'birth', en: 'Birth details & Tamil panchangam', ta: 'பிறப்பு விவரங்கள் & பஞ்சாங்கம்', build: printBirth },
  { key: 'charts', en: 'Rasi & Navamsa charts', ta: 'இராசி & நவாம்சச் சக்கரங்கள்', build: printCharts },
  { key: 'planets', en: 'Planetary positions', ta: 'கிரக நிலைகள்', build: printPlanets },
  { key: 'navamsa', en: 'Navamsa table', ta: 'நவாம்ச அட்டவணை', build: printNavamsa },
  { key: 'doshas', en: 'Doshas, yogas & matching notes', ta: 'தோஷங்கள், யோகங்கள் & பொருத்தக் குறிப்புகள்', build: printDoshas },
  { key: 'dasa', en: 'Dasa-Bhukti periods', ta: 'தசா புக்தி காலங்கள்', build: printDasa, newPage: true },
  { key: 'otherdasas', en: 'Ashtottari & Chara Dasa', ta: 'அஷ்டோத்தரி & சர தசை', build: printOtherDasas },
  { key: 'vargas', en: 'Shodasavarga charts & table', ta: 'ஷோடசவர்க்கச் சக்கரங்கள் & அட்டவணை', build: printVargas, newPage: true },
  { key: 'bhavas', en: 'Bhava chakra & house table', ta: 'பாவ சக்கரம் & பாவ அட்டவணை', build: printBhavas, newPage: true },
  { key: 'strength', en: 'Shadbala, Bhava Bala & Vimsopaka', ta: 'ஷட்பலம், பாவ பலம் & விம்சோபகம்', build: printStrength, newPage: true },
  { key: 'ashtakavarga', en: 'Ashtakavarga & Sodhya Pinda', ta: 'அஷ்டகவர்க்கம் & சோத்ய பிண்டம்', build: printAshtakavarga, newPage: true },
  { key: 'kp', en: 'KP cusps & significators', ta: 'கே.பி. பாவ ஆரம்பங்கள் & காரகத்துவம்', build: printKP, newPage: true },
  { key: 'predictions', en: 'Life predictions', ta: 'வாழ்க்கைப் பலன்கள்', build: printPredictions, newPage: true },
  { key: 'reports', en: 'Special reports', ta: 'சிறப்பு அறிக்கைகள்', build: printReportChapters, newPage: true }
];

const PRINT_PRESETS = {
  jathagam: {
    en: 'Traditional Jathagam', ta: 'பாரம்பரிய ஜாதகம்',
    hint_en: 'About 3 pages: birth notes, Rasi and Navamsa, planets, doshas and Dasa-Bhukti; the sheet families share for matching.',
    hint_ta: 'சுமார் 3 பக்கங்கள்: பிறப்புக் குறிப்பு, இராசி & நவாம்சம், கிரக நிலைகள், தோஷங்கள், தசா புக்தி; பொருத்தம் பார்க்கப் பகிரும் ஜாதகம்.',
    title_en: 'Horoscope', title_ta: 'ஜாதகம்',
    sections: ['birth', 'charts', 'planets', 'doshas', 'dasa']
  },
  detailed: {
    en: 'Detailed Horoscope', ta: 'விரிவான ஜாதகம்',
    hint_en: 'Adds the Navamsa and Shodasavarga, Bhava, strength, Ashtakavarga and KP tables an astrologer works from.',
    hint_ta: 'நவாம்சம், ஷோடசவர்க்கம், பாவம், பலம், அஷ்டகவர்க்கம், கே.பி. அட்டவணைகளுடன் ஜோதிடருக்கான விரிவான ஜாதகம்.',
    title_en: 'Detailed Horoscope', title_ta: 'விரிவான ஜாதகம்',
    sections: ['birth', 'charts', 'planets', 'navamsa', 'doshas', 'dasa', 'otherdasas', 'vargas', 'bhavas', 'strength', 'ashtakavarga', 'kp']
  },
  complete: {
    en: 'Complete Report', ta: 'முழுமையான ஜாதக அறிக்கை',
    hint_en: 'Everything above plus the life predictions: panchanga phala, the twelve bhavas, the running dasa, transits, career and health.',
    hint_ta: 'மேலுள்ள அனைத்தும் மற்றும் வாழ்க்கைப் பலன்கள்: பஞ்சாங்க பலன், 12 பாவங்கள், நடப்பு தசை, கோச்சாரம், தொழில், உடல்நலம்.',
    title_en: 'Complete Horoscope Report', title_ta: 'முழுமையான ஜாதக அறிக்கை',
    sections: PRINT_SECTIONS.map(s => s.key)
  }
};

const PRINT_GRAHAS = ['Ascendant', 'Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu'];
const PRINT_SEVEN = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'];
let pendingCharts = [];  // [element id, varga] rendered after the sheet's HTML is in place
let printChartStyle = 'south';  // south, north, east or srilanka
const PRINT_CHART_STYLES = {
  south: ['South Indian (Tamil, Kerala)', 'தென்னிந்திய (தமிழ், கேரளம்)'],
  north: ['North Indian', 'வடஇந்திய'],
  east: ['East Indian', 'கிழக்கிந்திய'],
  srilanka: ['Sri Lankan (Sinhala)', 'இலங்கை (சிங்கள)']
};

// ---------- small builders ----------
const pjKV = rows => rows.map(([k, v]) => `<div class="pj-kv"><span>${esc(k)}</span><strong>${v}</strong></div>`).join('');
// Tables are kept whole on a page; long ones go out in chunks that each carry the header row,
// since WebKit (Safari) does not repeat a table header after a page break
const PJ_TABLE_CHUNK = 28;
const pjTable = (head, rows, cls = '') => {
  const chunks = [];
  for (let i = 0; i < rows.length; i += PJ_TABLE_CHUNK) chunks.push(rows.slice(i, i + PJ_TABLE_CHUNK));
  if (!chunks.length) chunks.push([]);
  const header = `<thead><tr>${head.map(h => `<th>${h}</th>`).join('')}</tr></thead>`;
  return chunks.map(chunk => `
  <table class="pj-table ${cls}">
    ${header}
    <tbody>${chunk.map(r => `<tr>${r.map(cell => `<td>${cell}</td>`).join('')}</tr>`).join('')}</tbody>
  </table>`).join('');
};
const pjChart = (varga, caption) => {
  const id = `pj-chart-${varga}-${pendingCharts.length}`;
  pendingCharts.push([id, varga]);
  const drawing = printChartStyle === 'south'
    ? `<div id="${id}" class="south-chart-grid compact"></div>`
    : `<svg id="${id}" class="pj-svg-chart" viewBox="0 0 600 600" preserveAspectRatio="xMidYMid meet"></svg>`;
  return `<figure class="pj-figure">${drawing}${caption ? `<figcaption>${esc(caption)}</figcaption>` : ''}</figure>`;
};
const pjDate = iso => iso ? localDate(iso) : '—';
const pjLatLon = (v, pos, neg) => `${Math.abs(Number(v)).toFixed(4)}° ${Number(v) >= 0 ? pos : neg}`;
const pjSign = idx => esc(signName(idx));
const pjDeg = (lon) => `${pjSign(Math.floor(lon / 30) % 12)} ${formatDegrees(lon % 30)}`;

// ---------- sections ----------
function printBirth(c) {
  const prof = c.profile;
  const si = c.south_indian || {};
  const data = [
    [txt('Name', 'பெயர்'), esc(prof.name || '—')],
    [txt('Date of birth', 'பிறந்த தேதி'), esc(prof.date)],
    [txt('Time of birth', 'பிறந்த நேரம்'), esc(prof.time)],
    [txt('Place of birth', 'பிறந்த ஊர்'), esc(prof.city || '—')],
    [txt('Latitude · Longitude', 'அட்சரேகை · தீர்க்கரேகை'), `${pjLatLon(prof.latitude, 'N', 'S')} · ${pjLatLon(prof.longitude, 'E', 'W')}`],
    [txt('Time zone', 'நேர வலயம்'), esc(prof.timezone)],
    [txt('Ayanamsa', 'அயனாம்சம்'), `${esc(ayanamsaLabel(prof.ayanamsa))} ${formatDegrees(c.ayanamsa_degrees)}`],
    [txt('Sunrise · Sunset', 'சூரிய உதயம் · அஸ்தமனம்'), si.sunrise_local ? `${clockTime(si.sunrise_local)} · ${clockTime(si.sunset_local)}` : '—']
  ];
  const notes = si.vaaram ? kurippuRows().map(([k, v]) => [k, esc(v)]) : [];
  return `
    <div class="pj-two">
      <div><h3>${txt('Birth data', 'பிறப்புத் தரவு')}</h3><div class="pj-grid one">${pjKV(data)}</div></div>
      <div><h3>${txt('Jathaga Kurippu', 'ஜாதகக் குறிப்பு')}</h3><div class="pj-grid one">${pjKV(notes.slice(0, 8))}</div></div>
    </div>
    ${notes.length > 8 ? `<div class="pj-grid">${pjKV(notes.slice(8))}</div>` : ''}`;
}

function printCharts(c) {
  const irruppu = dasaIrruppuText(c.south_indian?.dasa_irruppu);
  return `
    <div class="pj-charts">${pjChart('D1', txt('Rasi (D1)', 'இராசி (D1)'))}${pjChart('D9', txt('Navamsa (D9)', 'நவாம்சம் (D9)'))}</div>
    ${irruppu ? `<p class="pj-note">${txt('Dasa balance at birth', 'பிறப்பு தசா இருப்பு')}: <strong>${esc(irruppu)}</strong></p>` : ''}`;
}

function printPlanets(c) {
  const bodies = [...PRINT_GRAHAS.map(n => [n, c.planets[n]]), ...(c.south_indian?.mandi ? [['Mandi', c.south_indian.mandi]] : [])];
  const rows = bodies.map(([name, p]) => {
    const flags = [
      p.retrograde && !['Rahu', 'Ketu', 'Ascendant', 'Mandi'].includes(name) ? txt('R', 'வ') : '',
      p.combust ? txt('C', 'அ') : '',
      p.vargas?.D9 === p.sign_index && name !== 'Mandi' ? txt('V', 'வர்') : ''
    ].filter(Boolean).join(' ');
    return [
      `<strong>${esc(grahaName(name))}</strong>`, pjSign(p.sign_index), formatDegrees(p.degree),
      `${esc(starName(p.nakshatra))} · ${p.pada}`, esc(grahaName(p.nakshatra_lord)),
      p.vargas?.D9 != null ? pjSign(p.vargas.D9) : '—', p.house ?? '—', p.bhava ?? '—',
      name === 'Ascendant' || name === 'Mandi' ? '—' : esc(dignityLabel(p.dignity)), flags || '—'
    ];
  });
  return pjTable([txt('Graha', 'கிரகம்'), txt('Rasi', 'ராசி'), txt('Degree', 'பாகை'), txt('Star · Pada', 'நட்சத்திரம் · பாதம்'),
    txt('Star lord', 'நட்சத்திர அதிபதி'), txt('Navamsa', 'நவாம்சம்'), txt('House', 'பாவகம்'), txt('Bhava', 'பாவம்'),
    txt('Dignity', 'நிலை'), txt('Notes', 'குறிப்பு')], rows) +
    `<p class="pj-note">${txt('R retrograde · C combust · V Vargottama · House counts whole signs from the Lagna; Bhava is the Sripati bhava.',
      'வ வக்ரம் · அ அஸ்தங்கம் · வர் வர்கோத்தமம் · பாவகம் லக்ன ராசியிலிருந்து; பாவம் ஸ்ரீபதி முறைப்படி.')}</p>`;
}

function printNavamsa(c) {
  const rows = (c.navamsa_table || []).map(r => [
    `<strong>${esc(grahaName(r.body))}</strong>`, esc(txt(r.rasi, r.rasi_ta)), `<strong>${esc(txt(r.navamsa, r.navamsa_ta))}</strong>`,
    `${r.navamsa_part}/9`, esc(grahaName(r.lord)), r.dignity ? esc(dignityLabel(r.dignity)) : '—',
    [r.vargottama ? txt('Vargottama', 'வர்கோத்தமம்') : '', r.pushkara ? txt('Pushkara', 'புஷ்கரம்') : ''].filter(Boolean).join(', ') || '—'
  ]);
  return pjTable([txt('Graha', 'கிரகம்'), txt('Rasi', 'ராசி'), txt('Navamsa', 'நவாம்சம்'), txt('Amsa', 'அம்சம்'),
    txt('Navamsa lord', 'நவாம்ச அதிபதி'), txt('Dignity in D9', 'நவாம்ச நிலை'), txt('Notes', 'குறிப்பு')], rows);
}

function printDoshas(c) {
  const d = c.doshas || {};
  const si = c.south_indian || {};
  const star = si.birth_star || {};
  const cv = d.chevvai || {};
  const status = (present, cancelled) => !present ? txt('Not present', 'இல்லை')
    : (cancelled ? txt('Present, cancelled', 'உண்டு, நிவர்த்தி') : txt('Present', 'உண்டு'));
  const doshas = [
    [txt('Chevvai Dosham', 'செவ்வாய் தோஷம்'), esc(status(cv.present, cv.cancelled) + (cv.effective ? ` (${cv.severity}/3)` : ''))],
    [txt('Rahu-Ketu Dosham', 'ராகு-கேது தோஷம்'), esc(status(d.rahu_ketu?.present, false))],
    [txt('Kaal Sarp Dosham', 'கால சர்ப்ப தோஷம்'), esc(d.kaal_sarp?.present ? txt(d.kaal_sarp.type, d.kaal_sarp.type_ta) : txt('Not present', 'இல்லை'))],
    [txt('Papa points (L / C / S)', 'பாப புள்ளிகள் (ல / ச / சு)'), si.papa_points ? `${si.papa_points.total} (${si.papa_points.breakdown.map(b => b.points).join(' / ')})` : '—']
  ];
  const matching = [
    [txt('Nakshatra · Pada', 'நட்சத்திரம் · பாதம்'), `${esc(starName(c.planets.Moon.nakshatra))} · ${c.planets.Moon.pada}`],
    [txt('Rasi', 'ராசி'), pjSign(c.planets.Moon.sign_index)],
    [txt('Gana · Yoni', 'கணம் · யோனி'), esc(txt(`${star.gana} · ${star.yoni}`, `${star.gana_ta} · ${star.yoni_ta}`))],
    [txt('Rajju · Nadi', 'ரஜ்ஜு · நாடி'), esc(txt(`${star.rajju} · ${star.nadi}`, `${star.rajju_ta} · ${star.nadi_ta}`))]
  ];
  const yogas = (c.yogas || []).map(y => [`<strong>${esc(txt(y.name, y.name_ta))}</strong>`, esc(txt(y.description, y.description_ta))]);
  return `
    <div class="pj-two">
      <div><h3>${txt('Doshas', 'தோஷங்கள்')}</h3><div class="pj-grid one">${pjKV(doshas)}</div></div>
      <div><h3>${txt('For marriage matching', 'திருமணப் பொருத்தத்திற்கு')}</h3><div class="pj-grid one">${pjKV(matching)}</div></div>
    </div>
    <h3>${txt('Yogas', 'யோகங்கள்')}</h3>
    ${yogas.length ? pjTable([txt('Yoga', 'யோகம்'), txt('Meaning', 'பலன்')], yogas) : `<p>${txt('No major yoga found.', 'முக்கிய யோகம் இல்லை.')}</p>`}`;
}

function printDasa(c) {
  const blocks = c.dasha.map(md => `
    <div class="pj-dasa-block${md.is_active ? ' active' : ''}">
      <strong>${esc(txt(`${md.lord} Maha Dasa`, `${grahaName(md.lord)} மகா தசை`))}</strong>
      <span>${pjDate(md.start)} → ${pjDate(md.end)}</span>
      <ul>${md.subperiods.map(b => `<li class="${b.is_active ? 'active' : ''}"><span>${esc(grahaName(b.lord))}</span><em>${pjDate(b.start)}</em></li>`).join('')}</ul>
    </div>`).join('');
  const yogini = (c.yogini_dasha || []).slice(0, 12).map(y => [
    esc(txt(y.yogini, y.yogini_ta)), esc(grahaName(y.lord)), `${y.years}`, pjDate(y.start), pjDate(y.end)]);
  return `
    <p class="pj-note">${txt('Vimshottari Maha Dasas with the start date of each Bhukti; the running periods are marked. Dates are at the birthplace.',
      'விம்சோத்தரி மகா தசைகளும் ஒவ்வொரு புக்தியின் தொடக்க நாளும்; நடப்பு காலங்கள் குறிக்கப்பட்டுள்ளன. தேதிகள் பிறந்த ஊர் நேரப்படி.')}</p>
    <div class="pj-dasa-grid">${blocks}</div>
    ${yogini.length ? `<h3>${txt('Yogini Dasa', 'யோகினி தசை')}</h3>${pjTable([txt('Yogini', 'யோகினி'), txt('Lord', 'அதிபதி'),
      txt('Years', 'ஆண்டுகள்'), txt('From', 'முதல்'), txt('To', 'வரை')], yogini, 'compact')}` : ''}`;
}

function printOtherDasas(c) {
  const head = [txt('Dasa', 'தசை'), txt('Years', 'ஆண்டுகள்'), txt('From', 'முதல்'), txt('To', 'வரை')];
  const mark = (row, label) => row.is_active ? `<strong>${label} ●</strong>` : label;
  const ashtottari = (c.ashtottari_dasha || []).map(r => [mark(r, esc(grahaName(r.lord))), `${r.years}`, pjDate(r.start), pjDate(r.end)]);
  const chara = (c.chara_dasha || []).map(r => [
    mark(r, esc(txt(`${r.sign} (${r.lord})${r.round === 2 ? ' · 2' : ''}`, `${r.sign_ta} (${grahaName(r.lord)})${r.round === 2 ? ' · 2' : ''}`))),
    `${r.years}`, pjDate(r.start), pjDate(r.end)]);
  const applies = c.ashtottari_applicable
    ? txt('Ashtottari applies to this chart (Rahu in a kendra or trikona from the Lagna lord).', 'அஷ்டோத்தரி இந்த ஜாதகத்திற்குப் பொருந்தும் (ராகு லக்னாதிபதிக்குக் கேந்திர / திரிகோணத்தில்).')
    : txt('Ashtottari is shown for reference; its classical condition does not hold here.', 'அஷ்டோத்தரி குறிப்புக்காக மட்டும்; அதன் பாரம்பரிய நிபந்தனை இங்கு பொருந்தவில்லை.');
  const year = c.dasa_year ? txt(` Dasa year: ${c.dasa_year.en}.`, ` தசை ஆண்டு: ${c.dasa_year.ta}.`) : '';
  return `
    <p class="pj-note">${applies}${year} ${txt('Chara Dasa by K.N. Rao; "· 2" marks the second round. ● is the running period.',
      'சர தசை கே.என். ராவ் முறைப்படி; "· 2" இரண்டாம் சுற்று. ● நடப்பு காலம்.')}</p>
    <div class="pj-two">
      <div><h3>${txt('Ashtottari Dasa', 'அஷ்டோத்தரி தசை')}</h3>${pjTable(head, ashtottari, 'compact')}</div>
      <div><h3>${txt('Jaimini Chara Dasa', 'ஜைமினி சர தசை')}</h3>${pjTable(head, chara, 'compact')}</div>
    </div>`;
}

// The chapters in the shared report shape (numerology and the newer reports), one after another
function printReportChapters(c) {
  const pred = c.predictions || {};
  const cell = x => esc(txt(x.en, x.ta));
  return REPORT_CHAPTERS.filter(key => pred[key]).map(key => {
    const ch = pred[key];
    const tables = ch.tables.map(t => `<h4>${cell(t.title)}</h4>` + pjTable(t.head.map(cell), t.rows.map(row => row.map(cell)), 'compact')).join('');
    const grid = ch.grid ? `<div class="pj-chakra">${ch.grid.flat().map(g => `<div class="${esc(g.cls || '')}">${cell(g)}</div>`).join('')}</div>` : '';
    const cards = ch.cards.map(k => `<div class="pj-reading"><h4>${cell(k.title)}</h4><p>${cell(k.body)}</p></div>`).join('');
    return `<h3>${cell(ch.title)}</h3><p class="pj-note">${cell(ch.intro)}</p>${grid}${tables}${cards}`;
  }).join('');
}

function printVargas(c) {
  const keys = ['D2', 'D3', 'D4', 'D7', 'D10', 'D12', 'D16', 'D20', 'D24', 'D27', 'D30', 'D40', 'D45', 'D60'];
  const charts = keys.map(k => pjChart(k, `${k} · ${txt(VARGA_NAMES[k][0], VARGA_NAMES[k][1])}`)).join('');
  const all = ['D1', 'D2', 'D3', 'D4', 'D7', 'D9', 'D10', 'D12', 'D16', 'D20', 'D24', 'D27', 'D30', 'D40', 'D45', 'D60'];
  const rows = PRINT_GRAHAS.map(b => [`<strong>${esc(grahaName(b))}</strong>`, ...all.map(k => {
    const s = c.vargas[k]?.[b];
    if (s == null) return '—';
    const label = currentLang === 'ta' ? SIGNS_TA[s] : SIGNS_EN[s].slice(0, 3);
    return k !== 'D1' && s === c.vargas.D1[b] ? `<strong>${esc(label)}</strong>` : esc(label);
  })]);
  return `<div class="pj-varga-grid">${charts}</div>
    <h3>${txt('Shodasavarga table (bold: same sign as the Rasi)', 'ஷோடசவர்க்க அட்டவணை (தடித்த எழுத்து: இராசியின் அதே ராசி)')}</h3>
    ${pjTable([txt('Graha', 'கிரகம்'), ...all], rows, 'compact center')}`;
}

function printBhavas(c) {
  const bb = c.predictions?.shadbala?.bhavas || [];
  const { madhya = [], sandhi = [] } = c.bhava_chakra || {};
  const rows = madhya.map((m, i) => {
    const n = i + 1;
    const occupants = PRINT_GRAHAS.filter(g => g !== 'Ascendant' && c.planets[g].bhava === n).map(grahaName).join(', ');
    return [`<strong>${n}</strong>`, pjDeg(sandhi[(i + 11) % 12]), `<strong>${pjDeg(m)}</strong>`, pjDeg(sandhi[i]),
      bb[i] ? esc(grahaName(bb[i].lord)) : '—', esc(occupants || '—'), bb[i] ? `${bb[i].rupas}` : '—'];
  });
  return `<div class="pj-charts single">${pjChart('Bhava', txt('Bhava Chakra (Sripati)', 'பாவ சக்கரம் (ஸ்ரீபதி)'))}</div>
    ${pjTable([txt('Bhava', 'பாவம்'), txt('Begins (sandhi)', 'ஆரம்பம் (சந்தி)'), txt('Madhya', 'மத்தி'), txt('Ends (sandhi)', 'முடிவு (சந்தி)'),
      txt('Lord', 'அதிபதி'), txt('Grahas', 'கிரகங்கள்'), txt('Bhava Bala (rupas)', 'பாவ பலம் (ரூபம்)')], rows)}`;
}

function printStrength(c) {
  const sb = c.predictions?.shadbala;
  if (!sb) return '';
  const byPlanet = Object.fromEntries(sb.planets.map(p => [p.planet, p]));
  const rows = PRINT_SEVEN.map(n => byPlanet[n]).filter(Boolean).map(p => [
    `<strong>${esc(grahaName(p.planet))}</strong>`, p.sthana_bala, p.dig_bala, p.kaala_bala, p.chesta_bala, p.naisargika_bala, p.drik_bala,
    `<strong>${p.total_rupas}</strong>`, p.min_required_rupas, p.strength_ratio, p.ishta_phala, p.kashta_phala, p.rank]);
  const bhava = sb.bhavas || [];
  const vims = (sb.vimsopaka || []).map(v => [`<strong>${esc(grahaName(v.planet))}</strong>`,
    ...['shadvarga', 'saptavarga', 'dasavarga', 'shodasavarga'].map(k => `${v[k].score}${v[k].bheda_en ? ` · ${esc(txt(v[k].bheda_en, v[k].bheda_ta))}` : ''}`)]);
  return `
    <h3>${txt('Shadbala (virupas; totals in rupas)', 'ஷட்பலம் (விரூபம்; மொத்தம் ரூபத்தில்)')}</h3>
    ${pjTable([txt('Graha', 'கிரகம்'), txt('Sthana', 'ஸ்தான'), txt('Dig', 'திக்'), txt('Kaala', 'கால'), txt('Cheshta', 'சேஷ்டா'),
      txt('Naisargika', 'நைசர்கிக'), txt('Drik', 'திருக்'), txt('Rupas', 'ரூபம்'), txt('Required', 'தேவை'), txt('Ratio', 'விகிதம்'),
      txt('Ishta', 'இஷ்ட'), txt('Kashta', 'கஷ்ட'), txt('Rank', 'இடம்')], rows, 'compact center')}
    <h3>${txt('Bhava Bala (rupas; minimum 7)', 'பாவ பலம் (ரூபம்; குறைந்தபட்சம் 7)')}</h3>
    ${pjTable([txt('Bhava', 'பாவம்'), ...bhava.map(b => b.bhava)],
      [[txt('Lord', 'அதிபதி'), ...bhava.map(b => esc(grahaName(b.lord)))], [txt('Rupas', 'ரூபம்'), ...bhava.map(b => b.is_strong ? `<strong>${b.rupas}</strong>` : b.rupas)]],
      'compact center')}
    <h3>${txt('Vimsopaka Bala (out of 20) & Varga Bheda', 'விம்சோபக பலம் (20-க்கு) & வர்க்க பேதம்')}</h3>
    ${pjTable([txt('Graha', 'கிரகம்'), txt('Shadvarga', 'ஷட்வர்க்கம்'), txt('Saptavarga', 'சப்தவர்க்கம்'), txt('Dasavarga', 'தசவர்க்கம்'),
      txt('Shodasavarga', 'ஷோடசவர்க்கம்')], vims, 'compact')}`;
}

function printAshtakavarga(c) {
  const av = c.ashtakavarga;
  const signs = SIGNS_EN.map((s, i) => currentLang === 'ta' ? SIGNS_TA[i] : s.slice(0, 3));
  const bav = PRINT_SEVEN.map(p => [`<strong>${esc(grahaName(p))}</strong>`, ...av.BAV[p], `<strong>${av.BAV[p].reduce((a, b) => a + b, 0)}</strong>`]);
  bav.push([`<strong>${txt('SAV', 'சர்வ')}</strong>`, ...av.SAV.map(v => `<strong>${v}</strong>`), `<strong>${av.total_points}</strong>`]);
  const sodhita = PRINT_SEVEN.map(p => [`<strong>${esc(grahaName(p))}</strong>`, ...(av.sodhita?.[p] || []),
    av.pindas?.[p]?.rasi ?? '—', av.pindas?.[p]?.graha ?? '—', `<strong>${av.pindas?.[p]?.sodhya ?? '—'}</strong>`]);
  return `
    <h3>${txt('Bhinnashtakavarga and Sarvashtakavarga', 'பின்னாஷ்டகவர்க்கம் & சர்வாஷ்டகவர்க்கம்')}</h3>
    ${pjTable([txt('Graha', 'கிரகம்'), ...signs, txt('Total', 'மொத்தம்')], bav, 'compact center')}
    <h3>${txt('After Trikona and Ekadhipatya reduction, with the Pindas', 'திரிகோண, ஏகாதிபத்ய சோதனைக்குப் பின் & பிண்டங்கள்')}</h3>
    ${pjTable([txt('Graha', 'கிரகம்'), ...signs, txt('Rasi P.', 'ராசி பி.'), txt('Graha P.', 'கிரக பி.'), txt('Sodhya P.', 'சோத்ய பி.')], sodhita, 'compact center')}`;
}

function printKP(c) {
  const kp = c.predictions?.kp_system;
  if (!kp) return '';
  const cusps = kp.cusps.map(r => [`<strong>${r.cusp}</strong>`, `${esc(txt(r.sign, r.sign_ta))} ${esc(r.degree_str)}`,
    esc(grahaName(r.sign_lord)), esc(grahaName(r.star_lord)), `<strong>${esc(grahaName(r.sub_lord))}</strong>`]);
  const planets = kp.planets.map(r => [`<strong>${esc(grahaName(r.planet))}</strong>`, `${esc(txt(r.sign, r.sign_ta))} ${esc(r.degree_str)}`,
    esc(grahaName(r.star_lord)), `<strong>${esc(grahaName(r.sub_lord))}</strong>`, r.kp_house ?? '—', (r.significations || []).join(', ')]);
  const verdicts = Object.values(kp.cuspal_predictions || {}).map(v => [esc(txt(v.title_en, v.title_ta)),
    `<strong>${esc(txt(v.verdict_en, v.verdict_ta))}</strong>`, esc(txt(v.reading_en, v.reading_ta))]);
  const ruling = (kp.ruling_planets || []).map(r => `${esc(txt(r.role_en, r.role_ta))}: <strong>${esc(grahaName(r.planet))}</strong>`).join(' · ');
  return `
    <p class="pj-note">${txt('Placidus cusps in the Krishnamurti ayanamsa', 'கிருஷ்ணமூர்த்தி அயனாம்சத்தில் பிளாசிடஸ் பாவ ஆரம்பங்கள்')}${kp.ayanamsa_degrees ? ` (${kp.ayanamsa_degrees}°)` : ''}.
      ${ruling ? `${txt('Ruling planets at birth', 'பிறப்பு ஆளும் கிரகங்கள்')}: ${ruling}` : ''}</p>
    <div class="pj-two">
      <div>${pjTable([txt('Cusp', 'பாவம்'), txt('Position', 'நிலை'), txt('Sign lord', 'ராசி அதிபதி'), txt('Star lord', 'நட்சத்திர அதிபதி'), txt('Sub lord', 'உப அதிபதி')], cusps, 'compact')}</div>
      <div>${pjTable([txt('Graha', 'கிரகம்'), txt('Position', 'நிலை'), txt('Star lord', 'நட்சத்திர அதிபதி'), txt('Sub lord', 'உப அதிபதி'), txt('House', 'பாவம்'), txt('Signifies', 'குறிப்பவை')], planets, 'compact')}</div>
    </div>
    <h3>${txt('Cuspal sub-lord verdicts', 'உப-அதிபதி தீர்ப்புகள்')}</h3>
    ${pjTable([txt('Matter', 'விஷயம்'), txt('Verdict', 'தீர்ப்பு'), txt('Reason', 'காரணம்')], verdicts, 'compact')}`;
}

function printPredictions(c) {
  const pred = c.predictions;
  if (!pred) return '';
  const ov = pred.overview || {};
  const para = (title, text) => text ? `<div class="pj-reading"><h4>${esc(title)}</h4><p>${esc(text)}</p></div>` : '';
  const phala = (pred.panchanga_phala || []).map(i => para(txt(i.title_en, i.title_ta), txt(i.reading_en, i.reading_ta))).join('');
  const bhavas = (pred.bhavas || []).map(b => para(
    `${txt(b.title_en, b.title_ta)} · ${txt(b.sign, b.tamil_sign)} · ${txt(b.strength, b.strength_ta)}`, txt(b.prediction_en, b.prediction_ta))).join('');
  const tr = pred.transits || {};
  const transits = ['saturn', 'jupiter', 'rahu_ketu'].map(k => tr[k] ? para(txt(tr[k].title_en, tr[k].title_ta), txt(tr[k].prediction_en, tr[k].prediction_ta)) : '').join('');
  const ayur = pred.ayur_jyotish;
  return `
    <h3>${txt('Panchanga Phala', 'பஞ்சாங்க பலன்')}</h3>${phala}
    <h3>${txt('Birth star and Lagna', 'ஜன்ம நட்சத்திரம் & லக்னம்')}</h3>
    ${para(starName(ov.nakshatra), txt(ov.nakshatra_pred_en, ov.nakshatra_pred_ta))}
    ${para(signName(ov.lagna), txt(ov.lagna_pred_en, ov.lagna_pred_ta))}
    <h3>${txt('The running Dasa', 'நடப்பு தசை')}</h3>
    ${para(txt('Dasa-Bhukti forecast', 'தசா புக்தி பலன்'), txt(pred.dasa_forecast?.active_forecast_en, pred.dasa_forecast?.active_forecast_ta))}
    ${pred.sudarshana ? para(txt('Sudarshana Chakra this year', 'இந்த ஆண்டு சுதர்சன சக்கரம்'), txt(pred.sudarshana.reading_en, pred.sudarshana.reading_ta)) : ''}
    <h3>${txt('Transits (Gochara)', 'கோச்சாரம்')}</h3>${transits}
    <h3>${txt('Career and health', 'தொழில் & உடல்நலம்')}</h3>
    ${para(txt('Career (Karmajeeva & D-10)', 'தொழில் (கர்மஜீவம் & D-10)'), txt(pred.career_d10?.narrative_en, pred.career_d10?.narrative_ta))}
    ${ayur ? para(txt(`Constitution: ${ayur.prakriti_en}`, `உடலமைப்பு: ${ayur.prakriti_ta}`), txt(ayur.lifestyle_guidance_en, ayur.lifestyle_guidance_ta)) : ''}
    <h3 class="pj-break">${txt('The twelve Bhavas', '12 பாவங்கள்')}</h3>${bhavas}`;
}

// ---------- assembling and printing ----------
function buildPrintReport(presetKey, sectionKeys, chartStyle = 'south') {
  const c = currentChart;
  printChartStyle = PRINT_CHART_STYLES[chartStyle] ? chartStyle : 'south';
  const preset = PRINT_PRESETS[presetKey] || PRINT_PRESETS.jathagam;
  const prof = c.profile;
  pendingCharts = [];
  const chosen = PRINT_SECTIONS.filter(s => sectionKeys.includes(s.key));
  const body = chosen.map((s, i) => {
    const html = s.build(c);
    if (!html) return '';
    return `<section class="pj-section${s.newPage && i > 0 ? ' pj-page' : ''}" data-section="${s.key}">
      <h2><span class="pj-num">${i + 1}</span>${esc(txt(s.en, s.ta))}</h2>${html}</section>`;
  }).join('');
  const title = txt(preset.title_en, preset.title_ta);
  $('#print-jathagam').dataset.lang = currentLang;
  $('#print-jathagam').innerHTML = `
    <header class="pj-header">
      <div class="pj-om">ௐ</div>
      <h1>${esc(title)}</h1>
      <p class="pj-name">${esc(prof.name || '')}</p>
      <p class="pj-sub">${esc(prof.date)} · ${esc(prof.time)}${prof.city ? ` · ${esc(prof.city)}` : ''}</p>
      ${chosen.length > 5 ? `<p class="pj-contents">${chosen.map((s, i) => `${i + 1}. ${esc(txt(s.en, s.ta))}`).join(' &nbsp;·&nbsp; ')}</p>` : ''}
    </header>
    ${body}
    <footer class="pj-footer">${esc(txt(
      `Calculated by JoRoScope with the Swiss Ephemeris · ${ayanamsaLabel(prof.ayanamsa)} ayanamsa · printed ${new Date().toLocaleDateString('en-GB')}. Readings are traditional guidance; consult an astrologer for important decisions.`,
      `ஜோரோஸ்கோப் சுவிஸ் எபிமெரிஸ் கணிதம் · ${ayanamsaLabel(prof.ayanamsa)} அயனாம்சம் · அச்சிட்ட நாள் ${new Date().toLocaleDateString('ta-IN')}. பலன்கள் பாரம்பரிய வழிகாட்டுதல் மட்டுமே; முக்கிய முடிவுகளுக்கு ஜோதிடரை அணுகவும்.`))}</footer>`;
  pendingCharts.forEach(([id, varga]) => {
    const el = document.getElementById(id);
    if (!el) return;
    if (printChartStyle === 'south') renderSouthChart(el, varga, true);
    else if (printChartStyle === 'east') renderEastChart(el, varga, { print: true });
    else renderDiamondChart(el, varga, { mirror: printChartStyle === 'srilanka', print: true });
  });
  setPrintPageStyle(`${title} · ${prof.name || ''}`);
}

// Running header and page numbers (CSS page margin boxes; ignored where unsupported)
function setPrintPageStyle(heading) {
  let style = document.getElementById('print-page-style');
  if (!style) {
    style = document.createElement('style');
    style.id = 'print-page-style';
    document.head.append(style);
  }
  const quote = s => `"${String(s).replace(/["\\\n\r]/g, ' ')}"`;
  const page = txt('Page', 'பக்கம்');
  style.textContent = `@media print { @page {
    size: A4; margin: 14mm 12mm 15mm;
    @top-left { content: ${quote(heading)}; font-size: 8pt; color: #666666; }
    @top-right { content: "JoRoScope"; font-size: 8pt; color: #666666; }
    @bottom-center { content: ${quote(page)} " " counter(page) " / " counter(pages); font-size: 8pt; color: #666666; }
  } }`;
}

function printWithLanguage(lang, build) {
  const saved = currentLang;
  currentLang = lang || saved;
  try {
    build();
    if (currentLang === 'ml') translateTree(document.getElementById('print-jathagam'));
  } finally {
    currentLang = saved;
  }
  document.body.classList.add('printing-jathagam');
  // Let the dialog close and the sheet lay out before the print window opens
  setTimeout(() => window.print(), 60);
}

// ---------- dialog ----------
function openPrintDialog(presetKey = 'jathagam') {
  if (!currentChart) {
    notify(txt('Generate a chart first.', 'முதலில் ஜாதகம் கணிக்கவும்.'));
    return;
  }
  const dialog = $('#print-dialog');
  $('#print-presets').innerHTML = `<legend>${txt('Report', 'அறிக்கை')}</legend>` + Object.entries(PRINT_PRESETS).map(([key, p]) => `
    <label class="print-preset">
      <input type="radio" name="print-preset" value="${key}" ${key === presetKey ? 'checked' : ''}>
      <span><strong>${esc(txt(p.en, p.ta))}</strong><small>${esc(txt(p.hint_en, p.hint_ta))}</small></span>
    </label>`).join('');
  const list = $('#print-section-list');
  const tick = key => {
    const wanted = PRINT_PRESETS[key].sections;
    list.querySelectorAll('input').forEach(box => { box.checked = wanted.includes(box.value); });
  };
  list.innerHTML = PRINT_SECTIONS.map(s => `
    <label><input type="checkbox" value="${s.key}"> ${esc(txt(s.en, s.ta))}</label>`).join('');
  tick(presetKey);
  $$('#print-presets input').forEach(radio => radio.addEventListener('change', () => tick(radio.value)));
  $('#print-language').value = currentLang;
  const styleSelect = $('#print-chart-style');
  if (styleSelect) {
    const chosen = styleSelect.value || (['north', 'east', 'srilanka'].includes(currentStyle) ? currentStyle : 'south');
    styleSelect.innerHTML = Object.entries(PRINT_CHART_STYLES).map(([key, [en, ta]]) =>
      `<option value="${key}">${esc(txt(en, ta))}</option>`).join('');
    styleSelect.value = chosen;
  }
  dialog.showModal();
}

function submitPrintDialog(event) {
  event.preventDefault();
  const preset = $('#print-presets input:checked')?.value || 'jathagam';
  const sections = [...$$('#print-section-list input:checked')].map(b => b.value);
  const lang = $('#print-language').value;
  const chartStyle = $('#print-chart-style')?.value || 'south';
  $('#print-dialog').close();
  if (!sections.length) {
    notify(txt('Choose at least one section.', 'குறைந்தது ஒரு பகுதியைத் தேர்ந்தெடுக்கவும்.'));
    return;
  }
  printWithLanguage(lang, () => buildPrintReport(preset, sections, chartStyle));
}

// The header Print button: a Porutham report on the matching page, the report dialog for a
// chart, and the page itself elsewhere (the daily panchangam, saved profiles)
function printCurrentView() {
  const active = [...$$('.app-page')].find(p => !p.hidden)?.id;
  if (active === 'page-matching' && lastMatch) return printPorutham();
  if (currentChart && !['page-panchangam', 'page-profiles', 'page-matching'].includes(active)) return openPrintDialog('detailed');
  window.print();
}

// ---------- Porutham report ----------
function buildPoruthamSheet(match) {
  const person = p => [
    [txt('Name', 'பெயர்'), esc(p.name || '—')],
    [txt('Nakshatra', 'நட்சத்திரம்'), esc(txt(p.nakshatra, p.nakshatra_ta) + (p.pada ? ` · ${txt('Pada', 'பாதம்')} ${p.pada}` : ''))],
    [txt('Rasi', 'ராசி'), esc(txt(p.sign, p.sign_ta))],
    [txt('Lagna', 'லக்னம்'), esc(p.lagna ? txt(p.lagna, p.lagna_ta) : '—')],
    [txt('Gana · Yoni', 'கணம் · யோனி'), esc(`${txt(p.gana, p.gana_ta)} · ${txt(p.yoni, p.yoni_ta)}`)],
    [txt('Rajju · Nadi', 'ரஜ்ஜு · நாடி'), esc(`${txt(p.rajju, p.rajju_ta)} · ${txt(p.nadi, p.nadi_ta)}`)]
  ];
  const poruthams = match.poruthams.map(p => [`<strong>${esc(txt(p.name, p.tamil))}</strong>`, esc(txt(p.description, p.description_ta)),
    `<span class="pj-nowrap">${p.passed ? txt('Yes ✔', 'உண்டு ✔') : txt('No ✖', 'இல்லை ✖')}</span>`,
    `<span class="pj-nowrap">${p.points} / ${p.max_points}</span>`]);
  const g = match.guna_milan;
  const gunas = GUNA_LABELS.map(([key, max, en, ta]) => [txt(en, ta), `${g[key]} / ${max}`]);
  const samyam = match.dosha_samyam ? `
    <section class="pj-section"><h2><span class="pj-num">3</span>${txt('Dosha Samyam', 'தோஷ சாம்யம்')}</h2>
      <table class="pj-table">
        <thead><tr><th>${txt('Dosha', 'தோஷம்')}</th><th>${txt('Bride', 'பெண்')}</th><th>${txt('Groom', 'ஆண்')}</th><th>${txt('Samyam', 'சாம்யம்')}</th></tr></thead>
        <tbody>${$('#dosha-samyam-tbody').innerHTML}</tbody>
      </table>
    </section>` : '';
  $('#print-jathagam').dataset.lang = currentLang;
  $('#print-jathagam').innerHTML = `
    <header class="pj-header">
      <div class="pj-om">ௐ</div>
      <h1>${txt('Marriage Compatibility Report', 'திருமணப் பொருத்த அறிக்கை')}</h1>
      ${[match.groom?.name, match.bride?.name].some(Boolean) ? `<p class="pj-name">${[match.groom?.name, match.bride?.name].filter(Boolean).map(esc).join(' · ')}</p>` : ''}
      <p class="pj-verdict">${esc(txt(match.verdict, match.verdict_ta))} · ${txt(`${match.passed_count} of 10 Poruthams`, `10-ல் ${match.passed_count} பொருத்தங்கள்`)} · ${txt('Guna', 'குணம்')} ${g.total_score} / 36</p>
      ${(match.verdict_notes || []).map(n => `<p class="pj-sub">⚠ ${esc(txt(n.en, n.ta))}</p>`).join('')}
    </header>
    <section class="pj-section"><h2><span class="pj-num">1</span>${txt('Birth stars', 'ஜன்ம நட்சத்திரங்கள்')}</h2>
      <div class="pj-two">
        <div><h3>${txt('Bride', 'மணமகள்')}</h3><div class="pj-grid one">${pjKV(person(match.bride))}</div></div>
        <div><h3>${txt('Groom', 'மணமகன்')}</h3><div class="pj-grid one">${pjKV(person(match.groom))}</div></div>
      </div>
    </section>
    <section class="pj-section"><h2><span class="pj-num">2</span>${txt('10 Poruthams', '10 பொருத்தங்கள்')}</h2>
      ${pjTable([txt('Porutham', 'பொருத்தம்'), txt('Significance', 'பலன்'), txt('Result', 'முடிவு'), txt('Points', 'மதிப்பெண்')], poruthams)}
    </section>
    ${samyam}
    <section class="pj-section"><h2><span class="pj-num">${match.dosha_samyam ? 4 : 3}</span>${txt('Ashta Koota (36 Gunas)', 'அஷ்ட கூடம் (36 குணங்கள்)')}</h2>
      <div class="pj-grid">${pjKV(gunas)}</div>
    </section>
    <footer class="pj-footer">${esc(txt(
      `Calculated by JoRoScope · printed ${new Date().toLocaleDateString('en-GB')} · Rules differ between traditions; consult an astrologer before deciding.`,
      `ஜோரோஸ்கோப் கணிதம் · அச்சிட்ட நாள் ${new Date().toLocaleDateString('ta-IN')} · மரபுக்கு மரபு விதிகள் வேறுபடும்; முடிவெடுக்கும் முன் ஜோதிடரை அணுகவும்.`))}</footer>`;
  setPrintPageStyle(txt('Marriage Compatibility Report', 'திருமணப் பொருத்த அறிக்கை'));
}

function printPorutham() {
  if (!lastMatch) return;
  buildPoruthamSheet(lastMatch);
  document.body.classList.add('printing-jathagam');
  window.print();
}

document.addEventListener('DOMContentLoaded', () => {
  $('#print-dialog-form')?.addEventListener('submit', submitPrintDialog);
  $('#print-dialog-cancel')?.addEventListener('click', () => $('#print-dialog').close());
});
