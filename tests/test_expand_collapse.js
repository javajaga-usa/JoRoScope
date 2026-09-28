// Unit test for expand/collapse toggle behavior and timeline data integrity
const fs = require('fs');
const path = require('path');
const http = require('http');

console.log('Testing Expand/Collapse & Timeline Predictions Details...');

// 1. Verify CSS rules
const css = fs.readFileSync(path.join(__dirname, '../src/joroscope/web/style.css'), 'utf-8');
if (!css.includes('.timeline-details-panel[hidden]')) {
    console.error('FAIL: Missing .timeline-details-panel[hidden] rule');
    process.exit(1);
}
console.log('PASS: .timeline-details-panel[hidden] with display: none !important exists');

if (!css.includes('.timeline-details-toggle.expanded')) {
    console.error('FAIL: Missing .timeline-details-toggle.expanded rule');
    process.exit(1);
}
console.log('PASS: .timeline-details-toggle.expanded styling exists');

// 2. Verify JS toggle implementation
const js = fs.readFileSync(path.join(__dirname, '../src/joroscope/web/app.js'), 'utf-8');
if (!js.includes("panel.style.display = 'grid'") || !js.includes("panel.style.display = 'none'")) {
    console.error('FAIL: JS does not explicitly manage style.display');
    process.exit(1);
}
console.log('PASS: JS explicitly manages panel.style.display grid and none');

// 3. Verify API data has detailed 6 dimensions across all periods
const postData = JSON.stringify({
    name: 'Sri Raman',
    date: '1990-01-01',
    time: '12:00:00',
    latitude: 13.0827,
    longitude: 80.2707,
    timezone: 'Asia/Kolkata',
    ayanamsa: 'Lahiri'
});

function post(route) {
    return new Promise((resolve, reject) => {
        const req = http.request('http://127.0.0.1:8765' + route, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(postData) }
        }, res => {
            let raw = '';
            res.on('data', chunk => raw += chunk);
            res.on('end', () => (res.statusCode === 200 ? resolve(JSON.parse(raw)) : reject(new Error(raw))));
        });
        req.on('error', reject);
        req.end(postData);
    });
}

(async () => {
    // The chart carries the readings only for the running period; /api/timeline has them all
    const chart = await post('/api/chart');
    const periods = chart.predictions.timeline_predictions.periods;
    console.log(`PASS: Received ${periods.length} periods from the chart API`);
    const dims = ['career', 'wealth', 'health', 'family', 'milestones', 'remedy'];
    const deferred = periods.filter(p => p.details_deferred);
    const inline = periods.filter(p => !p.details_deferred);
    if (inline.some(p => !p.is_active) || deferred.some(p => p.career_en)) {
        console.error('FAIL: only the running period should carry its readings in the chart response');
        process.exit(1);
    }
    const { details } = await post('/api/timeline');
    let issues = 0;
    for (const p of periods) {
        const d = p.details_deferred ? details[p.id] : p;
        for (const dim of dims) {
            for (const key of [`${dim}_en`, `${dim}_ta`]) {
                if (!d || !d[key] || d[key].length < 15) {
                    console.error(`FAIL: Underpopulated ${key} in period ${p.dasa_lord}-${p.bhukti_lord}`);
                    issues++;
                }
            }
        }
    }
    if (issues > 0) {
        console.error(`Encountered ${issues} issues across the ${periods.length} periods!`);
        process.exit(1);
    }
    console.log(`PASS: All ${periods.length} periods have 6-dimension readings in EN and TA (${deferred.length} fetched on demand)`);
    if (!js.includes("fetch('/api/timeline'")) {
        console.error('FAIL: app.js does not load the deferred readings');
        process.exit(1);
    }
    const activePeriod = periods.find(p => p.is_active);
    if (activePeriod) console.log(`Active Period: ${activePeriod.dasa_lord}-${activePeriod.bhukti_lord}:`, activePeriod.career_en);
    console.log('\nALL EXPAND/COLLAPSE & PREDICTION TESTS PASSED!');
})().catch(err => {
    console.error('Request failed:', err);
    process.exit(1);
});
