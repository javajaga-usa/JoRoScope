"""Year-by-year forecast for the coming years, as Astro-Vision's yearly predictions give it.

For each calendar year: the Maha Dasa and Bhukti periods running in it (dated), the sign changes of
Saturn, Jupiter and Rahu, and any Saturn cycle (Sade Sati, Ashtama, Kandaka) from the natal Moon.
Five areas (career, money, family, health, travel) are scored from:
- the Dasa and Bhukti lords, weighted by how much of the year each Bhukti covers: a lord that rules
  or occupies an area's houses activates it, in its favour when the lord is a functional benefic or
  well placed, against it when it is a functional malefic or weak; for health, lords of the 6th,
  8th and 12th count against;
- Jupiter and Saturn by transit: Jupiter in a good house from the Moon (2, 5, 7, 9, 11) and on or
  aspecting an area's house from the Lagna helps; Saturn in the 3rd, 6th or 11th from the Moon
  helps work and money; Sade Sati, Ashtama and Kandaka Sani weigh on health, work and family.
The good and careful months come from the Pratyantara periods in the year: a benefic, well-placed
Pratyantara lord gives good months, a malefic or the lord of the 8th or 12th careful ones.
"""
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from .common import DIGNITY_SCORE, DUSTHANAS, MALAYALAM_SIGNS, PLANET_ML, PLANET_TAMIL, SIGN_LORDS, SIGNS, TAMIL_SIGNS, _functional_role
from .report import card, chapter, table

AREAS = [  # key, houses it lives in, (en, ta, ml)
    ('career', (10, 6, 11), ('Career', 'தொழில்', 'തൊഴിൽ')),
    ('money', (2, 11), ('Money', 'பணம்', 'ധനം')),
    ('family', (4, 5, 7, 2), ('Family & marriage', 'குடும்பம் & திருமணம்', 'കുടുംബം & വിവാഹം')),
    ('health', (1,), ('Health', 'உடல்நலம்', 'ആരോഗ്യം')),
    ('travel', (3, 9, 12), ('Travel', 'பயணம்', 'യാത്ര')),
]
LEVELS = {  # verdict: (symbol, en, ta, ml)
    'good': ('✓', 'favourable', 'சாதகம்', 'അനുകൂലം'),
    'steady': ('•', 'steady', 'நிதானம்', 'സ്ഥിരം'),
    'care': ('!', 'needs care', 'கவனம் தேவை', 'ശ്രദ്ധ വേണം'),
}
AREA_TEXT = {  # area -> verdict -> (en, ta, ml)
    'career': {
        'good': ('rise, recognition and new responsibility; a good year to seek promotion or start something.',
                 'உயர்வு, அங்கீகாரம், புதிய பொறுப்பு; பதவி உயர்வு அல்லது புதிய தொடக்கத்துக்கு நல்ல ஆண்டு.',
                 'ഉയർച്ച, അംഗീകാരം, പുതിയ ചുമതല; സ്ഥാനക്കയറ്റത്തിനോ പുതിയ തുടക്കത്തിനോ നല്ല വർഷം.'),
        'steady': ('steady work; results match the effort put in.', 'நிலையான பணி; உழைப்புக்கேற்ற பலன்.',
                   'സ്ഥിരമായ ജോലി; പ്രയത്നത്തിനൊത്ത ഫലം.'),
        'care': ('pressure at work or with superiors; avoid hasty job changes and keep records in order.',
                 'பணியிலோ மேலதிகாரிகளிடமோ அழுத்தம்; அவசர வேலை மாற்றம் தவிர்த்து ஆவணங்களைச் சரியாக வைக்கவும்.',
                 'ജോലിയിലോ മേലധികാരികളുമായോ സമ്മർദ്ദം; തിടുക്കത്തിലുള്ള ജോലിമാറ്റം ഒഴിവാക്കി രേഖകൾ ക്രമത്തിൽ വയ്ക്കുക.'),
    },
    'money': {
        'good': ('income grows and savings build; a good year to invest or buy.', 'வருமானம் பெருகி சேமிப்பு கூடும்; முதலீடு, கொள்முதலுக்கு நல்ல ஆண்டு.',
                 'വരുമാനം വർധിച്ച് സമ്പാദ്യം കൂടും; നിക്ഷേപത്തിനും വാങ്ങലിനും നല്ല വർഷം.'),
        'steady': ('money flows evenly; plan larger spending.', 'பணவரவு சீராக இருக்கும்; பெரிய செலவுகளைத் திட்டமிடவும்.',
                   'പണവരവ് സ്ഥിരം; വലിയ ചെലവുകൾ ആസൂത്രണം ചെയ്യുക.'),
        'care': ('expenses run high; avoid lending, guarantees and speculation.', 'செலவு அதிகம்; கடன் கொடுத்தல், ஜாமீன், ஊகவணிகம் தவிர்க்கவும்.',
                 'ചെലവ് കൂടുതൽ; കടം കൊടുക്കൽ, ജാമ്യം, ഊഹക്കച്ചവടം ഒഴിവാക്കുക.'),
    },
    'family': {
        'good': ('harmony at home; marriage, a child or a family celebration is well supported.',
                 'இல்லத்தில் இணக்கம்; திருமணம், குழந்தை அல்லது குடும்ப விழாவுக்குச் சாதகம்.',
                 'വീട്ടിൽ ഐക്യം; വിവാഹം, കുഞ്ഞ് അല്ലെങ്കിൽ കുടുംബ ആഘോഷത്തിന് അനുകൂലം.'),
        'steady': ('family life runs smoothly with ordinary ups and downs.', 'குடும்ப வாழ்க்கை சாதாரண ஏற்ற இறக்கங்களுடன் சீராகச் செல்லும்.',
                   'കുടുംബജീവിതം സാധാരണ ഉയർച്ചതാഴ്ചകളോടെ സുഗമമായി നീങ്ങും.'),
        'care': ('misunderstandings or a family member\'s health need patience.', 'கருத்து வேறுபாடு அல்லது குடும்பத்தினர் உடல்நலத்தில் பொறுமை தேவை.',
                 'അഭിപ്രായഭിന്നതയിലോ കുടുംബാംഗത്തിന്റെ ആരോഗ്യത്തിലോ ക്ഷമ വേണം.'),
    },
    'health': {
        'good': ('good energy and recovery.', 'நல்ல ஆற்றலும் விரைவான குணமும்.', 'നല്ല ഊർജ്ജവും വേഗത്തിലുള്ള രോഗശാന്തിയും.'),
        'steady': ('average health; keep up routine and exercise.', 'சராசரி உடல்நலம்; ஒழுங்கும் உடற்பயிற்சியும் தொடரவும்.',
                   'ശരാശരി ആരോഗ്യം; ക്രമവും വ്യായാമവും തുടരുക.'),
        'care': ('fatigue or illness is more likely; do not skip check-ups and rest.', 'சோர்வு அல்லது நோய் வாய்ப்பு அதிகம்; பரிசோதனையும் ஓய்வும் தவறாதீர்.',
                 'ക്ഷീണമോ രോഗമോ വരാൻ സാധ്യത കൂടുതൽ; പരിശോധനയും വിശ്രമവും മുടക്കരുത്.'),
    },
    'travel': {
        'good': ('journeys, pilgrimage or a move abroad go well.', 'பயணம், தீர்த்த யாத்திரை அல்லது வெளிநாட்டு இடமாற்றம் நன்கு அமையும்.',
                 'യാത്ര, തീർത്ഥാടനം അല്ലെങ്കിൽ വിദേശത്തേക്കുള്ള മാറ്റം നന്നായി നടക്കും.'),
        'steady': ('only routine travel is indicated.', 'வழக்கமான பயணம் மட்டுமே.', 'സാധാരണ യാത്ര മാത്രം.'),
        'care': ('travel brings delays or expense; plan it with margin.', 'பயணத்தில் தாமதம் அல்லது செலவு; முன்னேற்பாட்டுடன் திட்டமிடவும்.',
                 'യാത്രയിൽ കാലതാമസമോ ചെലവോ; മുൻകരുതലോടെ ആസൂത്രണം ചെയ്യുക.'),
    },
}
CYCLE_WORDS = {'sade_sati': ('Sade Sati', 'ஏழரைச் சனி', 'ഏഴരശ്ശനി'), 'ashtama': ('Ashtama Sani', 'அஷ்டம சனி', 'അഷ്ടമശ്ശനി'),
               'kandaka': ('Kandaka Sani', 'கண்டக சனி', 'കണ്ടകശ്ശനി'), 'ardhashtama': ('Ardhashtama Sani', 'அர்த்தாஷ்டம சனி', 'അർദ്ധാഷ്ടമശ്ശനി')}
MONTHS_EN = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
JUPITER_GOOD, SATURN_GOOD = (2, 5, 7, 9, 11), (3, 6, 11)
JUPITER_ASPECTS = (1, 5, 7, 9)  # the sign it occupies and its 5th, 7th and 9th


def _houses_of(planets, g, asc):
    """Houses from the Lagna a graha activates: those it rules and the one it occupies (the nodes act
    through the lord of their sign)."""
    occupied = (planets[g]['sign_index'] - asc) % 12 + 1
    owner = g if g not in ('Rahu', 'Ketu') else SIGN_LORDS[planets[g]['sign_index']]
    owned = {h for h in range(1, 13) if SIGN_LORDS[(asc + h - 1) % 12] == owner}
    return owned | {occupied}


def _quality(planets, g, asc):
    """+1 when a graha gives good results by lordship and dignity, -1 when difficult, 0 mixed."""
    lord = g if g not in ('Rahu', 'Ketu') else SIGN_LORDS[planets[g]['sign_index']]
    role, _ = _functional_role(lord, asc)
    value = {'yogakaraka': 1.5, 'benefic': 1, 'malefic': -1}.get(role, 0)
    value += 0.5 * max(-1, min(1, DIGNITY_SCORE.get(planets[g].get('dignity', 'Neutral'), 0)))
    if g in ('Rahu', 'Ketu', 'Saturn') and (planets[g]['sign_index'] - asc) % 12 + 1 in DUSTHANAS:
        value -= 0.5
    return max(-1.5, min(1.5, value))


def _month(dt, lang):
    names = {'en': MONTHS_EN, 'ta': None, 'ml': None}[lang]
    if names is None:
        from ..monthly import MONTHS_ML, MONTHS_TA
        names = MONTHS_TA if lang == 'ta' else MONTHS_ML
    return names[dt.month - 1]


def _span(a, b, lang):
    """'Mar–Apr' style month range within a year; b is exclusive (a period clipped at 1 January ends in December)."""
    b = b - timedelta(seconds=1)
    return _month(a, lang) if (a.month, a.year) == (b.month, b.year) else f"{_month(a, lang)}–{_month(b, lang)}"


def calculate_yearly_forecast(chart, years=12, now=None):
    from ..engine import AYAN, swe, utc_to_jd
    from ..monthly import _segments
    swe.set_sid_mode(AYAN[chart.get('ayanamsa') or 'Lahiri'])
    tz = ZoneInfo(chart.get('timezone') or 'UTC')
    planets = chart['planets']
    asc = planets['Ascendant']['sign_index']
    moon = planets['Moon']['sign_index']
    now = (now or datetime.now(timezone.utc)).astimezone(tz)
    parse = lambda iso: datetime.fromisoformat(iso).astimezone(tz)
    dasha = chart.get('dasha') or []
    cycles = (chart.get('gochara') or {}).get('saturn_cycles') or []
    names = {'en': lambda g: g, 'ta': lambda g: PLANET_TAMIL[g], 'ml': lambda g: PLANET_ML[g]}
    sign_names = {'en': SIGNS, 'ta': TAMIL_SIGNS, 'ml': MALAYALAM_SIGNS}

    results, cards, rows, pending = [], [], [], []
    for year in range(now.year, now.year + years):
        y0, y1 = datetime(year, 1, 1, tzinfo=tz), datetime(year + 1, 1, 1, tzinfo=tz)
        span_days = (y1 - y0).days
        # Dasa-Bhukti periods and Pratyantaras in the year
        bhuktis, pratyantars = [], []
        for md in dasha:
            if parse(md['end']) <= y0 or parse(md['start']) >= y1:
                continue
            for b in md['subperiods']:
                s, e = parse(b['start']), parse(b['end'])
                if e <= y0 or s >= y1:
                    continue
                bhuktis.append(dict(dasa=md['lord'], bhukti=b['lord'], start=max(s, y0), end=min(e, y1),
                                    real_start=s, weight=(min(e, y1) - max(s, y0)).days / span_days))
                for p in b.get('pratyantars') or []:
                    ps, pe = parse(p['start']), parse(p['end'])
                    if pe > y0 and ps < y1:
                        pratyantars.append(dict(lord=p['lord'], start=max(ps, y0), end=min(pe, y1)))
        # Slow transits through the year
        jd0, jd1 = utc_to_jd(y0.astimezone(timezone.utc)), utc_to_jd(y1.astimezone(timezone.utc))
        transit = {}
        for name, body in (('Jupiter', swe.JUPITER), ('Saturn', swe.SATURN), ('Rahu', swe.MEAN_NODE)):
            segs = _segments(body, jd0, jd1)
            transit[name] = [dict(sign=sign, weight=(e - s) / (jd1 - jd0), start=s,
                                  back=i > 0 and name != 'Rahu' and sign == (segs[i - 1][2] - 1) % 12)  # moving back a sign: retrograde
                             for i, (s, e, sign) in enumerate(segs)]
        running_cycles = [c for c in cycles if parse(c['start']) < y1 and parse(c['end']) > y0]

        # Scores
        score = {key: 0.0 for key, _, _ in AREAS}
        activated = {key: [] for key, _, _ in AREAS}
        for b in bhuktis:
            for lord, share in ((b['dasa'], 0.4), (b['bhukti'], 0.6)):
                houses = _houses_of(planets, lord, asc)
                q = _quality(planets, lord, asc)
                for key, area_houses, _ in AREAS:
                    if key == 'health':
                        if houses & {6, 8, 12}:
                            score[key] -= b['weight'] * share * (0.6 if q < 0 else 0.3)
                        elif houses & {1}:
                            score[key] += b['weight'] * share * max(q, 0)
                        continue
                    if houses & set(area_houses):
                        score[key] += b['weight'] * share * (0.4 + q)
                        if share == 0.6 and lord not in activated[key]:
                            activated[key].append(lord)
        for seg in transit['Jupiter']:
            from_moon = (seg['sign'] - moon) % 12 + 1
            from_lagna = (seg['sign'] - asc) % 12 + 1
            aspected = {(from_lagna + a - 2) % 12 + 1 for a in JUPITER_ASPECTS}
            for key, area_houses, _ in AREAS:
                if from_moon in JUPITER_GOOD:
                    score[key] += 0.25 * seg['weight']
                if aspected & set(area_houses):
                    score[key] += 0.35 * seg['weight']
        for seg in transit['Saturn']:
            from_moon = (seg['sign'] - moon) % 12 + 1
            if from_moon in SATURN_GOOD:
                score['career'] += 0.3 * seg['weight']
                score['money'] += 0.3 * seg['weight']
        for c in running_cycles:
            overlap = (min(parse(c['end']), y1) - max(parse(c['start']), y0)).days / span_days
            hit = {'sade_sati': dict(health=0.4, money=0.3, family=0.3, career=0.2),
                   'ashtama': dict(health=0.6, career=0.4, travel=0.2),
                   'kandaka': dict(career=0.3, family=0.3, health=0.2),
                   'ardhashtama': dict(health=0.3, family=0.2)}.get(c['kind'], {})
            for key, value in hit.items():
                score[key] -= value * overlap
        pending.append(dict(year=year, score=score, activated=activated, bhuktis=bhuktis, transit=transit,
                            running_cycles=running_cycles, pratyantars=pratyantars, y0=y0, y1=y1))

    # Rank each area's years against each other: the best third favourable, the hardest third careful,
    # so the forecast separates the better years from the harder ones instead of calling most alike
    def classify(values):
        ordered = sorted(values)
        hi, lo = ordered[2 * len(ordered) // 3], ordered[len(ordered) // 3 - 1]
        return lambda v: 'good' if v >= hi and v > 0.05 else ('care' if v <= lo and v < 0 else 'steady')
    by_area = {key: classify([d['score'][key] for d in pending]) for key, _, _ in AREAS}
    overall_rank = classify([sum(d['score'].values()) for d in pending])
    for d in pending:
        year, score, activated, bhuktis, transit = d['year'], d['score'], d['activated'], d['bhuktis'], d['transit']
        running_cycles, pratyantars, y0, y1 = d['running_cycles'], d['pratyantars'], d['y0'], d['y1']
        verdicts = {key: by_area[key](score[key]) for key in score}

        # Good and careful months from the Pratyantaras
        good_months, care_months = [], []
        for p in pratyantars:
            q = _quality(planets, p['lord'], asc)
            houses = _houses_of(planets, p['lord'], asc)
            if (p['end'] - p['start']).days < 12:
                continue
            if q >= 0.75 and not houses <= {6, 8, 12}:
                good_months.append(p)
            elif q <= -0.5 or houses & {8, 12} and q < 0.5:
                care_months.append(p)
        good_months = sorted(good_months, key=lambda p: p['start'])[:4]
        care_months = sorted(care_months, key=lambda p: p['start'])[:3]

        level = overall_rank(sum(score.values()))

        def text(lang):
            n, sn = names[lang], sign_names[lang]
            parts = []
            dasa_bits = []
            for b in bhuktis:
                starts_now = b['real_start'] >= y0
                when = {'en': f" from {b['start'].day} {_month(b['start'], 'en')}",
                        'ta': f" {b['start'].day} {_month(b['start'], 'ta')} முதல்",
                        'ml': f" {b['start'].day} {_month(b['start'], 'ml')} മുതൽ"}[lang] if starts_now else ''
                dasa_bits.append({'en': f"{n(b['dasa'])} Dasa, {n(b['bhukti'])} Bhukti{when}",
                                  'ta': f"{n(b['dasa'])} தசை, {n(b['bhukti'])} புக்தி{when}",
                                  'ml': f"{n(b['dasa'])} ദശ, {n(b['bhukti'])} ഭുക്തി{when}"}[lang])
            parts.append('; '.join(dasa_bits) + '.')
            moves = []
            for g in ('Jupiter', 'Saturn', 'Rahu'):
                for seg in transit[g][1:]:
                    d = datetime.fromtimestamp((seg['start'] - 2440587.5) * 86400, tz)
                    from_moon = (seg['sign'] - moon) % 12 + 1
                    back = {'en': ', retrograde', 'ta': ', வக்ரமாக', 'ml': ', വക്രമായി'}[lang] if seg['back'] else ''
                    moves.append({'en': f"{g} enters {sn[seg['sign']]} ({from_moon} from the Moon{back}) in {_month(d, 'en')}",
                                  'ta': f"{_month(d, 'ta')}-இல் {n(g)} {sn[seg['sign']]} ராசிக்கு (சந்திரனிலிருந்து {from_moon}{back})",
                                  'ml': f"{_month(d, 'ml')}-ൽ {n(g)} {sn[seg['sign']]} രാശിയിലേക്ക് (ചന്ദ്രനിൽ നിന്ന് {from_moon}{back})"}[lang])
            if moves:
                parts.append('; '.join(moves) + '.')
            for c in running_cycles:
                w = CYCLE_WORDS.get(c['kind'])
                if w:
                    parts.append({'en': f"{w[0]} runs until {c['end'][:7]}.", 'ta': f"{w[1]} {c['end'][:7]} வரை.",
                                  'ml': f"{w[2]} {c['end'][:7]} വരെ."}[lang])
            for key, _, label in AREAS:
                i = {'en': 0, 'ta': 1, 'ml': 2}[lang]
                via = activated[key][:2]
                basis = ({'en': f" ({', '.join(n(g) for g in via)} Bhukti)", 'ta': f" ({', '.join(n(g) for g in via)} புக்தி)",
                          'ml': f" ({', '.join(n(g) for g in via)} ഭുക്തി)"}[lang] if via and key != 'health' else '')
                parts.append(f"{label[i]}{basis}: {AREA_TEXT[key][verdicts[key]][i]}")
            if good_months:
                parts.append({'en': 'Good months: ', 'ta': 'நல்ல மாதங்கள்: ', 'ml': 'നല്ല മാസങ്ങൾ: '}[lang]
                             + ', '.join(f"{_span(p['start'], p['end'], lang)} ({n(p['lord'])})" for p in good_months) + '.')
            if care_months:
                parts.append({'en': 'Careful months: ', 'ta': 'கவனமான மாதங்கள்: ', 'ml': 'ശ്രദ്ധിക്കേണ്ട മാസങ്ങൾ: '}[lang]
                             + ', '.join(f"{_span(p['start'], p['end'], lang)} ({n(p['lord'])})" for p in care_months) + '.')
            return '\n'.join(parts)

        main = max(bhuktis, key=lambda b: b['weight']) if bhuktis else None
        head = {lang: (f"{year}: {names[lang](main['dasa'])}–{names[lang](main['bhukti'])}" if main else str(year))
                for lang in ('en', 'ta', 'ml')}
        verdict_card = {'good': 'good', 'steady': 'mixed', 'care': 'bad'}[level]
        cards.append(card('📅', head['en'], head['ta'], text('en'), text('ta'),
                          f"Overall: {LEVELS[level][1]}", f"மொத்தம்: {LEVELS[level][2]}", verdict=verdict_card,
                          title_ml=head['ml'], body_ml=text('ml'), sub_ml=f"മൊത്തം: {LEVELS[level][3]}"))
        rows.append([str(year),
                     ('–'.join(dict.fromkeys(b['bhukti'] for b in bhuktis)),
                      '–'.join(dict.fromkeys(PLANET_TAMIL[b['bhukti']] for b in bhuktis)),
                      '–'.join(dict.fromkeys(PLANET_ML[b['bhukti']] for b in bhuktis)))]
                    + [(f"{LEVELS[verdicts[k]][0]} {LEVELS[verdicts[k]][1]}", f"{LEVELS[verdicts[k]][0]} {LEVELS[verdicts[k]][2]}",
                        f"{LEVELS[verdicts[k]][0]} {LEVELS[verdicts[k]][3]}") for k, _, _ in AREAS])
        results.append(dict(year=year, level=level, scores={k: round(v, 2) for k, v in score.items()}, verdicts=verdicts,
                            bhuktis=[dict(dasa=b['dasa'], bhukti=b['bhukti'], start=b['start'].date().isoformat(),
                                          end=b['end'].date().isoformat()) for b in bhuktis],
                            good_months=[dict(lord=p['lord'], start=p['start'].date().isoformat(), end=p['end'].date().isoformat())
                                         for p in good_months],
                            care_months=[dict(lord=p['lord'], start=p['start'].date().isoformat(), end=p['end'].date().isoformat())
                                         for p in care_months]))
    head = [('Year', 'ஆண்டு', 'വർഷം'), ('Bhuktis', 'புக்திகள்', 'ഭുക്തികൾ')] + [label for _, _, label in AREAS]
    return chapter(
        'yearly', f'Year-by-Year Forecast ({now.year}–{now.year + years - 1})', f'ஆண்டுவாரி பலன் ({now.year}–{now.year + years - 1})',
        'Each year from the Dasa-Bhukti periods running in it, the moves of Saturn, Jupiter and Rahu and the Saturn cycles, '
        'for career, money, family, health and travel, with the good and careful months from the Pratyantara periods.',
        'ஒவ்வொரு ஆண்டும்: அதில் நடக்கும் தசா புக்திகள், சனி, குரு, ராகு பெயர்ச்சிகள், சனி சுழற்சிகள் வழியாகத் தொழில், பணம், குடும்பம், '
        'உடல்நலம், பயணம்; பிரத்யந்தர காலங்களிலிருந்து நல்ல, கவனமான மாதங்கள்.',
        cards=cards, tables=[table('Year at a glance', 'ஆண்டுச் சுருக்கம்', head, rows, title_ml='വർഷ സംഗ്രഹം')],
        cards_first=False,
        title_ml=f'വർഷംതോറുമുള്ള ഫലം ({now.year}–{now.year + years - 1})',
        intro_ml=('ഓരോ വർഷവും: അതിൽ നടക്കുന്ന ദശാ-ഭുക്തികൾ, ശനി, വ്യാഴം, രാഹു എന്നിവയുടെ രാശിമാറ്റങ്ങൾ, ശനിചക്രങ്ങൾ എന്നിവയിലൂടെ തൊഴിൽ, '
                  'ധനം, കുടുംബം, ആരോഗ്യം, യാത്ര; പ്രത്യന്തര കാലങ്ങളിൽ നിന്ന് നല്ലതും ശ്രദ്ധിക്കേണ്ടതുമായ മാസങ്ങൾ.'),
        years=results)
