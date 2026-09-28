# JoRoScope Architectural Specification

JoRoScope is a modern, high-precision Vedic astrology suite calculated using the Swiss Ephemeris AGPL. It is architected for 100% offline privacy, zero cloud dependency, and multi-system astrological analysis.

---

## 1. System Architecture Overview

```
┌────────────────────────────────────────────────────────┐
│                   Frontend Client                      │
│   (HTML5 SPA · CSS Cosmic Luxury · Vanilla ES6+)       │
│                                                        │
│  - Multi-Person Profile Manager (Local Vault)          │
│  - South / North / East Indian SVG Chart Renderers    │
│  - Interactive House & Planet Inspector                │
│  - 17 Prediction Chapters Tab View                     │
│  - Horoscope Compatibility Matcher (10 Poruthams)      │
│  - Full Bilingual Engine (English & தமிழ்)             │
└───────────────────────────┬────────────────────────────┘
                            │ HTTP JSON / REST
┌───────────────────────────▼────────────────────────────┐
│              JoRoScope Local HTTP Server               │
│                  (joroscope.server)                    │
│                                                        │
│  - Endpoints: /api/chart, /api/match, /api/panchangam  │
│  - Strict Origin & Size Validation                     │
│  - Static Asset Delivery                               │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│            Core Astronomical & Vedic Engine            │
│               (joroscope.core.engine)                  │
│                                                        │
│  - Swiss Ephemeris C-Bridge (pyswisseph 2.10)          │
│  - IANA Timezone Conversion & DST Clock Folds          │
│  - 14 Divisional Vargas (D1, D2, D3, D4, D7, D9...)   │
│  - 3-Tier Vimshottari Dasa-Bhukti-Antardasa            │
│  - Parashara Ashtakavarga (BAV & SAV Matrices)         │
│  - Classical Yoga & Dosha Pattern Matcher              │
│  - 10 Poruthams & 36 Guna Milan Engine                 │
│  - Swiss Ephemeris Sunrise/Sunset & Local Panchangam   │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│          South Indian (Tamil) Jathagam Module          │
│             (joroscope.core.south_indian)              │
│                                                        │
│  - Tamil Calendar, Vaaram & Udayadi Nazhigai           │
│  - Dasa Irruppu & Mandi (Prasna Marga)                 │
│  - Chevvai, Rahu-Ketu Doshams & Papa Samyam            │
│  - Tamil Daily Panchangam (end times, Soolam, Balam)   │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│               Prediction & Sutra Engine                │
│            (joroscope.core.predictions)                │
│                                                        │
│  - Shadbala 6-Fold Planetary Strength & Dominance      │
│  - Krishnamurti Paddhati (KP) 249 Sub-Lord System      │
│  - Bhrigu Nandi Nadi (BNN) Karmic Planetary Sutras     │
│  - Baladi & Jagradadi Planetary Avasthas               │
│  - 108 Nakshatra Pada-by-Pada Destiny Readings        │
│  - Tajika & Parashara Sensitive Sahams (Cosmic Lots)   │
│  - Gochara (Transit) & Remedial Gemstones Guidance     │
└────────────────────────────────────────────────────────┘
```

---

## 2. Directory Structure

- `src/joroscope/`
  - `core/`: Core mathematical calculations and predictions.
  - `web/`: Frontend Single Page Application and astronomical city database.
  - `server.py`: Local web server daemon.
  - `cli.py`: Command-line interface.
- `tests/`: Automated unit and integration test suites.
- `scripts/`: Packaging, executable build, and data preparation utilities.
- `docs/`: In-depth documentation and references.
- `licenses/`: Open-source licensing documentation.
- `vendor/`: Swiss Ephemeris data files.

---

## 3. Astrological Calculations & Methodologies

### Ephemeris Precision
- Swiss Ephemeris version 2.10 provides sub-arcsecond accuracy across 1800 CE – 2200 CE.
- Topocentric and geocentric calculations with Lahiri (Chitra Paksha), Raman, Krishnamurti (KP), and Fagan-Bradley Ayanamsas.

### 14 Parashara Divisional Vargas
1. **D1 (Rasi)**: Physical reality, overall vitality.
2. **D2 (Hora)**: Wealth, liquid assets, resources.
3. **D3 (Drekkana)**: Courage, siblings, enterprise.
4. **D4 (Chaturthamsa)**: Fixed assets, home, vehicles.
5. **D7 (Saptamsa)**: Progeny, creative legacy.
6. **D9 (Navamsa)**: Dharma, spouse, inner potential.
7. **D10 (Dasamsa)**: Profession, career authority, status.
8. **D12 (Dvadasamsa)**: Ancestry, parents, lineage karma.
9. **D16 (Shodasamsa)**: Conveyances, luxuries, happiness.
10. **D20 (Vimsamsa)**: Spiritual progress, devotion, upasana.
11. **D24 (Chaturvimsamsa)**: Higher learning, analytical intellect.
12. **D27 (Saptavimsamsa)**: Subconscious strengths and vulnerabilities.
13. **D30 (Trimsamsa)**: Karmic afflictions, character resilience.
14. **D60 (Shashtiamsa)**: Past-life karma and ultimate destiny.

### 17 Prediction Chapters
- **Shadbala (Virupas & Rupas)**: `core/shadbala.py` computes Positional, Directional, Temporal, Motional, Natural and Aspectual strengths per BPHS, as worked in B.V. Raman's *Graha and Bhava Balas* (checked by `tests/test_shadbala.py`). The engine runs it over the Vedic day of birth, and `predictions.calculate_shadbala` interprets the result.
- **KP Sub-Lords**: Exact division of each constellation into unequal planetary sub-rulers according to Vimshottari proportions.
- **Bhrigu Nandi Nadi**: Conjunctions and 1-5-9 directional trinal alignments (Dharma, Artha, Kama, Moksha).
- **Planetary Avasthas**: Baladi (Bala, Kumara, Yuva, Vriddha, Mrita) and Jagradadi (Jagrat, Swapna, Sushupti).
- **Nakshatra Padas**: 108 Pada-specific destiny analysis.
- **Sensitive Sahams**: Punya, Vidya, Vivaha, Karma, Roga Sahams.
