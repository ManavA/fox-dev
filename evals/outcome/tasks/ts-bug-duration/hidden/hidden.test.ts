import { test } from "node:test";
import assert from "node:assert/strict";
import { formatDuration, parseDuration } from "../src/duration.ts";

test("decimals", () => {
  assert.equal(parseDuration("1.5h"), 5_400_000);
  assert.equal(parseDuration("0.25s"), 250);
  assert.equal(parseDuration("2.5d"), 216_000_000);
  assert.equal(parseDuration("1.5h30m"), 7_200_000);
});

test("whitespace", () => {
  assert.equal(parseDuration("1h 30m"), 5_400_000);
  assert.equal(parseDuration("  1h   30m  "), 5_400_000);
  assert.equal(parseDuration("\t5s\n"), 5000);
});

test("invalid input throws", () => {
  for (const bad of ["", "   ", "soon", "10 minutes", "5x", "1h junk", "h", "1h30", "30", "1h,30m", "-5s", "1..5h"]) {
    assert.throws(() => parseDuration(bad), undefined, `should reject ${JSON.stringify(bad)}`);
  }
});

test("still parses the basics", () => {
  assert.equal(parseDuration("1h30m"), 5_400_000);
  assert.equal(parseDuration("250ms"), 250);
  assert.equal(parseDuration("2d"), 172_800_000);
  assert.equal(parseDuration("1d2h3m4s5ms"), 93_784_005);
});

test("formatDuration drops zero units", () => {
  assert.equal(formatDuration(3_600_000), "1h");
  assert.equal(formatDuration(90_000), "1m 30s");
  assert.equal(formatDuration(86_400_000 + 5000), "1d 5s");
  assert.equal(formatDuration(1500), "1s 500ms");
  assert.equal(formatDuration(0), "0ms");
  assert.equal(formatDuration(5_405_000), "1h 30m 5s");
  assert.equal(formatDuration(250), "250ms");
  assert.equal(formatDuration(60_000), "1m");
  assert.equal(formatDuration(86_400_000), "1d");
  assert.equal(formatDuration(3_600_001), "1h 1ms");
});

test("formatDuration negative", () => {
  assert.throws(() => formatDuration(-1));
});
