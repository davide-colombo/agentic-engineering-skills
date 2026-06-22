# Agent Instructions

## Scope

These instructions apply to this repository. Keep this file short, stable, and task-agnostic. Put detailed procedures in skills and project-specific facts in the project profile.

## Instruction and evidence model

Apply this canonical model: current task prompt; project profile; selected public skill; local overlay; observed evidence; hooks or scripts for deterministic enforcement. The prompt defines the immediate objective, authorized actions, and task-specific constraints. The profile supplies stable project bindings. The skill supplies the reusable procedure. The overlay may specialize the skill or add stricter rules, but it must not weaken the skill, profile, or prompt unless the current task prompt explicitly authorizes the exception.

On-disk reality is evidence, not a lower-priority instruction. Stop and report when observed state contradicts instructions or assumptions. Hooks and scripts enforce non-negotiable checks at execution time and are not advisory. Stop and report unresolved instruction conflicts.

## Project profile

Load `[PROJECT_PROFILE_PATH]` before work that depends on repository policy, commands, infrastructure, or domain terminology. Treat placeholders or missing required values as unknown, not as permission.

## Volatile state

Keep current branches, commit identifiers, temporary exceptions, job identifiers, current incidents, and transient software behavior in the task prompt or session checkpoint. Verify behavior that may have changed against the installed version or current official documentation.

## Repository workflow

- Source-of-truth branch: `[SOURCE_OF_TRUTH_BRANCH]`
- Protected branches: `[PROTECTED_BRANCHES]`
- State-audit skill: `[REPO_STATE_AUDIT_PATH]`
- Test workflow: `[TEST_WORKFLOW_REFERENCE]`
- Build workflow: `[BUILD_WORKFLOW_REFERENCE]`
- Release workflow: `[RELEASE_WORKFLOW_REFERENCE]`

Run the repository state audit before state-changing work.

## Stop and report

Stop before acting when repository identity or expected state is unclear; protected-branch policy would be violated; unexpected changes may be overwritten; forbidden paths are involved; required authorization is absent; or work requires unauthorized remote access, push, destructive operations, dependency installation, deployment, or long-running execution.

## Reporting minimum

Report the outcome, files changed, validation commands and results, unresolved risks, and final repository status. For blocked work, report the exact condition and the minimum decision needed.
