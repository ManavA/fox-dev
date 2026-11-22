import { test } from "node:test";
import assert from "node:assert/strict";
import { parseCsv, parseRows, toCsv } from "../src/csv.ts";

test("simple rows", () => {
  assert.deepEqual(parseRows("a,b\nc,d"), [["a", "b"], ["c", "d"]]);
  assert.deepEqual(parseRows("a,b\nc,d\n"), [["a", "b"], ["c", "d"]]);
  assert.deepEqual(parseRows(""), []);
});

test("empty fields", () => {
  assert.deepEqual(parseRows("a,,c"), [["a", "", "c"]]);
  assert.deepEqual(parseRows("a,"), [["a", ""]]);
  assert.deepEqual(parseRows(",\n,"), [["", ""], ["", ""]]);
});

test("line endings", () => {
  assert.deepEqual(parseRows("a\r\nb\r\n"), [["a"], ["b"]]);
  assert.deepEqual(parseRows("a\rb"), [["a"], ["b"]]);
});

test("quoting", () => {
  assert.deepEqual(parseRows('"a,b",c'), [["a,b", "c"]]);
  assert.deepEqual(parseRows('"say ""hi""",x'), [['say "hi"', "x"]]);
  assert.deepEqual(parseRows('"line1\nline2",x'), [["line1\nline2", "x"]]);
  assert.deepEqual(parseRows('"",x'), [["", "x"]]);
  assert.deepEqual(parseRows('a"b,c'), [['a"b', "c"]]);
  assert.throws(() => parseRows('"open'));
});

test("custom delimiter", () => {
  assert.deepEqual(parseRows("a;b,c\nd;e", ";"), [["a", "b,c"], ["d", "e"]]);
  assert.deepEqual(parseRows("a\tb", "\t"), [["a", "b"]]);
});

test("parseCsv header", () => {
  assert.deepEqual(parseCsv("n,v\nx,1\ny,2", { header: true }), [{ n: "x", v: "1" }, { n: "y", v: "2" }]);
  assert.deepEqual(parseCsv("", { header: true }), []);
  assert.deepEqual(parseCsv("n,v", { header: true }), []);
  assert.throws(() => parseCsv("n,v\nx", { header: true }));
  assert.throws(() => parseCsv("n\nx,1", { header: true }));
  assert.deepEqual(parseCsv("a;b\n1;2", { header: true, delimiter: ";" }), [{ a: "1", b: "2" }]);
});

test("parseCsv without header", () => {
  assert.deepEqual(parseCsv("a,b"), [["a", "b"]]);
  assert.deepEqual(parseCsv("a;b", { delimiter: ";" }), [["a", "b"]]);
});

test("toCsv", () => {
  assert.equal(toCsv([["a", "b"], ["c", "d"]]), "a,b\nc,d");
  assert.equal(toCsv([["a,b", 'say "hi"', "x\ny", "z\rw"]]), '"a,b","say ""hi""","x\ny","z\rw"');
  assert.equal(toCsv([["a;b", "c"]], ";"), '"a;b";c');
  assert.equal(toCsv([["a,b", "c"]], ";"), "a,b;c");
  assert.equal(toCsv([]), "");
  assert.equal(toCsv([[""]]), "");
});

test("round trip", () => {
  const rows = [["a", 'q"uote', "c,d"], ["", "multi\nline", "e"]];
  assert.deepEqual(parseRows(toCsv(rows)), rows);
});
