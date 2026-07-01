# BlackBelt Claude Code marketplace

Internal Claude Code plugin marketplace. Contains **doc-generator** — generate the five-type
Mendix handover documentation set (FS, MG, ARCH, UG, TK) from the `.mpr` model via mxcli, lint
and version it, and optionally publish to Confluence.

## Install (teammate)

```
claude plugin marketplace add <git-url-of-this-repo>
claude plugin install doc-generator@blackbelt
```

Then run `/doc-generator:generate-doc` from inside any Mendix project directory.
mxcli is fetched per-platform on first use from the public `mendixlabs/mxcli` release — nothing
to build. Confluence publishing is optional and per-user (`/mcp` to authenticate once).

## Zero-setup via devcontainer

For teammates who want it ready on open: copy [`teammate-devcontainer/`](teammate-devcontainer/)
into their Mendix project as `.devcontainer/`, set `MARKETPLACE_URL` to this repo's git URL, and
Reopen in Container — the plugin auto-installs. See its
[README](teammate-devcontainer/README.md).

## Layout

| Path | Purpose |
|------|---------|
| `.claude-plugin/marketplace.json` | Marketplace manifest (this repo). |
| `plugins/doc-generator/` | The plugin (commands, skills, templates, linter, mxcli wrapper). |
| `teammate-devcontainer/` | Drop-in devcontainer that auto-installs the plugin. |

## Updating

After pushing changes here, bump `plugins/doc-generator/.claude-plugin/plugin.json` `version`,
then teammates run:

```
claude plugin marketplace update blackbelt
claude plugin update doc-generator@blackbelt
```

(then restart the Claude session).
