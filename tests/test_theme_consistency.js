// Test suite for JoRoScope Theme Consistency & Styling Integrity
const fs = require('fs');
const path = require('path');
const assert = require('assert');

console.log('--- Verifying CSS Tokens & Theme Rules in style.css ---');
const cssPath = path.join(__dirname, '..', 'src', 'joroscope', 'web', 'style.css');
const cssContent = fs.readFileSync(cssPath, 'utf8');

const requiredTokens = [
  '--bg-space',
  '--bg-deep',
  '--bg-card',
  '--bg-subtle',
  '--bg-subtle-hover',
  '--border-divider',
  '--track-bg',
  '--table-header-bg',
  '--hero-card-bg',
  '--gold-stat-bg',
  '--active-card-bg',
  '--annual-card-current-bg',
  '--text-primary',
  '--text-main',
  '--text-secondary',
  '--text-muted'
];

// Verify each token is defined in both :root and [data-theme="light"]
const rootMatch = cssContent.match(/:root\s*\{([^}]+)\}/);
assert(rootMatch, 'Could not find :root declaration in style.css');
const rootBlock = rootMatch[1];

const lightMatch = cssContent.match(/\[data-theme="light"\]\s*\{([^}]+)\}/);
assert(lightMatch, 'Could not find [data-theme="light"] declaration in style.css');
const lightBlock = lightMatch[1];

for (const token of requiredTokens) {
  assert(rootBlock.includes(token), `:root missing design token ${token}`);
  assert(lightBlock.includes(token), `[data-theme="light"] missing design token ${token}`);
  console.log(`[PASS] Token '${token}' defined in both Dark and Light themes`);
}

// Check that no hardcoded rgba(255, 255, 255) exists in component rules
const lines = cssContent.split('\n');
let outsideRootRgba255Count = 0;
let inRoot = false;
let inLight = false;

for (let i = 0; i < lines.length; i++) {
  const line = lines[i];
  if (line.includes(':root {')) inRoot = true;
  if (line.includes('[data-theme="light"] {')) inLight = true;
  if (inRoot && line.includes('}')) inRoot = false;
  if (inLight && line.includes('}')) inLight = false;

  if (!inRoot && !inLight && line.includes('rgba(255, 255, 255')) {
    console.error(`[FAIL] Hardcoded rgba(255, 255, 255) found on line ${i + 1}: ${line.trim()}`);
    outsideRootRgba255Count++;
  }
}

assert.strictEqual(outsideRootRgba255Count, 0, 'Found hardcoded rgba(255, 255, 255) outside theme declarations');
console.log('[PASS] Zero hardcoded rgba(255, 255, 255) in component rules!');

// Check app.js for theme persistence & dynamic SVG contrast
console.log('\n--- Verifying app.js Theme Functionality ---');
const webDir = path.join(__dirname, '..', 'src', 'joroscope', 'web');
const jsContent = fs.readdirSync(webDir).filter(f => f.endsWith('.js')).map(f => fs.readFileSync(path.join(webDir, f), 'utf8')).join('\n');

assert(jsContent.includes("localStorage.setItem('joroscope_theme'"), 'localStorage persistence missing in app.js');
console.log('[PASS] localStorage persistence implemented');

assert(jsContent.includes("localStorage.getItem('joroscope_theme')"), 'localStorage retrieval missing in app.js');
console.log('[PASS] localStorage initialization implemented');

assert(/function chartPalette[\s\S]*?getAttribute\('data-theme'\) === 'light'/.test(jsContent), 'SVG dynamic theme detection missing in app.js');
console.log('[PASS] Dynamic SVG theme detection verified in chartPalette');

assert(jsContent.includes("signIdx + 1, print ? 20 : 14, pal.accent"), 'Dynamic sign text color missing in SVG renderer');
console.log('[PASS] Dynamic sign text color applied to SVG');

assert(jsContent.includes("line, size, pal.text"), 'Dynamic planet text color missing in SVG renderer');
console.log('[PASS] Dynamic planet text color applied to SVG');

console.log('\nALL THEME CONSISTENCY CHECKS PASSED SUCCESSFULLY!');
