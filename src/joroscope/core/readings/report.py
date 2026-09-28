"""A common shape for the newer report chapters, so the page and the printed report draw them
with one renderer: a chapter has an introduction, reading cards and optional tables, each with
English, Tamil and (where written) Malayalam text.

    chapter(key, title, intro, cards=[card(...)], tables=[table(...)])
"""


def pair(en, ta, ml=None):
    out = {'en': en, 'ta': ta}
    if ml is not None:
        out['ml'] = ml
    return out


def card(icon, title_en, title_ta, body_en, body_ta, sub_en='', sub_ta='', verdict=None,
         title_ml=None, body_ml=None, sub_ml=None):
    """A reading card; verdict is 'good', 'mixed' or 'bad' when the card judges something."""
    return {'icon': icon, 'title': pair(title_en, title_ta, title_ml), 'sub': pair(sub_en, sub_ta, sub_ml),
            'body': pair(body_en, body_ta, body_ml), 'verdict': verdict}


def table(title_en, title_ta, head, rows, title_ml=None):
    """head: [(en, ta[, ml]), ...]; rows: lists of cells, each a string or an (en, ta[, ml]) tuple."""
    cell = lambda c: pair(*c) if isinstance(c, tuple) else pair(str(c), str(c))
    return {'title': pair(title_en, title_ta, title_ml), 'head': [pair(*h) for h in head],
            'rows': [[cell(c) for c in row] for row in rows]}


def chapter(key, title_en, title_ta, intro_en, intro_ta, cards=(), tables=(), title_ml=None, intro_ml=None, **extra):
    return dict(key=key, title=pair(title_en, title_ta, title_ml), intro=pair(intro_en, intro_ta, intro_ml),
                cards=list(cards), tables=list(tables), **extra)
