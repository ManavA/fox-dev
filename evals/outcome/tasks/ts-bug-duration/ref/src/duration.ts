const UNIT_MS: Record<string, number> = {
  ms: 1,
  s: 1000,
  m: 60_000,
  h: 3_600_000,
  d: 86_400_000,
};

const PART = /^(\d+(?:\.\d+)?)(ms|s|m|h|d)/;

/** Parse strings like "1h30m", "1.5h", "1h 30m" or "250ms" into milliseconds. */
export function parseDuration(input: string): number {
  let rest = input.trim();
  if (rest === "") throw new Error(`invalid duration: ${input}`);
  let total = 0;
  while (rest !== "") {
    const m = PART.exec(rest);
    if (!m) throw new Error(`invalid duration: ${input}`);
    total += Number(m[1]) * (UNIT_MS[m[2] as string] as number);
    rest = rest.slice(m[0].length).trimStart();
  }
  return Math.round(total);
}

/** Format milliseconds as e.g. "1h 30m 5s"; zero units are omitted. */
export function formatDuration(ms: number): string {
  if (ms < 0) throw new Error("negative duration");
  const parts: string[] = [];
  let rest = Math.floor(ms);
  for (const [unit, size] of [["d", 86_400_000], ["h", 3_600_000], ["m", 60_000], ["s", 1000]] as const) {
    const n = Math.floor(rest / size);
    rest -= n * size;
    if (n > 0) parts.push(`${n}${unit}`);
  }
  if (rest > 0 || parts.length === 0) parts.push(`${rest}ms`);
  return parts.join(" ");
}
