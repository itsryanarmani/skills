---
name: vscode-extension
description: "Use when building, packaging or publishing a VS Code extension to the Visual Studio Marketplace (vsce) and Open VSX (ovsx, which feeds Cursor, Windsurf, VSCodium and Gitpod)."
---

# Building + publishing a VS Code extension

A VS Code extension is a TypeScript module on the **Extension API** (`package.json` manifest with `contributes`, `activationEvents`, `main`). Source in `integrations/<name>/`. Publish to two marketplaces from one `.vsix`: the **Visual Studio Marketplace** (`vsce`) and **Open VSX** (`ovsx` — what Cursor / Windsurf / VSCodium / Gitpod install from). Command playbook: `itsryanarmani/scripts` `scripts/vscode-extension/README.md`.

## When to use

- **Triggers:** 'build a VS Code extension', 'publish to the VS Code Marketplace', 'vsce package/publish', 'ovsx publish', 'Open VSX', 'vsce segfault', 'SVG restricted in README', 'create a Marketplace publisher'.
- vsce, ovsx and their esbuild packaging segfault on Node 22+ (use Node 20); vsce rejects SVG images in README.md.
- The Marketplace publisher needs a hand-filled browser form and an Azure DevOps PAT; Open VSX is a GitHub login (`ovsx create-namespace`, `ovsx publish -p <token>`). Siblings: raycast-extension, browser-extension.

## The trap that segfaults packaging: Node version

`vsce package` / `vsce publish` / `ovsx publish` run an esbuild-based bundler that **segfaults on Node 22 and 25** (exit 139, no useful error). **Use Node 20 LTS** (`/opt/homebrew/opt/node@20/bin` on PATH, or `nvm use 20`). Same class of failure as several other CLIs — if packaging dies silently, check Node first.

## The other traps

1. **vsce rejects SVG in README.md.** `vsce package` errors "SVGs are restricted in README.md" if the README embeds any `.svg` image. Use PNG, or remove the image. It also warns on a missing `repository`/`license` — add both to `package.json` to keep the listing clean.
2. **`package.json` needs `publisher`.** The `publisher` field = the Marketplace publisher id / the Open VSX namespace. Set it before packaging.
3. **The VS Code Marketplace publisher form fights automation.** Creating a publisher at `marketplace.visualstudio.com/manage/createpublisher` is a React form whose Create button doesn't reliably submit via browser automation (coordinate scaling + trusted-event issues), and it needs a Microsoft-account login + an **Azure DevOps PAT** (scope: Marketplace → Manage) for `vsce publish -p <PAT>`. **Create the publisher + PAT by hand** — it's a 5-minute human step, not worth automating.
4. **Open VSX is the easy path.** GitHub login at `open-vsx.org`, sign the one-time **Eclipse Publisher Agreement**, mint an access token — then it's fully headless.

## Build + package

```
export PATH="/opt/homebrew/opt/node@20/bin:$PATH"   # Node 20
npm install && npm run compile
npx @vscode/vsce package                             # -> <name>-<version>.vsix
```

## Publish

**Open VSX (headless, do this one first):**
```
npx ovsx create-namespace <publisher> -p <OVSX_TOKEN>   # once
npx ovsx publish <name>-<version>.vsix -p <OVSX_TOKEN>   # -> live for Cursor/Windsurf/VSCodium/Gitpod
```

**VS Code Marketplace (after the human publisher + PAT exist):**
```
npx @vscode/vsce publish -p <AZURE_DEVOPS_PAT>
```

Store the tokens in the product `.env.local` (`OVSX_TOKEN`, `VSCE_PAT`), never commit.

## Related skills
- `raycast-extension` — the other dev-tool command surface (needs store screenshots, unlike this).
- `marketplace-app-hosting` — extensions don't need hosting; they're published bundles.
