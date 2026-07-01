---
name: track-doc-versions
description: Fingerprint the Mendix model and diff it against the saved manifest to maintain the Version history table in generated docs. Use whenever generating or regenerating documentation.
---

# Skill: track-doc-versions

Give every generated document a **version history** that is updated **automatically** from a
**model diff**: each run fingerprints the relevant model facts, compares them against the last
run's stored fingerprint, and — only when something actually changed — appends a new version
row describing the change. Used by `generate-handover-docs` on every run.

The goal: re-running the command on an unchanged model **does not** bump the version or add
noise; re-running after the app changed bumps the version and records *what* changed, with the
date and author.

---

## The version table (in every doc)

Place a **Version history** table near the top of each generated doc (right after the
highlighting key). Newest row last.

```
## Version history

| Version | Date | Author | Description |
|---------|------|--------|-------------|
| 1.0 | 2026-06-25 | <author> | Initial release. |
```

- **Author** = the git user (`git config user.name`) **only if already available**. Do not run
  git auth or prompt for it. If it isn't available, write the literal placeholder `🟡 [Author]`
  in the row for someone to fill in. Never invent or guess a name.
- **Date** = today (resolve the real current date; convert any relative date to absolute).

## The manifest (per scope, for diffing)

Store one manifest per scope at **`docs/generated/<scope>.manifest.json`** (scope = module name,
or the app name for app scope). It is the source of truth for the diff and the current version;
it is **not** a deliverable (don't publish it).

```json
{
  "scope": "<ModuleName>",
  "version": "1.1",
  "generated": "YYYY-MM-DD",
  "author": "<git user or 🟡 [Author]>",
  "fingerprint": {
    "entities":        ["EntityA|11|persistent", "EntityB|7|persistent"],
    "associations":    ["EntityB_EntityA|cascade"],
    "enumerations":    ["ENUM_StatusA|5", "ENUM_TypeB|4"],
    "microflows":      ["ACT_LoadA|2|8", "SUB_SyncA|3|16"],
    "pages":           ["EntityA_Overview|Overview title"],
    "moduleRoles":     ["Administrator", "RoleB"],
    "security":        ["EntityA:Administrator=CRWD;RoleB=R"],
    "constants":       ["ModuleLogNode|<value>"],
    "scheduledEvents": ["SE_LoadA", "SE_LoadB"]
  },
  "history": [
    {"version": "1.0", "date": "YYYY-MM-DD", "author": "<author>", "description": "Initial release."},
    {"version": "1.1", "date": "YYYY-MM-DD", "author": "<author>", "description": "Added entity EntityB; RoleB gained WRITE on EntityB."}
  ]
}
```

Each fingerprint entry is a stable `key|detail` string built from the same `mxcli`/catalog
extraction the docs use, **sorted** within each category so ordering never causes a false diff:

| Category | Entry format |
|----------|--------------|
| entities | `Name|attrCount|persistent\|non-persistent` |
| associations | `Name|deleteBehavior` |
| enumerations | `Name|valueCount` |
| microflows | `Name|complexity|activityCount` |
| pages | `Name|title` |
| moduleRoles | `Name` |
| security | `Entity:Role=RIGHTS;Role=RIGHTS` (roles sorted) |
| constants | `Name|defaultValue` |
| scheduledEvents | `Name` |

## Procedure (run on every generation)

1. **Load** `docs/generated/<scope>.manifest.json` if it exists.
2. **Build** the current fingerprint from this run's extraction.
3. **Diff** current vs. previous fingerprint, per category (added / removed / changed entries):
   - **No previous manifest** → version `1.0`, description `Initial release.`
   - **Identical fingerprint** → **no version bump, no new history row.** Regenerate the docs
     (content/templates may have improved) but keep the existing version table as-is. Tell the
     user "no model changes since v<X.Y>".
   - **Fingerprint differs** → **bump** (see rules) and add one history row whose **Description**
     summarizes the concrete diff, e.g.:
     > Added entities: A, B. Removed microflow: C. Page title fixed: D. Security: RoleB
     > gained WRITE on E. New scheduled event: F.
     Keep it factual and short — list the actual changed element names, grouped by kind.
4. **Write** the version table into every generated doc for the scope (all five FS/MG/ARCH/UG/TK,
   per language), using the full `history` list.
5. **Save** the updated manifest (new `version`, `generated`, `author`, `fingerprint`, and the
   appended `history` row).

## Version bump rules

Semantic-ish, kept simple:

- **Major** (`X.0`): a **removal** or breaking change — entity/association/attribute/microflow/page
  removed, or access rights revoked. These can break integrations or links.
- **Minor** (`X.Y+1`): additions or non-breaking modifications — new elements, new attributes,
  added access, title/text fixes, complexity changes.
- **No bump:** identical fingerprint (see above).

When both additions and removals occur, the removal wins → major bump.

## Notes

- The diff is **model-only**. It does not track business-narrative edits in `docs/input/` — those
  are the author's prose. (Optionally mention in the description if a sidecar was newly found.)
- If git is available, you may enrich the description with the `.mpr` commit range since the last
  `generated` date, but the **fingerprint diff is authoritative** — never invent changes that the
  fingerprint doesn't support.
- One manifest per scope covers all of a module's docs (the five types across every language), so
  versions stay in lockstep.

## Quality checklist

- [ ] Version table present and newest-row-last in every generated doc.
- [ ] Author from git if already available, else `🟡 [Author]` placeholder — never invented or prompted; date is the real current date.
- [ ] Manifest read before, written after; stored at `docs/generated/<scope>.manifest.json`.
- [ ] Identical model → no bump, no new row (no version noise on re-run).
- [ ] Changed model → correct major/minor bump and a description listing the actual changed elements.
- [ ] Manifest excluded from any Confluence publish (it is not a deliverable).
