#!/usr/bin/env python3
"""Re-run the (possibly corrected) hidden tests against each run's saved patch and update grade.json. usage: regrade_hidden.py RUNS_DIR"""
import glob, json, shutil, subprocess, sys, tempfile
from common import *
import grade_lib as G

for g in sorted(glob.glob(sys.argv[1] + "/*/grade.json")):
    d = g.rsplit("/", 1)[0]; j = json.load(open(g)); t = task(j["task"])
    if t["kind"] == "tests":
        continue
    tmp = tempfile.mkdtemp(prefix="rg_"); repo = prepare_repo(t, tmp + "/r")
    subprocess.run(["git", "apply", "--whitespace=nowarn", d + "/patch.diff"], cwd=repo, capture_output=True)
    h = G.hidden_pass(t, repo); shutil.rmtree(tmp)
    if h["frac"] != j["hidden_frac"]:
        print(d.rsplit("/", 1)[-1], j["hidden_frac"], "->", h["frac"])
    j["hidden"] = h; j["hidden_frac"] = h["frac"]; json.dump(j, open(g, "w"), indent=1)
