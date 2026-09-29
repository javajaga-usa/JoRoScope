/**
 * Node script to verify timeline frontend DOM elements, API integration and logic
 */
const fs = require('fs');
const path = require('path');
const http = require('http');
// The running JoRoScope server to test against: JOROSCOPE_TEST_PORT, or the default 8765
const TEST_PORT = Number(process.env.JOROSCOPE_TEST_PORT) || 8765;

const htmlPath = path.join(__dirname, '..', 'src', 'joroscope', 'web', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');

const requiredIds = [
  'page-dasha',
  'btn-mode-timeline',
  'btn-mode-cycles',
  'dasa-timeline-view',
  'dasa-tabular-view',
  'timeline-spotlight-card',
  'spotlight-lords-title',
  'spotlight-period-theme',
  'spotlight-dates',
  'spotlight-age',
  'spotlight-elapsed',
  'spotlight-remaining',
  'spotlight-potency-badge',
  'spotlight-progress-bar',
  'spotlight-progress-text',
  'spotlight-advice-text',
  'spotlight-remedy-text',
  'timeline-planet-select',
  'timeline-jump-year',
  'timeline-jump-btn',
  'timeline-count-badge',
  'annual-milestones-section',
  'annual-projections-grid',
  'timeline-periods-stream',
  'btn-jump-to-timeline'
];

console.log('--- Verifying HTML Elements ---');
let allFound = true;
for (const id of requiredIds) {
  if (html.includes(`id="${id}"`)) {
    console.log(`[PASS] Found id="${id}"`);
  } else {
    console.error(`[FAIL] Missing id="${id}"`);
    allFound = false;
  }
}

if (!allFound) {
  process.exit(1);
}

console.log(`\n--- Verifying API Endpoint on http://127.0.0.1:${TEST_PORT}/api/chart ---`);
const postData = JSON.stringify({
  name: 'Sri Raman',
  date: '1990-01-01',
  time: '12:00:00',
  latitude: 13.0827,
  longitude: 80.2707,
  timezone: 'Asia/Kolkata',
  ayanamsa: 'Lahiri'
});

const req = http.request(`http://127.0.0.1:${TEST_PORT}/api/chart`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': Buffer.byteLength(postData)
  }
}, (res) => {
  let body = '';
  res.on('data', chunk => body += chunk);
  res.on('end', () => {
    try {
      const data = JSON.parse(body);
      const tp = data.predictions.timeline_predictions;
      console.log(`[PASS] Received timeline predictions! Total periods: ${tp.total_periods}`);
      console.log(`[PASS] Active Spotlight: ${tp.active_spotlight.dasa_lord} - ${tp.active_spotlight.bhukti_lord} (${tp.active_spotlight.percent}% complete)`);
      console.log(`[PASS] Strategic advice: ${tp.active_spotlight.strategic_advice_en}`);
      console.log(`[PASS] Annual Projections count: ${tp.annual_projections.length}`);
      console.log(`[PASS] Sample Period: ${tp.periods[0].dasa_lord}-${tp.periods[0].bhukti_lord} | Aspect: ${tp.periods[0].mutual_rel} | Stars: ${tp.periods[0].stars}`);
      console.log('\nALL VERIFICATIONS PASSED SUCCESSFULLY!');
    } catch (e) {
      console.error('[FAIL] Parsing response error:', e);
      process.exit(1);
    }
  });
});

req.on('error', (e) => {
  console.error('[FAIL] HTTP request error:', e);
  process.exit(1);
});

req.write(postData);
req.end();
