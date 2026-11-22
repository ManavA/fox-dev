import { test } from "node:test";
import assert from "node:assert/strict";
import { compare, parse, valid } from "../src/semver.ts";

test("parse", () => {
  assert.deepEqual(parse("1.2.3"), { major: 1, minor: 2, patch: 3, prerelease: [] });
  assert.deepEqual(parse("1.0.0-beta.2").prerelease, ["beta", "2"]);
  assert.throws(() => parse("1.2"));
});

test("valid", () => {
  assert.equal(valid("1.2.3"), true);
  assert.equal(valid("v1.2.3"), false);
});

test("compare", () => {
  assert.equal(compare("1.2.3", "1.2.3"), 0);
  assert.equal(compare("1.2.3", "1.10.0"), -1);
  assert.equal(compare("2.0.0", "1.9.9"), 1);
  assert.equal(compare("1.0.0-alpha", "1.0.0"), -1);
  assert.equal(compare("1.0.0-alpha.2", "1.0.0-alpha.10"), -1);
});
