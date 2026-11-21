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
- **Errors**: generic messages to clients, detail only in server logs; failures closed, not open.

Condensed from agent-skills references/security-checklist.md (MIT, see NOTICE.md).
