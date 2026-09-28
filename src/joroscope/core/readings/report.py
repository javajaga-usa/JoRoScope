"""A common shape for the newer report chapters, so the page and the printed report draw them
with one renderer: a chapter has an introduction, reading cards and optional tables, each with
English and Tamil text.

    chapter(key, title, intro, cards=[card(...)], tables=[table(...)])
"""


def pair(en, ta):
    return {'en': en, 'ta': ta}


def card(icon, title_en, title_ta, body_en, body_ta, sub_en='', sub_ta='', verdict=None):
    """A reading card; verdict is 'good', 'mixed' or 'bad' when the card judges something."""
    return {'icon': icon, 'title': pair(title_en, title_ta), 'sub': pair(sub_en, sub_ta),
            'body': pair(body_en, body_ta), 'verdict': verdict}


def table(title_en, title_ta, head, rows):
    """head: [(en, ta), ...]; rows: lists of cells, each a string or an (en, ta) pair."""
    cell = lambda c: pair(*c) if isinstance(c, tuple) else pair(str(c), str(c))
    return {'title': pair(title_en, title_ta), 'head': [pair(*h) for h in head],
            'rows': [[cell(c) for c in row] for row in rows]}


def chapter(key, title_en, title_ta, intro_en, intro_ta, cards=(), tables=(), **extra):
    return dict(key=key, title=pair(title_en, title_ta), intro=pair(intro_en, intro_ta),
                cards=list(cards), tables=list(tables), **extra)
