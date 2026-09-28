/**
 * Print report checks: the dialog is in the page, print.js loads after app.js, and every
 * preset builds from a real chart and match (from the running server) in English and Tamil
 * without "undefined", "NaN" or "[object Object]" leaking onto the paper.
 */
const fs = require('fs');
const path = require('path');
const http = require('http');
const vm = require('vm');

const web = path.join(__dirname, '..', 'src', 'joroscope', 'web');
const html = fs.readFileSync(path.join(web, 'index.html'), 'utf8');
const printJs = fs.readFileSync(path.join(web, 'print.js'), 'utf8');

function fail(msg) {
  console.error('FAIL: ' + msg);
  process.exit(1);
}

['print-dialog', 'print-dialog-form', 'print-presets', 'print-section-list', 'print-language', 'print-jathagam']
  .forEach(id => { if (!html.includes(`id="${id}"`)) fail(`index.html lacks #${id}`); });
if (html.indexOf('src="print.js"') < html.indexOf('src="app.js"')) fail('print.js must load after app.js');
console.log('PASS: print dialog markup and script order');

function post(route, body) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify(body);
    const req = http.request({ host: '127.0.0.1', port: 8765, path: route, method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(data) } }, res => {
      let out = '';
      res.on('data', c => { out += c; });
      res.on('end', () => (res.statusCode === 200 ? resolve(JSON.parse(out)) : reject(new Error(out))));
    });
    req.on('error', reject);
    req.end(data);
  });
}

function sandbox(chart, match, lang) {
  const elements = {};
  const drawn = [];
  const el = id => (elements[id] = elements[id] || { id, innerHTML: '', textContent: '', dataset: {} });
  const signsEn = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'];
  const signsTa = ['மேஷம்', 'ரிஷபம்', 'மிதுனம்', 'கடகம்', 'சிம்மம்', 'கன்னி', 'துலாம்', 'விருச்சிகம்', 'தனுசு', 'மகரம்', 'கும்பம்', 'மீனம்'];
  const ctx = {
    currentChart: chart, lastMatch: match, currentLang: lang,
    txt: (en, ta) => (ctx.currentLang === 'ta' ? ta : en),
    esc: s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c])),
    grahaName: n => n, signName: i => (typeof i === 'number' ? signsEn[i] : i), starName: s => s,
    dignityLabel: d => d || 'Neutral', ayanamsaLabel: a => a, formatDegrees: v => `${Number(v).toFixed(2)}°`,
    localDate: iso => String(iso).slice(0, 10), clockTime: iso => String(iso).slice(11, 16),
    kurippuRows: () => [['Tamil Year', 'x'], ['Vaaram', 'y']], dasaIrruppuText: () => 'Mars · 0y 1m 8d',
    renderSouthChart: (el, varga) => { drawn.push(['south', el.id, varga]); },
    renderDiamondChart: (el, varga, opts) => { drawn.push([opts && opts.mirror ? 'srilanka' : 'north', el.id, varga]); },
    renderEastChart: (el, varga) => { drawn.push(['east', el.id, varga]); },
    currentStyle: 'south', REPORT_CHAPTERS: ['numerology'], notify: () => {}, SIGNS_EN: signsEn, SIGNS_TA: signsTa,
    VARGA_NAMES: new Proxy({}, { get: (_, k) => [String(k), String(k)] }),
    GUNA_LABELS: [['varna', 1, 'Varna', 'வர்ணம்'], ['nadi', 8, 'Nadi', 'நாடி']],
    $: sel => el(sel.replace(/^#/, '')), $$: () => [],
    document: {
      getElementById: id => elements[id] || (id.startsWith('pj-chart-') ? el(id) : null), head: { append: node => { elements[node.id] = node; } },
      createElement: () => ({ id: '', textContent: '' }), addEventListener: () => {}, body: { classList: { add() {}, remove() {} } }
    },
    Date, window: { print() {} }, setTimeout
  };
  vm.createContext(ctx);
  vm.runInContext(printJs + '\n;this.__print = { buildPrintReport, buildPoruthamSheet, PRINT_SECTIONS, PRINT_PRESETS };', ctx);
  return { ctx, drawn, sheet: () => el('print-jathagam').innerHTML, pageStyle: () => (elements['print-page-style'] || {}).textContent || '' };
}

function assertClean(html, label) {
  for (const bad of ['undefined', 'NaN', '[object Object]', 'null']) {
    if (html.includes(bad)) {
      const at = html.indexOf(bad);
      fail(`${label}: "${bad}" in the report near …${html.slice(Math.max(0, at - 80), at + 40)}…`);
    }
  }
}

(async () => {
  const birth = { name: 'Print Test', date: '1990-01-01', time: '12:00:00', timezone: 'Asia/Kolkata', city: 'Chennai',
    latitude: 13.0827, longitude: 80.2707, ayanamsa: 'Lahiri' };
  const chart = await post('/api/chart', birth);
  const match = await post('/api/match', { boy: birth, girl: { ...birth, name: 'Bride', date: '1993-05-20', time: '07:30:00' } });

  for (const lang of ['en', 'ta']) {
    const { ctx, drawn, sheet, pageStyle } = sandbox(chart, match, lang);
    const api = ctx.__print;
    for (const [key, preset] of Object.entries(api.PRINT_PRESETS)) {
      api.buildPrintReport(key, preset.sections);
      const out = sheet();
      assertClean(out, `${lang}/${key}`);
      const count = (out.match(/class="pj-section/g) || []).length;
      if (count !== preset.sections.length) fail(`${lang}/${key}: ${count} sections, expected ${preset.sections.length}`);
      if (!pageStyle().includes('counter(page)')) fail(`${lang}/${key}: no page numbering style`);
    }
    const complete = sheet();
    ['Navamsa', 'D60', 'Sodhya', 'Vimsopaka', 'Bhava'].forEach(word => {
      if (lang === 'en' && !complete.includes(word)) fail(`complete report lacks ${word}`);
    });
    // Every chart style draws each chart once, into SVG for the non-grid styles
    for (const style of ['north', 'east', 'srilanka', 'south']) {
      drawn.length = 0;
      api.buildPrintReport('jathagam', api.PRINT_PRESETS.jathagam.sections, style);
      const out = sheet();
      if (drawn.length !== 2 || drawn.some(([kind]) => kind !== style)) fail(`${lang}/${style}: charts drawn as ${JSON.stringify(drawn)}`);
      if (style !== 'south' && !out.includes('class="pj-svg-chart"')) fail(`${lang}/${style}: no SVG chart in the sheet`);
    }
    api.buildPoruthamSheet(match);
    assertClean(sheet(), `${lang}/porutham`);
    console.log(`PASS: ${lang} reports (Traditional, Detailed, Complete) and the Porutham report build cleanly`);
  }
  console.log('ALL PRINT REPORT CHECKS PASSED!');
})().catch(err => fail(err.stack || String(err)));
