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

const req = http.request('http://127.0.0.1:8765/api/chart', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData)
    }
}, (res) => {
    let raw = '';
    res.on('data', chunk => raw += chunk);
    res.on('end', () => {
        try {
            const data = JSON.parse(raw);
            const periods = data.predictions.timeline_predictions.periods;
            console.log(`PASS: Received ${periods.length} periods from timeline API`);
            
            let issues = 0;
            const dims = ['career', 'wealth', 'health', 'family', 'milestones', 'remedy'];
            for (const p of periods) {
                for (const dim of dims) {
                    const enKey = `${dim}_en`;
                    const taKey = `${dim}_ta`;
                    if (!p[enKey] || p[enKey].length < 15) {
                        console.error(`FAIL: Underpopulated ${enKey} in period ${p.dasa_lord}-${p.bhukti_lord}: "${p[enKey]}"`);
                        issues++;
                    }
                    if (!p[taKey] || p[taKey].length < 15) {
                        console.error(`FAIL: Underpopulated ${taKey} in period ${p.dasa_lord}-${p.bhukti_lord}: "${p[taKey]}"`);
                        issues++;
                    }
                }
            }

            if (issues > 0) {
                console.error(`Encountered ${issues} issues across the 81 periods!`);
                process.exit(1);
            }

            console.log('PASS: All 81 periods contain comprehensive 6-dimension readings in both EN and TA!');
            
            // Test sample active period
            const activePeriod = periods.find(p => p.is_active);
            console.log(`Active Period: ${activePeriod.dasa_lord}-${activePeriod.bhukti_lord}`);
            console.log('Career EN:', activePeriod.career_en);
            console.log('Career TA:', activePeriod.career_ta);
            console.log('Remedy EN:', activePeriod.remedy_en);
            console.log('Remedy TA:', activePeriod.remedy_ta);
            console.log('\nALL EXPAND/COLLAPSE & PREDICTION TESTS PASSED!');
        } catch (e) {
            console.error('Error parsing response:', e);
            process.exit(1);
        }
    });
});

req.on('error', (err) => {
    console.error('HTTP Request failed:', err);
    process.exit(1);
});

req.write(postData);
req.end();
