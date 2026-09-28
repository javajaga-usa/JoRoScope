/**
 * Saved-profile backups: the export file format and the checks an imported file goes through.
 * A backup is {app: 'JoRoScope', version, exported_at, profiles: [...]}; older backups that are a
 * bare array of profiles are accepted too. Every imported profile is validated and reduced to the
 * known fields, so a hand-edited or foreign file cannot put odd values into the vault.
 * Loaded before app.js; also required by the Node tests.
 */
const PROFILE_BACKUP_VERSION = 3;
const PROFILE_LIMIT = 5000;
const PROFILE_TEXT_FIELDS = ['name', 'city', 'timezone', 'lagna', 'lagna_ta', 'moon_sign', 'moon_sign_ta', 'nakshatra', 'nakshatra_ta'];
const PROFILE_AYANAMSAS = ['Lahiri', 'Raman', 'Krishnamurti', 'Fagan-Bradley'];
const PROFILE_DASA_YEARS = ['julian', 'sidereal', 'savana'];

function profileBackup(profiles, now = new Date()) {
  return { app: 'JoRoScope', version: PROFILE_BACKUP_VERSION, exported_at: now.toISOString(), count: profiles.length, profiles };
}

// A clean copy of one imported profile, or null with the reason it was rejected
function cleanProfile(raw) {
  if (!raw || typeof raw !== 'object' || Array.isArray(raw)) return [null, 'not a profile'];
  const text = (v, max = 120) => (typeof v === 'string' ? v.trim().slice(0, max) : '');
  const name = text(raw.name);
  if (!name) return [null, 'no name'];
  const date = text(raw.date, 10);
  const [y, m, d] = date.split('-').map(Number);
  const day = new Date(Date.UTC(y, m - 1, d));
  if (!/^\d{4}-\d{2}-\d{2}$/.test(date) || day.getUTCMonth() !== m - 1 || day.getUTCDate() !== d || y < 1 || y > 3000) {
    return [null, `${name}: invalid date`];
  }
  const timeMatch = text(raw.time, 8).match(/^([01]\d|2[0-3]):([0-5]\d)(?::([0-5]\d))?$/);
  if (!timeMatch) return [null, `${name}: invalid time`];
  const lat = Number(raw.latitude);
  const lon = Number(raw.longitude);
  if (!Number.isFinite(lat) || Math.abs(lat) > 90 || !Number.isFinite(lon) || Math.abs(lon) > 180) {
    return [null, `${name}: invalid latitude or longitude`];
  }
  const out = {};
  PROFILE_TEXT_FIELDS.forEach(key => { out[key] = text(raw[key]); });
  const index = (v, n) => (Number.isInteger(v) && v >= 0 && v < n ? v : undefined);
  const iso = v => (typeof v === 'string' && !Number.isNaN(Date.parse(v)) ? new Date(v).toISOString() : undefined);
  Object.assign(out, {
    id: text(raw.id, 64).replace(/[^\w-]/g, '') || undefined,
    name,
    date,
    time: `${timeMatch[1]}:${timeMatch[2]}:${timeMatch[3] || '00'}`,
    latitude: lat,
    longitude: lon,
    timezone: out.timezone || 'Asia/Kolkata',
    ayanamsa: PROFILE_AYANAMSAS.includes(raw.ayanamsa) ? raw.ayanamsa : 'Lahiri',
    fold: raw.fold === '0' || raw.fold === '1' ? raw.fold : '',
    dasa_year: PROFILE_DASA_YEARS.includes(raw.dasa_year) ? raw.dasa_year : 'julian',
    nakshatra_idx: index(raw.nakshatra_idx, 27),
    sign_idx: index(raw.sign_idx, 12),
    pada: Number.isInteger(raw.pada) && raw.pada >= 1 && raw.pada <= 4 ? raw.pada : undefined,
    created_at: iso(raw.created_at),
    updated_at: iso(raw.updated_at)
  });
  return [out, null];
}

const sameBirth = (a, b) => a.name.toLowerCase() === b.name.toLowerCase() && a.date === b.date && a.time === b.time;

// Merge a parsed backup into the saved list: new people are added, a profile with the same id
// (or the same name, date and time) is replaced when the imported copy is newer
function mergeProfileBackup(data, existing, makeId = () => `p-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`) {
  const incoming = Array.isArray(data) ? data : (data && Array.isArray(data.profiles) ? data.profiles : null);
  if (!incoming) throw new Error('This file is not a JoRoScope profile backup.');
  if (data && !Array.isArray(data) && data.app && data.app !== 'JoRoScope') throw new Error('This backup is from another application.');
  const merged = [...existing];
  const result = { merged, added: 0, updated: 0, unchanged: 0, rejected: [] };
  incoming.forEach(raw => {
    const [p, reason] = cleanProfile(raw);
    if (!p) {
      result.rejected.push(reason);
      return;
    }
    const at = merged.findIndex(ep => (p.id && ep.id === p.id) || (ep.name && sameBirth(ep, p)));
    if (at < 0) {
      if (merged.length >= PROFILE_LIMIT) {
        result.rejected.push(`${p.name}: the vault is full`);
        return;
      }
      merged.unshift({ ...p, id: p.id || makeId(), created_at: p.created_at || new Date().toISOString() });
      result.added++;
    } else if ((Date.parse(p.updated_at || p.created_at || 0) || 0) > (Date.parse(merged[at].updated_at || merged[at].created_at || 0) || 0)) {
      merged[at] = { ...merged[at], ...p, id: merged[at].id };
      result.updated++;
    } else {
      result.unchanged++;
    }
  });
  return result;
}

if (typeof module !== 'undefined') module.exports = { profileBackup, cleanProfile, mergeProfileBackup, PROFILE_LIMIT };
