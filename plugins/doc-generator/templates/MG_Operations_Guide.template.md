# Operations Guide (MG) — {{MODULE_NAME}} Module

This document describes the configuration parameters and how to set them. The functional behavior is
covered in the **Functional Specification (FS)**; the architecture in **Architecture (ARCH)**.

> **Highlighting key:** 🟡 = assumption / to be confirmed · 🔴 = needs changing / open issue.

## Version history

<!-- guidance: auto-maintained by the track-doc-versions skill from the model diff. Newest row last. Re-run the generator rather than hand-editing. -->

| Version | Date | Author | Description |
|---------|------|--------|-------------|
| 1.0 | {{DATE}} | {{AUTHOR}} | Initial release. |

## 1. Goal and scope

The parameters, schedules and monitoring information needed to operate the {{MODULE_NAME}} module.
{{REPLACES_SYSTEM_NOTE}}

## 2. Configuration parameters overview

| Parameter | Where to set | Value |
|-----------|--------------|-------|
| `{{CONSTANT_NAME}}` (constant) | Mendix constant (per environment) | {{CONSTANT_VALUE}} |
| {{INTEGRATION_PARAM}} | {{INTEGRATION_LOCATION}} | see section 4 |
| Identity / sign-in | {{AUTH_MODULE}} | environment-dependent |
| Scheduled events | Studio Pro / Mendix Cloud Portal | see section 5 |

## 3. In-application constant(s)

<!-- guidance: list each module-owned constant, its type, default, and what it controls. -->

**`{{CONSTANT_NAME}}`** — {{CONSTANT_TYPE}}, default `{{CONSTANT_DEFAULT}}`. {{CONSTANT_DESCRIPTION}}
It can be overridden per environment (Configuration).

## 4. {{INTEGRATION_NAME}} (external data source)

<!-- guidance: remove this whole section if the module has no external integration. -->

| Setting | Value |
|---------|-------|
| Client / connection | {{INTEGRATION_CLIENT}} |
| Protocol / version | {{INTEGRATION_PROTOCOL}} |
| Endpoint (TEST) | {{INTEGRATION_ENDPOINT}} |
| Operations called | {{INTEGRATION_OPERATIONS}} |

- **Where to set:** {{INTEGRATION_CONFIG_NOTE}}
- **Critical dependency:** {{INTEGRATION_DEPENDENCY_NOTE}}

## 5. Scheduled events

The module has **{{SE_COUNT}}** scheduled events. **Their interval and enabled state are set in
Studio Pro / the Mendix Cloud Portal "Scheduled events" page** (not part of the model), so they must
be checked per environment.

| Scheduled event | Function | Frequency |
|-----------------|----------|-----------|
| `{{SE_1}}` | {{SE_1_FUNCTION}} | {{SE_1_FREQUENCY}} |
| `{{SE_2}}` | {{SE_2_FUNCTION}} | 🟡 {{SE_2_FREQUENCY_ASSUMED}} |
| `{{SE_3}}` | {{SE_3_FUNCTION}} | {{SE_3_FREQUENCY}} |

<!-- guidance: prefix with 🟡 any frequency that is assumed rather than confirmed in the model. -->

> ⚠️ **Data housekeeping:** {{HOUSEKEEPING_NOTE}}

> ⚠️ 🔴 **Open point:** {{OPEN_POINT}}

## 6. Logging and monitoring

- **Log node:** `{{LOG_NODE}}`.
- **Expected log messages (normal operation):**

| Message | Source microflow |
|---------|------------------|
| `{{LOG_MESSAGE_1}}` | `{{LOG_SOURCE_1}}` |
| `{{LOG_MESSAGE_2}}` | `{{LOG_SOURCE_2}}` |

- **What to watch:** {{MONITORING_NOTE}}

## 7. Permission management

- **Module roles:** `{{ROLE_1}}`, `{{ROLE_2}}`. {{ROLE_PLAN_NOTE}}
- Module roles must be assigned to **user roles**; users obtain access through their user role.
  {{USER_ROLE_MAPPING_NOTE}}

**Access summary:**

<!-- guidance: granted = ✅ ; not granted = – . Markdown table (no HTML — Confluence escapes it). -->

| Action | {{ROLE_1}} | {{ROLE_2}} |
|--------|:---:|:---:|
| {{ACTION_1}} | ✅ | – |
| {{ACTION_2}} | ✅ | ✅ |

## 8. Error handling and reprocessing

| Symptom | Probable cause | Action |
|---------|----------------|--------|
| {{SYMPTOM_1}} | {{CAUSE_1}} | {{ACTION_1}} |
| {{SYMPTOM_2}} | {{CAUSE_2}} | {{ACTION_2}} |

## 9. References

- **FS / ARCH / TK — {{MODULE_NAME}}**.
