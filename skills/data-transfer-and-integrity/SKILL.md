---
name: data-transfer-and-integrity
description: Design, audit, or review data transfer, synchronization, artifact movement, manifests, checksums, partial-transfer recovery, archive handling, and provenance preservation. Use when scientific, computational, or large-data workflows need safe movement between locations, explicit inventory contracts, integrity validation before downstream use, resumable transfer behavior, or deliverable packaging assessment.
---

# Data Transfer and Integrity

## Purpose

Determine whether data movement preserves the expected payload, structure, integrity, metadata, and provenance without destructive or silent behavior. Detect missing, extra, partial, truncated, corrupted, stale, renamed, or unsafe linked content before transferred data is published, packaged, or used downstream.

## When to use

Use when designing or changing a transfer workflow, preparing or receiving deliverables, synchronizing locations, resuming interrupted movement, producing or auditing manifests, validating copied artifacts, handling archives, or diagnosing disagreement between source and destination.

## When not to use

Do not use as authorization to transfer data, contact remote systems, overwrite or delete destination content, extract untrusted archives, expose restricted metadata, or broaden data access. Do not substitute it for repository, security, privacy, retention, licensing, configuration, or domain validation. Perform the applicable higher-level audit first when authority or repository state is unknown.

## Required inputs

Obtain from the current prompt and authoritative project material:

- Task objective, selected task mode, allowed scope, data classification, and acceptance criteria.
- Source location, destination location, transfer direction, and permitted transfer mechanism.
- Expected file inventory, directory structure, naming rules, required metadata, and provenance contract.
- Applicable source and destination filesystem or storage semantics.
- Authorization for network access, transfer, overwrite, deletion, mirroring, archive extraction, or publication when any is required.
- Expected validation commands and evidence required before downstream use.

If the objective, locations, payload boundary, destination ownership, or side-effect authority cannot be established reliably, stop and report. Do not invent transfer policy absent from the current prompt, project profile, local overlay, or on-disk documentation.

## Optional inputs

Use when supplied or discoverable within scope:

- Source-produced or independently supplied manifests, checksums, file counts, byte counts, and transfer logs.
- Prior destination inventory, known stale-content policy, and retention or deletion constraints.
- Symlink, hidden-file, empty-file, permission, executable-bit, timestamp, and filename-normalization policy.
- Expected archive format, compression settings, extraction rules, and packaging specification.
- Interruption records, partial-transfer markers, temporary naming, resume tokens, or publication state.
- Downstream consumer requirements and provenance records.

Treat missing optional evidence as uncertainty, not as permission to infer integrity.

## Task modes

Choose exactly one mode and state it in the report:

- `TRANSFER_DESIGN_REVIEW`: Evaluate a proposed source-to-destination workflow, inventory contract, integrity strategy, failure behavior, publication boundary, and authority before execution.
- `PRE_TRANSFER_AUDIT`: Confirm locations, payload, mechanism, capacity, semantics, destructive behavior, provenance requirements, and validation plan before movement begins.
- `POST_TRANSFER_AUDIT`: Compare source, manifest, transfer evidence, and destination before declaring the transfer complete or permitting downstream use.
- `RESUME_TRANSFER_AUDIT`: Determine whether interrupted or partial state can be identified and resumed without accepting corruption, duplicating content, or overwriting valid data.
- `MANIFEST_AUDIT`: Assess manifest scope, producer, consumer, format, checksum strength, path semantics, and agreement with the intended payload.
- `DELIVERABLE_PACKAGING_AUDIT`: Validate payload inventory, archive or package integrity, extracted content, metadata, provenance, naming, and publication readiness.

A mode changes audit emphasis; it does not authorize transfer, deletion, overwrite, extraction, remote access, or publication.

## Data model

Define the payload using these terms precisely:

- `source file`: A file at the authoritative origin selected for transfer or comparison.
- `destination file`: A file present at the receiving location after or during transfer.
- `expected file`: A required payload member declared by the applicable inventory contract.
- `unexpected file`: A source or destination member outside the applicable inventory contract.
- `missing file`: An expected file absent from the location where validation requires it.
- `extra file`: A destination file not represented by the expected inventory and not explicitly permitted.
- `zero-byte valid file`: An empty file that the project contract explicitly permits as a meaningful payload member.
- `zero-byte suspicious file`: An empty file whose validity is not established or conflicts with expected content.
- `partial file`: A transfer artifact known or suspected to contain only part of the intended bytes or metadata.
- `truncated file`: A file ending before the complete expected content, even if it was published under the final name.
- `corrupted file`: A file whose bytes or structure fail the applicable integrity contract.
- `stale file`: A destination file from an earlier state that is no longer part of the intended payload or current version.
- `renamed file`: Content whose path or name differs from the declared source-to-destination mapping.
- `symlink`: A directory entry referring to another path rather than containing the target payload itself.
- `broken symlink`: A symlink whose target cannot be resolved in the applicable destination context.
- `dereferenced symlink`: A link transferred as the target content rather than preserved as a link.
- `manifest entry`: One declared payload record containing a path and applicable size, checksum, type, metadata, or provenance fields.
- `checksum match`: The computed digest agrees with the expected digest under the same algorithm and byte representation.
- `checksum mismatch`: The computed digest differs from the expected digest under comparable conditions.
- `count mismatch`: Observed file or entry counts differ from the applicable expected counts.
- `byte-size mismatch`: Observed bytes differ from the expected size for a file, archive, payload, or aggregate.
- `timestamp drift`: Source and destination timestamps differ beyond policy without independently proving content change.
- `permission drift`: Required permission or executable semantics differ between source, manifest, and destination.
- `destructive mirror operation`: Synchronization can delete, replace, or reconcile destination content to match the source.
- `non-destructive copy operation`: Movement adds or writes selected content without intentionally deleting unrelated destination entries.
- `archive payload`: The entries and metadata represented inside a package before extraction.
- `extracted payload`: The entries and metadata materialized from an archive.
- `provenance metadata`: Records required to identify origin, production context, transformation, version, transfer, validation, or custody.

State whether hidden files are included or excluded, whether symlinks are expected, forbidden, preserved, or dereferenced, and whether empty files are valid by contract or suspicious. Do not infer these policies from tool defaults.

## Transfer model

Define the complete movement contract:

- Canonical source and destination locations, direction, ownership, access boundaries, and destination publication point.
- Transfer tool or mechanism, relevant version or behavior when material, options, path mapping, include/exclude rules, and retry policy.
- Expected files, directories, hidden entries, symlinks, names, counts, bytes, permissions, executability, and metadata.
- Source and destination filesystem or storage differences, including naming, case, path, link, permission, timestamp, atomicity, consistency, and replacement semantics.
- Whether timestamps are authoritative or advisory and which evidence takes precedence when timestamps disagree.
- Temporary paths, partial naming, atomic transfer-to-temp then publish or move behavior, and cleanup authority.
- Overwrite, conflict, deletion, pruning, and mirroring behavior, including how stale destination files are detected and handled.
- Resume granularity, retry boundaries, idempotence, and how a resumed operation revalidates existing destination content.

Require deterministic file naming or a documented mapping from source identity to destination identity. Classify every operation as non-destructive, overwrite-capable, or destructive before execution.

## Integrity model

Define independent evidence for completeness and correctness:

- Expected inventory and directory structure from an authoritative manifest or explicit contract.
- Source and destination file counts and aggregate byte counts, with clear rules for files, directories, links, hidden entries, and archive members.
- Per-file or aggregate checksums where available, including algorithm, producer, byte representation, and verification environment.
- Structural or format validation when byte equality alone does not establish usability.
- Required permissions, executability, symlink semantics, metadata, and provenance consistency.
- Partial, truncated, corrupted, stale, extra, renamed, and unexpected-content detection.
- Validation boundary that must pass before publication, packaging, extraction acceptance, or downstream use.

Classify checksum algorithms as cryptographic or weak. Prefer cryptographic checksums for scientific or long-lived artifacts. Treat weak checksums as limited accidental-corruption evidence, not strong identity or adversarial-integrity proof.

## Audit procedure

1. Restate the objective, selected mode, scope, source, destination, direction, mechanism, payload contract, and authorized side effects.
2. Inspect the source inventory, directory structure, hidden entries, symlinks, empty files, counts, bytes, names, permissions, timestamps, and provenance requirements.
3. Inspect the destination before any overwrite, deletion, mirror, cleanup, resume, extraction, or publication decision. Identify existing, stale, partial, conflicting, and unrelated content.
4. Compare source and destination storage semantics and identify changes to paths, names, case, links, permissions, timestamps, atomicity, or consistency.
5. Inspect the transfer mechanism's include, exclude, overwrite, deletion, retry, resume, link, metadata, temporary-file, and completion behavior.
6. Establish the authoritative manifest, its producer and consumer, coverage, checksum strength, path base, and agreement with the payload contract.
7. Run the manifest, partial-transfer, provenance, archive, and validation procedures applicable to the selected mode.
8. Verify that transfer validation occurs before downstream use and that unresolved risks remain visible to consumers.
9. Classify findings, record commands actually run and evidence unavailable, and select exactly one verdict.

Do not treat a transfer completion message or successful command exit as proof of integrity.

## Manifest and checksum procedure

1. Identify the manifest format, version, path base, encoding, ordering requirements, producer, production time, and intended consumer.
2. Determine whether it covers every required file, directory when relevant, hidden entry, symlink, archive member, and required provenance record.
3. Verify path uniqueness, deterministic naming, type information, file counts, byte sizes, checksum fields, and required metadata.
4. Compare manifest entries with the expected inventory, source, destination, archive payload, and extracted payload as applicable.
5. Recompute checksums from source or destination bytes when authorized and feasible; record the algorithm and exact comparison scope.
6. Distinguish cryptographic checksums from weak checksums and explain the protection each provides.
7. Report missing, extra, duplicate, renamed, malformed, stale, or contradictory manifest entries explicitly.

Do not rely on file counts alone when checksums or byte counts are available. Prefer explicit manifests over implicit directory assumptions.

## Partial-transfer and resume procedure

1. Determine how in-progress content is named, isolated, recorded, and prevented from appearing complete.
2. Identify partial files using temporary names, expected sizes, manifests, checksums, transfer state, structural validation, or other independent evidence.
3. Detect interrupted operations whose final names exist despite truncated bytes, missing metadata, incomplete directory trees, or not-yet-published state.
4. Define whether resume continues partial content, retransfers whole files, skips validated files, or restarts a bounded unit.
5. Before skipping an existing destination file, validate it against the current manifest or source contract; existence alone is insufficient.
6. Confirm resumed transfer behavior is idempotent and does not append duplicate data, retain incompatible partial state, or overwrite verified content unexpectedly.
7. Re-run complete destination validation after resume. A successful resume command does not prove earlier or newly transferred content is valid.

Prefer atomic transfer-to-temp then publish or move when supported. Do not silently repair, delete, or rename partial state without authorization.

## Provenance and metadata procedure

1. Identify provenance needed for downstream interpretation, including origin, producer, version, transformation, manifest identity, transfer event, and validation result as applicable.
2. Map each required provenance field to an authoritative source and destination representation.
3. Verify manifests, logs, sidecars, embedded metadata, and naming agree internally and with the payload.
4. Determine whether permissions, executability, ownership class, timestamps, link targets, or extended metadata are required contracts or advisory observations.
5. Record transfer direction, mechanism, relevant options, validation evidence, and material transformations without exposing private locations, identities, credentials, or restricted metadata.
6. Confirm downstream consumers receive the provenance needed to interpret the transferred version and distinguish it from stale or alternate payloads.

Do not claim provenance is preserved unless required metadata, manifests, or logs are present and internally consistent. Do not rely on timestamps alone as integrity evidence.

## Archive and packaging procedure

1. Validate the intended payload inventory before archive or package creation. Do not package deliverables before this check passes.
2. Define archive format, compression behavior, root layout, deterministic naming, hidden-file policy, symlink policy, permissions, timestamps, and provenance contents.
3. Compare archive entries, counts, paths, types, sizes, and checksums when available with the intended manifest.
4. Validate the archive file itself using applicable checksum, structural listing, format test, or reader validation without assuming extraction success.
5. When safe and possible, extract into an isolated temporary location and compare the extracted payload with the manifest and intended payload.
6. Detect path traversal, absolute paths, unsafe links, duplicate paths, case collisions, unexpected entries, and overwrite behavior before extraction into a destination.
7. Record archive checksum separately from payload checksums because package-level equality and extracted-content integrity answer different questions.

Do not claim an archive is valid without validating both the archive file and the extracted payload when possible. If extraction validation is unavailable, report it as not run and explain the impact.

## Validation procedure

1. Confirm the source inventory is stable enough for the selected transfer and validation method, or record how concurrent source changes are detected.
2. Compare expected, source, manifest, destination, archive, and extracted inventories using consistent path, link, hidden-file, and type rules.
3. Compare file counts and byte counts, then verify checksums where available. Investigate every mismatch rather than allowing one aggregate to conceal another.
4. Validate zero-byte files against the explicit contract and distinguish valid from suspicious empty content.
5. Validate symlink preservation, dereferencing, target safety, and broken-link behavior.
6. Check missing, extra, partial, truncated, corrupted, stale, renamed, and unexpected files explicitly.
7. Validate required permissions, executability, structure, format, metadata, and provenance.
8. Confirm stale destination files cannot contaminate downstream discovery, aggregation, packaging, or execution.
9. Record commands actually run, exit statuses, locations or environments inspected, concise results, checks not run, reasons, and impact.
10. Block downstream use until validation passes or unresolved risks are explicitly reported to the authorized decision-maker and consumers.

## Risk classification

Assign each finding one primary category and a severity of `BLOCKING` or `NON_BLOCKING`:

- `inventory completeness`: Expected, missing, extra, unexpected, renamed, hidden, or stale content disagrees with the payload contract.
- `content integrity`: Checksums, sizes, structure, or format indicate partial, truncated, corrupted, or unverified content.
- `transfer safety`: Overwrite, deletion, mirroring, retry, resume, temporary-state, or publication behavior can lose or misrepresent data.
- `link and path safety`: Symlinks, broken links, dereferencing, path mapping, traversal, collision, or filesystem semantics are unsafe or ambiguous.
- `metadata and provenance`: Required permissions, executability, metadata, manifests, logs, or origin records are missing or inconsistent.
- `archive and packaging`: Archive structure, archive bytes, extracted payload, compression, or packaging contract is invalid or insufficiently verified.
- `validation evidence`: Required checks were not run, used weak evidence, or occurred after downstream consumption.
- `scope violation`: Transfer, access, deletion, extraction, publication, or other work exceeds authorized scope.
- `non-blocking improvement`: A substantiated improvement that does not threaten data identity, completeness, integrity, safety, provenance, or downstream interpretation.

Use `BLOCKING` for missing expected content, checksum mismatch, unexplained size or count mismatch, unsafe destructive behavior, unvalidated partial state, contaminating extra or stale content, unsafe links or paths, insufficient required provenance, or evidence gaps that prevent a reliable conclusion.

## Stop-and-report triggers

Stop before transfer, overwrite, deletion, mirroring, cleanup, extraction, publication, or downstream use when:

- Source, destination, direction, payload, ownership, data classification, or authority is ambiguous.
- The requested operation can overwrite or delete destination data without explicit current-prompt authorization.
- Destructive mirror or synchronization behavior is requested without explicit authorization and prior destination inspection.
- The manifest omits required content, has ambiguous path semantics, or disagrees materially with source or destination evidence.
- Expected files are missing, or extra or stale destination files can contaminate downstream use.
- Partial, truncated, corrupted, or checksum-mismatched content is detected or cannot be distinguished from complete content.
- Symlink preservation, dereferencing, broken-link behavior, or target safety is unknown and material.
- Source and destination semantics can change naming, links, permissions, timestamps, atomicity, or content interpretation without an accepted policy.
- Archive inspection or extraction would expose unsafe paths, overwrite content, contact an external system, or exceed authorization.
- Required provenance is missing or validation cannot occur before downstream use.

Report the trigger, evidence, affected content and location, consequence, and minimum decision, evidence, or authorization required. Prefer fail-loud reporting over silent repair or cleanup.

## Output contract

Produce these sections:

1. `VERDICT`: exactly one verdict and a one-sentence rationale.
2. `MODE AND SCOPE`: selected mode, objective, source, destination, direction, transfer mechanism, authorized actions, and exclusions.
3. `PAYLOAD CONTRACT`: expected inventory, directory structure, names, hidden files, empty files, symlinks, counts, bytes, metadata, and provenance.
4. `TRANSFER MODEL`: path mapping, storage semantics, options, overwrite or deletion behavior, temporary state, retry, resume, atomicity, and publication boundary.
5. `MANIFEST AND CHECKSUM EVIDENCE`: producer, consumer, format, coverage, algorithms, entries, comparisons, mismatches, and limitations.
6. `SOURCE AND DESTINATION COMPARISON`: missing, extra, partial, truncated, corrupted, stale, renamed, linked, count, byte, timestamp, and permission findings.
7. `ARCHIVE AND PACKAGING EVIDENCE`: archive validation, payload listing, extraction validation, safety checks, and package provenance.
8. `VALIDATION EVIDENCE`: commands actually run, exit statuses, concise results, checks not run, reasons, environments, and impact.
9. `FINDINGS`: blocking findings and non-blocking warnings with category, path or payload component, evidence, consequence, and minimum resolution; write `none` for empty categories.
10. `DOWNSTREAM-USE STATUS`: whether use is permitted, blocked, or requires an explicit risk decision.
11. `NEXT STEP`: the minimum correction, retransfer, validation, authorization, or publication action supported by the verdict.

Do not report content, checksums, manifests, provenance, archives, transfers, or destination state as verified unless supporting evidence was actually inspected or executed.

## Allowed actions

- Read task instructions, project profiles, overlays, manifests, logs, inventories, metadata, archive listings, and source or destination evidence within scope.
- Run local read-only inventory, checksum, structural, archive-listing, and comparison commands when explicitly safe and authorized.
- Inspect transfer configuration and dry-run output only when the mechanism guarantees no prohibited side effect.
- Calculate counts and byte totals, compare manifests, and propose safe transfer, resume, validation, or packaging procedures.
- Report mismatches, unavailable checks, uncertainty, and the minimum evidence or authorization needed.

## Forbidden actions

- Transfer, overwrite, delete, mirror, prune, clean, extract, publish, or use data downstream without the required explicit authorization and validation state.
- Treat command success, a completion message, file existence, counts alone, or timestamps alone as proof of integrity.
- Silently ignore missing expected files or contaminating extra or stale destination files.
- Assume symlink, hidden-file, empty-file, permission, timestamp, archive, or filesystem behavior from tool defaults.
- Use destructive mirror or synchronization behavior without explicit current-prompt authorization and destination inspection.
- Package an unvalidated payload or claim archive validity without the applicable archive and extracted-payload checks.
- Claim provenance preservation without internally consistent required evidence.
- Expose private locations, credentials, restricted metadata, or sensitive inventory in reports or commands.
- Broaden scope or silently repair, rename, overwrite, delete, or clean findings during an audit.

## Verdict vocabulary

- `TRANSFER_INTEGRITY_READY`: The applicable payload, transfer behavior, destination state, integrity evidence, metadata, provenance, and validation satisfy the selected mode with no remaining warnings.
- `TRANSFER_INTEGRITY_READY_WITH_WARNINGS`: No blocking finding remains, but substantiated non-blocking limitations, weak evidence, or residual risks are explicitly reported.
- `NEEDS_REVISION`: One or more correctable blocking design, manifest, resume, packaging, provenance, or validation findings prevent acceptance.
- `INTEGRITY_UNVERIFIED`: Available evidence is insufficient to establish required content identity, completeness, or integrity, but does not demonstrate unsafe data.
- `DATA_UNSAFE`: Available evidence demonstrates corruption, destructive risk, unsafe path or link behavior, contaminating content, or other conditions that make transfer, publication, packaging, or downstream use unsafe.
- `BLOCKED`: Missing inputs, inaccessible evidence, unsafe inspection conditions, or unavailable essential validation prevent a reliable conclusion.
- `OUT_OF_SCOPE`: The requested transfer, audit, deletion, extraction, publication, downstream use, or material payload component exceeds authorized scope.

When several verdicts apply, use `OUT_OF_SCOPE` for unauthorized scope, `BLOCKED` when the audit itself cannot proceed safely, `DATA_UNSAFE` for demonstrated unsafe data or behavior, `INTEGRITY_UNVERIFIED` when required integrity remains unproven, and `NEEDS_REVISION` for correctable blocking design findings. Use a ready verdict only when no blocking finding remains and evidence is sufficient for the selected mode.
