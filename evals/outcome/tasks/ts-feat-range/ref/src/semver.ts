export interface Version {
  major: number;
  minor: number;
  patch: number;
  prerelease: string[];
}

const RE = /^(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$/;

/** Parse "1.2.3" or "1.2.3-beta.1". Throws on anything else. */
export function parse(input: string): Version {
  const m = RE.exec(input.trim());
  if (!m) throw new Error(`invalid version: ${input}`);
  return {
    major: Number(m[1]),
    minor: Number(m[2]),
    patch: Number(m[3]),
    prerelease: m[4] ? m[4].split(".") : [],
  };
}

export function valid(input: string): boolean {
  return RE.test(input.trim());
}

function comparePre(a: string[], b: string[]): number {
  if (a.length === 0 && b.length === 0) return 0;
  if (a.length === 0) return 1; // a release is greater than its prereleases
  if (b.length === 0) return -1;
  for (let i = 0; i < Math.max(a.length, b.length); i++) {
    const x = a[i];
    const y = b[i];
    if (x === undefined) return -1;
    if (y === undefined) return 1;
    const xn = /^\d+$/.test(x);
    const yn = /^\d+$/.test(y);
    if (xn && yn) {
      if (Number(x) !== Number(y)) return Number(x) < Number(y) ? -1 : 1;
    } else if (xn !== yn) {
      return xn ? -1 : 1; // numeric identifiers sort before alphanumeric
    } else if (x !== y) {
      return x < y ? -1 : 1;
    }
  }
  return 0;
}

/** -1, 0 or 1 following semver precedence. */
export function compare(a: string, b: string): -1 | 0 | 1 {
  const x = parse(a);
  const y = parse(b);
  for (const k of ["major", "minor", "patch"] as const) {
    if (x[k] !== y[k]) return x[k] < y[k] ? -1 : 1;
  }
  return comparePre(x.prerelease, y.prerelease) as -1 | 0 | 1;
}

type Op = ">" | ">=" | "<" | "<=" | "=";
interface Comparator {
  op: Op;
  version: string;
}

const PARTIAL = /^(\d+|[xX*])(?:\.(\d+|[xX*]))?(?:\.(\d+|[xX*]))?(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$/;

interface Partial {
  major?: number;
  minor?: number;
  patch?: number;
  pre?: string;
}

function parsePartial(s: string): Partial {
  const m = PARTIAL.exec(s);
  if (!m) throw new Error(`invalid range: ${s}`);
  const num = (x: string | undefined): number | undefined =>
    x === undefined || /^[xX*]$/.test(x) ? undefined : Number(x);
  const major = num(m[1]);
  const minor = major === undefined ? undefined : num(m[2]);
  const patch = minor === undefined ? undefined : num(m[3]);
  return { major, minor, patch, pre: patch === undefined ? undefined : m[4] };
}

const v = (a: number, b: number, c: number, pre?: string): string =>
  `${a}.${b}.${c}${pre ? `-${pre}` : ""}`;

function lowerOf(p: Partial): string {
  return v(p.major ?? 0, p.minor ?? 0, p.patch ?? 0, p.pre);
}

/** The exclusive upper bound of a partial's x-range, or undefined if unbounded. */
function upperOf(p: Partial): string | undefined {
  if (p.major === undefined) return undefined;
  if (p.minor === undefined) return v(p.major + 1, 0, 0);
  if (p.patch === undefined) return v(p.major, p.minor + 1, 0);
  return undefined;
}

function expand(token: string): Comparator[] {
  const m = /^(\^|~|>=|<=|>|<|=)?\s*(.*)$/.exec(token);
  const op = m?.[1] ?? "";
  const p = parsePartial(m?.[2] ?? "");
  if (p.major === undefined) return op === "<" ? [{ op: "<", version: "0.0.0" }] : [];
  const lo = lowerOf(p);
  if (op === "^") {
    const upper =
      p.major > 0 || p.minor === undefined
        ? v(p.major + 1, 0, 0)
        : p.minor > 0 || p.patch === undefined
          ? v(p.major, p.minor + 1, 0)
          : v(0, 0, (p.patch ?? 0) + 1);
    return [{ op: ">=", version: lo }, { op: "<", version: upper }];
  }
  if (op === "~") {
    const upper = p.minor === undefined ? v(p.major + 1, 0, 0) : v(p.major, p.minor + 1, 0);
    return [{ op: ">=", version: lo }, { op: "<", version: upper }];
  }
  const upper = upperOf(p);
  if (op === "" || op === "=") {
    return upper ? [{ op: ">=", version: lo }, { op: "<", version: upper }] : [{ op: "=", version: lo }];
  }
  if (op === ">") return [{ op: upper ? ">=" : ">", version: upper ?? lo }];
  if (op === "<=") return upper ? [{ op: "<", version: upper }] : [{ op: "<=", version: lo }];
  return [{ op: op as Op, version: lo }];
}

function holds(version: string, c: Comparator): boolean {
  const r = compare(version, c.version);
  switch (c.op) {
    case ">": return r > 0;
    case ">=": return r >= 0;
    case "<": return r < 0;
    case "<=": return r <= 0;
    default: return r === 0;
  }
}

function tuple(s: string): string {
  const x = parse(s);
  return `${x.major}.${x.minor}.${x.patch}`;
}

function satisfiesSet(version: string, set: string): boolean {
  const tokens = set.replace(/(\^|~|>=|<=|>|<|=)\s+/g, "$1").split(/\s+/).filter(Boolean);
  const comps = tokens.flatMap(expand);
  if (!comps.every((c) => holds(version, c))) return false;
  const pre = parse(version);
  if (pre.prerelease.length === 0) return true;
  return comps.some((c) => parse(c.version).prerelease.length > 0 && tuple(c.version) === tuple(version));
}

export function satisfies(version: string, range: string): boolean {
  parse(version);
  return range.split("||").some((set) => satisfiesSet(version, set));
}
