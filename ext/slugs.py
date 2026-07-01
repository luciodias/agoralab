import re
import functools
import unicodedata

RE_HTML_TAGS = re.compile(r"</?[^>]*>", re.UNICODE)
RE_INVALID_SLUG_CHAR = re.compile(r"[^\w\- ]", re.UNICODE)
RE_WHITESPACE = re.compile(r"\s", re.UNICODE)

TRANSLIT_TABLE = str.maketrans({
    "á": "a", "à": "a", "â": "a", "ã": "a", "ä": "a",
    "é": "e", "è": "e", "ê": "e", "ë": "e",
    "í": "i", "ì": "i", "î": "i", "ï": "i",
    "ó": "o", "ò": "o", "ô": "o", "õ": "o", "ö": "o",
    "ú": "u", "ù": "u", "û": "u", "ü": "u",
    "ç": "c",
    "ñ": "n",
})

def _make_slug(text, sep, **kwargs):
    slug = unicodedata.normalize("NFC", text.lower())
    slug = RE_HTML_TAGS.sub("", slug)
    slug = slug.translate(TRANSLIT_TABLE)
    slug = RE_INVALID_SLUG_CHAR.sub("", slug)
    slug = slug.strip()
    slug = RE_WHITESPACE.sub(sep, slug)
    return slug

def _make_slug_short(text, sep, **kwargs):
    words = _make_slug(text, sep, **kwargs).split(sep)
    return sep.join(words[:8])

def slugify(**kwargs):
    if kwargs.get("short"):
        return functools.partial(_make_slug_short, **kwargs)
    return functools.partial(_make_slug, **kwargs)
