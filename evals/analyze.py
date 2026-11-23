#!/usr/bin/env python3
"""Grade runs: first Skill call per run vs expected family. usage: analyze.py <workdir> <cases.json> [runsdir]
Families: a skill family (hit = first Skill call is a plugin skill of that family), "none" (controls: any Skill call
is a false fire) and "not-<a>-<b>" negatives such as "not-ui-prose" or "not-retro" (hit unless the first Skill call is
one of the named skills; other skills are fine)."""
import json, sys, glob, os, collections, statistics
W, CASES = sys.argv[1], {c["id"]: c for c in json.load(open(sys.argv[2]))}
RUNS = sys.argv[3] if len(sys.argv) > 3 else "runs"
FAM = {  # expected family -> skill names (without plugin prefix) that count as a hit
 "A": {"shape": {"brainstorming", "grilling", "grill-me", "grill-with-docs", "to-spec", "prototype"},
       "plan": {"writing-plans", "to-tickets", "wayfinder"},
       "build": {"test-driven-development", "tdd", "implement", "implement-spec", "executing-plans", "subagent-driven-development"},
       "debug": {"systematic-debugging", "diagnosing-bugs"},
       "design": {"codebase-design", "improve-codebase-architecture", "domain-modeling"},
       "review": {"requesting-code-review", "receiving-code-review", "code-review"},
       "ship": {"finishing-a-development-branch", "pr"},
       "verify": {"verification-before-completion"},
       "research": {"research"},
       "swarm": {"dispatching-parallel-agents", "subagent-driven-development"},
       "write-for-agents": {"writing-for-agents", "writing-skills"},
       "handoff": {"handoff"}},
 "B": {f: {f} for f in "shape plan build debug design review ship verify research swarm write-for-agents handoff retro ui prose".split()}}
NEG = {"ui", "prose", "retro"}  # on-demand or user-invoked skills that must not fire outside their own family
isneg = lambda fam: fam.startswith("not-")
negset = lambda fam: set(fam[4:].split("-"))
def first_skill(path):
    first = None; usage = None; sk = []
    for l in open(path):
        try: e = json.loads(l)
        except Exception: continue
        if e.get("type") == "assistant":
            if usage is None:
                u = e["message"]["usage"]; usage = u["input_tokens"] + u["cache_read_input_tokens"] + u["cache_creation_input_tokens"]
            for c in e["message"]["content"]:
                if c["type"] == "tool_use" and c["name"] == "Skill": sk.append(c["input"].get("skill", ""))
    return (sk[0] if sk else None), sk, usage
rows = []
ARMS = sorted({os.path.basename(p)[:-6].split("__")[1] for p in glob.glob(f"{W}/{RUNS}/*.jsonl")})
for p in sorted(glob.glob(f"{W}/{RUNS}/*.jsonl")):
    cid, arm, s = os.path.basename(p)[:-6].split("__")
    f, allsk, usage = first_skill(p)
    c = CASES[cid]; bare = f.split(":")[-1] if f else None
    builtin = f is not None and ":" not in f
    if c["family"] == "none": hit = None
    elif isneg(c["family"]): hit = builtin or bare not in negset(c["family"])
    else: hit = (not builtin) and bare in FAM[arm].get(c["family"], set())
    rows.append(dict(id=cid, fam=c["family"], arm=arm[0], s=s, first=f, all=allsk, usage=usage, hit=hit))
json.dump(rows, open(f"{W}/graded-{RUNS}.json", "w"), indent=1)
print("== hit rate per family (first Skill call in family; builtin bare-name skills count as miss)")
for fam in dict.fromkeys(c["family"] for c in CASES.values()):
    if fam == "none" or isneg(fam): continue
    out = []
    for a in ARMS:
        r = [x for x in rows if x["fam"] == fam and x["arm"] == a]
        out.append(f"{a}: {sum(x['hit'] for x in r)}/{len(r)}")
    print(f"{fam:18s}", "  ".join(out))
SKILLFAM = lambda x: x["fam"] != "none" and not isneg(x["fam"])
OLD = set(FAM["A"])  # the twelve families measured before ui and prose were added
for a in ARMS:
    r = [x for x in rows if SKILLFAM(x) and x["arm"] == a]; print(f"overall {a}: {sum(x['hit'] for x in r)}/{len(r)}")
    r = [x for x in rows if SKILLFAM(x) and x["fam"] in OLD and x["arm"] == a]; print(f"  original 12 families {a}: {sum(x['hit'] for x in r)}/{len(r)}")
    r = [x for x in rows if SKILLFAM(x) and x["arm"] == a and x["first"] is None]; print(f"  no skill at all {a}: {len(r)}")
print("== controls false fires")
for a in ARMS:
    r = [x for x in rows if x["fam"] == "none" and x["arm"] == a]
    print(a, f"{sum(x['first'] is not None for x in r)}/{len(r)}", [(x['id'], x['first']) for x in r if x['first']])
print("== negatives: a named skill fired (must be 0)")
for a in ARMS:
    r = [x for x in rows if isneg(x["fam"]) and x["arm"] == a]
    print(a, f"{sum(not x['hit'] for x in r)}/{len(r)}", [(x['id'], x['first']) for x in r])
print("== ui, prose or retro fired on any case outside their family (must be 0)")
for a in ARMS:
    r = [x for x in rows if x["arm"] == a and x["fam"] not in NEG and x["first"] and x["first"].split(":")[-1] in NEG and ":" in x["first"]]
    print(a, len(r), [(x['id'], x['first']) for x in r])
print("== first-request prompt tokens (median / min / max)")
for a in ARMS:
    u = [x["usage"] for x in rows if x["arm"] == a and x["usage"]]; print(a, statistics.median(u), min(u), max(u), len(u))
print("== per-case first calls")
by = collections.defaultdict(dict)
for x in rows: by[(x["id"])].setdefault(x["arm"], []).append(x["first"])
for cid, d in by.items(): print(f"{cid:11s} [{CASES[cid]['family']}] A={d.get('A')} B={d.get('B')}")
