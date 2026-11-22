export interface ParseOptions {
  delimiter?: string;
  /** Treat the first row as column names and return objects. */
  header?: boolean;
}

/** Parse CSV text (RFC 4180 style quoting) into rows of strings. */
export function parseRows(text: string, delimiter = ","): string[][] {
  const rows: string[][] = [];
  let row: string[] = [];
  let field = "";
  let inQuotes = false;
  let i = 0;
  while (i < text.length) {
    const ch = text[i] as string;
    if (inQuotes) {
      if (ch === '"') {
        if (text[i + 1] === '"') {
          field += '"';
          i += 2;
          continue;
        }
        inQuotes = false;
      } else {
        field += ch;
      }
    } else if (ch === '"' && field === "") {
      inQuotes = true;
    } else if (ch === delimiter) {
      row.push(field);
      field = "";
    } else if (ch === "\n" || ch === "\r") {
      if (ch === "\r" && text[i + 1] === "\n") i++;
      row.push(field);
      rows.push(row);
      row = [];
      field = "";
    } else {
      field += ch;
    }
    i++;
  }
  if (inQuotes) throw new Error("unterminated quoted field");
  if (field !== "" || row.length > 0) {
    row.push(field);
    rows.push(row);
  }
  return rows;
}

/** Parse CSV; with `header: true` rows become objects keyed by the first row. */
export function parseCsv(text: string, opts: ParseOptions = {}): string[][] | Record<string, string>[] {
  const rows = parseRows(text, opts.delimiter ?? ",");
  if (!opts.header) return rows;
  const [names, ...rest] = rows;
  if (!names) return [];
  return rest.map((r) => {
    if (r.length !== names.length) throw new Error(`row has ${r.length} fields, expected ${names.length}`);
    const obj: Record<string, string> = {};
    names.forEach((n, idx) => {
      obj[n] = r[idx] as string;
    });
    return obj;
  });
}

function quote(value: string, delimiter: string): string {
  if (value.includes('"') || value.includes("\n") || value.includes("\r") || value.includes(delimiter)) {
    return `"${value.replace(/"/g, '""')}"`;
  }
  return value;
}

/** Serialise rows to CSV with "\n" line endings and no trailing newline. */
export function toCsv(rows: string[][], delimiter = ","): string {
  return rows.map((r) => r.map((v) => quote(v, delimiter)).join(delimiter)).join("\n");
}
