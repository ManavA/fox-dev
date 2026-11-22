"""Shared helpers for the outcome eval: task loading, repo prep, test running, result parsing."""
import json, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASKS = os.path.join(HERE, "tasks")
JUNK = ["__pycache__", ".pytest_cache", ".coverage", "node_modules", ".mypy_cache", ".ruff_cache", "coverage", ".claude", "*.pyc", "lcov.info"]
PYENV = os.environ.get("OUTCOME_PYENV", os.path.join(HERE, "pyenv"))
SHARED_NODE = os.environ.get("OUTCOME_NODE_MODULES", os.path.join(HERE, "ts-deps", "node_modules"))


def task(tid):
    m = json.load(open(f"{TASKS}/{tid}/meta.json"))
    m["dir"] = f"{TASKS}/{tid}"
    m["prompt"] = open(f"{TASKS}/{tid}/prompt.txt").read()
    return m


def all_tasks():
    return sorted(d for d in os.listdir(TASKS) if os.path.exists(f"{TASKS}/{d}/meta.json"))


def sh(cmd, cwd, env=None, timeout=120, input=None):
    e = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONPATH="")
    e["PATH"] = PYENV + "/bin:" + e["PATH"]
    e.update(env or {})
    try:
        p = subprocess.run(cmd, shell=isinstance(cmd, str), cwd=cwd, env=e, capture_output=True, text=True, timeout=timeout, input=input)
        return p.returncode, p.stdout + p.stderr
    except subprocess.TimeoutExpired as ex:
        return 124, (ex.stdout or b"").decode() if isinstance(ex.stdout, bytes) else (ex.stdout or "")


def prepare_repo(t, dest):
    """Fresh copy of the task repo with a git baseline commit. TS repos get the shared node_modules symlinked."""
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(f"{t['dir']}/repo", dest)
    with open(f"{dest}/.gitignore", "a") as f:
        f.write("\n".join(["__pycache__/", ".pytest_cache/", ".coverage", "node_modules", ".mypy_cache/", ".ruff_cache/", "coverage/", "lcov.info", "*.pyc", ""]))
    if t["lang"] == "ts":
        os.symlink(SHARED_NODE, f"{dest}/node_modules")
    g = lambda *a: subprocess.run(["git", *a], cwd=dest, capture_output=True, text=True, env=dict(os.environ, GIT_AUTHOR_NAME="e", GIT_AUTHOR_EMAIL="e@e", GIT_COMMITTER_NAME="e", GIT_COMMITTER_EMAIL="e@e"))
    g("init", "-q"); g("add", "-A"); g("commit", "-q", "-m", "baseline"); g("tag", "outcome-base")
    return dest


def apply_overlay(src_dir, dest):
    for root, _, files in os.walk(src_dir):
        for f in files:
            p = os.path.join(root, f); rel = os.path.relpath(p, src_dir)
            os.makedirs(os.path.dirname(os.path.join(dest, rel)) or dest, exist_ok=True)
            shutil.copy(p, os.path.join(dest, rel))


def parse_counts(out, lang):
    """-> (passed, failed). pytest summary or node TAP summary."""
    if lang == "py":
        p = sum(int(x) for x in re.findall(r"(\d+) passed", out)); f = sum(int(x) for x in re.findall(r"(\d+) (?:failed|error)", out))
        return p, f
    p = re.search(r"^# pass (\d+)", out, re.M); f = re.search(r"^# fail (\d+)", out, re.M)
    return (int(p.group(1)) if p else 0, int(f.group(1)) if f else 0)


def test_command(t, paths=None, reporter=True):
    if t["lang"] == "py":
        return "python -m pytest -q -p no:cacheprovider " + " ".join(paths or [])
    return "node --test --test-reporter=tap " + " ".join(paths or ["test/"])


def run_tests(t, repo, paths=None, timeout=120):
    rc, out = sh(test_command(t, paths), repo, timeout=timeout)
    p, f = parse_counts(out, t["lang"])
    return {"rc": rc, "passed": p, "failed": f, "out": out[-3000:]}


def install_hidden(t, repo):
    dest = f"{repo}/{t['hidden_dest']}"
    shutil.rmtree(dest, ignore_errors=True)
    shutil.copytree(f"{t['dir']}/hidden", dest, ignore=shutil.ignore_patterns("mutants*"))
    return dest
