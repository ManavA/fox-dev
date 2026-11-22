import { test } from "node:test";
import assert from "node:assert/strict";
import { memoize } from "../src/memoize.ts";

test("caches by args", () => {
  let calls = 0;
  const f = memoize((a: number, b: number) => { calls++; return a + b; });
  assert.equal(f(1, 2), 3);
  assert.equal(f(1, 2), 3);
  assert.equal(calls, 1);
  assert.equal(f(2, 1), 3);
  assert.equal(calls, 2);
});

test("clear and delete", () => {
  const f = memoize((a: number) => a * 2);
  f(1); f(2);
  assert.equal(f.size, 2);
  assert.equal(f.delete(1), true);
  assert.equal(f.delete(1), false);
  f.clear();
  assert.equal(f.size, 0);
});

test("custom key", () => {
  let calls = 0;
  const f = memoize((o: { id: number }) => { calls++; return o.id; }, { key: (o) => String(o.id) });
  f({ id: 1 }); f({ id: 1 });
  assert.equal(calls, 1);
});
