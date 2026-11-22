import { test } from "node:test";
import assert from "node:assert/strict";
import { formatDuration, parseDuration } from "../src/duration.ts";

test("parseDuration", () => {
  assert.equal(parseDuration("1h30m"), 5_400_000);
  assert.equal(parseDuration("250ms"), 250);
  assert.equal(parseDuration("2d"), 172_800_000);
  assert.throws(() => parseDuration("soon"));
});

test("formatDuration", () => {
  assert.equal(formatDuration(5_405_000), "1h 30m 5s");
  assert.equal(formatDuration(250), "250ms");
  assert.equal(formatDuration(0), "0ms");
});
