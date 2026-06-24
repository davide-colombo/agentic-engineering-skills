---
name: remote-execution-safety
description: Use when planning, preparing, inspecting, or performing SSH, remote-shell, remote file, process, transfer, monitoring, or production operations.
---

# Remote Execution Safety

## Purpose

Govern remote access and actions without confusing local and remote state, exceeding authorization, exposing secrets, or applying unsafe commands to remote repositories, processes, files, or production outputs.

## Use cases

Use this procedure for:

- SSH or remote-shell planning and remote command execution.
- Remote repository, environment, process, output, and log inspection.
- Remote process kill or restart requests.
- Remote file move, delete, overwrite, or quarantine requests.
- Synchronization or transfer planning.
- Remote production launch and monitoring support.
- Distinguishing local repository state from remote working-copy state.
- Preparing safe remote commands for a user to run.

This skill governs remote operations. It does not itself authorize network access, remote mutation, process control, transfer, production launch, credentials use, or push.

## Authorization model

Obtain explicit authorization before:

- Opening SSH, a remote shell, or another remote session.
- Running any command on a remote target, including read-only inspection.
- Editing remote files or modifying remote configs.
- Synchronizing or transferring data.
- Launching remote jobs.
- Killing, signaling, or restarting remote processes.
- Deleting, moving, overwriting, or quarantining remote files.
- Installing remote dependencies.
- Changing remote environment, module, container, or resource state.
- Creating, changing, or cleaning production outputs.
- Using remote credentials or secrets.
- Pushing code or tags from a remote machine.

Authorization for one remote action does not imply another. Without remote authorization, inspect local context or prepare commands for user review, but do not connect or perform remote actions. Distinguish permission to provide commands from permission for the agent to execute them.

## Required remote inputs

Identify and record:

- Remote host or execution target and remote user or security context when relevant.
- Local repository path and remote repository or working path.
- Explicit working directory for every command.
- Local branch, HEAD, and status.
- Remote branch, HEAD, and status when the remote path is a repository.
- Remote environment activation, module setup, container, or runtime context.
- Purpose and expected effect of each command.
- Allowed and forbidden remote paths.
- Allowed mutation scope and destructive-action policy.
- Whether the agent may execute commands or may only provide them to the user.
- Network, SSH, credential, and remote-shell authorization.
- Transfer source, destination, direction, authority, and overwrite policy when applicable.
- Process identity and process-control authorization when applicable.

Treat every missing input as unknown. Do not infer a host, path, environment, authorization, or command from local conventions.

## Local and remote state separation

Report local and remote evidence in separate sections. Local state is not evidence of remote state; remote state is not evidence of local state.

Before remote mutation, launch, transfer, or process control, verify and record:

- Local repository path, branch, HEAD, and status.
- Remote current directory and resolved target path.
- Remote path existence and type.
- Whether the remote path is a Git repository.
- Remote branch, HEAD, status, remotes, and relevant diff when applicable and authorized.
- Remote environment or container identity.
- Remote tool and dependency versions when relevant.
- Remote output, log, progress, sentinel, process, writer, and storage state when relevant.

If local and remote revisions differ, state the difference and stop before assuming code, configs, commands, or outputs are interchangeable.

## Procedure

### 1. Establish the remote boundary

1. State the task objective, remote target, action mode, allowed scope, and forbidden actions.
2. Select exactly one primary mode: `COMMAND_PREPARATION`, `REMOTE_INSPECTION`, `REMOTE_PREPARE_AND_HANDOFF_ONLY`, `REMOTE_EXECUTION`, `REMOTE_MONITORING`, `REMOTE_TRANSFER`, or `REMOTE_MUTATION`. For any remote long-running production, scientific, data-processing, extraction, or real-output validation run, default to `REMOTE_PREPARE_AND_HANDOFF_ONLY` unless the current prompt explicitly authorizes the specific run command.
3. Record whether commands will run inside an existing remote shell, be supplied as user-run one-liners, or be executed through authorized agent-side SSH.
4. Separate local facts, remote facts, assumptions, and unknowns.
5. Confirm authorization immediately before any network connection or remote action.

### 2. Inspect read-only before mutation

When remote inspection is authorized, establish:

- `pwd` or equivalent current-directory evidence.
- Target path existence, type, and bounded file or directory inventory.
- Repository identity, branch, HEAD, and status when applicable.
- Process list, process tree, and ownership when relevant.
- Active writers and open files when available.
- Disk, temporary, and scratch space.
- Logs, progress artifacts, checkpoints, and sentinels.
- Environment, runtime, container, module, and tool versions.
- Path ownership and permissions when relevant.

Use the smallest read-only command set that resolves the decision. Inspection authorization does not authorize mutation.

### 3. Construct remote commands safely

- Make the working directory explicit for every command group.
- Make environment, module, or container setup explicit.
- Do not rely on an inherited shell directory, profile, alias, or hidden `cd`.
- Quote paths and arguments for the actual local and remote shell layers.
- Prefer read-only inspection before mutation.
- Split inspection, mutation, launch, monitoring, transfer, and cleanup into separate commands and authorization gates.
- Do not chain destructive actions after inspection commands unless each action and failure behavior is separately authorized.
- Provide plain remote-shell commands when the user will run them inside an existing remote shell.
- Use an SSH-wrapped command only when agent-side SSH execution is authorized or the user explicitly requests a one-liner.
- Show placeholders rather than inventing targets, credentials, paths, or configs.

Record exact commands as prepared or run. A prepared command is not evidence that it executed.

### 4. Gate remote mutation

Stop before mutation when:

- The target or resolved path is ambiguous.
- The path may contain production data and applicable policy is absent.
- Active process, writer, or open-file state is unknown where it matters.
- Downstream consumers or references are unknown.
- The action is destructive or hard to reverse and preservation policy is absent.
- Backup, retention, or quarantine policy is absent where required.
- Transfer direction, authority, or overwrite behavior is ambiguous.
- The command may affect paths outside the allowed scope.
- Observed remote state contradicts local assumptions or supplied state.

After the gate passes, use the narrowest reversible mutation. Re-inspect the target immediately before execution and verify the postcondition afterward.

### 5. Control remote processes

Before kill, signal, or restart, obtain and record:

- PID and stable process or job identity.
- Parent and child process tree.
- Full command line and working directory when available.
- User ownership and privilege context.
- Runtime and elapsed time.
- CPU, memory, I/O, and accelerator indicators where available.
- Logs, progress, checkpoint, and sentinel state.
- Active output writes and affected paths.
- Supported safe shutdown or cancellation mechanism.
- Authorized restart command, environment, resource settings, and output policy.

Prefer a documented graceful mechanism over force. Never kill or restart because CPU is low, a process sleeps, or a log is quiet without phase and progress evidence. Re-check identity immediately before process control because PIDs and job state can change.

### 6. Plan remote sync or transfer

Require:

- Exact source and destination paths.
- Transfer direction and whether local or remote state is authoritative.
- Include and exclude rules.
- Overwrite, delete, conflict, and existing-partial behavior.
- Dry-run support and expected dry-run result.
- Expected inventory, counts, sizes, manifests, or checksums as appropriate.
- Symlink handling and path-containment rules.
- Partial-transfer recovery and retry behavior.
- Post-transfer verification and downstream acceptance criteria.

Run a dry-run first when supported and authorized. Use `data-transfer-and-integrity` for manifest, checksum, partial-transfer, archive, and provenance semantics instead of reproducing its full procedure.

### 7. Govern remote production work

For long-running remote jobs, apply `production-run-launch-and-monitoring` and require explicit launch authorization, observed preflight, resource settings, an approved long-run mechanism, inspectable logs and progress, sentinels, and a monitoring handoff. Use monitoring-only prompts after launch. Do not claim final success before completion evidence and validation exist.

The default remote posture for any long-running production, scientific, data-processing, extraction, or real-output validation run is `REMOTE_PREPARE_AND_HANDOFF_ONLY`. Under this posture:

1. Perform authorized read-only remote inspection and any explicitly authorized deployment, dependency, or configuration setup actions.
2. Verify input, config, environment, hardware, existing session, sentinel, and output-root state required for the run.
3. Stop before initiating the long-running run on the remote target. Do not open a fresh remote channel solely to start the run.
4. Produce exact, ready-to-paste handoff content for the user:
   - Long-run session creation command for the approved terminal multiplexer or detached session mechanism, including session name, working directory, environment activation, resource caps, and log path.
   - Run command to execute inside that session.
   - Detach and reattach instructions for the chosen session mechanism.
   - Read-only monitoring commands and observation cadence.
   - Post-run verification commands to run after independent completion evidence exists.
   - Expected success conditions and stop conditions for the user.

If a prompt combines remote preflight, deployment, setup, or verification with a long-running run command without explicit same-prompt run authorization for that specific command, treat the ambiguity as forbidding the run: complete the preflight, stop before the run, and produce the manual handoff above. Authorization to deploy code, update dependencies, run short bounded validation, or perform read-only inspection is not authorization to launch a long-running remote run.

### 8. Govern remote recovery and reruns

For failed runs or partial outputs, apply `failure-recovery-and-rerun-planning`. Classify failure and output state, inspect active processes and writers, preserve logs and evidence, prefer authorized quarantine to deletion, avoid blind reruns, and resume or rerun only from an evidence-supported safe boundary.

## Security and secrets

- Never print or reproduce secrets, tokens, passwords, private keys, credential files, or sensitive environment values.
- Do not ask the user to paste a secret unless it is essential, an approved secure channel exists, and the value need not enter prompts or logs.
- Do not store credentials in prompts, skills, shell history examples, logs, generated reports, or tracked files.
- Do not expose private hostnames, usernames, domains, or paths in public reusable documentation.
- Use existing secure credential mechanisms only when their use is explicitly authorized.
- If command output appears sensitive, stop displaying it, summarize the non-sensitive finding, and report the exposure risk without reproducing the secret.

## Generic command patterns

Use placeholders and adapt only within authorization. These patterns do not authorize network access or remote execution.

### Local pre-check

```sh
cd <local-repo>
git status --short --branch --untracked-files=all
git rev-parse HEAD
```

### Remote read-only inspection inside an existing remote shell

```sh
pwd
<path-existence-check> <remote-repo>
<bounded-inventory-command> <remote-repo>
<disk-space-command> <output-dir> <scratch-dir>
```

### Remote Git status

```sh
cd <remote-repo>
git status --short --branch --untracked-files=all
git rev-parse HEAD
```

### Remote environment and version check

```sh
cd <remote-repo>
<env-setup>
<environment-identity-command>
<tool> --version
```

### Remote process inspection

```sh
<process-inspection> <process-selector>
<process-tree-inspection> <process-id>
<active-writer-inspection> <output-dir>
<open-file-inspection> <output-dir>
```

### Remote log and progress inspection

```sh
<read-log-tail> <log-file>
<inspect-progress> <progress-artifact>
<inspect-sentinel> <sentinel>
```

### Sync dry-run

```sh
<sync-command> <dry-run-options> <include-exclude-options> <source> <destination>
```

### Authorized remote mutation

```sh
cd <authorized-working-dir>
<recheck-target-state>
<authorized-mutation-command> <authorized-target>
<verify-postcondition> <authorized-target>
```

### SSH-wrapped inspection when explicitly required

```sh
ssh <remote-user>@<remote-host> '<safely-quoted-read-only-command>'
```

## Public/private boundary

Keep reusable content generic. Do not include private hostnames, usernames, absolute paths, scheduler names, repositories, projects, environments, domains, datasets, credentials, tokens, or project-specific commands. Use placeholders such as `<remote-host>`, `<remote-repo>`, `<output-dir>`, `<env-setup>`, and `<command>`. Put private bindings and volatile remote state in an authorized project profile, local overlay, or current task prompt.

## Stop conditions

Stop and report when:

- Remote, network, or SSH authorization is absent for the requested action.
- The remote target, user context, or credential mechanism is ambiguous.
- The remote path is missing, resolves unexpectedly, or is not the expected repository.
- Local and remote branch, HEAD, status, or code assumptions conflict.
- Remote environment or container setup is unknown.
- Command purpose, expected effect, or working directory is unclear.
- Mutation scope or allowed paths are ambiguous.
- A target may contain production data and preservation, overwrite, or retention policy is absent.
- Active process or writer state matters but cannot be determined.
- Kill, signal, or restart is requested without evidence and explicit authorization.
- Transfer direction, authority, include/exclude rules, or overwrite policy is ambiguous.
- Command output appears sensitive.
- The operation requires credentials or secrets that are not already available through an authorized secure mechanism.

Report observed evidence, blocked action, risk, and the minimum authorization or input required. Do not silently choose a host, path, environment, credential, or destructive policy.

## Final report

Produce exactly these sections:

1. `VERDICT`: exactly one verdict and a one-sentence evidence basis.
2. `REMOTE TARGET`: target class, user context, remote paths, command purpose, and action mode without exposing secrets.
3. `AUTHORIZATION BASIS`: network, SSH, command, path, mutation, process, transfer, production, credential, and push boundaries.
4. `LOCAL STATE`: repository path, branch, HEAD, status, environment, and local assumptions.
5. `REMOTE STATE`: current directory, path identity, repository state, environment, tools, storage, and observed unknowns.
6. `COMMANDS PREPARED OR RUN`: exact non-secret commands, executor, working directory, environment setup, timestamps, and outcomes.
7. `OUTPUT / PROCESS / TRANSFER STATE`: outputs, writers, processes, logs, progress, sentinels, inventory, and integrity evidence.
8. `MUTATION / LAUNCH / CLEANUP STATUS`: actions authorized, performed, skipped, blocked, and verified.
9. `RISKS / WARNINGS`: substantiated warnings only; write `none` when empty.
10. `NEXT ACTION`: exactly one bounded next action.
11. `COMMANDS / EVIDENCE APPENDIX`: commands and evidence inspected, distinguishing local from remote and prepared from executed.

## Verdicts

- `REMOTE_INSPECTION_READY`: target, authorization, paths, and read-only commands are established for remote inspection.
- `REMOTE_COMMANDS_READY_FOR_USER`: safe commands are prepared for user execution but were not run by the agent.
- `REMOTE_LONG_RUN_PREPARED_FOR_MANUAL_HANDOFF`: remote preflight, authorized deployment or setup, and state verification completed; exact session creation, run, detach and reattach, monitoring, post-run verification, success-condition, and stop-condition content prepared for the user to execute manually; no long-running remote run launched.
- `REMOTE_EXECUTION_READY`: remote target, authorization, state, environment, command, and scope gates permit execution.
- `REMOTE_MONITORING_READY`: run identity, authorization, read-only evidence paths, and monitoring commands are established.
- `REMOTE_MUTATION_READY_WITH_AUTHORIZATION`: explicit mutation authorization and all target, active-state, preservation, and scope gates pass.
- `REMOTE_EXECUTION_BLOCKED`: a stop condition prevents safe remote work.
- `REMOTE_STATE_AMBIGUOUS`: local or remote evidence cannot establish the target, state, scope, or safe action.
- `REMOTE_EXECUTION_FAILED`: an authorized remote command or its required verification failed.

## Anti-patterns

Do not:

- Assume remote state from local state or local state from remote state.
- Use vague instructions such as “run it on the server.”
- Chain destructive commands after a read-only check.
- Edit remote code directly when the expected workflow is local Git change, review, and controlled synchronization.
- Sync without explicit direction, authority, and overwrite policy.
- Kill jobs because they sleep or use little CPU without phase and progress evidence.
- Delete remote outputs before active-writer and downstream-reference checks.
- Mix remote launch, monitoring, failure recovery, cleanup, and final validation in one prompt.
- Launch a long-running remote production, scientific, or data-processing run when the prompt mixes remote preflight, deployment, setup, or verification with the run command without explicit same-prompt run authorization that names the exact command, expected duration class, resource caps, detach behavior, monitoring behavior, and final-validation boundary.
- Include private remote details in public reusable instructions.
