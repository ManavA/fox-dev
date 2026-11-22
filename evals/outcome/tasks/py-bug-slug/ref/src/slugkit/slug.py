"""URL slug generation."""
import re
import unicodedata
from typing import Optional


def slugify(text: str, max_length: Optional[int] = None, sep: str = "-") -> str:
    """Lower-case ``text`` and join its words with ``sep``.

    ``max_length`` caps the length of the result.
    """
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", sep, ascii_text.lower()).strip(sep)
    if max_length is not None:
        slug = slug[:max_length].rstrip(sep)
    return slug
