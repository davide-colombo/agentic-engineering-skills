---
name: production-run-launch-and-monitoring
description: Use when planning, authorizing, launching, monitoring, intervening in, or validating long-running production jobs that require explicit controls, observable progress, and evidence-based state claims.
---

# Production Run Launch and Monitoring

## Purpose

Plan, authorize, launch, and monitor long-running production jobs without unsafe mutation or unsupported claims. Require observed preflight evidence, bounded resources, inspectable logs and progress, safe partial-state handling, and an explicit monitoring handoff.

## Use cases

Use this procedure for:

- Launching long-running production jobs or preparing launch-only prompts.
- Validating preflight readiness before a production run.
- Monitoring an active run or checking progress without interfering.
- Recording commands, configs, outputs, logs, resource settings, and provenance.
- Deciding whether evidence supports continuing, pausing, or stopping.
- Managing generic terminal multiplexers, detached sessions, `nohup`-style execution, or batch schedulers.
- Inspecting active processes and writers before rerun, recovery, or cleanup.
- Reporting current production state without implying final validation before completion.

This skill controls operations; it does not itself authorize them or replace workload correctness, configuration, resumability, hardware, security, or domain validation.

## Authorization model

Obtain explicit authorization for every applicable action before:

- Launching a long-running job or running on remote infrastructure.
- Using network access, SSH, or another remote-control mechanism.
- Modifying production configs or changing resource settings.
- Creating or overwriting production outputs.
- Deleting, moving, or quarantining outputs.
- Killing, signaling, or restarting processes.
- Resuming from a checkpoint or force-rerunning work.
- Pushing code or tags as part of a launch.

Authorization for one action does not imply another. Monitoring authority is read-only by default. If required authorization is absent, stop and report the action, evidence, risk, and exact authorization needed.

## Required launch inputs

Identify and record:

- Repository path, branch, HEAD, repository state, executable command, and working directory.
- Config files and the environment, modules, or container with versions.
- Output, log, temporary, and scratch directories.
- Expected sentinels or checkpoints and expected progress artifacts.
- Expected runtime class and resource budget.
- Thread and process topology, including hidden pools and hardware constraints.
- Input-data readiness and provenance.
- Overwrite and resume policy.
- Monitoring cadence and the responsible observer.
- Stop and alert criteria.
- Final report and post-completion validation expectations.

Treat missing required input as unknown, not as permission to infer a production value.

## Procedure

### 1. Establish mode and scope

Select one mode: `PREFLIGHT_ONLY`, `LAUNCH_ONLY`, `MONITORING_ONLY`, `FAILURE_TRIAGE`, `RECOVERY_PLANNING`, or `FINAL_VALIDATION`. Record the authorized actions, forbidden actions, target run identity, evidence sources, and completion boundary.

### 2. Run preflight checks

Before launch, verify and record:

- The repository state is clean, or observed dirtiness is explicitly allowed; branch and HEAD match assumptions and the code version is known.
- The environment is active, identified, and versioned.
- The command supports and passes dry-run or preflight behavior when applicable.
- Each config parses, its precedence is known, and resolved values match runtime behavior.
- Input files exist, are readable, and are ready for the requested scope.
- The output policy prevents accidental reuse, overwrite, or collision.
- No incompatible active job is running and no active writers use target outputs.
- Existing outputs are absent, proven resumable, or intentionally reused under explicit policy.
- Temporary and scratch capacity is sufficient for the bounded run.
- Logs, progress artifacts, and completion sentinels or checkpoints will be written to inspectable paths.
- The hardware and resource budget is observed or explicitly supplied.
- Thread, process, subprocess, and hidden library pools are capped where relevant.

Preflight evidence must describe what was actually observed. Config parsing alone does not prove runtime consumption; process absence alone does not prove output safety.

### 3. Launch

Launch only after preflight passes and explicit authorization covers the command and its side effects.

- Record the exact launch command before execution.
- Make the working directory and environment activation explicit.
- Set explicit thread, process, memory, accelerator, scheduler, and I/O caps when relevant.
- Use distinct, inspectable output, log, progress, checkpoint, and sentinel paths.
- Use an approved long-run mechanism when an interactive session is not expected to remain safe.
- Capture a stable run identifier such as a scheduler job ID, session name, or process identifier, plus start time.
- Record repository, config, environment, input, command, and resource provenance.
- If the run may outlive the session, report exact read-only inspection commands and monitoring cadence.

A launch-only prompt may claim readiness or launch, never final completion or success. If launch returns no stable identity or observability evidence, classify the state as ambiguous and stop.

### 4. Monitor read-only

Monitoring must remain read-only unless a separate intervention is explicitly authorized. At each observation, inspect available evidence for:

- Process existence and process tree where relevant.
- Elapsed time and phase-relative expected duration.
- CPU, memory, I/O, and accelerator indicators where available.
- Log growth and recent warnings or errors.
- Progress artifacts, sentinels, and checkpoints.
- Output-file existence, size, and growth.
- Active writers to target and temporary paths.
- Disk usage and temporary or scratch pressure.

Classify the current state as exactly one of:

- `running`: the job exists, but available evidence does not yet establish useful progress.
- `progressing`: process, log, progress, checkpoint, or output evidence shows expected forward movement.
- `idle but expected`: low activity matches a documented wait, queue, synchronization, or phase behavior.
- `stalled`: multiple time-separated observations contradict expected progress while the job remains present.
- `failed`: process, scheduler, log, sentinel, or output evidence identifies a terminal failure.
- `completed`: completion evidence exists, but final validation has not established success.
- `completed-with-warnings`: completion evidence exists with material warnings requiring disclosure or review.
- `unknown/ambiguous`: evidence is missing, conflicting, stale, or insufficient for another state.

Do not equate silence, low CPU, process exit, or output presence alone with stalled, failed, completed, or successful state.

### 5. Intervene only after a new gate

Stop and report before killing or restarting processes, changing parallelism, deleting or quarantining outputs, cleaning temporary files, modifying configs, resuming a checkpoint, or forcing a rerun. Proceed only when explicit authorization names the intervention and evidence establishes its safe boundary.

Before intervention, re-check run identity, process tree, active writers, downstream references, checkpoints, outputs, logs, resource state, and the consequences of interruption. Prefer the smallest reversible action supported by evidence.

### 6. Handle failure and partial state

1. Classify the failure phase: preflight, launch, queue/startup, execution, checkpoint, finalization, or validation.
2. Preserve logs and partial outputs until their status is classified.
3. Verify active writers before moving, removing, or reusing anything.
4. Distinguish reusable intermediates and valid checkpoints from corrupt, incomplete, or unknown partial state.
5. Identify the last verified safe boundary and the first unverified unit.
6. Prefer bounded resume or targeted rerun when correctness evidence supports it; do not default to a full rerun.
7. Avoid cleanup, recovery mutation, resume, or rerun without explicit authorization.

Report the exact safe boundary, retained evidence, affected outputs, remaining uncertainty, and prerequisites for recovery planning.

### 7. Validate after completion

Perform final validation only after independent completion evidence exists. Validate expected outputs, completeness, integrity, warnings, and workload-specific acceptance criteria. Keep `completed` distinct from `successful` until validation passes.

## Long-run prompt separation

Use separate prompts for:

1. Launch-only.
2. Monitoring-only.
3. Failure triage.
4. Recovery or rerun planning.
5. Final validation after completion.

Do not ask an agent to launch a long-running job and also claim final validation in the same prompt unless the job is demonstrably bounded and completes within the session. Do not combine launch, recovery, cleanup, and final validation authority.

## Evidence rules

- Claim `completed` only when a completion sentinel, expected output contract, or terminal log evidence supports it.
- Claim `successful` only when explicit validation evidence supports it.
- Claim `stalled` only from time-separated process, log, progress, or output evidence interpreted against the expected phase.
- Claim `safe to delete` only after active-writer and downstream-reference checks pass.
- Claim resource efficiency only from observed metrics against a stated budget and workload phase.
- Record commands, paths, timestamps, run identifiers, config identities, code revision, environment identity, resource settings, and evidence sources exactly.

## Generic command patterns

Use placeholders and adapt only within authorization. These patterns are not authorization to execute.

### Preflight inspection

```sh
cd <repository>
git status --short --branch --untracked-files=all
git rev-parse HEAD
<environment-inspection-command>
<executable> --config <config> --preflight
<active-process-inspection> <run-selector>
<active-writer-inspection> <output-directory>
```

### Launch in an approved long-run session

```sh
cd <working-directory>
<environment-activation>
<resource-caps> <long-run-mechanism> <executable> --config <config> > <log-file> 2>&1
```

### Monitor process, logs, and progress

```sh
<process-inspection> <run-identifier>
<process-tree-inspection> <run-identifier>
<read-log-tail> <log-file>
<inspect-progress> <progress-artifact>
<disk-usage-inspection> <output-directory> <scratch-directory>
```

### Verify completion sentinel

```sh
<inspect-sentinel> <completion-sentinel>
<read-log-tail> <log-file>
<validate-outputs> <output-directory>
```

### Record provenance

```text
repository=<repository> branch=<branch> head=<head>
command=<exact-command>
config=<config-identities> environment=<environment-identity>
inputs=<input-provenance> outputs=<output-directory>
resources=<resource-settings> run_id=<run-identifier> started_at=<timestamp>
```

## Public/private boundary

Keep public reusable content project-agnostic. Do not include private paths, repositories, clusters, environments, hostnames, datasets, pipeline names, config filenames, credentials, or scheduler brands. Use placeholders and generic mechanism classes. Put private bindings and volatile production state in an authorized project profile, local overlay, or current task prompt.

## Stop conditions

Stop and report when:

- Launch authorization is absent.
- Branch, HEAD, repository state, or run identity contradicts assumptions.
- The command, config, environment, working directory, or target paths are ambiguous.
- Dry-run or preflight fails.
- Input readiness or output overwrite, reuse, or resume policy is unsafe.
- An incompatible active process or active writer conflict exists.
- The resource budget is unknown for a high-cost run or hidden pools are uncontrolled.
- Logs, progress artifacts, checkpoints, or sentinels are not inspectable.
- Monitoring would require mutation.
- Intervention is required but not authorized.
- Failure or partial state cannot be classified safely.
- Remote or network access is required but not authorized.

State the evidence, blocked action, risk, and minimum authorization or correction required. Do not repair assumptions by silently changing production state.

## Final report

Produce exactly these sections:

1. `VERDICT`: exactly one verdict and a one-sentence evidence basis.
2. `RUN TARGET`: objective, mode, command identity, working directory, and run identifier.
3. `AUTHORIZATION BASIS`: authorized and forbidden actions, including remote and mutation boundaries.
4. `REPOSITORY / ENVIRONMENT STATE`: repository, branch, HEAD, status, environment, and config identities.
5. `PREFLIGHT`: checks, observed results, failures, and unresolved unknowns.
6. `LAUNCH OR MONITORING ACTIONS`: exact actions performed, timestamps, and skipped actions.
7. `RESOURCE SETTINGS`: limits, topology, hardware constraints, and observed metrics.
8. `OUTPUT / LOG / PROGRESS PATHS`: outputs, logs, temporary paths, sentinels, checkpoints, and progress artifacts.
9. `CURRENT RUN STATE`: one monitoring state with supporting evidence.
10. `RISKS / WARNINGS`: substantiated warnings only; write `none` when empty.
11. `NEXT ACTION`: exactly one bounded next action.
12. `COMMANDS / EVIDENCE APPENDIX`: exact commands run and evidence inspected, distinguishing observed results from assumptions.

## Verdicts

- `PRODUCTION_RUN_READY_TO_LAUNCH`: preflight passes and launch authorization exists, but no launch occurred.
- `PRODUCTION_RUN_LAUNCHED`: launch occurred, a stable run identity and inspectable evidence exist, but progress is not yet established.
- `PRODUCTION_RUN_RUNNING`: the run exists and monitoring evidence classifies it as running, progressing, or idle but expected.
- `PRODUCTION_RUN_COMPLETED_VALIDATION_PENDING`: completion evidence exists, but final validation is incomplete.
- `PRODUCTION_RUN_COMPLETED_VALIDATED`: completion and explicit final-validation evidence both pass.
- `PRODUCTION_RUN_BLOCKED`: a stop condition prevents safe launch, monitoring, intervention, or validation.
- `PRODUCTION_RUN_FAILED`: evidence establishes a terminal failure and its known phase.
- `PRODUCTION_RUN_STATE_AMBIGUOUS`: available evidence cannot support a safer specific state or verdict.

## Anti-patterns

Do not:

- Launch without explicit authorization.
- Use production outputs as scratch space.
- Run expensive jobs from dirty code without an explicit policy.
- Rely on hidden or default thread pools.
- Overwrite existing outputs without an explicit policy.
- Claim completion from process exit alone.
- Treat no recent log line as failure without phase and timing context.
- Kill or restart because CPU appears low without phase evidence.
- Delete partial outputs before classification and active-writer checks.
- Mix launch, recovery, cleanup, and final validation in one prompt.
- Hide exact commands or config paths from the final report.
