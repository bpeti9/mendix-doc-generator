---
name: capture-doc-screenshots
description: Capture real screenshots for generated Mendix docs with Playwright and wire them in, replacing the picture placeholders. Best-effort and never blocking; use only when the user opts into screenshots.
---

# Skill: capture-doc-screenshots

Optionally **capture real screenshots** for generated documentation and wire them into the
docs, replacing the `🖼️ [Screenshot: …]` placeholders. Used by `generate-handover-docs`
**only when the user opts in** (e.g. the "with screenshots" output choice, or a
`--screenshots` flag).

The guiding rule: **best-effort, never blocking.** If the app can't be started or
`playwright-cli` can't run, leave the placeholders exactly as they are and note why — do not
fail the documentation run.

---

## When to run

Only when screenshot capture was explicitly requested. If not requested, skip this skill
entirely and keep the `🖼️`/`📄` placeholders.

## Step 1 — Preflight (decide: capture or fall back)

Run these checks in order; on the first failure that can't be auto-resolved, **fall back to
placeholders** and record a one-line reason in the run summary.

```bash
# 1. Is the browser driver available?
command -v playwright-cli || echo "NO_PLAYWRIGHT"

# 2. Is the app already up?
curl -fs -o /dev/null http://localhost:8080 && echo "APP_UP" || echo "APP_DOWN"
```

- **No `playwright-cli`** → fall back to placeholders (note: "browser driver not installed").
- **App down** → try to start it (heavy; can take minutes). Detect the project file first:
  ```bash
  MPR=$(ls *.mpr 2>/dev/null | head -1)
  mxcli docker run -p "$MPR" --wait    # builds + starts; waits for "Runtime successfully started"
  ```
  If Docker is unavailable or the build fails → fall back to placeholders (note the reason).

> Confirm with the user before starting the app if it isn't already running — building and
> launching is a heavy, multi-minute operation. If they decline, fall back to placeholders.

## Step 2 — Open a session and sign in

```bash
playwright-cli open http://localhost:8080
playwright-cli snapshot                  # inspect the landing/login page structure
```

If a login form is shown, sign in with the project's configured credentials (demo user, or
admin). Resolve credentials from `SHOW DEMO USERS` / project settings — **do not hardcode or
guess passwords**; if none are available, fall back to placeholders for any page behind login.

```bash
playwright-cli fill <userRef> '<user>'
playwright-cli fill <passRef> '<password>'
playwright-cli click <loginButtonRef>
```

## Step 3 — Decide which pages are capturable

From the `SHOW PAGES IN <Module>` inventory, classify each page:

| Page kind | How to reach it | Capturable? |
|-----------|-----------------|-------------|
| Has a **URL** (the `url` column is set) | `http://localhost:8080/p/<url>` | ✅ directly |
| **Overview / no-param** page on the menu | navigate via the menu (snapshot → click) | ✅ if reachable |
| **Detail/edit** page needing a context object (`Params ≥ 1`) | open the overview, click a row | ⚠️ only if data exists; else placeholder |
| Page requiring data that isn't present | — | ❌ placeholder (note "no sample data") |

Capture what you can; leave placeholders (with a short reason) for the rest. Partial coverage
is fine and expected.

## Step 4 — Capture each page

For a URL-addressable page:

```bash
playwright-cli navigate "http://localhost:8080/p/<url>"
# optional: wait for a known widget to confirm the page rendered
playwright-cli run-code "document.querySelector('.mx-name-<knownWidget>') !== null"
playwright-cli screenshot --filename "docs/generated/<scope>/img/<Page>.png" --full-page
```

For a menu/row-navigated page: use `snapshot` to get element refs, `click` to reach the page,
then `screenshot` as above. Name each file after the page (`<Page>.png`) so it maps 1:1 to its
placeholder.

Store all images under **`docs/generated/<scope>/img/`** (create the folder). For artifact
samples (generated PDFs, exports) referenced by `📄` placeholders, capture or copy the file
into the same `img/` folder when feasible.

## Step 5 — Wire images into the docs

For every captured page, replace its placeholder line with a relative image reference:

- Placeholder: `> 🖼️ **[Screenshot: <PageName>]**`
- Becomes: `![<PageName>](img/<PageName>.png)`

(Use the path that resolves from the doc's own location — typically `img/<Page>.png` relative to
the language folder.) Leave untouched any placeholder whose page could not be captured, and keep
its reason in the run summary.

## Step 6 — Close and report

```bash
playwright-cli close
```

Report: how many pages were captured vs. left as placeholders, and the reason for each gap.
Leave the app running or stop it (`mxcli docker down -p "$MPR"`) per the user's preference.

---

## Confluence caveat (important)

The Atlassian MCP **cannot upload file attachments**, so even when local docs reference real
`img/<Page>.png` files, published Confluence pages will **not** show them automatically — the
images must be added manually (drag-drop) on the Confluence page. The image references and the
remaining `🖼️` placeholders mark exactly where each one goes.

## Quality checklist

- [ ] Capture attempted only because the user opted in.
- [ ] Preflight failures fell back to placeholders with a recorded reason — the doc run never blocked.
- [ ] No hardcoded/guessed credentials; pages behind an unresolved login stayed as placeholders.
- [ ] Captured images live under `docs/generated/<scope>/img/`, named per page.
- [ ] Placeholders replaced 1:1 only for pages actually captured.
- [ ] Run summary states captured-vs-placeholder counts and the Confluence manual-upload caveat.
