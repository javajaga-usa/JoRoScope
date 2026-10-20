# Validation: what is checked, and against what

JoRoScope's calculations are checked by automated tests against published worked examples and almanacs. The tests run in CI on every change (`python -m unittest discover -s tests -v`, then the Node tests against a running server). This page lists the checks so that anyone can see what has been verified and reproduce it.

## Calculations

| Calculation | Checked against | Test |
|---|---|---|
| Planetary longitudes | Swiss Ephemeris 2.10.03 (Moshier) against a fixed J2000 reference; Moshier agrees with JPL DE431 within about 1″ for 1800–2200 | `tests/test_engine.py` |
| Shadbala: all 16 sub-balas, Graha Yuddha, Ishta/Kashta Phala | B.V. Raman, *Graha and Bhava Balas* (16 Oct 1918, 14:22:16 IST, Raman ayanamsa) and V.P. Jain's Shadbala (13 Sep 1981, 01:30 IST, Lahiri), value by value | `tests/test_shadbala.py` |
| Sodhita Ashtakavarga, Trikona and Ekadhipatya Sodhana, Sodhya Pinda | P.V.R. Narasimha Rao, *Vedic Astrology: An Integrated Approach*, Charts 7 and 11 (exact) | `tests/test_astrovision_parity.py` |
| Tajika Sahams | Narasimha Rao's worked chart | `tests/test_prediction_accuracy.py` |
| Varshaphal (Varsha Pravesh moment) | PyJHora annual chart: 2026-01-01 17:35:19 IST, to the minute | `tests/test_reports.py` |
| Ashtottari and Chara Dasa | PyJHora for real charts (Jupiter Ashtottari from 1983-10-07 02:26 IST) | `tests/test_dasas.py` |
| Yogini Dasa star lists | PyJHora | `tests/test_south_indian.py` |
| Amavasai, Pournami, Pradosham, Sashti, Ekadasi, Karthigai, Sankatahara Chaturthi, Masa Shivaratri | Drik Panchang's published Chennai dates for 2025 and 2026, every date | `tests/test_tamil_calendar.py` |
| Classical yogas (about 75) | Hand-built charts for the rules in BPHS, Phaladeepika and B.V. Raman's *Three Hundred Important Combinations* | `tests/test_yogas.py` |
| KP sub-lord boundaries | The 249 Krishnamurti sub divisions at their exact arc limits | `tests/test_prediction_accuracy.py` |
| Time zones and clock changes | IANA zoneinfo: India's 1942-45 war time (+06:30), Sri Lanka's 1996 and 2006 changes, DST gaps and folds | `tests/test_calcsheet.py`, `tests/test_engine.py` |
| Birth-time sensitivity search | Minute-by-minute brute force for two charts | `tests/test_calcsheet.py` |
| Moon phases, sankranti and eclipses on the panchangam page | Pournami 26 Oct 2026, Amavasai 9 Nov 2026, the annular solar eclipse of 6 Feb 2027 and the penumbral lunar eclipse of 20 Feb 2027 | `tests/test_trust.py` |

Things a person can check without any software are on the **Daily Panchangam** page under *Check these yourself*: sunrise and sunset, the Moon's illumination, the next new and full moon, the next sankranti and eclipses. They come from the same Swiss Ephemeris call that places the grahas in the chart.

## Inputs you can compare

The **Calculation sheet** on the chart page states every input the engine applied: the UTC offset in force on the birth date, UT and local mean time, the sunrise and sunset used, the sidereal time, the Lagna and Moon to the arc second, the ayanamsa value, the node convention (mean node) and house conventions (whole sign; Sripati bhavas; Placidus KP cusps in the Krishnamurti ayanamsa), the dasa year length, the Julian day and ΔT. *Export calculation sheet* downloads it with every graha's longitude for checking in another program. When two programs disagree, the cause is almost always one of these inputs or a birth time near a boundary, which the **Birth-time sensitivity** panel shows.

## Predictions are a different matter

A correct calculation does not make a reading true. JoRoScope therefore separates the two and offers tests for the readings:

- **Chart Verification** states facts about the past (siblings, parents, dated events) with the rule and the confidence behind each, for the person to mark right or wrong. Each statement names its classical source.
- **Past years to check** on the Year-by-Year Forecast tab runs the forecast over the years the person remembers, to rate year by year. Every yearly card has a *Why these scores* list of the factors behind it.
- **Accuracy figures** come from the marks people choose to share (nothing personal is stored). Every hit rate for a dated event is shown beside its chance baseline: the share of the eligible years that the predicted windows covered. A marriage window covering 30% of the ages 18 to 45 is hit 30% of the time by luck, so only the lift above that baseline says anything. The public figures (`GET /api/accuracy`, and the *How accurate has it been?* card on the Tools page) show groups of 20 or more marks only.

## Reproducing the checks

```bash
python -m unittest discover -s tests -v
```

The Node tests need a running server: `python server.py 8765 --no-browser`, then `for t in tests/*.js; do node "$t"; done`.
