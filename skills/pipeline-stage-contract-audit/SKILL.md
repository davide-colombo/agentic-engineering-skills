---
name: pipeline-stage-contract-audit
description: Audit the explicit contract of one concrete stage in a multi-step computational pipeline. Use when a specific stage needs its identity, inputs, outputs, checkpoint semantics, resume and force behavior, intermediate state, atomic publication, logging, output column contracts, and downstream consumer assumptions inspected against on-disk and code evidence before downstream work depends on its results.
---

# Pipeline Stage Contract Audit

## Purpose

Determine whether one concrete pipeline stage has an explicit, inspectable contract and whether its implementation honors that contract end-to-end. This skill focuses on a single stage boundary rather than the whole workflow. Detect missing or implicit contract elements, divergence between declared inputs/outputs and code behavior, unsafe resume or force semantics, undeclared intermediate state, non-atomic publication, ambiguous output column contracts, and undocumented assumptions that downstream consumers rely on.

## When to use

Use when a specific pipeline stage will be designed, changed, audited, ported, accepted for reuse, repaired after failure, declared production-ready, or made a dependency of new downstream work. Use after a stage failed in a way that suggests its contract was implicit rather than explicit. Use before integrating a new stage between two existing stages.

For general resumability of an entire multi-step workflow, including cross-stage aggregation barriers, design-time state model, and pipeline-wide failure semantics, use [`resumable-pipeline-design`](../resumable-pipeline-design/SKILL.md). This skill is narrower: it inspects the explicit contract of one named stage and does not redesign the pipeline.

## When not to use

Do not use as authorization to implement, repair, rerun, force, delete, or publish stage outputs. Do not use as a substitute for repository-state, code-review, configuration, environment, data-transfer, or domain validation. Do not use to evaluate the cross-stage dependency graph; that work belongs in `resumable-pipeline-design`. Do not use to claim scientific correctness of the stage's results; that work belongs in [`scientific-data-integrity-audit`](../scientific-data-integrity-audit/SKILL.md).

## Required inputs

Obtain from the current prompt and authoritative project material:

- The unambiguous identity of the stage under audit, including its name, entry point, configured invocation, and position in the pipeline.
- The intended boundary of the stage: where it begins, where it ends, and what is explicitly out of scope.
- The current prompt's selected task mode and allowed scope.
- Applicable project instructions, acceptance criteria, and validation constraints for the stage.
- Permission to read the stage's code, configuration, and prior outputs at named locations.

If the stage identity, boundary, or invocation cannot be established reliably, stop and report. Do not infer a stage boundary from filename similarity, log lines, or convenience.

## Optional inputs

Use when supplied or discoverable within scope:

- Upstream stage outputs and the contract by which they are produced.
- Downstream stage inputs and the contract by which they are consumed.
- Existing checkpoint or sentinel files, resume logic, force/rerun flags, and progress logs.
- Sample successful run outputs, failed run remains, and prior incident records for the stage.
- Configuration parameters that affect the stage's behavior, including thresholds, paths, and concurrency.

Treat absent evidence as uncertainty, not as proof that the contract is correct.

## Task modes

Choose exactly one mode and state it in the report:

- `STAGE_CONTRACT_DESIGN_REVIEW`: Evaluate a proposed contract for a stage before implementation.
- `STAGE_CONTRACT_AUDIT`: Inspect an implemented stage's contract against code, configuration, and observable artifacts.
- `STAGE_RESUME_AUDIT`: Determine whether the stage's resume, force, and sentinel semantics are explicit and safe under interruption.
- `STAGE_OUTPUT_AUDIT`: Evaluate the stage's declared outputs, optional outputs, valid-empty outputs, and column contracts against produced artifacts.
- `STAGE_FAILURE_REPORTING_AUDIT`: Inspect how the stage reports local and global failure to operators and downstream consumers.

A mode changes audit emphasis; it does not authorize file changes, rerun, force, deletion, or publication.

## Stage identity and boundary

Define the stage precisely before evaluating its contract:

- Stage name as referenced in code, configuration, logs, and operator documentation.
- Concrete entry point (function, command, script, or job specification) and invocation parameters.
- Upstream artifact set the stage consumes and downstream artifact set the stage produces.
- The smallest resumable unit of work inside the stage (per record, per partition, per file, per global run) and its identity rule.
- Operations explicitly inside the stage versus operations that belong to upstream or downstream stages.

If two reasonable interpretations of the stage boundary exist, record both and stop until the prompt or project policy disambiguates.

## Inputs contract

For every upstream input the stage requires:

- Authoritative source location and naming rule.
- Required structural or schema contract that the stage relies on.
- Optional fields the stage tolerates without using.
- Valid-empty input semantics, when permitted by the upstream contract.
- How the stage detects missing, partial, corrupted, or stale upstream input.
- Preflight checks performed before any output is touched.

A stage that consumes an upstream output without inspecting the upstream contract is implicitly trusting it. Record this trust and report it as a finding when the upstream contract has no independent audit.

## Outputs contract

Distinguish the following output categories:

- `required output`: An artifact the stage must produce on success. Its absence is failure.
- `optional output`: An artifact the stage may produce when triggered by inputs, configuration, or detected conditions. Its absence is not failure.
- `valid-empty output`: An artifact that may legitimately contain zero records or zero bytes when the input or biology produces no result. The contract must explicitly distinguish a valid-empty result from a missing or corrupted result.
- `diagnostic output`: Logs, metrics, progress files, and intermediate human-inspection artifacts that are not part of the downstream-consumable contract.

For each declared output, specify:

- Path or naming rule, including any deterministic identifier that ties the output to the unit of work.
- Format, schema, encoding, and column or field contract, audited under [`output-contract-and-table-schema-audit`](../output-contract-and-table-schema-audit/SKILL.md) when tabular.
- Atomic publication boundary: how the output becomes visible to downstream consumers only after it is complete.
- Validation evidence: the smallest check that distinguishes a valid output from missing, partial, or corrupted state.

If a required output cannot be distinguished from a valid-empty output without inspecting code or operator memory, the contract is not explicit.

## Sentinel and checkpoint semantics

For each sentinel or checkpoint the stage uses:

- The path or storage rule, file name, and ownership.
- The schema or contents, including the unit-of-work identifier and any binding to inputs, configuration, code, or dependency identity required to detect stale state.
- The publication rule: a sentinel must be created after all required outputs are durably published, not before.
- Detection of interrupted runs whose outputs partially exist but whose sentinel does not.
- Rejection of a sentinel whose claimed outputs cannot be independently validated.

A sentinel that exists alongside missing, partial, corrupted, or stale outputs is not evidence of completion. Record this state and report it.

## Preflight checks

Identify the checks the stage performs before any output is mutated:

- Required upstream inputs present and structurally valid.
- Configuration parameters parsed, validated, and within supported ranges.
- Required external tools and dependency versions resolvable.
- Output paths writable, with sufficient space and no conflicting active state.
- No concurrent writer is operating on the same unit of work.

A stage that begins mutating outputs before preflight checks pass cannot be safely resumed and should be reported.

## Resume behavior

For the stage's normal resume path, document:

- Detection rule for already-completed units of work, including the evidence used (sentinel, output set, manifest, or external state).
- Behavior when a unit's outputs are missing, partial, corrupted, or stale.
- Behavior when a unit's sentinel is present but its outputs cannot be validated.
- Whether resume is unit-local, partition-local, or stage-global.
- How resume interacts with valid-empty outputs.

Existence of an output file alone is not a safe resume signal. Record the validation a resume decision actually performs.

## Force and rerun behavior

For the stage's force or rerun path, document:

- Operator-visible trigger (flag, configuration key, command-line option, or explicit deletion of sentinel).
- Scope: per unit, per partition, or whole stage.
- Whether forced rerun overwrites in place or republishes atomically.
- Downstream invalidation behavior when forced rerun changes outputs that downstream stages already consumed.
- Whether forced rerun is auditable: a log record that distinguishes forced rerun from normal resume and from automated retry.

A stage that performs forced rerun without auditable evidence cannot be relied on for provenance.

## Temporary and intermediate state

Identify and classify all intermediate state the stage produces:

- Working directories or scratch paths the stage writes to.
- Intermediate files that are not part of the published output contract.
- Cleanup responsibility: which step removes intermediate state, under which conditions, and whether failed runs leave intermediate state for diagnosis.
- Naming rules that distinguish intermediate state from published output.

Intermediate state that lives inside the published output path is unsafe. Intermediate state that has the same naming pattern as published output is unsafe. Report both.

## Atomic output publication

Describe how each required output transitions from in-progress to published:

- Whether outputs are written to a temporary path and then renamed or moved atomically.
- Whether outputs are written in place and may appear partially written to downstream consumers.
- Whether a manifest or sentinel is the publication barrier and is created after all outputs are durable.
- Whether the storage layer supports atomic rename or copy and whether the stage relies on that property.

A stage that publishes in place without atomic boundary cannot be safely interrupted. Report this and the consequence for downstream consumers.

## Logs and progress artifacts

Inspect operator-facing artifacts:

- Log path, log rotation rule, and structured-event fields if any.
- Progress reporting cadence and unit (records, partitions, files).
- Distinction in logs between started, completed, skipped, retried, forced, failed, interrupted, and operator-recovered work.
- Whether logs include the unit-of-work identifier and timestamps sufficient for after-the-fact diagnosis.
- Whether sensitive paths, credentials, or restricted identifiers leak into logs.

Diagnostic output is part of the stage contract. A stage whose logs cannot distinguish completion from interruption is not auditable.

## Output column contracts

When the stage produces tabular outputs, audit the column contract using [`output-contract-and-table-schema-audit`](../output-contract-and-table-schema-audit/SKILL.md). Within this stage audit, record at minimum:

- Required columns and whether their names, order, and types are contractual.
- Primary-key or row-identity columns and uniqueness expectations.
- Units, coordinate conventions, and missing-value conventions used by the stage.
- Valid-empty table semantics: a header-only file, an absent file, or another agreed representation.

Inconsistency between the stage's documented column contract and its produced tables is a blocking finding for downstream consumers.

## Downstream consumer assumptions

Identify each downstream consumer of the stage's outputs:

- Direct downstream stages, scripts, or operators.
- Required columns, fields, formats, or sentinels the consumer reads.
- Assumptions about output ordering, completeness, or freshness.
- Behavior of the consumer when the output is valid-empty, missing, or stale.

A downstream consumer that depends on an unstated property of the stage is a hidden contract. Record it and report whether the stage guarantees that property.

## Failure reporting

For each failure mode, document:

- Local failure: one unit cannot satisfy the stage contract while other units remain valid.
- Global failure: a shared precondition is invalid and the stage cannot safely continue.
- Operator-visible message: where it appears, what identifying information it includes, and how it distinguishes failure cause categories.
- State left on disk after failure: which artifacts persist for diagnosis and which are removed.
- Interaction with the resume path: whether a re-invocation after failure attempts recovery, skips the failed unit, or refuses to proceed until the operator intervenes.

A stage that silently exits zero after a partial failure is unsafe. Report this and the consequence.

## Audit procedure

1. Restate the objective, selected task mode, scope, stage identity, and stage boundary.
2. Locate the stage's entry point and configuration. Confirm the invocation path matches the declared boundary.
3. Inspect inputs contract against upstream artifacts and code that reads them.
4. Inspect outputs contract against code that writes them and against representative produced artifacts when available.
5. Inspect sentinel and checkpoint semantics against the code that creates and reads them.
6. Inspect preflight checks against the code that runs before any output is mutated.
7. Inspect resume behavior against representative resumed runs or, when not available, against the code that drives the resume decision.
8. Inspect force/rerun behavior against the operator-visible trigger and the code path it activates.
9. Inspect temporary and intermediate state against the code that writes it and the cleanup path.
10. Inspect atomic publication against the storage operations the code performs.
11. Inspect logs and progress artifacts against representative log output and the structured-event schema.
12. Inspect output column contracts against produced tables; defer detailed schema audit to [`output-contract-and-table-schema-audit`](../output-contract-and-table-schema-audit/SKILL.md).
13. Inspect downstream consumer assumptions against the consumers' code and contracts.
14. Inspect failure reporting against representative failed runs or, when not available, against the code that constructs operator-visible messages.
15. Classify findings, record commands actually run and evidence unavailable, and select exactly one verdict.

Do not treat presence of an output, presence of a sentinel, or successful invocation as proof that the contract is honored.

## Stop-and-report triggers

Stop before implementation, rerun, force, deletion, or publication when:

- Stage identity or boundary cannot be established.
- The stage's required and valid-empty outputs cannot be distinguished from missing or corrupted state.
- A sentinel exists alongside outputs that cannot be independently validated.
- Resume relies only on existence checks and no independent validation.
- Force/rerun behavior cannot be distinguished from normal resume in logs or state.
- Atomic publication is not used and downstream consumers can observe partial state.
- Intermediate state lives inside or shares a naming pattern with published output.
- Failure reporting cannot distinguish local from global failure or exits zero after partial failure.
- A downstream consumer depends on an unstated property of the stage.
- Required evidence cannot be inspected and the gap prevents a reliable verdict.

Report the trigger, the affected element, the evidence, and the minimum decision or authorization required.

## Output contract

Produce these sections:

1. `VERDICT`: exactly one verdict from the vocabulary below and a one-sentence rationale.
2. `MODE AND SCOPE`: selected task mode, stage identity and boundary, allowed scope, and exclusions.
3. `INPUTS CONTRACT`: required upstream inputs, optional inputs, valid-empty input semantics, and preflight checks.
4. `OUTPUTS CONTRACT`: required outputs, optional outputs, valid-empty outputs, diagnostic outputs, and column contracts.
5. `SENTINEL AND RESUME`: sentinel schema, publication rule, resume decision, force/rerun trigger, and downstream invalidation.
6. `INTERMEDIATE AND PUBLICATION STATE`: temporary paths, atomic publication boundary, cleanup, and concurrency rules.
7. `LOGS AND FAILURE REPORTING`: log artifacts, progress reporting, distinguishing run states, and operator-visible failure messages.
8. `DOWNSTREAM CONSUMER ASSUMPTIONS`: each direct consumer, the properties it depends on, and whether the stage guarantees them.
9. `VALIDATION EVIDENCE`: commands actually run, exit statuses, concise results, checks not run, and impact.
10. `FINDINGS`: blocking findings and non-blocking warnings with location, evidence, consequence, and minimum resolution; write `none` for empty categories.
11. `NEXT STEP`: the minimum design correction, implementation action, validation, or authorization supported by the verdict.

Do not claim a contract element was validated unless the supporting evidence was actually inspected or executed.

## Allowed actions

- Read the stage's code, configuration, sentinels, logs, and representative artifacts within scope.
- Inspect upstream and downstream contracts to the extent required to evaluate this stage's boundary.
- Run local read-only inspection and explicitly authorized safe validation commands.
- Propose contract corrections, implementation actions, or recovery decisions without applying them unless separately authorized.

## Forbidden actions

- Modify the stage's code, configuration, sentinels, or outputs during a contract audit.
- Silently repair sentinel/output disagreements or move failed-run artifacts.
- Treat the existence of a sentinel, a non-empty output, or a successful invocation as proof of contract compliance.
- Rerun, force, retry, or delete outputs without explicit authorization.
- Redesign the pipeline; redirect cross-stage concerns to [`resumable-pipeline-design`](../resumable-pipeline-design/SKILL.md).
- Conceal unrun validation, residual uncertainty, or implicit downstream-consumer assumptions.

## Verdict vocabulary

- `STAGE_CONTRACT_READY`: The stage's identity, inputs, outputs, sentinels, resume, force, intermediate state, atomic publication, logs, column contracts, downstream consumer assumptions, and failure reporting are explicit and consistent with inspected evidence, with no remaining warnings.
- `STAGE_CONTRACT_READY_WITH_WARNINGS`: No blocking finding remains, but substantiated non-blocking limitations or residual risks are explicitly reported.
- `NEEDS_REVISION`: One or more correctable blocking contract findings prevent acceptance.
- `STAGE_CONTRACT_IMPLICIT`: The stage relies on implicit behavior that the contract does not declare, and the implicit behavior materially affects safety, resume, or downstream consumers.
- `BLOCKED`: Missing inputs, inaccessible evidence, unsafe inspection conditions, or unavailable essential validation prevent a reliable conclusion.
- `OUT_OF_SCOPE`: The requested audit, contract change, or stage component exceeds authorized scope.

When several verdicts apply, use `OUT_OF_SCOPE` for unauthorized scope, `BLOCKED` when the audit itself cannot proceed safely, `STAGE_CONTRACT_IMPLICIT` for demonstrated implicit-contract risk, and `NEEDS_REVISION` for correctable blocking findings. Use a ready verdict only when contract elements are explicit and supported by inspected evidence.
