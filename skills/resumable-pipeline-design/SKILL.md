---
name: resumable-pipeline-design
description: Design, plan, or audit resumable multi-step pipelines for scientific software, data-intensive workflows, batch processing, and long-running computational systems. Use when work needs explicit stage contracts, independently validated checkpoints, safe interruption recovery, atomic outputs, selective reruns, aggregation barriers, or production-readiness evidence.
---

# Resumable Pipeline Design

## Purpose

Determine whether a multi-step pipeline can recover from interruption or failure without silently skipping corrupt work, losing valid results, repeating unnecessary expensive work, or aggregating incomplete inputs. Define or audit explicit work-unit, output, checkpoint, failure, and recovery contracts before declaring the design resumable.

## When to use

Use when designing a new long-running or multi-unit workflow, planning resumability before implementation, auditing an implemented pipeline, diagnosing recovery behavior after failure, or assessing production readiness. Use for local, distributed, scheduled, interactive, or batch execution when work persists across stages or process lifetimes.

## When not to use

Do not use for a single atomic operation with no meaningful intermediate state, as authorization to implement or repair a pipeline, or as a substitute for repository-state, code-review, security, data-governance, or infrastructure review. Do not claim operational readiness when required runtime evidence is unavailable.

## Required inputs

Obtain from the current prompt and authoritative project material:

- Task objective, selected task mode, and allowed scope.
- Pipeline entry and completion conditions.
- Pipeline stages or steps and the unit of work at each stage.
- Required inputs and declared outputs for each stage.
- Existing or proposed resume, force, rerun, and failure behavior.
- Applicable project instructions, acceptance criteria, and validation constraints.

If stages, work units, completion criteria, or scope cannot be established reliably, stop and report. Do not invent project rules absent from the current prompt, project profile, local overlay, or on-disk documentation.

## Optional inputs

Use when supplied or discoverable within scope:

- Dependency graph, execution plan, state machine, or scheduler configuration.
- Output schemas, manifests, checkpoint formats, sentinel definitions, and naming rules.
- Runtime and configuration matrix, storage semantics, and concurrency model.
- Expected data scale, retry policy, cost constraints, and retention policy.
- Failure logs, interrupted-run artifacts, prior recovery records, and operator procedures.
- Existing tests, validation commands, observability requirements, and service-level objectives.

Treat absent evidence as uncertainty, not as proof that recovery is safe.

## Task modes

Choose exactly one mode and state it in the report:

- `DESIGN_REVIEW`: Evaluate a proposed pipeline model and its contracts before implementation.
- `IMPLEMENTATION_PLANNING`: Produce an implementation plan that maps the approved design to concrete state, output, checkpoint, recovery, and validation work without applying changes.
- `POST_CHANGE_AUDIT`: Inspect an implemented change against the pipeline model, scope, failure semantics, and available validation evidence.
- `FAILURE_RECOVERY_AUDIT`: Diagnose interrupted, failed, or inconsistent state and recommend the narrowest safe recovery without performing it unless separately authorized.
- `PRODUCTION_READINESS_AUDIT`: Assess whether implementation and runtime evidence support safe operation, interruption recovery, observability, and aggregation at the intended scale.

A mode changes the audit emphasis, not the authority to modify files, delete state, rerun work, or contact external systems.

## Pipeline model

Model the pipeline as a dependency graph of stages operating on explicit units of work. For each stage and unit, define:

- Required inputs, preconditions, declared outputs, and completion evidence.
- Whether an output may be empty and, if so, how an empty but valid result is distinguished from missing, partial, or corrupted output.
- Deterministic output names and ownership boundaries.
- Temporary paths, atomic publication boundary, cleanup responsibility, and retention behavior.
- Checkpoint or sentinel location, contents, writer, and validation rule.
- Resume decision, forced-rerun decision, and downstream invalidation behavior.
- Local dependencies and cross-unit or cross-stage aggregation barriers.

Use these state terms precisely:

- `missing input`: A required input does not exist or cannot be accessed.
- `missing output`: A declared output expected for completed work does not exist.
- `empty but valid output`: An output contains no records or payload and the project contract explicitly permits that result.
- `corrupted output`: An output exists but fails its schema, integrity, readability, or semantic validation.
- `stale output`: An output is valid in isolation but no longer corresponds to current inputs, configuration, code identity, or dependencies.
- `partial output`: Publication began but the complete output contract was not satisfied.
- `failed unit`: One unit cannot satisfy its stage contract; other independent units may remain usable.
- `failed global precondition`: A shared prerequisite is invalid, so affected pipeline work must not proceed.
- `skipped completed unit`: A unit is not rerun because independently validated completion evidence remains current.
- `forced rerun`: An explicitly requested recomputation that bypasses normal completed-unit skipping under defined invalidation rules.
- `silent repair`: State is changed, deleted, regenerated, or reconciled without reporting the inconsistency and authorized recovery action.
- `explicit operator recovery`: A reported, deliberate recovery action performed under documented authorization and with an auditable result.

## Design procedure

1. Restate the objective, allowed scope, selected task mode, completion criteria, and material unknowns.
2. Enumerate stages and dependencies. Define the smallest practical resumable unit for each stage; do not rely on a final global sentinel alone when smaller resumable units exist.
3. Define each unit's required inputs, declared outputs, validation rules, deterministic names, and empty-output semantics. Do not treat file content emptiness as failure unless the project explicitly defines it as failure.
4. Define state transitions for not started, running, completed, failed, interrupted, stale, and forced rerun. Identify how interrupted runs are detected rather than inferred from absence alone.
5. Define checkpoint or sentinel semantics. Completion evidence must identify the unit and bind to the outputs and material inputs, configuration, code, or dependency versions needed to detect stale state.
6. Define normal resume and force/rerun behavior. Prefer the narrowest safe downstream recovery; do not rerun expensive upstream work when valid upstream outputs can be independently reused.
7. Define temporary-directory, atomic-write, publication, cleanup, and concurrency behavior. Prefer atomic writes over in-place mutation.
8. Define cross-unit and cross-stage aggregation barriers. Do not aggregate across incomplete required units; explicitly define whether failed or optional units may be excluded.
9. Define local and global failure handling, retry boundaries, logging, progress reporting, and operator-visible recovery instructions.
10. Confirm configuration/runtime parity so validation exercises the same state rules, paths, naming, and execution modes used in supported operation.
11. Evaluate idempotence: repeating a unit with identical authoritative inputs must either reproduce the declared result safely or fail loudly without corrupting valid state.
12. Record unresolved design decisions and select a verdict only after applying the validation procedure.

## Resume-state procedure

For every candidate completed unit:

1. Locate its checkpoint and all declared outputs without modifying them.
2. Validate checkpoint structure, unit identity, completion status, and binding to material inputs, configuration, code identity, and dependencies as required by project policy.
3. Validate every declared output independently for presence, schema or format, integrity, completeness, and currentness. Apply the explicit empty-output contract.
4. Compare checkpoint claims with filesystem or storage evidence. Do not silently repair a disagreement.
5. Classify the state as completed and reusable, missing, empty but valid, corrupted, stale, partial, failed, or indeterminate.
6. Skip only a completed unit whose resume state is independently validated. A checkpoint alone is insufficient when its claimed outputs cannot be verified.
7. For invalid or indeterminate state, fail loudly and report the narrowest authorized recovery: rerun the unit, invalidate downstream work, restore verified outputs, or request explicit operator recovery.
8. After recovery, revalidate the unit and every affected dependency before downstream execution or aggregation.

Do not declare a run resumable unless this procedure can distinguish valid completion from corrupted, stale, partial, and inconsistent state.

## Failure semantics

Classify each failure before choosing recovery:

- `LOCAL`: The failure is confined to one unit or independent partition, and unaffected units remain valid under the dependency contract.
- `GLOBAL`: A shared input, configuration, schema, runtime, aggregation barrier, or other global precondition is invalid for all affected work.

Define whether each failure is retryable, requires invalidation, or requires operator action. A failed unit must not be reported as completed. A failed global precondition must stop affected downstream work. Prefer fail-loud behavior over silent repair, and distinguish automated retry from forced rerun and explicit operator recovery in logs and state.

## Output and checkpoint contracts

For each declared output, specify its name, owner, format or schema, valid-empty rule, integrity and completeness checks, publication boundary, and downstream consumers. For each checkpoint or sentinel, specify its schema, atomic creation rule, unit identity, completion evidence, output bindings, provenance fields required for stale-state detection, and invalidation conditions.

Write completion evidence only after every required output has been atomically published and validated. A checkpoint must never convert missing, corrupted, stale, or partial output into apparent success. If transactional publication of several outputs is unavailable, use a manifest or equivalent commit record that becomes visible only after all component outputs are durable.

## Atomicity and partial-state rules

- Write new data to a unique temporary location and publish it atomically when the storage system supports that operation.
- Do not mutate a valid published output in place when replacement can preserve the previous valid version until commit.
- Keep temporary, partial, and published paths distinguishable through deterministic rules.
- Do not silently delete partial outputs; report them and apply only an explicitly authorized cleanup or recovery policy.
- Prevent concurrent attempts from publishing contradictory results for the same unit, or define deterministic conflict resolution that fails visibly.
- Publish the checkpoint after outputs, never before them. Detect the inverse disagreement and stop.
- Define how downstream checkpoints become stale when an upstream input or output changes.

## Validation procedure

1. Inspect the implementation or design against every stage, unit, output, checkpoint, and transition in the pipeline model.
2. Exercise or reason through clean execution, interruption before output, interruption during output, interruption after output but before checkpoint, and checkpoint present with missing or invalid output.
3. Validate missing input, empty but valid output, corrupted output, stale output, partial output, local failure, and failed global precondition behavior.
4. Confirm that normal resume skips only independently validated completed units and that forced rerun follows explicit invalidation rules.
5. Confirm that a downstream-only recovery reuses valid upstream work and that aggregation cannot cross an incomplete required barrier.
6. Test or inspect concurrent execution, retry, idempotence, deterministic naming, temporary-path isolation, atomic publication, and cleanup authorization where relevant.
7. Confirm logging and progress reports distinguish started, completed, skipped, retried, forced, failed, interrupted, and operator-recovered work.
8. Compare validation configuration and runtime behavior with supported operation. Record every command actually run, exit status, environment when material, and result.
9. Demonstrate that resume does not silently skip corrupted, stale, partial, or checkpoint-inconsistent state. If this cannot be demonstrated, the design is not ready.
10. Report tests that cannot run in the current environment as not run, explain the resulting uncertainty, and classify the impact as blocking or non-blocking.

Passing tests are evidence, not proof of resumability. Static inspection alone cannot establish production readiness when credible interruption or storage behavior requires runtime validation.

## Stop-and-report triggers

Stop before implementation, recovery, cleanup, or further execution when:

- The objective, scope, task mode, stages, work units, or completion contract cannot be established.
- Checkpoint claims disagree with output state, or state is corrupted, stale, partial, or indeterminate and no authorized recovery applies.
- A required global precondition or aggregation barrier is incomplete or invalid.
- Recovery would require deleting outputs, broad reruns, silent repair, or scope expansion without authorization.
- Resume validity depends only on a global sentinel or unvalidated existence checks.
- Concurrent writers can corrupt or ambiguously publish the same unit.
- Required validation cannot be performed and the gap prevents a reliable verdict.
- Continued work could conceal failure, overwrite valid output, expose prohibited data, or create unsafe downstream results.

Report the trigger, affected units and stages, evidence, impact, and minimum decision or authorization required. Preserve evidence unless explicit policy authorizes cleanup.

## Output contract

Produce these sections:

1. `VERDICT`: exactly one verdict and a one-sentence rationale.
2. `MODE AND SCOPE`: selected task mode, objective, allowed scope, pipeline boundary, and exclusions.
3. `PIPELINE MODEL`: stages, work-unit granularity, dependencies, required inputs, declared outputs, empty-output rules, and aggregation barriers.
4. `STATE AND RESUME CONTRACT`: checkpoints, validation rules, interrupted-run detection, resume decisions, force behavior, stale-state handling, and downstream invalidation.
5. `FAILURE AND RECOVERY`: local and global failures, retries, partial state, cleanup, silent-repair prohibitions, and operator recovery.
6. `ATOMICITY AND IDEMPOTENCE`: temporary paths, publication strategy, concurrency controls, deterministic naming, repeatability, and residual risks.
7. `VALIDATION EVIDENCE`: commands actually run, exit statuses, concise results, scenarios covered, commands not run, reasons, and impact.
8. `FINDINGS`: blocking findings and non-blocking warnings with location, evidence, consequence, and minimum resolution; write `none` for empty categories.
9. `NEXT STEP`: the minimum design correction, implementation action, validation, recovery decision, or release action supported by the verdict.

Do not claim a state, scenario, or command was validated unless the supporting evidence was actually inspected or executed.

## Allowed actions

- Read the task prompt, project instructions, profiles, overlays, pipeline design, implementation, configuration, logs, tests, and state artifacts within scope.
- Run local read-only inspection and explicitly authorized safe validation commands.
- Model stages, work units, dependencies, contracts, failure states, and recovery decisions.
- Propose implementation, validation, cleanup, or recovery steps without applying them unless separately authorized.
- Report findings, uncertainty, and the minimum authorization or evidence needed.

## Forbidden actions

- Modify files or runtime state during a read-only audit.
- Silently repair checkpoint/filesystem disagreements or conceal inconsistent state.
- Silently delete partial, stale, corrupted, or temporary outputs.
- Broaden scope, rerun work, force completion, retry failures, or perform operator recovery without authorization.
- Treat output existence, content non-emptiness, a final global sentinel, or passing tests alone as proof of completion or resumability.
- Treat empty content as failure without an explicit project contract.
- Aggregate across incomplete required units or allow failed global preconditions to appear local.
- Prefer a broad expensive rerun when a narrower validated recovery is available.
- Invent project rules, supported runtimes, storage guarantees, or completion criteria.
- Conceal unrun validation, destructive recovery requirements, or residual uncertainty.

## Verdict vocabulary

- `RESUMABLE_DESIGN_READY`: The stage, work-unit, output, checkpoint, failure, atomicity, and validation contracts support independently validated safe resume with no remaining warnings.
- `RESUMABLE_DESIGN_READY_WITH_WARNINGS`: The design supports safe resume, but substantiated non-blocking limitations or residual risks remain and are explicitly reported.
- `NEEDS_REVISION`: One or more blocking design or implementation findings have a clear correction before resumability can be accepted.
- `NOT_RESUMABLE`: The observed design cannot distinguish or safely recover completed, interrupted, corrupted, stale, or partial state under its current model.
- `BLOCKED`: Missing inputs, inaccessible evidence, unsafe conditions, or unavailable essential validation prevent a reliable conclusion.
- `OUT_OF_SCOPE`: The requested design, audit, recovery, or material pipeline component exceeds the authorized scope.

When several verdicts apply, use `OUT_OF_SCOPE` for unauthorized scope, `BLOCKED` when evidence cannot support a conclusion, `NOT_RESUMABLE` for a demonstrated fundamental resume-state failure, and `NEEDS_REVISION` for correctable blocking findings. Use a ready verdict only when resume state can be independently validated and no blocking finding remains.
