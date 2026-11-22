#!/usr/bin/env python3
"""Per-run table and per-arm means from runs/*/grade.json. usage: aggregate_hard.py WORK_DIR"""
import glob, json, statistics as S, sys

W = sys.argv[1]
rows = [json.load(open(f)) for f in sorted(glob.glob(f"{W}/runs/*/grade.json"))]
ARMS = ["none", "current", "foxdev"]
print("| task | arm | run | hidden | existing regressions | clippy | fmt | judge c/r/d/t | tests added | cost | wall s | turns | skills fired | subagents | tests first |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for g in sorted(rows, key=lambda g: (g["task"], ARMS.index(g["arm"]), g["rep"])):
    p = g["process"]; j = g.get("judge", {})
    jj = "/".join(str(j.get(k, "?")) for k in ("correctness", "readability", "design", "test_quality"))
    reg = ",".join(f"{k}:{v[1]}" for k, v in g["existing_regressions"].items()) or "0"
    cost = (g.get("run_cost") or 0)
    print(f"| {g['task']} | {g['arm']} | r{g['rep']} | {g['hidden']['passed']}/{g['hidden']['total']} | {reg} | {'ok' if g['clippy_ok'] else 'FAIL'} | {'ok' if g['fmt_ok'] else 'FAIL'} | {jj} | {g['tests_added']} | {cost:.2f} | {g['wall_s']:.0f} | {p.get('turns')} | {','.join(p['skills']) or '-'} | {p['agents_spawned']} | {p['tests_first']} |")


def m(xs):
    xs = [x for x in xs if x is not None]
    return round(S.mean(xs), 2) if xs else "n/a"


print("\n| arm | runs | hidden pass frac | all hidden pass | runs with regression | clippy ok | judge correctness | readability | design | tests | tests added | cost | wall s | turns | skill calls | subagents |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for a in ARMS:
    r = [g for g in rows if g["arm"] == a]
    if not r: continue
    jm = lambda k: m([g["judge"].get(k) for g in r if isinstance(g.get("judge", {}).get(k), (int, float))])
    print(f"| {a} | {len(r)} | {m([g['hidden']['frac'] for g in r])} | {sum(g['hidden']['frac'] == 1 for g in r)}/{len(r)} | {sum(bool(g['existing_regressions']) for g in r)} | {sum(g['clippy_ok'] for g in r)}/{len(r)} | "
          f"{jm('correctness')} | {jm('readability')} | {jm('design')} | {jm('test_quality')} | {m([g['tests_added'] for g in r])} | {m([g.get('run_cost') for g in r])} | {m([g['wall_s'] for g in r])} | {m([g['process'].get('turns') for g in r])} | "
          f"{m([len(g['process']['skills']) for g in r])} | {m([g['process']['agents_spawned'] for g in r])} |")
