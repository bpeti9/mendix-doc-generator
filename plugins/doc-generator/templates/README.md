# Module documentation templates

Reusable, project-agnostic templates for documenting a Mendix module. They were
distilled from a real module hand-over set, with all project-specific content
removed and replaced by placeholders.

## The five document types

| Code | Template file | Purpose | Audience |
|------|---------------|---------|----------|
| **FS** | `FS_Functional_Specification.template.md` | Black-box functional spec — what the module does, by screen, plus data interfaces | Business + technical |
| **MG** | `MG_Operations_Guide.template.md` | Configuration parameters, scheduled events, logging, error handling | Operations |
| **ARCH** | `ARCH_Architecture.template.md` | Building blocks, domain model, integrations, diagram | Technical |
| **UG** | `UG_User_Guide.template.md` | Step-by-step screen walkthrough | End users |
| **TK** | `TK_Developer_Support_Documentation.template.md` | Developer + support hybrid (glossary, install, functions w/ permission matrices, data types, support runbook) | Developers + support |

## How to use

1. Copy the template(s) you need into your output folder and rename them for the
   module (e.g. `MyModule_FS_Functional_Specification.md`).
2. Replace every `{{PLACEHOLDER}}` with real, model-verified content.
3. Remove any optional section that does not apply, and add sections where useful.
4. Delete the `<!-- guidance: ... -->` comments before publishing.

## Conventions baked into the templates

These match the `generate-handover-docs` engine skill. **Use markdown,
never raw HTML** — Confluence escapes `<table>`/`<mark>`/inline `style` to literal text.

- **Highlighting legend** (keep it at the top of every doc):
  - 🟡 = assumption / to be confirmed
  - 🔴 = needs changing / open issue
- **Access matrices** are markdown pipe tables (markdown cannot colour cells, so use icons):
  - granted: `✅`
  - not granted: `–`

  ```
  | Function | RoleA | RoleB |
  |----------|:---:|:---:|
  | List | ✅ | ✅ |
  | Delete | ✅ | – |
  ```
- **Diagrams** use fenced ```mermaid``` blocks.
- **Screenshots / file samples** are marked placeholders: `🖼️ [Screenshot: ...]`, `📄 [File sample: ...]`.

> **Rendering note:** markdown pipe tables, the ✅/– icons and the 🟡/🔴 cues render
> consistently in VSCode preview, GitHub, Confluence (with `contentFormat: "markdown"`) and
> Word. This is why the templates avoid HTML tables and `<mark>` entirely.

## Authoring rules

- State only facts you can verify from the model and supplied source material — do
  not invent or assume; flag anything uncertain with the yellow/red marks.
- Keep the language plain and human; nothing should read as machine-generated.
- Preserve original (e.g. localized) UI labels verbatim and gloss them where helpful.
