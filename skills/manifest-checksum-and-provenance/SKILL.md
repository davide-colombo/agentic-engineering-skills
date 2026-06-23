---
name: manifest-checksum-and-provenance
description: Audit manifests, checksums, provenance metadata, run inventories, and source/destination traceability for any generated scientific artifact, not only transfers. Use when a manifest must declare its files, an integrity contract must be verified, source-to-output provenance must be inspectable, and summary wording must not overclaim what validation establishes.
---

# Manifest and Checksum and Provenance

## Purpose

Determine whether a manifest, checksum record, or provenance metadata file correctly describes the artifact it covers, whether listed files exist and match recorded integrity evidence, whether unexpected or extra files are classified, and whether source-to-output traceability is inspectable. Detect omissions, drift, weak evidence, and summary wording that asserts integrity beyond what was actually validated.

## When to use

Use when generating, accepting, or auditing a manifest that describes any artifact set, including pipeline-stage outputs, deliverables, archives, packaged review material, restored backups, or run inventories. Use when a checksum file accompanies an artifact and downstream consumers will rely on it. Use when a provenance record must support reproducibility, attribution, or comparison across runs.

This skill is broader than [`data-transfer-and-integrity`](../data-transfer-and-integrity/SKILL.md), which focuses on source-to-destination movement. Use that skill when the manifest exists to validate a transfer between locations. Use this skill when the manifest covers a generated artifact whose primary integrity question is its own contents, regardless of movement.

## When not to use

Do not use as authorization to create, modify, or republish manifests; to overwrite or delete artifacts; or to publish summary statements without supporting evidence. Do not substitute it for repository-state, code-review, configuration, or domain validation. Do not use it to evaluate tabular schemas; defer to [`output-contract-and-table-schema-audit`](../output-contract-and-table-schema-audit/SKILL.md). Do not use it to evaluate sequence formats; defer to [`bioinformatics-sequence-output-audit`](../bioinformatics-sequence-output-audit/SKILL.md).

## Required inputs

Obtain from the current prompt and authoritative project material:

- Task objective, selected task mode, and allowed scope.
- The artifact set the manifest is claimed to describe.
- The manifest itself, its format, and its claimed coverage.
- The integrity contract: which fields are required, which checksum algorithms are accepted, and which provenance fields must be present.
- Permission to compute checksums, list files, and read artifact metadata at the named location.

If the artifact set, manifest, or integrity contract cannot be established, stop and report. Do not infer manifest semantics from extension or convention.

## Optional inputs

Use when supplied or discoverable within scope:

- A second independent manifest produced by a different tool or run.
- Prior validation evidence for the same artifact set.
- A registry, ledger, or external record that references the artifact by checksum or run identifier.
- Run logs, configuration snapshots, tool-version records, or operator notes.

Treat absent evidence as uncertainty, not as proof of integrity.

## Task modes

Choose exactly one mode and state it in the report:

- `MANIFEST_DESIGN_REVIEW`: Evaluate a proposed manifest format and coverage before implementation.
- `MANIFEST_AUDIT`: Inspect an implemented manifest against the artifact set it claims to describe.
- `CHECKSUM_AUDIT`: Verify checksum fields against recomputed digests over the artifact bytes.
- `PROVENANCE_AUDIT`: Inspect provenance metadata against the source-to-output traceability contract.
- `RUN_INVENTORY_AUDIT`: Evaluate an inventory of run artifacts (logs, sentinels, outputs, parameters) for completeness and consistency.
- `SUMMARY_WORDING_AUDIT`: Review human-readable summary statements about a manifest and confirm they do not overclaim integrity beyond what was actually validated.

A mode changes audit emphasis; it does not authorize creation, modification, or republication of manifests or artifacts.

## Manifest presence and schema

For each manifest under audit, identify:

- Path or storage location of the manifest.
- Format (plain text, JSON, JSONL, TSV, YAML, or other) and version when versioned.
- Producer identity (the tool, stage, or script that emitted the manifest).
- Required fields per entry (path, size, checksum, type, timestamp, source identifier, destination identifier, or others).
- Optional fields and their semantics.
- Encoding, line terminator, and field ordering when contractual.

A manifest without an explicit schema is not auditable. Record the absence and report it.

## Required files listed

Inspect that every required file in the artifact set is listed in the manifest:

- Enumerate the artifact set independently from the manifest.
- Compare the independently enumerated set against the manifest's path list.
- Record missing entries (required files not listed) and missing files (listed entries with no corresponding artifact on disk).
- Classify whether missing entries are a manifest-completeness defect or an artifact-loss defect.

Do not treat a manifest's count line as proof of completeness. Re-enumerate.

## Unexpected files classified

For each artifact present in the artifact set but absent from the manifest:

- Classify as expected-but-not-listed, intentional-not-included, scratch or intermediate, stale from a prior run, or unknown.
- For unknown entries, stop and report rather than silently include or exclude.

For each manifest entry not present in the artifact set:

- Classify as missing-required, retired-and-no-longer-produced, stale-from-prior-manifest, or unknown.
- For unknown entries, stop and report.

A manifest whose extra entries cannot be classified is unsafe for downstream use.

## Checksum matching

When the manifest carries checksums:

- Identify the algorithm (SHA-256, SHA-1, MD5, BLAKE2, or other).
- Classify each algorithm as cryptographically strong or weak. Treat weak checksums as accidental-corruption evidence only, not as identity or adversarial-integrity evidence.
- Recompute the digest from artifact bytes under the same algorithm and byte-scope rule.
- Record per-file pass, mismatch, missing-input, or unsupported-algorithm results.
- When the manifest references partial-content checksums (for example, header-only, payload-only, or by range), record the scope rule and verify it.

Do not declare integrity matched without enumerating the algorithm, scope, and per-file result.

## Source path or source identifier

For each artifact whose provenance includes an upstream source:

- Record the upstream source path, source identifier, or source-record key.
- Confirm the source is inspectable, or, when inspection is out of scope, record the upstream identifier and its issuer.
- Detect entries whose source identifier is missing, ambiguous, or inconsistent with the file content.

A manifest with implicit source provenance cannot support reproducibility claims.

## Destination path or artifact identity

For each manifest entry:

- Record the destination path or stable artifact identity.
- Confirm the path or identity is deterministic from the unit of work and not dependent on environment-specific naming.
- Detect entries whose destination identity could collide under concurrent runs.

## Tool and version when relevant

When the producing tool affects integrity or interpretation:

- Record the tool name and version that produced the artifact set.
- Record the tool name and version that produced the manifest, if different.
- Detect undeclared tool identity that is material to reproducibility.

Tool version is part of provenance when results depend on it.

## Parameters or configuration reference when relevant

When configuration affects the artifact:

- Record the configuration source: file path, hash, named parameter set, or commit identifier.
- Confirm the configuration is inspectable from the manifest at the time of audit.
- Detect configuration references that point to mutable, undated, or unreachable locations.

A manifest that references a mutable configuration without pinning is not reproducible.

## Timestamp or run identifier when relevant

When time-of-production or run identity matters:

- Record the timestamp format and time zone.
- Record the run identifier and its issuer.
- Detect timestamps that lack time zone or precision and run identifiers that are not unique across runs.

Timestamps alone are not integrity evidence; record them as metadata, not as proof.

## Inspectable input-to-output provenance

For each output entry:

- Identify the upstream inputs the entry depends on.
- Identify the transformation that produced the entry (tool, command, parameters).
- Confirm the chain from raw input to final output is inspectable from the manifest, logs, or referenced records.
- Detect chains broken by missing intermediate references, removed inputs, or rewritten history.

A manifest that cannot reconstruct input-to-output provenance does not support reproducibility.

## Summary wording that does not overclaim

When the manifest or its surrounding documentation includes human-readable summary statements:

- Record the exact summary wording.
- Compare each claim against the evidence the audit actually established.
- Flag wording such as "validated", "verified", "integrity confirmed", "reproducible", "complete", or "consistent" when the supporting evidence does not establish the claim.
- Recommend wording that distinguishes confirmed facts, partial evidence, and unvalidated assumptions.

Do not let the manifest's summary upgrade weak evidence into apparent strong evidence. Audit the wording explicitly.

## Unused or extra manifest entries

For each manifest entry that does not correspond to any artifact in scope:

- Classify as retired entry, scratch entry, stale entry, or unknown.
- For unknown entries, stop and report rather than silently accept or remove.

Extra entries that an audit cannot classify undermine the manifest's authority.

## Audit procedure

1. Restate the objective, selected task mode, scope, and the artifact set under audit.
2. Locate the manifest, its producer, its format, and its claimed coverage.
3. Enumerate the artifact set independently.
4. Compare the manifest path list against the enumerated set. Classify missing entries, missing files, and extra entries.
5. Recompute checksums where authorized and feasible. Record algorithm, scope, and per-file result.
6. Inspect source identifiers, destination identifiers, tool versions, parameter references, timestamps, and run identifiers as required by the contract.
7. Inspect input-to-output provenance chains for the artifacts within scope.
8. Inspect summary wording and recommend corrections when claims exceed evidence.
9. Classify findings, record commands actually run and evidence unavailable, and select exactly one verdict.

Do not treat the manifest's own assertions as independent evidence.

## Stop-and-report triggers

Stop before reuse, publication, downstream consumption, or summary release when:

- Manifest format or coverage is ambiguous and the gap is material.
- Required files are missing from the manifest, or listed files are missing from disk.
- Extra files or extra entries cannot be classified.
- Checksum algorithm is undeclared, weak, or scope is ambiguous, and integrity is being claimed.
- Source-to-output provenance chain is broken or unreachable.
- Tool version, parameter, or configuration references are required but missing.
- Timestamps lack time zone or precision and are being treated as integrity evidence.
- Summary wording overclaims integrity that the audit cannot establish.
- Required evidence cannot be inspected and the gap prevents a reliable verdict.

Report the trigger, affected entry or claim, evidence, and minimum decision or authorization required. Cross-reference [`evidence-citation-discipline`](../evidence-citation-discipline/SKILL.md) when reporting summary-wording corrections.

## Output contract

Produce these sections:

1. `VERDICT`: exactly one verdict from the vocabulary below and a one-sentence rationale.
2. `MODE AND SCOPE`: selected task mode, artifact set, manifest identity, allowed scope, and exclusions.
3. `MANIFEST SCHEMA`: format, version, producer, required fields, encoding, and ordering rules.
4. `COVERAGE COMPARISON`: required-files-listed evidence, missing entries, missing files, extra entries, and classification of each.
5. `CHECKSUM EVIDENCE`: algorithm, scope, per-file result, and limitations.
6. `SOURCE AND DESTINATION IDENTITY`: source identifiers, destination identifiers, and ambiguity findings.
7. `TOOL, CONFIGURATION, AND TIMESTAMP`: tool versions, configuration references, run identifiers, and timestamp findings.
8. `PROVENANCE CHAINS`: input-to-output traceability for each artifact in scope.
9. `SUMMARY WORDING REVIEW`: exact wording inspected and corrections recommended.
10. `VALIDATION EVIDENCE`: commands actually run, exit statuses, concise results, checks not run, and impact.
11. `FINDINGS`: blocking findings and non-blocking warnings with location, evidence, consequence, and minimum resolution; write `none` for empty categories.
12. `NEXT STEP`: the minimum design correction, implementation action, validation, or authorization supported by the verdict.

Do not claim entries, checksums, provenance, or summary statements were verified unless the supporting evidence was actually inspected or computed.

## Allowed actions

- Read the manifest, the artifact set, configuration, logs, and external records within scope.
- Recompute checksums under authorized algorithms.
- Compare enumerations, classify entries, and inspect provenance chains.
- Propose manifest schema corrections, additional fields, or summary-wording corrections without applying them unless separately authorized.

## Forbidden actions

- Modify the manifest, artifacts, or summary documentation during an audit.
- Treat the manifest's own count, summary line, or wording as integrity proof.
- Assume a checksum algorithm or byte-scope rule from convention without verification.
- Publish wording such as "verified", "validated", or "integrity confirmed" when supporting evidence is partial or absent.
- Expose private paths, restricted identifiers, or sensitive content in reports or commands.

## Verdict vocabulary

- `MANIFEST_INTEGRITY_READY`: Schema, coverage, checksum, source/destination, tool/configuration, provenance, and summary-wording elements satisfy the selected mode with no remaining warnings.
- `MANIFEST_INTEGRITY_READY_WITH_WARNINGS`: No blocking finding remains, but substantiated non-blocking limitations or residual risks are explicitly reported.
- `NEEDS_REVISION`: One or more correctable blocking manifest, checksum, provenance, or wording findings prevent acceptance.
- `MANIFEST_OVERCLAIMS`: Summary wording or documented claims assert integrity beyond what the audit can establish, even when underlying artifacts may be acceptable.
- `BLOCKED`: Missing inputs, inaccessible evidence, unsafe inspection conditions, or unavailable essential validation prevent a reliable conclusion.
- `OUT_OF_SCOPE`: The requested audit, manifest change, or artifact component exceeds authorized scope.

When several verdicts apply, use `OUT_OF_SCOPE` for unauthorized scope, `BLOCKED` when the audit itself cannot proceed safely, `MANIFEST_OVERCLAIMS` for demonstrated wording risk, and `NEEDS_REVISION` for correctable blocking findings. Use a ready verdict only when contract elements are explicit and supported by inspected evidence.
