#!/usr/bin/env python3
"""Re-run one corrected hidden test file against saved patches. usage: regrade_cpp.py WORK REPO TARGETS TASK RUNPREFIX"""
import sys, os, json, subprocess, shutil, glob, re
W, REPO, TG, task, pre = sys.argv[1:6]
H = os.path.dirname(os.path.abspath(__file__)); tasks = json.load(open(H + "/tasks.json")); t = tasks[task]
env = dict(os.environ, CARGO_PROFILE_RELEASE_LTO="off", CARGO_PROFILE_RELEASE_CODEGEN_UNITS="16", CARGO_PROFILE_RELEASE_INCREMENTAL="false", CARGO_NET_OFFLINE="true")
for pf in sorted(glob.glob(f"{W}/patches/{pre}*.patch")):
    name = os.path.basename(pf)[:-6]; wt = f"{W}/wt/rg_{name}"; tg = f"{TG}/rg_{name}"
    subprocess.run(["git", "-C", REPO, "worktree", "add", "--detach", wt, "eb36a4c"], capture_output=True)
    subprocess.run(["git", "apply", pf], cwd=wt, check=True)
    shutil.rmtree(tg, ignore_errors=True); os.makedirs(tg); subprocess.run(["cp", "-r", "--reflink=always", f"{TG}/seed2/release", tg + "/"], check=True)
    shutil.copy(f"{H}/hidden/{t['hidden']}.rs", f"{wt}/tests/{t['hidden']}.rs")
    p = subprocess.run(f"cargo test --release --test {t['hidden']} 2>&1", shell=True, cwd=wt, env=dict(env, CARGO_TARGET_DIR=tg), capture_output=True, text=True)
    m = re.search(r"(\d+) passed; (\d+) failed", p.stdout); ps, fl = (int(m.group(1)), int(m.group(2))) if m else (0, t["n_hidden"])
    gf = f"{W}/runs/{name}/grade.json"; g = json.load(open(gf))
    g["hidden_original"] = g["hidden"]; g["hidden"] = {"passed": ps, "failed": fl, "total": t["n_hidden"], "frac": round(ps / t["n_hidden"], 4)}
    json.dump(g, open(gf, "w"), indent=1)
    subprocess.run(["git", "-C", REPO, "worktree", "remove", "--force", wt], capture_output=True); shutil.rmtree(tg, ignore_errors=True)
    print(name, ps, fl, flush=True)
