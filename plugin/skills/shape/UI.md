# UI prototype

Several radically different variants of one screen, switchable in place, so the user can compare by looking rather than by reading descriptions.

1. **Prefer adjusting an existing page.** Render the variants inside the real route, switched by a URL search param (`?variant=a`). Build a new throwaway route only when no page exists yet, and follow the project's routing convention for it.
2. **State the question and pick N** (usually 3). Each variant answers the question differently: layout, density, navigation model. Variants that differ only in colour are one variant.
3. **Wire them** behind one switch on the param; share real data loading so only presentation differs.
4. **Add a floating switcher bar** at the bottom: variant names, prev/next, current one highlighted. Mark it clearly as a prototype.
5. **Hand it over** with the one command that starts it.
6. **Capture and clean up.** Record which variant won and why in the spec, port the winner properly with tests through `fox-dev:build`, and remove the switcher and losing variants from main (keep them on a throwaway branch if useful).

Avoid: polishing a variant before the choice is made, inventing new top-level structure, mixing prototype code into production components.
