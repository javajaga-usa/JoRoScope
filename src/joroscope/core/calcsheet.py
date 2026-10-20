"""The calculation sheet and the birth-time sensitivity of a chart: the two things a person can
check against another software or a printed horoscope.

The sheet states every input the engine applied (the time zone offset actually in force on the birth
date, the UT and local mean time, the sunrise and sunset used, the sidereal time, the ayanamsa to the
arc second, the node and house conventions, the dasa year) so that a difference from another program
can be traced to its cause. The sensitivity search finds how far the birth time can move before the
Lagna, the Navamsa Lagna, the Moon's sign, star or pada changes, and how many days every Dasa date
moves per minute of birth time.
"""
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import swisseph as swe

from .engine import DASHA_NAMES, DASHA_YEARS, SIGNS, STARS, calculate_vargas, jd_to_utc

NAK_SPAN = 40 / 3
PADA_SPAN = 10 / 3
SEARCH_LIMIT_MINUTES = 24 * 60  # the Moon crosses a star within about 26 hours; beyond a day, "stable"


def dms(deg, signed=False):
    """D°MM′SS″ of a longitude or latitude; signed adds +/-."""
    sign = '-' if deg < 0 else ('+' if signed else '')
    total = round(abs(deg) * 3600)
    d, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return f"{sign}{d}° {m:02d}′ {s:02d}″"


def hms(hours):
    total = round((hours % 24) * 3600)
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def _offset_text(minutes):
    sign = '+' if minutes >= 0 else '-'
    h, m = divmod(abs(int(round(minutes))), 60)
    return f"{sign}{h:02d}:{m:02d}"


def calculation_sheet(data, utc, jd, lat, lon, planets, ayan, ayanamsa_degrees, day_events, tz, dasa_year_kind, dasa_year):
    """Every input and convention the chart was computed with."""
    from .. import __version__
    from .dasas import DASA_YEARS
    local = utc.astimezone(tz)
    offset_minutes = local.utcoffset().total_seconds() / 60
    lmt = utc + timedelta(minutes=lon * 4)
    lmt_minutes = lon * 4
    sidereal_hours = (swe.sidtime(jd) + lon / 15) % 24
    rise = jd_to_utc(day_events['sunrise']).astimezone(tz)
    sset = jd_to_utc(day_events['sunset']).astimezone(tz)
    moon, asc = planets['Moon'], planets['Ascendant']
    return dict(
        app_version=__version__,
        engine=f"Swiss Ephemeris {swe.version}",
        ephemeris='Moshier analytical ephemeris (within about 1″ of JPL DE431 for 1800–2200)',
        timezone=data['timezone'],
        timezone_abbreviation=local.tzname() or '',
        utc_offset=_offset_text(offset_minutes),
        utc_offset_minutes=offset_minutes,
        local_time=local.strftime('%Y-%m-%d %H:%M:%S'),
        ut=utc.strftime('%Y-%m-%d %H:%M:%S'),
        julian_day=jd,
        delta_t_seconds=round(swe.deltat(jd) * 86400, 2),
        local_mean_time=lmt.strftime('%H:%M:%S'),
        lmt_offset=_offset_text(lmt_minutes),
        clock_ahead_of_lmt_minutes=round(offset_minutes - lmt_minutes, 1),
        local_sidereal_time=hms(sidereal_hours),
        latitude=dms(lat) + (' N' if lat >= 0 else ' S'),
        longitude=dms(lon) + (' E' if lon >= 0 else ' W'),
        sunrise=rise.strftime('%H:%M:%S'),
        sunset=sset.strftime('%H:%M:%S'),
        sunrise_rule='Upper limb of the Sun with standard refraction (Thirukanitha convention)',
        ayanamsa=ayan,
        ayanamsa_value=dms(ayanamsa_degrees),
        ayanamsa_degrees=ayanamsa_degrees,
        lagna=dms(asc['longitude'] % 30),
        lagna_sign=asc['sign'],
        lagna_longitude=dms(asc['longitude']),
        moon=dms(moon['longitude'] % 30),
        moon_sign=moon['sign'],
        moon_longitude=dms(moon['longitude']),
        nodes='Mean node (Rahu); Ketu exactly opposite',
        houses='Whole sign houses; Bhava Chakra by Sripati (Porphyry); KP cusps by Placidus in the Krishnamurti ayanamsa',
        dasa_year=DASA_YEARS[dasa_year_kind][1],
        dasa_year_days=dasa_year,
        coordinates='Geocentric sidereal ecliptic longitudes',
    )


def _first_change(value_at, step, limit):
    """Minutes (positive) until value_at(minutes) differs from value_at(0), searching outward in
    steps then bisecting to a tenth of a minute; None when nothing changes within the limit."""
    base = value_at(0)
    previous = 0.0
    t = step
    while t <= limit:
        if value_at(t) != base:
            lo, hi = previous, t
            while hi - lo > 0.1:
                mid = (lo + hi) / 2
                if value_at(mid) == base:
                    lo = mid
                else:
                    hi = mid
            return round(hi, 1), value_at(hi)
        previous, t = t, t + step
    return None, None


def birth_time_sensitivity(jd, lat, lon, dasa_year, uncertainty=None):
    """How many minutes earlier and later the birth time can move before each quantity changes."""
    flags = swe.FLG_MOSEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED
    lagna = lambda minutes: swe.houses_ex(jd + minutes / 1440, lat, lon, b'P', swe.FLG_SIDEREAL)[1][0]
    moon = lambda minutes: swe.calc_ut(jd + minutes / 1440, swe.MOON, flags)[0][0] % 360
    sign_label = lambda idx: dict(index=idx, en=SIGNS[idx])
    star_label = lambda idx: dict(index=idx, en=STARS[idx])
    quantities = [
        ('lagna_sign', lambda m: int(lagna(m) // 30), sign_label, 1),
        ('navamsa_lagna', lambda m: calculate_vargas(lagna(m))['D9'], sign_label, 0.5),
        ('moon_sign', lambda m: int(moon(m) // 30), sign_label, 4),
        ('moon_star', lambda m: int(moon(m) / NAK_SPAN), star_label, 4),
        ('moon_pada', lambda m: int(moon(m) / PADA_SPAN), lambda idx: dict(index=idx % 4 + 1, star=STARS[idx // 4], en=f"{STARS[idx // 4]} {idx % 4 + 1}"), 2),
    ]
    try:
        uncertainty = max(0.0, float(uncertainty)) if uncertainty not in (None, '') else None
    except (TypeError, ValueError):
        uncertainty = None
    rows = []
    for key, value_at, label, step in quantities:
        later, after = _first_change(value_at, step, SEARCH_LIMIT_MINUTES)
        earlier, before = _first_change(lambda m: value_at(-m), step, SEARCH_LIMIT_MINUTES)
        margin = min(x for x in (earlier, later) if x is not None) if (earlier is not None or later is not None) else None
        row = dict(key=key, value=label(value_at(0)), earlier=earlier, later=later,
                   before=label(before) if before is not None else None, after=label(after) if after is not None else None,
                   margin=margin, limit=SEARCH_LIMIT_MINUTES)
        if uncertainty is not None:
            row['stable'] = margin is None or margin > uncertainty
        rows.append(row)
    # Rates: the Lagna's motion and the shift of every Dasa date per minute of birth time
    lagna_rate = ((lagna(1) - lagna(0)) % 360) * 60  # arc-minutes per minute
    moon_speed = swe.calc_ut(jd, swe.MOON, flags)[0][3]  # degrees per day
    moon_now = moon(0)
    dasa_index = int(moon_now / NAK_SPAN) % 9
    dasa_days_per_minute = moon_speed / 1440 / NAK_SPAN * DASHA_YEARS[dasa_index] * dasa_year
    out = dict(quantities=rows, lagna_arcmin_per_minute=round(lagna_rate, 2),
               dasa_days_per_minute=round(dasa_days_per_minute, 2), dasa_at_birth=DASHA_NAMES[dasa_index],
               uncertainty_minutes=uncertainty)
    if uncertainty is not None:
        out['dasa_uncertainty_days'] = round(dasa_days_per_minute * uncertainty, 1)
        out['lagna_uncertainty_degrees'] = round(lagna_rate * uncertainty / 60, 2)
        out['unstable'] = [r['key'] for r in rows if not r['stable']]
    return out
