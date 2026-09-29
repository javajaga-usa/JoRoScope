/**
 * JoRoScope: The daily Panchangam, the monthly Tamil calendar, the Muhurtham finder, transits and
 * Saturn cycles, horas, Gowri Panchangam and the personal Tara and Chandra Balam.
 * A classic script sharing the page's global scope with app.js; see index.html for the order.
 */

// Daily Panchangam: fetch the Tamil panchangam for the birth form's location
async function loadDailyPanchangam() {
  const form = $('#birth-form');
  const errorEl = $('#panch-error');
  errorEl.hidden = true;
  const city = form.elements['city']?.value || '';
  const lat = form.elements['latitude']?.value;
  const lon = form.elements['longitude']?.value;
  const tz = form.elements['timezone']?.value || 'Asia/Kolkata';
  $('#panch-location').textContent = `${city || `${lat}, ${lon}`} · ${tz}`;

  const payload = { latitude: lat, longitude: lon, timezone: tz };
  const picked = $('#panch-date').value;
  if (picked) payload.date = picked;
  if (currentChart) {
    payload.natal_nakshatra_index = STARS_EN.indexOf(currentChart.planets.Moon.nakshatra);
    payload.natal_sign_index = currentChart.planets.Moon.sign_index;
  }

  try {
    const resp = await fetch('/api/panchangam', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const panch = await resp.json();
    if (!resp.ok) throw new Error(panch.error || 'Panchangam calculation failed.');
    lastDailyPanchangam = panch;
    learnMalayalam(panch);
    populatePanchangamView(panch);
  } catch (err) {
    errorEl.textContent = errorText(err.message);
    errorEl.hidden = false;
  }
}

// Monthly Tamil calendar for the birth form's location
function shiftCalendarMonth(step) {
  const m = calendarMonth.month - 1 + step;
  calendarMonth = { year: calendarMonth.year + Math.floor(m / 12), month: ((m % 12) + 12) % 12 + 1 };
  loadMonthCalendar();
}

// Muhurtham finder: auspicious daytime windows for an undertaking over the coming days
let lastMuhurthams = null;
async function loadMuhurthams() {
  const form = $('#birth-form');
  const payload = {
    event: $('#muhurtham-event').value,
    days: Number($('#muhurtham-days').value),
    start_date: $('#panch-date').value || undefined,
    latitude: form.elements['latitude']?.value,
    longitude: form.elements['longitude']?.value,
    timezone: form.elements['timezone']?.value || 'Asia/Kolkata'
  };
  if (currentChart) {
    payload.natal_nakshatra_index = STARS_EN.indexOf(currentChart.planets.Moon.nakshatra);
    payload.natal_sign_index = currentChart.planets.Moon.sign_index;
  }
  const btn = $('#muhurtham-btn');
  btn.disabled = true;
  try {
    const resp = await fetch('/api/muhurtham', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await resp.json();
    if (!resp.ok) throw new Error(data.error || 'Muhurtham search failed.');
    lastMuhurthams = data;
    learnMalayalam(data);
    renderMuhurthams(data);
  } catch (err) {
    notify(errorText(err.message));
  } finally {
    btn.disabled = false;
  }
}

function renderMuhurthams(data) {
  if (!data) return;
  const personal = data.personal ? txt(' Checked against your birth star and Moon sign.', ' உங்கள் ஜன்ம நட்சத்திரம், ராசிக்கு ஏற்பச் சரிபார்க்கப்பட்டது.') : '';
  $('#muhurtham-summary').textContent = txt(
    `${data.days_found} suitable day${data.days_found === 1 ? '' : 's'} for ${data.event_en} in the ${data.days} days from ${data.start}.${personal}`,
    `${data.start} முதல் ${data.days} நாட்களில் ${data.event_ta} செய்ய ${data.days_found} உகந்த நாட்கள்.${personal}`);
  $('#muhurtham-ics-btn').hidden = !data.results.length;
  $('#muhurtham-list').innerHTML = data.results.map(d => `
    <div class="muhurtham-day">
      <h4>${d.date} · ${esc(txt(d.weekday, d.weekday_ta))} <small class="muted">(${esc(d.tamil_date)})</small></h4>
      <ul>${d.windows.map(w => `
        <li><strong>${clockTime(w.start_local)} – ${clockTime(w.end_local)}</strong> ·
          ${esc(txt(`${w.lagna} Lagna`, `${w.lagna_ta} லக்னம்`))} · ${esc(txt(w.tamil_yogam.en, w.tamil_yogam.ta))} ·
          ${esc(txt(w.nakshatra, w.nakshatra_ta))} ·
          ${esc(txt(`${w.tithi} (${w.paksha})`, `${w.tithi_ta} (${w.paksha === 'Shukla' ? 'வளர்பிறை' : 'தேய்பிறை'})`))}
          ${w.notes_en.length ? `<br><small class="muted">${esc(txt(w.notes_en.join(', '), w.notes_ta.join(', ')))}</small>` : ''}</li>`).join('')}
      </ul>
    </div>`).join('') || `<p class="muted">${txt('No suitable day in this period; try a longer range.', 'இந்தக் காலத்தில் உகந்த நாள் இல்லை; நீண்ட காலத்தைத் தேர்ந்தெடுக்கவும்.')}</p>`;
}

async function loadMonthCalendar() {
  const form = $('#birth-form');
  if (!calendarMonth) {
    const picked = $('#panch-date').value;
    const base = picked ? new Date(`${picked}T12:00:00`) : new Date();
    calendarMonth = { year: base.getFullYear(), month: base.getMonth() + 1 };
  }
  try {
    const resp = await fetch('/api/calendar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...calendarMonth,
        latitude: form.elements['latitude']?.value,
        longitude: form.elements['longitude']?.value,
        timezone: form.elements['timezone']?.value || 'Asia/Kolkata'
      })
    });
    const cal = await resp.json();
    if (!resp.ok) throw new Error(cal.error || 'Calendar calculation failed.');
    lastCalendar = cal;
    learnMalayalam(cal);
    renderMonthCalendar(cal);
  } catch (err) {
    notify(errorText(err.message));
  }
}

const OBSERVANCE_ICONS = {
  amavasai: '🌑', pournami: '🌕', ekadasi: '🙏', pradosham: '🔱', sashti: '🦚',
  sankatahara: '🐘', shivaratri: '🕉', karthigai: '🪔', month_start: '🗓'
};

function renderMonthCalendar(cal) {
  const isTa = currentLang === 'ta';
  const first = new Date(`${cal.days[0].date}T12:00:00`);
  $('#month-cal-label').textContent = first.toLocaleDateString(isTa ? 'ta-IN' : 'en-GB', { month: 'long', year: 'numeric' });
  const headers = VAARAM_SHORT.map(([en, ta]) => `<div class="month-head">${txt(en, ta)}</div>`).join('');
  const blanks = '<div class="month-cell empty"></div>'.repeat(first.getDay());
  const today = new Date().toLocaleDateString('en-CA');
  const cells = cal.days.map(d => `
    <div class="month-cell${d.date === today ? ' today' : ''}${d.observances.length ? ' has-obs' : ''}">
      <div class="month-cell-top">
        <strong>${Number(d.date.slice(8))}</strong>
        <small>${esc(txt(`${d.tamil_month.slice(0, 3)} ${d.tamil_day}`, `${d.tamil_month_ta} ${d.tamil_day}`))}</small>
      </div>
      <small class="month-cell-anga">${esc(txt(d.tithi_name, d.tithi_ta))} · ${esc(txt(d.nakshatra, d.nakshatra_ta))}</small>
      <div class="month-cell-obs">${d.observances.map(o => `<span title="${esc(txt(o.en, o.ta))}">${OBSERVANCE_ICONS[o.key]}</span>`).join('')}</div>
    </div>`).join('');
  $('#month-grid').innerHTML = headers + blanks + cells;

  const listed = cal.days.flatMap(d => d.observances.map(o => ({ d, o })));
  $('#month-observances').innerHTML = listed.map(({ d, o }) => `
    <div class="month-obs-row">
      <span>${OBSERVANCE_ICONS[o.key]} ${esc(txt(o.en, o.ta))}</span>
      <span>${new Date(`${d.date}T12:00:00`).toLocaleDateString(isTa ? 'ta-IN' : 'en-GB', { weekday: 'short', day: 'numeric', month: 'short' })}</span>
    </div>`).join('') || `<p class="muted">${txt('No observances this month.', 'இம்மாதம் விரத நாட்கள் இல்லை.')}</p>`;
}

// "until HH:MM", with the date when the anga runs past the panchangam's day
function untilLabel(endIso, dayIso) {
  if (!endIso) return '';
  const time = clockTime(endIso);
  const sameDay = endIso.slice(0, 10) === dayIso;
  const date = new Date(`${endIso.slice(0, 10)}T00:00:00`);
  const dayText = date.toLocaleDateString(currentLang === 'ta' ? 'ta-IN' : 'en-GB', { day: 'numeric', month: 'short' });
  if (currentLang === 'ta') return sameDay ? `${time} வரை` : `${dayText} ${time} வரை`;
  return sameDay ? `until ${time}` : `until ${time}, ${dayText}`;
}

function populatePanchangamView(panch) {
  if (!panch) return;
  const isTa = currentLang === 'ta';
  const ends = panch.ends_local || {};
  const day = panch.local_date;
  const tc = panch.tamil_calendar;

  const mc = panch.malayalam_calendar;
  if (mc && currentLang === 'ml') {
    // Kerala readers get the Malayalam (Kollavarsham) date in place of the Tamil one
    $('#panch-tamil-date').textContent = `${mc.month_ml} ${mc.day}, ${mlTerm(panch.vaaram.en)}`;
    $('#panch-tamil-year').textContent = `കൊല്ലവർഷം ${mc.year} · ${day}`;
  } else if (tc) {
    $('#panch-tamil-date').textContent = isTa
      ? `${tc.month_ta} ${tc.day}, ${panch.vaaram.ta}`
      : `${tc.month} ${tc.day} (${tc.month_ta} ${tc.day}), ${panch.vaaram.en}`;
    $('#panch-tamil-year').textContent = isTa
      ? `${tc.year_ta} வருடம் · ${day}`
      : `${tc.year} year (${tc.year_ta}), #${tc.year_number} of the 60-year cycle · ${day}`;
    if (mc) {
      $('#panch-tamil-year').textContent += isTa ? ` · கொல்லம் ஆண்டு ${mc.year}, ${mc.month_ta} ${mc.day}`
        : ` · Kollam era ${mc.year}, ${mc.month} ${mc.day}`;
    }
  }
  if (panch.tamil_yogam) {
    const ty = panch.tamil_yogam;
    const yogamEl = $('#panch-tamil-yogam');
    yogamEl.textContent = txt(ty.en, ty.ta);
    yogamEl.className = ty.good ? 'good-text' : 'bad-text';
    $('#panch-tamil-yogam-next').textContent = txt(`until ${clockTime(ty.until_local)}, then ${ty.next.en}`,
      `${clockTime(ty.until_local)} வரை, பின் ${ty.next.ta}`);
  }
  if (panch.soolam) {
    const sl = panch.soolam;
    $('#panch-soolam').textContent = isTa ? sl.direction_ta : sl.direction;
    $('#panch-parigaram').textContent = isTa ? `பரிகாரம்: ${sl.parigaram_ta}` : `Parigaram (remedy): ${sl.parigaram}`;
  }
  if (panch.chandrashtamam) {
    const ch = panch.chandrashtamam;
    $('#panch-chandrashtamam').textContent = isTa ? `${ch.sign_ta} ராசி` : `${ch.sign} (${ch.sign_ta}) Rasi`;
    $('#panch-chandrashtamam-stars').textContent = ch.stars.map(st => isTa ? st.ta : st.en).join(', ');
  }

  const when = panch.moment_local ? `${panch.moment_local.slice(0, 10)} ${clockTime(panch.moment_local)}` : day;
  $('#panch-moment').textContent = isTa
    ? `${when} நிலவரப்படி அங்கங்களும் அவை முடியும் நேரமும்`
    : `Angas prevailing at ${when}, with the local time each one ends`;

  if (panch.vaaram) {
    $('#panch-vaaram').textContent = isTa ? panch.vaaram.ta : panch.vaaram.en;
    $('#panch-vaaram-sub').textContent = isTa ? panch.vaaram.en : panch.vaaram.ta;
  }
  $('#panch-tithi').textContent = `${tithiLabel(panch.tithi_name)} (${panch.tithi})`;
  $('#panch-paksha').textContent = `${pakshaLabel(panch.paksha)} · ${untilLabel(ends.tithi, day)}`;

  $('#panch-nakshatra').textContent = isTa ? panch.tamil_nakshatra : `${panch.nakshatra} (${panch.tamil_nakshatra})`;
  $('#panch-pada').textContent = `${isTa ? 'பாதம்' : 'Pada'} ${panch.pada} · ${untilLabel(ends.nakshatra, day)}`;

  $('#panch-yoga').textContent = `${nityaYogaLabel(panch.yoga_name)} (${panch.yoga_number})`;
  $('#panch-yoga-nature').textContent = `${panch.yoga_auspiciousness === 'Auspicious' ? txt('Auspicious', 'சுபம்') : txt('Inauspicious', 'அசுபம்')} · ${untilLabel(ends.yoga, day)}`;

  $('#panch-karana').textContent = karanaLabel(panch.karana_name);
  $('#panch-karana-type').textContent = untilLabel(ends.karana, day);

  // Older payloads (a chart's birth panchanga) only carry UTC timings
  const local = key => panch[`${key}_local`] || `${panch[`${key}_utc`]} UTC`;
  $('#panch-abhijit').textContent = local('abhijit_muhurtham');
  $('#panch-rahu').textContent = local('rahu_kalam');
  $('#panch-yama').textContent = local('yamagandam');
  $('#panch-gulika').textContent = local('gulika_kalam');
  $('#panch-sun-times').textContent = `${local('sunrise')} – ${local('sunset')}`;
  $('#panch-tz').textContent = isTa
    ? `${panch.timezone} · பகல் ${panch.day_length_hours} மணி`
    : `${panch.timezone} · day length ${panch.day_length_hours} h`;

  renderHoraTable(panch.horas);
  renderGowriTable(panch.gowri);
  renderPersonalBalam(panch.personal);
}

// Date and clock time of an ISO timestamp in the chart location's timezone, e.g. "3 Jun 2027, 05:28"
function formatLocalDateTime(iso) {
  return new Date(iso).toLocaleString(currentLang === 'ta' ? 'ta-IN' : 'en-GB', {
    timeZone: currentChart?.profile?.timezone || undefined,
    day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit', hour12: false
  });
}

// Gochara (transits today) and upcoming Peyarchi, on the Predictions transit tab
function renderGochara() {
  const g = currentChart?.gochara;
  if (!g) return;
  const isTa = currentLang === 'ta';
  const houseLabel = h => isTa ? `${h}-ம் இடம்` : `House ${h}`;
  const planetLabel = n => isTa ? PLANET_NAMES[n].ta : PLANET_NAMES[n].en;

  $('#peyarchi-tbody').innerHTML = g.peyarchi.map(pe => `
    <tr>
      <td><strong>${planetLabel(pe.planet)}</strong></td>
      <td>${esc(formatLocalDateTime(pe.date))}</td>
      <td>${esc(isTa ? `${pe.from_tamil} → ${pe.to_tamil}` : `${pe.from_sign} → ${pe.to_sign}`)}</td>
      <td>${houseLabel(pe.house_from_moon)}</td>
    </tr>
  `).join('');

  renderSaturnCycles(g.saturn_cycles);
  $('#gochara-computed-at').textContent = isTa
    ? `${formatLocalDateTime(g.computed_at)} நிலவரப்படி · சந்திர ராசியிலிருந்து`
    : `As of ${formatLocalDateTime(g.computed_at)} · counted from the Moon sign`;
  $('#gochara-tbody').innerHTML = Object.entries(g.planets).map(([name, t]) => {
    const bindus = t.bindus === null ? '—'
      : `<span class="status-pill ${t.bindus >= 5 ? 'success' : (t.bindus >= 4 ? 'neutral' : 'danger')}">${t.bindus} / 8</span>`;
    const result = t.favourable ? (isTa ? 'சுபம்' : 'Favourable') : (isTa ? 'அசுபம்' : 'Unfavourable');
    const retro = t.retrograde ? (isTa ? ' (வ)' : ' ᴿ') : '';
    return `
      <tr>
        <td><strong>${planetLabel(name)}${retro}</strong></td>
        <td>${esc(isTa ? t.tamil : t.sign)}</td>
        <td>${formatDegrees(t.degree)}</td>
        <td>${houseLabel(t.house_from_moon)}</td>
        <td>${bindus}</td>
        <td><span class="status-pill ${t.favourable ? 'success' : 'neutral'}">${result}</span></td>
      </tr>`;
  }).join('');
}

const SATURN_CYCLE_LABELS = {
  sade_sati: ['Ezharai Sani (Sade Sati)', 'ஏழரைச் சனி'],
  ardhashtama: ['Ardhashtama Sani (4th)', 'அர்த்தாஷ்டமச் சனி (4-ம் இடம்)'],
  kandaka: ['Kandaka Sani (7th)', 'கண்டச் சனி (7-ம் இடம்)'],
  ashtama: ['Ashtama Sani (8th)', 'அஷ்டமச் சனி (8-ம் இடம்)']
};
const SADE_SATI_PHASES = {
  1: ['Rising (12th)', 'விரயச் சனி (12)'],
  2: ['Janma (1st)', 'ஜென்மச் சனி (1)'],
  3: ['Setting (2nd)', 'பாதச் சனி (2)']
};

function renderSaturnCycles(cycles) {
  const tbody = $('#saturn-cycles-tbody');
  if (!tbody || !cycles) return;
  tbody.innerHTML = cycles.map(c => {
    const [en, ta] = SATURN_CYCLE_LABELS[c.kind];
    const phases = c.phases.map(ph => {
      const [pen, pta] = SADE_SATI_PHASES[ph.phase];
      return `<div><small>${txt(pen, pta)}: ${localDate(ph.start)} → ${localDate(ph.end)}</small></div>`;
    }).join('') || '—';
    return `
      <tr class="${c.active ? 'active-period' : ''}">
        <td><strong>${txt(en, ta)}</strong>${c.active ? ` <span class="status-pill danger">${txt('Now', 'நடப்பில்')}</span>` : ''}</td>
        <td>${c.from_birth ? txt('from birth', 'பிறப்பு முதல்') : localDate(c.start)} → ${localDate(c.end)}</td>
        <td>${c.age_start < 0 ? 0 : c.age_start}</td>
        <td>${phases}</td>
      </tr>`;
  }).join('');
}

function renderHoraTable(horas) {
  const grid = $('#hora-grid');
  if (!grid || !horas) return;
  const isTa = currentLang === 'ta';
  grid.innerHTML = horas.map(h => `
    <div class="hora-item ${h.auspicious ? 'auspicious' : 'inauspicious'}${h.current ? ' current' : ''}">
      <span class="hora-time">${clockTime(h.start_local)}–${clockTime(h.end_local)}</span>
      <strong>${esc(isTa ? `${h.lord_ta} ஓரை` : `${h.lord} Hora`)}</strong>
      <small>${h.daytime ? (isTa ? 'பகல்' : 'Day') : (isTa ? 'இரவு' : 'Night')}${h.current ? (isTa ? ' · இப்போது' : ' · now') : ''}</small>
    </div>
  `).join('');
}

function renderGowriTable(gowri) {
  const grid = $('#gowri-grid');
  if (!grid || !gowri) return;
  grid.innerHTML = gowri.map(g => `
    <div class="hora-item ${g.good ? 'auspicious' : 'inauspicious'}${g.current ? ' current' : ''}">
      <span class="hora-time">${clockTime(g.start_local)}–${clockTime(g.end_local)}</span>
      <strong>${esc(txt(g.name, g.name_ta))}</strong>
      <small>${g.daytime ? txt('Day', 'பகல்') : txt('Night', 'இரவு')} · ${g.good ? txt('Nalla Neram', 'நல்ல நேரம்') : txt('Avoid', 'தவிர்க்கவும்')}${g.current ? txt(' · now', ' · இப்போது') : ''}</small>
    </div>
  `).join('');
}

// Upcoming Chandrashtamam periods and the Nakshatra birthday from the loaded chart
function renderUpcomingDates() {
  const up = currentChart?.south_indian?.upcoming;
  const isTa = currentLang === 'ta';
  if (!up) return;
  const ch = up.chandrashtamam;
  $('#panch-next-chandrashtamam').innerHTML = ch.periods.map(pr => `
    <div class="${pr.active ? 'upcoming-active' : ''}">${esc(formatLocalDateTime(pr.start_local))} → ${esc(formatLocalDateTime(pr.end_local))}</div>
  `).join('');

  const sb = up.star_birthday;
  if (sb) {
    $('#panch-star-birthday').textContent = sb.dates
      .map(d => new Date(`${d}T00:00:00`).toLocaleDateString(isTa ? 'ta-IN' : 'en-GB', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' }))
      .join(isTa ? ' மற்றும் ' : ' and ');
    $('#panch-star-birthday-sub').textContent = isTa
      ? `${sb.month_ta} மாதம், ${sb.star_ta} நட்சத்திரம் சூரிய உதயத்தில்`
      : `${sb.star} at sunrise in the Tamil month of ${sb.month}`;
  } else {
    $('#panch-star-birthday').textContent = '—';
    $('#panch-star-birthday-sub').textContent = '';
  }
}

function renderPersonalBalam(personal) {
  const card = $('#panch-personal-card');
  card.hidden = !(personal && currentChart);
  if (card.hidden) return;
  const isTa = currentLang === 'ta';
  const tara = personal.tara;
  const cb = personal.chandra_balam;
  const moon = currentChart.planets.Moon;
  $('#panch-personal-for').textContent = isTa
    ? `${currentChart.profile.name} · ${moon.tamil_nakshatra} · ${moon.tamil} ராசி`
    : `${currentChart.profile.name} · ${moon.nakshatra} · ${moon.sign} Rasi`;

  $('#panch-tara').textContent = isTa ? `${tara.name_ta} தாரை` : `${tara.name} Tara`;
  $('#panch-tara-sub').textContent = isTa
    ? `ஜன்ம நட்சத்திரத்திலிருந்து ${tara.count}-வது நட்சத்திரம்`
    : `Today's star is ${tara.count} from the birth star · ${tara.quality === 'good' ? 'favourable' : (tara.quality === 'bad' ? 'unfavourable' : 'mixed')}`;

  $('#panch-chandra').textContent = isTa ? `${cb.house}-ம் இடத்தில் சந்திரன்` : `Moon in house ${cb.house}`;
  $('#panch-chandra-sub').textContent = personal.chandrashtamam
    ? (isTa ? 'சந்திராஷ்டமம்: முக்கிய முடிவுகளைத் தவிர்க்கவும்' : 'Chandrashtamam: postpone important decisions')
    : (cb.favourable ? (isTa ? 'சந்திர பலம் உண்டு' : 'Favourable Chandra Balam') : (isTa ? 'சந்திர பலம் குறைவு' : 'Weak Chandra Balam'));

  const good = tara.quality === 'good' && cb.favourable;
  const bad = personal.chandrashtamam || (tara.quality === 'bad' && !cb.favourable);
  const status = $('#panch-personal-status');
  status.className = `status-pill ${good ? 'success' : (bad ? 'danger' : 'neutral')}`;
  status.textContent = good ? (isTa ? 'சாதகமான நாள்' : 'Favourable day')
    : (bad ? (isTa ? 'கவனம் தேவை' : 'Take care') : (isTa ? 'கலப்பு' : 'Mixed'));
  renderUpcomingDates();
}

// Calendar (.ics) export of muhurthams, the month's observances and Chandrashtamam periods, in
// the page language
function exportMuhurthamsIcs() {
  const data = lastMuhurthams;
  if (!data || !data.results.length) return;
  const events = data.results.flatMap(d => d.windows.map((w, i) => ({
    uid: `muhurtham-${data.event}-${d.date}-${i}`,
    title: txt(`Muhurtham: ${data.event_en}`, `முகூர்த்தம்: ${data.event_ta}`),
    description: txt(`${w.nakshatra} · ${w.tithi} (${w.paksha}) · ${w.lagna} Lagna · ${w.tamil_yogam.en}${w.notes_en.length ? ' · ' + w.notes_en.join(', ') : ''}`,
      `${w.nakshatra_ta} · ${w.tithi_ta} · ${w.lagna_ta} லக்னம் · ${w.tamil_yogam.ta}${w.notes_ta.length ? ' · ' + w.notes_ta.join(', ') : ''}`),
    start: w.start_local, end: w.end_local
  })));
  downloadText(`JoRoScope-Muhurtham-${data.event}-${data.start}.ics`, buildIcs(events, txt('JoRoScope Muhurthams', 'ஜோரோஸ்கோப் முகூர்த்தங்கள்')), 'text/calendar');
}

function exportMonthIcs() {
  const cal = lastCalendar;
  if (!cal) return;
  const events = cal.days.flatMap(d => d.observances.map(o => ({
    uid: `observance-${o.key}-${d.date}`, title: txt(o.en, o.ta),
    description: txt(`${d.tithi_name} · ${d.nakshatra} · ${d.tamil_month} ${d.tamil_day}`, `${d.tithi_ta} · ${d.nakshatra_ta} · ${d.tamil_month_ta} ${d.tamil_day}`),
    start: d.date
  })));
  if (!events.length) {
    notify(txt('No observances this month.', 'இம்மாதம் விரத நாட்கள் இல்லை.'));
    return;
  }
  downloadText(`JoRoScope-Observances-${cal.days[0].date.slice(0, 7)}.ics`, buildIcs(events, txt('JoRoScope Tamil calendar', 'ஜோரோஸ்கோப் தமிழ் நாட்காட்டி')), 'text/calendar');
}

function exportChandrashtamamIcs() {
  const up = currentChart?.south_indian?.upcoming;
  if (!up) return;
  const name = currentChart.profile?.name || 'JoRoScope';
  const events = up.chandrashtamam.periods.map(pr => ({
    uid: `chandrashtamam-${name.replace(/\W+/g, '')}-${pr.start_local.slice(0, 10)}`,
    title: txt(`Chandrashtamam (${name})`, `சந்திராஷ்டமம் (${name})`),
    description: txt('The Moon transits the 8th sign from the birth Moon: avoid starting important work.',
      'சந்திரன் ஜன்ம ராசிக்கு 8-ஆம் ராசியில்: முக்கிய காரியங்களைத் தொடங்குவதைத் தவிர்க்கவும்.'),
    start: pr.start_local, end: pr.end_local
  }));
  downloadText(`JoRoScope-Chandrashtamam-${name.replace(/\W+/g, '-')}.ics`, buildIcs(events, txt('Chandrashtamam', 'சந்திராஷ்டமம்')), 'text/calendar');
}

// Prasna (horary): the question list comes from the server's answer, so the first ask fills it
const PRASNA_QUESTIONS = [
  ['general', 'General question', 'பொதுக் கேள்வி', 'പൊതുവായ ചോദ്യം'], ['marriage', 'Marriage or relationship', 'திருமணம் / உறவு', 'വിവാഹം / ബന്ധം'],
  ['career', 'Job, career or promotion', 'வேலை / தொழில் / பதவி உயர்வு', 'ജോലി / തൊഴിൽ / സ്ഥാനക്കയറ്റം'], ['money', 'Money, loans or business gain', 'பணம் / கடன் / வியாபார லாபம்', 'പണം / കടം / വ്യാപാര ലാഭം'],
  ['health', 'Health or recovery', 'உடல்நலம் / குணமடைதல்', 'ആരോഗ്യം / രോഗശാന്തി'], ['travel', 'Travel or going abroad', 'பயணம் / வெளிநாடு', 'യാത്ര / വിദേശം'],
  ['children', 'Children or conception', 'குழந்தை / கருத்தரிப்பு', 'സന്താനം / ഗർഭധാരണം'], ['property', 'House, land or vehicle', 'வீடு / நிலம் / வாகனம்', 'വീട് / ഭൂമി / വാഹനം'],
  ['education', 'Studies or examinations', 'படிப்பு / தேர்வு', 'പഠനം / പരീക്ഷ'], ['lost', 'A lost or stolen object', 'தொலைந்த / திருடுபோன பொருள்', 'നഷ്ടപ്പെട്ട / മോഷണം പോയ വസ്തു'],
  ['dispute', 'Dispute or court case', 'வழக்கு / தகராறு', 'കേസ് / തർക്കം']
];
let lastPrasna = null;

function fillPrasnaQuestions() {
  const sel = $('#prasna-question');
  if (!sel) return;
  const chosen = sel.value || 'general';
  sel.innerHTML = PRASNA_QUESTIONS.map(([k, en, ta, ml]) => `<option value="${k}">${esc(txt(en, ta, ml))}</option>`).join('');
  sel.value = chosen;
}

async function askPrasna() {
  const form = $('#birth-form');
  const payload = {
    question: $('#prasna-question').value, arudha: $('#prasna-arudha').value || null,
    date: $('#prasna-date').value || '', time: $('#prasna-time').value || '',
    latitude: form.elements['latitude']?.value, longitude: form.elements['longitude']?.value,
    timezone: form.elements['timezone']?.value || 'Asia/Kolkata', ayanamsa: form.elements['ayanamsa']?.value || 'Lahiri'
  };
  const btn = $('#prasna-btn');
  btn.disabled = true;
  try {
    const resp = await fetch('/api/prasna', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
    const data = await resp.json();
    if (!resp.ok) throw new Error(data.error || 'Prasna failed.');
    lastPrasna = data;
    learnMalayalam(data);
    renderChapterInto($('#prasna-result'), data);
  } catch (err) {
    notify(errorText(err.message));
  } finally {
    btn.disabled = false;
  }
}

// Birth time rectification: an editable list of dated life events
const RECT_EVENTS = [
  ['marriage', 'Marriage', 'திருமணம்', 'വിവാഹം'], ['child', 'Birth of a child', 'குழந்தை பிறப்பு', 'കുഞ്ഞിന്റെ ജനനം'],
  ['career', 'Job, promotion or business start', 'வேலை / பதவி உயர்வு / தொழில் தொடக்கம்', 'ജോലി / സ്ഥാനക്കയറ്റം / സംരംഭ തുടക്കം'],
  ['education', 'Degree or education milestone', 'பட்டம் / கல்வி நிலை', 'ബിരുദം / വിദ്യാഭ്യാസ നേട്ടം'],
  ['relocation', 'Moving house or abroad', 'இடமாற்றம் / வெளிநாடு', 'താമസംമാറ്റം / വിദേശം'],
  ['property', 'Buying property or a vehicle', 'சொத்து / வாகனம் வாங்குதல்', 'സ്വത്ത് / വാഹനം വാങ്ങൽ'],
  ['illness', 'Illness, surgery or accident', 'நோய் / அறுவை சிகிச்சை / விபத்து', 'രോഗം / ശസ്ത്രക്രിയ / അപകടം'],
  ['father', 'Loss of father', 'தந்தை இழப்பு', 'അച്ഛന്റെ വിയോഗം'], ['mother', 'Loss of mother', 'தாய் இழப்பு', 'അമ്മയുടെ വിയോഗം']
];
let rectEvents = [{ date: '', type: 'marriage' }];
const RECT_FAMILY = ['elder_brothers', 'elder_sisters', 'younger_brothers', 'younger_sisters'];
let lastRectification = null;

function renderRectEvents() {
  const box = $('#rect-events');
  if (!box) return;
  box.innerHTML = rectEvents.map((ev, i) => `
    <div class="rect-event-row">
      <input type="date" value="${esc(ev.date)}" data-rect-date="${i}" aria-label="Event date">
      <select data-rect-type="${i}" aria-label="Event">${RECT_EVENTS.map(([k, en, ta, ml]) =>
        `<option value="${k}"${k === ev.type ? ' selected' : ''}>${esc(txt(en, ta, ml))}</option>`).join('')}</select>
      <button class="link-btn" type="button" data-rect-remove="${i}" aria-label="Remove">✕</button>
    </div>`).join('');
  box.querySelectorAll('[data-rect-date]').forEach(el => el.addEventListener('change', () => { rectEvents[el.dataset.rectDate].date = el.value; }));
  box.querySelectorAll('[data-rect-type]').forEach(el => el.addEventListener('change', () => { rectEvents[el.dataset.rectType].type = el.value; }));
  box.querySelectorAll('[data-rect-remove]').forEach(el => el.addEventListener('click', () => {
    rectEvents.splice(Number(el.dataset.rectRemove), 1);
    if (!rectEvents.length) rectEvents.push({ date: '', type: 'marriage' });
    renderRectEvents();
  }));
}

async function runRectification() {
  const form = $('#birth-form');
  const birth = Object.fromEntries(new FormData(form));
  const events = rectEvents.filter(ev => ev.date);
  const family = Object.fromEntries(RECT_FAMILY.map(k => [k, $(`#rect-${k.replace('_', '-')}`)?.value]).filter(([, v]) => v !== '' && v != null));
  const btn = $('#rect-run');
  btn.disabled = true;
  try {
    const resp = await fetch('/api/rectify', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ birth, events, family, window: Number($('#rect-window').value), step: 2 })
    });
    const data = await resp.json();
    if (!resp.ok) throw new Error(data.error || 'Rectification failed.');
    lastRectification = data;
    learnMalayalam(data);
    renderChapterInto($('#rect-result'), data);
  } catch (err) {
    notify(errorText(err.message));
  } finally {
    btn.disabled = false;
  }
}
