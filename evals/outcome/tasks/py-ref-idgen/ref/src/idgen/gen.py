"""Sequential identifier generation."""


class IdGenerator:
    """Hands out ids like ``id-1``, ``id-2``. Each instance has its own sequence."""

    def __init__(self, prefix="id", start=1):
        self.configure(prefix, start)

    def configure(self, prefix, start=1):
        """Set the prefix and the number the next id will carry. Forgets issued ids."""
        if not prefix or not prefix.isidentifier():
            raise ValueError("prefix must be a non-empty identifier")
        if start < 0:
            raise ValueError("start must be >= 0")
        self._prefix = prefix
        self._counter = start - 1
        self._issued = []

    def next_id(self):
        """Return the next id, e.g. ``id-1``, ``id-2``."""
        self._counter += 1
        value = "%s-%d" % (self._prefix, self._counter)
        self._issued.append(value)
        return value

    def issued(self):
        """Ids handed out since the last configure/reset, oldest first."""
        return list(self._issued)

    def reset(self):
        """Back to the defaults: prefix ``id``, counting from 1, nothing issued."""
        self.configure("id", 1)


_default = IdGenerator()

configure = _default.configure
next_id = _default.next_id
issued = _default.issued
reset = _default.reset
