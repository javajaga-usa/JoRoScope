"""Month-by-month transit (Gochara) forecast for the coming year, read from the natal Moon.

For each month the grahas' signs are taken for the larger part of the month, with every sign
change dated. A graha is favourable in the houses Gochara gives it (Phaladeepika 26), unless another
graha stands in its Vedha (obstruction) house; the Sun and Saturn, and the Moon and Mercury, do not
obstruct each other. The Ashtakavarga bindus of the sign it transits strengthen or weaken the
result. Chandrashtamam days (the Moon in the 8th from the natal Moon) are listed for each month.
"""
from datetime import datetime, timezone

from .engine import AYAN, GOCHARA_GOOD_HOUSES, SIGNS, TAMIL, jd_to_utc, sidereal_position, sign_ingresses, swe, utc_to_jd
from .readings.common import HOUSE_THEMES, PLANET_TAMIL
from .readings.report import card, chapter, table

TRANSIT_BODIES = (('Sun', swe.SUN), ('Mars', swe.MARS), ('Mercury', swe.MERCURY), ('Jupiter', swe.JUPITER),
                  ('Venus', swe.VENUS), ('Saturn', swe.SATURN), ('Rahu', swe.MEAN_NODE))
# Vedha house for each good house, from the natal Moon (Phaladeepika 26)
VEDHA = {
    'Sun': {3: 9, 6: 12, 10: 4, 11: 5}, 'Mars': {3: 12, 6: 9, 11: 5}, 'Saturn': {3: 12, 6: 9, 11: 5},
    'Mercury': {2: 5, 4: 3, 6: 9, 8: 1, 10: 8, 11: 12}, 'Jupiter': {2: 12, 5: 4, 7: 3, 9: 10, 11: 8},
    'Venus': {1: 8, 2: 7, 3: 1, 4: 10, 5: 9, 8: 5, 9: 11, 11: 6, 12: 3},
    'Rahu': {3: 12, 6: 9, 11: 5}, 'Ketu': {3: 12, 6: 9, 11: 5},
}
NO_VEDHA_BETWEEN = ({'Sun', 'Saturn'}, {'Moon', 'Mercury'})
WEIGHT = {'Saturn': 2.0, 'Jupiter': 2.0, 'Rahu': 1.5, 'Ketu': 1.5, 'Sun': 1.0, 'Mars': 1.0, 'Mercury': 0.75, 'Venus': 0.75}
MONTHS_TA = ['ஜனவரி', 'பிப்ரவரி', 'மார்ச்', 'ஏப்ரல்', 'மே', 'ஜூன்', 'ஜூலை', 'ஆகஸ்ட்', 'செப்டம்பர்', 'அக்டோபர்', 'நவம்பர்', 'டிசம்பர்']


def _segments(body, jd0, jd1):
    """[(start, end, sign)] of a graha's signs between two moments."""
    edges = [(jd0, int(sidereal_position(jd0, body)[0] // 30))]
    step = 0.25 if body == swe.MOON else 2.0
    for jd, _, sign in sign_ingresses(body, jd0, jd1, step=step):
        edges.append((jd, sign))
    return [(start, (edges[i + 1][0] if i + 1 < len(edges) else jd1), sign) for i, (start, sign) in enumerate(edges)]


def _node_sign(sign, name):
    return (sign + 6) % 12 if name == 'Ketu' else sign


def month_forecast(planets, bav, jd0, jd1, tz):
    moon = planets['Moon']['sign_index']
    signs, changes = {}, []
    for name, body in TRANSIT_BODIES:
        segs = _segments(body, jd0, jd1)
        for nm in ((name, 'Ketu') if name == 'Rahu' else (name,)):
            main = max(segs, key=lambda s: s[1] - s[0])[2]
            signs[nm] = _node_sign(main, nm)
            for start, _, sign in segs[1:]:
                sg = _node_sign(sign, nm)
                changes.append(dict(planet=nm, date=jd_to_utc(start).astimezone(tz).date().isoformat(),
                                    sign=SIGNS[sg], sign_ta=TAMIL[sg], house=(sg - moon) % 12 + 1))
    house = {nm: (sg - moon) % 12 + 1 for nm, sg in signs.items()}
    rows, score, good, bad = [], 0.0, [], []
    for nm in ('Jupiter', 'Saturn', 'Rahu', 'Ketu', 'Sun', 'Mars', 'Mercury', 'Venus'):
        h = house[nm]
        favourable = h in GOCHARA_GOOD_HOUSES[nm]
        blocked_by = None
        if favourable and h in VEDHA[nm]:
            vh = VEDHA[nm][h]
            blocked_by = next((o for o, oh in house.items() if oh == vh and o != nm and
                               not any({nm, o} == pair for pair in NO_VEDHA_BETWEEN)), None)
        bindus = bav[nm][signs[nm]] if nm in bav else None
        value = (1 if favourable and not blocked_by else (0 if blocked_by else -1))
        if bindus is not None:
            value += 0.5 if bindus >= 5 else (-0.5 if bindus <= 2 else 0)
        score += value * WEIGHT[nm]
        (good if value > 0 else bad if value < 0 else []).append((nm, h))
        verdict_en = 'favourable' if value > 0 else ('obstructed (Vedha)' if blocked_by else ('mixed' if value == 0 else 'unfavourable'))
        verdict_ta = 'சாதகம்' if value > 0 else ('வேதை தடை' if blocked_by else ('கலப்பு' if value == 0 else 'பாதகம்'))
        rows.append(dict(planet=nm, sign=SIGNS[signs[nm]], sign_ta=TAMIL[signs[nm]], house=h, bindus=bindus,
                         vedha_by=blocked_by, verdict_en=verdict_en, verdict_ta=verdict_ta, value=value))
    # Chandrashtamam: the Moon in the 8th sign from the natal Moon
    eighth = (moon + 7) % 12
    chandrashtamam = [dict(start=jd_to_utc(s).astimezone(tz).isoformat(timespec='minutes'),
                           end=jd_to_utc(e).astimezone(tz).isoformat(timespec='minutes'))
                      for s, e, sg in _segments(swe.MOON, jd0, jd1) if sg == eighth]
    return dict(score=round(score, 2), grahas=rows, changes=sorted(changes, key=lambda c: c['date']),
                chandrashtamam=chandrashtamam, good=good, bad=bad)


def _summary(m):
    theme = lambda h, i: HOUSE_THEMES[h][i]
    good_en = '; '.join(f"{g} (house {h}: {theme(h, 0)})" for g, h in m['good'][:3])
    good_ta = '; '.join(f"{PLANET_TAMIL[g]} ({h}-ஆம் இடம்: {theme(h, 1)})" for g, h in m['good'][:3])
    bad_en = '; '.join(f"{g} (house {h}: {theme(h, 0)})" for g, h in m['bad'][:3])
    bad_ta = '; '.join(f"{PLANET_TAMIL[g]} ({h}-ஆம் இடம்: {theme(h, 1)})" for g, h in m['bad'][:3])
    en = (f"Supportive: {good_en}. " if good_en else 'Few grahas support you this month. ') + \
         (f"Take care with: {bad_en}." if bad_en else 'No transit works strongly against you.')
    ta = (f"துணை நிற்பவை: {good_ta}. " if good_ta else 'இம்மாதம் துணை நிற்கும் கிரகங்கள் குறைவு. ') + \
         (f"கவனம் தேவை: {bad_ta}." if bad_ta else 'பெரிதாகப் பாதிக்கும் கோச்சாரம் இல்லை.')
    if m['changes']:
        en += ' Sign changes: ' + ', '.join(f"{c['planet']} into {c['sign']} ({c['date']})" for c in m['changes']) + '.'
        ta += ' ராசி மாற்றங்கள்: ' + ', '.join(f"{PLANET_TAMIL[c['planet']]} {c['sign_ta']} ({c['date']})" for c in m['changes']) + '.'
    if m['chandrashtamam']:
        day = lambda iso: datetime.fromisoformat(iso)
        en += ' Chandrashtamam: ' + ', '.join(f"{day(c['start']):%d %b %H:%M} to {day(c['end']):%d %b %H:%M}" for c in m['chandrashtamam']) + '.'
        ta += ' சந்திராஷ்டமம்: ' + ', '.join(
            f"{day(c['start']).day} {MONTHS_TA[day(c['start']).month - 1]} {day(c['start']):%H:%M} முதல் "
            f"{day(c['end']).day} {MONTHS_TA[day(c['end']).month - 1]} {day(c['end']):%H:%M} வரை" for c in m['chandrashtamam']) + '.'
    return en, ta


def calculate_monthly_transits(chart, months=12, now=None):
    from zoneinfo import ZoneInfo
    tz = ZoneInfo(chart.get('timezone') or 'UTC')
    swe.set_sid_mode(AYAN[chart.get('ayanamsa') or 'Lahiri'])
    planets = chart['planets']
    bav = (chart.get('ashtakavarga') or {}).get('BAV', {})
    local_now = (now or datetime.now(timezone.utc)).astimezone(tz)
    year, month = local_now.year, local_now.month
    results, cards = [], []
    for _ in range(months):
        start = datetime(year, month, 1, tzinfo=tz)
        year, month = (year + 1, 1) if month == 12 else (year, month + 1)
        end = datetime(year, month, 1, tzinfo=tz)
        m = month_forecast(planets, bav, utc_to_jd(start.astimezone(timezone.utc)), utc_to_jd(end.astimezone(timezone.utc)), tz)
        m['month'] = start.strftime('%Y-%m')
        results.append(m)
    scores = sorted(r['score'] for r in results)
    low, high = scores[len(scores) // 3], scores[2 * len(scores) // 3]
    for m in results:
        verdict = 'good' if m['score'] >= high and m['score'] > 0 else ('bad' if m['score'] <= low and m['score'] < 0 else 'mixed')
        m['verdict'] = verdict
        en, ta = _summary(m)
        y, mo = int(m['month'][:4]), int(m['month'][5:])
        label_en = datetime(y, mo, 1).strftime('%B %Y')
        cards.append(card('🗓️', label_en, f'{MONTHS_TA[mo - 1]} {y}', en, ta,
                          f"Transit score {m['score']:+.1f}", f"கோச்சார மதிப்பு {m['score']:+.1f}", verdict=verdict))
    first = results[0]
    rows = [((g['planet'], PLANET_TAMIL[g['planet']]), (g['sign'], g['sign_ta']), g['house'],
             '—' if g['bindus'] is None else g['bindus'], (g['verdict_en'] + (f" by {g['vedha_by']}" if g['vedha_by'] else ''),
                                                          g['verdict_ta'] + (f" ({PLANET_TAMIL[g['vedha_by']]})" if g['vedha_by'] else '')))
            for g in first['grahas']]
    return chapter(
        'monthly', 'Monthly Transit Forecast', 'மாதாந்திர கோச்சார பலன்',
        'The next twelve months from your Moon sign: each graha\'s house from the natal Moon, the Vedha (obstruction) rule, '
        'Ashtakavarga bindus, sign changes and Chandrashtamam days. Months are ranked against each other for this chart.',
        'உங்கள் ஜன்ம ராசியிலிருந்து அடுத்த 12 மாதங்கள்: ஒவ்வொரு கிரகத்தின் இடம், வேதை விதி, அஷ்டகவர்க்கப் பரல்கள், ராசி மாற்றங்கள், '
        'சந்திராஷ்டம நாட்கள். மாதங்கள் இந்த ஜாதகத்திற்குள் ஒப்பிடப்படுகின்றன.',
        cards=cards,
        tables=[table('This month, graha by graha', 'இம்மாதம், கிரக வாரியாக',
                      [('Graha', 'கிரகம்'), ('Sign', 'ராசி'), ('House from Moon', 'சந்திரனிலிருந்து'), ('Bindus', 'பரல்கள்'),
                       ('Result', 'பலன்')], rows)],
        months=results)
