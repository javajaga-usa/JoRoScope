/**
 * JoRoScope: The Dasa page: Vimshottari, Yogini, Ashtottari and Chara Dasa, and the Dasa-Bhukti timeline
 * with its readings loaded on demand.
 * A classic script sharing the page's global scope with app.js; see index.html for the order.
 */

// 3-Tier Vimshottari Dasa Accordion
function renderDashaAccordion() {
  if (!currentChart || !currentChart.dasha) return;
  const container = $('#dasa-accordion');
  container.replaceChildren();

  currentChart.dasha.forEach(d => {
    const details = document.createElement('details');
    details.className = 'dasa-item';
    if (d.is_active) details.open = true;

    const summary = document.createElement('summary');
    summary.className = `dasa-summary ${d.is_active ? 'active-period' : ''}`;
    summary.innerHTML = `
      <div>
        <span class="dasa-name">${txt(`${d.lord} Maha Dasa`, `${grahaName(d.lord)} மகா தசை`)}</span>
        ${d.is_active ? `<span class="status-pill success" style="margin-left:8px">${txt('ACTIVE', 'நடப்பில்')}</span>` : ''}
      </div>
      <span class="dasa-dates">${localDate(d.start)} → ${localDate(d.end)}</span>
    `;
    details.append(summary);

    // Subperiods table
    const table = document.createElement('table');
    table.className = 'luxury-table bhukti-table';
    table.innerHTML = `
      <thead>
        <tr>
          <th>${txt('Bhukti', 'புக்தி')}</th>
          <th>${txt('Pratyantardasa Details', 'அந்தர விவரங்கள்')}</th>
          <th>${txt('Start', 'தொடக்கம்')}</th>
          <th>${txt('End', 'முடிவு')}</th>
        </tr>
      </thead>
      <tbody>
        ${d.subperiods.map(b => `
          <tr class="${b.is_active ? 'active-period' : ''}">
            <td><strong>${grahaName(b.lord)}</strong> ${b.is_active ? `<span class="status-pill success">${txt('Active', 'நடப்பில்')}</span>` : ''}</td>
            <td>${(b.pratyantars || []).map(p => `<span class="planet-badge ${p.is_active ? 'asc' : ''}" style="margin:2px">${grahaName(p.lord)}</span>`).join('')}</td>
            <td>${localDate(b.start)}</td>
            <td>${localDate(b.end)}</td>
          </tr>
        `).join('')}
      </tbody>
    `;
    details.append(table);
    container.append(details);
  });
}

// Yogini Dasa accordion: each yogini with its ruling graha, then its eight bhuktis
function renderYoginiAccordion() {
  const container = $('#yogini-accordion');
  const rows = currentChart?.yogini_dasha;
  if (!container || !rows) return;
  const yName = y => txt(`${y.yogini} (${grahaName(y.lord)})`, `${y.yogini_ta} (${grahaName(y.lord)})`);
  container.innerHTML = rows.map(d => `
    <details class="dasa-item"${d.is_active ? ' open' : ''}>
      <summary class="dasa-summary ${d.is_active ? 'active-period' : ''}">
        <div>
          <span class="dasa-name">${esc(yName(d))} · ${d.years} ${txt(d.years === 1 ? 'year' : 'years', 'ஆண்டு')}</span>
          ${d.is_active ? `<span class="status-pill success" style="margin-left:8px">${txt('ACTIVE', 'நடப்பில்')}</span>` : ''}
        </div>
        <span class="dasa-dates">${localDate(d.start)} → ${localDate(d.end)}</span>
      </summary>
      <table class="luxury-table bhukti-table">
        <thead><tr><th>${txt('Bhukti', 'புக்தி')}</th><th>${txt('Start', 'தொடக்கம்')}</th><th>${txt('End', 'முடிவு')}</th></tr></thead>
        <tbody>${d.subperiods.map(b => `
          <tr class="${b.is_active ? 'active-period' : ''}">
            <td><strong>${esc(yName(b))}</strong>${b.is_active ? ` <span class="status-pill success">${txt('Active', 'நடப்பில்')}</span>` : ''}</td>
            <td>${localDate(b.start)}</td><td>${localDate(b.end)}</td>
          </tr>`).join('')}
        </tbody>
      </table>
    </details>`).join('');
}

// Ashtottari and Chara Dasa accordions share one layout: a dasa row, then its sub-periods
function renderPeriodAccordion(container, rows, nameOf, subNameOf, subLabel) {
  if (!container || !rows) return;
  const yearsText = y => txt(`${y} ${y === 1 ? 'year' : 'years'}`, `${y} ஆண்டு`);
  container.innerHTML = rows.map(d => `
    <details class="dasa-item"${d.is_active ? ' open' : ''}>
      <summary class="dasa-summary ${d.is_active ? 'active-period' : ''}">
        <div>
          <span class="dasa-name">${esc(nameOf(d))} · ${yearsText(d.years)}</span>
          ${d.is_active ? `<span class="status-pill success" style="margin-left:8px">${txt('ACTIVE', 'நடப்பில்')}</span>` : ''}
        </div>
        <span class="dasa-dates">${localDate(d.start)} → ${localDate(d.end)}</span>
      </summary>
      <table class="luxury-table bhukti-table">
        <thead><tr><th>${subLabel}</th><th>${txt('Start', 'தொடக்கம்')}</th><th>${txt('End', 'முடிவு')}</th></tr></thead>
        <tbody>${d.subperiods.map(b => `
          <tr class="${b.is_active ? 'active-period' : ''}">
            <td><strong>${esc(subNameOf(b))}</strong>${b.is_active ? ` <span class="status-pill success">${txt('Active', 'நடப்பில்')}</span>` : ''}</td>
            <td>${localDate(b.start)}</td><td>${localDate(b.end)}</td>
          </tr>`).join('')}
        </tbody>
      </table>
    </details>`).join('');
}

function renderExtraDasas() {
  const chart = currentChart;
  if (!chart) return;
  const yearNote = chart.dasa_year ? txt(` Dasa year: ${chart.dasa_year.en}.`, ` தசை ஆண்டு: ${chart.dasa_year.ta}.`) : '';
  const note = $('#ashtottari-note');
  if (note) {
    note.textContent = (chart.ashtottari_applicable
      ? txt('Applies to this chart: Rahu is in a kendra or trikona from the Lagna lord, not in the Lagna.',
        'இந்த ஜாதகத்திற்குப் பொருந்தும்: ராகு லக்னாதிபதிக்குக் கேந்திர / திரிகோணத்தில், லக்னத்தில் இல்லை.')
      : txt('Classically used when Rahu is in a kendra or trikona from the Lagna lord; that does not hold here, so read it alongside Vimshottari.',
        'ராகு லக்னாதிபதிக்குக் கேந்திர / திரிகோணத்தில் இருக்கும்போது பாரம்பரியமாகப் பயன்படும்; இங்கு அது இல்லை, எனவே விம்சோத்தரியுடன் சேர்த்துப் பார்க்கவும்.')) + yearNote;
  }
  renderPeriodAccordion($('#ashtottari-accordion'), chart.ashtottari_dasha, d => grahaName(d.lord), b => grahaName(b.lord),
    txt('Bhukti', 'புக்தி'));
  renderPeriodAccordion($('#chara-accordion'), chart.chara_dasha,
    d => txt(`${d.sign} (lord ${d.lord})${d.round === 2 ? ', 2nd round' : ''}`,
      `${d.sign_ta} (அதிபதி ${grahaName(d.lord)})${d.round === 2 ? ', 2-ஆம் சுற்று' : ''}`),
    b => txt(b.sign, b.sign_ta), txt('Antardasa', 'அந்தர தசை'));
}

function renderUpagrahas() {
  const tbody = $('#upagrahas-tbody');
  const rows = currentChart?.south_indian?.upagrahas;
  if (!tbody || !rows) return;
  tbody.innerHTML = rows.map(u => `
    <tr>
      <td><strong>${esc(txt(u.name, u.name_ta))}</strong></td>
      <td>${esc(signName(u.sign_index))}</td>
      <td>${formatDegrees(u.degree)}</td>
      <td>${esc(starName(u.nakshatra))} (${txt('Pada', 'பாதம்')} ${u.pada})</td>
      <td>${txt(`House ${u.house}`, `${u.house}-ம் பாவம்`)}</td>
    </tr>`).join('');
}

// Dasa View Switcher & Timeline Predictions Engine
function setDasaViewMode(mode) {
  currentDasaMode = mode;
  $('#btn-mode-timeline')?.classList.toggle('active', mode === 'timeline');
  $('#btn-mode-cycles')?.classList.toggle('active', mode === 'cycles');
  $('#btn-mode-yogini')?.classList.toggle('active', mode === 'yogini');
  ['ashtottari', 'chara'].forEach(m => {
    $(`#btn-mode-${m}`)?.classList.toggle('active', mode === m);
    const view = $(`#dasa-${m}-view`);
    if (view) view.hidden = (mode !== m);
  });
  const tView = $('#dasa-timeline-view');
  const cView = $('#dasa-tabular-view');
  const yView = $('#dasa-yogini-view');
  if (tView) tView.hidden = (mode !== 'timeline');
  if (cView) cView.hidden = (mode !== 'cycles');
  if (yView) yView.hidden = (mode !== 'yogini');
}

function handleTimelineYearJump() {
  const yrVal = parseInt($('#timeline-jump-year')?.value, 10);
  if (!yrVal || isNaN(yrVal)) {
    timelineSearchYear = null;
  } else {
    timelineSearchYear = yrVal;
    currentTimelineFilter = 'all';
    $$('.timeline-filter-btn').forEach(b => b.classList.toggle('active', b.dataset.tfilter === 'all'));
  }
  renderDasaTimelineView();
}

function renderDasaTimelineView() {
  if (!currentChart || !currentChart.predictions) return;
  const tp = currentChart.predictions.timeline_predictions;
  if (!tp) return;
  const isTa = currentLang === 'ta';

  // 1. Active Period Spotlight Card
  const sp = tp.active_spotlight;
  const spotCard = $('#timeline-spotlight-card');
  if (sp && spotCard) {
    const dLordName = isTa ? (sp.dasa_lord_ta || sp.dasa_lord) : sp.dasa_lord;
    const bLordName = isTa ? (sp.bhukti_lord_ta || sp.bhukti_lord) : sp.bhukti_lord;

    $('#spotlight-lords-title').textContent = isTa
      ? `${dLordName} மகா தசை — ${bLordName} புக்தி`
      : `${dLordName} Maha Dasa — ${bLordName} Bhukti`;

    $('#spotlight-period-theme').textContent = isTa ? (sp.title_ta || sp.strategic_advice_ta) : (sp.title_en || sp.strategic_advice_en);
    $('#spotlight-dates').textContent = `${sp.start_date} → ${sp.end_date}`;
    $('#spotlight-age').textContent = `${sp.age} ${isTa ? 'வயது' : 'Years'}`;
    $('#spotlight-elapsed').textContent = `${sp.elapsed_days} ${isTa ? 'நாட்கள்' : 'Days'}`;
    $('#spotlight-remaining').textContent = `${sp.remaining_days} ${isTa ? 'நாட்கள்' : 'Days'}`;

    const starIcons = '★'.repeat(sp.potency) + '☆'.repeat(Math.max(0, 5 - sp.potency));
    const potencyBadge = $('#spotlight-potency-badge');
    if (potencyBadge) {
      potencyBadge.textContent = `${starIcons} ${sp.potency >= 4 ? (isTa ? 'அதி உத்தமம்' : 'High Potency') : (sp.potency >= 3 ? (isTa ? 'மத்திமம்' : 'Moderate') : (isTa ? 'கவனம் தேவை' : 'Caution Required'))}`;
    }

    const progBar = $('#spotlight-progress-bar');
    if (progBar) progBar.style.width = `${sp.percent}%`;
    const progText = $('#spotlight-progress-text');
    if (progText) {
      progText.textContent = isTa
        ? `${sp.percent}% காலம் முடிவடைந்தது (${sp.elapsed_days} நாட்கள் நிறைவு · ${sp.remaining_days} நாட்கள் மீதம்)`
        : `${sp.percent}% Elapsed (${sp.elapsed_days} days passed · ${sp.remaining_days} days remaining)`;
    }

    $('#spotlight-advice-text').textContent = isTa ? sp.strategic_advice_ta : sp.strategic_advice_en;
    $('#spotlight-remedy-text').textContent = isTa ? sp.primary_remedy_ta : sp.primary_remedy_en;
  }

  // 2. 10-Year Annual Projections Grid
  const annualGrid = $('#annual-projections-grid');
  const annualSec = $('#annual-milestones-section');
  if (annualGrid && tp.annual_projections) {
    annualGrid.replaceChildren();
    tp.annual_projections.forEach(ap => {
      const aCard = document.createElement('div');
      aCard.className = `annual-card ${ap.is_current_year ? 'current-year' : ''}`;

      const dStr = isTa ? (ap.dasa_lord_ta || ap.dasa_lord) : ap.dasa_lord;
      const bStr = isTa ? (ap.bhukti_lord_ta || ap.bhukti_lord) : ap.bhukti_lord;
      const theme = isTa ? ap.theme_ta : ap.theme_en;

      aCard.innerHTML = `
        <div class="annual-card-top">
          <span class="annual-year-badge">${ap.icon} ${ap.year}</span>
          <span class="annual-age-pill">${isTa ? 'வயது' : 'Age'} ${ap.age}</span>
        </div>
        <div class="annual-lords">${esc(dStr)} / ${esc(bStr)}</div>
        <p class="annual-theme-text">${esc(theme)}</p>
        <div class="annual-score-wrap">
          <span>${isTa ? 'சுப பலம்' : 'Astro Score'}: ${ap.score}/100</span>
          <div class="annual-score-bar-track">
            <div class="annual-score-bar-fill" style="width: ${ap.score}%"></div>
          </div>
        </div>
      `;
      annualGrid.append(aCard);
    });
  }

  if (annualSec) {
    annualSec.hidden = (currentTimelineFilter !== 'annual' && currentTimelineFilter !== 'all');
  }

  // 3. Chronological Periods Stream Filtered
  renderTimelineStream(tp.periods, isTa);
}

function renderTimelineStream(periods, isTa) {
  const container = $('#timeline-periods-stream');
  if (!container) return;
  container.replaceChildren();

  if (!periods || !periods.length) {
    container.innerHTML = `<p class="muted">${isTa ? 'காலவரிசை விவரங்கள் கிடைக்கவில்லை.' : 'No timeline periods available.'}</p>`;
    return;
  }

  const nowYear = new Date().getFullYear();

  const filtered = periods.filter(p => {
    // Planet filter
    if (currentTimelinePlanet !== 'all') {
      if (p.dasa_lord.toLowerCase() !== currentTimelinePlanet.toLowerCase()) {
        return false;
      }
    }

    // Specific Year Search filter
    if (timelineSearchYear !== null) {
      try {
        const sYr = parseInt(p.start_date.slice(0, 4), 10);
        const eYr = parseInt(p.end_date.slice(0, 4), 10);
        if (timelineSearchYear < sYr || timelineSearchYear > eYr) {
          return false;
        }
      } catch (e) {
        return false;
      }
    }

    // Category button filter
    if (currentTimelineFilter === 'active') {
      return p.is_active;
    } else if (currentTimelineFilter === 'next5') {
      try {
        const sYr = parseInt(p.start_date.slice(0, 4), 10);
        const eYr = parseInt(p.end_date.slice(0, 4), 10);
        return p.is_active || (p.is_future && sYr <= nowYear + 5);
      } catch (e) {
        return p.is_active;
      }
    } else if (currentTimelineFilter === 'annual') {
      return false; // Annual view displays the annual grid prominently
    } else if (currentTimelineFilter === 'auspicious') {
      return p.potency >= 3;
    } else if (currentTimelineFilter === 'caution') {
      return p.potency <= 2;
    }

    return true; // 'all'
  });

  const countBadge = $('#timeline-count-badge');
  if (countBadge) {
    countBadge.textContent = isTa
      ? `${filtered.length} / ${periods.length} காலங்கள்`
      : `Showing ${filtered.length} of ${periods.length} Periods`;
  }

  if (filtered.length === 0) {
    container.innerHTML = `<div class="cosmic-card" style="text-align:center;padding:30px;"><p class="muted">${isTa ? 'தேர்ந்தெடுக்கப்பட்ட வடிகட்டியில் காலங்கள் எதுவும் அமையவில்லை.' : 'No periods matched the selected filter criteria.'}</p></div>`;
    return;
  }

  filtered.forEach(p => {
    const card = document.createElement('div');
    card.className = `timeline-card ${p.is_active ? 'active-period' : (p.is_past ? 'past-period' : '')}`;

    const dLordStr = isTa ? (p.dasa_lord_ta || p.dasa_lord) : p.dasa_lord;
    const bLordStr = isTa ? (p.bhukti_lord_ta || p.bhukti_lord) : p.bhukti_lord;
    const titleStr = isTa ? (p.title_ta || p.theme_ta) : (p.title_en || p.theme_en);
    const themeStr = isTa ? p.theme_ta : p.theme_en;

    let statusLabel = '';
    if (p.is_active) {
      statusLabel = `<span class="status-pill success">${isTa ? '🔴 நடைமுறையில் உள்ள காலம்' : '🔴 LIVE ACTIVE'}</span>`;
    } else if (p.is_future) {
      statusLabel = `<span class="status-pill info">${isTa ? 'எதிர்காலம்' : 'UPCOMING'}</span>`;
    } else {
      statusLabel = `<span class="status-pill neutral">${isTa ? 'முடிந்த காலம்' : 'PAST'}</span>`;
    }

    const starIcons = '★'.repeat(p.potency) + '☆'.repeat(Math.max(0, 5 - p.potency));

    card.innerHTML = `
      <div class="timeline-card-header">
        <div class="timeline-title-wrap">
          <h3>
            <span>${esc(dLordStr)} — ${esc(bLordStr)}</span>
            ${statusLabel}
          </h3>
          <div class="timeline-timing-pill">
            📅 ${p.start_date} → ${p.end_date} · <strong>${isTa ? 'வயது' : 'Age'} ${p.age_start} – ${p.age_end}</strong> (${p.duration_months} ${isTa ? 'மாதங்கள்' : 'months'})
          </div>
        </div>
      </div>

      <div class="timeline-badges-row">
        <span class="mutual-badge ${p.mutual_class}">${esc(isTa ? (p.mutual_rel_ta || p.mutual_rel) : p.mutual_rel)}</span>
        <span class="potency-pill">${starIcons} (${isTa ? (p.potency >= 4 ? 'உத்தமம்' : (p.potency >= 3 ? 'மத்திமம்' : 'எச்சரிக்கை')) : (p.potency >= 4 ? 'Favorable' : (p.potency >= 3 ? 'Moderate' : 'Caution'))})</span>
      </div>

      <div class="timeline-theme-narrative">
        <strong>${esc(titleStr)}:</strong> ${esc(themeStr)}
      </div>

      <button type="button" class="timeline-details-toggle ${p.is_active ? 'expanded' : ''}" aria-expanded="${p.is_active ? 'true' : 'false'}">
        <span class="toggle-icon">${p.is_active ? '▼' : '▶'}</span>
        <span class="toggle-label">${isTa
          ? (p.is_active ? 'விரிவான பலாபலன்கள் (திறக்கப்பட்டுள்ளது - மூட கிளிக் செய்யவும்)' : 'விரிவான பலாபலன்கள் (தொழில், தனம், நலம், குடும்பம், பரிகாரம்)')
          : (p.is_active ? 'Detailed Breakdown (Expanded - Click to Collapse)' : 'Detailed Breakdown (Career, Wealth, Health, Family, Remedies)')}</span>
      </button>

      <div class="timeline-details-panel" ${p.is_active ? '' : 'hidden'} style="display: ${p.is_active ? 'grid' : 'none'};">
        ${timelineDetailHtml(p)}
      </div>
    `;

    const toggleBtn = card.querySelector('.timeline-details-toggle');
    const panel = card.querySelector('.timeline-details-panel');
    if (toggleBtn && panel) {
      toggleBtn.addEventListener('click', (e) => {
        e.preventDefault();
        const willOpen = panel.hidden || panel.style.display === 'none' || panel.hasAttribute('hidden');
        if (willOpen && p.details_deferred) {
          loadTimelineDetails().then(() => { panel.innerHTML = timelineDetailHtml(p); });
        }
        if (willOpen) {
          panel.hidden = false;
          panel.removeAttribute('hidden');
          panel.style.display = 'grid';
          toggleBtn.classList.add('expanded');
          toggleBtn.setAttribute('aria-expanded', 'true');
          toggleBtn.querySelector('.toggle-icon').textContent = '▼';
          toggleBtn.querySelector('.toggle-label').textContent = isTa
            ? 'விரிவான பலாபலன்கள் (திறக்கப்பட்டுள்ளது - மூட கிளிக் செய்யவும்)'
            : 'Detailed Breakdown (Expanded - Click to Collapse)';
        } else {
          panel.hidden = true;
          panel.setAttribute('hidden', '');
          panel.style.display = 'none';
          toggleBtn.classList.remove('expanded');
          toggleBtn.setAttribute('aria-expanded', 'false');
          toggleBtn.querySelector('.toggle-icon').textContent = '▶';
          toggleBtn.querySelector('.toggle-label').textContent = isTa
            ? 'விரிவான பலாபலன்கள் (தொழில், தனம், நலம், குடும்பம், பரிகாரம்)'
            : 'Detailed Breakdown (Career, Wealth, Health, Family, Remedies)';
        }
      });
    }

    container.append(card);
  });
}

// The six reading cards of a timeline period; a placeholder while its texts are still loading
function timelineDetailHtml(p) {
  if (p.details_deferred) {
    return `<p class="muted">${txt('Loading the detailed reading…', 'விரிவான பலன் ஏற்றப்படுகிறது…')}</p>`;
  }
  const isTa = currentLang === 'ta';
  const dims = [
    ['💼', 'Career & Profession', 'தொழில் & உத்தியோகம்', 'career'],
    ['💰', 'Wealth & Assets', 'தனம் & முதலீடு', 'wealth'],
    ['🌿', 'Health & Vitality', 'உடல்நலம் & உணவு', 'health'],
    ['🏡', 'Family & Relationships', 'குடும்பம் & இல்லறம்', 'family'],
    ['🎯', 'Key Milestones', 'முக்கிய மைல்கல்', 'milestones'],
    ['🕉️', 'Remedy & Mantra', 'வேத பரிகாரம் & வழிபாடு', 'remedy']
  ];
  return dims.map(([icon, en, ta, key]) => `
        <div class="timeline-dim-card">
          <h4>${icon} ${isTa ? ta : en}</h4>
          <p>${esc(isTa ? p[`${key}_ta`] : p[`${key}_en`])}</p>
        </div>`).join('');
}

// The chart response carries the reading texts only for the running period; the rest are
// fetched once, when a card is first opened, and merged into the chart
function loadTimelineDetails() {
  if (!timelineDetailsLoad) {
    const chart = currentChart;
    timelineDetailsLoad = fetch('/api/timeline', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(currentChartPayload)
    }).then(resp => resp.json().then(data => {
      if (!resp.ok) throw new Error(data.error || 'Timeline details failed.');
      (chart.predictions.timeline_predictions.periods || []).forEach(p => {
        const details = data.details[p.id];
        if (details) {
          Object.assign(p, details);
          delete p.details_deferred;
        }
      });
    })).catch(err => {
      timelineDetailsLoad = null;
      notify(errorText(err.message));
    });
  }
  return timelineDetailsLoad;
}
