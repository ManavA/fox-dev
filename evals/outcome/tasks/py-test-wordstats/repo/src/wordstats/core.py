"""Word statistics for plain text."""
import math
import re
from collections import Counter

_WORD = re.compile(r"[a-z0-9']+")
STOPWORDS = frozenset({"a", "an", "the", "and", "or", "of", "to", "in", "is", "it"})


def tokenize(text, keep_stopwords=True):
    """Lower-case words made of letters, digits and apostrophes; edge apostrophes are dropped."""
    words = [w.strip("'") for w in _WORD.findall(text.lower())]
    words = [w for w in words if w]
    if not keep_stopwords:
        words = [w for w in words if w not in STOPWORDS]
    return words


def word_freq(text, keep_stopwords=True):
    """Map each word to the number of times it occurs."""
    return dict(Counter(tokenize(text, keep_stopwords)))


def top_words(text, n=10, keep_stopwords=False):
    """The ``n`` most frequent words as ``(word, count)``; ties are broken alphabetically."""
    if n < 0:
        raise ValueError("n must be >= 0")
    freq = word_freq(text, keep_stopwords)
    ranked = sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))
    return ranked[:n]


def sentences(text):
    """Split on ., ! or ? followed by whitespace; empty pieces are dropped."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p]


def avg_sentence_length(text):
    """Mean number of words per sentence; 0.0 for text without sentences."""
    sents = sentences(text)
    if not sents:
        return 0.0
    counts = [len(tokenize(s)) for s in sents]
    return sum(counts) / len(counts)


def reading_time_minutes(text, wpm=200):
    """Whole minutes needed to read ``text`` (rounded up); 0 for no words."""
    if wpm <= 0:
        raise ValueError("wpm must be positive")
    words = len(tokenize(text))
    return math.ceil(words / wpm) if words else 0
