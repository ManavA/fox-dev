import { test } from "node:test";
import assert from "node:assert/strict";
import { memoizeAsync } from "../src/memoize.ts";

function deferred<T>() {
  let resolve!: (v: T) => void;
  let reject!: (e: unknown) => void;
  const promise = new Promise<T>((res, rej) => { resolve = res; reject = rej; });
  return { promise, resolve, reject };
}

test("caches resolved values", async () => {
  let calls = 0;
  const f = memoizeAsync(async (a: number) => { calls++; return a * 2; });
  assert.equal(await f(2), 4);
  assert.equal(await f(2), 4);
  assert.equal(calls, 1);
  assert.equal(await f(3), 6);
  assert.equal(calls, 2);
});

test("concurrent calls share one in-flight promise", async () => {
  let calls = 0;
  const d = deferred<number>();
  const f = memoizeAsync((_a: number) => { calls++; return d.promise; });
  const p1 = f(1), p2 = f(1);
  assert.equal(calls, 1);
  d.resolve(7);
  assert.deepEqual(await Promise.all([p1, p2]), [7, 7]);
  assert.equal(await f(1), 7);
  assert.equal(calls, 1);
});

test("rejections are not cached, all waiters reject", async () => {
  let calls = 0;
  const d = deferred<number>();
  const f = memoizeAsync((_a: number) => { calls++; return calls === 1 ? d.promise : Promise.resolve(42); });
  const p1 = f(1), p2 = f(1);
  d.reject(new Error("boom"));
  await assert.rejects(p1, /boom/);
  await assert.rejects(p2, /boom/);
  assert.equal(f.size, 0);
  assert.equal(await f(1), 42);
  assert.equal(calls, 2);
});

test("ttl counts from resolution, boundary is stale", async () => {
  let t = 1000;
  let calls = 0;
  const d = deferred<string>();
  const f = memoizeAsync((_a: number) => { calls++; return calls === 1 ? d.promise : Promise.resolve("fresh"); }, { ttlMs: 100, now: () => t });
  const p = f(1);
  t = 1500; // call has been pending for a long time: not stale while pending
  assert.equal(await Promise.race([f(1), Promise.resolve("no")]) === "no" ? "pending" : "x", "pending");
  assert.equal(calls, 1);
  d.resolve("old"); // resolves at t=1500
  assert.equal(await p, "old");
  t = 1599;
  assert.equal(await f(1), "old");
  assert.equal(calls, 1);
  t = 1600;
  assert.equal(await f(1), "fresh");
  assert.equal(calls, 2);
});

test("size ignores known-stale entries", async () => {
  let t = 0;
  const f = memoizeAsync(async (a: number) => a, { ttlMs: 10, now: () => t });
  await f(1); await f(2);
  assert.equal(f.size, 2);
  t = 10;
  assert.equal(f.size, 0);
});

test("maxSize evicts least recently used, hits count as use", async () => {
  const calls: number[] = [];
  const f = memoizeAsync(async (a: number) => { calls.push(a); return a; }, { maxSize: 2 });
  await f(1); await f(2);
  await f(1); // 1 is now most recent
  await f(3); // evicts 2
  assert.equal(f.size, 2);
  calls.length = 0;
  await f(1); await f(3);
  assert.deepEqual(calls, []);
  await f(2);
  assert.deepEqual(calls, [2]);
});

test("evicted in-flight promise resolves for holders but is not stored", async () => {
  const ds = [deferred<string>(), deferred<string>()];
  let n = 0;
  const f = memoizeAsync((_a: number) => ds[n++]!.promise, { maxSize: 1 });
  const p1 = f(1);
  const p2 = f(2); // evicts the pending entry for 1
  assert.equal(f.size, 1);
  ds[0]!.resolve("one");
  assert.equal(await p1, "one");
  assert.equal(f.size, 1);
  ds[1]!.resolve("two");
  assert.equal(await p2, "two");
  // 1 was evicted: a new call must call fn again (ds has no third entry -> throws synchronously inside fn)
  assert.throws(() => f(1));
});

test("joining an in-flight promise counts as a use", async () => {
  const d1 = deferred<number>();
  let calls = 0;
  const f = memoizeAsync((a: number) => { calls++; return a === 1 ? d1.promise : Promise.resolve(a); }, { maxSize: 2 });
  const p1 = f(1);
  await f(2);
  const p1b = f(1); // joins; 1 becomes most recent
  await f(3); // evicts 2, not 1
  d1.resolve(1);
  assert.equal(await p1, 1);
  assert.equal(await p1b, 1);
  const before = calls;
  await f(1);
  assert.equal(calls, before);
});

test("clear detaches in-flight calls", async () => {
  const d = deferred<number>();
  let calls = 0;
  const f = memoizeAsync((_a: number) => { calls++; return calls === 1 ? d.promise : Promise.resolve(2); });
  const p = f(1);
  f.clear();
  d.resolve(1);
  assert.equal(await p, 1);
  assert.equal(f.size, 0);
  assert.equal(await f(1), 2);
  assert.equal(calls, 2);
});

test("delete detaches in-flight calls and reports existence", async () => {
  const d = deferred<number>();
  let calls = 0;
  const f = memoizeAsync((a: number) => { calls++; return a === 1 ? d.promise : Promise.resolve(a); });
  const p = f(1);
  assert.equal(f.delete(1), true);
  assert.equal(f.delete(1), false);
  assert.equal(f.delete(9), false);
  d.resolve(1);
  assert.equal(await p, 1);
  assert.equal(f.size, 0);
  await f(1);
  assert.equal(calls, 2);
});

test("a late rejection of a detached call does not remove the new entry", async () => {
  const d = deferred<number>();
  let calls = 0;
  const f = memoizeAsync((_a: number) => { calls++; return calls === 1 ? d.promise : Promise.resolve(2); });
  const p = f(1);
  f.clear();
  assert.equal(await f(1), 2);
  d.reject(new Error("late"));
  await assert.rejects(p, /late/);
  assert.equal(f.size, 1);
  assert.equal(await f(1), 2);
  assert.equal(calls, 2);
});

test("custom key", async () => {
  let calls = 0;
  const f = memoizeAsync(async (o: { id: number; x: string }) => { calls++; return o.x; }, { key: (o) => String(o.id) });
  await f({ id: 1, x: "a" });
  assert.equal(await f({ id: 1, x: "b" }), "a");
  assert.equal(calls, 1);
});

test("sync throw from fn propagates and is not cached", async () => {
  let calls = 0;
  const f = memoizeAsync((_a: number): Promise<number> => { calls++; if (calls === 1) throw new Error("sync"); return Promise.resolve(5); });
  assert.throws(() => f(1), /sync/);
  assert.equal(f.size, 0);
  assert.equal(await f(1), 5);
});
