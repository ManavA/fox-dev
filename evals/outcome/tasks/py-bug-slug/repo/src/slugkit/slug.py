"""URL slug generation."""
import re
from typing import Optional


def slugify(text: str, max_length: Optional[int] = None, sep: str = "-") -> str:
    """Lower-case ``text`` and join its words with ``sep``.

    ``max_length`` caps the length of the result.
    """
    slug = re.sub(r"[^a-z0-9]", sep, text.lower())
    if max_length is not None:
        slug = slug[:max_length]
    return slug
