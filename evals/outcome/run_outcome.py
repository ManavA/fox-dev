#!/usr/bin/env python3
"""Outcome eval driver. One isolated `claude -p` run per (task, arm, rep), then mechanical grading and one blind judge call.

usage: run_outcome.py --work DIR [--tasks a,b] [--arms none,current,foxdev] [--reps N] [--cap USD] [--par N] [--turns N] [--run-cap USD]
DIR holds home/ (scratch HOME with only OAuth credentials) and receives runs/<task>__<arm>__r<rep>/.
Arms: none = no plugins; current = superpowers + mattpocock-skills from the plugin cache; foxdev = this repo's plugin/.
Halts on rate limits / auth errors, permission denials or when the total cost cap is reached."""
import argparse, json, os, re, shutil, subprocess, sys, threading, time
from concurrent.futures import ThreadPoolExecutor
from common import *
import grade_lib as G

ap = argparse.ArgumentParser()
ap.add_argument("--work", required=True); ap.add_argument("--tasks"); ap.add_argument("--arms", default="none,current,foxdev")
ap.add_argument("--reps", type=int, default=1); ap.add_argument("--rep-start", type=int, default=1); ap.add_argument("--cap", type=float, default=50.0)
ap.add_argument("--par", type=int, default=3); ap.add_argument("--turns", type=int, default=60); ap.add_argument("--run-cap", type=float, default=1.5)
ap.add_argument("--no-judge", action="store_true")
A = ap.parse_args()
W = os.path.abspath(A.work)
PC = os.path.expanduser("~/.claude/plugins/cache/claude-plugins-official")  # read-only plugin cache of the real HOME
PLUGINS = {"none": [], "current": [f"{PC}/superpowers/7.0.0", f"{PC}/mattpocock-skills/1.3.1"], "foxdev": [os.path.join(os.path.dirname(HERE), "..", "plugin")]}
PLUGINS["foxdev"] = [os.path.normpath(p) for p in PLUGINS["foxdev"]]
MODEL = "claude-sonnet-5-5"; JUDGE_MODEL = "claude-opus-5-5"
TOOLS = "Read,Edit,Write,Bash,Grep,Glob,Skill,Agent"
bins = [PYENV + "/bin", os.path.expanduser("~/.local/bin"), os.path.dirname(shutil.which("node") or "/usr/bin/node"), "/usr/bin", "/bin"]
ENV = {"HOME": f"{W}/home", "USER": "eval", "PATH": ":".join(dict.fromkeys(bins)), "LANG": "C.UTF-8", "TERM": "dumb", "PYTHONDONTWRITEBYTECODE": "1", "PIP_REQUIRE_VIRTUALENV": "1",
       "GIT_AUTHOR_NAME": "eval", "GIT_AUTHOR_EMAIL": "eval@example.invalid", "GIT_COMMITTER_NAME": "eval", "GIT_COMMITTER_EMAIL": "eval@example.invalid", "CI": "1",
       "CLAUDE_CODE_DISABLE_CLAUDE_MDS": "1", "CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1", "DISABLE_AUTOUPDATER": "1", "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1", "ENABLE_CLAUDEAI_MCP_SERVERS": "false"}
LIM = re.compile(r"(usage limit|rate.?limit|\b429\b|overloaded|quota|limit reached|too many requests|credit balance|authentication_error|oauth|unauthori[sz]ed)", re.I)
lock = threading.Lock(); spent = [0.0]; halt = [None]

PROMPT = ("You are working in the repository in the current directory. Tests: Python repos use `python -m pytest`; TypeScript repos use `node --test test/` and `npm run typecheck`.\n\n{task}")

JUDGE = """You are a strict senior reviewer. Below is a task given to an engineer and the diff they produced (tests included). You cannot run the code.
Score each criterion from 1 (poor) to 5 (excellent):
- correctness: does the diff fully and correctly do what the task asks, without breaking existing behaviour?
- readability: clarity of the code, naming, comments, idiomatic style, appropriate size.
- design: fit with the existing code, sensible structure, no needless complexity, no unrelated or out-of-scope changes (extra docs/plans/files count against this).
- test_quality: do the tests added meaningfully pin down the behaviour including edge cases (not just the happy path)? If the task did not ask for tests but changed behaviour, absence of tests scores 1.
Reply with ONLY a JSON object: {{"correctness": n, "readability": n, "design": n, "test_quality": n, "note": "one sentence"}}

=== TASK ===
{task}

=== DIFF ===
{diff}
"""


def claude_cmd(arm, budget, turns):
    plug = sum((["--plugin-dir", p] for p in PLUGINS[arm]), [])
    return ["claude", "-p", "--model", MODEL, "--effort", "low", "--setting-sources", "project", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}', *plug,
            "--output-format", "stream-json", "--verbose", "--no-session-persistence", "--max-turns", str(turns), "--max-budget-usd", str(budget),
            "--tools", TOOLS, "--allowedTools", TOOLS, "--permission-mode", "default"]


def judge(t, patch, stem):
    d = patch if len(patch) < 30000 else patch[:30000] + "\n[diff truncated]"
    cmd = ["claude", "-p", "--model", JUDGE_MODEL, "--effort", "low", "--setting-sources", "project", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
           "--tools", "", "--max-turns", "3", "--output-format", "json", "--no-session-persistence", "--max-budget-usd", "0.5"]
    cwd = f"{W}/judge_cwd"; os.makedirs(cwd, exist_ok=True)
    p = subprocess.run(cmd, input=JUDGE.format(task=t["prompt"], diff=d), text=True, capture_output=True, cwd=cwd, env=ENV, timeout=300)
    try:
        r = json.loads(p.stdout); txt = r.get("result", ""); cost = r.get("total_cost_usd") or 0
        m = re.search(r"\{.*\}", txt, re.S); j = json.loads(m.group(0))
        return {**{k: j.get(k) for k in ("correctness", "readability", "design", "test_quality", "note")}, "cost": cost}
    except Exception as e:
        return {"error": str(e)[:200], "raw": (p.stdout + p.stderr)[-400:]}


def run(job):
    tid, arm, rep = job; t = task(tid)
    stem = f"{W}/runs/{tid}__{arm}__r{rep}"
    if os.path.exists(stem + "/grade.json") or halt[0]:
        return
    shutil.rmtree(stem, ignore_errors=True); os.makedirs(stem)
    repo = prepare_repo(t, stem + "/repo")
    t0 = time.time()
    try:
        p = subprocess.run(claude_cmd(arm, A.run_cap, A.turns), input=PROMPT.format(task=t["prompt"]), text=True, capture_output=True, cwd=repo, env=ENV, timeout=1500)
        out, err, rc = p.stdout, p.stderr, p.returncode
    except subprocess.TimeoutExpired as e:
        out, err, rc = (e.stdout or b"").decode() if isinstance(e.stdout, bytes) else (e.stdout or ""), "timeout", "timeout"
    wall = time.time() - t0
    open(stem + "/out.jsonl", "w").write(out); open(stem + "/err.txt", "w").write(err)
    cost = 0.0; blob = err[-1500:]; denials = None
    for l in out.splitlines():
        try: e = json.loads(l)
        except Exception: continue
        if e.get("type") == "result":
            cost = e.get("total_cost_usd") or 0; denials = e.get("permission_denials")
            if e.get("is_error") and e.get("subtype") not in ("error_max_turns", "error_max_budget_usd"): blob += json.dumps(e)[:1500]
        if e.get("type") == "rate_limit_event" and e["rate_limit_info"].get("status") not in ("allowed", "allowed_warning"): blob += json.dumps(e)[:500]
    bad = None
    with lock:
        spent[0] += cost
        if LIM.search(blob) and not out.count('"type":"result"'): bad = f"{tid} {arm} r{rep}: {blob[-400:]}"
        elif denials: bad = f"{tid} {arm} r{rep}: PERMISSION DENIALS {json.dumps(denials)[:400]}"
        if bad: halt[0] = bad
        if spent[0] >= A.cap: halt[0] = f"cost cap reached: {spent[0]:.2f}"
    if bad:
        print("HALT", bad, flush=True); return
    g = G.grade(t, repo, stem + "/out.jsonl", seed=hash((tid, arm, rep)) & 0xffff)
    patch = g.pop("patch"); open(stem + "/patch.diff", "w").write(patch)
    g.update({"arm": arm, "rep": rep, "wall_s": round(wall, 1), "rc": rc})
    if not A.no_judge:
        g["judge"] = judge(t, patch, stem)
        with lock: spent[0] += (g["judge"].get("cost") or 0)
    json.dump(g, open(stem + "/grade.json", "w"), indent=1)
    shutil.rmtree(repo, ignore_errors=True)  # keep patch + transcript, drop the working copy
    with lock:
        print(f"{tid} {arm} r{rep} rc={rc} hidden={g['hidden_frac']} cost={cost:.2f} wall={wall:.0f}s total={spent[0]:.2f}", flush=True)


tasks = A.tasks.split(",") if A.tasks else all_tasks()
arms = A.arms.split(",")
jobs = []
for rep in range(A.rep_start, A.rep_start + A.reps):
    for ti, tid in enumerate(tasks):
        k = (ti + rep) % len(arms)
        for a in arms[k:] + arms[:k]:
            jobs.append((tid, a, rep))
os.makedirs(f"{W}/runs", exist_ok=True)
with ThreadPoolExecutor(A.par) as ex: list(ex.map(run, jobs))
print("HALT:", halt[0] or "none", f"spent={spent[0]:.2f}")
