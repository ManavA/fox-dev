# Debugging techniques

## Root-cause tracing

Bugs often surface deep in a call chain (a file written to the wrong directory, a database opened with the wrong path). Fixing where the error appears treats the symptom.

1. **Observe the symptom** exactly (message, value, location).
2. **Find the immediate cause**: the line that directly produced it.
3. **Ask what called it, with what values.** Walk one frame up at a time.
4. **Keep going** until you reach the first place the value was wrong (often a default, an empty string, a test fixture, an environment variable).
5. **Fix at that source.** Then consider defense in depth below.

When you cannot walk the chain by reading, add a stack capture at the failure point (`new Error().stack`, `traceback.print_stack()`, `std::backtrace`) that also logs the suspect values, run the loop, and read upward. To find which test pollutes shared state, bisect the test list: run halves until one test reproduces it.

## Defense in depth

After fixing the root cause of bad data, consider validating at each layer the data passes, so the bug becomes structurally impossible rather than fixed once:

- **Entry point**: reject obviously invalid input at the API boundary.
- **Business logic**: check the preconditions this operation relies on.
- **Environment guards**: refuse dangerous operations in the wrong context (for example, destructive file operations outside a temp dir during tests).
- **Diagnostics**: log enough context at the failure point to debug the next case.

Apply this where the cost of the bug justifies it; one well-placed check is often enough.

## Condition-based waiting

Flaky tests often guess at timing with sleeps. Wait for the condition you care about instead:

```typescript
// Guessing
await new Promise(r => setTimeout(r, 50));
expect(getResult()).toBeDefined();

// Waiting for the condition, with a timeout and a clear failure message
await waitFor(() => getResult() !== undefined, { timeoutMs: 5000, what: "result ready" });
expect(getResult()).toBeDefined();
```

Poll at a short interval, fail with a message naming the condition, and keep a hard timeout. Keep a fixed delay only when timing itself is under test (debounce, throttle), and comment why.

## Performance work

Use this loop both for a regression and for "make it faster".

1. **Measure** a baseline with real data: a profiler, timing harness, query plan (`EXPLAIN ANALYZE`) or Lighthouse run, several times so you know the run-to-run noise. For a regression, bisect between a fast and a slow known state.
2. **Find the bottleneck** in the profile, not by guessing. Usual suspects: N+1 queries, unbounded fetches, a query that ignores its index, connection-pool waits (every endpoint slows at once), missing or mis-keyed caching, long main-thread tasks, oversized bundles or images. See [performance.md](../review/performance.md).
3. **Fix that one thing.** One change per measurement, or the number cannot be attributed.
4. **Re-measure the same way** (same command, conditions and budget) and decide strictly: past the noise with tests green, keep it and put before and after numbers in the commit; inside the noise, worse, or faster but a test went red, revert it. A win that drops work the product needs is a regression.
5. **Log every attempt**, reverted ones too (idea, baseline to result, verdict, why), in the PR or a notes file, so a dead idea is not retried.
6. **Guard** the metric users feel with a budget check in CI (compare a median, not one run) or a monitor, and re-baseline when it fires.
