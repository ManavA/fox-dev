# Performance checklist (on demand)

Measure first: a baseline from a profiler, timing harness, query plan or Lighthouse run, before and after the change.

## Backend
- No N+1 queries; queries use indexes (check the plan); result sets paginated or bounded.
- No unbounded loads into memory; stream large inputs.
- Expensive pure work cached with a clear invalidation rule; repeated network calls batched.
- Slow or non-urgent work moved off the request path (queue, background job).
- Timeouts on every outbound call; connection pools sized.
- Hot loops avoid allocation and repeated parsing; algorithms suit the input size.

## Frontend
- Core Web Vitals targets: LCP under 2.5 s, INP under 200 ms, CLS under 0.1.
- Images in modern formats, responsively sized, with width and height; below-the-fold lazy; the LCP image not lazy and high priority.
- Initial JS bundle small (around 200 KB gzipped); routes and heavy features code-split; no blocking scripts in `<head>`.
- Long tasks over 50 ms broken up so input stays responsive; non-urgent work deferred.
- Critical CSS inlined; fonts limited, WOFF2, preloaded when on the LCP path, `font-display: swap`.
- Static assets cached with long max-age and content hashes.

## Anti-patterns
Optimising without a measurement; caching without invalidation; memoising everything; premature micro-optimisation off the hot path.

Condensed from agent-skills references/performance-checklist.md (MIT, see NOTICE.md).
