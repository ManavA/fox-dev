#!/usr/bin/env python3
"""For kind=tests tasks: the reference tests must pass on the original and kill every hidden mutant."""
import sys, json, tempfile, shutil
from common import *
from grade_lib import hidden_mutant_kill

for tid in (sys.argv[1:] or [x for x in all_tasks() if task(x)["kind"] == "tests"]):
    t = task(tid); tmp = tempfile.mkdtemp(prefix="vm_"); repo = prepare_repo(t, tmp + "/r")
    apply_overlay(f"{t['dir']}/ref", repo)
    r = hidden_mutant_kill(t, repo)
    print(tid, r["on_original"], f"killed {r['killed']}/{r['total']}", "survivors:", r["survivors"])
    shutil.rmtree(tmp)
