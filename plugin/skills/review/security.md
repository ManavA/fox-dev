# Security checklist (on demand)

- **Threat model**: trust boundaries mapped (requests, uploads, webhooks, third-party APIs, LLM output, files other processes write); assets named (credentials, personal data, payments, admin actions); "how would I misuse this?" asked for each new entry point.
- **Secrets**: none in code, tests, logs or error messages; `.env` and key files ignored; examples use placeholders.
- **Authentication**: passwords hashed with argon2, scrypt or bcrypt; session cookies httpOnly, secure, sameSite; sessions expire; login rate-limited; reset tokens short-lived and single-use.
- **Authorization**: every protected route checks identity, and every resource access checks ownership or role (no IDOR); admin paths check admin; tokens validated (signature, expiry, issuer); keys scoped to least privilege.
- **Input**: validated at the boundary with allowlists; lengths and ranges bounded; formats parsed with real libraries; uploads restricted by type and size and content-checked.
- **Injection**: parameterised queries only; no shell strings built from input; output encoded for its context (HTML, URL, SQL, shell); no `eval` of untrusted data.
- **Transport and headers**: HTTPS; CSP, HSTS, X-Content-Type-Options; CORS restricted to known origins, never `*` with credentials.
- **Data**: sensitive fields encrypted at rest where required; minimum data kept; personal data out of logs.
- **Dependencies**: lockfile committed; audit run; no unmaintained or typo-squatted packages added.
- **LLM features**: model output treated as untrusted input; tool permissions minimal; prompt injection considered for any text the model reads from users or the web; no secrets in prompts.
- **Server-side fetches (SSRF)**: any URL a user influences (webhooks, imports, image proxies, link previews) has its scheme and host allowlisted, every resolved address checked against private, loopback, link-local and reserved ranges (IPv4 and IPv6), and redirects refused.
- **Deletes and overwrites on computed paths**: the resolved target (symlinks followed) sits under an allowlisted root, at least one level below it, with ownership checked before the operation; on refusal, log and stop rather than fall back to a broader path.
- **Rate limits**: general limits on the API, strict ones on auth endpoints; with more than one process serving, the counter lives in a shared store.
- **Errors**: generic messages to clients, no stack traces, detail only in server logs; failures closed, not open.
- **Ask the user first** before adding or changing an auth flow, storing a new kind of sensitive data, adding an external integration or upload handler, changing CORS or rate limits, or granting elevated roles.

Condensed from agent-skills references/security-checklist.md and security-and-hardening (MIT, see NOTICE.md).
