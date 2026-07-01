---
name: generate-handover-docs
description: Generate the five-type Mendix handover documentation set (FS, MG, ARCH, UG, TK) for an app or modules from the model via mxcli, and optionally publish to Confluence. Use when generating Mendix handover or technical documentation.
---

# Skill: generate-handover-docs

Generate the **five-type handover documentation set** for a Mendix application or one
or more modules, and (optionally) **publish it to Confluence**.

Read this skill in full before generating. It defines the extraction recipe (technical
facts come from the model, never invented), the business merge rules, the five fixed
document templates, the highlighting conventions, and the Confluence publishing
procedure and its formatting gotchas.

This skill is **project-agnostic**. Nothing here is tied to a specific app, module, space
or site — every such value is resolved at run time or passed as an argument.

---

## The document set (five types per scope)

| Code | Document | Template |
|------|----------|----------|
| **FS** | Functional Specification (black-box, by screen, data interfaces) | `${CLAUDE_PLUGIN_ROOT}/templates/FS_Functional_Specification.template.md` |
| **MG** | Operations Guide (config, scheduled events, logging, errors) | `${CLAUDE_PLUGIN_ROOT}/templates/MG_Operations_Guide.template.md` |
| **ARCH** | Architecture (building blocks, domain model, diagram, integrations) | `${CLAUDE_PLUGIN_ROOT}/templates/ARCH_Architecture.template.md` |
| **UG** | User Guide (step-by-step screen walkthrough) | `${CLAUDE_PLUGIN_ROOT}/templates/UG_User_Guide.template.md` |
| **TK** | Developer & Support Documentation (glossary, install, functions + permission matrices, data types, support runbook) | `${CLAUDE_PLUGIN_ROOT}/templates/TK_Developer_Support_Documentation.template.md` |

Always start from these templates so every module reads the same. See
`${CLAUDE_PLUGIN_ROOT}/templates/README.md` for the conventions baked into them.

---

## Core principles

1. **Technical facts are extracted, never guessed.** Entities, attributes, associations,
   microflows, pages, roles, constants and dependencies all come from `mxcli` / catalog
   queries. If a fact isn't in the model, it does not go in the doc.
2. **Business context is layered, not fabricated.** Business narrative comes only from
   (a) **inline sources the user points to at run time** — file path(s), URL(s), or pasted text,
   (b) the team sidecar at `docs/input/<Module>.md`, and (c) Mendix **Documentation fields** on
   elements. Inline and sidecar are equal first-class paths. If none exists, say so — do **not**
   invent purpose or behaviour.
3. **Same templates every time.** Use the five templates above, in their section order.
4. **Mark, don't invent.** Anything uncertain gets a highlight (see below), not a guess.
5. **No machine-written tells.** Plain, human voice. No "as an AI", no provenance notes,
   no tool names in the deliverable. Preserve localized UI labels verbatim and gloss them.

---

## Step 0 — Resolve the project file (no hardcoding)

Auto-detect the `.mpr` in the working directory; never assume a name:

```bash
MPR=$(ls *.mpr 2>/dev/null | head -1)
mxcli -p "$MPR" -c "SHOW MODULES"
```

If there are multiple `.mpr` files, ask the user which one. Always call the local binary
as `mxcli`.

---

## Step 1 — Resolve scope

- **App scope** (the `/generate-doc` "Whole app" choice): document every **application module** —
  rows in `SHOW MODULES` where the `Source` column is **empty**, excluding `System`.
  Marketplace/platform modules (rows with a `Source`) are out of scope except as one-line
  dependency pointers.
- **Module scope** (the `/generate-doc` "Specific module(s)" choice): document only the chosen
  module(s). Still classify each; warn if the user picked a Marketplace module.

Run `REFRESH CATALOG FULL` once at the start so catalog queries are populated.

---

## Step 2 — Extract per module (the recipe)

Substitute `$M` with the module name and `$MPR` with the detected project file.

```bash
# Structure, folders, scheduled events (interval/enabled NOT exposed — note "set in Studio Pro/Cloud Portal")
mxcli -p "$MPR" -c "SHOW STRUCTURE DEPTH 3 IN $M ALL"

# Domain model
mxcli -p "$MPR" -c "SHOW ENTITIES IN $M"
mxcli -p "$MPR" -c "SHOW ASSOCIATIONS IN $M"
mxcli -p "$MPR" -c "SHOW ENUMERATIONS IN $M"
mxcli -p "$MPR" -c "DESCRIBE ENTITY $M.<Entity>"   # run for EVERY entity (business, staging, AND non-persistent) — full attribute list, types, indexes, event handlers, access

# Microflows (group by prefix convention — see note)
mxcli -p "$MPR" -c "SELECT Name, MicroflowType, ReturnType, ActivityCount, Complexity FROM CATALOG.MICROFLOWS WHERE ModuleName='$M' ORDER BY Name"

# Pages, navigation, security, constants
mxcli -p "$MPR" -c "SHOW PAGES IN $M"
mxcli -p "$MPR" -c "SHOW NAVIGATION MENU"           # map the module's menu group(s); EVERY page there needs a Functions subsection, incl. Administrator-only pages
mxcli -p "$MPR" -c "SHOW MODULE ROLES IN $M"
mxcli -p "$MPR" -c "SHOW SECURITY MATRIX IN $M"
mxcli -p "$MPR" -c "SELECT Name, DataType, DefaultValue, ExposedToClient FROM CATALOG.CONSTANTS WHERE ModuleName='$M'"

# Cross-module dependencies (real architecture)
mxcli -p "$MPR" -c "SHOW CALLEES OF $M.<EntryFlow>"   # collect callees outside $M and outside utility modules
```

**Microflow prefix convention (configurable per project).** A common convention groups
flows as `ACT_` (action), `DS_` (data source), `NAV_` (navigation), `SE_` (scheduled-event
logic), `SUB_` (sub-process), `VAL_` (validation). If a project uses different prefixes,
detect them from the names and adapt — do not assume these.

Flag high-complexity flows (Complexity ≥ 5 or ActivityCount ≥ 20) as "review carefully"
in the support notes.

---

## Step 3 — Gather business context

Pull business narrative from any of these sources (all optional; merge whatever exists):
1. **Inline sources the user points to at run time** — file path(s) anywhere (read directly),
   URL(s) (fetch with WebFetch; authenticated/private URLs can't be fetched — ask the user to
   paste those), or text pasted straight into the chat.
2. **`docs/input/<Module>.md`** sidecar, if present.
3. **Mendix Documentation fields** (from the catalog) on the module/entities/microflows.

Inline sources and the sidecar are equal first-class paths — use whichever the user provides, or
both. If all are empty, the business sections state that no business source was found and where to
add it. Never fabricate.

---

## Step 4 — Assemble the five documents

Fill each template. Produce them in the language(s) the user wants (a common setup is a
primary language plus English). Keep both/all language versions structurally identical.

### Versioning (automatic, every run)
Follow the **`track-doc-versions`** skill: fingerprint the model facts extracted in Step 2,
diff against `docs/generated/<scope>.manifest.json`, and write the **Version history** table
(top of every doc, newest row last). An unchanged model → no version bump and no new row; a
changed model → a major/minor bump and a description listing the actual changed elements. Save
the updated manifest (not a deliverable — exclude it from any Confluence publish).

### Highlighting conventions (use in every doc)
Put this legend near the top of each doc and apply the cues inline:

> **Highlighting key:** 🟡 = assumption / to be confirmed · 🔴 = needs changing / open issue.

- 🟡 prefix for any assumed/unconfirmed value (e.g. a cadence not exposed by the model).
- 🔴 prefix for open points, blocked items, tech debt, things that must change.

### Access / permission matrices
Render as a **markdown table** with **✅** = allowed and **–** = not allowed, e.g.:

```
| Function | RoleA | RoleB |
|----------|:---:|:---:|
| List | ✅ | ✅ |
| Delete | ✅ | – |
```

(Do **not** use HTML `<td>`/`<mark>` cells — they survive in GitHub/VSCode but are
**escaped to literal text by Confluence markdown**. The ✅/– table renders everywhere.)

### Diagrams
Use fenced ```mermaid``` blocks (architecture: `flowchart TB`; context: hub-and-spoke
`flowchart RL` with `classDef` colors). See the rendering note in Step 6.

### Screenshots / file samples
Leave marked placeholders: `🖼️ [Screenshot: …]`, `📄 [File sample: …]`.

**TK Functions must cover every menu page — one subsection each.** Give **every page** in the
module's navigation menu group(s) its **own** numbered subsection with its **own** access matrix —
cross-check `SHOW NAVIGATION MENU` against `SHOW PAGES IN $M` so none is omitted, and explicitly
include **Administrator-only pages** (interface/staging data, master-data admin) as their own
subsections (do **not** merge several pages into one). Each also gets a screenshot (overview +
edit/detail dialogs) and samples of useful artifacts (generated documents/PDFs, key filters, notable
error/empty states). One `🖼️` (or `📄`) placeholder per page/artifact. In **§4.2 Entities**, give
**every** entity its **own** attribute table listing **all** its attributes — never summarize, merge
attributes, or omit an entity.

Capturing real images: **only if the user opted in** (the "with screenshots" output choice or a
`--screenshots` flag). When opted in, follow the **`capture-doc-screenshots`** skill — it starts
the app if needed, drives `playwright-cli` to each capturable page, stores images under
`docs/generated/<scope>/img/`, and replaces the `🖼️` placeholders 1:1 with `![…](img/<Page>.png)`
references. It is **best-effort and never blocking**: if `playwright-cli` or the running app is
unavailable, the placeholders stay as-is and the reason is noted. **Confluence caveat:** the
Atlassian MCP cannot upload attachments, so on published pages screenshots must be **added
manually** (drag-drop) — the references/placeholders mark exactly where each one goes.

---

## Step 5 — Write local output

Write Markdown to `docs/generated/<scope>/...`. Suggested layout per scope:

```
docs/generated/<AppOrModule>/
  <lang>/
    <Code>_<DocName>.md      # FS, MG, ARCH, UG, TK
```

Update an index (`docs/generated/README.md`) with one row per generated doc set.

---

## Step 6 — Publish to Confluence (optional, via the Atlassian MCP)

Only if the user asks to publish. This uses the Atlassian (Rovo) MCP server. **Confirm the
target before any write** — publishing is outward-facing.

### 6a.0. Ensure the Atlassian (Rovo) MCP is connected (offer to connect)
Before anything else, check whether the Atlassian MCP tools are available (e.g. `atlassianUserInfo`
/ `getConfluenceSpaces` resolve, or `claude mcp list` shows `atlassian` as **Connected**). If they
are, continue to 6a.

If it is **not** connected, do not silently fall back — **ask** the user (AskUserQuestion) whether
to connect now:

- **Connect now (recommended)** — set it up per Atlassian's getting-started guide
  (`https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/`):
  1. Add the server (HTTP transport; the agent may run this):
     ```bash
     claude mcp add --transport http atlassian https://mcp.atlassian.com/v1/mcp/authv2
     ```
     Use `-s project` instead of the default local scope to share it via a committed `.mcp.json`.
  2. **Sign in — interactive, the agent cannot complete OAuth.** Tell the user to finish it
     themselves: either `/mcp` → **atlassian** → **Authenticate** (reload the session first so it
     sees the new server), or `claude mcp login atlassian` in an interactive terminal, then approve
     in the browser. **Never run the login from a non-interactive shell** — it fails with "stdin
     isn't a terminal".
  3. After they confirm sign-in, verify with `claude mcp list` (status **Connected**) and continue.
- **Skip / publish later** — write the docs to the repo only and tell the user they can publish any
  time with `/publish-confluence <scope>` once the MCP is connected. Do not block the rest of the run.

Only proceed past here once the MCP tools actually resolve.

### 6a. Resolve identity and site (read-only first)
1. `atlassianUserInfo` — confirm who is signed in.
2. `getAccessibleAtlassianResources` — get the **cloudId** (and confirm the right site if
   several are accessible).

### 6b. Resolve the target location (where to upload)
The full destination is a **path**:

```
Space  /  Folder  /  Folder  /  …  /  <Language>  /  <Doc>
└ spaceId   └─────── container path (0..N levels) ──────┘   └ per-lang child   └ FS/MG/ARCH/UG/TK
```

Inputs (from command args, or ask if missing — **never assume**):

- **Space** (`--space <KEY | name>`): resolve to a `spaceId`.
  - By key/title: `getConfluenceSpaces` with `keys` (global) — or for a personal space,
    `getConfluenceSpaces type=personal keys=["~<accountId>"]`. If ambiguous, list and ask.
- **Container path** (`--path "A/B/C"`): the ordered folder titles under the space, top→down.
  Any number of levels (0..N). If omitted, defaults to a single level = the app/module name.
  - Separator is `/`. If a folder title itself contains `/`, pass that segment quoted, or set
    `--path-sep "::"` and use that instead.
  - `--parent <pageId>` may pin the **starting** parent (an existing page id) the path hangs off;
    otherwise the path starts at the space top level.

> **"Folders" = parent pages.** This MCP creates pages/blogs only; a Confluence page acts as
> the folder/container. (Native Folder content type is not creatable here.)

### 6c. Walk the path — find-or-create each level
Resolve the destination by walking the path **segment by segment**, each as a direct child of
the previous. This is what makes `Space / Folder / Folder / Language / Docs` (any depth) work.

Maintain a running `parentId` (start = `--parent` if given, else none = space root). For **each
segment** in: `[ …container path… , <Language> , <Doc title> ]`:

1. **Search** for an existing page with that exact title that is a **direct child** of the
   running parent (use `parent`, not `ancestor`, so deeper namesakes don't match):
   ```
   space = "<KEY>" AND type = page AND title = "<Segment>" AND parent = <parentId>
   ```
   (at space root, omit `parent`) via `searchConfluenceUsingCql`. Fallback:
   `getConfluencePageDescendants <parentId> depth=1` and match the title.
2. **If found →** reuse its `id` (update body if it's a leaf doc and content changed).
3. **If not found →** `createConfluencePage` (spaceId + current `parentId`).
4. Set `parentId = <this page's id>` and continue to the next segment.

So a missing middle folder is created on the way down; an existing one is reused — duplicates
can't accumulate at any level. Capture every resolved id for the map (6f).

**`--on-existing`** controls leaf behavior when the doc pages already exist:
- `reuse` (default): update the existing pages in place.
- `new`: create a fresh container at the **last path segment**, date-suffixed (e.g.
  `<App> (YYYY-MM-DD)`), leaving the old set intact.
- `skip`: if the destination docs already exist, stop and report — don't write.

### 6d. Resulting hierarchy
```
<Space>
  └─ A/                         ← container path, found-or-created level by level
      └─ B/
          ├─ <Lang A>/          ← per-language child
          │    ├─ FS · MG · ARCH · UG · TK
          └─ <Lang B>/
               └─ …
```
Single language → omit the language level (docs go directly under the last folder) unless the
user wants the language folder kept for symmetry.

### 6e. Formatting rules for Confluence (learned, important)
Publish with **`contentFormat: "markdown"`**. Then:

- **Markdown pipe tables → render as native Confluence tables.** ✅ Use them for everything,
  including access matrices (with ✅ / –).
- **Raw HTML (`<table>`, `<mark>`, inline `style`) is ESCAPED to literal text.** ❌ Never
  embed HTML. This is why the matrices use markdown + ✅/– and highlights use 🟡/🔴.
- **`mermaid` fenced blocks → become a Confluence code macro** (the diagram **source** shows,
  not a rendered picture). Confluence has no native mermaid rendering. To get real diagrams,
  either (a) install a **Mermaid macro app** from the Marketplace so the code blocks render,
  or (b) embed an external render (e.g. kroki.io) — sends content to a third party and may be
  blocked by the instance. **Note:** this MCP server cannot upload file attachments, so PNGs
  cannot be auto-attached; that path needs a manual upload.
- Accented/non-English text and emoji render fine.

### 6f. Idempotency
Store a map of `doc → pageId` (plus the resolved `spaceId` and container `pageId`) in
`docs/generated/<scope>/.confluence-map.json`. On re-run, prefer the map, fall back to the
find-or-create search (6c), and **update** existing pages with `updateConfluencePage` (bump
version, include a versionMessage) instead of creating duplicates.

### 6g. Verify
After publishing, `getConfluencePage` (contentFormat markdown) on one page to confirm tables,
✅/– matrices and 🟡/🔴 cues rendered (ignore the cached `summary` field; check `body`).

---

## Quality checklist before finishing

- [ ] Project `.mpr` auto-detected, not hardcoded.
- [ ] Every technical claim traces to an mxcli/catalog result.
- [ ] No fabricated business content — gaps stated, not filled with guesses.
- [ ] All five doc types present per scope, structurally identical across languages.
- [ ] Version history table written from the model diff (`track-doc-versions`); no bump on an
      unchanged model; manifest saved and excluded from publish.
- [ ] Highlighting legend + 🟡/🔴 cues applied; access matrices use markdown + ✅/–.
- [ ] No machine-written tells, no tool/provenance mentions in the deliverable.
- [ ] Localized UI labels preserved verbatim and glossed.
- [ ] (If publishing) target **space + parent/folder** confirmed before any write;
      container resolved via **find-or-create** (no duplicates); hierarchy built; page-id
      map saved; one page verified.
