---
description: Publish already-generated Mendix docs from docs/generated/ to Confluence (space / path / on-existing).
argument-hint: "[scope] [--space KEY] [--path \"A/B\"] [--on-existing reuse|new|skip]"
---

# Publish Confluence

Publish **already-generated** documentation from `docs/generated/` to Confluence — the same
way the generator's Confluence step does, but **without generating or modifying any docs**.
This command only **reads** local Markdown and **writes** to Confluence; it never touches the
Mendix model or the `docs/generated/*.md` files.

Use it when the docs already exist (from `/generate-doc`) and you just want to (re)publish them.

**The publishing mechanics are not redefined here.** Follow `generate-handover-docs.md`
**Step 6 (6a–6g)** exactly — identity/site resolution, find-or-create per path segment,
`contentFormat: "markdown"`, ✅/– matrices, the `.confluence-map.json` idempotency map, and the
post-publish verify. This command only decides **what to publish** and collects the **same
target questions** the generator asks.

## Usage

| Invocation | Behaviour |
|------------|-----------|
| `/publish-confluence` | Interactive: pick a generated scope, then ask space / path / on-existing. |
| `/publish-confluence <scope>` | Publish a known scope, e.g. `/publish-confluence <ModuleName>`. |
| `/publish-confluence <scope> --space <KEY> --path "A/B" --on-existing reuse` | Non-interactive. |

### Options (same semantics as the generator)
| Option | Meaning |
|--------|---------|
| `--space <KEY \| name>` | Target space (key, title, or `~accountId` for personal). Asked if omitted. |
| `--path "A/B/C"` | Ordered folder path under the space; each level found-or-created. Default: one level = the scope name. |
| `--parent <pageId>` | Existing page id the path hangs off (pins the start). |
| `--on-existing reuse\|new\|skip` | If destination pages exist: `reuse` (update in place, default), `new` (date-suffixed container), `skip` (stop, write nothing). |
| `--lang <a,b>` | Which language folder(s) to publish, if the scope has several. Default: all present. |

## Procedure

### Step 0 — Discover what's already generated (no model access)
1. Read `docs/generated/README.md` and/or scan `docs/generated/`. Build the list of scopes and,
   per scope, which languages exist:
   - **Five-type set:** `docs/generated/<Scope>/<lang>/FS|MG|ARCH|UG|TK_*.md`
2. If nothing is generated, **stop** and suggest running `/generate-doc` first.
3. Ignore non-deliverables: `*.manifest.json`, `README.md` index, and `img/` folders.

### Step 1 — Pick what to publish
If a scope was named on the command line, use it. Otherwise ask one AskUserQuestion listing the
discovered scopes. If the chosen scope has **both** shapes or **multiple languages**, ask which
to publish (multiSelect). Map the selection to the concrete `.md` files to upload.

### Step 2 — Ensure the MCP is connected, then resolve identity and site
**First ensure the Atlassian (Rovo) MCP is connected** (follow `generate-handover-docs.md` Step
6a.0): if its tools don't resolve, **ask the user whether to connect now** and walk them through
`claude mcp add --transport http atlassian https://mcp.atlassian.com/v1/mcp/authv2` + the
interactive sign-in (`/mcp` → **atlassian** → **Authenticate**, or `claude mcp login atlassian`) —
**the user completes OAuth**, the agent can't (never run the login in a non-interactive shell). If
they decline, stop and say it can be published once the MCP is connected.

Then (read-only first): `atlassianUserInfo`, then `getAccessibleAtlassianResources` for the
**cloudId**; confirm the site if several are accessible. (Step 6a.)

### Step 3 — Ask the target (same questions as the generator's Confluence step)
Publishing is **outward-facing — confirm the target before any write.** Ask one AskUserQuestion:
1. **Space** — `--space` if given, else ask; resolve via `getConfluenceSpaces`.
2. **Path** — `--path` if given, else ask; default a single level = the scope name.
3. **On existing** — `Reuse` (default) / `New` / `Skip`.

### Step 4 — Publish (follow generate-handover-docs.md Step 6)
Walk the path find-or-create per segment (6c), publish each doc with `contentFormat: "markdown"`
(6e), and resolve the hierarchy to:

```
<Space> / <path…> / <Language> / FS · MG · ARCH · UG · TK
```

Reuse the existing `docs/generated/<scope>/.confluence-map.json` for idempotency — prefer the map,
fall back to find-or-create, and **update** existing pages rather than duplicating (6f).
Save/refresh the map. Verify one page afterward (6g).

## Notes
- **Does not regenerate.** If the local docs may be stale versus the current model, say so and
  suggest `/generate-doc`; optionally compare the live model fingerprint to the saved
  `*.manifest.json` (via `track-doc-versions`) and warn if they differ — but do **not** change
  the docs here.
- **Screenshots:** the Atlassian MCP cannot upload attachments, so any `![…](img/…)` images and
  `🖼️` placeholders will not render on Confluence — they must be added manually (drag-drop). The
  references mark where each goes.
- The `.manifest.json` and `img/` folders are **not** published.
- Nothing about a space, path, or scope is assumed — all are asked unless passed as flags.
