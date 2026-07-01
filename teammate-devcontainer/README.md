# Teammate devcontainer — Mendix doc generation

Drop-in devcontainer that gives any teammate the `doc-generator` plugin, ready to use, the
moment they open their Mendix project in a container. This is the **Path A (Linux/devcontainer)**
setup — the bundled/fetched mxcli runs natively, so nothing has to be built.

## One-time setup by the maintainer

1. Push the `mendix-doc-generator/` marketplace folder to a git remote your team can reach
   (Azure DevOps, GitHub, GitLab).
2. In [`devcontainer.json`](devcontainer.json), set `MARKETPLACE_URL` to that git URL.
3. Commit this `teammate-devcontainer/` folder alongside the marketplace so teammates can grab it.

## What a teammate does

1. Copy this folder into their Mendix project repo as **`.devcontainer/`** (the repo that
   contains the `.mpr`).
2. In VS Code: **Reopen in Container**.
3. On first build, `postCreate` installs Claude Code + the plugin automatically.
4. Open a Claude session and run:

   ```
   /doc-generator:generate-doc
   ```

   (or `/doc-generator:publish-confluence` to publish already-generated docs).

Docs are written to **their** project's `docs/generated/`. mxcli is fetched per-platform from the
public `mendixlabs/mxcli` release on first use — no manual install.

## Two variants

| File | Use when | Cost |
|------|----------|------|
| `devcontainer.json` (default) | You want the docs. Screenshots come out as `🖼️` placeholders. | Light, fast build. |
| `devcontainer.with-screenshots.json` | You want **real page screenshots**. Rename it to `devcontainer.json`. | Heavy: adds JDK 21 + Node + Playwright + docker-in-docker, and the generator must **build and run the Mendix app** to capture pages (multi-minute). |

Screenshots need two things: Playwright **and** a running app. The lean container has neither
(by design), so it always falls back to placeholders — that is expected, not an error.

## Notes

- **Python** is included (via the devcontainers feature) for the doc linter.
- **No JDK/Node needed for doc generation.** They're only in the screenshot variant, for
  running the app and capturing pages.
- **Confluence publishing** is optional and per-user: each teammate runs `/mcp` once to
  authenticate Atlassian. Repo-only generation needs no MCP.
- To update the plugin after you push changes:
  `claude plugin marketplace update blackbelt && claude plugin update doc-generator@blackbelt`
  (then restart the Claude session).
