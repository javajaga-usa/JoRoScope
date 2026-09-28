/**
 * JoRoScope: The saved profiles vault: the quick loader, saving, the profile cards, and backup export
 * and import (the checks live in profiles.js).
 * A classic script sharing the page's global scope with app.js; see index.html for the order.
 */

// Saved Profiles Vault & Multi-Person Management
function getSavedProfiles() {
  try {
    let p = JSON.parse(localStorage.getItem(STORAGE_KEY));
    if (!p || !Array.isArray(p) || p.length === 0) {
      // Check for legacy migration
      const legacy = JSON.parse(localStorage.getItem(LEGACY_STORAGE_KEY) || 'null');
      if (Array.isArray(legacy) && legacy.length) {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(legacy));
        return legacy;
      }
      // Seed default profiles for immediate out-of-the-box multi-person testing
      localStorage.setItem(STORAGE_KEY, JSON.stringify(DEFAULT_SEED_PROFILES));
      return [...DEFAULT_SEED_PROFILES];
    }
    return p;
  } catch (e) {
    console.warn('LocalStorage access issue:', e);
    return [...DEFAULT_SEED_PROFILES];
  }
}

function populateQuickProfileDropdown(selectedId = null) {
  const select = $('#quick-profile-select');
  if (!select) return;
  const profiles = getSavedProfiles();
  const isTa = currentLang === 'ta';

  select.innerHTML = `<option value="">👤 ${isTa ? '-- நபரைத் தேர்வு செய்க --' : '-- Quick Load Person --'}</option>`;

  profiles.forEach(p => {
    const opt = document.createElement('option');
    opt.value = p.id || p.name;
    const starStr = isTa ? (p.nakshatra_ta || p.nakshatra || '') : (p.nakshatra || '');
    const astroStr = starStr ? ` — ${starStr}` : (p.city ? ` (${p.city})` : '');
    opt.textContent = `${p.name}${astroStr}`;
    select.appendChild(opt);
  });

  if (selectedId) {
    select.value = selectedId;
  }
}

function handleQuickProfileChange(e) {
  const val = e.target.value;
  if (!val) return;
  const profiles = getSavedProfiles();
  const profile = profiles.find(p => (p.id === val || p.name === val));
  if (profile) {
    loadProfileIntoForm(profile);
  }
}

function loadProfileIntoForm(p) {
  if (!p) return;
  const form = $('#birth-form');
  if (!form) return;

  if (form.elements['name']) form.elements['name'].value = p.name || '';
  if (form.elements['date']) form.elements['date'].value = p.date || '';
  if (form.elements['time']) form.elements['time'].value = p.time || '';
  if (form.elements['city']) form.elements['city'].value = p.city || '';
  if (form.elements['latitude']) form.elements['latitude'].value = p.latitude ?? '';
  if (form.elements['longitude']) form.elements['longitude'].value = p.longitude ?? '';
  if (form.elements['timezone']) form.elements['timezone'].value = p.timezone || 'Asia/Kolkata';
  if (form.elements['ayanamsa']) form.elements['ayanamsa'].value = p.ayanamsa || 'Lahiri';
  if (form.elements['fold']) form.elements['fold'].value = p.fold ?? '';
  if (form.elements['dasa_year']) form.elements['dasa_year'].value = p.dasa_year || 'julian';

  const qSelect = $('#quick-profile-select');
  if (qSelect) qSelect.value = p.id || p.name;

  // Auto-submit to compute chart immediately
  form.requestSubmit();
  notify(currentLang === 'ta' ? `${p.name} ஜாதகம் கணிக்கப்படுகிறது...` : `Loaded chart for ${p.name}`);
}

function saveCurrentProfile() {
  const form = $('#birth-form');
  if (!form) return;

  const nameInput = form.elements['name'];
  const name = (nameInput ? nameInput.value : '').trim();
  if (!name) {
    notify(currentLang === 'ta' ? 'தயவுசெய்து பெயரை உள்ளிடவும்' : 'Please enter a name first.');
    if (nameInput) nameInput.focus();
    return;
  }

  const date = form.elements['date']?.value || '';
  const time = form.elements['time']?.value || '';
  const city = form.elements['city']?.value || '';
  const lat = parseFloat(form.elements['latitude']?.value || '0');
  const lon = parseFloat(form.elements['longitude']?.value || '0');
  const timezone = form.elements['timezone']?.value || 'Asia/Kolkata';
  const ayanamsa = form.elements['ayanamsa']?.value || 'Lahiri';
  const fold = form.elements['fold']?.value || '';
  const dasa_year = form.elements['dasa_year']?.value || 'julian';

  const list = getSavedProfiles();
  const existingIndex = list.findIndex(p => p.name.toLowerCase() === name.toLowerCase());

  let nakshatra = '';
  let nakshatra_ta = '';
  let nakshatra_idx = undefined;
  let moon_sign = '';
  let moon_sign_ta = '';
  let sign_idx = undefined;
  let lagna = '';
  let lagna_ta = '';
  let pada = undefined;

  if (currentChart && currentChart.planets && currentChart.profile && currentChart.profile.name === name) {
    const pMoon = currentChart.planets.Moon;
    const pAsc = currentChart.planets.Ascendant;
    if (pMoon) {
      nakshatra = pMoon.nakshatra || '';
      nakshatra_idx = STARS_EN.indexOf(pMoon.nakshatra);
      if (nakshatra_idx >= 0) nakshatra_ta = STARS_TA[nakshatra_idx];
      moon_sign = pMoon.sign || '';
      sign_idx = pMoon.sign_index;
      if (sign_idx !== undefined && sign_idx >= 0) moon_sign_ta = SIGNS_TA[sign_idx];
      pada = pMoon.pada;
    }
    if (pAsc) {
      lagna = pAsc.sign || '';
      if (pAsc.sign_index !== undefined && pAsc.sign_index >= 0) lagna_ta = SIGNS_TA[pAsc.sign_index];
    }
  }

  const profileId = existingIndex >= 0 ? (list[existingIndex].id || crypto.randomUUID()) : crypto.randomUUID();

  const item = {
    id: profileId,
    name,
    date,
    time,
    city,
    latitude: lat,
    longitude: lon,
    timezone,
    ayanamsa,
    fold,
    dasa_year,
    lagna: lagna || (existingIndex >= 0 ? list[existingIndex].lagna : ''),
    lagna_ta: lagna_ta || (existingIndex >= 0 ? list[existingIndex].lagna_ta : ''),
    moon_sign: moon_sign || (existingIndex >= 0 ? list[existingIndex].moon_sign : ''),
    moon_sign_ta: moon_sign_ta || (existingIndex >= 0 ? list[existingIndex].moon_sign_ta : ''),
    nakshatra: nakshatra || (existingIndex >= 0 ? list[existingIndex].nakshatra : ''),
    nakshatra_ta: nakshatra_ta || (existingIndex >= 0 ? list[existingIndex].nakshatra_ta : ''),
    nakshatra_idx: nakshatra_idx !== undefined ? nakshatra_idx : (existingIndex >= 0 ? list[existingIndex].nakshatra_idx : undefined),
    sign_idx: sign_idx !== undefined ? sign_idx : (existingIndex >= 0 ? list[existingIndex].sign_idx : undefined),
    pada: pada !== undefined ? pada : (existingIndex >= 0 ? list[existingIndex].pada : undefined),
    created_at: existingIndex >= 0 ? (list[existingIndex].created_at || new Date().toISOString()) : new Date().toISOString(),
    updated_at: new Date().toISOString()
  };

  if (existingIndex >= 0) {
    list[existingIndex] = item;
  } else {
    list.unshift(item);
  }

  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(list));
    populateQuickProfileDropdown(item.id);
    renderProfilesList();
    populateMatchDropdowns();
    const msg = currentLang === 'ta'
      ? `'${item.name}' ஜாதகம் வெற்றிகரமாக சேமிக்கப்பட்டது!`
      : `Profile '${item.name}' saved successfully!`;
    notify(msg);
  } catch (err) {
    console.error(err);
    notify(txt('Storage error: please export profiles backup.', 'சேமிப்புப் பிழை: ஜாதகங்களை பேக்கப் எடுக்கவும்.'));
  }
}

function syncCalculatedProfileWithStorage(chartResult) {
  if (!chartResult || !chartResult.profile || !chartResult.planets) return;
  const name = (chartResult.profile.name || '').trim();
  if (!name) return;

  const list = getSavedProfiles();
  const idx = list.findIndex(p => p.name.toLowerCase() === name.toLowerCase());
  if (idx < 0) return;

  const pMoon = chartResult.planets.Moon;
  const pAsc = chartResult.planets.Ascendant;

  if (pMoon) {
    list[idx].nakshatra = pMoon.nakshatra || '';
    const starIdx = STARS_EN.indexOf(pMoon.nakshatra);
    list[idx].nakshatra_idx = starIdx >= 0 ? starIdx : undefined;
    if (starIdx >= 0) list[idx].nakshatra_ta = STARS_TA[starIdx];
    list[idx].moon_sign = pMoon.sign || '';
    list[idx].sign_idx = pMoon.sign_index;
    if (pMoon.sign_index !== undefined && pMoon.sign_index >= 0) list[idx].moon_sign_ta = SIGNS_TA[pMoon.sign_index];
    list[idx].pada = pMoon.pada;
  }

  if (pAsc) {
    list[idx].lagna = pAsc.sign || '';
    if (pAsc.sign_index !== undefined && pAsc.sign_index >= 0) list[idx].lagna_ta = SIGNS_TA[pAsc.sign_index];
  }

  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(list));
    populateQuickProfileDropdown(list[idx].id);
    renderProfilesList();
    populateMatchDropdowns();
  } catch (e) {
    console.warn('Auto-sync profile storage failed:', e);
  }
}

function clearFormForNewPerson() {
  const form = $('#birth-form');
  if (!form) return;

  const nameInput = form.elements['name'];
  if (nameInput) {
    nameInput.value = '';
    nameInput.focus();
  }

  // Set default date to today
  const today = new Date().toISOString().slice(0, 10);
  if (form.elements['date']) form.elements['date'].value = today;
  if (form.elements['time']) form.elements['time'].value = '12:00:00';

  const qSelect = $('#quick-profile-select');
  if (qSelect) qSelect.value = '';

  const msg = currentLang === 'ta'
    ? 'புதிய நபரின் விவரங்களை உள்ளிட தயார்.'
    : 'Form ready for new person details.';
  notify(msg);
}

function clearAllProfiles() {
  const isTa = currentLang === 'ta';
  const confirmMsg = isTa
    ? 'அனைத்து சேமிக்கப்பட்ட ஜாதகங்களையும் நீக்க விரும்புகிறீர்களா? இதை மீண்டும் பெற இயலாது.'
    : 'Are you sure you want to delete all saved profiles? This cannot be undone.';
  if (!window.confirm(confirmMsg)) return;

  localStorage.setItem(STORAGE_KEY, JSON.stringify([]));
  populateQuickProfileDropdown();
  renderProfilesList();
  populateMatchDropdowns();
  notify(isTa ? 'அனைத்து ஜாதகங்களும் நீக்கப்பட்டன.' : 'All profiles cleared.');
}

function deleteProfile(idx) {
  const list = getSavedProfiles();
  if (idx < 0 || idx >= list.length) return;
  const p = list[idx];
  const isTa = currentLang === 'ta';
  if (!window.confirm(`${isTa ? 'இந்த ஜாதகத்தை நீக்க வேண்டுமா:' : 'Delete profile for'} ${p.name}?`)) return;

  list.splice(idx, 1);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(list));
  populateQuickProfileDropdown();
  renderProfilesList();
  populateMatchDropdowns();
  notify(isTa ? `'${p.name}' நீக்கப்பட்டது` : `Deleted '${p.name}'`);
}

function renderProfilesList() {
  const list = getSavedProfiles();
  const q = ($('#profile-search')?.value || '').toLowerCase().trim();
  const grid = $('#profiles-grid');
  const countBadge = $('#profiles-count-badge');
  const isTa = currentLang === 'ta';

  if (countBadge) {
    countBadge.textContent = isTa ? `${list.length} சேமிக்கப்பட்டது` : `${list.length} saved`;
  }

  if (!grid) return;
  grid.replaceChildren();

  const filtered = list.filter(p => {
    if (!q) return true;
    const nameMatch = (p.name || '').toLowerCase().includes(q);
    const cityMatch = (p.city || '').toLowerCase().includes(q);
    const starMatch = (p.nakshatra || '').toLowerCase().includes(q) || (p.nakshatra_ta || '').toLowerCase().includes(q);
    const signMatch = (p.moon_sign || '').toLowerCase().includes(q) || (p.moon_sign_ta || '').toLowerCase().includes(q);
    return nameMatch || cityMatch || starMatch || signMatch;
  });

  if (!filtered.length) {
    grid.innerHTML = `
      <div class="empty-state" style="grid-column:1/-1;min-height:220px;padding:30px;">
        <span style="font-size:36px;margin-bottom:12px;">📁</span>
        <h3 style="margin-bottom:6px;color:var(--text-primary);">${isTa ? 'ஜாதகங்கள் எதுவும் இல்லை' : 'No Profiles Found'}</h3>
        <p class="muted">${isTa ? 'புதிய நபரை சேர்க்க "புதிய நபர்" பொத்தானை அழுத்தவும்.' : 'Click "New Person" to enter birth details and save a chart.'}</p>
      </div>
    `;
    return;
  }

  filtered.forEach(p => {
    const originalIdx = list.indexOf(p);
    const card = document.createElement('div');
    card.className = 'profile-card';

    const initial = (p.name || 'J').charAt(0).toUpperCase();
    const lagnaStr = isTa ? (p.lagna_ta || p.lagna || '—') : (p.lagna || '—');
    const moonStr = isTa ? (p.moon_sign_ta || p.moon_sign || '—') : (p.moon_sign || '—');
    const starStr = isTa ? (p.nakshatra_ta || p.nakshatra || '—') : (p.nakshatra || '—');
    const padaStr = p.pada ? (isTa ? `பாதம் ${p.pada}` : `P${p.pada}`) : '';

    card.innerHTML = `
      <div class="profile-card-header">
        <div class="profile-avatar-initial">${initial}</div>
        <div class="profile-header-meta">
          <h3>${esc(p.name)}</h3>
          <span class="pill-badge" style="font-size:10px;padding:2px 8px;">${esc(p.city || txt('Custom Location', 'தனிப்பயன் இருப்பிடம்'))}</span>
        </div>
      </div>

      <p class="muted" style="font-size:11.5px;margin:6px 0 8px;line-height:1.5;">
        📅 ${esc(p.date)} · ⏰ ${esc(p.time)}<br>
        🌐 ${esc(p.timezone || 'Asia/Kolkata')} · ${esc(ayanamsaLabel(p.ayanamsa || 'Lahiri'))}
      </p>

      <div class="profile-astro-badges">
        <span class="mini-astro-tag lagna-tag" title="${txt('Ascendant', 'லக்னம்')}">
          <span>🌌</span> <strong>${isTa ? 'லக்னம்' : 'Asc'}:</strong> ${esc(lagnaStr)}
        </span>
        <span class="mini-astro-tag moon-tag" title="${txt('Moon Sign / Rasi', 'சந்திர ராசி')}">
          <span>🌙</span> <strong>${isTa ? 'ராசி' : 'Rasi'}:</strong> ${esc(moonStr)}
        </span>
        <span class="mini-astro-tag star-tag" title="${txt('Birth Star / Nakshatra', 'ஜென்ம நட்சத்திரம்')}">
          <span>⭐</span> <strong>${isTa ? 'நட்சத்திரம்' : 'Star'}:</strong> ${esc(starStr)} ${padaStr}
        </span>
      </div>

      <div class="profile-card-actions">
        <button class="action-btn btn-full" data-load="${originalIdx}">
          <span>🪐</span> <span>${isTa ? 'ஜாதகம் திறக்க ↗' : 'Open Chart ↗'}</span>
        </button>
        <button class="action-btn" data-match-boy="${originalIdx}" title="${txt('Use as Boy in Horoscope Compatibility', 'திருமணப் பொருத்தத்தில் மணமகனாகப் பயன்படுத்து')}">
          <span>👦</span> <span>${isTa ? 'மணமகன்' : 'Boy'}</span>
        </button>
        <button class="action-btn" data-match-girl="${originalIdx}" title="${txt('Use as Girl in Horoscope Compatibility', 'திருமணப் பொருத்தத்தில் மணமகளாகப் பயன்படுத்து')}">
          <span>👧</span> <span>${isTa ? 'மணமகள்' : 'Girl'}</span>
        </button>
        <button class="action-btn" data-delete="${originalIdx}" style="color:var(--ruby);grid-column:1/-1;" title="${txt("Delete this person's record", 'இந்த நபரின் ஜாதகத்தை நீக்கு')}">
          <span>🗑️</span> <span>${isTa ? 'நீக்கு' : 'Delete'}</span>
        </button>
      </div>
    `;

    // Open Chart
    card.querySelector('[data-load]').onclick = () => {
      loadProfileIntoForm(p);
      navigatePage('chart');
    };

    // Use as Boy in Matcher
    card.querySelector('[data-match-boy]').onclick = () => {
      navigatePage('matching');
      const bProf = $('#match-boy-profile');
      if (bProf) {
        bProf.value = originalIdx;
        bProf.dispatchEvent(new Event('change'));
      }
      notify(isTa ? `${p.name} மணமகனாக தேர்வு செய்யப்பட்டார்` : `Selected ${p.name} as Boy`);
    };

    // Use as Girl in Matcher
    card.querySelector('[data-match-girl]').onclick = () => {
      navigatePage('matching');
      const gProf = $('#match-girl-profile');
      if (gProf) {
        gProf.value = originalIdx;
        gProf.dispatchEvent(new Event('change'));
      }
      notify(isTa ? `${p.name} மணமகளாக தேர்வு செய்யப்பட்டார்` : `Selected ${p.name} as Girl`);
    };

    // Delete
    card.querySelector('[data-delete]').onclick = () => {
      deleteProfile(originalIdx);
    };

    grid.append(card);
  });
}

function exportProfilesJSON() {
  const profiles = getSavedProfiles();
  const blob = new Blob([JSON.stringify(profileBackup(profiles), null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `JoRoScope-Profiles-${new Date().toISOString().slice(0, 10)}.json`;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1500);
  notify(txt(`Exported ${profiles.length} profiles to a backup file`, `${profiles.length} ஜாதகங்கள் பேக்கப் கோப்பில் சேமிக்கப்பட்டன`));
}

async function importProfilesJSON(e) {
  try {
    const file = e.target.files[0];
    if (!file) return;
    if (file.size > 20 * 1024 * 1024) throw new Error(txt('The file is too large for a profile backup.', 'இந்தக் கோப்பு பேக்கப்பிற்கு மிகப் பெரியது.'));
    let data;
    try {
      data = JSON.parse(await file.text());
    } catch {
      throw new Error(txt('The file is not valid JSON.', 'கோப்பு சரியான JSON அல்ல.'));
    }
    const result = mergeProfileBackup(data, getSavedProfiles(), () => crypto.randomUUID());
    localStorage.setItem(STORAGE_KEY, JSON.stringify(result.merged));
    populateQuickProfileDropdown();
    renderProfilesList();
    populateMatchDropdowns();
    const skipped = result.rejected.length;
    notify(txt(
      `Imported: ${result.added} new, ${result.updated} updated, ${result.unchanged} already saved${skipped ? `, ${skipped} skipped (${result.rejected.slice(0, 3).join('; ')})` : ''}.`,
      `இறக்குமதி: ${result.added} புதியவை, ${result.updated} புதுப்பிக்கப்பட்டவை, ${result.unchanged} ஏற்கனவே உள்ளவை${skipped ? `, ${skipped} தவிர்க்கப்பட்டவை (${result.rejected.slice(0, 3).join('; ')})` : ''}.`));
  } catch (err) {
    notify(`${txt('Import error', 'இறக்குமதிப் பிழை')}: ${errorText(err.message)}`);
  } finally {
    e.target.value = '';
  }
}
