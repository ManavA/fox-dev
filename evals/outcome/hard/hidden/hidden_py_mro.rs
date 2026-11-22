//! Hidden acceptance test (hard eval, task py-mro): `self.method()` and `super().method()` resolve
//! to the override that Python's method resolution order picks, so callers of each override are right.
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
    ("pkg/__init__.py", ""),
    ("pkg/base.py", "class Base:\n    def run(self):\n        return self.step()\n\n    def step(self):\n        return 1\n"),
    ("pkg/mixins.py", "class Mixin:\n    def step(self):\n        return 2\n\n    def hook(self):\n        return 0\n"),
    ("pkg/child.py", "from pkg.base import Base\nfrom pkg.mixins import Mixin\n\n\nclass Child(Mixin, Base):\n    def go(self):\n        return self.step()\n\n    def both(self):\n        return super().step()\n\n\nclass Leaf(Child):\n    def step(self):\n        return super().step() + 1\n\n    def deep(self):\n        return self.step()\n\n    def inherited(self):\n        return self.go()\n"),
    ("pkg/diamond.py", "class A:\n    def f(self):\n        return 0\n\n\nclass B(A):\n    def f(self):\n        return 1\n\n\nclass C(A):\n    def f(self):\n        return 2\n\n\nclass D(B, C):\n    def g(self):\n        return self.f()\n"),
    ("pkg/skip.py", "class Q:\n    def other(self):\n        return 0\n\n\nclass P:\n    def hook(self):\n        return 1\n\n\nclass R(Q, P):\n    def go(self):\n        return self.hook()\n"),
];

#[test]
fn self_call_reaches_the_first_override_in_mro_order() {
    let _g = SERIAL.lock().unwrap_or_else(|e| e.into_inner());
    let (_h, _r, p) = inline_project(FILES);
    let out = fox_code(&p, "Mixin.step", "callers");
    assert!(rows(&out).contains("Child.go"), "Child(Mixin, Base).go calls Mixin.step: {out}");
    let out = fox_code(&p, "Base.step", "callers");
    assert!(!rows(&out).contains("Child.go"), "Mixin overrides it for Child: {out}");
    assert!(rows(&out).contains("Base.run"), "{out}");
}

#[test]
fn super_calls_follow_the_mro_after_the_current_class() {
    let _g = SERIAL.lock().unwrap_or_else(|e| e.into_inner());
    let (_h, _r, p) = inline_project(FILES);
    let out = fox_code(&p, "Mixin.step", "callers");
    assert!(rows(&out).contains("Child.both") && rows(&out).contains("Leaf.step"), "super() in Child and in Leaf both reach Mixin.step: {out}");
    let out = fox_code(&p, "Base.step", "callers");
    assert!(!rows(&out).contains("Child.both") && !rows(&out).contains("Leaf.step"), "{out}");
}

#[test]
fn a_subclass_override_takes_its_own_self_calls() {
    let _g = SERIAL.lock().unwrap_or_else(|e| e.into_inner());
    let (_h, _r, p) = inline_project(FILES);
    let out = fox_code(&p, "Leaf.step", "callers");
    assert!(rows(&out).contains("Leaf.deep"), "{out}");
    assert!(!rows(&out).contains("Child.go") && !rows(&out).contains("Leaf.inherited"), "{out}");
    let out = fox_code(&p, "Mixin.step", "callers");
    assert!(!rows(&out).contains("Leaf.deep"), "{out}");
}

#[test]
fn diamond_inheritance_picks_the_left_base_first() {
    let _g = SERIAL.lock().unwrap_or_else(|e| e.into_inner());
    let (_h, _r, p) = inline_project(FILES);
    let out = fox_code(&p, "B.f", "callers");
    assert!(rows(&out).contains("D.g"), "{out}");
    let out = fox_code(&p, "C.f", "callers");
    assert!(!rows(&out).contains("D.g"), "{out}");
    let out = fox_code(&p, "A.f", "callers");
    assert!(!rows(&out).contains("D.g"), "{out}");
}

#[test]
fn a_method_defined_only_further_along_the_mro_is_found() {
    let _g = SERIAL.lock().unwrap_or_else(|e| e.into_inner());
    let (_h, _r, p) = inline_project(FILES);
    let out = fox_code(&p, "P.hook", "callers");
    assert!(rows(&out).contains("R.go"), "{out}");
    let out = fox_code(&p, "Mixin.hook", "callers");
    assert!(!rows(&out).contains("R.go"), "{out}");
}
