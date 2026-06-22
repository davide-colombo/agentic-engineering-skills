---
name: failure-recovery-and-rerun-planning
description: Use when investigating failed, partial, interrupted, corrupted, or ambiguous operations and planning evidence-preserving recovery, resume, or rerun boundaries.
---

# Failure Recovery and Rerun Planning

## Purpose

Classify failed or uncertain state, preserve useful evidence, identify reusable intermediates, and produce the narrowest safe recovery plan. Prevent blind reruns, unsafe cleanup, evidence loss, and unsupported recovery claims.

## Use cases

Use this procedure to plan recovery after:

- Failed production or validation runs and failed reruns.
- Interrupted, killed, timed-out, or crashed jobs.
- Partial outputs or corrupted, incomplete, or contract-invalid artifacts.
- Failed commits, integrations, transfers, synchronizations, archives, or checksum checks.
- Ambiguous process, writer, output, checkpoint, or sentinel state.
- Stale or conflicting checkpoints and sentinels.
- User-reported failures that require evidence-based triage.

This skill plans and bounds recovery. It does not itself authorize cleanup, mutation, resume, rerun, relaunch, remote access, or repository changes.

## Recovery authorization model

Obtain explicit authorization before:

- Deleting, moving, or quarantining outputs.
- Overwriting outputs or force-rerunning work.
- Resuming from a checkpoint.
- Changing config or resource settings.
- Killing, signaling, or restarting processes.
- Editing recovery scripts.
- Using remote infrastructure, network access, or SSH.
- Synchronizing or transferring data.
- Committing recovery changes.
- Changing durable documentation.

Authorization for one action does not imply another. Without required authorization, inspect read-only and propose a recovery plan, but do not mutate state. Record the exact authorized paths, actions, commands, and limits.

## Required recovery inputs

Identify and record:

- Repository path, branch, HEAD, and observed repository state.
- Failed command or operation and its working directory.
- Expected command, configs, environment, and resource settings when known.
- Run and output directories.
- Log, progress, sentinel, checkpoint, temporary, and scratch paths.
- Expected outputs, output contracts, and validation criteria.
- Active process, writer, session, or scheduler state.
- Allowed mutation scope and forbidden paths.
- Overwrite, resume, force, and rerun policy.
- Available validation evidence.
- Downstream consumers, published references, and dependency boundaries.
- The user's desired endpoint: diagnosis, plan, resume readiness, rerun readiness, or validated recovery.

Treat missing inputs as unknown. Do not infer authorization or safe state from absence of evidence.

## Procedure

### 1. Establish scope and preserve initial evidence

Before recovery mutation:

1. Capture repository branch, HEAD, status, relevant diff or commit range, and task authorization.
2. Record the exact failed command or operation, exit state, timestamps, run identity, working directory, and environment when observed.
3. Preserve logs, failure messages, progress records, sentinels, checkpoints, manifests, and validation output.
4. Identify the failure phase when evidence permits: input, setup, launch, execution, checkpoint, finalization, transfer, integration, or validation.
5. Record timestamps and checkpoint positions only as observed evidence; do not invent ordering or causality.
6. Do not clean, move, quarantine, rewrite, or delete partial outputs before classification.
7. Do not rerun before determining whether partial state is reusable, invalid, actively written, or hazardous.

Preservation does not authorize copying or moving evidence. When preservation requires mutation, stop and obtain authorization first.

### 2. Inspect active state

Before cleanup, quarantine, resume, or rerun, inspect available evidence for:

- Active processes and relevant process trees.
- Active writers and open files when inspection is available.
- Log growth and recent errors or warnings.
- Progress-artifact updates.
- Temporary and scratch usage or pressure.
- File timestamps, sizes, and growth across time-separated observations.
- Lock files and their ownership or freshness.
- Scheduler, detached-session, or terminal-multiplexer state where relevant.

Do not declare a run failed, stalled, safe to delete, or safe to rerun without active-state evidence. If active state matters but cannot be determined, classify it as ambiguous and stop before mutation.

### 3. Classify the failure

Assign one primary failure class and retain secondary contributing evidence:

- `input missing or unreadable`
- `config, schema, or environment error`
- `dependency or tool failure`
- `resource exhaustion`
- `permission or filesystem error`
- `timeout or interruption`
- `process killed or crashed`
- `partial output with valid checkpoint`
- `partial output without valid checkpoint`
- `completed but validation failed`
- `output contract mismatch`
- `transfer, archive, or checksum failure`
- `stale checkpoint or sentinel disagreement`
- `unknown or ambiguous failure`

Distinguish confirmed cause, likely cause, contributing condition, symptom, and unknown. A single log line, exit code, missing sentinel, or resource metric rarely establishes root cause alone.

### 4. Classify every relevant output

Classify outputs, intermediates, checkpoints, sentinels, and temporary state as exactly one of:

- `valid reusable intermediate`
- `invalid partial state`
- `valid-empty output`
- `missing output`
- `unknown or ambiguous output`
- `final output needing validation`
- `stale output from previous run`

Base classification on the declared contract, provenance, writer state, integrity evidence, and dependencies. Preserve partial state by default. If quarantine is authorized, preserve names, relative structure, provenance, logs, timestamps where required, and a mapping from original to quarantine location. Quarantine is isolation, not proof that an artifact is invalid or safe to delete.

### 5. Identify the safe recovery boundary

Determine and record:

- The last verified valid stage, unit, checkpoint, commit, transfer boundary, or artifact.
- The first failed or unverified boundary.
- Whether resume is supported and how checkpoint validity is established.
- Which intermediates may be reused and which outputs must be regenerated.
- Which checkpoints or sentinels remain trustworthy and which require authorized invalidation.
- Whether config, environment, dependency, permission, storage, or resource changes are required.
- Whether downstream consumers must be paused, isolated, or revalidated.
- Whether a targeted retry, resume, partial rerun, full rerun, rollback, or no action is safest.

Prefer the narrowest recovery that preserves correctness and evidence. Do not prefer resume merely because a checkpoint exists, or a full rerun merely because it is simpler.

### 6. Prepare the resume or rerun plan

The plan must state:

1. Preconditions and the evidence that satisfies each one.
2. Exact safe restart boundary.
3. Reused, regenerated, quarantined, retained, and forbidden artifacts.
4. Checkpoint and sentinel trust or invalidation decisions.
5. Required config, environment, tool, permission, storage, or resource corrections.
6. Exact command only when resume, rerun, or launch is explicitly authorized.
7. Output, log, progress, checkpoint, and sentinel destinations.
8. Active-state and downstream-consumer rechecks immediately before execution.
9. Monitoring and stop criteria.
10. Post-rerun validation and evidence needed to claim recovery.

Use `production-run-launch-and-monitoring` for authorized relaunch and monitoring. Planning a command is not authorization to execute it.

### 7. Apply rerun safety gates

Block resume or rerun when:

- An active process or writer conflict exists.
- Output state or ownership is ambiguous.
- Overwrite, reuse, or resume policy is missing.
- The failure cause is unknown and likely to recur.
- Inputs, configs, environment, dependencies, or permissions remain invalid.
- Resource limits or temporary-space requirements remain unresolved.
- Downstream consumers may read inconsistent outputs.
- Rerun, overwrite, cleanup, or quarantine would erase evidence.
- Launch, restart, resume, force, or rerun authorization is absent.

Report the blocked action, evidence, consequence, and minimum decision or correction required.

### 8. Validate after recovery

Validate from the repaired boundary through every affected downstream contract. Check expected outputs, valid-empty semantics, sentinels, checkpoints, manifests, integrity, logs, warnings, and downstream readiness. Keep execution completion distinct from validated recovery.

## Related skills

- Use repository-state audit before modifying repository state.
- Use `resumable-pipeline-design` to interpret or design checkpoint, sentinel, stage, and selective-rerun semantics.
- Use `production-run-launch-and-monitoring` to authorize, launch, and monitor a recovery run.
- Use `data-transfer-and-integrity` for transfer, synchronization, archive, manifest, or checksum failures.
- Use `configuration-and-environment-integrity` for config, dependency, tool, or environment failures.

Apply the relevant procedure rather than duplicating its full audit. This recovery skill integrates their evidence into one bounded recovery decision.

## Evidence and claim discipline

- Claim `fixed` only after the applicable validation passes.
- Claim `safe to rerun` only after active-state, output-state, downstream, and overwrite-policy evidence passes.
- Claim `safe to delete` only after active-writer and downstream-reference checks pass and deletion is authorized.
- Claim `completed` only when sentinel, output-contract, or terminal-log evidence supports it.
- Claim `root cause` only when evidence establishes causality; label weaker conclusions `likely cause`.
- Distinguish observed facts, interpretations, assumptions, and missing evidence.
- Preserve failed validation results and disclose skipped or unavailable checks.

## Generic command patterns

Use placeholders and adapt only within authorization. These patterns do not authorize mutation or execution.

### Inspect repository state

```sh
cd <repository>
git status --short --branch --untracked-files=all
git rev-parse HEAD
git log --oneline -n <count>
```

### Inspect logs, progress, and sentinels

```sh
<read-log-tail> <log-file>
<inspect-progress> <progress-artifact>
<inspect-checkpoint> <checkpoint>
<inspect-sentinel> <sentinel>
```

### Inspect active processes and writers

```sh
<process-inspection> <run-selector>
<process-tree-inspection> <run-identifier>
<active-writer-inspection> <output-directory>
<open-file-inspection> <output-directory>
```

### Classify outputs

```sh
<list-output-metadata> <output-directory>
<validate-output-contract> <output>
<verify-integrity> <output>
<inspect-downstream-references> <output>
```

### Quarantine partial output when authorized

```sh
<quarantine-command> <partial-output> <quarantine-directory>
<record-quarantine-mapping> <partial-output> <quarantine-directory> <provenance-record>
```

### Prepare rerun command when authorized

```sh
cd <working-directory>
<environment-activation>
<resource-caps> <executable> --config <config> <resume-or-rerun-options>
```

### Verify post-rerun status

```sh
<inspect-active-state> <run-identifier>
<inspect-sentinel> <completion-sentinel>
<read-log-tail> <log-file>
<validate-output-contract> <output-directory>
```

## Public/private boundary

Keep reusable instructions generic. Do not include private paths, project names, repositories, datasets, hostnames, clusters, scheduler names, environments, pipeline names, config filenames, credentials, or project-specific commands. Put private bindings and current failure state in an authorized project profile, local overlay, or task prompt. Use placeholders in public command patterns.

## Stop conditions

Stop and report when:

- Required recovery authorization is absent for a mutation.
- The repository, run, output, quarantine, or working path is ambiguous.
- Branch, HEAD, repository state, or run identity contradicts assumptions.
- Active process or writer state matters but cannot be determined.
- Partial output, checkpoint, sentinel, or provenance classification remains ambiguous.
- A proposed action would destroy logs, failed validation, or other evidence.
- Quarantine, deletion, overwrite, resume, or rerun would touch forbidden paths.
- Downstream consumers or dependencies are unknown where consistency matters.
- Remote or network access is required but not authorized.
- Launch, restart, kill, signal, resume, or rerun is needed but not authorized.
- Required validation evidence or an output contract is missing.

Continue read-only inspection only when it is authorized and can reduce uncertainty without mutation. Otherwise report the evidence gap and minimum authorization or input needed.

## Final report

Produce exactly these sections:

1. `VERDICT`: exactly one verdict and a one-sentence evidence basis.
2. `FAILURE TARGET`: failed command or operation, run identity, paths, expected result, and desired endpoint.
3. `AUTHORIZATION BASIS`: authorized and forbidden inspection, mutation, remote, resume, rerun, and repository actions.
4. `REPOSITORY / ENVIRONMENT STATE`: repository, branch, HEAD, status, configs, environment, tools, and resources.
5. `FAILURE EVIDENCE`: phase, classification, confirmed and likely causes, logs, errors, timestamps, and validation evidence.
6. `ACTIVE STATE`: processes, writers, open files, locks, progress, sessions, and ambiguity.
7. `OUTPUT STATE`: classification, contracts, provenance, checkpoints, sentinels, partial state, and downstream references.
8. `RECOVERY PLAN`: ordered preservation, correction, isolation, and safe-boundary actions.
9. `RERUN / RESUME PLAN`: preconditions, reusable state, invalidation, exact authorized command, monitoring, and stop criteria.
10. `RISKS / WARNINGS`: substantiated warnings only; write `none` when empty.
11. `VALIDATION PLAN`: exact checks, success criteria, and claim boundary.
12. `NEXT ACTION`: exactly one bounded next action.
13. `COMMANDS / EVIDENCE APPENDIX`: exact commands run and evidence inspected, separating observations from assumptions.

## Verdicts

- `RECOVERY_PLAN_READY`: a complete evidence-supported recovery plan exists without material unresolved warnings.
- `RECOVERY_PLAN_READY_WITH_WARNINGS`: a usable plan exists, but named non-blocking risks or uncertainties remain.
- `RECOVERY_INSPECTION_ONLY`: read-only classification or planning was completed, but mutation was not authorized.
- `RECOVERY_RERUN_READY`: active-state, output-policy, cause-correction, authorization, command, and validation gates permit resume or rerun.
- `RECOVERY_BLOCKED`: a stop condition prevents a safe plan or authorized action.
- `RECOVERY_FAILED`: an authorized recovery action or its required validation failed.
- `RECOVERY_STATE_AMBIGUOUS`: evidence cannot safely classify the failure, active state, outputs, or recovery boundary.

## Anti-patterns

Do not:

- Delete partial outputs before classification.
- Rerun blindly or overwrite outputs without policy.
- Treat a missing sentinel as proof of failure without logs and process state.
- Treat process exit as proof of valid completion.
- Change configs and rerun in one step without recording the change.
- Hide failed validation or unavailable checks.
- Claim a root cause from a single symptom.
- Mix recovery planning with destructive cleanup.
- Mix recovery planning with production relaunch unless explicitly authorized.
- Put private paths or project-specific commands in public reusable instructions.
