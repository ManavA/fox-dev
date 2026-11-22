"""Mechanical grading for one finished run: correctness, test quality (coverage, mutation), code quality, diff size."""
import ast, copy, glob, json, os, random, re, shutil, subprocess, tempfile
from concurrent.futures import ThreadPoolExecutor
from common import *

MUT_CAP = 40


# ---------------------------------------------------------------- diff
def git(repo, *a):
    return subprocess.run(["git", *a], cwd=repo, capture_output=True, text=True).stdout


def diff_info(repo):
    """Stage everything (gitignored junk stays out) and describe the change against the baseline commit."""
    git(repo, "add", "-A")
    patch = git(repo, "diff", "--cached", "--binary", "outcome-base")
    files = {}
    for l in git(repo, "diff", "--cached", "--numstat", "outcome-base").splitlines():
        a, d, p = l.split("\t", 2)
        files[p] = (int(a) if a.isdigit() else 0, int(d) if d.isdigit() else 0)
    changed = {}  # path -> set of new-side line numbers added/changed
    cur = None
    for l in git(repo, "diff", "--cached", "-U0", "outcome-base").splitlines():
        if l.startswith("+++ b/"):
            cur = l[6:]; changed.setdefault(cur, set())
        elif l.startswith("@@") and cur:
            m = re.search(r"\+(\d+)(?:,(\d+))?", l)
            s = int(m.group(1)); n = int(m.group(2)) if m.group(2) is not None else 1
            changed[cur].update(range(s, s + n))
    return patch, files, changed


def under(p, roots):
    return any(p.startswith(r.rstrip("/") + "/") for r in roots)


def classify(t, files):
    src = {p: v for p, v in files.items() if under(p, t["src"]) and not under(p, t["tests"])}
    tst = {p: v for p, v in files.items() if under(p, t["tests"])}
    out = [p for p in files if not any(p.startswith(s) for s in t["scope"])]
    return src, tst, out


def ref_diff(t):
    """Diff of the reference solution, cached on the task."""
    f = f"{t['dir']}/ref_diff.json"
    if os.path.exists(f):
        return json.load(open(f))
    tmp = tempfile.mkdtemp(prefix="rd_"); repo = prepare_repo(t, tmp + "/r"); apply_overlay(f"{t['dir']}/ref", repo)
    _, files, _ = diff_info(repo); src, tst, _ = classify(t, files)
    r = {"src": sum(a + d for a, d in src.values()), "test": sum(a + d for a, d in tst.values())}
    shutil.rmtree(tmp); json.dump(r, open(f, "w"))
    return r


# ---------------------------------------------------------------- correctness
def hidden_pass(t, repo):
    tmp = tempfile.mkdtemp(prefix="hp_"); c = tmp + "/r"; shutil.copytree(repo, c, symlinks=True)
    install_hidden(t, c)
    cmd = ("python -m pytest -q -p no:cacheprovider " if t["lang"] == "py" else "node --test --test-reporter=tap ") + t["hidden_dest"]
    rc, out = sh(cmd, c, timeout=180)
    p, f = parse_counts(out, t["lang"]); shutil.rmtree(tmp)
    total = json.load(open(f"{t['dir']}/verified.json"))["hidden_passed"] if os.path.exists(f"{t['dir']}/verified.json") else p + f
    return {"passed": p, "failed": f, "total": total, "frac": round(min(p, total) / total, 4) if total else 0.0}


def orig_test_files(t):
    base = f"{t['dir']}/repo"
    out = []
    for r in t["tests"]:
        for root, _, fs in os.walk(f"{base}/{r}"):
            out += [os.path.relpath(os.path.join(root, f), base) for f in fs if re.search(r"(^test_.*\.py|\.test\.ts)$", f)]
    return sorted(out)


def existing_pass(t, repo):
    """Original test files, restored byte-for-byte, run against the agent's source."""
    files = orig_test_files(t)
    if not files:
        return {"passed": 0, "failed": 0, "frac": 1.0, "n_files": 0}
    tmp = tempfile.mkdtemp(prefix="ex_"); c = tmp + "/r"; shutil.copytree(repo, c, symlinks=True)
    for f in files:
        shutil.copy(f"{t['dir']}/repo/{f}", f"{c}/{f}")
    r = run_tests(t, c, files); shutil.rmtree(tmp)
    # denominators come from the same files at baseline
    b = tempfile.mkdtemp(prefix="exb_"); bc = prepare_repo(t, b + "/r"); br = run_tests(t, bc, files); shutil.rmtree(b)
    tot = br["passed"] + br["failed"]
    return {"passed": r["passed"], "failed": r["failed"], "baseline_total": tot, "frac": round(min(r["passed"], tot) / tot, 4) if tot else 1.0}


# ---------------------------------------------------------------- agent tests
def agent_test_files(t, files):
    """Test files the agent added or modified (not the originals' untouched siblings)."""
    pat = r"(^|/)(test_.*\.py|.*\.test\.ts)$"
    return sorted(p for p in files if under(p, t["tests"]) and re.search(pat, p))


def count_tests(t, repo, paths):
    if not paths:
        return {"files": 0, "passed": 0, "failed": 0}
    r = run_tests(t, repo, paths)
    return {"files": len(paths), "passed": r["passed"], "failed": r["failed"], "rc": r["rc"]}


def lines_to_check(t, repo, changed):
    """Lines of source files the change touched; for test-only tasks, every line of the source modules."""
    src_changed = {p: l for p, l in changed.items() if under(p, t["src"]) and not under(p, t["tests"])}
    if src_changed:
        return src_changed
    out = {}
    for r in t["src"]:
        for p in glob.glob(f"{repo}/{r}/**/*", recursive=True):
            if os.path.isfile(p) and re.search(r"\.(py|ts)$", p) and "__init__" not in p:
                out[os.path.relpath(p, repo)] = set(range(1, len(open(p).read().splitlines()) + 1))
    return out


def coverage(t, repo, paths, targets):
    if not paths or not targets:
        return None
    tmp = tempfile.mkdtemp(prefix="cv_"); c = tmp + "/r"; shutil.copytree(repo, c, symlinks=True)
    cov = covd = 0
    if t["lang"] == "py":
        sh(f"python -m coverage run --branch --data-file=.cov -m pytest -q -p no:cacheprovider {' '.join(paths)}", c, timeout=180)
        sh("python -m coverage json --data-file=.cov -o cov.json", c)
        try: data = json.load(open(c + "/cov.json"))["files"]
        except Exception: shutil.rmtree(tmp); return None
        for p, lines in targets.items():
            d = next((v for k, v in data.items() if k.replace("\\", "/").endswith(p)), None)
            if d is None:
                continue
            ex = set(d["executed_lines"]); mi = set(d["missing_lines"]); exe = (ex | mi) & lines
            cov += len(ex & exe); covd += len(exe)
    else:
        sh(f"node --test --experimental-test-coverage --test-reporter=lcov --test-reporter-destination=lcov.info {' '.join(paths)}", c, timeout=180)
        try: txt = open(c + "/lcov.info").read()
        except Exception: shutil.rmtree(tmp); return None
        for rec in txt.split("end_of_record"):
            m = re.search(r"SF:(.*)", rec)
            if not m: continue
            p = next((k for k in targets if m.group(1).endswith(k)), None)
            if not p: continue
            da = {int(a): int(b) for a, b in re.findall(r"^DA:(\d+),(\d+)", rec, re.M)}
            exe = {l for l in da if l in targets[p]}
            cov += sum(1 for l in exe if da[l] > 0); covd += len(exe)
    shutil.rmtree(tmp)
    return {"covered": cov, "executable": covd, "frac": round(cov / covd, 4) if covd else None}


# ---------------------------------------------------------------- mutation
_CMP = {ast.Eq: ast.NotEq, ast.NotEq: ast.Eq, ast.Lt: ast.LtE, ast.LtE: ast.Lt, ast.Gt: ast.GtE, ast.GtE: ast.Gt, ast.Is: ast.IsNot, ast.IsNot: ast.Is, ast.In: ast.NotIn, ast.NotIn: ast.In}
_BIN = {ast.Add: ast.Sub, ast.Sub: ast.Add, ast.Mult: ast.Div, ast.Div: ast.Mult, ast.FloorDiv: ast.Mult, ast.Mod: ast.Mult}


def py_mutants(src, lines):
    tree = ast.parse(src); par = {}
    for n in ast.walk(tree):
        for c in ast.iter_child_nodes(n): par[c] = n
    nodes = list(ast.walk(tree)); sites = []
    for i, n in enumerate(nodes):
        if getattr(n, "lineno", None) not in lines:
            continue
        if isinstance(n, ast.Compare):
            for k, op in enumerate(n.ops):
                if type(op) in _CMP: sites.append((i, "cmp", k))
        elif isinstance(n, ast.BinOp) and type(n.op) in _BIN: sites.append((i, "bin", 0))
        elif isinstance(n, ast.BoolOp): sites.append((i, "bool", 0))
        elif isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.Not): sites.append((i, "not", 0))
        elif isinstance(n, ast.Constant) and not isinstance(par.get(n), ast.Expr) and not isinstance(par.get(n), ast.JoinedStr):
            if isinstance(n.value, bool) or (isinstance(n.value, int) and not isinstance(n.value, bool)) or (isinstance(n.value, str) and n.value):
                sites.append((i, "const", 0))
        elif isinstance(n, ast.Return) and n.value is not None and not (isinstance(n.value, ast.Constant) and n.value.value is None):
            sites.append((i, "ret", 0))
        elif isinstance(n, (ast.If, ast.While)): sites.append((i, "neg", 0))
    out = []
    for i, kind, k in sites:
        t2 = copy.deepcopy(tree); n = list(ast.walk(t2))[i]
        if kind == "cmp": n.ops[k] = _CMP[type(n.ops[k])]()
        elif kind == "bin": n.op = _BIN[type(n.op)]()
        elif kind == "bool": n.op = ast.Or() if isinstance(n.op, ast.And) else ast.And()
        elif kind == "not":
            p = None
            for q in ast.walk(t2):
                for f, v in ast.iter_fields(q):
                    if v is n: p = (q, f, None)
                    elif isinstance(v, list) and n in v: p = (q, f, v.index(n))
            if not p: continue
            if p[2] is None: setattr(p[0], p[1], n.operand)
            else: getattr(p[0], p[1])[p[2]] = n.operand
        elif kind == "const":
            v = n.value
            n.value = (not v) if isinstance(v, bool) else (v + 1 if isinstance(v, int) else "XX" + v)
        elif kind == "ret": n.value = ast.Constant(None)
        elif kind == "neg": n.test = ast.UnaryOp(ast.Not(), n.test)
        try:
            ast.fix_missing_locations(t2); out.append((f"{kind}@{getattr(n, 'lineno', '?')}", ast.unparse(t2)))
        except Exception:
            pass
    return out


_TS_OPS = [(r" === ", " !== "), (r" !== ", " === "), (r" <= ", " < "), (r" >= ", " > "), (r" < ", " <= "), (r" > ", " >= "), (r" && ", " || "), (r" \|\| ", " && "),
           (r" \+ ", " - "), (r" - ", " + "), (r"\btrue\b", "false"), (r"\bfalse\b", "true"), (r"(?<![=!<>])!(?=[A-Za-z(])", ""), (r"(?<![\w.\"'`$])(\d+)(?![\w.\"'`])", None)]


def ts_mutants(src, lines):
    ls = src.split("\n"); out = []
    for ln in sorted(lines):
        if ln > len(ls): continue
        s = ls[ln - 1]; st = s.strip()
        if not st or st.startswith(("//", "/*", "*", "import ", "export interface", "interface ", "type ")): continue
        for pat, rep in _TS_OPS:
            for m in re.finditer(pat, s):
                new = (str(int(m.group(1)) + 1) if rep is None else rep)
                out.append((f"L{ln}:{pat[:8]}", "\n".join(ls[: ln - 1] + [s[: m.start()] + new + s[m.end():]] + ls[ln:])))
    return out


def run_mutant(t, repo, rel, mutated, tests, probe):
    tmp = tempfile.mkdtemp(prefix="mu_"); c = tmp + "/r"; shutil.copytree(repo, c, symlinks=True)
    open(f"{c}/{rel}", "w").write(mutated)
    if t["lang"] == "ts":
        rc, _ = sh(["node", "--input-type=module", "-e", f"import('./{rel}')"], c, timeout=20)
        if rc != 0:
            shutil.rmtree(tmp); return "invalid"
    rc, out = sh(test_command(t, tests) + (" -x" if t["lang"] == "py" else ""), c, timeout=30)
    shutil.rmtree(tmp)
    return "killed" if rc != 0 else "survived"


def mutation(t, repo, tests, targets, seed):
    """Mutation score of the agent's tests over the changed source lines."""
    if not tests or not targets:
        return {"score": None, "reason": "no tests" if not tests else "no source lines"}
    base = run_tests(t, repo, tests)
    if base["rc"] != 0:
        return {"score": None, "reason": "agent tests fail on final code"}
    muts = []
    for rel, lines in targets.items():
        src = open(f"{repo}/{rel}").read()
        for name, m in (py_mutants if t["lang"] == "py" else ts_mutants)(src, lines):
            if m.strip() != src.strip(): muts.append((rel, name, m))
    random.Random(seed).shuffle(muts); muts = muts[: MUT_CAP + 20]
    with ThreadPoolExecutor(4) as ex:
        res = list(ex.map(lambda m: run_mutant(t, repo, m[0], m[2], tests, None), muts))
    valid = [(m, r) for m, r in zip(muts, res) if r != "invalid"][:MUT_CAP]
    k = sum(1 for _, r in valid if r == "killed")
    return {"score": round(k / len(valid), 4) if valid else None, "killed": k, "total": len(valid), "survivors": [m[1] for m, r in valid if r == "survived"][:15]}


def hidden_mutant_kill(t, repo):
    """For test-writing tasks: do the agent's tests pass on the original and kill the hidden mutants?"""
    spec = json.load(open(f"{t['dir']}/hidden/mutants.json"))
    paths = agent_test_files(t, diff_info(repo)[1])
    if not paths:
        return {"on_original": "no tests", "killed": 0, "total": len(spec["mutants"]), "survivors": []}
    base = run_tests(t, repo, paths)
    ok = base["rc"] == 0 and base["passed"] > 0
    src = open(f"{repo}/{spec['file']}").read(); res = []; survivors = []
    jobs = []
    for i, m in enumerate(spec["mutants"]):
        if m["old"] not in src:
            res.append("badmutant"); survivors.append(f"{i}:old-not-found"); continue
        jobs.append((i, src.replace(m["old"], m["new"], 1)))
    with ThreadPoolExecutor(4) as ex:
        out = list(ex.map(lambda j: run_mutant(t, repo, spec["file"], j[1], paths, None), jobs))
    killed = 0
    for (i, _), r in zip(jobs, out):
        if r == "killed" or r == "invalid": killed += 1
        else: survivors.append(i)
    return {"on_original": "pass" if ok else "fail", "killed": killed if ok else 0, "total": len(spec["mutants"]), "survivors": survivors}


# ---------------------------------------------------------------- lint
def lint_counts(t, repo):
    r = {}
    if t["lang"] == "py":
        rc, out = sh("ruff check --isolated --select E,F,W,B,C4 --line-length 100 --output-format concise src tests", repo)
        r["lint"] = len([l for l in out.splitlines() if re.match(r"\S+:\d+:\d+:", l)])
        rc, out = sh("mypy --ignore-missing-imports --no-error-summary --cache-dir=/dev/null src", repo, timeout=120)
        r["types"] = len([l for l in out.splitlines() if ": error:" in l])
    else:
        tsc = os.path.join(SHARED_NODE, ".bin", "tsc")
        rc, out = sh([tsc, "--noEmit", "-p", "."], repo, timeout=120)
        r["lint"] = 0
        r["types"] = len([l for l in out.splitlines() if "error TS" in l])
    return r


_base_lint = {}


def lint_delta(t, repo):
    if t["id"] not in _base_lint:
        tmp = tempfile.mkdtemp(prefix="lb_"); _base_lint[t["id"]] = lint_counts(t, prepare_repo(t, tmp + "/r")); shutil.rmtree(tmp)
    b = _base_lint[t["id"]]; a = lint_counts(t, repo)
    return {"lint_after": a["lint"], "types_after": a["types"], "lint_delta": a["lint"] - b["lint"], "types_delta": a["types"] - b["types"]}


# ---------------------------------------------------------------- transcript
TESTRUN = re.compile(r"pytest|node --test|npm (run )?test|unittest|coverage run")


WRITE_HINT = re.compile(r"(>>?\s*[\w./\"'-]|sed\s+-i|\btee\b|open\([^)]*['\"][wa]|write_text|writeFileSync|\bcp\b|\bmv\b|git apply|patch\s)")


def transcript(path, t):
    """Tool-use order of the main agent. Writes are Edit/Write calls or Bash commands that write to a path (heredocs, sed -i, python open(..., 'w'))."""
    ev = []
    res = None
    for l in open(path):
        try: e = json.loads(l)
        except Exception: continue
        if e.get("type") == "result": res = e
        if e.get("type") == "assistant":
            for b in e["message"].get("content", []):
                if b.get("type") == "tool_use": ev.append((b["name"], b["input"], e.get("parent_tool_use_id")))
    top = [x for x in ev if x[2] is None]
    test_re = re.compile(r"(\b(tests?)/|\btest_\w*\.py|\.test\.ts|hidden_tests)")
    src_re = re.compile(r"\b(" + "|".join(re.escape(r.rstrip("/")) for r in t["src"]) + r")/[\w./-]+\.(py|ts)")
    writes = []  # (index, kind)
    for i, (name, inp, _) in enumerate(top):
        n = name.lower()
        if n in ("edit", "write"):
            p = inp.get("file_path", ""); rel = p.split("/repo/", 1)[-1] if "/repo/" in p else p
            writes.append((i, "test" if test_re.search(rel) else "other" if not under(rel.lstrip("./"), t["src"]) else "src"))
        elif n == "bash":
            c = inp.get("command", "")
            if WRITE_HINT.search(c) and not re.match(r"\s*(ls|cat|head|grep|git (diff|status|log))\b", c):
                if test_re.search(c): writes.append((i, "test"))
                if src_re.search(c) and re.search(r"(sed\s+-i[^\n]*src/|>>?\s*src/|open\([^)]*src|cat\s*>+\s*src|write_text|\.replace\(|p\s*=\s*['\"]src)", c): writes.append((i, "src"))
    first_test = next((i for i, k in writes if k == "test"), None)
    first_src = next((i for i, k in writes if k == "src"), None)
    last_write = max([i for i, _ in writes], default=-1)
    isrun = lambda x: x[0].lower() == "bash" and TESTRUN.search(x[1].get("command", ""))
    any_run_placeholder = False
    runs_after = any(isrun(x) for x in top[max(last_write, 0):]) if writes else any_run_placeholder
    any_run = any(isrun(x) for x in top)
    skills = [x[1].get("skill", x[1].get("name", "")) for x in top if x[0] == "Skill"]
    agents = sum(1 for x in ev if x[0] in ("Agent", "Task"))
    r = {"tool_calls": len(top), "tests_first": (first_test < first_src) if (first_test is not None and first_src is not None) else None, "wrote_tests_detected": first_test is not None,
         "ran_tests_after_last_edit": runs_after, "ran_tests_any": any_run, "skills": skills, "agents_spawned": agents}
    if res:
        mu = res.get("modelUsage", {}) or {}
        r.update({"cost": res.get("total_cost_usd"), "turns": res.get("num_turns"), "duration_ms": res.get("duration_ms"), "subtype": res.get("subtype"), "is_error": res.get("is_error"),
                  "tokens_out": sum(v.get("outputTokens", 0) for v in mu.values()), "tokens_in": sum(v.get("inputTokens", 0) + v.get("cacheReadInputTokens", 0) + v.get("cacheCreationInputTokens", 0) for v in mu.values()),
                  "final_message": (res.get("result") or "")[:600]})
    return r


def grade(t, repo, jsonl, seed=0):
    patch, files, changed = diff_info(repo)
    src, tst, out = classify(t, files)
    ref = ref_diff(t)
    paths = agent_test_files(t, files)
    targets = lines_to_check(t, repo, changed)
    g = {"task": t["id"], "files_changed": sorted(files), "out_of_scope": out, "src_lines": sum(a + d for a, d in src.values()), "test_lines": sum(a + d for a, d in tst.values()),
         "ref_src_lines": ref["src"], "ref_test_lines": ref["test"]}
    g["diff_ratio"] = round(g["src_lines"] / ref["src"], 3) if ref["src"] else None
    g["hidden"] = hidden_pass(t, repo) if t["kind"] != "tests" else None
    g["existing"] = existing_pass(t, repo)
    g["agent_tests"] = count_tests(t, repo, paths)
    g["coverage"] = coverage(t, repo, paths, targets)
    g["mutation"] = mutation(t, repo, paths, targets, seed)
    if t["kind"] == "tests":
        g["hidden_mutants"] = hidden_mutant_kill(t, repo)
        g["src_untouched"] = not src
        g["hidden_frac"] = round(g["hidden_mutants"]["killed"] / g["hidden_mutants"]["total"], 4) if g["hidden_mutants"]["on_original"] == "pass" and not src else 0.0
    else:
        g["hidden_frac"] = g["hidden"]["frac"]
    g.update(lint_delta(t, repo))
    g["process"] = transcript(jsonl, t)
    g["patch"] = patch
    return g
