#!/usr/bin/env python3
"""Check a task is solvable: hidden tests fail on baseline (unless a refactor), all pass with the reference, existing suite passes both ways."""
import sys, tempfile, shutil, os
from common import *

for tid in (sys.argv[1:] or all_tasks()):
    t = task(tid); tmp = tempfile.mkdtemp(prefix="vt_"); repo = prepare_repo(t, tmp + "/r")
    base_exist = run_tests(t, repo)
    install_hidden(t, repo)
    base_hid = run_tests(t, repo, [t["hidden_dest"]]) if t["kind"] != "tests" else {"passed":0,"failed":0,"out":""}
    if os.path.isdir(f"{t['dir']}/ref"):
        apply_overlay(f"{t['dir']}/ref", repo)
    ref_hid = run_tests(t, repo, [t["hidden_dest"]])
    ref_exist = run_tests(t, repo)
    import json as _j
    if ref_hid["passed"] and not ref_hid["failed"]: _j.dump({"hidden_passed": ref_hid["passed"]}, open(f"{t['dir']}/verified.json", "w"))
    print(f"{tid}: baseline existing {base_exist['passed']}p/{base_exist['failed']}f | baseline hidden {base_hid['passed']}p/{base_hid['failed']}f | ref hidden {ref_hid['passed']}p/{ref_hid['failed']}f | ref existing {ref_exist['passed']}p/{ref_exist['failed']}f")
    if ref_hid["failed"] or not ref_hid["passed"]:
        print(ref_hid["out"])
    shutil.rmtree(tmp)
