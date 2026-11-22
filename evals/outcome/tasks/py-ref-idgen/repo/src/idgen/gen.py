"""Sequential identifier generation (module-level state)."""
_prefix = "id"
_counter = 0
_issued = []


def configure(prefix, start=1):
    """Set the prefix and the number the next id will carry. Forgets issued ids."""
    global _prefix, _counter, _issued
    if not prefix or not prefix.isidentifier():
        raise ValueError("prefix must be a non-empty identifier")
    if start < 0:
        raise ValueError("start must be >= 0")
    _prefix = prefix
    _counter = start - 1
    _issued = []


def next_id():
    """Return the next id, e.g. ``id-1``, ``id-2``."""
    global _counter
    _counter += 1
    value = "%s-%d" % (_prefix, _counter)
    _issued.append(value)
    return value


def issued():
    """Ids handed out since the last configure/reset, oldest first."""
    return list(_issued)


def reset():
    """Back to the defaults: prefix ``id``, counting from 1, nothing issued."""
    configure("id", 1)
