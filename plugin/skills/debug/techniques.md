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

## Performance regressions

Measure before changing anything: a timing harness, profiler, or query plan, run several times for a stable baseline. Bisect between a fast and a slow known state. Change one thing and re-measure. Report the measured difference, not an impression.
