# doc-generator (Claude Code plugin)

Generate the **five-type Mendix handover documentation set** (FS, MG, ARCH, UG, TK) straight
from the `.mpr` model via `mxcli`, lint and version it, and optionally publish to Confluence —
without fabricating anything (technical facts come from the model; business context only from
supplied material).

## Install

```
/plugin marketplace add <git-url-of-this-repo>       # e.g. git@your-org:blackbelt/mendix-doc-generator.git
/plugin install doc-generator@blackbelt
```

Then, one time, authenticate the Confluence (Atlassian) MCP that ships with the plugin:

```
/mcp        # select "atlassian" -> Authenticate (browser sign-in)
```

## Use

From inside any Mendix project directory (the one containing the `.mpr`):

```
/doc-generator:generate-doc          # interactive: scope, language, output, (Confluence)
/doc-generator:publish-confluence    # publish already-generated docs
```

Generated docs are written to **your project's** `docs/generated/`. Templates, the linter, and
`mxcli` are provided by the plugin.

## What's inside

| Path | Purpose |
|------|---------|
| `commands/` | `/generate-doc`, `/publish-confluence` slash commands |
| `skills/` | `generate-handover-docs`, `capture-doc-screenshots`, `track-doc-versions` |
| `templates/` | The five document templates |
| `tools/lint_docs.py` | Deterministic doc linter |
| `bin/` | `mxcli` selector wrapper + per-platform binaries (`mxcli-<os>-<arch>`) + `setup-mxcli` fetcher (on PATH while enabled) |
| `.mcp.json` | Atlassian (Confluence) MCP server declaration |

Bundled assets are referenced via `${CLAUDE_PLUGIN_ROOT}`, so the plugin works from any project.

## Notes & caveats

- **mxcli is cross-platform via a selector.** `bin/mxcli` is a wrapper that detects OS/arch and
  execs `bin/mxcli-<os>-<arch>` (`.exe` on Windows). Bundled today: **linux-amd64** (v0.13.0). To
  support other platforms, either drop the matching build into `bin/` (e.g. `mxcli-darwin-arm64`),
  or set a download source in `bin/mxcli-sources.json` — a `urlTemplate` with `{os}/{arch}/{ext}/
  {version}` placeholders, or per-platform `urls` — and the wrapper auto-fetches it via
  `bin/setup-mxcli` on first use. mxcli has no public download URL, so point it at your internal
  artifact store / release bucket. (Windows runs the wrapper under Claude Code's Git Bash/WSL shell.)
- **The MCP sign-in is per user.** The plugin provides the server config; each teammate does the
  one-time OAuth via `/mcp`. Publishing is optional — repo-only generation needs no MCP.
- **Namespaced commands.** Plugin commands are `/doc-generator:generate-doc` (not `/generate-doc`).

## Local development

```
claude --plugin-dir ./plugins/doc-generator     # load without installing
/reload-plugins                                  # pick up edits live
claude plugin validate ./plugins/doc-generator   # validate structure
```
