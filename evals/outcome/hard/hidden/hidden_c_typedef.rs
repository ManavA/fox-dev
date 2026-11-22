//! Hidden acceptance test (hard eval, task c-typedef-fnptr): member calls and stores through
//! typedef'd function-pointer fields behave like the plain `int (*run)(int)` case.
use foxdb::{code, db, inventory, project, tsindex};
use std::sync::Mutex;

static SERIAL: Mutex<()> = Mutex::new(());

/// A project from inline files under a scratch FOXDB_HOME, indexed.
fn inline_project(files: &[(&str, &str)]) -> (tempfile::TempDir, tempfile::TempDir, project::Project) {
    let home = tempfile::tempdir().unwrap();
    // SAFETY: tests touching FOXDB_HOME hold SERIAL.
    unsafe { std::env::set_var("FOXDB_HOME", home.path()) };
    let repo = tempfile::tempdir().unwrap();
    for (path, text) in files {
        let f = repo.path().join(path);
        std::fs::create_dir_all(f.parent().unwrap()).unwrap();
        std::fs::write(f, text).unwrap();
    }
    let mut c = db::open_rw().unwrap();
    let p = project::ensure(&c, &project::locate(repo.path())).unwrap();
    inventory::index_project(&mut c, &p).unwrap();
    tsindex::index_project(&mut c, &p).unwrap();
    (home, repo, p)
}

fn fox_code(p: &project::Project, sym: &str, rel: &str) -> String {
    let c = db::open_ro().unwrap();
    code::run(&c, p, sym, &code::CodeOpts { rel, depth: 2, budget: 6000, cursor: 0, fallback: false }).unwrap()
}

/// Call-site rows of a `callers` answer (`  :13 Child.go c:17 | ...`), joined.
fn rows(out: &str) -> String {
    out.lines().filter(|l| l.trim_start().starts_with(':') && l.trim_start()[1..].starts_with(|c: char| c.is_ascii_digit())).collect::<Vec<_>>().join("\n")
}

const FILES: &[(&str, &str)] = &[
    ("include/ops.h", "typedef int (*op_fn)(int);\ntypedef op_fn op_alias;\nstruct ops {\n\tint count;\n\top_fn run;\n\top_alias stop;\n};\n"),
    ("core/call.c", "#include \"ops.h\"\nint drive(struct ops *o, int x)\n{\n\treturn o->run(x);\n}\nint halt(struct ops *o)\n{\n\treturn o->stop(0);\n}\n"),
    ("drv/a.c", "#include \"ops.h\"\nstatic int a_run(int x) { return x; }\nstatic int a_stop(int x) { return x; }\nstatic struct ops a_ops = {\n\t.count = 3,\n\t.run = a_run,\n\t.stop = a_stop,\n};\n"),
    ("drv/b.c", "#include \"ops.h\"\nstatic int b_run(int x) { return x; }\nvoid b_init(struct ops *o)\n{\n\to->run = b_run;\n}\n"),
];

#[test]
fn typedef_fn_pointer_member_callers_list_calls_and_stores() {
    let _g = SERIAL.lock().unwrap_or_else(|e| e.into_inner());
    let (_h, _r, p) = inline_project(FILES);
    let out = fox_code(&p, "ops.run", "callers");
    assert!(out.contains("1 call sites in 1 files") && rows(&out).contains("drive"), "{out}");
    assert!(out.contains("stores a function in it (not calls): 2\n"), "{out}");
    assert!(out.contains("drv/a.c:6 |") && out.contains("drv/b.c:5 |"), "{out}");
    assert!(!out.contains("references, not calls") && !out.contains("may be incomplete"), "{out}");
}

#[test]
fn typedef_of_a_typedef_member_resolves_too() {
    let _g = SERIAL.lock().unwrap_or_else(|e| e.into_inner());
    let (_h, _r, p) = inline_project(FILES);
    let out = fox_code(&p, "ops.stop", "callers");
    assert!(out.contains("1 call sites in 1 files") && rows(&out).contains("halt") && !rows(&out).contains("drive"), "{out}");
    assert!(out.contains("stores a function in it (not calls): 1\n") && out.contains("drv/a.c:7 |"), "{out}");
}

#[test]
fn function_stored_in_a_typedef_member_is_reached_through_its_calls() {
    let _g = SERIAL.lock().unwrap_or_else(|e| e.into_inner());
    let (_h, _r, p) = inline_project(FILES);
    let out = fox_code(&p, "a_run", "impact");
    assert!(out.contains("drive") && out.contains("via ops.run"), "{out}");
    assert!(!out.contains("halt"), "{out}");
    let out = fox_code(&p, "b_run", "impact");
    assert!(out.contains("drive") && out.contains("via ops.run"), "{out}");
    let out = fox_code(&p, "ops.run", "impact");
    assert!(out.contains("a_run c:") && out.contains("b_run c:") && out.contains("implements ops.run"), "{out}");
    assert!(!out.contains("a_stop c:"), "{out}");
    let out = fox_code(&p, "ops.stop", "impact");
    assert!(out.contains("a_stop c:") && !out.contains("a_run c:") && !out.contains("b_run c:"), "{out}");
}

#[test]
fn plain_data_fields_with_a_typedef_type_are_not_function_members() {
    let _g = SERIAL.lock().unwrap_or_else(|e| e.into_inner());
    let (_h, _r, p) = inline_project(&[
        ("include/t.h", "typedef unsigned long u64x;\nstruct stats { u64x hits; };\n"),
        ("src/s.c", "#include \"t.h\"\nint get(struct stats *s) { return s->hits; }\nint hits_fn(void) { return 1; }\nstatic struct stats g = { .hits = 3 };\nint use(void) { return hits_fn(); }\n"),
    ]);
    // A call of the plain function stays the function's; the data field is not a call target.
    let out = fox_code(&p, "hits_fn", "callers");
    assert!(out.contains("1 call sites in 1 files") && rows(&out).contains("use"), "{out}");
    assert!(!rows(&out).contains("get"), "{out}");
}
