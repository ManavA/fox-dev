#!/usr/bin/env python3
"""Skill-firing comparison driver. usage: run_firing.py <workdir> <cases.json> [--samples N] [--cap USD] [--turns N] [--runs DIR] [--arms AB|B]
workdir holds home/ (scratch HOME with credentials only), repo/ (sample git repo with .claude/settings.json) and runs/.
Arm A loads superpowers + mattpocock-skills from the plugin cache; arm B loads this repo's plugin/ only.
Grades the first Skill tool call (stream-json, --max-turns 2). Halts on rate limits or when the cost cap is reached."""
import json, os, subprocess, sys, threading, re
from concurrent.futures import ThreadPoolExecutor

W = sys.argv[1]; CASES = json.load(open(sys.argv[2]))
N = int(sys.argv[sys.argv.index("--samples") + 1]) if "--samples" in sys.argv else 2
TURNS = sys.argv[sys.argv.index("--turns") + 1] if "--turns" in sys.argv else "2"
RUNS = sys.argv[sys.argv.index("--runs") + 1] if "--runs" in sys.argv else "runs"
ARMS = sys.argv[sys.argv.index("--arms") + 1] if "--arms" in sys.argv else "AB"
CAP = float(sys.argv[sys.argv.index("--cap") + 1]) if "--cap" in sys.argv else 8.0
PC = os.path.expanduser("~/.claude/plugins/cache/claude-plugins-official")  # read-only plugin cache of the real HOME
HERE = os.path.dirname(os.path.abspath(__file__))
PLUGINS = {"A": [f"{PC}/superpowers/7.0.0", f"{PC}/mattpocock-skills/1.3.1"], "B": [os.path.join(os.path.dirname(HERE), "plugin")]}
MODEL = "claude-sonnet-5-5"
ENV = {"HOME": f"{W}/home", "USER": "eval", "PATH": os.path.expanduser("~/.local/bin") + ":/usr/bin:/bin", "LANG": "C.UTF-8", "TERM": "dumb",
       "CLAUDE_CODE_DISABLE_CLAUDE_MDS": "1", "CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1", "DISABLE_AUTOUPDATER": "1",
       "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1", "ENABLE_CLAUDEAI_MCP_SERVERS": "false"}
LIM = re.compile(r"(usage limit|rate.?limit|\b429\b|overloaded|quota|limit reached|too many requests|credit balance|authentication_error|oauth)", re.I)
lock = threading.Lock(); spent = [0.0]; halt = [None]

def run(case, arm, s):
    stem = f"{W}/{RUNS}/{case['id']}__{arm}__s{s}"
    if os.path.exists(stem + ".done"): return
    if halt[0]: return
    cmd = ["claude", "-p", "--model", MODEL, "--setting-sources", "project", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
           *sum((["--plugin-dir", p] for p in PLUGINS[arm]), []), "--output-format", "stream-json", "--verbose", "--no-session-persistence",
           "--max-turns", TURNS, "--max-budget-usd", "0.6", "--tools", "Skill,Read,Grep,Glob", "--allowedTools", "Skill,Read,Grep,Glob",
           "--permission-mode", "default"]
    p = subprocess.run(cmd, input=case["prompt"], text=True, capture_output=True, cwd=f"{W}/repo", env=ENV, timeout=280)
    open(stem + ".jsonl", "w").write(p.stdout); open(stem + ".err", "w").write(p.stderr)
    cost = 0.0; blob = p.stderr[-1500:]
    for l in p.stdout.splitlines():
        try: e = json.loads(l)
        except Exception: continue
        if e.get("type") == "result":
            cost = e.get("total_cost_usd") or 0
            if e.get("is_error") and e.get("subtype") != "error_max_turns": blob += json.dumps(e)[:1500]
        if e.get("type") == "rate_limit_event" and e["rate_limit_info"].get("status") not in ("allowed", "allowed_warning"):
            blob += json.dumps(e)[:500]
    with lock:
        spent[0] += cost
        if LIM.search(blob): halt[0] = f"{case['id']} {arm} s{s}: {blob[-400:]}"
        if spent[0] >= CAP: halt[0] = f"cost cap reached: {spent[0]:.2f}"
        print(f"{case['id']} {arm} s{s} rc={p.returncode} cost={cost:.3f} total={spent[0]:.2f}", flush=True)
    if not halt[0]: open(stem + ".done", "w").write("1")

jobs = [(c, a, s) for s in range(1, N + 1) for c in CASES for a in ARMS]
with ThreadPoolExecutor(3) as ex: list(ex.map(lambda j: run(*j), jobs))
print("HALT:", halt[0] if halt[0] else "none", f"spent={spent[0]:.2f}")
