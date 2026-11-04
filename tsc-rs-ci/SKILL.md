---
name: tsc-rs-ci
description: >-
  Adopt tsc-rs (Rust TypeScript 7 checker) in a JS/TS monorepo for faster CI and
  local typecheck. Use when swapping tsc for tsc-rs, measuring typecheck speedups,
  wiring Bun postinstall trust, or fixing TS7 checker deltas after migration.
---

# tsc-rs for CI and local typecheck

[tsc-rs](https://github.com/pingdotgg/ts-rust) is a drop-in `tsc` CLI (TypeScript **7**
semantics). Same flags as `tsc`; npm package `tsc-rs` (pin a release, e.g. `0.8.x`).

## When to use

- `bun run typecheck` or Wireit/Turbo typecheck jobs are slow on self-hosted or GitHub runners.
- You want one native binary instead of Node driving the checker.
- You are **not** ready to replace emit/build yet — start with `--noEmit` typecheck only.

## Adoption (monorepo)

1. **Pin the tool** at the repo root: `bun add -d tsc-rs@<version>`.
2. **Allow the native postinstall** (Bun blocks it by default):
   `bun pm trust --all` or trust `@tsc-rs/*` / `tsc-rs` only.
3. **Replace checker invocations**, not necessarily the `typescript` package yet:
   - Wireit: `"command": "tsc-rs --noEmit"` (and `-p tsconfig.json` where present).
   - Turbo package scripts: `"typecheck": "tsc-rs --noEmit"`.
   - Avoid `bunx tsc --noEmit` — use `tsc-rs` from the root devDependency.
4. **Run typecheck** and fix any **TS 5 → TS 7** deltas (new errors are expected; they are real checker changes).
   - Common: side-effect `import "./file.css"` → add `declare module "*.css";` in a `.d.ts` file included by the app tsconfig.
5. **Optional speed knob**: `tsc-rs --fast --noEmit` after a clean full check (see upstream README).

Keep **`typescript@5.x`** for emit/build until you deliberately move to
`"typescript": "npm:@tsc-rs/typescript@<version>"` so check and emit stay aligned.

## Measure before you merge

Use the `typecheck-bench` script in this org's scripts repo:

```bash
TYPECHECK_BENCH_LABEL=before typecheck-bench /path/to/repo --runs 1
# apply tsc-rs
TYPECHECK_BENCH_LABEL=after typecheck-bench /path/to/repo --runs 1
```

Record **median wall seconds** with a cold Wireit cache (`typecheck-bench` deletes `.wireit` each run).
Put numbers in the PR body. CI job time drops only if typecheck is on the **critical path**; parallel jobs may still be build-bound — see `ci-build-speed`.

Example outcome on a Wireit monorepo (starter site, Linux/macOS arm64, one machine):

| Checker | Median wall (cold `.wireit`) |
| --- | ---: |
| `tsc --noEmit` | ~78s |
| `tsc-rs --noEmit` | ~8s |

Your repo will differ; always re-measure.

## CI notes

- Install step unchanged; add `tsc-rs` to lockfile.
- On Bun in CI, trust postinstall in the install command or document `bun pm trust` in the workflow if the runner blocks scripts.
- Private `file:` deps (support packages, etc.) must still be present — tsc-rs does not fix missing checkouts.
- Known upstream edge cases: monorepo `rootDir` (TS6059), `tsc -b` without project references — read upstream "Known problems".

## Editor (optional second PR)

Point VS Code / Cursor at `@tsc-rs/typescript` and the TypeScript 7 native preview extension — only after CI typecheck is stable on `tsc-rs`.

## Do not

- Bump every npm dependency in the same PR as the checker swap (separate initiative).
- Claim "10× faster CI" without job timings — measure typecheck job duration with `gh run view`.
