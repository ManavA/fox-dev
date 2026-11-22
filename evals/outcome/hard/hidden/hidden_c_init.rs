//! Hidden acceptance test (hard eval, task c-initializers): positional and macro-wrapped struct
//! initializers bind each function to the member at its position.
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
    ("include/dev.h", "struct dev_ops {\n\tint (*open)(int);\n\tint (*close)(int);\n\tint (*read)(int);\n};\nstruct chip {\n\tconst char *name;\n\tint flags;\n\tint (*enable)(int);\n\tint (*disable)(int);\n};\n#define DEV_OPS(n, o, c) static const struct dev_ops n = { .open = o, .close = c }\n#define OPEN_CLOSE(o, c) { .open = o, .close = c }\n"),
    ("core/call.c", "#include \"dev.h\"\nint drive(struct dev_ops *o, struct chip *c)\n{\n\to->open(1);\n\to->close(2);\n\to->read(3);\n\tc->enable(1);\n\treturn c->disable(0);\n}\n"),
    ("drv/a.c", "#include \"dev.h\"\nstatic int a_open(int x) { return x; }\nstatic int a_close(int x) { return x; }\nstatic int a_read(int x) { return x; }\nstatic const struct dev_ops a_ops = {\n\ta_open,\n\ta_close,\n\ta_read,\n};\n"),
    ("drv/b.c", "#include \"dev.h\"\nstatic int b_open(int x) { return x; }\nstatic int b_close(int x) { return x; }\nDEV_OPS(b_ops, b_open, b_close);\n"),
    ("drv/c.c", "#include \"dev.h\"\nstatic int c_open(int x) { return x; }\nstatic int c_close(int x) { return x; }\nstatic struct dev_ops c_ops = OPEN_CLOSE(c_open, c_close);\n"),
    ("drv/d.c", "#include \"dev.h\"\nstatic int d_open(int x) { return x; }\nstatic int d_read(int x) { return x; }\nstatic struct dev_ops d_ops = {\n\td_open,\n\t.read = d_read,\n};\n"),
    ("drv/e.c", "#include \"dev.h\"\nstatic int e_open(int x) { return x; }\nstatic int e_close(int x) { return x; }\nstatic int f_open(int x) { return x; }\nstatic struct dev_ops tbl[] = {\n\t{\n\t\te_open,\n\t\te_close,\n\t},\n\t{ f_open },\n};\n"),
    ("drv/g.c", "#include \"dev.h\"\nstatic int g_enable(int x) { return x; }\nstatic int g_disable(int x) { return x; }\nstatic struct chip g_chip = {\n\t\"g\",\n\t0,\n\tg_enable,\n\tg_disable,\n};\n"),
];

#[test]
fn positional_initializers_bind_by_field_order() {
    let _g = SERIAL.lock().unwrap_or_else(|e| e.into_inner());
    let (_h, _r, p) = inline_project(FILES);
    let out = fox_code(&p, "dev_ops.close", "impact");
    for f in ["a_close", "e_close"] {
        assert!(out.contains(&format!("{f} c:")) && out.contains("implements dev_ops.close"), "{f}: {out}");
    }
    for f in ["a_open", "a_read", "e_open", "f_open", "d_open"] {
        assert!(!out.contains(&format!("{f} c:")), "{f} wrongly bound to close: {out}");
    }
    let out = fox_code(&p, "dev_ops.open", "impact");
    for f in ["a_open", "d_open", "e_open", "f_open"] {
        assert!(out.contains(&format!("{f} c:")), "{f}: {out}");
    }
    assert!(!out.contains("a_close c:") && !out.contains("e_close c:"), "{out}");
    let out = fox_code(&p, "dev_ops.read", "impact");
    assert!(out.contains("a_read c:") && out.contains("d_read c:") && !out.contains("a_open c:"), "{out}");
}

#[test]
fn positional_stores_are_listed_as_stores_on_the_member() {
    let _g = SERIAL.lock().unwrap_or_else(|e| e.into_inner());
    let (_h, _r, p) = inline_project(FILES);
    let out = fox_code(&p, "dev_ops.close", "callers");
    assert!(out.contains("stores a function in it (not calls):"), "{out}");
    assert!(out.contains("drv/a.c:7 |") && out.contains("drv/e.c:8 |"), "{out}");
    assert!(!out.contains("drv/a.c:6 |") && !out.contains("drv/a.c:8 |"), "{out}");
    // The call through the member is still the one call site.
    assert!(out.contains("1 call sites in 1 files") && rows(&out).contains("drive"), "{out}");
}

#[test]
fn positional_fields_after_non_function_members_count_them() {
    let _g = SERIAL.lock().unwrap_or_else(|e| e.into_inner());
    let (_h, _r, p) = inline_project(FILES);
    let out = fox_code(&p, "chip.disable", "impact");
    assert!(out.contains("g_disable c:") && !out.contains("g_enable c:"), "{out}");
    let out = fox_code(&p, "chip.enable", "impact");
    assert!(out.contains("g_enable c:") && !out.contains("g_disable c:"), "{out}");
}

#[test]
fn macro_wrapped_initializers_bind_the_macro_arguments() {
    let _g = SERIAL.lock().unwrap_or_else(|e| e.into_inner());
    let (_h, _r, p) = inline_project(FILES);
    let out = fox_code(&p, "dev_ops.close", "impact");
    for f in ["b_close", "c_close"] {
        assert!(out.contains(&format!("{f} c:")) && out.contains("implements dev_ops.close"), "{f}: {out}");
    }
    assert!(!out.contains("b_open c:") && !out.contains("c_open c:"), "{out}");
    let out = fox_code(&p, "dev_ops.open", "impact");
    assert!(out.contains("b_open c:") && out.contains("c_open c:") && !out.contains("b_close c:"), "{out}");
    // The call of the member reaches the function stored through the macro.
    let out = fox_code(&p, "b_close", "impact");
    assert!(out.contains("drive") && out.contains("via dev_ops.close"), "{out}");
    let out = fox_code(&p, "dev_ops.close", "callers");
    assert!(out.contains("drv/b.c:4 |") && out.contains("drv/c.c:4 |"), "{out}");
}

#[test]
fn designated_initializers_keep_working() {
    let _g = SERIAL.lock().unwrap_or_else(|e| e.into_inner());
    let (_h, _r, p) = inline_project(FILES);
    let out = fox_code(&p, "dev_ops.read", "callers");
    assert!(out.contains("drv/d.c:6 |") && out.contains("1 call sites in 1 files"), "{out}");
}
