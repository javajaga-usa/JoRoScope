"""Birth time rectification helper: tests candidate birth times against dated life events.

For every candidate time in a window around the stated one, the Lagna and the Moon (and so the
Vimshottari dasas) are recomputed; the other grahas barely move and are taken at the stated time.
Each event scores when the Maha Dasa and Bhukti lords running on its date signify the event (they
rule or occupy its houses from the candidate Lagna, or are its karaka), and when Saturn and Jupiter
both influence its main house or that house's lord by transit (K.N. Rao's double transit).
Candidates that share a Lagna and Navamsa are grouped, and the groups ranked by their best score.
This narrows the birth time; confirm it with an astrologer.
"""
import math
from datetime import datetime, timedelta, timezone

from .engine import (AYAN, SIGNS, TAMIL, calculate_vargas, dasha, local_to_utc, sidereal_position, swe, utc_to_jd)
from .readings.common import PLANET_TAMIL, SIGN_LORDS
from .readings.report import card, chapter, table

EVENTS = {
    'marriage': ('Marriage', 'திருமணம்', (7, 2, 11), ('Venus', 'Jupiter')),
    'child': ('Birth of a child', 'குழந்தை பிறப்பு', (5, 9, 11), ('Jupiter',)),
    'career': ('Job, promotion or business start', 'வேலை / பதவி உயர்வு / தொழில் தொடக்கம்', (10, 6, 11), ('Sun', 'Saturn', 'Mercury')),
    'education': ('Degree or education milestone', 'பட்டம் / கல்வி நிலை', (4, 5, 9), ('Mercury', 'Jupiter')),
    'relocation': ('Moving house or abroad', 'இடமாற்றம் / வெளிநாடு', (12, 9, 4, 3), ('Rahu', 'Moon')),
    'property': ('Buying property or a vehicle', 'சொத்து / வாகனம் வாங்குதல்', (4, 11), ('Mars', 'Venus')),
    'illness': ('Illness, surgery or accident', 'நோய் / அறுவை சிகிச்சை / விபத்து', (6, 8, 12, 1), ('Mars', 'Saturn', 'Rahu')),
    'father': ('Loss of father', 'தந்தை இழப்பு', (10, 3, 9), ('Sun', 'Saturn')),
    'mother': ('Loss of mother', 'தாய் இழப்பு', (5, 11, 4), ('Moon', 'Saturn')),
}
SLOW = (('Sun', swe.SUN), ('Mars', swe.MARS), ('Mercury', swe.MERCURY), ('Jupiter', swe.JUPITER), ('Venus', swe.VENUS),
        ('Saturn', swe.SATURN), ('Rahu', swe.MEAN_NODE))
SATURN_ASPECTS, JUPITER_ASPECTS = (1, 3, 7, 10), (1, 5, 7, 9)
EVENT_MAX = 7  # Maha Dasa 2, Bhukti 2, Pratyantar 1, double transit 2


def _running(rows, moment):
    """(Maha Dasa, Bhukti, Pratyantar) lords running at a moment (ISO, UTC)."""
    for md in rows:
        if md['start'] <= moment < md['end']:
            for b in md['subperiods']:
                if b['start'] <= moment < b['end']:
                    pd = next((p['lord'] for p in b.get('pratyantars', []) if p['start'] <= moment < p['end']), None)
                    return md['lord'], b['lord'], pd
    return None, None, None


def _influences(transit_sign, target_sign, aspects):
    return (target_sign - transit_sign) % 12 + 1 in aspects


def rectify(data, events, window_minutes=60, step_minutes=2):
    if not events:
        raise ValueError('Add at least one dated life event.')
    if len(events) > 12:
        raise ValueError('Use at most 12 events.')
    window_minutes = max(4, min(int(window_minutes), 240))
    step_minutes = max(1, min(int(step_minutes), 10))
    lat, lon = float(data['latitude']), float(data['longitude'])
    if not math.isfinite(lat) or not -66 <= lat <= 66:
        raise ValueError('Latitude must be between 66° south and 66° north in this version.')
    ayanamsa = data.get('ayanamsa') or 'Lahiri'
    swe.set_sid_mode(AYAN[ayanamsa])
    stated = local_to_utc(data['date'], data['time'], data.get('timezone', 'Asia/Kolkata'), data.get('fold'))
    jd0 = utc_to_jd(stated)
    slow = {name: int(sidereal_position(jd0, body)[0] // 30) for name, body in SLOW}
    slow['Ketu'] = (slow['Rahu'] + 6) % 12

    parsed = []
    for ev in events:
        kind = ev.get('type')
        if kind not in EVENTS:
            raise ValueError('Choose an event type: ' + ', '.join(EVENTS))
        try:
            when = datetime.fromisoformat(ev['date']).replace(tzinfo=timezone.utc) + timedelta(hours=12)
        except (KeyError, ValueError):
            raise ValueError('Enter each event date as YYYY-MM-DD.')
        if when <= stated:
            raise ValueError('Event dates must be after the birth.')
        ejd = utc_to_jd(when)
        parsed.append(dict(kind=kind, date=ev['date'], when=when.isoformat(),
                           saturn=int(sidereal_position(ejd, swe.SATURN)[0] // 30),
                           jupiter=int(sidereal_position(ejd, swe.JUPITER)[0] // 30)))

    candidates = []
    for k in range(-window_minutes // step_minutes, window_minutes // step_minutes + 1):
        minutes = k * step_minutes
        utc = stated + timedelta(minutes=minutes)
        jd = utc_to_jd(utc)
        asc_lon = swe.houses_ex(jd, lat, lon, b'P', swe.FLG_SIDEREAL)[1][0]
        asc = int(asc_lon // 30)
        moon = sidereal_position(jd, swe.MOON)[0]
        signs = dict(slow, Moon=int(moon // 30))
        rows = dasha(moon, utc)
        total, detail = 0, []
        for ev in parsed:
            label, label_ta, houses, karakas = EVENTS[ev['kind']]
            house_signs = [(asc + h - 1) % 12 for h in houses]
            sig = {SIGN_LORDS[s] for s in house_signs} | {g for g, s in signs.items() if s in house_signs} | set(karakas)
            md, ad, pd = _running(rows, ev['when'])
            score = (2 if md in sig else 0) + (2 if ad in sig else 0) + (1 if pd in sig else 0)
            main = house_signs[0]
            main_lord_sign = signs[SIGN_LORDS[main]] if SIGN_LORDS[main] in signs else main
            sat = _influences(ev['saturn'], main, SATURN_ASPECTS) or _influences(ev['saturn'], main_lord_sign, SATURN_ASPECTS)
            jup = _influences(ev['jupiter'], main, JUPITER_ASPECTS) or _influences(ev['jupiter'], main_lord_sign, JUPITER_ASPECTS)
            score += 2 if (sat and jup) else 0
            total += score
            detail.append(dict(kind=ev['kind'], date=ev['date'], dasa=md, bhukti=ad, pratyantar=pd, score=score, double_transit=sat and jup))
        candidates.append(dict(offset=minutes, utc=utc.isoformat(timespec='minutes'), lagna=asc, navamsa=calculate_vargas(asc_lon)['D9'],
                               asc_degree=round(asc_lon % 30, 2), score=total, events=detail))

    # Group consecutive candidates with the same Lagna and Navamsa
    groups = []
    for c in candidates:
        if groups and groups[-1]['lagna'] == c['lagna'] and groups[-1]['navamsa'] == c['navamsa']:
            groups[-1]['members'].append(c)
        else:
            groups.append(dict(lagna=c['lagna'], navamsa=c['navamsa'], members=[c]))
    best_score = max(c['score'] for c in candidates)
    top = best_score / (EVENT_MAX * len(parsed))
    for g in groups:
        g['best'] = max(g['members'], key=lambda c: (c['score'], -abs(c['offset'])))
        g['score'] = g['best']['score']
    ranked = sorted(groups, key=lambda g: (-g['score'], abs(g['best']['offset'])))

    tz_name = data.get('timezone', 'Asia/Kolkata')
    from zoneinfo import ZoneInfo
    local = lambda iso: datetime.fromisoformat(iso).astimezone(ZoneInfo(tz_name)).strftime('%H:%M')
    best = ranked[0]
    first, last = best['members'][0], best['members'][-1]
    cards = [card('🕰️', f"Most consistent: {local(best['best']['utc'])} ({SIGNS[best['lagna']]} Lagna)",
                  f"மிகப் பொருத்தமானது: {local(best['best']['utc'])} ({TAMIL[best['lagna']]} லக்னம்)",
                  f"Times from {local(first['utc'])} to {local(last['utc'])} give a {SIGNS[best['lagna']]} Lagna with a "
                  f"{SIGNS[best['navamsa']]} Navamsa and fit the events best (score {best['score']} of {EVENT_MAX * len(parsed)}). "
                  f"Within that range {local(best['best']['utc'])} fits best, {best['best']['offset']:+d} minutes from the stated time.",
                  f"{local(first['utc'])} முதல் {local(last['utc'])} வரையிலான நேரங்கள் {TAMIL[best['lagna']]} லக்னம், "
                  f"{TAMIL[best['navamsa']]} நவாம்சம் தருகின்றன; நிகழ்வுகளுடன் மிகப் பொருந்துகின்றன (மதிப்பு {best['score']} / {EVENT_MAX * len(parsed)}). "
                  f"அவற்றில் {local(best['best']['utc'])} மிகப் பொருத்தம், கூறப்பட்ட நேரத்திலிருந்து {best['best']['offset']:+d} நிமிடங்கள்.",
                  verdict='good' if top >= 0.6 else 'mixed')]
    for d in best['best']['events']:
        label, label_ta = EVENTS[d['kind']][:2]
        ok = d['score'] >= 4
        cards.append(card('✅' if ok else '•', f"{label}, {d['date']}", f"{label_ta}, {d['date']}",
                          f"{d['dasa']} Dasa, {d['bhukti']} Bhukti, {d['pratyantar']} Pratyantar" + (' with a double transit' if d['double_transit'] else '')
                          + f": score {d['score']} of {EVENT_MAX}.",
                          f"{PLANET_TAMIL.get(d['dasa'], d['dasa'])} தசை, {PLANET_TAMIL.get(d['bhukti'], d['bhukti'])} புக்தி, "
                          f"{PLANET_TAMIL.get(d['pratyantar'], d['pratyantar'])} அந்தரம்"
                          + (', இரட்டைக் கோச்சாரத்துடன்' if d['double_transit'] else '') + f": மதிப்பு {d['score']} / {EVENT_MAX}.",
                          verdict='good' if ok else 'mixed'))
    rows = [((f"{local(g['members'][0]['utc'])}–{local(g['members'][-1]['utc'])}",) * 2, (SIGNS[g['lagna']], TAMIL[g['lagna']]),
             (SIGNS[g['navamsa']], TAMIL[g['navamsa']]), local(g['best']['utc']), g['score']) for g in ranked[:8]]
    return chapter(
        'rectification', 'Birth Time Rectification', 'ஜனன நேரத் திருத்தம்',
        f"Candidate birth times {window_minutes} minutes either side of the stated time, every {step_minutes} minutes, "
        'tested against your life events by their running dasas and double transits. Use it to narrow the time, then confirm with an astrologer.',
        f"கூறப்பட்ட நேரத்திற்கு முன்னும் பின்னும் {window_minutes} நிமிடங்கள், ஒவ்வொரு {step_minutes} நிமிடமும், வாழ்க்கை நிகழ்வுகளுடன் "
        'அவற்றின் தசைகள், இரட்டைக் கோச்சாரம் மூலம் சோதிக்கப்பட்டன. நேரத்தைச் சுருக்க இதைப் பயன்படுத்தி ஜோதிடரிடம் உறுதிப்படுத்தவும்.',
        cards=cards,
        tables=[table('Candidate times', 'சாத்தியமான நேரங்கள்',
                      [('Time range', 'நேர வரம்பு'), ('Lagna', 'லக்னம்'), ('Navamsa', 'நவாம்சம்'), ('Best time', 'சிறந்த நேரம்'), ('Score', 'மதிப்பு')],
                      rows)],
        cards_first=True, best_utc=best['best']['utc'], best_offset=best['best']['offset'], max_score=EVENT_MAX * len(parsed),
        event_types=[dict(key=k, en=v[0], ta=v[1]) for k, v in EVENTS.items()])
