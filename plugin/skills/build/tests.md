# Good and bad tests

## Good: behaviour through the interface

```typescript
test("user can check out with a valid cart", async () => {
  const cart = createCart();
  cart.add(product);
  const result = await checkout(cart, paymentMethod);
  expect(result.status).toBe("confirmed");
});
```

It uses only the public API, describes what (not how), survives internal refactors, and makes one logical assertion.

## Bad: implementation-coupled

```typescript
test("checkout calls paymentService.process", async () => {
  const mockPayment = jest.mock(paymentService);
  await checkout(cart, payment);
  expect(mockPayment.process).toHaveBeenCalledWith(cart.total);
});
```

Red flags: mocking internal collaborators, testing private methods, asserting call counts or order, a name that says how, a test that breaks on a refactor with no behaviour change.

## Bad: verifying through a side channel

```typescript
// Bypasses the interface
await createUser({ name: "Alice" });
expect(await db.query("SELECT * FROM users WHERE name = ?", ["Alice"])).toBeDefined();

// Through the interface
const user = await createUser({ name: "Alice" });
expect((await getUser(user.id)).name).toBe("Alice");
```

## Bad: tautological

```typescript
// Recomputes the expected value the way the code does: passes by construction
const expected = items.reduce((sum, i) => sum + i.price, 0);
expect(calculateTotal(items)).toBe(expected);

// Independent literal
expect(calculateTotal([{ price: 10 }, { price: 5 }])).toBe(15);
```

## Shape

- Arrange, act, assert, in that order.
- Descriptive names: `rejects_expired_token`, not `test_auth_2`.
- In tests, prefer readable repetition (DAMP) over clever shared helpers that hide what is being tested.
- Assert on state and outputs, not on which internal calls happened.
