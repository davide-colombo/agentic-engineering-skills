---
name: large-output-root-hygiene
description: Classify and safely manage large output roots that mix final outputs, stale backups, failed runs, partial outputs, scratch data, and generated deliverables. Use when an output root must be inventoried, partitioned, quarantined, or reorganized without losing valid results, breaking downstream references, deleting evidence, or violating no-deletion-by-default policy.
---

# Large Output Root Hygiene

## Purpose

Determine the actual contents of a large output root, classify every top-level item by current status (final, partial, failed, stale backup, scratch, or unknown), and recommend a safe move-or-leave decision per item. Detect active writers before any non-read action, preserve downstream references, and never delete without explicit authorization.

## When to use

Use when an output root has grown beyond informal management, when free space or filesystem capacity is being negotiated, when a project needs to separate final outputs from failed and stale runs, when a deliverable is being assembled from a noisy root, or when the receiver of an inherited output area must understand what is safe to touch.

## When not to use

Do not use as authorization to delete output. This skill always defaults to no deletion. Do not use it to evaluate the scientific correctness of outputs; defer to [`scientific-data-integrity-audit`](../scientific-data-integrity-audit/SKILL.md). Do not use it to audit a manifest covering a transferred artifact set; defer to [`manifest-checksum-and-provenance`](../manifest-checksum-and-provenance/SKILL.md). Do not use it as a substitute for repository-state, configuration, or domain validation.

## Required inputs

Obtain from the current prompt and authoritative project material:

- Task objective, selected task mode, and allowed scope.
- The output root path and the policy that governs it.
- The naming and classification conventions the project uses, when documented.
- Permission boundaries: which actions are permitted (inventory, classification, move, quarantine, delete) and which are forbidden.
- Identity of active writers, schedulers, or operators that may be using the root concurrently.

If the output root, the governing policy, or the permission boundary cannot be established, stop and report. Do not infer policy from filesystem conventions.

## Optional inputs

Use when supplied or discoverable within scope:

- Run logs, sentinels, or job records that indicate which top-level items belong to which run.
- Downstream references (configuration files, scripts, dashboards) that point into the output root.
- Prior inventory or quarantine records.
- Storage quota, retention policy, or backup policy applicable to the root.

Treat absent evidence as uncertainty, not as permission to move or delete.

## Task modes

Choose exactly one mode and state it in the report:

- `OUTPUT_ROOT_INVENTORY`: Read-only enumeration and classification, without any non-read action.
- `OUTPUT_ROOT_CLASSIFICATION_AUDIT`: Inspect a prior classification against current on-disk state.
- `QUARANTINE_PLAN`: Propose a quarantine layout that preserves names, structure, and downstream references, without applying it.
- `QUARANTINE_EXECUTION`: Apply an authorized quarantine plan with auditable move records and explicit authorization quoted in the prompt.
- `DELETION_PROPOSAL`: Identify items that the operator may consider deleting, with evidence per item, without performing any deletion.

A mode changes audit emphasis and permission, but never grants deletion. Deletion requires separate explicit authorization per item or per category quoted in the current prompt.

## Output root identity

Define the root precisely:

- Absolute path or unambiguous identifier of the output root.
- Filesystem type and any quota, snapshot, or backup behavior relevant to safety.
- Whether the root is shared with other projects, users, or services.
- The boundary between this skill's scope and surrounding directories that must not be touched.

If the root is shared and other consumers cannot be enumerated, default to read-only mode.

## Top-level item categories

Classify every top-level directory or file under the root into exactly one category:

- `final active output`: An output that is current, complete, referenced by downstream consumers, and inside the project's published-output contract.
- `final but inactive output`: An output that is complete and was once active but is no longer referenced; retention policy decides whether it remains.
- `stale backup`: A copy made at an earlier point, identifiable by naming, timestamp, or sidecar; not the current output.
- `failed run`: An output set whose sentinel is absent, whose log shows failure, or whose outputs are missing or partial in a way that matches the project's failure-state contract.
- `partial active output`: A run that is in progress at audit time or whose outputs are present but whose sentinel has not yet been written.
- `scratch or intermediate`: Working data not part of the published output contract.
- `non-final deliverable copy`: A copy assembled for review or handoff; not the canonical output.
- `unknown`: An item that does not match any defined category. Treat every unknown as a stop trigger; do not guess.

Record the classification, the evidence used, and the confidence per item.

## Active writer and process checks

Before any non-read action, confirm there is no active writer for any item in scope:

- Inspect process tables, job records, and schedulers for processes operating on the root.
- Inspect file locks, in-progress sentinels, and recent modification times for items considered for move.
- Inspect for `.tmp`, `.part`, `.inprogress`, or other in-progress naming patterns that indicate active writes.
- Confirm that no parallel run is producing outputs into the same item under audit.

If any item shows evidence of an active writer, exclude it from non-read action and report it explicitly. Do not race a writer.

## Downstream reference checks

For every item considered for move or quarantine:

- Search configuration, scripts, dashboards, and downstream consumers for references to the item's path or identity.
- Record references found and assess the impact of moving the item.
- Confirm the project's policy for updating references after a move.
- When references cannot be enumerated, default to leaving the item in place and reporting the risk.

A move that breaks downstream references is a regression, not housekeeping.

## Naming conventions

Document and apply naming conventions the project actually uses:

- The naming rule for final outputs, failed runs, scratch directories, and quarantined items.
- Date formats, run identifiers, and any prefix or suffix that classifies an item at a glance.
- Whether the convention permits embedded spaces, non-ASCII characters, or symbols that affect tooling.

Do not invent a new convention to make classification easier. Use the project's actual convention and report ambiguous items.

## Quarantine strategy

When a quarantine plan is permitted by mode and authorization:

- Define a quarantine root inside the same filesystem when atomic rename is required, or a clearly separated root when policy demands it.
- Preserve top-level item names and internal structure under quarantine. Do not flatten or rename without authorization.
- Record the source path, destination path, classification, evidence, and time of move per item.
- Provide a reversible audit trail so quarantined items can be returned to the original root if classification was wrong.

A quarantine that loses item identity is not quarantine; it is deletion.

## Move versus delete policy

This skill defaults to no deletion. Even in `DELETION_PROPOSAL` mode, no deletion occurs.

- Move is the default safe action for stale backups, failed runs, scratch data, and inactive outputs when explicitly authorized.
- Delete requires separate explicit authorization per item or category, quoted in the current prompt, and even then is performed under [`remote-execution-safety`](../remote-execution-safety/SKILL.md) for remote roots or under equivalent local discipline.
- Items classified as unknown, final active, or partial active are never deleted.
- Items with active writers are never touched.

If the prompt requests deletion broadly without per-item or per-category authorization, stop and report.

## No destructive action without explicit authorization

Confirm before any move:

- The current prompt explicitly authorizes the action category.
- The classification and evidence per item are recorded.
- The destination preserves names and structure.
- The action is reversible by inspection of the audit trail.

If any of these conditions cannot be met for an item, leave the item in place and report.

## Preservation of names and structure when moving

When items are moved into quarantine or another root:

- Preserve the original top-level name.
- Preserve internal directory structure.
- Preserve file permissions and timestamps when policy requires it.
- Do not rename, flatten, deduplicate, or merge contents.
- Do not silently change file metadata.

A move that mutates contents is a transformation, not a move. Mutating transformations require their own authorization and audit trail.

## Audit trail for moved or quarantined items

For every non-read action:

- Record source path, destination path, classification, evidence, time, operator, and tool used.
- Store the audit trail outside the moved items so it survives a later reorganization.
- Make the audit trail inspectable by any future operator who must reverse or extend the action.

An action without an audit trail is an action that cannot be safely reviewed. Do not perform it.

## Audit procedure

1. Restate the objective, selected task mode, scope, output root, and permission boundary.
2. Enumerate the top-level items under the root using read-only listing.
3. Classify every item into exactly one category. Record evidence and confidence per item. Treat unknowns as stop triggers.
4. Inspect process tables, job records, schedulers, and in-progress naming patterns for active writers.
5. Search for downstream references to each item.
6. When `QUARANTINE_PLAN` is the selected mode, produce a per-item plan with source path, destination path, classification, and evidence; do not apply it.
7. When `QUARANTINE_EXECUTION` is the selected mode and explicit per-item or per-category authorization is present, execute the plan with audit trail, preserving names and structure.
8. When `DELETION_PROPOSAL` is the selected mode, list items the operator may consider deleting, with evidence per item; do not delete.
9. Classify findings, record commands actually run and evidence unavailable, and select exactly one verdict.

Do not treat free-space pressure as authorization to broaden actions.

## Stop-and-report triggers

Stop before any move, quarantine, or deletion when:

- The output root, governing policy, or permission boundary is ambiguous.
- Any item in scope is classified as unknown.
- Any item shows evidence of an active writer.
- Downstream references to an item cannot be enumerated.
- The naming convention does not allow reliable classification.
- The proposed quarantine destination cannot preserve names or structure.
- The prompt does not include explicit authorization for the requested action category.
- The audit trail cannot be inspected, preserved, or reversed.
- Required evidence cannot be inspected and the gap prevents a reliable verdict.

Report the trigger, affected items, evidence, and minimum decision or authorization required.

## Output contract

Produce these sections:

1. `VERDICT`: exactly one verdict from the vocabulary below and a one-sentence rationale.
2. `MODE AND SCOPE`: selected task mode, output root identity, allowed actions, and exclusions.
3. `ROOT INVENTORY`: enumeration of top-level items with classification, evidence, and confidence.
4. `ACTIVE WRITER CHECKS`: process, sentinel, and naming evidence per item.
5. `DOWNSTREAM REFERENCES`: references discovered per item and impact of moving.
6. `NAMING CONVENTION FINDINGS`: items whose names follow or violate the project's convention.
7. `MOVE OR QUARANTINE PLAN OR ACTIONS`: per-item plan or per-item action with source path, destination path, classification, and evidence; write `none` if no plan or action applies.
8. `DELETION PROPOSAL`: items the operator may consider deleting with evidence per item, when the mode is `DELETION_PROPOSAL`; otherwise write `none`.
9. `AUDIT TRAIL`: where the trail for any executed action is stored and how to inspect it; write `none` when no action was executed.
10. `VALIDATION EVIDENCE`: commands actually run, exit statuses, concise results, checks not run, and impact.
11. `FINDINGS`: blocking findings and non-blocking warnings with location, evidence, consequence, and minimum resolution; write `none` for empty categories.
12. `NEXT STEP`: the minimum classification correction, plan revision, authorization, or operator decision supported by the verdict.

Do not claim a move or deletion occurred unless an audit-trail record was written and can be inspected.

## Allowed actions

- Read top-level item listings, sentinels, logs, configuration, and downstream-reference sources.
- Inspect process tables, job records, and schedulers for active-writer evidence.
- Compute classification and confidence per item.
- Propose move-or-quarantine plans without applying them.
- Apply an authorized quarantine plan only when the prompt explicitly authorizes the action and an audit trail is written.

## Forbidden actions

- Delete any item by default; deletion requires separate explicit authorization quoted in the current prompt.
- Touch any item with evidence of an active writer.
- Rename, flatten, deduplicate, or mutate contents during a move.
- Move items whose downstream references cannot be enumerated.
- Classify an unknown item by guessing in order to proceed.
- Treat free-space pressure as authorization.
- Expose private paths or restricted identifiers in shared reports or commands.

## Verdict vocabulary

- `OUTPUT_ROOT_READY`: Inventory, classification, active-writer checks, downstream references, and any executed actions satisfy the selected mode with no remaining warnings.
- `OUTPUT_ROOT_READY_WITH_WARNINGS`: No blocking finding remains, but substantiated non-blocking limitations or residual risks are explicitly reported.
- `NEEDS_REVISION`: One or more correctable blocking inventory, classification, reference, or plan findings prevent acceptance.
- `OUTPUT_ROOT_UNSAFE`: Active writers, broken references, unknown items, or missing authorization make the requested action unsafe.
- `BLOCKED`: Missing inputs, inaccessible evidence, unsafe inspection conditions, or unavailable essential validation prevent a reliable conclusion.
- `OUT_OF_SCOPE`: The requested audit, plan, or action exceeds authorized scope.

When several verdicts apply, use `OUT_OF_SCOPE` for unauthorized scope, `BLOCKED` when the audit itself cannot proceed safely, `OUTPUT_ROOT_UNSAFE` for demonstrated unsafe conditions, and `NEEDS_REVISION` for correctable blocking findings. Use a ready verdict only when the selected mode's conditions are fully met by inspected evidence.
