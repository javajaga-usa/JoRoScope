# Swiss Ephemeris Compliance & Astronomical Standards

JoRoScope utilizes the **Swiss Ephemeris** (developed by Astrodienst AG, Zurich) via the `pyswisseph` Python C-extension binding.

---

## License & Compliance
- The Swiss Ephemeris is published under the **GNU Affero General Public License version 3 (AGPLv3)**.
- JoRoScope complies fully with the AGPLv3. Complete source code is provided.
- Swiss Ephemeris copyright belongs to Astrodienst AG.

---

## Astronomical Algorithms
- **Ephemeris Model**: Moshier planetary ephemeris / JPL DE431 compressed ephemeris data.
- **Coordinate System**: Geocentric ecliptic longitude and latitude.
- **Topocentric Capability**: Available with geographic latitude, longitude, and elevation.
- **Ayanamsa Models**:
  - Lahiri (Chitra Paksha) — Standard Indian Government Ephemeris (`swe.SIDM_LAHIRI`).
  - B.V. Raman — Traditional Raman Ayanamsa (`swe.SIDM_RAMAN`).
  - Krishnamurti (KP) — KP System reference (`swe.SIDM_KRISHNAMURTI`).
  - Fagan-Bradley — Western sidereal baseline (`swe.SIDM_FAGAN_BRADLEY`).
- **House Systems**:
  - Sripati / Porphyry (Bhava Chalita standard for Vedic systems).
  - Placidus (Krishnamurti KP Cusps standard).
  - Equal House / Whole Sign.
