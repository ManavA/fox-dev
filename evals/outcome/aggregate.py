#!/usr/bin/env python3
"""Aggregate graded runs into per-arm and per-task tables. usage: aggregate.py RUNS_DIR [--md OUT.md] [--json OUT.json]"""
import glob, json, os, random, statistics as st, sys
from common import *
import grade_lib as G

RUNS = sys.argv[1]
rows = []
for d in sorted(glob.glob(RUNS + "/*/grade.json")):
    g = json.load(open(d)); base = os.path.dirname(d); t = task(g["task"])
    if os.path.exists(base + "/out.jsonl"):
        g["process"] = G.transcript(base + "/out.jsonl", t)
    rows.append(g)
ARMS = ["none", "current", "foxdev"]
mean = lambda xs: (sum(xs) / len(xs)) if xs else None
f = lambda x, n=2: "n/a" if x is None else f"{x:.{n}f}"


def metric(g, k):
    p = g["process"]; j = g.get("judge") or {}
    return {
        "hidden": g["hidden_frac"], "allpass": 1.0 if g["hidden_frac"] >= 0.9999 and g["existing"]["frac"] >= 0.9999 else 0.0, "existing": g["existing"]["frac"],
        "tests_added": g["agent_tests"]["passed"], "wrote_tests": 1.0 if g["agent_tests"]["files"] else 0.0,
        "cov": (g["coverage"] or {}).get("frac"), "mut": g["mutation"].get("score"),
        "lint_new": max(g["lint_delta"], 0) + max(g["types_delta"], 0), "ratio": g["diff_ratio"], "oos": len(g["out_of_scope"]),
        "j_correct": j.get("correctness"), "j_read": j.get("readability"), "j_design": j.get("design"), "j_tests": j.get("test_quality"),
        "wall": g["wall_s"], "turns": p.get("turns"), "cost": p.get("cost"), "tok_out": p.get("tokens_out"),
        "tests_first": None if p.get("tests_first") is None else float(p["tests_first"]), "ran_tests": float(p["ran_tests_after_last_edit"]), "skills": len(p["skills"]), "agents": p["agents_spawned"],
    }[k]


KEYS = [("allpass", "all tests pass (hidden+existing), share of runs"), ("hidden", "hidden-test pass fraction (mean)"), ("existing", "existing suite pass fraction"), ("wrote_tests", "wrote tests, share of runs"),
        ("tests_added", "tests added (count, mean)"), ("cov", "changed-line coverage by own tests"), ("mut", "mutation score of own tests on changed code"), ("lint_new", "new lint+type errors (mean)"),
        ("ratio", "src diff size vs reference (mean)"), ("oos", "files touched outside scope (mean)"), ("j_correct", "judge correctness"), ("j_read", "judge readability"), ("j_design", "judge design"),
        ("j_tests", "judge test quality"), ("wall", "wall seconds"), ("turns", "turns"), ("cost", "cost USD"), ("tok_out", "output tokens"), ("tests_first", "tests before impl (where detectable)"),
        ("ran_tests", "ran tests after last edit"), ("skills", "Skill calls per run"), ("agents", "subagents per run")]
out = {"n_runs": len(rows), "arms": {}, "tasks": {}}
for a in ARMS:
    rs = [g for g in rows if g["arm"] == a]
    out["arms"][a] = {"n": len(rs), **{k: mean([v for v in (metric(g, k) for g in rs) if v is not None]) for k, _ in KEYS}}
tasks = sorted({g["task"] for g in rows})
for tid in tasks:
    out["tasks"][tid] = {}
    for a in ARMS:
        rs = [g for g in rows if g["arm"] == a and g["task"] == tid]
        out["tasks"][tid][a] = {"n": len(rs), **{k: mean([v for v in (metric(g, k) for g in rs) if v is not None]) for k, _ in KEYS}}


def boot(a, b, k, n=2000):
    """Paired difference (a - b) per task (mean over reps), bootstrap over tasks."""
    d = []
    for tid in tasks:
        x = [metric(g, k) for g in rows if g["task"] == tid and g["arm"] == a]; y = [metric(g, k) for g in rows if g["task"] == tid and g["arm"] == b]
        x = [v for v in x if v is not None]; y = [v for v in y if v is not None]
        if x and y: d.append(mean(x) - mean(y))
    if len(d) < 3: return None
    r = random.Random(1); bs = sorted(mean([r.choice(d) for _ in d]) for _ in range(n))
    return mean(d), bs[int(.025 * n)], bs[int(.975 * n)]


md = ["# Outcome eval: per-arm results", f"{len(rows)} graded runs. Means over runs.", "", "| metric | none | current | foxdev |", "|---|---|---|---|"]
md.append("| runs | " + " | ".join(str(out["arms"][a]["n"]) for a in ARMS) + " |")
for k, label in KEYS:
    md.append(f"| {label} | " + " | ".join(f(out["arms"][a][k], 3 if k in ("allpass", "hidden", "existing", "cov", "mut", "wrote_tests") else 2) for a in ARMS) + " |")
md += ["", "## Paired differences (mean over tasks, 95% bootstrap CI over tasks)", "", "| metric | foxdev - current | foxdev - none | current - none |", "|---|---|---|---|"]
for k, label in KEYS:
    cells = []
    for a, b in (("foxdev", "current"), ("foxdev", "none"), ("current", "none")):
        r = boot(a, b, k); cells.append("n/a" if r is None else f"{r[0]:+.3f} [{r[1]:+.3f}, {r[2]:+.3f}]")
    md.append(f"| {label} | " + " | ".join(cells) + " |")
md += ["", "## Per task (hidden pass / mutation / cost / judge-mean), none | current | foxdev", ""]
for tid in tasks:
    cells = []
    for a in ARMS:
        m = out["tasks"][tid][a]
        jm = mean([m[k] for k in ("j_correct", "j_read", "j_design", "j_tests") if m[k] is not None])
        cells.append(f"{f(m['hidden'])} / {f(m['mut'])} / ${f(m['cost'], 3)} / {f(jm, 1)}")
    md.append(f"- {tid} ({task(tid)['kind']}): " + " | ".join(cells))
text = "\n".join(md)
if "--md" in sys.argv: open(sys.argv[sys.argv.index("--md") + 1], "w").write(text + "\n")
if "--json" in sys.argv: json.dump(out, open(sys.argv[sys.argv.index("--json") + 1], "w"), indent=1)
print(text)
