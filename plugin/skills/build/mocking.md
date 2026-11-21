# When to mock

Preference order: **real > fake > stub > mock**.

- **Real**: the actual implementation. Default for anything you own.
- **Fake**: a working lightweight version (in-memory store, embedded database, temp directory).
- **Stub**: returns canned answers, no logic.
- **Mock**: records and asserts calls. Last resort.

Mock at **system boundaries** only:

- third-party APIs (payments, email, SMS);
- time and randomness;
- sometimes the database or filesystem, when no fake is practical.

Do not mock your own modules or internal collaborators.

## Designing for mockability at boundaries

1. **Inject dependencies** instead of constructing them inside:

```typescript
function processPayment(order, paymentClient) {   // easy to substitute
  return paymentClient.charge(order.total);
}
```

2. **Prefer SDK-style interfaces** (one function per external operation: `getUser`, `createOrder`) over one generic `fetch(endpoint, options)`. Each mock then returns one shape, setup needs no conditional logic, and it is obvious which endpoints a test touches.
