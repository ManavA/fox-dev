#!/usr/bin/env python3
"""Hard outcome eval on real foxdb gaps. One isolated `claude -p` (Sonnet, effort high) per (task, arm, rep) in its own
git worktree of the pinned foxdb commit, then grading (hidden tests, whole existing suite, clippy, fmt), one blind Opus judge call.

usage: run_hard.py --work DIR --repo ~/foxdb [--tasks a,b] [--arms none,current,foxdev] [--reps N] [--rep-start N] [--cap USD] [--run-cap USD] [--par N] [--smoke]
DIR holds home/ (scratch HOME with OAuth credentials only), seed/ (a built worktree + target seed), wt/ (worktrees), runs/<task>__<arm>__r<rep>/ and patches/.
Never edits the source repo; worktrees and cargo target dirs (reflink copies of the seed) are per run."""
import argparse, json, os, re, shutil, subprocess, sys, threading, time
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
OUTCOME = os.path.dirname(HERE)
sys.path.insert(0, OUTCOME)

ap = argparse.ArgumentParser()
ap.add_argument("--work", required=True); ap.add_argument("--repo", required=True); ap.add_argument("--targets", required=True)
ap.add_argument("--commit", default="eb36a4c"); ap.add_argument("--tasks"); ap.add_argument("--arms", default="none,current,foxdev")
ap.add_argument("--reps", type=int, default=1); ap.add_argument("--rep-start", type=int, default=1); ap.add_argument("--cap", type=float, default=80.0)
ap.add_argument("--run-cap", type=float, default=4.0); ap.add_argument("--par", type=int, default=3); ap.add_argument("--turns", type=int, default=150)
ap.add_argument("--timeout", type=int, default=3000)
A = ap.parse_args()
W = os.path.abspath(A.work); REPO = os.path.abspath(A.repo); TG = os.path.abspath(A.targets)
TASKS = json.load(open(f"{HERE}/tasks.json"))
PC = os.path.expanduser("~/.claude/plugins/cache/claude-plugins-official")  # read-only plugin cache
PLUGINS = {"none": [], "current": [f"{PC}/superpowers/7.0.0", f"{PC}/mattpocock-skills/1.3.1"], "foxdev": [os.path.normpath(f"{OUTCOME}/../../plugin")]}
MODEL = "claude-sonnet-5-5"; JUDGE_MODEL = "claude-opus-5-5"
TOOLS = "Read,Edit,Write,Bash,Grep,Glob,Skill,Agent"
CARGO_HOME = os.path.expanduser("~/.cargo"); RUSTUP_HOME = os.path.expanduser("~/.rustup")
ENV = {"HOME": f"{W}/home", "USER": "eval", "PATH": ":".join([f"{CARGO_HOME}/bin", os.path.expanduser("~/.local/bin"), "/usr/bin", "/bin"]), "LANG": "C.UTF-8", "TERM": "dumb",
       "CARGO_HOME": CARGO_HOME, "RUSTUP_HOME": RUSTUP_HOME, "CARGO_NET_OFFLINE": "true", "CARGO_PROFILE_RELEASE_LTO": "off", "CARGO_PROFILE_RELEASE_CODEGEN_UNITS": "16", "CARGO_PROFILE_RELEASE_INCREMENTAL": "false", "CARGO_TERM_COLOR": "never",
       "GIT_AUTHOR_NAME": "eval", "GIT_AUTHOR_EMAIL": "eval@example.invalid", "GIT_COMMITTER_NAME": "eval", "GIT_COMMITTER_EMAIL": "eval@example.invalid", "CI": "1",
       "CLAUDE_CODE_DISABLE_CLAUDE_MDS": "1", "CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1", "DISABLE_AUTOUPDATER": "1", "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1", "ENABLE_CLAUDEAI_MCP_SERVERS": "false"}
LIM = re.compile(r"(usage limit|rate.?limit|\b429\b|overloaded|quota|limit reached|too many requests|credit balance|authentication_error|oauth|unauthori[sz]ed)", re.I)
lock = threading.Lock(); spent = [0.0]; halt = [None]

PROMPT = ("You are working in the foxdb repository (Rust) in the current directory. Cargo is offline and a warm build cache is in place; run builds and tests with `cargo build --release` / "
          "`cargo test --release [--test NAME]`, and the repo's own gate also includes `cargo clippy --release --all-targets -- -D warnings` and `cargo fmt --check`.\n\n{task}")

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


def sh(cmd, cwd, env=None, timeout=600):
    e = dict(ENV, **(env or {}))
    try:
        p = subprocess.run(cmd, shell=isinstance(cmd, str), cwd=cwd, env=e, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout + p.stderr
    except subprocess.TimeoutExpired as ex:
        o = ex.stdout.decode() if isinstance(ex.stdout, bytes) else (ex.stdout or "")
        return 124, o + "\n[timeout]"


def claude_cmd(arm):
    plug = sum((["--plugin-dir", p] for p in PLUGINS[arm]), [])
    return ["claude", "-p", "--model", MODEL, "--effort", "high", "--setting-sources", "project", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}', *plug,
            "--output-format", "stream-json", "--verbose", "--no-session-persistence", "--max-turns", str(A.turns), "--max-budget-usd", str(A.run_cap),
            "--tools", TOOLS, "--allowedTools", TOOLS, "--permission-mode", "default"]


def judge(prompt, patch):
    d = patch if len(patch) < 40000 else patch[:40000] + "\n[diff truncated]"
    cmd = ["claude", "-p", "--model", JUDGE_MODEL, "--effort", "low", "--setting-sources", "project", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
           "--tools", "", "--max-turns", "3", "--output-format", "json", "--no-session-persistence", "--max-budget-usd", "0.8"]
    cwd = f"{W}/judge_cwd"; os.makedirs(cwd, exist_ok=True)
    p = subprocess.run(cmd, input=JUDGE.format(task=prompt, diff=d), text=True, capture_output=True, cwd=cwd, env=ENV, timeout=400)
    try:
        r = json.loads(p.stdout); m = re.search(r"\{.*\}", r.get("result", ""), re.S); j = json.loads(m.group(0))
        return {**{k: j.get(k) for k in ("correctness", "readability", "design", "test_quality", "note")}, "cost": r.get("total_cost_usd") or 0}
    except Exception as e:
        return {"error": str(e)[:200], "raw": (p.stdout + p.stderr)[-400:]}


def cargo_counts(out):
    """Per test binary: name -> (passed, failed); a compile failure adds '<compile>'."""
    res = {}; cur = None
    for l in out.splitlines():
        m = re.match(r"\s+Running (?:unittests )?(\S+)", l)
        if m:
            path = m.group(1); mm = re.match(r"tests/(.+)\.rs$", path)
            cur = mm.group(1) if mm else ("lib" if path == "src/lib.rs" else path)
        m = re.match(r"test result: \w+\. (\d+) passed; (\d+) failed", l)
        if m and cur:
            p, f = res.get(cur, (0, 0)); res[cur] = (p + int(m.group(1)), f + int(m.group(2)))
    if re.search(r"could not compile|error: aborting", out): res["<compile>"] = (0, 1)
    return res


def transcript(path):
    ev = []; res = None; init = None
    for l in open(path):
        try: e = json.loads(l)
        except Exception: continue
        if e.get("type") == "system" and e.get("subtype") == "init": init = e
        if e.get("type") == "result": res = e
        if e.get("type") == "assistant":
            for b in e["message"].get("content", []):
                if b.get("type") == "tool_use": ev.append((b["name"], b["input"], e.get("parent_tool_use_id")))
    top = [x for x in ev if x[2] is None]
    skills = [x[1].get("skill", x[1].get("name", "")) for x in top if x[0] == "Skill"]
    agents = sum(1 for x in ev if x[0] in ("Agent", "Task"))
    first = {"test": None, "src": None}
    for i, (n, inp, _) in enumerate(top):
        if n in ("Edit", "Write"):
            p = inp.get("file_path", "")
            k = "test" if "/tests/" in p else "src" if "/src/" in p else None
            if k and first[k] is None: first[k] = i
    r = {"tool_calls": len(top), "skills": skills, "agents_spawned": agents, "tests_first": (first["test"] < first["src"]) if first["test"] is not None and first["src"] is not None else None,
         "skills_available": len((init or {}).get("skills", [])), "plugins_loaded": [p.get("name") if isinstance(p, dict) else p for p in (init or {}).get("plugins", [])]}
    if res:
        r.update({"cost": res.get("total_cost_usd"), "turns": res.get("num_turns"), "duration_ms": res.get("duration_ms"), "subtype": res.get("subtype"), "is_error": res.get("is_error"),
                  "final_message": (res.get("result") or "")[:500]})
    return r


def grade(tid, wt, tg, jsonl):
    t = TASKS[tid]; g = {"task": tid}
    sh(["git", "add", "-A"], wt)
    patch = sh(["git", "diff", "--cached", "--binary", A.commit], wt)[1]
    files = sh(["git", "diff", "--cached", "--numstat", A.commit], wt)[1]
    g["files_changed"] = [l.split("\t")[2] for l in files.splitlines() if l.count("\t") >= 2]
    g["lines_added_removed"] = [sum(int(l.split("\t")[0]) for l in files.splitlines() if l.split("\t")[0].isdigit()), sum(int(l.split("\t")[1]) for l in files.splitlines() if l.split("\t")[1].isdigit())]
    # existing tests the agent edited or deleted (it may have rewritten an expectation to pass)
    g["existing_tests_touched"] = {p: [a, d] for p, a, d in ((l.split("\t")[2], l.split("\t")[0], l.split("\t")[1]) for l in files.splitlines()) if p.startswith("tests/") and sh(["git", "cat-file", "-e", f"{A.commit}:{p}"], wt)[0] == 0}
    new_tests = sh(f"git diff --cached -U0 {A.commit} -- tests src | grep -c '^+.*#\\[test\\]' || true", wt)[1].strip()
    g["tests_added"] = int(new_tests) if new_tests.isdigit() else 0
    # hidden tests go in as an extra test binary; the whole suite runs once, no fail-fast
    shutil.copy(f"{HERE}/hidden/{t['hidden']}.rs", f"{wt}/tests/{t['hidden']}.rs")
    env = {"CARGO_TARGET_DIR": tg}
    rc, out = sh("cargo test --release --no-fail-fast 2>&1", wt, env, timeout=2400)
    open(os.path.dirname(jsonl) + "/test_out.txt", "w").write(out[-60000:])
    res = cargo_counts(out); g["suite"] = res; g["suite_rc"] = rc
    hp, hf = res.get(t["hidden"], (0, 0))
    if "<compile>" in res and hp + hf == 0: hp = 0
    g["hidden"] = {"passed": hp, "failed": hf, "total": t["n_hidden"], "frac": round(min(hp, t["n_hidden"]) / t["n_hidden"], 4)}
    reg = {k: v for k, v in res.items() if k != t["hidden"] and (v[1] > 0)}
    g["existing_regressions"] = reg
    g["existing_passed"] = sum(v[0] for k, v in res.items() if k != t["hidden"])
    os.remove(f"{wt}/tests/{t['hidden']}.rs")
    rc, out = sh("cargo clippy --release --all-targets -- -D warnings 2>&1", wt, env, timeout=1200)
    g["clippy_ok"] = rc == 0; g["clippy_errors"] = len(re.findall(r"^(?:error|warning)(?:\[|:)", out, re.M)) - (1 if "could not compile" in out else 0) if rc else 0
    rc, out = sh("cargo fmt --check 2>&1", wt, env, timeout=120); g["fmt_ok"] = rc == 0
    g["process"] = transcript(jsonl); g["patch"] = patch
    return g


def run(job):
    tid, arm, rep = job
    stem = f"{W}/runs/{tid}__{arm}__r{rep}"
    if os.path.exists(stem + "/grade.json") or halt[0]: return
    shutil.rmtree(stem, ignore_errors=True); os.makedirs(stem)
    wt = f"{W}/wt/{tid}__{arm}__r{rep}"; tg = f"{TG}/{tid}__{arm}__r{rep}"
    if os.path.exists(wt): sh(["git", "-C", REPO, "worktree", "remove", "--force", wt], REPO)
    shutil.rmtree(tg, ignore_errors=True); os.makedirs(tg)
    sh(["git", "-C", REPO, "worktree", "add", "--detach", wt, A.commit], REPO)
    subprocess.run(["cp", "-r", "--reflink=always", f"{TG}/seed2/release", tg + "/"], check=True)
    env = dict(ENV, CARGO_TARGET_DIR=tg)
    t0 = time.time()
    try:
        p = subprocess.run(claude_cmd(arm), input=PROMPT.format(task=TASKS[tid]["prompt"]), text=True, capture_output=True, cwd=wt, env=env, timeout=A.timeout)
        out, err, rc = p.stdout, p.stderr, p.returncode
    except subprocess.TimeoutExpired as e:
        out, err, rc = (e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or "")), "timeout", "timeout"
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
    g = grade(tid, wt, tg, stem + "/out.jsonl")
    patch = g.pop("patch")
    open(stem + "/patch.diff", "w").write(patch)
    os.makedirs(f"{W}/patches", exist_ok=True); open(f"{W}/patches/{tid}__{arm}__r{rep}.patch", "w").write(patch)
    g.update({"arm": arm, "rep": rep, "wall_s": round(wall, 1), "rc": rc, "run_cost": cost})
    g["judge"] = judge(TASKS[tid]["prompt"], patch)
    with lock: spent[0] += g["judge"].get("cost") or 0
    json.dump(g, open(stem + "/grade.json", "w"), indent=1)
    sh(["git", "-C", REPO, "worktree", "remove", "--force", wt], REPO); shutil.rmtree(tg, ignore_errors=True)
    with lock:
        print(f"{tid} {arm} r{rep} rc={rc} hidden={g['hidden']['passed']}/{g['hidden']['total']} reg={len(g['existing_regressions'])} clippy={g['clippy_ok']} cost={cost:.2f} wall={wall:.0f}s turns={g['process'].get('turns')} skills={g['process']['skills']} total={spent[0]:.2f}", flush=True)


tasks = A.tasks.split(",") if A.tasks else list(TASKS)
arms = A.arms.split(",")
jobs = []
for rep in range(A.rep_start, A.rep_start + A.reps):
    for ti, tid in enumerate(tasks):
        k = (ti + rep) % len(arms)
        for a in arms[k:] + arms[:k]: jobs.append((tid, a, rep))
os.makedirs(f"{W}/runs", exist_ok=True); os.makedirs(f"{W}/wt", exist_ok=True)
with ThreadPoolExecutor(A.par) as ex: list(ex.map(run, jobs))
print("HALT:", halt[0] or "none", f"spent={spent[0]:.2f}")
