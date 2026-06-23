---
name: excel-workbook-integrity
description: Audit Excel workbook updates used for scientific review, summaries, manual curation, or reporting, with strict preservation of the original workbook, explicit new-workbook path, sheet inventory, column contracts, formula and style contracts, data validation, manual-curation flag handling, and export consistency for workbooks derived from TSV or CSV. Use before any workbook edit, after assembly, or before the workbook is shared.
---

# Excel Workbook Integrity

## Purpose

Determine whether an Excel workbook update preserves the original workbook, writes to an explicit new path, contains the intended sheet inventory, honors per-column contracts, preserves required formulas, styles, filters, and data validation, supports manual-curation flag columns, treats empty cells in a documented way, and remains consistent with any TSV or CSV source from which it is derived.

## When to use

Use before producing a new Excel workbook from a TSV or CSV input, before updating an existing workbook used for review or curation, after a workbook assembly to inspect the result, or before sharing a workbook with collaborators. Use alongside [`output-contract-and-table-schema-audit`](../output-contract-and-table-schema-audit/SKILL.md) when the workbook's sheets are governed by a tabular contract, alongside [`manual-curation-artifact-packaging`](../manual-curation-artifact-packaging/SKILL.md) when the workbook is part of a review deliverable, and alongside [`manifest-checksum-and-provenance`](../manifest-checksum-and-provenance/SKILL.md) when a manifest accompanies the workbook.

## When not to use

Do not use as authorization to share, transmit, or publish a workbook. Do not substitute it for repository-state, code-review, configuration, or domain validation. Do not use it to evaluate the scientific correctness of the contents; defer to [`scientific-data-integrity-audit`](../scientific-data-integrity-audit/SKILL.md).

## Required inputs

Obtain from the current prompt and authoritative project material:

- Task objective, selected task mode, and allowed scope.
- The workbook under audit, the source it is derived from (if any), and the intended audience.
- The preservation policy for the original workbook.
- Permission boundaries: whether the original may be overwritten and whether new sheets may be added.

If the workbook, source, audience, or preservation policy cannot be established, stop and report.

## Optional inputs

Use when supplied or discoverable within scope:

- Prior workbook versions for comparison.
- Sheet-level expectations documented in the project's curation procedure.
- Reviewer-side tool constraints (Excel version, Google Sheets compatibility, LibreOffice compatibility).
- Existing summary, audit, or change-tracking sheets.

Treat absent evidence as uncertainty, not as proof of workbook correctness.

## Task modes

Choose exactly one mode and state it in the report:

- `WORKBOOK_DESIGN_REVIEW`: Evaluate a proposed workbook layout before assembly.
- `WORKBOOK_UPDATE_PLAN`: Produce an inspectable plan for updating a workbook without performing the write.
- `WORKBOOK_AUDIT`: Inspect an assembled or updated workbook against the contract.
- `EXPORT_CONSISTENCY_AUDIT`: Compare a workbook with its TSV or CSV source for parity.
- `MANUAL_CURATION_AUDIT`: Inspect manual-curation flag columns and operator-edit hygiene.

A mode changes audit emphasis; it does not authorize overwriting the original workbook or sharing the result.

## Workbook path and preservation policy

State explicitly:

- The path to the original workbook.
- The path to the new workbook produced by the update.
- Whether the original may be overwritten and, if so, under what authorization quoted in the current prompt.
- The retention policy for prior versions.

The default is that the original workbook is preserved at its original path. Any deviation requires explicit authorization.

## Original workbook not overwritten unless explicitly authorized

Confirm before any write:

- The current prompt explicitly authorizes overwriting the original, if that is the intent.
- When no authorization is present, the operation produces a new file at a distinct path.
- The new file is written atomically: the consumer sees the complete file or no file.
- A failed write does not corrupt the original.

A workbook update that silently overwrites the original is a destructive action. Stop and report.

## New workbook path

For the new workbook produced by the update:

- Confirm the path follows the project's deliverable-naming convention.
- Confirm the path does not collide with another current workbook unless intentional.
- Confirm the path does not encode private machine paths, host names, or environment-specific strings.
- Cross-reference [`manual-curation-artifact-packaging`](../manual-curation-artifact-packaging/SKILL.md) when the workbook is part of a deliverable.

## Sheet inventory

Document and verify:

- The list of sheets the workbook is supposed to contain.
- Each sheet's name, role, and intended audience.
- Whether sheet order is contractual.
- Whether hidden or very-hidden sheets are permitted.
- Whether protected sheets are required.

A workbook whose sheet inventory is implicit cannot be safely updated or audited.

## Expected sheets

For each expected sheet:

- Confirm presence under the contractual name (case-sensitive).
- Confirm the sheet is visible if visibility is contractual.
- Confirm the sheet's protection status follows the contract.
- Detect duplicate sheets, hidden sheets that should be visible, or visible sheets that should be hidden.

## Row counts

For each data sheet:

- Confirm the row count matches the source TSV or CSV when applicable.
- Confirm the row count matches the intended record count when independently enumerated.
- Detect trailing empty rows, hidden filtered rows, and rows whose visibility differs from the contract.

## Column contracts

For each sheet's columns:

- Document the expected column names, column order (when contractual), and per-column types.
- Detect missing, extra, renamed, or reordered columns.
- Confirm types are honored (numeric where contractual, text where contractual, dates with consistent format).
- Cross-reference [`output-contract-and-table-schema-audit`](../output-contract-and-table-schema-audit/SKILL.md) for full tabular-schema audit.

## Formulas if relevant

When the workbook contains formulas:

- Document the formulas the contract requires.
- Confirm formulas are present, syntactically valid, and reference the intended cells, sheets, or named ranges.
- Detect broken references, `#REF!`, `#NAME?`, `#VALUE!`, `#DIV/0!`, or other formula errors.
- Confirm computed cells are not replaced by stale literal values from a prior recalculation.

## Styles if relevant

When the workbook contract includes styles:

- Document required font, color, conditional-formatting, and number-format expectations.
- Confirm styles are applied where required and not applied where the contract forbids.
- Detect styles that visually communicate information the contract does not declare (for example, color-coded review state that is not documented).

## Filters and frozen panes if relevant

When the workbook contract specifies filters or frozen panes:

- Confirm filter rows are present on the contractual columns.
- Confirm frozen-pane positions match the contract.
- Detect autofilters that hide rows the consumer expects to see.
- Detect frozen-pane settings that conflict with the contract.

## Data validation and dropdowns if relevant

When the workbook contract includes data validation:

- Document the validated columns, the validation rules, and the dropdown lists when applicable.
- Confirm validation rules match the contract.
- Confirm dropdown lists reference the authoritative source list.
- Detect cells that violate the validation rule due to manual edit, paste, or import behavior.

## Representative or manual-curation flags

When the workbook contains review flags:

- Document the flag column, the controlled vocabulary it uses, and the consumer's interpretation.
- Confirm flag values fall within the vocabulary.
- Confirm representative selections or curation decisions follow a documented rule.
- Detect flags that were retained from a prior version when the underlying record changed.

Cross-reference [`classification-and-grouping-audit`](../classification-and-grouping-audit/SKILL.md) when flag columns interact with grouping or classification decisions.

## No unintended sheet edits

For workbook updates that should only touch named sheets:

- Confirm sheets outside the intended scope are byte-for-byte equivalent to the prior version, or that any differences are documented and authorized.
- Detect incidental edits introduced by the writing tool (default formatting, locale-specific number formats, recalculated cached values).
- Detect changes to defined names, sheet order, or workbook-level metadata that the contract does not authorize.

## Empty and missing cell semantics

For each data sheet:

- Document the meaning of an empty cell, including whether it represents "not measured", "intentionally blank", or "value is zero".
- Confirm the workbook respects this contract per column.
- Confirm consumers parse empty cells consistently with the contract.

Inconsistent empty-cell meaning is a frequent silent-corruption source.

## Export consistency if workbook is derived from TSV or CSV

When the workbook is derived from a TSV or CSV source:

- Confirm row counts agree between the source and the workbook (excluding header).
- Confirm column counts and column names agree.
- Confirm encoding differences do not corrupt non-ASCII text.
- Confirm date and number formatting differences do not change meaning.
- Confirm leading zeros, scientific notation, and locale conventions do not silently transform values.

A workbook that silently transforms TSV values is not consistent with its source. Record this and report it.

## Audit summary of changed sheets

When the audit reports a workbook update:

- Enumerate every sheet that was added, removed, or modified.
- For each modified sheet, record the cell or column-level change summary.
- Confirm the change summary is consistent with the intended update scope.

A workbook update without a change summary cannot be reviewed.

## Audit procedure

1. Restate the objective, selected task mode, scope, original workbook path, and new workbook path.
2. Inspect preservation policy and confirm the original is not overwritten without authorization.
3. Inspect sheet inventory against the contract.
4. Inspect row counts, column contracts, formulas, styles, filters, frozen panes, and data validation per sheet.
5. Inspect manual-curation flag columns against the controlled vocabulary.
6. Inspect for unintended sheet edits and unauthorized workbook-level changes.
7. Inspect empty-cell semantics per column.
8. Compare against TSV or CSV source for export consistency, when applicable.
9. Produce an audit summary of changed sheets.
10. Classify findings, record commands actually run and evidence unavailable, and select exactly one verdict.

Do not treat a workbook that opens without error as proof of contract compliance.

## Stop-and-report triggers

Stop before sharing or finalizing the workbook when:

- Preservation policy is ambiguous or the original has been or would be overwritten without authorization.
- Sheet inventory disagrees with the contract.
- Row counts or column contracts disagree with the source or the intended record count.
- Required formulas are missing or yield error values.
- Required styles, filters, frozen panes, or data validation are absent or incorrect.
- Curation flags fall outside the controlled vocabulary or were retained on stale records.
- Sheets outside the update scope were modified.
- Empty-cell semantics are inconsistent with the contract.
- Export from TSV or CSV silently transformed values.
- Required evidence cannot be inspected and the gap prevents a reliable verdict.

Report the trigger, affected sheet or cell range, evidence, and minimum decision or authorization required.

## Output contract

Produce these sections:

1. `VERDICT`: exactly one verdict from the vocabulary below and a one-sentence rationale.
2. `MODE AND SCOPE`: selected task mode, original and new workbook paths, allowed scope, and exclusions.
3. `PRESERVATION POLICY`: original workbook path, new workbook path, overwrite authorization, and atomic-write evidence.
4. `SHEET INVENTORY`: expected sheets, observed sheets, visibility, protection, and ordering findings.
5. `PER-SHEET CONTRACT`: row counts, column contracts, formulas, styles, filters, frozen panes, and data validation per sheet.
6. `CURATION FLAGS`: flag columns, controlled vocabulary, and operator-edit hygiene; write `none` when not applicable.
7. `UNINTENDED EDITS`: sheets or workbook-level elements outside the update scope and their byte- or content-level status.
8. `EMPTY CELL SEMANTICS`: per-column meaning and observed behavior.
9. `EXPORT CONSISTENCY`: comparison with TSV or CSV source when applicable; write `none` when not derived from such a source.
10. `CHANGE SUMMARY`: added, removed, and modified sheets with cell- or column-level descriptions.
11. `VALIDATION EVIDENCE`: commands actually run, exit statuses, concise results, checks not run, and impact.
12. `FINDINGS`: blocking findings and non-blocking warnings with location, evidence, consequence, and minimum resolution; write `none` for empty categories.
13. `NEXT STEP`: the minimum correction, reassembly, redaction, or authorization supported by the verdict.

## Allowed actions

- Read the original and new workbook, accompanying source files, and contract documents within scope.
- Run local read-only inspection commands (sheet listing, cell extraction, formula listing, validation rule extraction) when explicitly safe and authorized.
- Propose layout, formula, style, validation, or vocabulary corrections without applying them unless separately authorized.

## Forbidden actions

- Overwrite the original workbook without explicit authorization quoted in the current prompt.
- Treat a workbook that opens without error as proof of contract compliance.
- Assume default cell format, locale, or encoding from convention without inspection.
- Modify sheets outside the intended update scope.
- Include private machine paths, host names, or environment-specific strings in sheet names or cell contents unless audit-material policy explicitly requires retention.
- Share the workbook without separate explicit authorization.

## Verdict vocabulary

- `WORKBOOK_INTEGRITY_READY`: Preservation policy, sheet inventory, per-sheet contract, curation flags, unintended-edit checks, empty-cell semantics, export consistency, and change summary satisfy the selected mode with no remaining warnings.
- `WORKBOOK_INTEGRITY_READY_WITH_WARNINGS`: No blocking finding remains, but substantiated non-blocking limitations or residual risks are explicitly reported.
- `NEEDS_REVISION`: One or more correctable blocking sheet, column, formula, validation, or export findings prevent acceptance.
- `WORKBOOK_UNSAFE`: Original-workbook overwrite without authorization, silent value transformation, missing required validations, or unintended sheet edits make the workbook unsafe to share.
- `BLOCKED`: Missing inputs, inaccessible evidence, unsafe inspection conditions, or unavailable essential validation prevent a reliable conclusion.
- `OUT_OF_SCOPE`: The requested audit, workbook change, or sheet component exceeds authorized scope.

When several verdicts apply, use `OUT_OF_SCOPE` for unauthorized scope, `BLOCKED` when the audit itself cannot proceed safely, `WORKBOOK_UNSAFE` for demonstrated unsafe state, and `NEEDS_REVISION` for correctable blocking findings. Use a ready verdict only when the inspected evidence supports each contract element.
