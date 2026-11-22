export interface MemoizeOptions<A extends unknown[]> {
  /** Maps call arguments to a cache key. Defaults to JSON.stringify(args). */
  key?: (...args: A) => string;
}

export type Memoized<A extends unknown[], R> = ((...args: A) => R) & {
  clear(): void;
  delete(...args: A): boolean;
  readonly size: number;
};

/** Memoize a synchronous function. */
export function memoize<A extends unknown[], R>(fn: (...args: A) => R, opts: MemoizeOptions<A> = {}): Memoized<A, R> {
  const keyOf = opts.key ?? ((...args: A) => JSON.stringify(args));
  const cache = new Map<string, R>();
  const wrapped = ((...args: A): R => {
    const k = keyOf(...args);
    if (cache.has(k)) return cache.get(k) as R;
    const v = fn(...args);
    cache.set(k, v);
    return v;
  }) as Memoized<A, R>;
  wrapped.clear = () => cache.clear();
  wrapped.delete = (...args: A) => cache.delete(keyOf(...args));
  Object.defineProperty(wrapped, "size", { get: () => cache.size });
  return wrapped;
}
