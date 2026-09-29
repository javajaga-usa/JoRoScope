/**
 * JoRoScope: The chart views: South, North, East Indian and Sri Lankan charts, the house inspector, the
 * planets table, Ashtakavarga, and yogas and doshas.
 * A classic script sharing the page's global scope with app.js; see index.html for the order.
 */

// Chart Style & Varga Switching
function setChartStyle(style) {
  currentStyle = style;
  ['south', 'north', 'east', 'srilanka', 'dual'].forEach(st => {
    $(`#btn-${st}-style`).classList.toggle('active', style === st);
    $(`#${st}-chart-container`).hidden = (style !== st);
  });

  renderCurrentChart();
}

function setVarga(varga) {
  currentVarga = varga;
  $$('.varga-pill').forEach(b => b.classList.toggle('active', b.dataset.varga === varga));
  renderCurrentChart();
}

function vargaTitle(varga) {
  const [en, ta] = VARGA_NAMES[varga] || [varga, varga];
  return currentLang === 'ta' ? ta : (varga === 'Bhava' ? `${en} (Sripati)` : `${en} (${varga})`);
}

function renderCurrentChart() {
  if (!currentChart) return;
  // Rasi + Navamsa always shows D1 on the left; the right panel follows the varga pills (D9 by default).
  const amsa = currentVarga === 'D1' ? 'D9' : currentVarga;
  $('#current-varga-display').textContent = currentStyle === 'dual'
    ? `${vargaTitle('D1')} + ${vargaTitle(amsa)}`
    : vargaTitle(currentVarga);
  $('#legend-retro').textContent = currentLang === 'ta' ? '(வ) வக்ரம்' : 'Rx Retro';
  $('#legend-lagna').textContent = currentLang === 'ta' ? '╱ லக்னம்' : '╱ Lagna';

  if (currentStyle === 'south') {
    renderSouthChart($('#south-chart-container'), currentVarga);
  } else if (currentStyle === 'dual') {
    renderSouthChart($('#dual-rasi-grid'), 'D1', true);
    renderSouthChart($('#dual-amsa-grid'), amsa, true);
  } else if (currentStyle === 'north') {
    renderNorthChart();
  } else if (currentStyle === 'east') {
    renderEastChart();
  } else if (currentStyle === 'srilanka') {
    renderSriLankanChart();
  }
}

// Grahas plus Mandi (Maandhi), which Tamil and Kerala charts always show
function chartBodies() {
  const bodies = Object.entries(currentChart.planets);
  const mandi = currentChart.south_indian?.mandi;
  if (mandi) bodies.push(['Mandi', mandi]);
  return bodies;
}

function grahaAbbrev(pName) {
  const meta = PLANET_NAMES[pName];
  return currentLang === 'ta' ? meta.ta_short : (currentLang === 'ml' ? ML_SHORT[pName] : meta.short);
}

// Balance of the birth Maha Dasa as years / months / days (வருடம் / மாதம் / நாள்)
function irruppuSpan(irr) {
  return currentLang === 'ta'
    ? `${irr.years} வ ${irr.months} மா ${irr.days} நா`
    : `${irr.years}y ${irr.months}m ${irr.days}d`;
}

function dasaIrruppuText(irr) {
  if (!irr) return '';
  return currentLang === 'ta'
    ? `${irr.lord_ta} தசை இருப்பு: ${irruppuSpan(irr)}`
    : `${irr.lord} Dasa balance: ${irruppuSpan(irr)}`;
}

// 1. South Indian Layout (Traditional 4x4 Grid with Fixed Signs)
function renderSouthChart(container, varga, compact = false) {
  container.replaceChildren();
  const isTa = currentLang === 'ta';

  // South Indian Sign positions [row, col] (1-indexed)
  // 0: Aries (1,2), 1: Taurus (1,3), 2: Gemini (1,4), 3: Cancer (2,4), 4: Leo (3,4), 5: Virgo (4,4),
  // 6: Libra (4,3), 7: Scorpio (4,2), 8: Sagittarius (4,1), 9: Capricorn (3,1), 10: Aquarius (2,1), 11: Pisces (1,1)
  const pos = [
    [1, 2], [1, 3], [1, 4], [2, 4],
    [3, 4], [4, 4], [4, 3], [4, 2],
    [4, 1], [3, 1], [2, 1], [1, 1]
  ];

  // Houses count from this varga's own Lagna; the inspector describes the Rasi (D1) house.
  const vargaAsc = currentChart.planets.Ascendant.vargas[varga];
  const rasiAsc = currentChart.planets.Ascendant.sign_index;
  const bodies = chartBodies();

  for (let s = 0; s < 12; s++) {
    const cell = document.createElement('div');
    cell.className = `house-cell${s === vargaAsc ? ' lagna-cell' : ''}`;
    cell.style.gridArea = `${pos[s][0]} / ${pos[s][1]}`;

    const houseNum = (s - vargaAsc + 12) % 12 + 1;

    const header = document.createElement('div');
    header.className = 'house-header';
    header.innerHTML = `
      <div>
        <span class="sign-label">${isTa ? SIGNS_TA[s] : SIGNS_EN[s]}</span>
        ${compact ? '' : `<span class="tamil-sign-label" data-keep-en>${currentLang === 'en' ? SIGNS_TA[s] : SIGNS_EN[s]}</span>`}
      </div>
      <span class="house-num-badge">${isTa ? houseNum : `H${houseNum}`}</span>
    `;
    cell.append(header);

    const flow = document.createElement('div');
    flow.className = 'house-planets-flow';

    bodies.forEach(([pName, pData]) => {
      if (pData.vargas[varga] !== s) return;
      const badge = document.createElement('span');
      const isAsc = pName === 'Ascendant';
      const isBenefic = ['Jupiter', 'Venus', 'Moon', 'Mercury'].includes(pName);
      const kind = isAsc ? 'asc' : (pName === 'Mandi' ? 'upagraha' : (isBenefic ? 'benefic' : 'malefic'));
      badge.className = `planet-badge ${kind} ${pData.retrograde && !['Rahu', 'Ketu'].includes(pName) ? 'retro' : ''} ${pData.combust ? 'combust' : ''}`;
      badge.dataset.retro = isTa ? '(வ)' : 'ᴿ';
      badge.title = `${isTa ? PLANET_NAMES[pName].ta : PLANET_NAMES[pName].en} ${formatDegrees(pData.degree)}`;
      badge.textContent = grahaAbbrev(pName);
      if (varga === 'D1' && !compact) {
        const deg = document.createElement('small');
        deg.className = 'badge-deg';
        deg.textContent = `${Math.floor(pData.degree)}°`;
        badge.append(deg);
      }
      flow.append(badge);
    });

    cell.append(flow);
    cell.onclick = () => openHouseInspector((s - rasiAsc + 12) % 12 + 1, s);
    container.append(cell);
  }

  // Center box: the birth details a Tamil jathagam writes between the houses
  const prof = currentChart.profile;
  const center = document.createElement('div');
  center.className = 'chart-center-box';
  const irruppu = varga === 'D1' ? dasaIrruppuText(currentChart.south_indian?.dasa_irruppu) : '';
  center.innerHTML = `
    ${compact ? '' : '<span class="center-star">✦</span>'}
    <h3 class="center-title">${esc(isTa ? VARGA_NAMES[varga]?.[1] : VARGA_NAMES[varga]?.[0] || varga)}</h3>
    <p class="center-sub">${esc(prof.name || 'JoRoScope')}</p>
    <span class="center-meta">${esc(prof.date)} · ${esc(prof.time)}${prof.city ? ` · ${esc(prof.city)}` : ''}</span>
    ${irruppu ? `<span class="center-irruppu">${esc(irruppu)}</span>` : ''}
  `;
  container.append(center);
}

// Colours for the SVG charts: the page theme on screen, black on white on paper
function chartPalette(print = false) {
  if (print) return { fill: '#ffffff', lagnaFill: '#f1ece0', stroke: '#444444', text: '#111111', accent: '#333333' };
  const light = document.documentElement.getAttribute('data-theme') === 'light';
  return light
    ? { fill: '#fafbf7', lagnaFill: '#f3ead2', stroke: '#b38628', text: '#15221b', accent: '#b38628' }
    : { fill: 'rgba(15, 20, 42, 0.6)', lagnaFill: 'rgba(229, 195, 120, 0.14)', stroke: '#e5c378', text: '#ffffff', accent: '#e5c378' };
}

// Graha labels for an SVG chart cell, retrograde marked
function svgGrahaLabels(varga, sign) {
  const isTa = currentLang === 'ta';
  return chartBodies()
    .filter(([, pData]) => pData.vargas[varga] === sign)
    .map(([n, pData]) => `${grahaAbbrev(n)}${pData.retrograde && !['Rahu', 'Ketu'].includes(n) ? (isTa ? '(வ)' : 'ᴿ') : ''}`);
}

// 2. North Indian Diamond Layout (SVG Renderer). Houses are fixed with the Lagna in the top
// diamond and run anticlockwise; the Sri Lankan (Sinhala) kendaraya is the same drawing with
// the houses running clockwise, so it is this chart mirrored left to right.
const DIAMOND_HOUSES = [  // outline, centre of the graha labels, sign number, labels per line
  { path: [[300, 0], [450, 150], [300, 300], [150, 150]], text: [300, 150], num: [300, 40], per: 3 },
  { path: [[300, 0], [150, 150], [0, 0]], text: [150, 52], num: [150, 124], per: 3 },
  { path: [[0, 0], [150, 150], [0, 300]], text: [52, 150], num: [124, 150], per: 2 },
  { path: [[0, 300], [150, 150], [300, 300], [150, 450]], text: [150, 300], num: [60, 300], per: 3 },
  { path: [[0, 300], [150, 450], [0, 600]], text: [52, 450], num: [124, 450], per: 2 },
  { path: [[0, 600], [150, 450], [300, 600]], text: [150, 548], num: [150, 476], per: 3 },
  { path: [[300, 600], [150, 450], [300, 300], [450, 450]], text: [300, 450], num: [300, 560], per: 3 },
  { path: [[300, 600], [450, 450], [600, 600]], text: [450, 548], num: [450, 476], per: 3 },
  { path: [[600, 600], [450, 450], [600, 300]], text: [548, 450], num: [476, 450], per: 2 },
  { path: [[600, 300], [450, 450], [300, 300], [450, 150]], text: [450, 300], num: [540, 300], per: 3 },
  { path: [[600, 300], [450, 150], [600, 0]], text: [548, 150], num: [476, 150], per: 2 },
  { path: [[600, 0], [450, 150], [300, 0]], text: [450, 52], num: [450, 124], per: 3 }
];

function renderDiamondChart(svg, varga, { mirror = false, print = false } = {}) {
  const NS = 'http://www.w3.org/2000/svg';
  svg.replaceChildren();
  const pal = chartPalette(print);
  const ascSign = currentChart.planets.Ascendant.vargas[varga];
  const rasiAsc = currentChart.planets.Ascendant.sign_index;
  const fx = x => (mirror ? 600 - x : x);
  const text = (x, y, content, size, color, weight = 700) => {
    const t = document.createElementNS(NS, 'text');
    t.setAttribute('x', fx(x));
    t.setAttribute('y', y);
    t.setAttribute('fill', color);
    t.setAttribute('font-size', size);
    t.setAttribute('font-weight', weight);
    t.setAttribute('text-anchor', 'middle');
    t.setAttribute('dominant-baseline', 'middle');
    t.textContent = content;
    return t;
  };

  DIAMOND_HOUSES.forEach((house, i) => {
    const signIdx = (ascSign + i) % 12;
    const g = document.createElementNS(NS, 'g');
    if (!print) {
      g.style.cursor = 'pointer';
      // The inspector describes the Rasi (D1) house of this sign
      g.onclick = () => openHouseInspector((signIdx - rasiAsc + 12) % 12 + 1, signIdx);
    }
    const path = document.createElementNS(NS, 'path');
    path.setAttribute('d', 'M ' + house.path.map(([x, y]) => `${fx(x)},${y}`).join(' L ') + ' Z');
    path.setAttribute('fill', i === 0 ? pal.lagnaFill : pal.fill);
    path.setAttribute('stroke', pal.stroke);
    path.setAttribute('stroke-width', '1.2');
    g.append(path);
    // Sign number (1 = Aries ... 12 = Pisces), as North Indian and Sinhala charts write it
    g.append(text(house.num[0], house.num[1], signIdx + 1, print ? 20 : 14, pal.accent));
    const names = svgGrahaLabels(varga, signIdx);
    const lines = [];
    for (let k = 0; k < names.length; k += house.per) lines.push(names.slice(k, k + house.per).join(' '));
    // Paper charts are small, so their text is drawn larger
    const size = print ? 22 : 14;
    lines.forEach((line, k) => g.append(text(house.text[0], house.text[1] + (k - (lines.length - 1) / 2) * (size + 3), line, size, pal.text)));
    svg.append(g);
  });
}

function renderNorthChart() {
  renderDiamondChart($('#north-svg'), currentVarga);
}

function renderSriLankanChart() {
  renderDiamondChart($('#srilanka-svg'), currentVarga, { mirror: true });
}

// 3. East Indian Layout (SVG Renderer): signs are fixed with Aries at the top centre,
// running anticlockwise; each corner square is split diagonally toward the centre.
const EAST_CELLS = [
  { pts: '200,0 400,0 400,200 200,200', at: [300, 100] },    // Aries
  { pts: '0,0 200,0 200,200', at: [133, 62] },               // Taurus
  { pts: '0,0 0,200 200,200', at: [67, 138] },               // Gemini
  { pts: '0,200 200,200 200,400 0,400', at: [100, 300] },    // Cancer
  { pts: '0,400 200,400 0,600', at: [67, 462] },             // Leo
  { pts: '200,400 200,600 0,600', at: [133, 538] },          // Virgo
  { pts: '200,400 400,400 400,600 200,600', at: [300, 500] }, // Libra
  { pts: '400,400 400,600 600,600', at: [467, 538] },        // Scorpio
  { pts: '400,400 600,400 600,600', at: [533, 462] },        // Sagittarius
  { pts: '400,200 600,200 600,400 400,400', at: [500, 300] }, // Capricorn
  { pts: '400,200 600,200 600,0', at: [533, 138] },          // Aquarius
  { pts: '400,0 600,0 400,200', at: [467, 62] }              // Pisces
];

function renderEastChart(svg = $('#east-svg'), varga = currentVarga, { print = false } = {}) {
  svg.replaceChildren();
  const NS = 'http://www.w3.org/2000/svg';
  const isTa = currentLang === 'ta';
  const pal = chartPalette(print);
  const [fill, lagnaFill, stroke, textColor] = [pal.fill, pal.lagnaFill, pal.stroke, pal.text];

  const vargaAsc = currentChart.planets.Ascendant.vargas[varga];
  const rasiAsc = currentChart.planets.Ascendant.sign_index;

  const text = (x, y, content, size, color, weight = 700) => {
    const t = document.createElementNS(NS, 'text');
    t.setAttribute('x', x);
    t.setAttribute('y', y);
    t.setAttribute('fill', color);
    t.setAttribute('font-size', size);
    t.setAttribute('font-weight', weight);
    t.setAttribute('text-anchor', 'middle');
    t.textContent = content;
    return t;
  };

  EAST_CELLS.forEach((cell, s) => {
    const g = document.createElementNS(NS, 'g');
    if (!print) {
      g.style.cursor = 'pointer';
      g.onclick = () => openHouseInspector((s - rasiAsc + 12) % 12 + 1, s);
    }

    const poly = document.createElementNS(NS, 'polygon');
    poly.setAttribute('points', cell.pts);
    poly.setAttribute('fill', s === vargaAsc ? lagnaFill : fill);
    poly.setAttribute('stroke', stroke);
    poly.setAttribute('stroke-width', s === vargaAsc ? '2.4' : '1.2');
    g.append(poly);

    const [x, y] = cell.at;
    const houseNum = (s - vargaAsc + 12) % 12 + 1;
    const signName = isTa ? SIGNS_TA[s] : SIGNS_EN[s].slice(0, 3);
    g.append(text(x, y - 22, `${signName} · ${isTa ? houseNum : `H${houseNum}`}`, 11, stroke));

    // Up to three grahas per line so the corner triangles stay legible
    const names = svgGrahaLabels(varga, s);
    for (let i = 0; i < names.length; i += 3) {
      g.append(text(x, y + (i / 3) * 16, names.slice(i, i + 3).join(' '), 12, textColor));
    }
    svg.append(g);
  });

  const title = VARGA_NAMES[varga] || [varga, varga];
  svg.append(text(300, 292, isTa ? title[1] : title[0], 18, stroke));
  svg.append(text(300, 316, currentChart.profile.name || 'JoRoScope', 12, textColor, 500));
}

// House Inspector Drawer
function openHouseInspector(houseNum, signIdx) {
  if (!currentChart) return;
  const inspector = $('#house-inspector-card');
  inspector.hidden = false;

  const sign = signName(signIdx);
  const signLord = grahaName(currentChart.house_details[houseNum - 1].lord);

  $('#inspect-title').textContent = txt(`House ${houseNum} (${sign}) Inspector`, `${houseNum}-ம் பாவம் (${sign}) விவரம்`);
  $('#inspect-sign').textContent = txt(
    `Sign: ${sign} · Lord: ${signLord} · House ${houseNum} from Lagna`,
    `ராசி: ${sign} · அதிபதி: ${signLord} · லக்னத்திலிருந்து ${houseNum}-ம் பாவம்`,
    `രാശി: ${sign} · നാഥൻ: ${signLord} · ലഗ്നത്തിൽ നിന്ന് ${houseNum}-ാം ഭാവം`);

  // Occupants in D1
  const occupants = Object.entries(currentChart.planets).filter(([n, p]) => p.house === houseNum);
  const occEl = $('#inspect-occupants');
  occEl.replaceChildren();
  if (occupants.length) {
    occupants.forEach(([n, p]) => {
      const pill = document.createElement('span');
      pill.className = 'planet-badge';
      pill.textContent = `${grahaName(n)} (${formatDegrees(p.degree)})`;
      occEl.append(pill);
    });
  } else {
    occEl.innerHTML = `<span class="muted">${txt('No occupant planets', 'கிரகங்கள் இல்லை')}</span>`;
  }

  // Aspects received
  const aspecting = Object.entries(currentChart.planets).filter(([n, p]) => {
    return n !== 'Ascendant' && p.aspects_cast && p.aspects_cast.includes(houseNum);
  });
  const aspEl = $('#inspect-aspects');
  aspEl.replaceChildren();
  if (aspecting.length) {
    aspecting.forEach(([n, p]) => {
      const pill = document.createElement('span');
      pill.className = 'planet-badge benefic';
      pill.textContent = txt(`${grahaName(n)} (from H${p.house})`, `${grahaName(n)} (${p.house}-ம் பாவத்திலிருந்து)`);
      aspEl.append(pill);
    });
  } else {
    aspEl.innerHTML = `<span class="muted">${txt('No direct major aspects', 'நேரடிப் பார்வைகள் இல்லை')}</span>`;
  }

  // Ashtakavarga SAV points
  const sav = currentChart.ashtakavarga.SAV[signIdx];
  $('#inspect-sav').textContent = txt(`${sav} Bindus`, `${sav} பரல்கள்`);

  // Significations
  $('#inspect-significations').textContent = txt(HOUSE_BHAVAS[houseNum], HOUSE_BHAVAS_TA[houseNum]);

  inspector.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Planets Table Rendering
function renderPlanetsTable() {
  if (!currentChart) return;
  const tbody = $('#planets-tbody');
  tbody.replaceChildren();

  Object.entries(currentChart.planets).forEach(([pName, p]) => {
    const tr = document.createElement('tr');
    const signName = currentLang === 'ta' ? p.tamil : p.sign;
    const starName = currentLang === 'ta' ? p.tamil_nakshatra : p.nakshatra;
    const pLabel = currentLang === 'ta' ? PLANET_NAMES[pName].ta : PLANET_NAMES[pName].en;

    const dignityClass = (p.dignity || '').toLowerCase().replace(/\s+/g, '-');
    const aspectsCastStr = (p.aspects_cast || []).join(', ') || '—';

    tr.innerHTML = `
      <td><strong>${pLabel}</strong></td>
      <td>${signName}</td>
      <td>${formatDegrees(p.degree)}</td>
      <td>${starName} (${txt('Pada', 'பாதம்')} ${p.pada})</td>
      <td><strong>${txt(`House ${p.house}`, `${p.house}-ம் பாவம்`)}</strong></td>
      <td>${p.bhava ? txt(`Bhava ${p.bhava}`, `${p.bhava}-ம் பாவம்`) : '—'}${p.bhava && p.bhava !== p.house ? ' ⇄' : ''}</td>
      <td><span class="dignity-badge ${dignityClass}">${dignityLabel(p.dignity)}</span></td>
      <td>${p.retrograde ? `<span class="legend-badge retro">${txt('Retrograde (Rx)', 'வக்ரம் (வ)')}</span>` : txt('Direct', 'நேர்கதி')} ${p.combust ? `<span class="legend-badge combust">🔥 ${txt('Combust', 'அஸ்தங்கம்')}</span>` : ''}</td>
      <td>${aspectsCastStr}</td>
    `;
    tbody.append(tr);
  });
}

// Ashtakavarga Rendering
function renderAshtakavarga() {
  if (!currentChart || !currentChart.ashtakavarga) return;
  const sav = currentChart.ashtakavarga.SAV;
  const bav = currentChart.ashtakavarga.BAV;

  // Render 12 SAV Cards
  const grid = $('#sav-signs-grid');
  grid.replaceChildren();

  sav.forEach((pts, idx) => {
    const card = document.createElement('div');
    const isStrong = pts >= 28;
    card.className = `sav-sign-card ${isStrong ? 'strong' : 'moderate'}`;
    card.innerHTML = `
      <small>${currentLang === 'ta' ? SIGNS_TA[idx] : SIGNS_EN[idx]}</small>
      <div class="sav-points">${pts}</div>
      <span class="muted">${isStrong ? txt('Auspicious', 'சுபம்') : txt('Average', 'சராசரி')}</span>
    `;
    grid.append(card);
  });

  // Render BAV Table
  const thead = $('#bav-header');
  thead.innerHTML = `<th>${txt('Planet', 'கிரகம்')}</th>` + SIGNS_EN.map((s, i) => `<th>${currentLang === 'ta' ? SIGNS_TA[i] : s.slice(0, 3)}</th>`).join('') + `<th>${txt('Total', 'மொத்தம்')}</th>`;

  const tbody = $('#bav-tbody');
  tbody.replaceChildren();

  Object.entries(bav).forEach(([pName, row]) => {
    const tr = document.createElement('tr');
    const rowSum = row.reduce((a, b) => a + b, 0);
    tr.innerHTML = `<td><strong>${grahaName(pName)}</strong></td>` + row.map(v => `<td>${v}</td>`).join('') + `<td><strong>${rowSum}</strong></td>`;
    tbody.append(tr);
  });

  // Sodhita (reduced) bindus with the Rasi, Graha and Sodhya Pindas
  const { sodhita, pindas } = currentChart.ashtakavarga;
  const sHead = $('#sodhana-header');
  const sBody = $('#sodhana-tbody');
  if (sHead && sBody && sodhita && pindas) {
    sHead.innerHTML = `<th>${txt('Planet', 'கிரகம்')}</th>` + SIGNS_EN.map((s, i) => `<th>${currentLang === 'ta' ? SIGNS_TA[i] : s.slice(0, 3)}</th>`).join('')
      + `<th>${txt('Rasi Pinda', 'ராசி பிண்டம்')}</th><th>${txt('Graha Pinda', 'கிரக பிண்டம்')}</th><th>${txt('Sodhya Pinda', 'சோத்ய பிண்டம்')}</th>`;
    sBody.replaceChildren();
    Object.entries(sodhita).forEach(([pName, row]) => {
      const pin = pindas[pName];
      const tr = document.createElement('tr');
      tr.innerHTML = `<td><strong>${grahaName(pName)}</strong></td>` + row.map(v => `<td>${v}</td>`).join('')
        + `<td>${pin.rasi}</td><td>${pin.graha}</td><td><strong style="color:var(--gold)">${pin.sodhya}</strong></td>`;
      sBody.append(tr);
    });
  }
}

// Yogas & Doshas Rendering
function renderYogasAndDoshas() {
  if (!currentChart) return;
  const yogas = currentChart.yogas || [];
  const doshas = currentChart.doshas || {};

  const isTa = currentLang === 'ta';
  const houseWord = h => isTa ? `${h}-ம் வீடு` : `house ${h}`;

  // Chevvai Dosham: Tamil rule from Lagna, Moon and Venus
  const cv = doshas.chevvai;
  const mCard = $('#manglik-card');
  if (cv) {
    const status = $('#manglik-status');
    if (cv.effective) {
      mCard.className = 'cosmic-card dosha-card active-dosha';
      status.className = 'status-pill danger';
      status.textContent = isTa ? `உள்ளது (${cv.severity}/3)` : `Present (${cv.severity} of 3)`;
    } else if (cv.present) {
      mCard.className = 'cosmic-card dosha-card cancelled-dosha';
      status.className = 'status-pill success';
      status.textContent = isTa ? 'உள்ளது, ஆனால் நிவர்த்தி' : 'Present but Cancelled';
    } else {
      mCard.className = 'cosmic-card dosha-card';
      status.className = 'status-pill neutral';
      status.textContent = isTa ? 'இல்லை' : 'Not Present';
    }
    $('#manglik-desc').textContent = txt(
      `Mars is in ${cv.mars_sign}. The dosha arises when Mars occupies houses 2, 4, 7, 8 or 12 counted from Lagna, Moon or Venus.`,
      `செவ்வாய் ${cv.mars_sign_ta} ராசியில் உள்ளது. லக்னம், சந்திரன், சுக்கிரனிலிருந்து 2, 4, 7, 8, 12-ம் வீடுகளில் செவ்வாய் இருந்தால் தோஷம்.`,
      `ചൊവ്വ ${mlTerm(cv.mars_sign)} രാശിയിലാണ്. ലഗ്നം, ചന്ദ്രൻ, ശുക്രൻ എന്നിവയിൽ നിന്ന് 2, 4, 7, 8, 12 ഭാവങ്ങളിൽ ചൊവ്വ നിന്നാൽ ദോഷം.`);
    $('#chevvai-references').innerHTML = cv.references.map(r => {
      const state = r.afflicting ? (isTa ? 'தோஷம்' : 'afflicts') : (r.exempt ? (isTa ? 'விதிவிலக்கு' : 'exempt by sign') : (isTa ? 'தோஷமில்லை' : 'clear'));
      const cls = r.afflicting ? 'danger' : (r.exempt ? 'success' : 'neutral');
      return `<div class="dosha-ref"><span>${esc(isTa ? r.reference_ta : r.reference)}</span><span>${houseWord(r.house)}</span><span class="status-pill ${cls}">${state}</span></div>`;
    }).join('');
    $('#manglik-reasons').innerHTML = cv.cancellations.map(c => `<div>✔ ${esc(isTa ? c.ta : c.en)}</div>`).join('');
  }
  const m = doshas.manglik;
  if (m) {
    const northState = !m.present ? (isTa ? 'இல்லை' : 'not present')
      : (m.cancelled ? (isTa ? 'நிவர்த்தி' : 'cancelled') : (isTa ? 'உள்ளது' : 'present'));
    $('#manglik-north-note').textContent = isTa
      ? `வட இந்திய மாங்கலிக் விதி (லக்னத்திலிருந்து 1, 2, 4, 7, 8, 12): ${northState}.`
      : `North Indian Manglik rule (1, 2, 4, 7, 8, 12 from Lagna only): ${northState}.`;
  }

  // Rahu-Ketu Dosham
  const rk = doshas.rahu_ketu;
  const rkCard = $('#rahuketu-card');
  if (rk) {
    const status = $('#rahuketu-status');
    rkCard.className = `cosmic-card dosha-card${rk.present ? ' active-dosha' : ''}`;
    status.className = `status-pill ${rk.present ? 'danger' : 'neutral'}`;
    status.textContent = rk.present ? (isTa ? 'உள்ளது' : 'Present') : (isTa ? 'இல்லை' : 'Not Present');
    $('#rahuketu-desc').textContent = txt(
      'Arises when Rahu or Ketu occupies houses 1, 2, 7 or 8 from Lagna or Moon. In matching, it is best balanced by a similar dosha in the partner.',
      'லக்னம் அல்லது சந்திரனிலிருந்து 1, 2, 7, 8-ம் வீடுகளில் ராகு அல்லது கேது இருந்தால் தோஷம்; திருமணப் பொருத்தத்தில் இருவருக்கும் சமமாக இருப்பது நல்லது.',
      'ലഗ്നം അല്ലെങ്കിൽ ചന്ദ്രനിൽ നിന്ന് 1, 2, 7, 8 ഭാവങ്ങളിൽ രാഹുവോ കേതുവോ നിന്നാൽ ദോഷം; വിവാഹപ്പൊരുത്തത്തിൽ ഇരുവർക്കും സമാനമായിരിക്കുന്നത് നല്ലത്.');
    $('#rahuketu-references').innerHTML = rk.references.map(r => {
      const nodes = isTa ? `ராகு ${r.rahu_house} · கேது ${r.ketu_house}` : `Rahu ${r.rahu_house} · Ketu ${r.ketu_house}`;
      const cls = r.afflicting ? 'danger' : 'neutral';
      const state = r.afflicting ? (isTa ? 'தோஷம்' : 'afflicts') : (isTa ? 'தோஷமில்லை' : 'clear');
      return `<div class="dosha-ref"><span>${esc(isTa ? r.reference_ta : r.reference)}</span><span>${nodes}</span><span class="status-pill ${cls}">${state}</span></div>`;
    }).join('');
  }

  // Kaal Sarp
  const ks = doshas.kaal_sarp;
  const ksCard = $('#kaalsarp-card');
  if (ks) {
    if (ks.present) {
      ksCard.className = 'cosmic-card dosha-card active-dosha';
      $('#kaalsarp-status').className = 'status-pill danger';
      $('#kaalsarp-status').textContent = txt(ks.type, ks.type_ta);
      $('#kaalsarp-desc').textContent = txt(ks.description, ks.description_ta);
    } else {
      ksCard.className = 'cosmic-card dosha-card';
      $('#kaalsarp-status').className = 'status-pill neutral';
      $('#kaalsarp-status').textContent = txt('Not Present', 'இல்லை');
      $('#kaalsarp-desc').textContent = txt(ks.description, ks.description_ta);
    }
  }

  // Detected Yogas Grid
  $('#yogas-count').textContent = txt(`${yogas.length} Detected`, `${yogas.length} யோகங்கள்`);
  const grid = $('#yogas-grid');
  grid.replaceChildren();

  if (yogas.length) {
    yogas.forEach(y => {
      const card = document.createElement('div');
      card.className = 'yoga-card';
      card.innerHTML = `
        <h3>${esc(txt(y.name, y.name_ta))}</h3>
        <div class="yoga-meta">${esc(txt(y.category, y.category_ta))} · <span style="color:${{ good: 'var(--emerald)', mixed: 'var(--gold)', bad: 'var(--ruby)' }[y.nature] || 'var(--text-muted)'}">${esc(txt(y.auspiciousness, y.auspiciousness_ta))}</span></div>
        <p class="yoga-desc">${esc(txt(y.description, y.description_ta))}</p>
        <div class="pill-list" style="margin-top:8px">
          ${(y.planets || []).map(p => `<span class="planet-badge ${y.nature === 'bad' ? 'malefic' : 'benefic'}">${grahaName(p)}</span>`).join('')}
        </div>
      `;
      grid.append(card);
    });
  } else {
    grid.innerHTML = `<p class="muted">${txt('No major classical yogas triggered under primary rules.', 'முதன்மை விதிகளின்படி முக்கிய யோகங்கள் எதுவும் அமையவில்லை.')}</p>`;
  }
}
