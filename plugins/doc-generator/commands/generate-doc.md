---
description: Interactively generate the five-type Mendix handover documentation set (scope, language, output) from the model, with optional Confluence publishing.
---

# Generate Doc (interactive)

Interactive entry point for documentation generation. **Always asks the relevant
questions first** (via AskUserQuestion), then runs the engine. Nothing is
assumed — scope, language, and output are all chosen by the user at run time.

This command is a **router + question flow**. It does not define its own extraction or
template rules — it delegates to the engine skill:

| Engine skill | Produces |
|--------------|----------|
| `${CLAUDE_PLUGIN_ROOT}/skills/generate-handover-docs/SKILL.md` | The **five-type** handover set (FS, MG, ARCH, UG, TK), multi-language folders |

**Read that skill before generating.** Follow it exactly; this command only decides
*what* to generate and *where* to put it, never *how* to structure the docs.

## Usage

| Invocation | Behaviour |
|------------|-----------|
| `/generate-doc` | Run the full interactive flow (recommended). |

All inputs are collected through questions — there are no required flags. This is the **single
entry point** for documentation generation; it routes to the engine skills based on your answers.

## Procedure

### Step 0 — Prepare (silent)
1. **Read the engine skill** listed above, plus the helper skills `track-doc-versions`
   (always applies) and `capture-doc-screenshots` (only if a "with screenshots" output is chosen).
   All three live in `${CLAUDE_PLUGIN_ROOT}/skills/`.
2. **Auto-detect the `.mpr`** in the working directory (`ls *.mpr | head -1`). If several,
   ask which one. Always call the local binary as `mxcli -p <detected>.mpr`.
3. Run `REFRESH CATALOG FULL` once, then `SHOW MODULES`. Classify application modules
   (Source empty, excluding `System`) vs Marketplace/platform modules. Keep this list for
   the scope question.

### Step 1 — Ask the core questions (one AskUserQuestion call, 3 questions)

1. **Scope** — header `Scope`:
   - `Whole app` — every application module (Recommended default if unsure).
   - `Specific module(s)` — triggers the module picker in Step 2.
2. **Language** — header `Language`:
   - `Hungarian (HU)`
   - `English (EN)`
   - `Both HU + EN` — structurally identical versions.
3. **Output** — header `Output` (this single question covers both destination **and**
   screenshots, so no extra popup is needed):
   - `Repo only` — Markdown under `docs/generated/`, screenshot placeholders (Recommended default).
   - `Repo + screenshots` — repo, and auto-capture page screenshots if Playwright can run (Step 4).
   - `Repo + Confluence` — also publish (Step 3), screenshot placeholders.
   - `Repo + Confluence + screenshots` — publish (Step 3) and auto-capture screenshots (Step 4).

### Step 2 — Module picker (only if "Specific module(s)")
Ask a second AskUserQuestion with `multiSelect: true`, header `Modules`, listing the
application modules from Step 0 as options. With many modules, split them across several
multiSelect questions ("tabs"); in that case **every tab must include a `None of these` /
`None in this group` option** so the user can decline a whole group without being forced to
pick an unrelated module just because a tab requires an answer. Only treat genuinely selected
module names as scope; ignore the `None` choices. Warn if the user picks a Marketplace/platform
module (those get a one-line dependency pointer only, not full docs).

### Step 2b — Business sources (optional, every run)
Business narrative is never invented, so offer the user a way to provide it. With a short
plain-text prompt (not a fixed-choice popup), let them either:
- **point at file path(s) or URL(s)** (read files directly; fetch URLs with WebFetch — note that
  authenticated/private URLs can't be fetched, so ask them to paste those instead),
- **paste the text** (user stories, functional doc) straight into the chat, or
- **rely on the `docs/input/<Module>.md` sidecar** / Mendix Documentation fields, or **skip**.

Always auto-check `docs/input/<Module>.md` and the model's Documentation fields regardless. Pass
everything gathered to the engine's business merge (their Step 3). Inline sources and the sidecar
are equal first-class paths — there is no need to create a folder file if the user prefers inline.

### Step 3 — Confluence details (only if "Repo + Confluence")
**First, ensure the Atlassian (Rovo) MCP is connected.** Check whether its tools resolve; if not,
**ask the user whether to connect now** (AskUserQuestion) and walk them through it: run
`claude mcp add --transport http atlassian https://mcp.atlassian.com/v1/mcp/authv2`, then the
**interactive sign-in the user must complete** — `/mcp` → **atlassian** → **Authenticate** (after a
session reload), or `claude mcp login atlassian` in a terminal (the agent cannot finish OAuth; never
run the login in a non-interactive shell). If they decline or it can't be completed, fall back to
repo-only and tell them they can publish later with `/publish-confluence`. Follow the full procedure
in `generate-handover-docs.md` Step 6 (6a.0).

Publishing is **outward-facing — confirm the target before any write.** Once connected, resolve
identity and site first (`atlassianUserInfo`, `getAccessibleAtlassianResources` for the cloudId),
then ask one AskUserQuestion (up to 4 questions):

1. **Space** — header `Space`: ask for the target space (key, title, or `~accountId` for a
   personal space). Resolve via `getConfluenceSpaces`; if ambiguous, list and ask again.
2. **Path** — header `Path`: the ordered folder path under the space (e.g. `A/B/C`), each
   level found-or-created. Default = a single level named after the app/module.
3. **On existing** — header `On existing`: behaviour if the destination docs already exist:
   - `Reuse` — update pages in place (Recommended default).
   - `New` — fresh date-suffixed container at the last path level; leave old intact.
   - `Skip` — stop and report; write nothing.

Follow the full publishing procedure (find-or-create per path segment, `contentFormat:
"markdown"`, ✅/– matrices, save the `.confluence-map.json`, verify one page) from
`generate-handover-docs.md` Step 6.

### Step 4 — Screenshots (only if a "with screenshots" output was chosen)
Follow the **`capture-doc-screenshots`** skill: start the app if needed (confirm first — it is a
heavy, multi-minute build), drive `playwright-cli` to each capturable page, store images under
`docs/generated/<scope>/img/`, and replace the `🖼️` placeholders 1:1 with `![…](img/<Page>.png)`.
It is **best-effort and never blocking** — if `playwright-cli` or the running app is unavailable,
keep the placeholders and note the reason. Report captured-vs-placeholder counts, and remind that
Confluence needs **manual** image upload (the MCP cannot attach files).

If a placeholder-only output was chosen, skip capture entirely and leave `🖼️`/`📄` as-is.

### Step 5 — Generate
Echo the chosen options back in one line, then run the engine: follow
`generate-handover-docs.md` → the five-type set under `docs/generated/<scope>/<lang>/...`.

**Versioning (always):** apply the `track-doc-versions` skill — fingerprint the model, diff against
`docs/generated/<scope>.manifest.json`, and write/append the **Version history** table in each doc.
No model change → no version bump and no new row (say "no model changes since v<X.Y>"); a change →
a major/minor bump with a description of the actual changed elements. Save the manifest.

**Lint (always):** after writing, run `python3 ${CLAUDE_PLUGIN_ROOT}/tools/lint_docs.py docs/generated` and **fix any
ERROR** (leftover `{{placeholders}}`, raw HTML, missing version row) before finishing; surface
remaining WARN/INFO in the report.

Update `docs/generated/README.md` index. Report what was created in plain language, including the
resulting version per scope, lint result, and (if screenshots) captured-vs-placeholder counts.

## Notes
- **Never fabricate.** Technical facts come from `mxcli`/catalog; business context comes
  only from `docs/input/<Module>.md`, Mendix Documentation fields, or user-supplied
  material. Gaps are marked 🟡, not filled with guesses.
- Templates for the five-type set live in `${CLAUDE_PLUGIN_ROOT}/templates/`.
- Preserve localized page titles/labels verbatim.
- Marketplace/platform modules get a one-line dependency pointer only.
- This command never assumes a space, path, language, or scope — all are asked.
