"""Verification marks that people choose to share, and the accuracy report built from them.

A shared entry keeps only what the marks say about the rules: each statement's type, confidence and
right-or-wrong mark; for past events with a real date, whether that date fell inside the predicted
Dasa-Bhukti window and inside its Pratyantara months; and the predicted and real sibling counts. It
keeps no name, birth date, time or place: the birth details are used in memory to check event dates
against the windows and are then dropped. Entries are JSON lines in JOROSCOPE_DATA_DIR (by default
~/.local/share/joroscope); a person sharing again from the same browser replaces their entry.
"""
import json
import os
import re
import threading
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .. import __version__

LOCK = threading.Lock()
SIBLING_KEYS = {11: ('elder_brothers', 'elder_sisters'), 3: ('younger_brothers', 'younger_sisters')}


def data_file():
    base = Path(os.environ.get('JOROSCOPE_DATA_DIR') or Path.home() / '.local' / 'share' / 'joroscope')
    return base / 'feedback.jsonl'


def owner_passcode():
    return os.environ.get('JOROSCOPE_OWNER_PASSCODE') or ''


def _in(date, start, end):
    return start[:10] <= date <= end[:10]


def _days(a, b):
    return max(0, (datetime.fromisoformat(b[:10]) - datetime.fromisoformat(a[:10])).days)


def coverage(chart, statement, now=None):
    """The share of the eligible age range that a statement's windows (and their Pratyantara months)
    cover: the chance that a real date falls inside by luck alone, the baseline a hit rate is judged against."""
    from .readings.parisodhanai import EVENT_AGES
    birth = datetime.fromisoformat(chart['utc'])
    now = now or datetime.now(timezone.utc)
    low, high = EVENT_AGES.get(statement.get('event'), (0, 90))
    start = birth + timedelta(days=365.25 * low)
    end = min(birth + timedelta(days=365.25 * high), now)
    total = (end - start).days
    if total <= 0:
        return None, None
    clip = lambda a, b: _days(max(a, start.date().isoformat()), min(b, end.date().isoformat()))
    windows = statement.get('windows') or []
    in_windows = sum(clip(w['start'], w['end']) for w in windows)
    in_months = sum(clip(m['start'], m['end']) for w in windows for m in w.get('months') or [])
    return round(min(1.0, in_windows / total), 4), round(min(1.0, in_months / total), 4)


def entry_from_marks(chart, marks, submission_id):
    """The anonymous record of one person's marks against their chart."""
    if not re.fullmatch(r'[A-Za-z0-9_-]{8,64}', str(submission_id or '')):
        raise ValueError('Missing submission id.')
    statements = (chart.get('predictions') or {}).get('parisodhanai', {}).get('statements', [])
    items = []
    for s in statements:
        m = (marks or {}).get(s['key']) or {}
        mark = m.get('mark') if m.get('mark') in ('right', 'wrong') else None
        date = str(m.get('date') or '')[:10]
        date = date if re.fullmatch(r'\d{4}-\d{2}-\d{2}', date) else None
        if not mark and not date:
            continue
        item = dict(key=s['key'], topic=s['topic'], confidence=s['confidence'], mark=mark)
        if s.get('event') and date:
            windows = s.get('windows') or []
            item['in_window'] = any(_in(date, w['start'], w['end']) for w in windows)
            item['in_months'] = any(_in(date, mo['start'], mo['end']) for w in windows for mo in w.get('months') or [])
            item['coverage'], item['months_coverage'] = coverage(chart, s)
        items.append(item)
    # Past years rated against memory: only each year's rank band and the mark, never the year itself
    years = []
    year_marks = (marks or {}).get('years') or {}
    if year_marks:
        from .readings.yearly import calculate_past_years
        past = calculate_past_years(chart)
        for y in (past or {}).get('years') or []:
            mark = year_marks.get(str(y['year']))
            if mark in ('matched', 'partly', 'no'):
                years.append(dict(level=y['level'], mark=mark))
    siblings = []
    family = (marks or {}).get('family') or {}
    for s in statements:
        if s['topic'] != 'siblings':
            continue
        b_key, s_key = SIBLING_KEYS[s['house']]
        try:
            actual = (int(family.get(b_key)), int(family.get(s_key)))
        except (TypeError, ValueError):
            continue
        siblings.append(dict(house=s['house'], confidence=s['confidence'], predicted=[s['brothers'], s['sisters']], actual=list(actual)))
    if not items and not siblings and not years:
        raise ValueError('Mark at least one statement before sharing.')
    return dict(id=submission_id, date=datetime.now(timezone.utc).date().isoformat(), version=__version__,
                items=items, siblings=siblings, years=years)


def save(entry):
    path = data_file()
    with LOCK:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')


def load():
    """The latest entry from each browser."""
    path = data_file()
    latest = {}
    with LOCK:
        if not path.exists():
            return []
        for line in path.read_text(encoding='utf-8').splitlines():
            try:
                e = json.loads(line)
            except ValueError:
                continue
            latest[e.get('id')] = e
    return list(latest.values())


def report():
    """Hit rates by statement type and confidence, from every shared entry, each beside its chance
    baseline (the share of the eligible years the windows covered) and the lift over it."""
    entries = load()
    by_key = defaultdict(lambda: dict(right=0, wrong=0, dated=0, in_window=0, in_months=0, coverage=[], months_coverage=[]))
    by_conf = defaultdict(lambda: dict(right=0, wrong=0))
    sib = defaultdict(lambda: dict(n=0, exact=0, total=0))
    years = defaultdict(lambda: dict(matched=0, partly=0, no=0))
    for e in entries:
        for i in e.get('items', []):
            k = by_key[i['key']]
            if i.get('mark'):
                k[i['mark']] += 1
                by_conf[i['confidence']][i['mark']] += 1
            if 'in_window' in i:
                k['dated'] += 1
                k['in_window'] += bool(i['in_window'])
                k['in_months'] += bool(i['in_months'])
                if i.get('coverage') is not None:
                    k['coverage'].append(i['coverage'])
                    k['months_coverage'].append(i.get('months_coverage') or 0)
        for s in e.get('siblings', []):
            g = sib['elder' if s['house'] == 11 else 'younger']
            g['n'] += 1
            g['exact'] += s['predicted'] == s['actual']
            g['total'] += sum(s['predicted']) == sum(s['actual'])
        for y in e.get('years', []):
            if y.get('mark') in ('matched', 'partly', 'no'):
                years[y['level']][y['mark']] += 1
    rate = lambda a, b: round(100 * a / b) if b else None
    mean_pct = lambda xs: round(100 * sum(xs) / len(xs)) if xs else None
    lift = lambda hit, base: round(hit / base, 1) if hit is not None and base else None

    def statement_row(k, v):
        base, base_months = mean_pct(v['coverage']), mean_pct(v['months_coverage'])
        in_window, in_months = rate(v['in_window'], v['dated']), rate(v['in_months'], v['dated'])
        return dict(key=k, right=v['right'], wrong=v['wrong'], right_pct=rate(v['right'], v['right'] + v['wrong']),
                    dated=v['dated'], in_window_pct=in_window, in_months_pct=in_months,
                    baseline_pct=base, months_baseline_pct=base_months, lift=lift(in_window, base), months_lift=lift(in_months, base_months))

    return dict(
        entries=len(entries),
        statements=[statement_row(k, v) for k, v in sorted(by_key.items())],
        confidence=[dict(level=c, right=v['right'], wrong=v['wrong'], right_pct=rate(v['right'], v['right'] + v['wrong']))
                    for c, v in sorted(by_conf.items())],
        siblings=[dict(group=g, count=v['n'], exact_pct=rate(v['exact'], v['n']), total_pct=rate(v['total'], v['n']))
                  for g, v in sorted(sib.items())],
        years=[dict(level=level, count=sum(v.values()), matched_pct=rate(v['matched'], sum(v.values())),
                    partly_pct=rate(v['partly'], sum(v.values())), no_pct=rate(v['no'], sum(v.values())))
               for level, v in sorted(years.items(), key=lambda kv: ['good', 'steady', 'care'].index(kv[0]) if kv[0] in ('good', 'steady', 'care') else 9)])


PUBLIC_MIN = 20  # aggregates with fewer marks than this stay with the owner


def public_report(min_n=PUBLIC_MIN):
    """What everyone may see: only aggregates built from at least min_n marks, so no small group
    can be traced to anyone, with the baselines that make the hit rates honest."""
    r = report()
    return dict(
        entries=r['entries'], min_n=min_n,
        statements=[s for s in r['statements'] if s['right'] + s['wrong'] >= min_n or s['dated'] >= min_n],
        confidence=[c for c in r['confidence'] if c['right'] + c['wrong'] >= min_n],
        siblings=[s for s in r['siblings'] if s['count'] >= min_n],
        years=[y for y in r['years'] if y['count'] >= min_n])
