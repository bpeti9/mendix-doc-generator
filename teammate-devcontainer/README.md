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

## Notes

- **Python** is included (via the devcontainers feature) for the doc linter.
- **No JDK/Node needed for doc generation.** Add them only if you also want `mx check`
  validation (JDK 21) or Playwright screenshots (Node + `@playwright/cli`).
- **Confluence publishing** is optional and per-user: each teammate runs `/mcp` once to
  authenticate Atlassian. Repo-only generation needs no MCP.
- To update the plugin after you push changes:
  `claude plugin marketplace update blackbelt && claude plugin update doc-generator@blackbelt`
  (then restart the Claude session).
