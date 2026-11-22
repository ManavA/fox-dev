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

export interface AsyncMemoizeOptions<A extends unknown[]> extends MemoizeOptions<A> {
  ttlMs?: number;
  maxSize?: number;
  now?: () => number;
}

export type MemoizedAsync<A extends unknown[], R> = ((...args: A) => Promise<R>) & {
  clear(): void;
  delete(...args: A): boolean;
  readonly size: number;
};

interface Entry<R> {
  promise: Promise<R>;
  storedAt?: number; // set once resolved
}

/** Memoize an async function: shares in-flight calls, never caches rejections, optional TTL and LRU bound. */
export function memoizeAsync<A extends unknown[], R>(fn: (...args: A) => Promise<R>, opts: AsyncMemoizeOptions<A> = {}): MemoizedAsync<A, R> {
  const keyOf = opts.key ?? ((...args: A) => JSON.stringify(args));
  const now = opts.now ?? Date.now;
  const cache = new Map<string, Entry<R>>(); // insertion order = recency

  const stale = (e: Entry<R>): boolean => opts.ttlMs !== undefined && e.storedAt !== undefined && now() - e.storedAt >= opts.ttlMs;

  const wrapped = ((...args: A): Promise<R> => {
    const k = keyOf(...args);
    const hit = cache.get(k);
    if (hit && !stale(hit)) {
      cache.delete(k);
      cache.set(k, hit);
      return hit.promise;
    }
    if (hit) cache.delete(k);
    const entry: Entry<R> = { promise: undefined as unknown as Promise<R> };
    entry.promise = fn(...args).then(
      (v) => {
        if (cache.get(k) === entry) entry.storedAt = now();
        return v;
      },
      (err) => {
        if (cache.get(k) === entry) cache.delete(k);
        throw err;
      },
    );
    cache.set(k, entry);
    if (opts.maxSize !== undefined) {
      while (cache.size > opts.maxSize) cache.delete(cache.keys().next().value as string);
    }
    return entry.promise;
  }) as MemoizedAsync<A, R>;

  wrapped.clear = () => cache.clear();
  wrapped.delete = (...args: A) => cache.delete(keyOf(...args));
  Object.defineProperty(wrapped, "size", {
    get: () => {
      for (const [k, e] of cache) if (stale(e)) cache.delete(k);
      return cache.size;
    },
  });
  return wrapped;
}
