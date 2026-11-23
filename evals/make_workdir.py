#!/usr/bin/env python3
"""Create a firing-eval workdir. usage: make_workdir.py <workdir>
Makes <workdir>/home (a scratch HOME holding only a copy of the Claude Code OAuth credentials file,
so no user settings, plugins, CLAUDE.md or memory leak in), <workdir>/repo (a tiny Python items
service as a git repo, with a feature/pagination branch) and <workdir>/runs."""
import os, shutil, subprocess, sys, textwrap

W = os.path.abspath(sys.argv[1])
home, repo = f"{W}/home", f"{W}/repo"
os.makedirs(f"{home}/.claude", exist_ok=True); os.makedirs(f"{W}/runs", exist_ok=True)
cred = os.path.expanduser("~/.claude/.credentials.json")
if os.path.exists(cred):
    shutil.copy(cred, f"{home}/.claude/.credentials.json"); os.chmod(f"{home}/.claude/.credentials.json", 0o600)
else:
    print("no credentials file found; log in under the scratch HOME before running", file=sys.stderr)
if os.path.exists(repo): shutil.rmtree(repo)

FILES = {
"README.md": """\
# items

A tiny items service: an in-memory store, a request handler, pagination and a TTL cache.

Run the tests with `python -m pytest`.
""",
"app.py": """\
from cache import TTLCache
from utils import paginate

ITEMS = {
    1: {"id": 1, "name": "apple"},
    2: {"id": 2, "name": "pear"},
    3: {"id": 3, "name": "plum"},
}

_cache = TTLCache(ttl=30)


def handle(request):
    \"\"\"Dispatch a request dict to a handler.\"\"\"
    user = request["user"]
    action = request.get("action", "list")
    if action == "get":
        return get_item(request["id"])
    return list_items(request.get("page", 0), request.get("size", 10))


def get_item(item_id):
    # TODO: return a 404-style error for missing ids
    return ITEMS[item_id]


def list_items(page=0, size=10):
    \"\"\"Return one page of items, newest id first, cached for ttl seconds.\"\"\"
    key = (page, size)
    hit = _cache.get(key)
    if hit is not None:
        return hit
    items = sorted(ITEMS.values(), key=lambda i: -i["id"])
    result = paginate(items, page=page, size=size)
    _cache.set(key, result)
    return result
""",
"utils.py": """\
def paginate(items, page=1, size=10):
    \"\"\"Return the given 1-based page of items.\"\"\"
    start = page * size
    return items[start:start + size]
""",
"cache.py": """\
import time


class TTLCache:
    def __init__(self, ttl):
        self.ttl = ttl
        self._data = {}

    def set(self, key, value):
        self._data[key] = (value, time.time())

    def get(self, key):
        entry = self._data.get(key)
        if entry is None:
            return None
        value, stored = entry
        if time.time() - stored > self.ttl:
            del self._data[key]
            return None
        return value
""",
"tests/test_cache.py": """\
import time

from cache import TTLCache


def test_set_get():
    c = TTLCache(ttl=10)
    c.set("a", 1)
    assert c.get("a") == 1


def test_expiry():
    c = TTLCache(ttl=0.01)
    c.set("a", 1)
    time.sleep(0.01)
    assert c.get("a") is None
""",
"tests/test_utils.py": """\
from utils import paginate


def test_first_page():
    assert paginate([1, 2, 3, 4], page=1, size=2) == [1, 2]
""",
"SPEC.md": """\
# Pagination spec (agreed)

- `paginate(items, page, size)`: pages are 1-based; page 1 is the first `size` items.
- `list_items` and `handle` take `page` and `size` from the request, defaulting to 1 and 10.
- A page past the end returns an empty list; `size` must be between 1 and 100, else a 400-style error.
- The HTTP layer returns `{"items": [...], "page": n, "total": t}`.
- Tests cover the first page, the last partial page, a page past the end and the size limits.
""",
"templates/items.html": """\
<html>
<head><title>Items</title></head>
<body>
<div class="top"><b>Items</b> <span onclick="location='/new'">new</span></div>
<table>
{% for item in items %}<tr><td>{{ item.id }}</td><td>{{ item.name }}</td><td><span onclick="del({{ item.id }})">x</span></td></tr>{% endfor %}
</table>
<div><span onclick="prev()">&lt;</span> <span onclick="next()">&gt;</span></div>
</body>
</html>
""",
".claude/settings.json": "{}\n",
}
for path, body in FILES.items():
    os.makedirs(os.path.dirname(f"{repo}/{path}") or repo, exist_ok=True)
    open(f"{repo}/{path}", "w").write(body)

def git(*a): subprocess.run(["git", "-C", repo, *a], check=True, capture_output=True)
git("init", "-q", "-b", "main"); git("config", "user.email", "eval@example.com"); git("config", "user.name", "eval")
git("add", "-A"); git("commit", "-qm", "Initial items service")
git("checkout", "-qb", "feature/pagination")
open(f"{repo}/utils.py", "w").write(FILES["utils.py"].replace("start = page * size", "start = (page - 1) * size"))
git("commit", "-qam", "Fix paginate off-by-one: pages are 1-based")
git("checkout", "-q", "main")
print(W)
