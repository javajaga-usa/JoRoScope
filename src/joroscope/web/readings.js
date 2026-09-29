/**
 * JoRoScope: The Life Predictions page: every reading chapter of the report.
 * A classic script sharing the page's global scope with app.js; see index.html for the order.
 */

// Life Predictions Multi-Chapter Comprehensive Renderer
// Verdict pill for a house or planet reading: strong / moderate / weak
function strengthPill(item) {
  if (!item.strength) return '';
  const cls = { strong: 'success', moderate: 'neutral', weak: 'danger' }[item.strength];
  const en = { strong: 'Strong', moderate: 'Moderate', weak: 'Needs care' }[item.strength];
  return `<span class="status-pill ${cls}">${txt(en, item.strength_ta)}</span>`;
}

function renderLifeReadings() {
  if (!currentChart) return;
  const pred = currentChart.predictions;
  if (!pred) return;
  const isTa = currentLang === 'ta';

  // Chapter 1: Natal Elements & Personality
  const ov = pred.overview;
  if (ov) {
    // Star
    $('#pred-star-title').textContent = txt(`Birth Star: ${ov.nakshatra} (${ov.tamil_nakshatra})`,
      `ஜென்ம நட்சத்திரம்: ${ov.tamil_nakshatra} (${ov.nakshatra})`, `ജന്മനക്ഷത്രം: ${mlTerm(ov.nakshatra)}`);
    $('#pred-star-sub').textContent = txt('Core Character, Temperament & Destiny',
      'குணம், மனோபாவம் மற்றும் விதியின் தாக்கம்', 'സ്വഭാവം, മനോഭാവം, വിധി');
    $('#pred-star-text').textContent = isTa ? ov.nakshatra_pred_ta : ov.nakshatra_pred_en;

    // Lagna
    $('#pred-lagna-title').textContent = txt(`Ascendant (Lagna): ${ov.lagna} (${ov.tamil_lagna})`,
      `லக்னம் (உதய ராசி): ${ov.tamil_lagna} (${ov.lagna})`, `ലഗ്നം (ഉദയ രാശി): ${mlTerm(ov.lagna)}`);
    $('#pred-lagna-sub').textContent = txt('Body Constitution, Leadership & Life Path',
      'உடல்வாகு, தலைமைப் பண்பு மற்றும் வாழ்க்கை திசை', 'ശരീരപ്രകൃതി, നേതൃഗുണം, ജീവിതദിശ');
    $('#pred-lagna-text').textContent = isTa ? ov.lagna_pred_ta : ov.lagna_pred_en;

    // Moon Sign
    $('#pred-moon-title').textContent = txt(`Moon Sign (Rasi): ${ov.moon_sign} (${ov.tamil_moon_sign})`,
      `சந்திர ராசி: ${ov.tamil_moon_sign} (${ov.moon_sign})`, `ചന്ദ്രരാശി: ${mlTerm(ov.moon_sign)}`);
    $('#pred-moon-sub').textContent = txt('Emotional Landscape, Instincts & Mental Equanimity',
      'உள்மன உணர்வுகள், சிந்தனை ஓட்டம் மற்றும் கற்பனை வளம்', 'ഉള്ളിലെ വികാരങ്ങൾ, ചിന്താഗതി, മനസ്സമാധാനം');
    $('#pred-moon-text').textContent = currentLang === 'ml'
      ? `മനഃകാരകനായ ചന്ദ്രൻ ${mlTerm(ov.moon_sign)} രാശിയിൽ നിന്ന് നിങ്ങളുടെ ഉപബോധ സ്വഭാവം, സഹാനുഭൂതി, ഉൾക്കാഴ്ചയോടെയുള്ള പ്രതികരണങ്ങൾ എന്നിവയെ നയിക്കുന്നു. വൈകാരികമായ ഇണക്കം, ഭാവനയുടെ തെളിച്ചം, അമ്മയുടെ അനുഗ്രഹം, ഗൃഹൈശ്വര്യം എന്നിവ സ്വാഭാവികമായി ലഭിക്കും.`
      : isTa
      ? `சந்திர பகவான் உங்கள் மனோகாரகனாக ${ov.tamil_moon_sign} ராசியில் அமைந்து, சிந்தனைத் தெளிவையும் உணர்ச்சிப் பெருக்கையும் நிர்வகிக்கிறார். கற்பனை வளம், தாய்வழி ஆசிகள், சூழலுக்கு ஏற்ப பொருந்தும் நெகிழ்வுத்தன்மை இயல்பாகவே அமையும்.`
      : `The Moon placed in ${ov.moon_sign} governs your subconscious temperament, empathy, and intuitive reactions. It provides emotional adaptability, imaginative clarity, maternal grace, and domestic prosperity.`;

    // Sudarshana Chakra: houses from Lagna, Moon and Sun, with this year's activated house
    const sd = pred.sudarshana;
    if (sd) {
      $('#sudarshana-reading').textContent = txt(sd.reading_en, sd.reading_ta);
      const cell = c => `${esc(txt(c.sign, c.sign_ta))}${c.planets.length ? ` <small style="color:var(--gold)">${grahaNames(c.planets, ', ')}</small>` : ''}`;
      $('#sudarshana-tbody').innerHTML = sd.rows.map(r => `
        <tr${r.house === sd.active_house ? ' style="background:var(--gold-glow, rgba(212,175,55,0.12))"' : ''}>
          <td><strong>${r.house}</strong></td><td>${cell(r.lagna)}</td><td>${cell(r.moon)}</td><td>${cell(r.sun)}</td>
        </tr>`).join('');
    }

    // Panchanga Phala: birth weekday, tithi, nitya yoga and karana
    $('#pred-sun-title').textContent = txt('Panchanga Phala', 'பஞ்சாங்க பலன்');
    $('#pred-sun-sub').textContent = txt('Weekday, Tithi, Yoga & Karana at Birth', 'பிறந்த கிழமை, திதி, யோகம் & கரணம்');
    $('#pred-sun-text').innerHTML = (pred.panchanga_phala || []).map(item => `
      <p style="margin:0 0 8px"><strong style="color:var(--gold)">${esc(txt(item.title_en, item.title_ta))}:</strong> ${esc(txt(item.reading_en, item.reading_ta))}</p>`).join('');
  }

  // Chapter 2: 12 Bhavas Comprehensive Life Path
  const bhavasContainer = $('#bhavas-cards-container');
  bhavasContainer.replaceChildren();
  if (pred.bhavas && pred.bhavas.length) {
    pred.bhavas.forEach(b => {
      const card = document.createElement('div');
      card.className = 'bhava-card';
      const isSavStrong = b.sav_points >= 28;
      const occStr = b.occupants && b.occupants.length ? grahaNames(b.occupants) : (isTa ? 'கிரகங்கள் இல்லை' : 'None');
      const aspStr = b.aspected_by && b.aspected_by.length ? grahaNames(b.aspected_by) : (isTa ? 'நேரடி பார்வைகள் இல்லை' : 'None');
      const title = isTa ? b.title_ta : b.title_en;
      const narrative = isTa ? b.prediction_ta : b.prediction_en;

      card.innerHTML = `
        <div class="bhava-header">
          <div class="bhava-title-group">
            <span class="bhava-num-badge">${b.house}</span>
            <div>
              <h3>${esc(title)}</h3>
              <small class="muted">${isTa ? b.tamil_sign : b.sign} · ${isTa ? 'அதிபதி' : 'Lord'}: ${grahaName(b.lord)} (${isTa ? `${b.lord_house}-ம் பாவம்` : `H${b.lord_house}`})</small>
            </div>
          </div>
          <span class="bhava-meta-pill ${isSavStrong ? 'highlight' : ''}">${b.sav_points} ${txt('SAV Bindus', 'சர்வாஷ்டக பரல்கள்')}</span>
        </div>
        <div class="bhava-meta-strip">
          ${strengthPill(b)}
          <span class="bhava-meta-pill">${isTa ? 'அதிபதி நிலை' : 'Lord Dignity'}: <strong>${dignityLabel(b.lord_dignity)}</strong></span>
          ${b.bhava_bala_rupas != null ? `<span class="bhava-meta-pill">${txt('Bhava Bala', 'பாவ பலம்')}: <strong>${b.bhava_bala_rupas} ${txt('rupas', 'ரூபம்')}</strong></span>` : ''}
          <span class="bhava-meta-pill">${isTa ? 'அமர்ந்த கிரகங்கள்' : 'Occupants'}: <strong>${esc(occStr)}</strong></span>
          <span class="bhava-meta-pill">${isTa ? 'பார்வை கிரகங்கள்' : 'Aspects'}: <strong>${esc(aspStr)}</strong></span>
        </div>
        <p class="reading-body">${esc(narrative)}</p>
        ${(b.factors || []).length ? `<ul class="bhava-factors">${b.factors.map(f => `
          <li class="${f.effect > 0 ? 'plus' : (f.effect < 0 ? 'minus' : 'neutral')}">${esc(txt(f.en, f.ta))}</li>`).join('')}
        </ul>` : ''}
      `;
      bhavasContainer.append(card);
    });
  }

  // Chapter 3: Planets in Houses
  const planetsContainer = $('#planets-cards-container');
  planetsContainer.replaceChildren();
  if (pred.planets_in_houses && pred.planets_in_houses.length) {
    pred.planets_in_houses.forEach(p => {
      const card = document.createElement('div');
      card.className = 'planet-pred-card';
      const pInfo = PLANET_NAMES[p.planet] || { en: p.planet, ta: p.planet, color: '#e5c378' };
      const pLabel = isTa ? pInfo.ta : pInfo.en;
      const narrative = isTa ? p.prediction_ta : p.prediction_en;
      const dignityClass = (p.dignity || '').toLowerCase().replace(/\s+/g, '-');

      card.innerHTML = `
        <div class="planet-pred-header">
          <div class="planet-title-group">
            <span class="bhava-num-badge" style="border-color:${pInfo.color}; color:${pInfo.color}">${pInfo.short || p.planet.slice(0, 2)}</span>
            <div>
              <h3>${esc(pLabel)}</h3>
              <small class="muted">${isTa ? 'பாவம்' : 'House'} ${p.house} · ${isTa ? p.tamil_sign : p.sign}</small>
            </div>
          </div>
          <span class="dignity-badge ${dignityClass}">${dignityLabel(p.dignity)}</span>
        </div>
        <div class="planet-meta-strip">
          ${strengthPill(p)}
          ${p.retrograde ? `<span class="legend-badge retro">${isTa ? 'வக்ரம் (Rx)' : 'Retrograde (Rx)'}</span>` : ''}
          ${p.combust ? `<span class="legend-badge combust">${isTa ? '🔥 அஸ்தமனம்' : '🔥 Combust'}</span>` : ''}
          <span class="bhava-meta-pill">${isTa ? 'ராசி' : 'Rasi'}: <strong>${isTa ? p.tamil_sign : p.sign}</strong></span>
        </div>
        <p class="reading-body">${esc(narrative)}</p>
      `;
      planetsContainer.append(card);
    });
  }

  // Chapter 4: Dasa-Bhukti Life Phases
  const dasaForecast = pred.dasa_forecast;
  if (dasaForecast) {
    if (dasaForecast.active_period) {
      const ad = dasaForecast.active_period;
      $('#pred-dasa-active-title').textContent = isTa
        ? `தற்போதைய இயங்கும் தசா-புக்தி: ${grahaName(ad.dasa)} தசை — ${grahaName(ad.bhukti)} புக்தி`
        : `Active Running Period: ${ad.dasa} Maha Dasa — ${ad.bhukti} Bhukti`;
      $('#pred-dasa-active-desc').textContent = isTa ? dasaForecast.active_forecast_ta : dasaForecast.active_forecast_en;
    }

    const dasasList = $('#maha-dasas-list');
    dasasList.replaceChildren();
    if (dasaForecast.all_dasas) {
      const activeLord = dasaForecast.active_period ? dasaForecast.active_period.dasa : '';
      Object.entries(dasaForecast.all_dasas).forEach(([pLord, texts]) => {
        const dCard = document.createElement('div');
        const isActive = pLord.toLowerCase() === activeLord.toLowerCase();
        dCard.className = `maha-dasa-card ${isActive ? 'active-period' : ''}`;
        const pInfo = PLANET_NAMES[pLord] || { en: pLord, ta: pLord };
        const label = isTa ? pInfo.ta : pInfo.en;
        const text = isTa ? texts.ta : texts.en;

        dCard.innerHTML = `
          <h4>
            <span>${esc(label)} ${isTa ? 'மகா தசை' : 'Maha Dasa'}</span>
            ${isActive ? `<span class="status-pill success">${isTa ? 'நடைமுறையில் உள்ளது' : 'ACTIVE'}</span>` : ''}
          </h4>
          <p class="reading-body" style="font-size:12px">${esc(text)}</p>
        `;
        dasasList.append(dCard);
      });
    }
  }

  // Chapter 5: Transits (Gochara)
  const transits = pred.transits;
  if (transits) {
    const s = transits.saturn;
    if (s) {
      $('#saturn-transit-title').textContent = isTa ? s.title_ta : s.title_en;
      $('#saturn-transit-badge').textContent = isTa
        ? `சந்திரனிலிருந்து ${s.house_from_moon}-ஆம் இடம்`
        : `House ${s.house_from_moon} from Moon`;
      $('#saturn-transit-badge').className = `status-pill ${[12, 1, 2, 8].includes(s.house_from_moon) ? 'danger' : 'success'}`;
      $('#saturn-transit-desc').textContent = isTa ? s.prediction_ta : s.prediction_en;
    }

    const j = transits.jupiter;
    if (j) {
      $('#jupiter-transit-title').textContent = isTa
        ? 'குருப் பெயர்ச்சி பலன்'
        : 'Jupiter Transit (Guru Peyarchi)';
      $('#jupiter-transit-badge').textContent = j.favorable
        ? (isTa ? 'சுப பலன்' : 'Auspicious')
        : (isTa ? 'மத்திம பலன்' : 'Moderate');
      $('#jupiter-transit-badge').className = `status-pill ${j.favorable ? 'success' : 'neutral'}`;
      $('#jupiter-transit-desc').textContent = isTa ? j.prediction_ta : j.prediction_en;
    }

    const rk = transits.rahu_ketu;
    if (rk) {
      $('#rahuketu-transit-title').textContent = isTa ? 'ராகு-கேது பெயர்ச்சி பலன்' : 'Rahu-Ketu Transit';
      $('#rahuketu-transit-badge').textContent = rk.favorable
        ? (isTa ? 'சுப பலன்' : 'Favourable')
        : (isTa ? 'கவனம் தேவை' : 'Caution');
      $('#rahuketu-transit-badge').className = `status-pill ${rk.favorable ? 'success' : 'neutral'}`;
      $('#rahuketu-transit-desc').textContent = isTa ? rk.prediction_ta : rk.prediction_en;
    }
  }
  renderGochara();

  // Chapter 6: Lucky Gemstones & Remedies
  const luck = pred.lucky_factors;
  if (luck) {
    $('#gem-primary').textContent = txt(luck.primary_gem, luck.primary_gem_ta) || '—';
    $('#gem-fortune').textContent = txt(luck.fortune_gem, luck.fortune_gem_ta) || '—';
    $('#gem-metal').textContent = txt(luck.metal, luck.metal_ta) || '—';
    $('#gem-finger').textContent = txt(luck.finger, luck.finger_ta) || '—';
    $('#gem-day').textContent = txt(luck.wearing_day, luck.wearing_day_ta) || '—';
    $('#gem-basis').textContent = txt(luck.gem_basis_en, luck.gem_basis_ta) || '';

    $('#luck-numbers').textContent = luck.lucky_numbers ? luck.lucky_numbers.join(', ') : '—';
    $('#luck-days').textContent = (txt(luck.lucky_days, luck.lucky_days_ta) || []).join(', ') || '—';
    $('#luck-colors').textContent = (txt(luck.lucky_colors, luck.lucky_colors_ta) || []).join(', ') || '—';
    $('#luck-deities').textContent = isTa ? luck.deity_worship_ta : luck.deity_worship_en;
  }

  // Chapter 7: Jaimini Chara Karakas & Karakamsha
  const jk = pred.jaimini_karakas;
  if (jk) {
    if (jk.karakamsha) {
      $('#jaimini-karakamsha-title').textContent = txt(`Karakamsha Lagna: ${jk.karakamsha.sign} (${jk.karakamsha.tamil_sign})`,
        `காரகாம்சம்: ${jk.karakamsha.tamil_sign} (${jk.karakamsha.sign})`,
        `കാരകാംശ ലഗ്നം: ${mlTerm(jk.karakamsha.sign)}`);
      $('#jaimini-karakamsha-desc').textContent = isTa
        ? jk.karakamsha.interpretation_ta
        : jk.karakamsha.interpretation_en;
    }

    const aStrip = $('#jaimini-arudha-strip');
    if (aStrip && jk.arudhas) {
      aStrip.innerHTML = jk.arudhas.map(a => `<span class="bhava-meta-pill${[1, 12].includes(a.house) ? ' highlight' : ''}" title="${esc(txt(a.name_en, a.name_ta))}">${a.house === 1 ? 'AL' : (a.house === 12 ? 'UL' : a.code)}: <strong>${esc(txt(a.sign, a.sign_ta))}</strong></span>`).join('');
    }
    const aNotes = $('#jaimini-arudha-notes');
    if (aNotes) aNotes.innerHTML = (jk.arudha_notes || []).map(n => `<li class="neutral">${esc(txt(n.en, n.ta))}</li>`).join('');

    const jGrid = $('#jaimini-karakas-grid');
    jGrid.replaceChildren();
    if (jk.karakas) {
      jk.karakas.forEach(k => {
        const card = document.createElement('div');
        const isAk = k.code === 'AK';
        card.className = `karaka-card ${isAk ? 'ak-card' : ''}`;
        card.innerHTML = `
          <div class="karaka-card-header">
            <div>
              <span class="karaka-code-badge">${k.code}</span>
              <strong style="margin-left:8px; font-family:var(--font-serif); font-size:15px; color:var(--gold);">
                ${isTa ? k.title_ta : k.title_en}
              </strong>
            </div>
            <small class="muted">${k.degree_str}</small>
          </div>
          <div class="bhava-meta-strip">
            <span class="bhava-meta-pill">${isTa ? 'கிரகம்' : 'Planet'}: <strong>${isTa ? k.tamil_planet : k.planet}</strong></span>
            <span class="bhava-meta-pill">${isTa ? 'ராசி' : 'Sign'}: <strong>${isTa ? k.tamil_sign : k.sign}</strong></span>
            <span class="bhava-meta-pill">${isTa ? 'பாவம்' : 'House'}: <strong>${k.house}</strong></span>
            <span class="bhava-meta-pill">${isTa ? 'நிலை' : 'Dignity'}: <strong>${dignityLabel(k.dignity)}</strong></span>
          </div>
          <p class="reading-body" style="font-size:12.5px">${esc(isTa ? k.reading_ta : k.reading_en)}</p>
        `;
        jGrid.append(card);
      });
    }
  }

  // Chapter 8: Double Transit (Dwi-Gochara) Timing Engine
  const dt = pred.double_transit;
  if (dt) {
    if (dt.calculation_date_utc) {
      $('#timing-calc-date').textContent = `${txt('Live', 'நேரலை')}: ${dt.calculation_date_utc.slice(0, 10)}`;
    }
    if (dt.transit_saturn) {
      $('#timing-saturn-pos').textContent = `${isTa ? dt.transit_saturn.tamil_sign : dt.transit_saturn.sign} (${dt.transit_saturn.degree_str})`;
    }
    if (dt.transit_jupiter) {
      $('#timing-jupiter-pos').textContent = `${isTa ? dt.transit_jupiter.tamil_sign : dt.transit_jupiter.sign} (${dt.transit_jupiter.degree_str})`;
    }

    const tGrid = $('#timing-milestones-grid');
    tGrid.replaceChildren();
    if (dt.milestones) {
      dt.milestones.forEach(m => {
        const card = document.createElement('div');
        card.className = `timing-event-card ${m.is_active ? 'active-window' : ''}`;
        card.innerHTML = `
          <div class="timing-card-header">
            <div>
              <h3 style="font-family:var(--font-serif); font-size:16px; color:var(--gold); margin:0 0 4px;">
                ${esc(isTa ? m.title_ta : m.title_en)}
              </h3>
              <small class="muted">${isTa ? m.target_house_ta : m.target_house}</small>
            </div>
            <span class="status-pill ${m.is_active ? 'success' : 'neutral'}">
              ${esc(isTa ? m.status_ta : m.status_en)}
            </span>
          </div>
          <div class="timing-score-bar">
            <small class="muted">${isTa ? 'சாதக சதவீதம்' : 'Probability Score'}:</small>
            <div class="timing-track">
              <div class="timing-fill" style="width:${m.score}%"></div>
            </div>
            <strong style="color:var(--gold); font-size:12px">${m.score}%</strong>
          </div>
          <p class="reading-body" style="font-size:12.5px">${esc(isTa ? m.desc_ta : m.desc_en)}</p>
          ${(m.windows || []).length ? `<ul class="bhava-factors">${m.windows.map(w => `
            <li class="${w.dasa_support ? 'plus' : 'neutral'}">${w.start} – ${w.end} · ${esc(grahaName(w.dasa))}–${esc(grahaName(w.bhukti))} ${txt('dasa', 'தசை')}${w.dasa_support ? ` · ${txt('dasa supports', 'தசா ஆதரவு')}` : ''}</li>`).join('')}
          </ul>` : ''}
        `;
        tGrid.append(card);
      });
    }
  }

  // Chapter 9: D-10 Dasamsa Career & Vocation
  const c10 = pred.career_d10;
  if (c10) {
    if (c10.top_archetype) {
      $('#career-top-title').textContent = `${isTa ? 'முதன்மை யோகம்' : 'Prime Calling'}: ${isTa ? c10.top_archetype.title_ta : c10.top_archetype.title_en}`;
      $('#career-top-badge').textContent = `${c10.top_archetype.score}% ${isTa ? 'பொருத்தம்' : 'Aptitude Match'}`;
      $('#career-top-narrative').textContent = isTa ? c10.narrative_ta : c10.narrative_en;
    }
    const cStrip = $('#career-meta-strip');
    if (cStrip && c10.karmajeeva) {
      const kj = c10.karmajeeva;
      cStrip.innerHTML = `
        <span class="bhava-meta-pill highlight">${txt('Karmajeeva graha', 'கர்மஜீவ கிரகம்')}: <strong>${esc(grahaName(kj.planet))}</strong></span>
        <span class="bhava-meta-pill">${txt('Reckoned from', 'கணக்கிட்டது')}: <strong>${esc(txt(kj.reference, kj.reference_ta))}</strong></span>
        <span class="bhava-meta-pill">${txt('10th lord', '10-ஆம் அதிபதி')}: <strong>${esc(grahaName(c10.tenth_lord))}</strong></span>
        ${c10.d10 ? `<span class="bhava-meta-pill">${txt('D-10 Lagna', 'தசாம்ச லக்னம்')}: <strong>${esc(txt(c10.d10.lagna, c10.d10.lagna_ta))}</strong></span>` : ''}`;
    }

    const cContainer = $('#career-archetypes-container');
    cContainer.replaceChildren();
    if (c10.all_archetypes) {
      c10.all_archetypes.forEach((arch, idx) => {
        const card = document.createElement('div');
        const isTop = idx === 0;
        card.className = `career-arch-card ${isTop ? 'top-calling' : ''}`;
        card.innerHTML = `
          <div class="career-arch-header">
            <div>
              <strong style="font-size:15px; font-family:var(--font-serif); color:var(--gold);">
                ${esc(isTa ? arch.title_ta : arch.title_en)}
              </strong>
              <div style="font-size:11.5px; color:var(--text-muted); margin-top:2px">
                ${isTa ? arch.suitability_ta : arch.suitability}
              </div>
            </div>
            <span class="status-pill ${arch.score >= 80 ? 'success' : 'neutral'}">${arch.score}%</span>
          </div>
          <div class="career-progress-track">
            <div class="career-progress-fill" style="width:${arch.score}%"></div>
          </div>
          <div style="font-size:12px; color:var(--text-secondary); margin-top:4px">
            <strong>${isTa ? 'முக்கிய துறைகள்' : 'Industry Sectors'}:</strong> ${esc(isTa ? arch.key_sectors_ta : arch.key_sectors_en)}
          </div>
        `;
        cContainer.append(card);
      });
    }
  }

  // Chapter 10: Ayur-Jyotish & Tridosha Wellness
  const ayur = pred.ayur_jyotish;
  if (ayur) {
    $('#ayur-prakriti-title').textContent = isTa ? ayur.prakriti_ta : ayur.prakriti_en;
    $('#vata-pct').textContent = `${ayur.vata_percentage}%`;
    $('#vata-fill').style.width = `${ayur.vata_percentage}%`;

    $('#pitta-pct').textContent = `${ayur.pitta_percentage}%`;
    $('#pitta-fill').style.width = `${ayur.pitta_percentage}%`;

    $('#kapha-pct').textContent = `${ayur.kapha_percentage}%`;
    $('#kapha-fill').style.width = `${ayur.kapha_percentage}%`;

    $('#ayur-vulnerabilities-text').textContent = isTa ? ayur.anatomical_vulnerabilities_ta : ayur.anatomical_vulnerabilities_en;
    $('#ayur-lifestyle-text').textContent = isTa ? ayur.lifestyle_guidance_ta : ayur.lifestyle_guidance_en;
    const listInto = (el, items, cls) => {
      if (el) el.innerHTML = (items || []).map(f => `<li class="${cls}">${esc(txt(f.en, f.ta))}</li>`).join('');
    };
    listInto($('#ayur-factors'), ayur.factors, 'neutral');
    listInto($('#ayur-health-watch'), ayur.health_watch, 'minus');
  }

  // Chapter 11: Ashtakavarga Kakshya Precision Transits
  const kt = pred.kakshya_transits;
  if (kt) {
    if (kt.saturn) {
      const sat = kt.saturn;
      $('#kakshya-sat-badge').textContent = sat.current_degree;
      $('#kakshya-sat-badge').className = `status-pill ${sat.current_kakshya.has_bindu ? 'success' : 'danger'}`;
      $('#kakshya-sat-summary').textContent = isTa ? sat.summary_ta : sat.summary_en;

      const sBody = $('#kakshya-sat-tbody');
      sBody.replaceChildren();
      (sat.kakshya_timeline || []).forEach(row => {
        const tr = document.createElement('tr');
        if (row.is_current) tr.className = 'active-period';
        tr.innerHTML = `
          <td><strong>${row.kakshya_num}</strong> ${row.is_current ? `<span class="status-pill success" style="font-size:9px">${txt('Active', 'நடப்பில்')}</span>` : ''}</td>
          <td>${row.range_str}</td>
          <td><strong>${isTa ? row.lord_ta : row.lord}</strong></td>
          <td>${row.has_bindu ? `<span style="color:#2ecc71; font-weight:700">${txt('1 Bindu', '1 பரல்')}</span>` : `<span style="color:#e63946">${txt('0 Bindu', '0 பரல்')}</span>`}</td>
          <td><span class="dignity-badge ${row.has_bindu ? 'own-sign' : 'enemy'}">${isTa ? row.status_ta : row.status_en}</span></td>
        `;
        sBody.append(tr);
      });
    }

    if (kt.jupiter) {
      const jup = kt.jupiter;
      $('#kakshya-jup-badge').textContent = jup.current_degree;
      $('#kakshya-jup-badge').className = `status-pill ${jup.current_kakshya.has_bindu ? 'success' : 'neutral'}`;
      $('#kakshya-jup-summary').textContent = isTa ? jup.summary_ta : jup.summary_en;

      const jBody = $('#kakshya-jup-tbody');
      jBody.replaceChildren();
      (jup.kakshya_timeline || []).forEach(row => {
        const tr = document.createElement('tr');
        if (row.is_current) tr.className = 'active-period';
        tr.innerHTML = `
          <td><strong>${row.kakshya_num}</strong> ${row.is_current ? `<span class="status-pill success" style="font-size:9px">${txt('Active', 'நடப்பில்')}</span>` : ''}</td>
          <td>${row.range_str}</td>
          <td><strong>${isTa ? row.lord_ta : row.lord}</strong></td>
          <td>${row.has_bindu ? `<span style="color:#2ecc71; font-weight:700">${txt('1 Bindu', '1 பரல்')}</span>` : `<span style="color:#e63946">${txt('0 Bindu', '0 பரல்')}</span>`}</td>
          <td><span class="dignity-badge ${row.has_bindu ? 'exalted' : 'neutral'}">${isTa ? row.status_ta : row.status_en}</span></td>
        `;
        jBody.append(tr);
      });
    }
  }

  // Chapter 12: Shadbala Planetary Strengths & Potency
  const SHADBALA_PARTS = [
    ['uchcha', 'Uchcha', 'உச்ச'], ['saptavargaja', 'Saptavargaja', 'சப்தவர்க்கஜ'], ['ojayugma', 'Ojayugma', 'ஓஜயுக்ம'],
    ['kendra', 'Kendradi', 'கேந்திராதி'], ['drekkana', 'Drekkana', 'திரேக்காண'], ['nathonnatha', 'Nathonnatha', 'நதோன்னத'],
    ['paksha', 'Paksha', 'பக்ஷ'], ['tribhaga', 'Tribhaga', 'திரிபாக'], ['abda', 'Abda', 'அப்த'], ['masa', 'Masa', 'மாச'],
    ['vara', 'Vara', 'வார'], ['hora', 'Hora', 'ஹோரா'], ['ayana', 'Ayana', 'அயன'], ['yuddha', 'Yuddha', 'யுத்த'],
    ['cheshta', 'Cheshta', 'சேஷ்டா'], ['drik', 'Drik', 'திருக்']
  ];
  const sb = pred.shadbala;
  if (sb) {
    $('#shadbala-master-summary').textContent = isTa ? sb.summary_ta : sb.summary_en;
    if (sb.dominant_planet) {
      const dp = sb.dominant_planet;
      $('#shadbala-dom-planet').textContent = `${isTa ? dp.planet_ta : dp.planet} (${dp.strength_ratio}x)`;
      $('#shadbala-dom-sub').textContent = isTa ? dp.theme_ta : dp.theme_en;
    }
    if (sb.vulnerable_planet) {
      const vp = sb.vulnerable_planet;
      $('#shadbala-vuln-planet').textContent = `${isTa ? vp.planet_ta : vp.planet} (${vp.strength_ratio}x)`;
      $('#shadbala-vuln-sub').textContent = isTa ? vp.theme_ta : vp.theme_en;
    }

    const sbGrid = $('#shadbala-cards-grid');
    if (sbGrid && sb.planets) {
      sbGrid.replaceChildren();
      sb.planets.forEach(p => {
        const card = document.createElement('div');
        card.className = 'cosmic-card reading-card';
        const pInfo = PLANET_NAMES[p.planet] || { en: p.planet, ta: p.planet, color: '#e5c378' };
        const label = isTa ? p.planet_ta : p.planet;
        const reading = isTa ? p.reading_ta : p.reading_en;
        const statusBadge = p.is_adequate
          ? `<span class="status-pill success">${isTa ? 'சுப பலம் வாய்ந்தது' : 'Adequate'} (${p.strength_ratio}x)</span>`
          : `<span class="status-pill neutral">${isTa ? 'வளர்ச்சி தேவை' : 'Growth Area'} (${p.strength_ratio}x)</span>`;

        card.innerHTML = `
          <div class="reading-header">
            <span class="bhava-num-badge" style="border-color:${pInfo.color}; color:${pInfo.color}">#${p.rank}</span>
            <div>
              <h3>${esc(label)} — ${p.total_rupas} ${txt('Rupas', 'ரூபம்')} (${p.total_virupas} ${txt('Virupas', 'விரூபம்')})</h3>
              <small class="muted">${isTa ? 'தேவை' : 'Required'}: ${p.min_required_rupas} ${txt('Rupas', 'ரூபம்')} · ${txt(`Rank ${p.rank} of 7`, `7-ல் ${p.rank}-வது இடம்`)}</small>
            </div>
          </div>
          <div class="timing-score-bar" style="margin:8px 0;">
            <small class="muted">${isTa ? 'பலம் விகிதம்' : 'Strength Ratio'}:</small>
            <div class="timing-track" style="flex:1; margin:0 8px;">
              <div class="timing-fill" style="width:${Math.min(100, p.strength_ratio * 70)}%; background:${p.is_adequate ? 'var(--gold)' : '#e63946'}"></div>
            </div>
            ${statusBadge}
          </div>
          <div class="bhava-meta-strip" style="font-size:11px;">
            <span class="bhava-meta-pill">${txt('Sthana', 'ஸ்தான')}: <strong>${p.sthana_bala}</strong></span>
            <span class="bhava-meta-pill">${txt('Dig', 'திக்')}: <strong>${p.dig_bala}</strong></span>
            <span class="bhava-meta-pill">${txt('Kaala', 'கால')}: <strong>${p.kaala_bala}</strong></span>
            <span class="bhava-meta-pill">${txt('Chesta', 'சேஷ்டா')}: <strong>${p.chesta_bala}</strong></span>
            <span class="bhava-meta-pill">${txt('Naisargika', 'நைசர்கிக')}: <strong>${p.naisargika_bala}</strong></span>
            <span class="bhava-meta-pill">${txt('Drik', 'திருக்')}: <strong>${p.drik_bala}</strong></span>
          </div>
          <p class="reading-body" style="font-size:12.5px; margin-top:8px;">${esc(reading)}</p>
          ${(p.factors || []).length ? `<ul class="bhava-factors">${p.factors.map(f => `
            <li class="${f.effect > 0 ? 'plus' : 'minus'}">${esc(txt(f.en, f.ta))}</li>`).join('')}
          </ul>` : ''}
          <div class="bhava-meta-strip" style="font-size:11px; margin-top:8px;">
            <span class="bhava-meta-pill">${txt('Ishta Phala', 'இஷ்ட பலன்')}: <strong>${p.ishta_phala}</strong></span>
            <span class="bhava-meta-pill">${txt('Kashta Phala', 'கஷ்ட பலன்')}: <strong>${p.kashta_phala}</strong></span>
          </div>
          ${p.components ? `<details class="shadbala-breakdown">
            <summary>${txt('Component breakdown (virupas)', 'உட்கூறு பலங்கள் (விரூபம்)')}</summary>
            <div class="shadbala-components">${SHADBALA_PARTS.map(([key, en, ta]) => `
              <div><span>${esc(txt(en, ta))}</span><strong>${p.components[key]}</strong></div>`).join('')}
            </div>
          </details>` : ''}
        `;
        sbGrid.append(card);
      });
    }

    const bbBody = $('#bhava-bala-tbody');
    if (bbBody && sb.bhavas) {
      bbBody.replaceChildren();
      sb.bhavas.forEach(b => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><strong>${b.bhava}</strong></td>
          <td>${esc(grahaName(b.lord))}</td>
          <td>${b.adhipati}</td>
          <td>${b.dig}</td>
          <td>${b.drishti}</td>
          <td><strong style="color:${b.is_strong ? 'var(--gold)' : 'var(--ruby)'}">${b.rupas}</strong></td>
          <td>${b.rank}</td>
        `;
        bbBody.append(tr);
      });
    }

    const vBody = $('#vimsopaka-tbody');
    if (vBody && sb.vimsopaka) {
      vBody.replaceChildren();
      sb.vimsopaka.forEach(v => {
        const tr = document.createElement('tr');
        const cell = c => `<strong>${c.score}</strong> <small class="muted">${esc(txt(c.grade_en, c.grade_ta))}</small>${c.bheda_en ? `<br><small style="color:var(--gold)">${esc(txt(c.bheda_en, c.bheda_ta))}</small>` : ''}`;
        tr.innerHTML = `
          <td><strong>${esc(grahaName(v.planet))}</strong></td>
          <td>${cell(v.shadvarga)}</td>
          <td>${cell(v.saptavarga)}</td>
          <td>${cell(v.dasavarga)}</td>
          <td>${cell(v.shodasavarga)}</td>
        `;
        vBody.append(tr);
      });
    }
  }

  // Chapter 13: Krishnamurti Paddhati (KP System) Sub-Lord Analysis
  const kp = pred.kp_system;
  if (kp) {
    const rStrip = $('#kp-ruling-strip');
    if (rStrip) {
      rStrip.innerHTML = (kp.ayanamsa ? `<span class="bhava-meta-pill highlight">${txt('Ayanamsa', 'அயனாம்சம்')}: <strong>${txt('Krishnamurti', 'கிருஷ்ணமூர்த்தி')} ${kp.ayanamsa_degrees}°</strong></span>` : '')
        + (kp.ruling_planets || []).map(r => `<span class="bhava-meta-pill">${esc(txt(r.role_en, r.role_ta))}: <strong>${esc(grahaName(r.planet))}</strong></span>`).join('');
    }
    const kpGrid = $('#kp-cusp-preds-grid');
    if (kpGrid && kp.cuspal_predictions) {
      kpGrid.replaceChildren();
      Object.values(kp.cuspal_predictions).forEach(cp => {
        const card = document.createElement('div');
        card.className = 'cosmic-card reading-card';
        const title = isTa ? cp.title_ta : cp.title_en;
        const subLord = isTa ? cp.sub_lord_ta : cp.sub_lord;
        const reading = isTa ? cp.reading_ta : cp.reading_en;
        const verdictClass = { promised: 'success', mixed: 'neutral', weak: 'neutral', denied: 'danger', neutral: 'neutral' }[cp.verdict] || 'neutral';
        card.innerHTML = `
          <div class="reading-header">
            <span class="reading-icon">🔍</span>
            <div>
              <h3>${esc(title)}</h3>
              <small class="muted">${isTa ? 'உப-அதிபதி' : 'Sub-Lord'}: <strong style="color:var(--gold);">${esc(subLord)}</strong>${cp.star_lord ? ` · ${txt('Star lord', 'நட்சத்திர அதிபதி')}: ${esc(grahaName(cp.star_lord))}` : ''}</small>
            </div>
            ${cp.verdict ? `<span class="status-pill ${verdictClass}">${esc(txt(cp.verdict_en, cp.verdict_ta))}</span>` : ''}
          </div>
          <p class="reading-body" style="font-size:12.5px">${esc(reading)}</p>
        `;
        kpGrid.append(card);
      });
    }

    const cBody = $('#kp-cusps-tbody');
    if (cBody && kp.cusps) {
      cBody.replaceChildren();
      kp.cusps.forEach(c => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><strong>${c.cusp}</strong></td>
          <td>${c.degree_str}</td>
          <td>${isTa ? c.sign_ta : c.sign}</td>
          <td>${isTa ? c.sign_lord_ta : c.sign_lord}</td>
          <td>${starName(c.star_name)} (${isTa ? c.star_lord_ta : c.star_lord})</td>
          <td><strong style="color:var(--gold)">${isTa ? c.sub_lord_ta : c.sub_lord}</strong></td>
        `;
        cBody.append(tr);
      });
    }

    const pBody = $('#kp-planets-tbody');
    if (pBody && kp.planets) {
      pBody.replaceChildren();
      kp.planets.forEach(p => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><strong>${isTa ? p.planet_ta : p.planet}</strong></td>
          <td>${p.degree_str}</td>
          <td>${isTa ? p.sign_ta : p.sign}</td>
          <td>${isTa ? p.sign_lord_ta : p.sign_lord}</td>
          <td>${starName(p.star_name)} (${isTa ? p.star_lord_ta : p.star_lord})</td>
          <td><strong style="color:var(--gold)">${isTa ? p.sub_lord_ta : p.sub_lord}</strong></td>
          <td>${p.kp_house ?? '—'}</td>
          <td>${(p.significations || []).join(', ')}</td>
        `;
        pBody.append(tr);
      });
    }
  }

  // Chapter 14: Bhrigu Nandi Nadi (BNN) Karmic Sutras
  const bnn = pred.bhrigu_nandi_nadi;
  if (bnn) {
    $('#bnn-summary-text').textContent = isTa ? bnn.summary_ta : bnn.summary_en;
    const tRow = $('#bnn-trines-row');
    if (tRow && bnn.trines) {
      tRow.replaceChildren();
      Object.entries(bnn.trines).forEach(([tKey, tData]) => {
        const item = document.createElement('div');
        item.className = 'timing-meta-item';
        const pNames = tData.planets.map(p => isTa ? p.tamil : p.name).join(', ') || (isTa ? 'கிரகங்கள் இல்லை' : 'Empty');
        item.innerHTML = `
          <small>${esc(isTa ? tData.name_ta : tData.name_en)}</small>
          <strong style="font-size:13px; color:var(--text-primary)">${esc(pNames)}</strong>
        `;
        tRow.append(item);
      });
    }

    const sGrid = $('#bnn-sutras-grid');
    if (sGrid && bnn.sutras) {
      sGrid.replaceChildren();
      bnn.sutras.forEach(s => {
        const card = document.createElement('div');
        card.className = 'cosmic-card reading-card';
        const title = isTa ? s.title_ta : s.title_en;
        const desc = isTa ? s.significance_ta : s.significance_en;
        card.innerHTML = `
          <div class="reading-header">
            <span class="reading-icon">📜</span>
            <div>
              <h3 style="color:var(--gold);">${esc(title)}</h3>
              <small class="muted">${isTa ? 'இணைந்த கிரகங்கள்' : 'Associated Grahas'}: ${grahaNames(s.planets, ' + ')}</small>
            </div>
          </div>
          <p class="reading-body" style="font-size:12.5px">${esc(desc)}</p>
        `;
        sGrid.append(card);
      });
    }
  }

  // Chapter 15: Planetary Avasthas & Consciousness States
  const av = pred.avasthas;
  if (av && av.avasthas) {
    const aGrid = $('#avasthas-cards-grid');
    if (aGrid) {
      aGrid.replaceChildren();
      av.avasthas.forEach(a => {
        const card = document.createElement('div');
        card.className = 'cosmic-card reading-card';
        const pInfo = PLANET_NAMES[a.planet] || { en: a.planet, ta: a.planet, color: '#e5c378' };
        const label = isTa ? a.planet_ta : a.planet;
        const bLabel = isTa ? a.baladi_ta : a.baladi;
        const jLabel = isTa ? a.jagradadi_ta : a.jagradadi;
        const interp = isTa ? a.interpretation_ta : a.interpretation_en;

        card.innerHTML = `
          <div class="reading-header">
            <span class="bhava-num-badge" style="border-color:${pInfo.color}; color:${pInfo.color}">${pInfo.short || a.planet.slice(0, 2)}</span>
            <div>
              <h3>${esc(label)} — ${a.degree_str}</h3>
              <small class="muted">${esc(bLabel)} · ${esc(jLabel)}</small>
            </div>
          </div>
          <div class="timing-score-bar" style="margin:8px 0;">
            <small class="muted">${isTa ? 'நடைமுறை பலன் கொடுக்கும் விகிதம்' : 'Fruit Potency'}:</small>
            <div class="timing-track" style="flex:1; margin:0 8px;">
              <div class="timing-fill" style="width:${a.fruit_potency}%; background:${a.fruit_potency >= 75 ? '#2ecc71' : (a.fruit_potency >= 40 ? 'var(--gold)' : '#e63946')}"></div>
            </div>
            <strong style="color:var(--gold); font-size:12px">${a.fruit_potency}%</strong>
          </div>
          <p class="reading-body" style="font-size:12.5px">${esc(interp)}</p>
          ${(a.lajjitadi || []).length ? `<ul class="bhava-factors">${a.lajjitadi.map(m => `
            <li class="${m.effect > 0 ? 'plus' : 'minus'}"><strong>${esc(txt(m.en, m.ta))}</strong> — ${esc(txt(m.reading_en, m.reading_ta))}</li>`).join('')}
          </ul>` : ''}
        `;
        aGrid.append(card);
      });
    }
  }

  // Chapter 16: Birth Nakshatra Pada Reading
  const pada = pred.pada_reading;
  if (pada) {
    $('#pada-element-badge').textContent = isTa ? pada.element_ta : pada.element;
    $('#pada-star-name').textContent = isTa ? pada.tamil_nakshatra : pada.nakshatra;
    $('#pada-num-display').textContent = `${isTa ? 'பாதம்' : 'Pada'} ${pada.pada} (${isTa ? pada.element_ta : pada.element})`;
    $('#pada-nav-sign').textContent = isTa ? pada.navamsa_ta : pada.navamsa_sign;
    $('#pada-nav-lord').textContent = `${isTa ? 'அதிபதி' : 'Lord'}: ${isTa ? pada.pada_lord_ta : pada.pada_lord}`;
    $('#pada-reading-title').textContent = isTa
      ? `${pada.tamil_nakshatra} பாதம் ${pada.pada} வாழ்க்கைப் பலன்கள்`
      : `${pada.nakshatra} Pada ${pada.pada} Destiny Analysis`;
    $('#pada-reading-sub').textContent = isTa
      ? `நவாம்சம்: ${pada.navamsa_ta} · பூத தத்துவம்: ${pada.element_ta}`
      : `Navamsa: ${pada.navamsa_sign} · Element: ${pada.element}`;
    $('#pada-reading-body').textContent = isTa ? pada.reading_ta : pada.reading_en;
  }

  // Chapter 17: Sensitive Sahams
  const sh = pred.sahams;
  if (sh) {
    $('#sahams-birth-type-badge').textContent = isTa ? sh.birth_type_ta : sh.birth_type_en;
    const sGrid = $('#sahams-cards-grid');
    if (sGrid && sh.sahams) {
      sGrid.replaceChildren();
      sh.sahams.forEach(s => {
        const card = document.createElement('div');
        card.className = 'cosmic-card reading-card';
        const name = isTa ? s.name_ta : s.name_en;
        const sign = isTa ? s.tamil_sign : s.sign;
        const kw = isTa ? s.keyword_ta : s.keyword_en;
        const reading = isTa ? s.reading_ta : s.reading_en;

        card.innerHTML = `
          <div class="reading-header">
            <span class="reading-icon">🔮</span>
            <div>
              <h3>${esc(name)}</h3>
              <small class="muted">${sign} ${s.degree_str} · ${isTa ? 'பாவம்' : 'House'} ${s.house} (${esc(kw)})</small>
            </div>
            ${s.strength ? `<span class="status-pill ${s.strength === 'strong' ? 'success' : (s.strength === 'weak' ? 'danger' : 'neutral')}">${esc(txt({ strong: 'Strong', moderate: 'Moderate', weak: 'Weak' }[s.strength], { strong: 'பலம்', moderate: 'மத்திமம்', weak: 'பலவீனம்' }[s.strength]))}</span>` : ''}
          </div>
          <p class="reading-body" style="font-size:12.5px">${esc(reading)}</p>
        `;
        sGrid.append(card);
      });
    }
  }

  // Chapters in the shared report shape (numerology and the newer reports)
  REPORT_CHAPTERS.forEach(key => renderReportChapter(key, pred[key]));
  renderParisodhanai(pred.parisodhanai);
  renderAskPanel();
  // The long chapters follow in the background once the first screen is drawn
  if (pred.deferred_chapters?.length) setTimeout(loadDeferredChapters, 1200);
}

// The long report chapters (the yearly forecast, monthly transits, the life areas) arrive separately
// from the chart; fetched once per chart, then drawn into their tabs
function loadDeferredChapters() {
  const chart = currentChart;
  const keys = chart?.predictions?.deferred_chapters || [];
  if (!keys.length) return Promise.resolve();
  if (!chart._chaptersLoad) {
    chart._chaptersLoad = fetch('/api/chapters', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...currentChartPayload, lang: currentLang, keys })
    }).then(resp => resp.json().then(data => {
      if (!resp.ok) throw new Error(data.error || 'The reports could not be loaded.');
      learnMalayalam(data);
      Object.assign(chart.predictions, data.chapters);
      chart.predictions.deferred_chapters = keys.filter(k => !data.chapters[k]);
      if (chart === currentChart) Object.keys(data.chapters).forEach(k => renderReportChapter(k, data.chapters[k]));
    })).catch(err => {
      chart._chaptersLoad = null;
      notify(errorText(err.message));
    });
  }
  return chart._chaptersLoad;
}

// Chapters that use the shared report shape: a tab and panel each, drawn by renderReportChapter
const REPORT_CHAPTERS = ['parihara', 'monthly', 'varshaphal', 'marriage', 'career_report', 'chakras', 'numerology', 'yearly',
  'education', 'children', 'health', 'wealth', 'foreign', 'spiritual'];
const VERDICT_PILLS = { good: ['success', 'Favourable', 'சாதகம்'], mixed: ['neutral', 'Mixed', 'கலப்பு'], bad: ['danger', 'Needs care', 'கவனம் தேவை'] };

function reportCardHtml(c) {
  const pill = c.verdict ? VERDICT_PILLS[c.verdict] : null;
  return `
    <div class="cosmic-card reading-card">
      <div class="reading-header">
        <span class="reading-icon">${esc(c.icon || '✦')}</span>
        <div>
          <h3>${esc(txt(c.title.en, c.title.ta, c.title.ml))}</h3>
          ${c.sub && (c.sub.en || c.sub.ta) ? `<small class="muted">${esc(txt(c.sub.en, c.sub.ta, c.sub.ml))}</small>` : ''}
        </div>
        ${pill ? `<span class="status-pill ${pill[0]}">${txt(pill[1], pill[2])}</span>` : ''}
      </div>
      <p class="reading-body">${esc(txt(c.body.en, c.body.ta, c.body.ml))}</p>
    </div>`;
}

function reportTableHtml(t) {
  return `
    <div class="cosmic-card report-table-card">
      <h3>${esc(txt(t.title.en, t.title.ta, t.title.ml))}</h3>
      <div class="table-responsive">
        <table class="luxury-table">
          <thead><tr>${t.head.map(h => `<th>${esc(txt(h.en, h.ta, h.ml))}</th>`).join('')}</tr></thead>
          <tbody>${t.rows.map(row => `<tr>${row.map(c => `<td>${esc(txt(c.en, c.ta, c.ml))}</td>`).join('')}</tr>`).join('')}</tbody>
        </table>
      </div>
    </div>`;
}

// A square chakra (the Sarvatobhadra's 9 x 9 cells), east on top
function reportGridHtml(grid) {
  return `<div class="cosmic-card report-table-card"><div class="chakra-grid">${grid.flat().map(c =>
    `<div class="chakra-cell ${esc(c.cls || '')}">${esc(txt(c.en, c.ta, c.ml))}</div>`).join('')}</div></div>`;
}

function renderReportChapter(key, ch) {
  const panel = document.getElementById(`ppanel-${key}`);
  renderChapterInto(panel, ch);
  if (key === 'yearly' && ch && panel) {
    const intro = panel.querySelector('.report-intro');
    intro?.insertAdjacentHTML('beforeend', `<button type="button" class="action-btn ics-btn" id="yearly-ics-btn">📅 ${esc(txt(
      'Add dasa changes and good/careful periods to my calendar', 'தசா மாற்றங்கள், நல்ல/கவனமான காலங்களை நாட்காட்டியில் சேர்',
      'ദശാമാറ്റങ്ങളും നല്ല/ശ്രദ്ധിക്കേണ്ട കാലങ്ങളും കലണ്ടറിൽ ചേർക്കുക'))}</button>`);
    $('#yearly-ics-btn')?.addEventListener('click', exportYearlyIcs);
  }
}

// The year-by-year forecast as calendar events: each Bhukti's start, the good and careful Pratyantara
// periods, and Saturn's cycles from the Moon, from today on
function exportYearlyIcs() {
  const ch = currentChart?.predictions?.yearly;
  if (!ch) return;
  const name = currentChart.profile?.name || 'JoRoScope';
  const tag = name.replace(/\W+/g, '');
  const today = new Date().toISOString().slice(0, 10);
  const dayBefore = ymd => { const d = new Date(`${ymd}T00:00:00Z`); d.setUTCDate(d.getUTCDate() - 1); return d.toISOString().slice(0, 10); };
  const lastDay = (start, end) => (end > start ? dayBefore(end) : start);  // periods end on the day the next begins
  const events = [];
  const seen = new Set();
  ch.years.forEach(y => {
    y.bhuktis.forEach(b => {
      const key = `${b.dasa}-${b.bhukti}`;
      if (b.start < today || seen.has(key) || b.start.endsWith('-01-01')) return;  // a Bhukti running on 1 January began earlier
      seen.add(key);
      events.push({ uid: `bhukti-${tag}-${b.start}`, start: b.start,
        title: txt(`${grahaName(b.dasa)} Dasa, ${grahaName(b.bhukti)} Bhukti begins (${name})`, `${grahaName(b.dasa)} தசை, ${grahaName(b.bhukti)} புக்தி தொடக்கம் (${name})`,
          `${grahaName(b.dasa)} ദശ, ${grahaName(b.bhukti)} ഭുക്തി ആരംഭം (${name})`) });
    });
    [['good', y.good_months], ['care', y.care_months]].forEach(([kind, list]) => list.forEach(m => {
      if (lastDay(m.start, m.end) < today) return;
      events.push({ uid: `${kind}-${tag}-${m.start}`, start: m.start < today ? today : m.start, end: lastDay(m.start, m.end),
        title: kind === 'good'
          ? txt(`Good period: ${grahaName(m.lord)} Pratyantara (${name})`, `நல்ல காலம்: ${grahaName(m.lord)} பிரத்யந்தரம் (${name})`, `നല്ല കാലം: ${grahaName(m.lord)} പ്രത്യന്തരം (${name})`)
          : txt(`Careful period: ${grahaName(m.lord)} Pratyantara (${name})`, `கவனமான காலம்: ${grahaName(m.lord)} பிரத்யந்தரம் (${name})`, `ശ്രദ്ധിക്കേണ്ട കാലം: ${grahaName(m.lord)} പ്രത്യന്തരം (${name})`) });
    }));
  });
  const cycleNames = { sade_sati: ['Sade Sati', 'ஏழரைச் சனி', 'ഏഴരശ്ശനി'], ashtama: ['Ashtama Sani', 'அஷ்டம சனி', 'അഷ്ടമശ്ശനി'],
    kandaka: ['Kandaka Sani', 'கண்டக சனி', 'കണ്ടകശ്ശനി'], ardhashtama: ['Ardhashtama Sani', 'அர்த்தாஷ்டம சனி', 'അർദ്ധാഷ്ടമശ്ശനി'] };
  (currentChart.gochara?.saturn_cycles || []).forEach(c => {
    const words = cycleNames[c.kind];
    if (!words || c.end.slice(0, 10) < today) return;
    events.push({ uid: `saturn-${c.kind}-${tag}-${c.start.slice(0, 10)}`, start: c.start.slice(0, 10) < today ? today : c.start.slice(0, 10),
      end: c.end.slice(0, 10), title: `${txt(...words)} (${name})` });
  });
  if (!events.length) return;
  downloadText(`JoRoScope-Forecast-${name.replace(/\W+/g, '-')}.ics`, buildIcs(events, txt('JoRoScope forecast', 'JoRoScope பலன்', 'JoRoScope ഫലം')), 'text/calendar');
}

function renderChapterInto(panel, ch) {
  if (!panel) return;
  const key = panel.id.replace('ppanel-', '');
  if (!ch && currentChart?.predictions?.deferred_chapters?.includes(key)) {
    panel.innerHTML = `<p class="muted">${esc(txt('Loading this report…', 'இந்த அறிக்கை ஏற்றப்படுகிறது…', 'ഈ റിപ്പോർട്ട് ലോഡ് ചെയ്യുന്നു…'))}</p>`;
    return;
  }
  if (!ch) {
    panel.innerHTML = `<p class="muted">${txt('Not available for this chart.', 'இந்த ஜாதகத்திற்குக் கிடைக்கவில்லை.')}</p>`;
    return;
  }
  panel.innerHTML = `
    <div class="cosmic-card report-intro">
      <h2>${esc(txt(ch.title.en, ch.title.ta, ch.title.ml))}</h2>
      <p class="muted">${esc(txt(ch.intro.en, ch.intro.ta, ch.intro.ml))}</p>
    </div>
    ${ch.grid ? reportGridHtml(ch.grid) : ''}
    ${ch.cards_first ? '' : ch.tables.map(reportTableHtml).join('')}
    <div class="readings-grid">${ch.cards.map(reportCardHtml).join('')}</div>
    ${ch.cards_first ? ch.tables.map(reportTableHtml).join('') : ''}`;
}

// Parisodhanai (chart verification): the person marks each statement about their past right or
// wrong, enters the real dates of past events, and can send those dates to rectification. The
// marks are kept in this browser, per birth data.
const VERIFY_GROUPS = [
  ['siblings', 'Siblings', 'உடன்பிறப்புகள்', 'സഹോദരങ്ങൾ'],
  ['parents', 'Parents', 'பெற்றோர்', 'മാതാപിതാക്കൾ'],
  ['events', 'Past events', 'கடந்த நிகழ்வுகள்', 'കഴിഞ്ഞ സംഭവങ്ങൾ'],
];
const CONFIDENCE_PILLS = { strong: 'success', moderate: 'neutral', weak: 'danger' };
const FAMILY_LABELS = {
  elder_brothers: ['Elder brothers', 'அண்ணன்', 'ജ്യേഷ്ഠന്മാർ'], elder_sisters: ['Elder sisters', 'அக்கா', 'ജ്യേഷ്ഠത്തിമാർ'],
  younger_brothers: ['Younger brothers', 'தம்பி', 'അനുജന്മാർ'], younger_sisters: ['Younger sisters', 'தங்கை', 'അനുജത്തിമാർ'],
};

function verifyKey() {
  const prof = currentChart?.profile || {};
  return `joroscope_verify_${prof.date}_${prof.time}_${prof.latitude}_${prof.longitude}`;
}

function loadVerify() {
  try {
    return JSON.parse(localStorage.getItem(verifyKey()) || '{}');
  } catch (e) {
    return {};
  }
}

function saveVerify(marks) {
  try {
    localStorage.setItem(verifyKey(), JSON.stringify(marks));
  } catch (e) {}
}

function verifyScoreText(statements, marks) {
  const right = statements.filter(s => marks[s.key]?.mark === 'right').length;
  const wrong = statements.filter(s => marks[s.key]?.mark === 'wrong').length;
  const checked = right + wrong;
  if (!checked) {
    return txt('Mark each statement ✔ right or ✘ wrong to see how well the chart matches your life.',
      'ஒவ்வொரு கூற்றையும் ✔ சரி அல்லது ✘ தவறு எனக் குறித்தால் ஜாதகம் உங்கள் வாழ்க்கையுடன் எவ்வளவு பொருந்துகிறது எனத் தெரியும்.',
      'ഓരോ പ്രസ്താവനയും ✔ ശരി അല്ലെങ്കിൽ ✘ തെറ്റ് എന്ന് അടയാളപ്പെടുത്തിയാൽ ജാതകം നിങ്ങളുടെ ജീവിതവുമായി എത്രത്തോളം യോജിക്കുന്നു എന്ന് കാണാം.');
  }
  const pct = Math.round(right / checked * 100);
  const verdict = pct >= 70
    ? txt('The chart matches your life well; its predictions can be relied on.', 'ஜாதகம் உங்கள் வாழ்க்கையுடன் நன்கு பொருந்துகிறது; அதன் பலன்களை நம்பலாம்.',
      'ജാതകം നിങ്ങളുടെ ജീവിതവുമായി നന്നായി യോജിക്കുന്നു; ഇതിന്റെ ഫലങ്ങൾ വിശ്വസിക്കാം.')
    : pct >= 50
      ? txt('A partial match; entering the real dates of past events and rectifying the birth time may improve it.',
        'பகுதியளவு பொருத்தம்; கடந்த நிகழ்வுகளின் உண்மையான தேதிகளை உள்ளிட்டு பிறந்த நேரத்தைத் திருத்தினால் மேம்படலாம்.',
        'ഭാഗികമായ യോജിപ്പ്; കഴിഞ്ഞ സംഭവങ്ങളുടെ യഥാർത്ഥ തീയതികൾ നൽകി ജനനസമയം തിരുത്തിയാൽ മെച്ചപ്പെടാം.')
      : txt('A poor match: the birth time is probably off. Enter the real dates of past events and run Birth Time Rectification.',
        'பொருத்தம் குறைவு: பிறந்த நேரம் மாறியிருக்கலாம். கடந்த நிகழ்வுகளின் உண்மையான தேதிகளை உள்ளிட்டு ஜனன நேரத் திருத்தம் செய்யவும்.',
        'യോജിപ്പ് കുറവ്: ജനനസമയം മാറിയിരിക്കാം. കഴിഞ്ഞ സംഭവങ്ങളുടെ യഥാർത്ഥ തീയതികൾ നൽകി ജനനസമയ തിരുത്തൽ ചെയ്യുക.');
  return txt(`${right} of ${checked} checked statements are right (${pct}%). `, `சரிபார்த்த ${checked} கூற்றுகளில் ${right} சரி (${pct}%). `,
    `പരിശോധിച്ച ${checked} പ്രസ്താവനകളിൽ ${right} ശരി (${pct}%). `) + verdict;
}

function renderParisodhanai(ch) {
  const panel = document.getElementById('ppanel-parisodhanai');
  if (!panel) return;
  if (!ch) {
    panel.innerHTML = `<p class="muted">${txt('Not available for this chart.', 'இந்த ஜாதகத்திற்குக் கிடைக்கவில்லை.')}</p>`;
    return;
  }
  const marks = loadVerify();
  const item = s => {
    const m = marks[s.key] || {};
    const dateField = s.topic === 'events' ? `
      <label class="verify-date">${esc(txt('When did it happen?', 'எப்போது நடந்தது?', 'എപ്പോൾ സംഭവിച്ചു?'))}
        <input type="date" data-verify-date="${esc(s.key)}" value="${esc(m.date || '')}"></label>` : '';
    return `
      <div class="verify-item${m.mark ? ` marked-${m.mark}` : ''}" data-key="${esc(s.key)}">
        <div class="verify-text">
          <p><strong>${esc(txt(s.en, s.ta, s.ml))}</strong>
            <span class="status-pill ${CONFIDENCE_PILLS[s.confidence]}">${esc(txt(s.confidence_en, s.confidence_ta, s.confidence_ml))}</span></p>
          <small class="muted">${esc(txt(s.basis_en, s.basis_ta, s.basis_ml))}</small>
          ${dateField}
        </div>
        <div class="verify-buttons">
          <button type="button" class="verify-btn right${m.mark === 'right' ? ' active' : ''}" data-mark="right"
            aria-pressed="${m.mark === 'right'}">✔ ${esc(txt('Right', 'சரி', 'ശരി'))}</button>
          <button type="button" class="verify-btn wrong${m.mark === 'wrong' ? ' active' : ''}" data-mark="wrong"
            aria-pressed="${m.mark === 'wrong'}">✘ ${esc(txt('Wrong', 'தவறு', 'തെറ്റ്'))}</button>
        </div>
      </div>`;
  };
  panel.innerHTML = `
    <div class="cosmic-card report-intro">
      <h2>${esc(txt(ch.title.en, ch.title.ta, ch.title.ml))}</h2>
      <p class="muted">${esc(txt(ch.intro.en, ch.intro.ta, ch.intro.ml))}</p>
      <p class="verify-score" id="verify-score">${esc(verifyScoreText(ch.statements, marks))}</p>
    </div>
    ${VERIFY_GROUPS.map(([topic, en, ta, ml]) => {
      const list = ch.statements.filter(s => s.topic === topic);
      const family = topic === 'siblings' ? `
      <div class="verify-family">
        <span class="muted">${esc(txt('Your real numbers (they help Birth Time Rectification):', 'உங்கள் உண்மையான எண்ணிக்கை (ஜனன நேரத் திருத்தத்துக்கு உதவும்):',
          'നിങ്ങളുടെ യഥാർത്ഥ എണ്ണം (ജനനസമയ തിരുത്തലിന് സഹായിക്കും):'))}</span>
        ${RECT_FAMILY.map(k => `<label>${esc(txt(...FAMILY_LABELS[k]))}
          <input type="number" min="0" max="15" inputmode="numeric" data-family="${k}" value="${esc(marks.family?.[k] ?? '')}"></label>`).join('')}
      </div>` : '';
    return list.length ? `<div class="cosmic-card verify-group"><h3>${esc(txt(en, ta, ml))}</h3>${list.map(item).join('')}${family}</div>` : '';
    }).join('')}
    <div class="cosmic-card verify-actions">
      <p class="muted">${esc(txt('The dates of past events and your real sibling numbers can test the birth time on the Tools page.',
        'கடந்த நிகழ்வுத் தேதிகளும் உண்மையான உடன்பிறப்பு எண்ணிக்கையும் கருவிகள் பக்கத்தில் பிறந்த நேரத்தைச் சோதிக்க உதவும்.',
        'കഴിഞ്ഞ സംഭവങ്ങളുടെ തീയതികളും സഹോദരങ്ങളുടെ യഥാർത്ഥ എണ്ണവും ടൂൾസ് പേജിൽ ജനനസമയം പരിശോധിക്കാൻ സഹായിക്കും.'))}</p>
      <button type="button" class="action-btn" id="verify-to-rect">${esc(txt('Send to Birth Time Rectification',
        'ஜனன நேரத் திருத்தத்திற்கு அனுப்பு', 'ജനനസമയ തിരുത്തലിലേക്ക് അയയ്ക്കുക'))}</button>
    </div>
    <div class="cosmic-card verify-share">
      <h3>${esc(txt('Help make JoRoScope more accurate', 'JoRoScope-ஐ மேலும் துல்லியமாக்க உதவுங்கள்', 'JoRoScope കൂടുതൽ കൃത്യമാക്കാൻ സഹായിക്കുക'))}</h3>
      <p class="muted">${esc(txt('Share your right/wrong marks, the dates you entered and your sibling numbers with the owner of this JoRoScope, to measure which rules work. Your name, birth date, time and place are not stored.',
        'எந்த விதிகள் சரியாக வேலை செய்கின்றன என அளக்க, உங்கள் சரி/தவறு குறிப்புகள், உள்ளிட்ட தேதிகள், உடன்பிறப்பு எண்ணிக்கையை இந்த JoRoScope உரிமையாளருடன் பகிரவும். உங்கள் பெயர், பிறந்த தேதி, நேரம், இடம் சேமிக்கப்படாது.',
        'ഏത് നിയമങ്ങൾ ശരിയാകുന്നു എന്ന് അളക്കാൻ, നിങ്ങളുടെ ശരി/തെറ്റ് അടയാളങ്ങൾ, നൽകിയ തീയതികൾ, സഹോദരങ്ങളുടെ എണ്ണം എന്നിവ ഈ JoRoScope ഉടമയുമായി പങ്കിടുക. നിങ്ങളുടെ പേര്, ജനനതീയതി, സമയം, സ്ഥലം എന്നിവ സൂക്ഷിക്കില്ല.'))}</p>
      <label class="verify-consent"><input type="checkbox" id="share-consent">
        ${esc(txt('I agree to share these marks anonymously.', 'இந்தக் குறிப்புகளைப் பெயரின்றிப் பகிர ஒப்புக்கொள்கிறேன்.', 'ഈ അടയാളങ്ങൾ പേരില്ലാതെ പങ്കിടാൻ ഞാൻ സമ്മതിക്കുന്നു.'))}</label>
      <button type="button" class="action-btn" id="share-marks">${esc(txt('Share my marks', 'என் குறிப்புகளைப் பகிர்', 'എന്റെ അടയാളങ്ങൾ പങ്കിടുക'))}</button>
    </div>`;

  const refresh = () => { $('#verify-score').textContent = verifyScoreText(ch.statements, marks); };
  panel.querySelectorAll('.verify-item').forEach(row => {
    const key = row.dataset.key;
    row.querySelectorAll('.verify-btn').forEach(btn => btn.addEventListener('click', () => {
      const mark = marks[key]?.mark === btn.dataset.mark ? null : btn.dataset.mark;  // a second click clears it
      marks[key] = { ...(marks[key] || {}), mark };
      row.classList.remove('marked-right', 'marked-wrong');
      if (mark) row.classList.add(`marked-${mark}`);
      row.querySelectorAll('.verify-btn').forEach(b => {
        b.classList.toggle('active', b.dataset.mark === mark);
        b.setAttribute('aria-pressed', String(b.dataset.mark === mark));
      });
      saveVerify(marks);
      refresh();
    }));
    row.querySelector('[data-verify-date]')?.addEventListener('change', e => {
      marks[key] = { ...(marks[key] || {}), date: e.target.value };
      saveVerify(marks);
    });
  });
  $('#share-marks').addEventListener('click', () => shareMarks(marks));
  panel.querySelectorAll('[data-family]').forEach(input => input.addEventListener('change', () => {
    marks.family = { ...(marks.family || {}), [input.dataset.family]: input.value };
    saveVerify(marks);
  }));
  $('#verify-to-rect').addEventListener('click', () => {
    const events = ch.statements.filter(s => s.event && marks[s.key]?.date).map(s => ({ date: marks[s.key].date, type: s.event }));
    const family = Object.entries(marks.family || {}).filter(([, v]) => v !== '' && v != null);
    if (!events.length && !family.length) {
      notify(txt('Enter a past event date or your sibling numbers first.', 'முதலில் ஒரு கடந்த நிகழ்வுத் தேதி அல்லது உடன்பிறப்பு எண்ணிக்கையை உள்ளிடவும்.',
        'ആദ്യം ഒരു കഴിഞ്ഞ സംഭവ തീയതിയോ സഹോദരങ്ങളുടെ എണ്ണമോ നൽകുക.'));
      return;
    }
    if (events.length) rectEvents.splice(0, rectEvents.length, ...events.slice(0, 12));
    navigatePage('tools');
    renderRectEvents();
    family.forEach(([k, v]) => { const el = $(`#rect-${k.replace('_', '-')}`); if (el) el.value = v; });
    $('#rect-events')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
  });
}

// Ask about my chart: questions answered by Claude from the chart the server calculates. The
// conversation lives in this page, per chart; the passcode is kept for the browser session only.
const ASK_EXAMPLES = [
  ['When is a good time for a job change?', 'வேலை மாற்றத்திற்கு நல்ல காலம் எப்போது?', 'ജോലി മാറ്റത്തിന് നല്ല സമയം എപ്പോൾ?'],
  ['What does my current dasa mean for me?', 'தற்போதைய தசை எனக்கு என்ன பலன் தரும்?', 'ഇപ്പോഴത്തെ ദശ എനിക്ക് എന്ത് ഫലം നൽകും?'],
  ['Is next year good for buying a house?', 'அடுத்த ஆண்டு வீடு வாங்க நல்லதா?', 'അടുത്ത വർഷം വീട് വാങ്ങാൻ നല്ലതാണോ?'],
  ['Which remedy should I start with?', 'எந்தப் பரிகாரத்தை முதலில் செய்ய வேண்டும்?', 'ഏത് പരിഹാരം ആദ്യം ചെയ്യണം?'],
];
let aiStatus = null;
let askChat = { key: null, turns: [] };
let askBusy = false;

async function loadAiStatus() {
  try {
    const resp = await fetch('/api/ai-status');
    aiStatus = resp.ok ? await resp.json() : null;
  } catch (e) {
    aiStatus = null;
  }
  return aiStatus;
}

function askPasscode(value) {
  try {
    if (value !== undefined) sessionStorage.setItem('joroscope_ai_passcode', value);
    return sessionStorage.getItem('joroscope_ai_passcode') || '';
  } catch (e) {
    return value || '';
  }
}

// Answers come as light Markdown: headings, bullets and bold, drawn safely from escaped text
function askAnswerHtml(text) {
  const inline = s => esc(s).replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  let html = '', list = false;
  text.split('\n').forEach(line => {
    const t = line.trim();
    const bullet = /^[-*•]\s+/.test(t);
    if (list && !bullet) { html += '</ul>'; list = false; }
    if (!t) return;
    if (/^#{1,4}\s/.test(t)) html += `<h4>${inline(t.replace(/^#+\s*/, ''))}</h4>`;
    else if (bullet) { if (!list) { html += '<ul>'; list = true; } html += `<li>${inline(t.replace(/^[-*•]\s+/, ''))}</li>`; }
    else html += `<p>${inline(t)}</p>`;
  });
  return html + (list ? '</ul>' : '');
}

async function renderAskPanel() {
  const panel = document.getElementById('ppanel-ask');
  if (!panel || !currentChart) return;
  const key = verifyKey();
  if (askChat.key !== key) askChat = { key, turns: [] };
  const status = aiStatus || await loadAiStatus();
  const canAsk = !!(status?.enabled && !status.remote_blocked);  // answers inside JoRoScope need the owner's API key
  panel.innerHTML = `
    <div class="cosmic-card report-intro">
      <h2>${esc(txt('Ask about my chart', 'ஜாதகம் பற்றிக் கேளுங்கள்', 'ജാതകത്തെക്കുറിച്ച് ചോദിക്കുക'))}</h2>
      <p class="muted">${esc(txt('Claude, an AI, answers from the chart JoRoScope has calculated and cites the dasas and placements it used. The answers are classical indications, not certainties.',
        'Claude என்ற AI, JoRoScope கணித்த ஜாதகத்திலிருந்து பதிலளித்து, பயன்படுத்திய தசைகளையும் கிரக நிலைகளையும் குறிப்பிடும். பதில்கள் பாரம்பரியக் குறிப்புகள், உறுதியானவை அல்ல.',
        'Claude എന്ന AI, JoRoScope കണക്കാക്കിയ ജാതകത്തിൽ നിന്ന് ഉത്തരം നൽകുകയും ഉപയോഗിച്ച ദശകളും ഗ്രഹസ്ഥിതികളും സൂചിപ്പിക്കുകയും ചെയ്യും. ഉത്തരങ്ങൾ പരമ്പരാഗത സൂചനകളാണ്, ഉറപ്പല്ല.'))}</p>
      <p class="ask-privacy">📋 ${esc(txt('Copy for Claude: copies your chart and question to paste into Claude (claude.ai) with your own account. JoRoScope sends nothing itself.',
        'Claude-க்கு நகலெடு: உங்கள் ஜாதகத்தையும் கேள்வியையும் நகலெடுக்கும்; அதை உங்கள் சொந்தக் கணக்கில் Claude (claude.ai)-இல் ஒட்டவும். JoRoScope தானாக எதையும் அனுப்பாது.',
        'Claude-നായി പകർത്തുക: നിങ്ങളുടെ ജാതകവും ചോദ്യവും പകർത്തുന്നു; അത് സ്വന്തം അക്കൗണ്ടിൽ Claude (claude.ai)-ൽ ഒട്ടിക്കുക. JoRoScope സ്വയം ഒന്നും അയയ്ക്കുന്നില്ല.'))}</p>
      ${canAsk ? `<p class="ask-privacy">🔒 ${esc(txt('Ask: answers here, sending this birth date, time and place and the chart to Anthropic, the maker of Claude.',
        'கேள்: இங்கேயே பதில்; இதற்காக இந்தப் பிறந்த தேதி, நேரம், இடம், ஜாதகம் Claude-ஐ உருவாக்கிய Anthropic-க்கு அனுப்பப்படும்.',
        'ചോദിക്കുക: ഇവിടെത്തന്നെ ഉത്തരം; ഇതിനായി ഈ ജനനതീയതി, സമയം, സ്ഥലം, ജാതകം Claude നിർമ്മിച്ച Anthropic-ലേക്ക് അയയ്ക്കുന്നു.'))}</p>` : ''}
    </div>
    <div class="cosmic-card ask-card">
      ${canAsk && status.passcode_required ? `<label class="ask-passcode">${esc(txt('Passcode', 'கடவுக்குறி', 'പാസ്‌കോഡ്'))}
        <input type="password" id="ask-passcode" autocomplete="off" value="${esc(askPasscode())}"></label>` : ''}
      <div class="ask-log" id="ask-log" aria-live="polite"></div>
      <div class="ask-examples">
        ${ASK_EXAMPLES.map((q, i) => `<button type="button" class="link-btn ask-example" data-example="${i}">${esc(txt(...q))}</button>`).join('')}
      </div>
      <form class="ask-form" id="ask-form">
        <textarea id="ask-question" rows="2" maxlength="1000" placeholder="${esc(txt('Ask a question about this chart…', 'இந்த ஜாதகம் பற்றி ஒரு கேள்வி கேளுங்கள்…', 'ഈ ജാതകത്തെക്കുറിച്ച് ഒരു ചോദ്യം ചോദിക്കുക…'))}"></textarea>
        <div class="ask-actions">
          ${canAsk ? `<button type="submit" class="action-btn" id="ask-send">${esc(txt('Ask', 'கேள்', 'ചോദിക്കുക'))}</button>` : ''}
          <button type="button" class="action-btn" id="ask-copy">📋 ${esc(txt('Copy for Claude', 'Claude-க்கு நகலெடு', 'Claude-നായി പകർത്തുക'))}</button>
        </div>
      </form>
      <div class="ask-reading">
        <span class="muted">${esc(txt('Overall reading of this chart:', 'இந்த ஜாதகத்தின் முழுப் பலன்:', 'ഈ ജാതകത്തിന്റെ സമഗ്ര ഫലം:'))}</span>
        ${canAsk ? `<button type="button" class="link-btn" id="ask-reading">✨ ${esc(txt('Write it here', 'இங்கே எழுது', 'ഇവിടെ എഴുതുക'))}</button>` : ''}
        <button type="button" class="link-btn" id="copy-reading">📋 ${esc(txt('Copy for Claude', 'Claude-க்கு நகலெடு', 'Claude-നായി പകർത്തുക'))}</button>
      </div>
      <div id="ask-copied" hidden></div>
    </div>`;
  drawAskLog();
  $('#ask-passcode')?.addEventListener('change', e => askPasscode(e.target.value));
  const question = () => $('#ask-question').value.trim();
  $('#ask-form').addEventListener('submit', e => {
    e.preventDefault();
    if (!canAsk) return copyForClaude(question(), 'question');
    if (question()) sendAsk(question(), 'question');
  });
  $('#ask-question').addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey && canAsk) { e.preventDefault(); $('#ask-form').requestSubmit(); }
  });
  $('#ask-copy').addEventListener('click', () => copyForClaude(question(), 'question'));
  $('#copy-reading').addEventListener('click', () => copyForClaude('', 'reading'));
  $('#ask-reading')?.addEventListener('click', () => sendAsk(txt('Write my overall reading', 'எனது முழுப் பலனை எழுது', 'എന്റെ സമഗ്ര ഫലം എഴുതുക'), 'reading'));
  panel.querySelectorAll('.ask-example').forEach(b => b.addEventListener('click', () => {
    $('#ask-question').value = txt(...ASK_EXAMPLES[b.dataset.example]);
    $('#ask-question').focus();
  }));
}

// Copy the prompt the server builds (rules, fact sheet, question) and point to Claude
async function copyForClaude(question, mode) {
  const box = $('#ask-copied');
  if (mode === 'question' && !question) {
    notify(txt('Type a question first.', 'முதலில் கேள்வியை உள்ளிடவும்.', 'ആദ്യം ചോദ്യം നൽകുക.'));
    return;
  }
  const marks = Object.fromEntries(Object.entries(loadVerify()).filter(([, m]) => m && (m.mark || m.date)));
  const promptPromise = fetch('/api/ai-prompt', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ birth: currentChartPayload, question, lang: currentLang, mode, marks })
  }).then(async resp => {
    const data = await resp.json();
    if (!resp.ok) throw new Error(data.error || 'Could not prepare the question.');
    return data.prompt;
  });
  // Start the clipboard write inside the click itself, with the text to follow: Safari refuses a
  // write that begins only after the page has waited for the server
  let clipboardWrite = null;
  try {
    if (window.ClipboardItem && navigator.clipboard?.write) {
      clipboardWrite = navigator.clipboard.write([new ClipboardItem({
        'text/plain': promptPromise.then(text => new Blob([text], { type: 'text/plain' }))
      })]);
    }
  } catch (e) {
    clipboardWrite = null;
  }
  clipboardWrite?.catch(() => {});  // a failure is handled below; this only silences an unawaited rejection
  try {
    const data = { prompt: await promptPromise };
    let copied = false;
    try {
      if (!clipboardWrite) throw new Error('no clipboard item');
      await clipboardWrite;
      copied = true;
    } catch (e) {
      try {
        await navigator.clipboard.writeText(data.prompt);
        copied = true;
      } catch (e2) {}
    }
    box.hidden = false;
    box.className = 'ask-copied';
    box.innerHTML = `
      <p>${esc(copied
        ? txt('Copied. Open Claude, paste it into a new chat (⌘V or Ctrl+V) and send. You can ask follow-up questions there.',
          'நகலெடுக்கப்பட்டது. Claude-ஐத் திறந்து புதிய உரையாடலில் ஒட்டி (⌘V அல்லது Ctrl+V) அனுப்பவும். தொடர் கேள்விகளை அங்கேயே கேட்கலாம்.',
          'പകർത്തി. Claude തുറന്ന് പുതിയ ചാറ്റിൽ ഒട്ടിച്ച് (⌘V അല്ലെങ്കിൽ Ctrl+V) അയയ്ക്കുക. തുടർചോദ്യങ്ങൾ അവിടെത്തന്നെ ചോദിക്കാം.')
        : txt('Your browser did not allow copying. Select the text below, copy it, and paste it into a new Claude chat.',
          'உங்கள் உலாவி நகலெடுக்க அனுமதிக்கவில்லை. கீழுள்ள உரையைத் தேர்ந்தெடுத்து நகலெடுத்து புதிய Claude உரையாடலில் ஒட்டவும்.',
          'നിങ്ങളുടെ ബ്രൗസർ പകർത്താൻ അനുവദിച്ചില്ല. താഴെയുള്ള വാചകം തിരഞ്ഞെടുത്ത് പകർത്തി പുതിയ Claude ചാറ്റിൽ ഒട്ടിക്കുക.'))}</p>
      <a class="action-btn" href="https://claude.ai/new" target="_blank" rel="noopener">${esc(txt('Open Claude ↗', 'Claude-ஐத் திற ↗', 'Claude തുറക്കുക ↗'))}</a>
      <details${copied ? '' : ' open'}><summary>${esc(txt('Show the text', 'உரையைக் காட்டு', 'വാചകം കാണിക്കുക'))}</summary>
        <textarea readonly rows="8">${esc(data.prompt)}</textarea></details>`;
    if (!copied) {
      const area = box.querySelector('textarea');
      area.select();
      try {
        copied = document.execCommand('copy');  // the older copy command, where the clipboard API is refused
      } catch (e) {}
      if (copied) {
        box.querySelector('p').textContent = txt('Copied. Open Claude, paste it into a new chat (⌘V or Ctrl+V) and send. You can ask follow-up questions there.',
          'நகலெடுக்கப்பட்டது. Claude-ஐத் திறந்து புதிய உரையாடலில் ஒட்டி (⌘V அல்லது Ctrl+V) அனுப்பவும். தொடர் கேள்விகளை அங்கேயே கேட்கலாம்.',
          'പകർത്തി. Claude തുറന്ന് പുതിയ ചാറ്റിൽ ഒട്ടിച്ച് (⌘V അല്ലെങ്കിൽ Ctrl+V) അയയ്ക്കുക. തുടർചോദ്യങ്ങൾ അവിടെത്തന്നെ ചോദിക്കാം.');
        box.querySelector('details').open = false;
      }
    }
  } catch (err) {
    notify(errorText(err.message));
  }
}

function drawAskLog() {
  const log = $('#ask-log');
  if (!log) return;
  log.innerHTML = askChat.turns.map(t => t.role === 'user'
    ? `<div class="ask-turn user"><p>${esc(t.content)}</p></div>`
    : `<div class="ask-turn assistant${t.error ? ' error' : ''}">${t.error ? `<p>${esc(t.content)}</p>` : askAnswerHtml(t.content)}</div>`).join('')
    + (askBusy ? `<div class="ask-turn assistant thinking"><p>${esc(txt('Reading your chart…', 'உங்கள் ஜாதகத்தைப் படிக்கிறது…', 'നിങ്ങളുടെ ജാതകം വായിക്കുന്നു…'))}</p></div>` : '');
  log.hidden = !askChat.turns.length && !askBusy;
  log.scrollTop = log.scrollHeight;
}

async function sendAsk(question, mode) {
  if (askBusy || !currentChartPayload) return;
  const chat = askChat;
  const history = chat.turns.filter(t => !t.error).map(t => ({ role: t.role, content: t.content }));
  chat.turns.push({ role: 'user', content: question });
  askBusy = true;
  if ($('#ask-question')) $('#ask-question').value = '';
  if ($('#ask-send')) $('#ask-send').disabled = true;
  drawAskLog();
  try {
    const marks = Object.fromEntries(Object.entries(loadVerify()).filter(([, m]) => m && (m.mark || m.date)));
    const resp = await fetch('/api/ask', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ birth: currentChartPayload, question, history, lang: currentLang, mode, marks,
        passcode: $('#ask-passcode')?.value || askPasscode() })
    });
    const data = await resp.json();
    if (!resp.ok) throw new Error(data.error || 'The question could not be answered.');
    chat.turns.push({ role: 'assistant', content: data.answer });
  } catch (err) {
    chat.turns.push({ role: 'assistant', content: errorText(err.message), error: true });
  } finally {
    askBusy = false;
    if ($('#ask-send')) $('#ask-send').disabled = false;
    if (askChat === chat) drawAskLog();
  }
}

// A random id per chart in this browser, so sharing again replaces the earlier entry
function shareId() {
  const make = () => [...crypto.getRandomValues(new Uint8Array(16))].map(b => b.toString(16).padStart(2, '0')).join('');
  const key = `${verifyKey()}_share`;
  try {
    let id = localStorage.getItem(key);
    if (!id) {
      id = make();
      localStorage.setItem(key, id);
    }
    return id;
  } catch (e) {
    return make();
  }
}

async function shareMarks(marks) {
  if (!$('#share-consent')?.checked) {
    notify(txt('Tick the box to agree first.', 'முதலில் ஒப்புதல் பெட்டியைத் தேர்ந்தெடுக்கவும்.', 'ആദ്യം സമ്മതം അടയാളപ്പെടുത്തുക.'));
    return;
  }
  try {
    const resp = await fetch('/api/feedback', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ birth: currentChartPayload, marks, submission_id: shareId(), consent: true })
    });
    const data = await resp.json();
    if (!resp.ok) throw new Error(data.error || 'Sharing failed.');
    const n = data.items + data.siblings;
    notify(txt(`Thank you: ${n} marks shared.`, `நன்றி: ${n} குறிப்புகள் பகிரப்பட்டன.`, `നന്ദി: ${n} അടയാളങ്ങൾ പങ്കിട്ടു.`));
  } catch (err) {
    notify(errorText(err.message));
  }
}

// The owner's accuracy report of shared marks (Tools page)
function renderAccuracyCard() {
  const box = document.getElementById('accuracy-card');
  if (!box) return;
  box.innerHTML = `
    <div class="card-header"><div>
      <h2>${esc(txt('Accuracy report', 'துல்லிய அறிக்கை', 'കൃത്യതാ റിപ്പോർട്ട്'))}</h2>
      <p class="card-subtitle">${esc(txt('For the owner: how often each kind of statement was marked right, from the marks people shared in Chart Verification.',
        'உரிமையாளருக்கு: ஜாதகப் பரிசோதனையில் பகிரப்பட்ட குறிப்புகளின்படி ஒவ்வொரு வகைக் கூற்றும் எவ்வளவு முறை சரியாக இருந்தது.',
        'ഉടമയ്ക്ക്: ജാതക പരിശോധനയിൽ പങ്കിട്ട അടയാളങ്ങൾ പ്രകാരം ഓരോ തരം പ്രസ്താവനയും എത്ര തവണ ശരിയായി.'))}</p>
    </div><span class="card-badge">📊</span></div>
    <div class="muhurtham-controls">
      <input type="password" id="owner-passcode" autocomplete="off" placeholder="${esc(txt('Owner passcode (not needed on this computer)', 'உரிமையாளர் கடவுக்குறி (இந்தக் கணினியில் தேவையில்லை)', 'ഉടമ പാസ്‌കോഡ് (ഈ കമ്പ്യൂട്ടറിൽ ആവശ്യമില്ല)'))}">
      <button type="button" class="action-btn" id="accuracy-run">${esc(txt('Show report', 'அறிக்கையைக் காட்டு', 'റിപ്പോർട്ട് കാണിക്കുക'))}</button>
    </div>
    <div id="accuracy-result"></div>`;
  $('#accuracy-run').addEventListener('click', loadAccuracyReport);
}

async function loadAccuracyReport() {
  const out = $('#accuracy-result');
  try {
    const resp = await fetch('/api/feedback-report', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ passcode: $('#owner-passcode').value })
    });
    const r = await resp.json();
    if (!resp.ok) throw new Error(r.error || 'The report could not be loaded.');
    const pct = v => v == null ? '—' : `${v}%`;
    const tableHtml = (head, rows) => `<div class="table-responsive"><table class="luxury-table"><thead><tr>${head.map(h => `<th>${esc(h)}</th>`).join('')}</tr></thead>
      <tbody>${rows.map(row => `<tr>${row.map(c => `<td>${esc(String(c))}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
    out.innerHTML = `<p class="muted">${esc(txt(`${r.entries} people have shared their marks.`, `${r.entries} பேர் குறிப்புகளைப் பகிர்ந்துள்ளனர்.`, `${r.entries} പേർ അടയാളങ്ങൾ പങ്കിട്ടു.`))}</p>`
      + (r.statements.length ? tableHtml([txt('Statement', 'கூற்று', 'പ്രസ്താവന'), txt('Right', 'சரி', 'ശരി'), txt('Wrong', 'தவறு', 'തെറ്റ്'), '%',
          txt('Dates given', 'தேதிகள்', 'തീയതികൾ'), txt('In window', 'காலத்துக்குள்', 'കാലത്തിനുള്ളിൽ'), txt('In months', 'மாதங்களுக்குள்', 'മാസങ്ങൾക്കുള്ളിൽ')],
        r.statements.map(s => [s.key, s.right, s.wrong, pct(s.right_pct), s.dated, pct(s.in_window_pct), pct(s.in_months_pct)])) : '')
      + (r.confidence.length ? tableHtml([txt('Confidence', 'நம்பகத்தன்மை', 'ഉറപ്പ്'), txt('Right', 'சரி', 'ശരി'), txt('Wrong', 'தவறு', 'തെറ്റ്'), '%'],
        r.confidence.map(c => [c.level, c.right, c.wrong, pct(c.right_pct)])) : '')
      + (r.siblings.length ? tableHtml([txt('Siblings', 'உடன்பிறப்புகள்', 'സഹോദരങ്ങൾ'), txt('People', 'நபர்கள்', 'ആളുകൾ'),
          txt('Exact', 'சரியாக', 'കൃത്യം'), txt('Total right', 'மொத்தம் சரி', 'ആകെ ശരി')],
        r.siblings.map(s => [s.group, s.count, pct(s.exact_pct), pct(s.total_pct)])) : '');
  } catch (err) {
    out.innerHTML = `<p class="muted">${esc(errorText(err.message))}</p>`;
  }
}
