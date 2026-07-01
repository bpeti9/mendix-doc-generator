# Functional Specification (FS) — {{MODULE_NAME}} Module

This document is a black-box description of the application: it presents the implemented
functions without the technical implementation details. Configuration is covered in the
**Operations Guide (MG)**; the architecture in **Architecture (ARCH)**. Roll-out and routine
operational tasks are out of scope.

> **Highlighting key:** 🟡 = assumption / to be confirmed · 🔴 = needs changing / open issue.

## Version history

<!-- guidance: auto-maintained by the track-doc-versions skill from the model diff. Newest row last. Re-run the generator rather than hand-editing. -->

| Version | Date | Author | Description |
|---------|------|--------|-------------|
| 1.0 | {{DATE}} | {{AUTHOR}} | Initial release. |

## 1. Business goal and background

<!-- guidance: 1–2 paragraphs. What business problem does the module solve, for whom, and what is the high-level solution? Note any system it replaces and parallel-operation context. -->

{{BUSINESS_GOAL}}

**The business problem:** {{BUSINESS_PROBLEM}}

1. {{SOLUTION_STEP_1}}
2. {{SOLUTION_STEP_2}}
3. {{SOLUTION_STEP_3}}

The module is part of the `{{APP_NAME}}` Mendix application{{REPLACES_SYSTEM_NOTE}}.

## 2. Business process overview

The functional areas are reached from the **"{{MENU_GROUP}}"** navigation menu group (the menu items
and labels below are the actual on-screen texts):

| Menu item (UI label) | Internal/business name | Function |
|----------------------|------------------------|----------|
| {{UI_LABEL_1}} | {{BUSINESS_NAME_1}} | {{FUNCTION_1}} |
| {{UI_LABEL_2}} | {{BUSINESS_NAME_2}} | {{FUNCTION_2}} |
| ... | ... | ... |

## 3. Roles

The module has **{{ROLE_COUNT}}** module roles.

| Role | Access |
|------|--------|
| **{{ROLE_1}}** | {{ROLE_1_ACCESS}} |
| **{{ROLE_2}}** | {{ROLE_2_ACCESS}} |

**Field-level rights:** {{FIELD_LEVEL_RIGHTS_NOTE}}

## 4. Functions by screen

<!-- guidance: one subsection per page/screen. For each: purpose, filters, actions (with the backing microflow in code font), and a field/column table where the screen edits data. Mark editable vs read-only fields. -->

### 4.1 {{SCREEN_1_NAME}}

{{SCREEN_1_DESCRIPTION}}

| Column (UI label) | Field (type) | Editable |
|-------------------|--------------|----------|
| {{COL_1}} | {{FIELD_1}} | {{YES_NO_1}} |
| {{COL_2}} | {{FIELD_2}} | {{YES_NO_2}} |

> 🖼️ **[Screenshot: {{SCREEN_1_NAME}}]**

### 4.2 {{SCREEN_2_NAME}}

{{SCREEN_2_DESCRIPTION}}

> 🖼️ **[Screenshot: {{SCREEN_2_NAME}}]**

## 5. Data interfaces and file samples

### 5.1 Inbound data — {{INBOUND_SOURCE}} (import)

<!-- guidance: where inbound data comes from, via which connector/entities, and any filtering. Provide a field reference for the most-used interfaces. -->

{{INBOUND_DESCRIPTION}}

> 📄 **[Data sample: {{INBOUND_SAMPLE}}]**

### 5.2 Outbound data — {{OUTBOUND_NAME}} (export)

<!-- guidance: the module's main output(s). File/document naming, content, where the data is assembled from. -->

{{OUTBOUND_DESCRIPTION}}

> 📄 **[File sample: {{OUTBOUND_SAMPLE}}]**

## 6. Status handling

<!-- guidance: describe any status/state model (enumeration values) and the logic that transitions between them. Remove if the module has none. -->

{{STATUS_HANDLING}}

## 7. Notes, known deviations and open points

<!-- guidance: bullet the de-scoped, blocked, nice-to-have and open items. Mark each with 🟡 or 🔴. -->

- 🟡 **De-scoped:** {{DESCOPED_ITEM}}
- 🔴 **Blocked (to be clarified):** {{BLOCKED_ITEM}}
- 🟡 **Nice-to-have:** {{NICE_TO_HAVE_ITEM}}
- 🔴 **Open point:** {{OPEN_POINT}}

## 8. References

- **MG / ARCH / UG / TK — {{MODULE_NAME}}**.
