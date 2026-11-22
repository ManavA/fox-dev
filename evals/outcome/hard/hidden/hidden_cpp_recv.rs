//! Hidden acceptance test (hard eval, task cpp-receiver): a C++ member call whose receiver has a
//! declared type reaches that class's method, not a guess among same-name methods.
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
    ("src/engine.hpp", "class Engine {\npublic:\n    int start(int x) { return x; }\n    int stop() { return 0; }\n};\n"),
    ("src/pump.hpp", "class Pump {\npublic:\n    int start(int x) { return x + 1; }\n};\n"),
    ("src/valve.hpp", "class Valve {\npublic:\n    int start(int x) { return x + 2; }\n};\n"),
    ("src/car.cpp", "#include \"engine.hpp\"\n#include \"pump.hpp\"\n#include \"valve.hpp\"\n#include <memory>\nstruct Car {\n    Engine eng;\n    Pump* pump;\n};\nint local_obj() {\n    Engine e;\n    return e.start(1);\n}\nint by_ptr(Pump* p) {\n    return p->start(2);\n}\nint by_ref(const Pump& p) {\n    return p.start(3);\n}\nint by_member(Car& c) {\n    return c.eng.start(4) + c.pump->start(5);\n}\nint by_auto_ctor() {\n    auto e = Engine();\n    return e.start(6);\n}\nint by_make_unique() {\n    auto p = std::make_unique<Pump>();\n    return p->start(7);\n}\nint by_valve(Valve v) {\n    return v.start(8);\n}\nint unknown(T t) {\n    return t.start(9);\n}\n"),
];

fn row_for<'a>(out: &'a str, func: &str) -> Option<&'a str> {
    out.lines().find(|l| l.trim_start().starts_with(':') && l.contains(&format!(" {func} c:")))
}

fn certain(out: &str, funcs: &[&str]) {
    for f in funcs {
        let r = row_for(out, f).unwrap_or_else(|| panic!("{f} missing: {out}"));
        assert!(!r.contains("guess"), "{f} should be a certain call: {out}");
    }
}

fn absent(out: &str, funcs: &[&str]) {
    for f in funcs {
        assert!(row_for(out, f).is_none(), "{f} must not call it: {out}");
    }
}

#[test]
fn locals_params_and_members_of_a_known_type_reach_their_class() {
    let _g = SERIAL.lock().unwrap_or_else(|e| e.into_inner());
    let (_h, _r, p) = inline_project(FILES);
    let out = fox_code(&p, "Engine.start", "callers");
    certain(&out, &["local_obj", "by_member", "by_auto_ctor"]);
    absent(&out, &["by_ptr", "by_ref", "by_make_unique", "by_valve"]);
}

#[test]
fn pointer_and_reference_receivers_reach_their_class() {
    let _g = SERIAL.lock().unwrap_or_else(|e| e.into_inner());
    let (_h, _r, p) = inline_project(FILES);
    let out = fox_code(&p, "Pump.start", "callers");
    certain(&out, &["by_ptr", "by_ref", "by_member"]);
    absent(&out, &["local_obj", "by_valve", "by_auto_ctor"]);
}

#[test]
fn smart_pointer_factories_give_the_receiver_its_type() {
    let _g = SERIAL.lock().unwrap_or_else(|e| e.into_inner());
    let (_h, _r, p) = inline_project(FILES);
    let out = fox_code(&p, "Pump.start", "callers");
    certain(&out, &["by_make_unique"]);
    let out = fox_code(&p, "Valve.start", "callers");
    certain(&out, &["by_valve"]);
    absent(&out, &["by_make_unique", "by_ptr"]);
}

#[test]
fn an_untyped_receiver_stays_a_guess_or_unresolved_never_certain() {
    let _g = SERIAL.lock().unwrap_or_else(|e| e.into_inner());
    let (_h, _r, p) = inline_project(FILES);
    for q in ["Engine.start", "Pump.start", "Valve.start"] {
        let out = fox_code(&p, q, "callers");
        if let Some(r) = row_for(&out, "unknown") {
            assert!(r.contains("guess"), "{q}: {out}");
        }
    }
}

#[test]
fn only_the_untyped_receiver_is_still_a_guess() {
    let _g = SERIAL.lock().unwrap_or_else(|e| e.into_inner());
    let (_h, _r, p) = inline_project(FILES);
    let out = fox_code(&p, "Engine.start", "callers");
    // Three typed calls are certain; only the receiver of unknown type is a guess.
    assert!(out.contains("4 call sites in 1 files, 1 guessed by name"), "{out}");
    // Engine.stop has one definition and no caller; nothing leaks onto it.
    let out = fox_code(&p, "Engine.stop", "callers");
    assert!(out.contains("0 call sites"), "{out}");
}
