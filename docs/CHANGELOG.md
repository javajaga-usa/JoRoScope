# JoRoScope Changelog

## [2.3.0] - 2026-09-28

### Malayalam readings
- Every reading now has Malayalam: natal, the twelve bhavas, planets in houses, the Dasa-Bhukti forecast and all 81 periods of the timeline, transits, lucky factors, yogas and their cancellations, Bhrigu Nandi Nadi, avasthas, nakshatra pada, sahams, Panchanga Phala, Sudarshana Chakra, Shadbala and Vimsopaka, the KP cusps, Jaimini karakas and arudhas, D-10 career, Ayur-Jyotish, double transit, kakshya transits, the doshas, and every report chapter (Parihara, monthly transits, Varshaphal, marriage, career, Sarvatobhadra and Kota, numerology).
- Tools in Malayalam too: Prasna, birth time rectification and the Muhurtham finder.
- The chart sends Malayalam only when the page is in Malayalam, so English and Tamil charts stay small; switching to Malayalam fetches the chart again.
- In Malayalam, the second label beside a sign shows English instead of Tamil, and the "readings appear in English" notice is gone.
- A new test checks that no Tamil reading in a chart lacks its Malayalam.

## [2.2.0] - 2026-09-28

Reports in the style of Astro-Vision's, a Tools page for Prasna and birth time rectification, and Malayalam.

### New report chapters (Life Predictions page and the Complete print report)
- **Parihara (remedies):** remedies drawn from what the chart shows: Chevvai, Kaal Sarp and Rahu-Ketu doshams, a running Sade Sati, Ashtama or Kandaka Sani, grahas below their required Shadbala or debilitated, the running dasa lords and difficult yogas. Each graha's Navagraha temple in Tamil Nadu, deity, day, beeja mantra with its japa count, charity and fasting.
- **Monthly transits:** the next twelve months from the Moon sign, with the Vedha (obstruction) rule, Ashtakavarga bindus, dated sign changes and Chandrashtamam days; months ranked for the chart.
- **Varshaphal (annual horoscope):** the Tajika chart for the Sun's return (matches PyJHora's Varsha Pravesh to the minute), Muntha, the lord of the year from the five office-bearers and Pancha-vargeeya Bala, Ithasala promises for wealth, marriage, career and other matters, and the Mudda Dasa.
- **Marriage (Kalatra) and career reports:** the 7th and 10th houses, their lords, occupants and aspects, the karakas, Darakaraka, Upapada, Amatyakaraka and the Navamsa and Dasamsa, with the Dasa-Bhukti periods that bring them and the double-transit windows.
- **Sarvatobhadra and Kota Chakra:** today's transit Vedha on the birth star, its special stars and the birth sign, drawn on the 9 x 9 chakra; the Kota Chakra's rings with malefics entering or leaving the fort.
- **Numerology:** Chaldean birth, destiny and name numbers, their ruling grahas and whether they agree.

### Tools page
- **Prasna (horary):** a chart for the moment the question is asked, judged by Prasna Marga (Shirshodaya Lagna, Mandi, benefics and malefics in the kendras, the Moon) and Tajika (Ithasala between the Lagna lord and the lord of the matter), with an optional Arudha number and a timing estimate.
- **Birth time rectification:** candidate times around the stated one are tested against dated life events by their Dasa, Bhukti and Pratyantar lords and Saturn-Jupiter double transits; candidates are grouped by Lagna and Navamsa and ranked. It narrows the time; an astrologer confirms it.

### Also
- **Malayalam:** the language button cycles English, Tamil and Malayalam. The interface, astrological names (signs, stars, grahas, weekdays, tithis, yogas, karanas, months) and labels are in Malayalam; long readings stay in English until translated.
- **Calendar export:** muhurthams, the month's observances and Chandrashtamam periods download as .ics files for phone and desktop calendars.
- **Printing:** long tables print in chunks that each carry their header row, as Safari does not repeat table headers.
- New API routes `/api/prasna` and `/api/rectify`; a markup test checks that element ids are unique and every interface key has English, Tamil and Malayalam text.

## [2.1.0] - 2026-09-28

The South Indian (Tamil) jathagam release: Tamil calendar and panchangam, accurate Shadbala, about 75 classical yogas, KP, Jaimini (arudhas, Chara Dasa), Ashtottari Dasa, a Muhurtham finder with Tamil yogam and Lagna Shuddhi, chart-specific Dasa-Bhukti ratings, Sri Lankan charts, a restructured print report checked on paper, safer profile backups, one-click launchers for macOS and Windows, and a faster, smaller chart response.

### Printing checked on paper (WebKit PDF)
- The report title printed near-white when the app was in the dark theme; it now prints black.
- The Lagna corner mark in South Indian charts printed as a solid black square hiding the sign name (a gradient with transparent stops); it is now a thin line.
- Shodasavarga charts could be cut in half at a page break; they are now laid out so each chart stays whole, with a gap between them.
- North Indian and Sri Lankan charts use larger text on paper.
- `scripts/print_pdf.swift` prints any report and chart style to PDF through WebKit on macOS for checking layouts.

### Code structure
- `core/predictions.py` (2,600 lines) is split into `core/readings/`: `common`, `life`, `jaimini`, `timing`, `career_health`, `strength_kp` and `classical`. `predictions.py` now only assembles the report and re-exports the old names, so existing imports keep working; the report output is byte-identical.
- `web/app.js` (4,500 lines) is split into `i18n.js`, the core `app.js`, and one script per page: `chart-views.js`, `dasa.js`, `readings.js`, `panchangam.js`, `matching.js` and `profiles-ui.js`. CI syntax-checks every script in `web/`.

### Safer profile backups
- Profile backups carry the app name, format version, export time and count. Import accepts these, older backups and bare lists of profiles.
- Every imported profile is checked (name, a real calendar date, time, latitude and longitude) and reduced to the known fields; bad entries are skipped and named in the summary, which also counts new, updated and already-saved profiles.
- A newer copy of a saved person (same id, or same name, date and time) replaces the older one instead of being ignored. Files from other applications are refused.
- The backup logic lives in `web/profiles.js` with its own Node test.

### Chart styles on screen and in print
- Sri Lankan (Sinhala kendaraya) chart: the diamond drawing with the Lagna at the top and the houses running clockwise.
- The print dialog has a chart style: South Indian (also the Kerala layout), North Indian, East Indian or Sri Lankan. Every chart in the report, including the Shodasavarga pages, uses it, drawn black on white.
- North Indian and Sri Lankan charts put the sign numbers at the inner corners and wrap the grahas onto several lines, so crowded houses stay legible; the Lagna house is shaded.

### Windows launcher
- `Launch.ps1` and `Start JoRoScope.cmd` now work like the macOS launcher: they find Python 3.11 or newer (the `py` launcher, then `python`), create a private `.venv` and install the requirements on the first run, then start the server. They no longer look for a developer-machine runtime under `.cache\codex-runtimes` or require exactly Python 3.12.

### Faster chart loading
- The chart response keeps the six detailed readings (career, wealth, health, family, milestones, remedy) only for the running Dasa-Bhukti; the other 80 periods' readings load from the new `/api/timeline` endpoint the first time a card is opened.
- JSON responses are gzip-compressed when the browser accepts it. A chart now transfers about 80 KB instead of about 950 KB.

### Ashtottari and Jaimini Chara Dasa, and the dasa year
- Ashtottari Dasa (108 years, eight lords counted from Ardra) with bhuktis from the Dasa lord, and whether its classical condition (Rahu in a kendra or trikona from the Lagna lord) holds. Dates match PyJHora.
- Jaimini Chara Dasa by K.N. Rao's method: signs from the Lagna in the direction the 9th sign sets, each sign's years from its distance to its lord (the stronger lord for Scorpio and Aquarius), a second round of 12 less the first, and twelve antardasas ending with the dasa sign. It matches PyJHora on 35,548 of 36,000 random sign periods; the differences are Mercury in Virgo (counted as exalted here) and the choice of the stronger co-lord (P.V.R. Narasimha Rao's rules, as for the arudhas).
- A Dasa Year setting in the birth form: 365.25 days (default, South Indian almanacs), the sidereal year (Jagannatha Hora) or the 360-day Savana year. It applies to Vimshottari, Yogini, Ashtottari and Chara Dasa and is saved with each profile.
- New Ashtottari and Chara views on the Dasa page, and an "Ashtottari & Chara Dasa" section in the Detailed and Complete print reports. The dasa view switcher now wraps and follows the light theme.

### Tamil Yogam and Lagna in the Muhurtham finder
- Amirthathi (Tamil) yogam: Siddha, Amirtha, Marana or Prabalarishta from the weekday and nakshatra, by the table Tamil calendars print (cross-checked with PyJHora; Monday + Purattathi as in the Sringeri Tamil Panchangam). The daily Panchangam shows it with its end time and the yogam that follows.
- Muhurthams now require Siddha or Amirtha yogam and a clean rising Lagna: no malefic in the 8th, the Moon not in the 6th, 8th or 12th, and not the person's Janma Ashtama rasi. Windows split at each Lagna change and name it; notes flag Jupiter or Venus in a kendra, a clear 7th for marriage and a fixed Lagna for griha pravesam.

### Chart-specific Dasa-Bhukti timeline
- Each Dasa-Bhukti rating now weighs the two lords' house lordships in this chart (kendra/trikona against dusthana, with Vipareeta cases), their dignity and their natural relationship; Rahu and Ketu act through their dispositors. The reason opens every reading in Tamil and English.
- The ten-year view scores each year from its running period, less a little under Sade Sati or Ashtama Sani, instead of a year-based variation; the icon follows the Bhukti lord.
- Swabhukti periods are named as such instead of repeating the lord.
- Gemstones: the fortune stone is now always the 9th lord's (corrected for Cancer, Leo and Pisces Lagnas, with their days and fingers), and the card states the basis and cautions against stones of the 6th, 8th and 12th lords.

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
- **Navamsa (D9) table** on the chart page: each graha's Navamsa sign, amsa number, lord and dignity there, with Vargottama and Pushkara Navamsa. It sits beside a full **Shodasavarga table** (every graha in all 16 vargas).
- Fixed the "ready to calculate" placeholder staying on screen after a chart was calculated: a component's display rule overrode the `hidden` attribute. The chart page now stacks below 1100px so the Rasi and Navamsa charts are no longer clipped.
- **Bhava Bala** (BPHS): Bhavadhipati, Bhava Dig and Bhava Drishti Bala for the twelve Sripati bhavas. Each house reading now weighs its Bhava Bala against the 7-rupa minimum.
- **Shodasavarga** is complete with D40 (Khavedamsa) and D45 (Akshavedamsa). All 16 vargas match PyJHora across 20,000 longitudes; the only exception is D2, where we keep the Parashara Sun/Moon hora.
- **Vimsopaka Bala and Varga Bheda** in the Shadvarga, Saptavarga, Dasavarga and Shodasavarga schemes (BPHS weights), with dignity names from Parijatamsa to Sri Vallabhamsa.
- **Sodhita Ashtakavarga and Sodhya Pinda:** Trikona and Ekadhipatya reductions with Rasi, Graha and Sodhya Pindas. These reproduce P.V.R. Narasimha Rao's worked Charts 7 and 11 exactly. PyJHora misses Chart 7 because of a Virgo multiplier of 6 (the classical value is 5) and its rule for equal counts.
- **Jathaga Kurippu** additions: Yogi, Duplicate Yogi and Avayogi; Dagdha Rasi; Chandra Avastha, Vela and Kriya; Moudhyam; and Graha Yuddha. These also appear on the printed Jathagam.
- **Panchanga Phala:** readings for the birth weekday (day lord), tithi (Nanda, Bhadra, Jaya, Rikta or Purna class and presiding deity, with Tamil observances such as Pradosham, Ekadasi and Amavasai tarpanam), nitya yoga (meaning, and the nine difficult yogas) and karana. This replaces a generic Sun-and-tithi paragraph. Vishkambha is now correctly listed among the difficult yogas.
- **Sudarshana Chakra:** the houses counted from the Lagna, the Moon and the Sun, and the house the current year of life activates.
- **Muhurtham finder** (`/api/muhurtham` and the Panchangam page): daytime windows for marriage, griha pravesam, a business opening, a vehicle purchase or any auspicious start. It applies the Muhurta Chintamani rules: event nakshatras; Sunday to Friday except Tuesday; good tithis; the difficult nitya yogas avoided in their inauspicious ghatis; no Vishti karana; Rahu Kalam, Yamagandam and Gulika cut out exactly; and no Aadi, Purattasi or Margazhi for marriage and griha pravesam. With a chart loaded it also applies Tara and Chandra Bala and leaves out Chandrashtamam days.
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

### Yogas: about 75 classical combinations
- A new `yogas.py` covers:
  - the Pancha Mahapurusha yogas;
  - the Chandra yogas (Sunapha, Anapha, Durudhara, Kemadruma and its cancellation, Adhi, Gaja Kesari with Raman's conditions, Chandra-Mangala, Sakata, Vasumati);
  - the Surya yogas (Vesi, Vasi, Ubhayachari, Budhaditya, noting a combust Mercury);
  - Raja yogas from kendra and trikona lords, the Yogakaraka, Dharma-Karmadhipati and Dhana yogas;
  - the named yogas: Lakshmi, Saraswati, Parvata, Kahala, Chamara, Sankha, Bheri, Guru-Mangala, Amala, Lagnadhi, and Shubha and Papa Kartari;
  - Maha, Khala and Dainya Parivartana, the three Vipareeta Raja yogas, and Neechabhanga with all its classical cancellations named;
  - the challenging combinations: Guru Chandala, Grahana, Angaraka, Punarphoo and Daridra;
  - all 32 Nabhasa yogas.
- Every yoga has Tamil and English names and readings, a category, and a nature (auspicious, mixed, challenging or cancelled). The yogas are ordered and coloured by nature.
- Checked against PyJHora on 3,000 random charts. Where they differ it is by documented convention: we exclude the nodes from the Surya, Chandra and Nabhasa yogas as BPHS does; Sunapha, Anapha and Durudhara are mutually exclusive; and we follow Raman's text where PyJHora departs from its own documentation.

### Print and PDF, restructured
- A print dialog offers three presets modelled on current tools; every section can also be switched on or off, and the report prints in Tamil or English whatever language the app shows.
  - **Traditional Jathagam** (about 3 pages, like Prokerala's basic report and the sheet Tamil families share).
  - **Detailed Horoscope**, which adds the tables AstroSage's PDF carries: Navamsa and Shodasavarga charts and tables, the Sripati Bhava table, Shadbala, Bhava Bala and Vimsopaka, Ashtakavarga with Sodhya Pinda, and KP.
  - **Complete Report**, which adds the readings, as Astro-Vision's reports do: Panchanga Phala, birth star and Lagna, the running dasa, Sudarshana, transits, career, health and the twelve bhavas.
- A4 layout: a formal header with a contents line, numbered section bands, every major section on a fresh page, repeating table headers, and charts that fit the page in both languages. A running header and page numbers print where the browser supports CSS page margin boxes (Chrome and Edge 131+). Colours are tuned for paper.
- The header Print button prints the Porutham report on the matching page and the page itself on the Panchangam and Profiles pages. Elsewhere it opens the report dialog instead of printing the web interface.
- The Porutham report shares the new layout.
- `esc()` now turns `<` into `&lt;`; it was being shown as `>`.

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
