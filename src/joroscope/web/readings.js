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
    $('#pred-star-title').textContent = isTa
      ? `ஜென்ம நட்சத்திரம்: ${ov.tamil_nakshatra} (${ov.nakshatra})`
      : `Birth Star: ${ov.nakshatra} (${ov.tamil_nakshatra})`;
    $('#pred-star-sub').textContent = isTa
      ? 'குணம், மனோபாவம் மற்றும் விதியின் தாக்கம்'
      : 'Core Character, Temperament & Destiny';
    $('#pred-star-text').textContent = isTa ? ov.nakshatra_pred_ta : ov.nakshatra_pred_en;

    // Lagna
    $('#pred-lagna-title').textContent = isTa
      ? `லக்னம் (உதய ராசி): ${ov.tamil_lagna} (${ov.lagna})`
      : `Ascendant (Lagna): ${ov.lagna} (${ov.tamil_lagna})`;
    $('#pred-lagna-sub').textContent = isTa
      ? 'உடல்வாகு, தலைமைப் பண்பு மற்றும் வாழ்க்கை திசை'
      : 'Body Constitution, Leadership & Life Path';
    $('#pred-lagna-text').textContent = isTa ? ov.lagna_pred_ta : ov.lagna_pred_en;

    // Moon Sign
    $('#pred-moon-title').textContent = isTa
      ? `சந்திர ராசி: ${ov.tamil_moon_sign} (${ov.moon_sign})`
      : `Moon Sign (Rasi): ${ov.moon_sign} (${ov.tamil_moon_sign})`;
    $('#pred-moon-sub').textContent = isTa
      ? 'உள்மன உணர்வுகள், சிந்தனை ஓட்டம் மற்றும் கற்பனை வளம்'
      : 'Emotional Landscape, Instincts & Mental Equanimity';
    $('#pred-moon-text').textContent = isTa
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
      $('#jaimini-karakamsha-title').textContent = isTa
        ? `காரகாம்சம்: ${jk.karakamsha.tamil_sign} (${jk.karakamsha.sign})`
        : `Karakamsha Lagna: ${jk.karakamsha.sign} (${jk.karakamsha.tamil_sign})`;
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
}

// Chapters that use the shared report shape: a tab and panel each, drawn by renderReportChapter
const REPORT_CHAPTERS = ['numerology', 'remedies'];
const VERDICT_PILLS = { good: ['success', 'Favourable', 'சாதகம்'], mixed: ['neutral', 'Mixed', 'கலப்பு'], bad: ['danger', 'Needs care', 'கவனம் தேவை'] };

function reportCardHtml(c) {
  const pill = c.verdict ? VERDICT_PILLS[c.verdict] : null;
  return `
    <div class="cosmic-card reading-card">
      <div class="reading-header">
        <span class="reading-icon">${esc(c.icon || '✦')}</span>
        <div>
          <h3>${esc(txt(c.title.en, c.title.ta))}</h3>
          ${c.sub && (c.sub.en || c.sub.ta) ? `<small class="muted">${esc(txt(c.sub.en, c.sub.ta))}</small>` : ''}
        </div>
        ${pill ? `<span class="status-pill ${pill[0]}">${txt(pill[1], pill[2])}</span>` : ''}
      </div>
      <p class="reading-body">${esc(txt(c.body.en, c.body.ta))}</p>
    </div>`;
}

function reportTableHtml(t) {
  return `
    <div class="cosmic-card report-table-card">
      <h3>${esc(txt(t.title.en, t.title.ta))}</h3>
      <div class="table-responsive">
        <table class="luxury-table">
          <thead><tr>${t.head.map(h => `<th>${esc(txt(h.en, h.ta))}</th>`).join('')}</tr></thead>
          <tbody>${t.rows.map(row => `<tr>${row.map(c => `<td>${esc(txt(c.en, c.ta))}</td>`).join('')}</tr>`).join('')}</tbody>
        </table>
      </div>
    </div>`;
}

function renderReportChapter(key, ch) {
  const panel = document.getElementById(`ppanel-${key}`);
  if (!panel) return;
  if (!ch) {
    panel.innerHTML = `<p class="muted">${txt('Not available for this chart.', 'இந்த ஜாதகத்திற்குக் கிடைக்கவில்லை.')}</p>`;
    return;
  }
  panel.innerHTML = `
    <div class="cosmic-card report-intro">
      <h2>${esc(txt(ch.title.en, ch.title.ta))}</h2>
      <p class="muted">${esc(txt(ch.intro.en, ch.intro.ta))}</p>
    </div>
    ${ch.tables.map(reportTableHtml).join('')}
    <div class="readings-grid">${ch.cards.map(reportCardHtml).join('')}</div>`;
}
