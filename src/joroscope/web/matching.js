/**
 * JoRoScope: Horoscope matching: Porutham, Ashta Koota, Dosha Samyam and Dasa Sandhi.
 * A classic script sharing the page's global scope with app.js; see index.html for the order.
 */

// Horoscope Matching Tool
function populateMatchDropdowns() {
  const gStar = $('#match-girl-star');
  const bStar = $('#match-boy-star');
  const gSign = $('#match-girl-sign');
  const bSign = $('#match-boy-sign');

  if (gStar && !gStar.options.length) {
    STARS_EN.forEach((s, i) => {
      gStar.add(new Option('', i));
      bStar.add(new Option('', i));
    });
    SIGNS_EN.forEach((s, i) => {
      gSign.add(new Option('', i));
      bSign.add(new Option('', i));
    });
  }
  [gStar, bStar].forEach(sel => [...(sel?.options || [])].forEach((o, i) => {
    o.textContent = txt(`${i + 1}. ${STARS_EN[i]} (${STARS_TA[i]})`, `${i + 1}. ${STARS_TA[i]} (${STARS_EN[i]})`);
  }));
  [gSign, bSign].forEach(sel => [...(sel?.options || [])].forEach((o, i) => {
    o.textContent = txt(`${SIGNS_EN[i]} (${SIGNS_TA[i]})`, `${SIGNS_TA[i]} (${SIGNS_EN[i]})`);
  }));

  // Populate profiles
  const profiles = getSavedProfiles();
  const gProf = $('#match-girl-profile');
  const bProf = $('#match-boy-profile');
  const isTa = currentLang === 'ta';

  if (gProf && bProf) {
    const defaultText = isTa ? '-- நபர் அல்லது கைமுறை தேர்வு --' : '-- Choose Profile or Manual --';
    gProf.innerHTML = `<option value="">${defaultText}</option>`;
    bProf.innerHTML = `<option value="">${defaultText}</option>`;

    profiles.forEach((p, idx) => {
      const starText = isTa ? (p.nakshatra_ta || p.nakshatra || '') : (p.nakshatra || '');
      const signText = isTa ? (p.moon_sign_ta || p.moon_sign || '') : (p.moon_sign || '');
      const astroLabel = starText && signText ? ` (${starText} · ${signText})` : (starText ? ` (${starText})` : '');
      const optText = `${p.name}${astroLabel}`;

      gProf.add(new Option(optText, idx));
      bProf.add(new Option(optText, idx));
    });

    gProf.onchange = () => {
      if (gProf.value === '') return;
      const p = profiles[gProf.value];
      if (p && p.nakshatra_idx !== undefined && p.sign_idx !== undefined) {
        gStar.value = p.nakshatra_idx;
        gSign.value = p.sign_idx;
      }
    };
    bProf.onchange = () => {
      if (bProf.value === '') return;
      const p = profiles[bProf.value];
      if (p && p.nakshatra_idx !== undefined && p.sign_idx !== undefined) {
        bStar.value = p.nakshatra_idx;
        bSign.value = p.sign_idx;
      }
    };
  }
}

// Full birth details let the server compare Chevvai Dosham and Papa Samyam;
// fall back to star and sign when no profile is chosen or the selects were changed by hand.
function matchCandidate(side) {
  const star = parseInt($(`#match-${side}-star`).value, 10);
  const sign = parseInt($(`#match-${side}-sign`).value, 10);
  const profIdx = $(`#match-${side}-profile`).value;
  const prof = profIdx === '' ? null : getSavedProfiles()[profIdx];
  if (prof && prof.date && prof.time && prof.nakshatra_idx === star && prof.sign_idx === sign) {
    const { name, date, time, timezone, latitude, longitude, ayanamsa, fold, city } = prof;
    return { name, date, time, timezone, latitude, longitude, ayanamsa, fold, city };
  }
  return { nakshatra_index: star, sign_index: sign };
}

async function runHoroscopeMatch() {
  const payload = {
    girl: matchCandidate('girl'),
    boy: matchCandidate('boy')
  };

  try {
    const resp = await fetch('/api/match', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const match = await resp.json();
    if (!resp.ok) throw new Error(match.error);
    lastMatch = match;
    syncProfilesFromMatch(match);
    renderMatchResult(match);
    notify(txt('Horoscope compatibility calculated', 'திருமணப் பொருத்தம் கணிக்கப்பட்டது'));
  } catch (err) {
    notify(`${txt('Matching error', 'பொருத்தப் பிழை')}: ${errorText(err.message)}`);
  }
}

// A full-chart match computes each partner's true star and sign; store them on the
// matching saved profile and selects so older or hand-entered values are corrected.
function syncProfilesFromMatch(match) {
  const list = getSavedProfiles();
  let changed = false;
  [['bride', 'girl'], ['groom', 'boy']].forEach(([side, prefix]) => {
    const info = match[side];
    if (!info?.name) return;
    const prof = list.find(p => p.name.toLowerCase() === info.name.toLowerCase());
    if (prof && (prof.nakshatra_idx !== info.nakshatra_index || prof.sign_idx !== info.sign_index || prof.pada !== info.pada)) {
      Object.assign(prof, {
        nakshatra: info.nakshatra, nakshatra_ta: info.nakshatra_ta, nakshatra_idx: info.nakshatra_index,
        moon_sign: info.sign, moon_sign_ta: info.sign_ta, sign_idx: info.sign_index, pada: info.pada,
        lagna: info.lagna, lagna_ta: info.lagna_ta
      });
      changed = true;
    }
    $(`#match-${prefix}-star`).value = info.nakshatra_index;
    $(`#match-${prefix}-sign`).value = info.sign_index;
  });
  if (!changed) return;
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(list));
  } catch (e) {}
  const [gSel, bSel] = [$('#match-girl-profile').value, $('#match-boy-profile').value];
  populateMatchDropdowns();
  $('#match-girl-profile').value = gSel;
  $('#match-boy-profile').value = bSel;
  renderProfilesList();
}

const GUNA_LABELS = [
  ['varna', 1, 'Varna (Work & Spiritual Nature)', 'வர்ணம் (தொழில் & ஆன்மீக இயல்பு)'],
  ['vashya', 2, 'Vashya (Mutual Magnetism)', 'வசியம் (பரஸ்பர ஈர்ப்பு)'],
  ['tara', 3, 'Tara (Health & Longevity)', 'தாரை (ஆரோக்கியம் & ஆயுள்)'],
  ['yoni', 4, 'Yoni (Physical Harmony)', 'யோனி (உடல் ஒற்றுமை)'],
  ['graha_maitri', 5, 'Graha Maitri (Mental Friendship)', 'கிரக மைத்ரி (மன நட்பு)'],
  ['gana', 6, 'Gana (Temperament Alignment)', 'கணம் (குண ஒற்றுமை)'],
  ['bhakoot', 7, 'Bhakoot (Family Fortune)', 'பகூட் (குடும்ப அதிர்ஷ்டம்)'],
  ['nadi', 8, 'Nadi (Genetic / Health Affinity)', 'நாடி (மரபு & ஆரோக்கிய ஒற்றுமை)']
];

function renderMatchResult(match) {
  const g = match.guna_milan;
  $('#match-results-container').hidden = false;
  $('#match-score-num').textContent = g.total_score;
  $('#match-verdict-title').textContent = txt(match.verdict, match.verdict_ta);
  const notes = (match.verdict_notes || []).map(n => txt(n.en, n.ta)).join('; ');
  $('#match-verdict-desc').textContent = txt(
    `${match.passed_count} of 10 Poruthams passed. Guna score: ${g.total_score} of 36.`,
    `10-ல் ${match.passed_count} பொருத்தங்கள் உள்ளன. குண மதிப்பெண்: 36-ல் ${g.total_score}.`) +
    (notes ? txt(` Verdict lowered: ${notes}.`, ` முடிவு குறைக்கப்பட்டது: ${notes}.`) : '');

  const rajjuBadge = $('#match-rajju-badge');
  rajjuBadge.textContent = match.rajju_agreement
    ? txt('Rajju Match: Harmonious (Passed)', 'ரஜ்ஜு பொருத்தம் உண்டு')
    : txt('Rajju Dosha: Inauspicious (Same Rajju)', 'ரஜ்ஜு தோஷம்: ஒரே ரஜ்ஜு');
  rajjuBadge.className = `badge ${match.rajju_agreement ? 'status-pill success' : 'status-pill danger'}`;
  $('#match-porutham-count').textContent = txt(`${match.passed_count} of 10 Passed`, `10-ல் ${match.passed_count} பொருத்தம்`);

  // 10 Poruthams table: the other language's name sits underneath
  const tbody = $('#poruthams-tbody');
  tbody.replaceChildren();
  match.poruthams.forEach(p => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><strong>${txt(p.name, p.tamil)}</strong> <small style="display:block;color:var(--gold-dim)">${txt(p.tamil, p.name)}</small></td>
      <td>${esc(txt(p.description, p.description_ta))}</td>
      <td><span class="status-pill ${p.passed ? 'success' : 'danger'}">${p.passed ? txt('Passed ✔', 'உண்டு ✔') : txt('Not Matched ✖', 'இல்லை ✖')}</span></td>
      <td>${p.points} / ${p.max_points}</td>
    `;
    tbody.append(tr);
  });

  // 8 Gunas Grid
  const gunasGrid = $('#gunas-grid');
  gunasGrid.replaceChildren();
  GUNA_LABELS.forEach(([key, max, en, ta]) => {
    const card = document.createElement('div');
    card.className = 'guna-card';
    card.innerHTML = `
      <small style="font-size:10px;color:var(--text-muted)">${txt(en, ta)}</small>
      <div style="font-size:18px;font-weight:700;color:var(--gold);margin:4px 0">${g[key]} / ${max}</div>
    `;
    gunasGrid.append(card);
  });
  renderDoshaSamyam(match);
}

// Dasa Sandhi: both Maha Dasas changing within about six months of each other
function dasaSandhiRows(sandhi) {
  if (!sandhi) return [];
  const label = txt('Dasa Sandhi', 'தசா சந்தி');
  if (!sandhi.present) {
    return [[label, '—', '—', `<span class="status-pill success">${txt(`None in the next ${sandhi.horizon_years} years ✔`, `அடுத்த ${sandhi.horizon_years} ஆண்டுகளில் இல்லை ✔`)}</span>`]];
  }
  return sandhi.conflicts.map(c => [
    label,
    `${grahaName(c.bride_from)} → ${grahaName(c.bride_to)}<br><small>${localDate(c.bride_date)}</small>`,
    `${grahaName(c.groom_from)} → ${grahaName(c.groom_to)}<br><small>${localDate(c.groom_date)}</small>`,
    `<span class="status-pill danger">${txt(`${c.gap_days} days apart ✖`, `${c.gap_days} நாள் இடைவெளி ✖`)}</span>`
  ]);
}

function renderDoshaSamyam(match) {
  const card = $('#dosha-samyam-card');
  const hint = $('#dosha-samyam-hint');
  const ds = match.dosha_samyam;
  const isTa = currentLang === 'ta';
  card.hidden = !ds;
  hint.hidden = !!ds;
  if (!ds) {
    hint.textContent = isTa
      ? 'செவ்வாய் தோஷ சாம்யம் மற்றும் பாப சாம்யம் ஒப்பிட, முழு பிறப்பு விவரங்களுடன் சேமிக்கப்பட்ட ஜாதகங்களைத் தேர்வு செய்யவும்.'
      : 'Choose saved profiles with full birth details to compare Chevvai Dosham and Papa Samyam as well.';
    return;
  }

  const chevvaiText = c => !c.present ? (isTa ? 'இல்லை' : 'None')
    : (c.cancelled ? (isTa ? 'நிவர்த்தி' : 'Cancelled') : (isTa ? `உள்ளது (${c.severity}/3)` : `Present (${c.severity}/3)`));
  const rkText = r => r.present ? (isTa ? 'உள்ளது' : 'Present') : (isTa ? 'இல்லை' : 'None');
  const papaText = pp => `${pp.total} (${pp.breakdown.map(b => b.points).join(' / ')})`;
  const pill = ok => `<span class="status-pill ${ok ? 'success' : 'danger'}">${ok ? (isTa ? 'சமம் ✔' : 'Balanced ✔') : (isTa ? 'சமமில்லை ✖' : 'Unbalanced ✖')}</span>`;
  const rkBalanced = ds.boy.rahu_ketu.present === ds.girl.rahu_ketu.present;

  $('#dosha-samyam-tbody').innerHTML = [
    [isTa ? 'செவ்வாய் தோஷம்' : 'Chevvai Dosham', chevvaiText(ds.girl.chevvai), chevvaiText(ds.boy.chevvai), pill(ds.chevvai_balanced)],
    [isTa ? 'ராகு-கேது தோஷம்' : 'Rahu-Ketu Dosham', rkText(ds.girl.rahu_ketu), rkText(ds.boy.rahu_ketu), pill(rkBalanced)],
    [isTa ? 'பாப புள்ளிகள் (ல / ச / சு)' : 'Papa Points (L / C / S)', papaText(ds.girl.papa), papaText(ds.boy.papa), pill(ds.papa_balanced)],
    ...dasaSandhiRows(ds.dasa_sandhi)
  ].map(([label, girl, boy, state]) => `<tr><td><strong>${label}</strong></td><td>${girl}</td><td>${boy}</td><td>${state}</td></tr>`).join('');

  const status = $('#dosha-samyam-status');
  status.className = `status-pill ${ds.balanced ? 'success' : 'danger'}`;
  status.textContent = ds.balanced ? (isTa ? 'தோஷ சாம்யம் உண்டு' : 'Doshas Balanced') : (isTa ? 'ஜோதிடரை அணுகவும்' : 'Needs Review');
  $('#dosha-samyam-summary').textContent = isTa
    ? 'செவ்வாய் தோஷம் இருவருக்கும் இருக்க வேண்டும் அல்லது இருவருக்கும் இல்லாமல் இருக்க வேண்டும்; பெண்ணின் பாப புள்ளிகள் ஆணின் புள்ளிகளை விட அதிகமாக இருக்கக் கூடாது.'
    : "Chevvai Dosham should be present in both charts or neither, and the bride's Papa points should not exceed the groom's.";
}
