/**
 * Markup checks: every element id in index.html is unique, and every data-i18n key used there
 * has English and Tamil text.
 */
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const web = path.join(__dirname, '..', 'src', 'joroscope', 'web');
const html = fs.readFileSync(path.join(web, 'index.html'), 'utf8');
const fail = msg => { console.error('FAIL: ' + msg); process.exit(1); };

const ids = [...html.matchAll(/\sid="([^"]+)"/g)].map(m => m[1]);
const dupes = [...new Set(ids.filter((id, i) => ids.indexOf(id) !== i))];
if (dupes.length) fail(`duplicate ids in index.html: ${dupes.join(', ')}`);
console.log(`PASS: ${ids.length} unique element ids`);

const ctx = {};
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(path.join(web, 'i18n.js'), 'utf8') + '\n;this.I18N = I18N;', ctx);
const keys = [...new Set([...html.matchAll(/data-i18n(?:-placeholder|-title)?="([^"]+)"/g)].map(m => m[1]))];
const missing = keys.filter(k => !ctx.I18N.en[k] || !ctx.I18N.ta[k]);
if (missing.length) fail(`i18n keys without English and Tamil text: ${missing.join(', ')}`);
console.log(`PASS: ${keys.length} data-i18n keys have English and Tamil text`);
console.log('ALL MARKUP CHECKS PASSED!');
