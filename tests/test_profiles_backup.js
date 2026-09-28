/**
 * Profile backup checks: an export round-trips, older bare-array backups import, bad entries are
 * rejected with a reason, and newer copies replace older ones while unchanged ones are kept.
 */
const assert = require('assert');
const path = require('path');
const { profileBackup, cleanProfile, mergeProfileBackup } = require(path.join(__dirname, '..', 'src', 'joroscope', 'web', 'profiles.js'));

const raman = {
  id: 'seed-raman-1990', name: 'Sri Raman', date: '1990-01-01', time: '12:00:00', city: 'Chennai (Madras)',
  latitude: 13.0827, longitude: 80.2707, timezone: 'Asia/Kolkata', ayanamsa: 'Lahiri', fold: '', dasa_year: 'julian',
  nakshatra: 'Dhanishtha', nakshatra_idx: 22, sign_idx: 10, pada: 4, created_at: '2026-01-01T12:00:00.000Z'
};
let n = 0;
const makeId = () => `new-${++n}`;

// Export and import back: nothing new, nothing lost
const backup = JSON.parse(JSON.stringify(profileBackup([raman], new Date('2026-09-28T00:00:00Z'))));
assert.strictEqual(backup.app, 'JoRoScope');
assert.strictEqual(backup.count, 1);
let r = mergeProfileBackup(backup, [raman], makeId);
assert.deepStrictEqual([r.added, r.updated, r.unchanged, r.rejected.length], [0, 0, 1, 0]);
console.log('PASS: an export imports back without duplicates');

// A bare array from an old version, with times without seconds and no id
r = mergeProfileBackup([{ name: 'Meena', date: '1993-05-20', time: '07:30', latitude: '9.9252', longitude: 78.1198 }], [raman], makeId);
assert.strictEqual(r.added, 1);
const meena = r.merged[0];
assert.deepStrictEqual([meena.id, meena.time, meena.latitude, meena.ayanamsa, meena.dasa_year], ['new-1', '07:30:00', 9.9252, 'Lahiri', 'julian']);
console.log('PASS: legacy array backups import, filling defaults');

// Bad entries are skipped with reasons; unknown fields and markup-bearing extras are dropped
r = mergeProfileBackup({ profiles: [
  { name: '', date: '1990-01-01', time: '12:00', latitude: 1, longitude: 1 },
  { name: 'Feb30', date: '1990-02-30', time: '12:00', latitude: 1, longitude: 1 },
  { name: 'Late', date: '1990-01-01', time: '25:00', latitude: 1, longitude: 1 },
  { name: 'Far', date: '1990-01-01', time: '12:00', latitude: 95, longitude: 1 },
  'text',
  { name: 'Ok', date: '2001-03-04', time: '05:06:07', latitude: -33.9, longitude: 18.4, ayanamsa: 'Bogus', evil: '<img src=x>', sign_idx: 99 }
] }, [], makeId);
assert.strictEqual(r.added, 1);
assert.strictEqual(r.rejected.length, 5);
assert.ok(r.rejected.some(x => x.includes('Feb30')) && r.rejected.some(x => x.includes('Late')));
const ok = r.merged[0];
assert.strictEqual(ok.evil, undefined);
assert.strictEqual(ok.ayanamsa, 'Lahiri');
assert.strictEqual(ok.sign_idx, undefined);
console.log('PASS: invalid profiles are rejected with reasons and fields are sanitised');

// A newer copy of the same person replaces the saved one; an older copy does not
const edited = { ...raman, city: 'Madurai', updated_at: '2026-05-01T00:00:00.000Z' };
r = mergeProfileBackup({ app: 'JoRoScope', profiles: [edited] }, [raman], makeId);
assert.deepStrictEqual([r.updated, r.merged[0].city, r.merged.length], [1, 'Madurai', 1]);
r = mergeProfileBackup({ app: 'JoRoScope', profiles: [raman] }, [edited], makeId);
assert.deepStrictEqual([r.unchanged, r.merged[0].city], [1, 'Madurai']);
console.log('PASS: newer copies update saved profiles, older ones do not');

assert.throws(() => mergeProfileBackup({ hello: 1 }, [], makeId), /not a JoRoScope profile backup/);
assert.throws(() => mergeProfileBackup({ app: 'Other', profiles: [] }, [], makeId), /another application/);
assert.strictEqual(cleanProfile(null)[0], null);
console.log('PASS: foreign files are refused');
console.log('ALL PROFILE BACKUP CHECKS PASSED!');
