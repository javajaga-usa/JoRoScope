# JoRoScope Changelog

## [Unreleased]

### South Indian (Tamil) Jathagam
- New `joroscope.core.south_indian` module: Tamil calendar (60-year cycle, month and date by the sunset rule), Vaaram, Udayadi Nazhigai, Dasa Irruppu, Mandi, Chevvai and Rahu-Ketu Doshams, Papa Samyam, and a Tamil daily panchangam.
- Chart API adds `south_indian` (Jathaga Kurippu) and `doshas.chevvai` / `doshas.rahu_ketu`; `/api/match` adds `dosha_samyam` when full birth details are sent.
- South Indian chart: Tamil abbreviations, Lagna diagonal, Mandi, degrees, Dasa balance in the centre, and a Rasi + Navamsa view.
- Daily Panchangam page now shows today's (or any date's) panchangam for the form location instead of the birth moment.
- Hora (Orai) table with the current hora, upcoming Chandrashtamam periods, and the next Nakshatra birthday.

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
