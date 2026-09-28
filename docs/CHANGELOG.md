# JoRoScope Changelog

## [Unreleased]

### macOS launcher
- `Start JoRoScope.command` starts the app with a double-click on macOS: it finds Python 3.11+, sets up a private `.venv` with the Swiss Ephemeris on first run, and opens the browser.

### South Indian (Tamil) Jathagam
- New `joroscope.core.south_indian` module: Tamil calendar (60-year cycle, month and date by the sunset rule), Vaaram, Udayadi Nazhigai, Dasa Irruppu, Mandi, Chevvai and Rahu-Ketu Doshams, Papa Samyam, and a Tamil daily panchangam.
- Chart API adds `south_indian` (Jathaga Kurippu) and `doshas.chevvai` / `doshas.rahu_ketu`; `/api/match` adds `dosha_samyam` when full birth details are sent.
- South Indian chart: Tamil abbreviations, Lagna diagonal, Mandi, degrees, Dasa balance in the centre, and a Rasi + Navamsa view.
- Daily Panchangam page now shows today's (or any date's) panchangam for the form location instead of the birth moment.
- Hora (Orai) table with the current hora, upcoming Chandrashtamam periods, and the next Nakshatra birthday.

### Benchmark gaps closed (vs Jagannatha Hora / PyJHora, Astro-Vision, Prokerala, Drik Panchang)
- Gowri Panchangam (Nalla Neram) for day and night, matching Drik Panchang's published weekday tables.
- Sripati Bhava Chakra: bhava madhyas by Porphyry trisection, sandhis midway; shown as a "Bhava" chart and a planets-table column.
- Lifetime Saturn cycles: Ezharai Sani with its three phases, Ardhashtama, Kandaka and Ashtama Sani from the natal Moon, found by sweeping Saturn's exact sign changes.
- Printable Porutham report; the match verdict drops one step when Chevvai or Papa Samyam is unbalanced or a Dasa Sandhi falls, and says why.
- Full-chart matches correct saved profiles whose stored star or sign was wrong.
- Monthly Tamil calendar with observance days; every rule reproduces Drik Panchang's Chennai dates for 2025 and 2026 (Ekadasi 49/49, Pradosham 49/49), enforced by tests.
- Upagrahas: Gulika, Kaala, Mrityu, Artha Praharaka, Yama Ghantaka (Jagannatha Hora conventions) and the Dhuma group (BPHS).
- Yogini Dasa with bhuktis, its star mapping checked against PyJHora.
- Dasa Sandhi in matching: Maha Dasa changes of bride and groom within 182 days of each other over the next 30 years.

### Accurate Shadbala
- New `joroscope.core.shadbala` module computes every classical component: Uchcha, Saptavargaja (compound relationships over D1/D2/D3/D7/D9/D12/D30), Ojayugma, Kendradi, Drekkana; Dig from the Sripati bhava madhyas; Nathonnatha from apparent midnight, Paksha, Tribhaga, Abda and Masa from the Kali ahargana, Vara, Hora, Ayana from the kranti, and Graha Yuddha; Cheshta from B.V. Raman's mean-longitude tables; and Drik from sphuta drishti.
- Reproduces B.V. Raman's *Graha and Bhava Balas* example and V.P. Jain's example within one virupa per component. The only differences are documented where a book goes beyond BPHS: a Dig Bala above the classical 60, and Moolatrikona taken over the whole sign.
- The Shadbala chapter adds Ishta and Kashta Phala, the reasons behind each graha's strength, and a full component breakdown in Tamil and English.
- Replaces the earlier approximation: sign-distance Saptavargaja, a wrong Mercury/Saturn Ojayugma, Kaala Bala with only three parts, speed-bucket Cheshta and ±15 aspect Drik.

### Astro-Vision (LifeSign) parity
- **Bhava Bala** (BPHS): Bhavadhipati, Bhava Dig and Bhava Drishti Bala for the twelve Sripati bhavas. Each house reading now weighs its Bhava Bala against the 7-rupa minimum.
- **Shodasavarga** is complete with D40 (Khavedamsa) and D45 (Akshavedamsa). All 16 vargas match PyJHora across 20,000 longitudes; the only exception is D2, where we keep the Parashara Sun/Moon hora.
- **Vimsopaka Bala and Varga Bheda** in the Shadvarga, Saptavarga, Dasavarga and Shodasavarga schemes (BPHS weights), with dignity names from Parijatamsa to Sri Vallabhamsa.
- **Sodhita Ashtakavarga and Sodhya Pinda:** Trikona and Ekadhipatya reductions with Rasi, Graha and Sodhya Pindas. These reproduce P.V.R. Narasimha Rao's worked Charts 7 and 11 exactly. PyJHora misses Chart 7 because of a Virgo multiplier of 6 (the classical value is 5) and its rule for equal counts.
- **Jathaga Kurippu** additions: Yogi, Duplicate Yogi and Avayogi; Dagdha Rasi; Chandra Avastha, Vela and Kriya; Moudhyam; and Graha Yuddha. These also appear on the printed Jathagam.
- **Jaimini Arudha padas** (A1–A12, AL and UL) with PVR's stronger co-lord rules for Scorpio and Aquarius. They agree with PyJHora on every chart once two PyJHora bugs are reproduced. Adds readings for gains and losses from the AL and marital continuity from the UL.

### Prediction chapters audited for accuracy
- **KP:** positions and Placidus cusps now always use the Krishnamurti ayanamsa, and sub-lords are computed in exact arc-minutes. The sub-lord matches PyJHora at more than 500,000 test longitudes. Cusp readings now use real significators (the houses occupied and owned by the sub-lord's star lord and by the sub-lord itself), check them against the houses that promise or negate each matter, and give a verdict. KP ruling planets at birth are added.
- **Sahams:** Karma (Mars − Mercury) and Roga (Lagna − Moon) now use the Tajika Neelakanthi formulas. Night reversals and the 30° rule are applied, and day or night is taken from the Sun's position above the horizon. Putra, Artha, Vanika and Samartha sahams are added. Artha, Samartha and Vanika reproduce P.V.R. Narasimha Rao's worked Chart 66, and each saham is judged by its lord.
- **Kakshya:** a kakshya is fruitful only when its own lord gave a bindu. The rule is read from the new prastara (per-contributor) Ashtakavarga; before, the first *n* kakshyas were marked fruitful.
- **Nakshatra pada:** the Moon's Navamsa sign and pada lord were always shown as Aries and Mars; they now follow the chart.
- **Double transit:** follows K.N. Rao's rule that transit Saturn and Jupiter must both reach the house or its lord while the running dasa is connected with the matter. Dated windows are listed for the next six years, each checked against its dasa.
- **Career:** Varahamihira's Karmajeeva rule (strongest of Lagna, Moon and Sun, then the 10th lord's Navamsa lord) with D-10 dignity, replacing points for arbitrary Dasamsa signs.
- **Avasthas:** adds BPHS Lajjitadi states (Lajjita, Garvita, Kshudita, Trushita, Mudita, Kshobhita).
- **Bhrigu Nandi Nadi:** adds the missing conjunction, opposition and 2nd/12th links, and the rule that a retrograde graha also acts from the previous sign. Adds Saturn- and Moon-based sutras, ranked by link strength.
- **Ayur:** prakriti now comes from the Lagna, its lord, the Moon and the grahas on the Lagna, using BPHS graha doshas; before, a fixed set of planet points was added to every chart. Adds a health watch for the 6th and 8th houses.
- **Jaimini:** results for grahas in the Karakamsa (Upadesa Sutras) and for Ketu in the 12th from it.
- The Ashtakavarga tables were checked against BPHS and B.V. Raman: Moon from Mars 2, 3, 5, 6, 9, 10, 11 and Venus from Mars 3, 5, 6, 9, 11, 12, with totals 48/49/39/54/56/52/39. Unchanged.

### Printable Jathagam
- One click prints a traditional horoscope sheet in the chosen language: birth details and Tamil notes, Rasi and Navamsa side by side, planetary positions, doshas and yogas, and the full Dasa-Bhukti table.
- Dasa-Bhukti dates everywhere are calendar dates at the birthplace; they were UTC dates, a day early for boundaries after 18:30 UTC in India.

### Detailed Predictions
- 12 Bhava readings are chart-specific: lord dignity and placement (with Vipareeta for dusthana lords), benefic and malefic occupants, Jupiter/Saturn/Mars aspects and Ashtakavarga bindus produce a strength verdict and a list of contributing factors.
- Planet readings weigh dignity, functional lordship from the Lagna (Yogakaraka, functional benefic or malefic), Dig Bala, combustion, retrogression and Jupiter's aspect.
- The active Dasa-Bhukti reading explains what each lord rules and occupies and how the two lords relate.

### Tamil & English
- Every static label, tooltip, placeholder, chart, table, reading, yoga, dosha, porutham, toast and error message switches language; engine output carries Tamil for all generated text; the language choice persists.

### Gochara (Transits)
- Transits are computed live from Swiss Ephemeris in the chart's ayanamsa (`gochara` in the chart API), with Ashtakavarga bindus and Phaladeepika house results for all nine grahas.
- Upcoming Peyarchi (sign change) dates for Saturn, Jupiter and Rahu-Ketu, and a Rahu-Ketu transit reading.

### Fixes
- The Gochara chapter used hard-coded 2024 positions for Saturn, Jupiter, Rahu and Ketu, so Sade Sati, Ashtama Sani and Guru Balam were wrong.
- Prediction modules reset the global ayanamsa to Lahiri, so the reported ayanamsa was Lahiri's for Raman, KP and Fagan-Bradley charts.
- Charts crashed with the PyPI `pyswisseph` build, which returns 12 house cusps instead of 13.
- Panchangam used the UTC weekday and an approximate sunrise; it now uses the local date and Swiss Ephemeris rise/set, and reports local times.
- Vedha Porutham pairs (8 of 13 were wrong), Dina Porutham counts and same-star rules, Nadi and Varna tables in Guna Milan.
- Divisional charts numbered houses from the Rasi Lagna instead of their own Lagna.
- The South Indian grid stayed visible after switching chart styles.
- Seed profiles carried incorrect stars and signs.
- The standalone executable served 404 for the whole UI: web assets were bundled outside the package.
- The East Indian chart was blank; it now has its own renderer (fixed signs, Aries at the top, anticlockwise).
- D30 Trimsamsa placed the Venus portion of odd signs in Taurus instead of Libra.
- Guna Milan: Bhakoot scored 5/9 as good and same-rasi as bad; Tara and Graha Maitri looked at only one partner.
- Choosing most non-Indian cities kept the previous timezone; the form now infers one and flags guesses to confirm.
- CI now also runs the Node frontend tests; dead code and unused imports removed across the package.

## [2.0.0] - 2026-09-12

### Architecture & Reorganization
- Reorganized codebase into professional Python package layout (`src/joroscope/`).
- Added modular core (`joroscope.core.engine`, `joroscope.core.predictions`).
- Added comprehensive unit and API integration test suite (`tests/`).
- Created standardized build and release scripts (`scripts/`).
- Integrated GitHub Actions CI workflow (`.github/workflows/ci.yml`).

### Features & Astrological Systems
- **Expanded to 17 In-Depth Prediction Chapters**:
  - Shadbala 6-Fold planetary potency with dominant planet detection.
  - Krishnamurti Paddhati (KP) 249 Sub-Lord cuspal analysis.
  - Bhrigu Nandi Nadi (BNN) Karmic Planetary Sutras & Trinal combinations.
  - Baladi and Jagradadi Planetary Avasthas with fruition delivery percentages.
  - 108 Nakshatra Pada-specific destiny readings.
  - Sensitive Sahams (Punya, Vidya, Vivaha, Karma, Roga).
- **Multi-Person Profile System**:
  - Quick Profile Selector on the Birth Form for 1-click loading and calculation.
  - Form Save & New/Clear action buttons for rapid multi-person data entry.
  - Enhanced Saved Profiles Vault with astrological badges (Lagna, Rasi, Star Pada).
  - Quick matchmaking shortcuts (`👦 Boy` / `👧 Girl`) directly from profile cards.
  - Complete JSON backup export and de-duplicating import.
- **Bilingual Engine**:
  - 100% authentic English and Tamil (தமிழ்) translation for all calculations, charts, predictions, and UI components.
- **Horoscope Matching**:
  - 10 Poruthams and 36 Guna Milan compatibility calculation with Rajju Dosha verification.
