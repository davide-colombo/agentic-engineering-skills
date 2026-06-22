---
name: cross-session-handoff-and-continuity
description: Use when closing, resuming, or transferring coding-agent work across chats, tools, or runs while preserving verified repository state, evidence, blockers, decisions, and one executable next action.
---

# Cross-Session Handoff and Continuity

## Purpose

Produce a compact, evidence-based handoff that another agent can use without hidden chat memory. Preserve completed work, current repository state, validation and audit evidence, blockers, authorization boundaries, and the exact next decision while separating verified facts from assumptions and plans.

## Use cases

Use for:

- Resuming work in a new chat or session.
- Transferring context from ChatGPT to Codex or Claude Code, or between other coding-agent tools.
- Transferring context from one coding-agent run to another.
- Summarizing a completed implementation, audit, integration, or release cycle.
- Continuing after a blocked or failed run.
- Preserving continuity across long-running projects.
- Recording what was committed, merged, pushed, tagged, or intentionally not done.
- Preparing the exact next prompt or decision point.

Create a handoff at a meaningful boundary: completed commit, audit verdict, integration result, validation failure, blocked action, monitoring checkpoint, or user decision.

## Evidence-first rule

Classify every material statement as one of:

- `OBSERVED FACT`: Directly inspected current state.
- `COMMAND EVIDENCE`: Command, exit status, and relevant result.
- `INSPECTED PATH`: File or artifact actually read.
- `COMMITTED STATE`: Content proven reachable from an identified commit.
- `UNCOMMITTED STATE`: Staged, unstaged, untracked, ignored, generated, or local-only content.
- `USER INSTRUCTION`: Supplied objective, policy, authorization, or expected state.
- `ASSUMPTION`: Unverified condition required for planning.
- `INFERENCE`: Conclusion derived from identified evidence.
- `UNRESOLVED QUESTION`: Missing decision or evidence.
- `PLANNED`: Proposed but unimplemented work.

Do not present memory, assumptions, prior summaries, user-provided roadmap claims, remote-tracking references, or planned work as verified repository state. Verify on disk or label the statement. A prior agent report is evidence of what was reported, not independent proof that the reported action occurred.

When evidence conflicts, preserve the conflict and prefer current observed state for the handoff. Do not silently reconcile or repair it.

## Required handoff inputs

Collect or explicitly report as unavailable:

- Repository path.
- Current branch and exact HEAD.
- Full status, including staged, unstaged, untracked, and relevant ignored or local-only files.
- Relevant commits and messages.
- Changed files and comparison range.
- Validation commands, exit statuses, and outcomes.
- Audit targets and verdicts.
- Local merge, remote push, tag, and release state.
- Current blockers and failed checks.
- Allowed and forbidden next actions.
- Relevant documentation, skills, project profile, and local overlay paths.
- Exact next task or decision point.
- Constraints and accepted warnings that must survive into the next session.

Write `not supplied`, `not inspected`, `not authorized`, or `not applicable` rather than omitting a material field or guessing.

## Handoff procedure

1. Define the handoff boundary and objective: completed, blocked, failed, paused, or awaiting decision.
2. Re-read applicable current instructions, selected skills, profile, and overlay. Record their paths and roles without copying unnecessary text.
3. Capture repository and operational state using the checks below.
4. Establish the exact commit or range associated with completed work and inspect changed-file scope.
5. Reconcile implementation, validation, audit, integration, push, tag, and cleanup claims with direct evidence.
6. Separate committed, uncommitted, ignored, generated, local-only, and remote state.
7. Record blockers, failures, partial state, active processes, missing evidence, and actions intentionally not performed.
8. Construct exactly one recommended next action unless the user requests alternatives.
9. Apply the public/private boundary and remove unsupported or unnecessary private detail.
10. Produce the required structure and perform a final facts-versus-assumptions check.

Do not change repository, process, remote, or output state merely to make the handoff cleaner unless the current task separately authorizes that action.

## Repository-state capture

Verify before writing the handoff:

- Repository root and identity.
- Current branch or detached-HEAD state.
- Exact HEAD.
- `git status`, including staged, unstaged, and untracked paths.
- Recent relevant commits and their messages.
- Tags at HEAD when tag or release state matters.
- Ignored and local-only files when they affect continuation.
- Existence and HEADs of relevant feature and protected branches.
- Whether the completed range is merged into the expected protected branch.
- Whether a push occurred, only when relevant and supported by observed evidence.

Use local read-only inspection by default. Do not contact a remote solely to strengthen a handoff unless network access is explicitly authorized and current remote state is necessary. Mark local remote-tracking references as potentially stale. A configured upstream or matching local tracking reference does not prove that a push occurred.

If a long-running process matters, record only directly observed process identity, status, start evidence, logs, output location, writer risk, and monitoring boundary. Do not claim future completion.

## Completed-work summary

State:

- What was actually implemented, reviewed, audited, validated, integrated, or documented.
- Full commit hashes and exact commit messages.
- Files changed by the relevant commit or range.
- Validation commands that passed and their observed outcomes.
- Audit target, evidence boundary, and verdict.
- What was merged and into which local branch.
- What remains local only, unmerged, unpushed, untagged, or unpublished.
- What was intentionally not done because it was forbidden, unnecessary, deferred, or not requested.

Distinguish a created commit from a merged commit, a local merge from a pushed branch, a local tag from a pushed tag, and a pushed tag from a published release.

## Blocked or failed work summary

State:

- Exact blocker or failed validation.
- Last safe completed step and where the agent stopped.
- Files, refs, processes, outputs, or remotes not modified.
- Partial changes, outputs, branches, commits, or processes that exist.
- Whether cleanup is needed and whether it is authorized.
- Commands, outputs, paths, or policy supporting the blocker.
- Minimum next safe action, evidence, correction, or user decision.

Do not compress a failure into “did not work.” Preserve the failing command, exit status, concise error, affected scope, and resulting uncertainty. Do not prescribe cleanup as performed work.

## Next-action construction

Include exactly one recommended next action unless alternatives are requested. Specify:

- Target repository.
- Expected branch and HEAD or base assumption.
- Single objective.
- Allowed files or inspection scope.
- Forbidden files and actions.
- Required validation and success criteria.
- Whether implementation, audit, merge, push, tag, remote execution, process control, transfer, or cleanup is authorized.
- Stop conditions for state mismatch, missing evidence, validation failure, or unauthorized side effects.

When the next action is a coding-agent prompt, make it runnable without unshared memory. Include every volatile fact and authorization needed, require fresh on-disk verification, and identify the selected skill or private binding when applicable. Do not embed several independent lifecycle steps in one next action.

## Continuity risks

Warn explicitly when applicable:

- Branch, HEAD, tag, process, output, or remote information may be stale.
- Commits are unaudited or an audit applies to a different range.
- Feature branches remain unmerged.
- The protected branch remains unpushed or remote state is unverified.
- Dirty, ignored, generated, or local-only files may affect continuation.
- Required validation evidence is missing, partial, reported-only, or failed.
- Output provenance, completion, or active-writer state is ambiguous.
- Volatile task state was placed in durable documentation.
- Future roadmap language could be mistaken for implemented state.
- Private information could leak into a public handoff.

Do not list generic risks without evidence. State the affected claim, evidence gap, consequence, and minimum verification needed.

## Public/private boundary

For public handoffs:

- Exclude private absolute paths, repository names, infrastructure, hosts, credentials, secrets, unpublished data, and user-specific project facts.
- Use generic placeholders when a reusable public artifact needs a path, identity, or environment binding.
- Include only repository facts intended for public disclosure.

For private handoffs:

- Mark private project bindings explicitly.
- Keep credentials and secrets out of the handoff even when the handoff is private.
- Store private paths, infrastructure, current operational state, and project-specific policy in the private handoff, profile, or overlay—not in a public skill file.

If the intended audience or publication boundary is unclear, stop and request classification before exposing sensitive detail.

## Compact handoff formats

Use the common final structure below and apply the indicated emphasis.

### Implementation-complete handoff

Emphasize objective, commit hash and message, changed files, validation evidence, audit status, local-only state, actions intentionally not performed, and the independent audit or integration next action.

### Read-only audit handoff

Emphasize immutable audit target and base, repository state, inspected paths, commands, verdict, findings, evidence limitations, absence of mutation, and the permitted integration or remediation next action.

### Blocked-run handoff

Emphasize exact blocker, last safe step, partial state, untouched scope, failed or unavailable evidence, cleanup status, minimum decision, and the next safe action.

### Cross-chat briefing

Emphasize the durable objective, verified current state, chronological completed milestones, current lifecycle boundary, open decisions, continuity risks, and one next task. Exclude conversational history that does not affect execution.

### Next-agent prompt brief

Emphasize repository and branch assumptions, one objective, allowed and forbidden scope, authorizations, exact validation, stop conditions, required report, and the instruction to re-check all volatile state.

## Final handoff structure

Produce exactly these sections:

1. `OBJECTIVE`: handoff boundary, original objective, and current lifecycle state.
2. `VERIFIED STATE`: repository root, branch, HEAD, status, relevant refs, local-only state, and observation time or session boundary when material.
3. `COMPLETED WORK`: commits, messages, changed files, merges, pushes, tags, releases, and explicitly unperformed actions.
4. `VALIDATION / AUDIT EVIDENCE`: exact commands run, exit statuses, concise results, audit targets and verdicts, skipped evidence, and impact.
5. `OPEN ISSUES / WARNINGS`: blockers, failures, partial state, stale evidence, private-boundary risks, and unresolved decisions; write `none` when empty.
6. `NEXT ACTION`: exactly one complete action or decision point with repository, branch assumption, scope, authorization, validation, and expected result.
7. `STOP CONDITIONS`: concrete state, evidence, authorization, validation, destructive-risk, and privacy triggers for the next session.
8. `FACTS VS ASSUMPTIONS`: labeled observed facts, user instructions, inferences, assumptions, unresolved questions, and planned-but-unimplemented work.

Do not call the handoff complete if required facts remain unlabeled or the next action depends on hidden context.

## Anti-patterns

Do not:

- Say “done” without commit, changed-file, status, and validation evidence.
- Claim a merge, push, tag, or release without verifying the distinct applicable state.
- Hide failed, skipped, unavailable, or filtered validation.
- Compress away the exact blocker, stopping point, partial state, or untouched scope.
- Mix roadmap, planned work, or user aspirations with implemented repository state.
- Omit branch, HEAD, or status.
- Omit exact relevant file paths or comparison range.
- Omit whether work is committed, merged, pushed, tagged, or local only.
- Write a handoff that depends on unshared chat memory.
- Copy volatile task state into durable documentation and treat it as current indefinitely.
- Expose private bindings in a public handoff or reusable skill.

## Output contract

Return one self-contained handoff in the required structure. Use concise evidence references rather than raw logs, preserve exact hashes and commands where material, and recommend exactly one next action.
