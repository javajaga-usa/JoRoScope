# JoRoScope Changelog

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
