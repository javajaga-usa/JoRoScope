/**
 * Calendar export checks: RFC 5545 line endings, 75-byte folding that keeps Tamil characters whole,
 * escaping, UTC times for timed events and exclusive end dates for all-day events.
 */
const assert = require('assert');
const path = require('path');
const { buildIcs, icsFold } = require(path.join(__dirname, '..', 'src', 'joroscope', 'web', 'ics.js'));

const ics = buildIcs([
  { uid: 'm1', title: 'Muhurtham: Marriage, Vivaham; test', description: 'முகூர்த்தம் · ரோகிணி · சுக்ல பஞ்சமி · துலாம் லக்னம் · சித்த யோகம் · குரு / சுக்கிரன் கேந்திரத்தில்',
    start: '2026-10-30T06:01:12+05:30', end: '2026-10-30T07:20:00+05:30' },
  { uid: 'o1', title: 'Ekadasi', start: '2026-12-31' }
], 'JoRoScope test', new Date('2026-09-28T00:00:00Z'));

assert.ok(ics.startsWith('BEGIN:VCALENDAR\r\n') && ics.endsWith('END:VCALENDAR\r\n'));
assert.ok(!/[^\r]\n/.test(ics), 'every line ends with CRLF');
const physical = ics.split('\r\n').filter(Boolean);
physical.forEach(l => assert.ok(new TextEncoder().encode(l).length <= 75, `line over 75 bytes: ${l}`));
// Unfolding restores the Tamil description exactly
const unfolded = ics.replace(/\r\n /g, '');
assert.ok(unfolded.includes('DESCRIPTION:முகூர்த்தம் · ரோகிணி · சுக்ல பஞ்சமி · துலாம் லக்னம் · சித்த யோகம் · குரு / சுக்கிரன் கேந்திரத்தில்'));
assert.ok(unfolded.includes('SUMMARY:Muhurtham: Marriage\\, Vivaham\\; test'));
assert.ok(unfolded.includes('DTSTART:20261030T003112Z') && unfolded.includes('DTEND:20261030T015000Z'));
assert.ok(unfolded.includes('DTSTART;VALUE=DATE:20261231') && unfolded.includes('DTEND;VALUE=DATE:20270101'));
assert.strictEqual((unfolded.match(/BEGIN:VEVENT/g) || []).length, 2);
assert.strictEqual(icsFold('short'), 'short');
console.log('ALL CALENDAR EXPORT CHECKS PASSED!');
