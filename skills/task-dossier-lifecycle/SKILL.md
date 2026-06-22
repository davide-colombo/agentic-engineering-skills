---
name: task-dossier-lifecycle
description: Use when a prompt, project profile, local overlay, or repository convention authorizes creating, updating, inspecting, or closing a durable task dossier.
---

# Task Dossier Lifecycle

## Purpose

Manage an authorized, scoped task dossier as a durable record of decisions, evidence, plans, acceptance criteria, and lifecycle state. Treat dossiers as optional project-policy artifacts, not universal requirements. Never create or edit one merely because a task is complex or this skill is available.

## Use cases

Use an authorized dossier for:

- Medium or large implementation plans.
- Design records and architecture decisions.
- Acceptance criteria and validation plans.
- Audit evidence.
- Cross-session continuity.
- Long-running task planning.
- Risk registers.
- Integration or release notes when authorized.
- Failure or postmortem notes when authorized.

Do not use a dossier for:

- Small, single-commit tasks that do not require one.
- Ordinary final reports.
- Volatile run status or live process tracking.
- Temporary chat or scratch notes.
- Private or local-machine notes in a public repository.
- Any work not authorized by the current prompt, project profile, local overlay, repository convention, or existing dossier instructions.

## Authorization model

Before dossier work, identify the authorization basis in this order:

1. Current task prompt.
2. Project profile.
3. Local overlay.
4. Repository convention.
5. Instructions within an existing dossier.

Record which source authorizes read-only inspection, creation, editing, appending, lifecycle changes, and committing. These are separate permissions. A repository convention may define structure without authorizing the current mutation.

If authorization is absent, do not create or edit a dossier. Report that constraint and, when useful, recommend a dossier for a separately authorized task. Do not infer permission from similar dossiers, filesystem access, task size, prior work, or technical capability.

## Required inputs

Identify before acting:

- Repository path.
- Task identifier.
- Exact dossier path.
- Owner or requesting context, if available.
- Current branch and exact HEAD.
- Protected or base branch when relevant.
- Allowed dossier files.
- Whether read-only inspection, creation, edit, append, or lifecycle transition is authorized.
- Whether implementation files may also be changed.
- Whether volatile state is forbidden or explicitly allowed.
- Commit authorization and expected commit policy.
- Final report expectations.

Treat missing values as unknown, not permission. Keep dossier scope separate from implementation scope.

## Discovery and preconditions

Before creating or editing:

- Verify the repository root, branch, HEAD, and full status.
- Determine whether the exact dossier path exists.
- Inspect similar dossiers only within authorized read scope.
- Identify naming, layout, section, and task-identifier conventions.
- Check whether an index or README references dossiers.
- Determine whether the target path is tracked, untracked, or ignored.
- Confirm the current branch and dirty state permit the authorized edit.
- Check whether another task, branch, or owner already controls the target path.

If the dossier exists, read it before modifying it. Preserve unknown or unexplained material and stop if it conflicts with the requested work. Do not overwrite a directory or file because its name matches an expected convention.

## Procedure

1. State the task identifier, dossier target, requested lifecycle action, and authorization basis.
2. Verify repository state and discover applicable dossier conventions.
3. Inspect the existing dossier and related index references when present.
4. Define the exact allowed dossier files and whether implementation changes are separately permitted.
5. Classify proposed content by evidence type and remove unauthorized volatile or private state.
6. Create, append, or narrowly edit only the authorized material.
7. Preserve prior decisions and record justified lifecycle transitions.
8. Validate file scope, structure, factual claims, privacy boundary, and repository status.
9. Commit only when the current task explicitly authorizes it.
10. Report the resulting dossier state, evidence captured, open risks, and one next action.

## Recommended dossier contents

Adapt sections to project policy and task scale. Omit inapplicable sections rather than filling them with generic prose:

- `OBJECTIVE`
- `SCOPE`
- `NON-GOALS`
- `REPOSITORY STATE AT CREATION / UPDATE`
- `EVIDENCE SOURCES`
- `DESIGN DECISIONS`
- `ALTERNATIVES REJECTED`
- `IMPLEMENTATION PLAN`
- `VALIDATION PLAN`
- `ACCEPTANCE CRITERIA`
- `RISKS AND MITIGATIONS`
- `OPEN QUESTIONS`
- `CHANGE LOG`
- `NEXT ACTION`

Repository state recorded in a dossier is a dated or commit-bound snapshot, not a permanently current claim. Link decisions to evidence or authority when the distinction matters.

## Evidence discipline

Separate and label:

- `VERIFIED FACT`: Directly observed and supported by identified evidence.
- `USER INSTRUCTION`: Requirement or authorization supplied by the user.
- `DESIGN DECISION`: Chosen approach, owner, rationale, and decision state.
- `ASSUMPTION`: Unverified condition used for planning.
- `HYPOTHESIS`: Testable explanation awaiting evidence.
- `UNRESOLVED QUESTION`: Missing fact or decision.
- `PLANNED WORK`: Proposed but not implemented.
- `COMPLETED WORK`: Work supported by repository or operational evidence.
- `VALIDATION EVIDENCE`: Command or inspection, outcome, and applicable target.

Do not claim implementation, validation, audit, merge, push, tag, release, deployment, or production status without evidence for that exact state. A plan, checklist, prior report, or user expectation is not proof of completion. Mark stale evidence rather than silently carrying it forward.

## Volatile-state policy

A dossier is not a general session log or live job tracker unless project policy explicitly authorizes that use and defines retention. Keep active process identifiers, transient timestamps, scratch paths, temporary errors, progress percentages, current worker state, and other short-lived observations in the current prompt, final report, monitoring record, or external session handoff.

When limited volatile state is authorized, label its observation time, source, expected lifetime, and replacement or cleanup rule. Do not commit volatile state merely to preserve chat continuity.

## Public/private boundary

For public repositories:

- Exclude private absolute paths, secrets, credentials, private infrastructure, hosts, unpublished proprietary details, and user-specific project facts.
- Use generic placeholders for reusable examples.
- Confirm that evidence and linked artifacts are intended for public disclosure.

For private repositories:

- Include private bindings only where project policy permits.
- Keep secrets and credentials out of dossiers.
- Keep private dossier content in the private project; never copy it into a public reusable skill.

Stop when the publication boundary is unclear or a public dossier would expose private content.

## Mutation rules

- Read before write.
- Prefer an append or narrow edit over broad rewriting.
- Preserve prior decisions unless explicitly superseded.
- Mark a superseded decision with its replacement, rationale, and evidence; do not delete history unless cleanup is authorized.
- Do not rewrite a dossier to match an unverified narrative.
- Do not add generated junk, raw logs, caches, or unrelated artifacts.
- Do not modify unrelated dossiers or index files outside the allowlist.
- Do not use dossier authorization to expand implementation scope.
- Do not commit dossier changes unless commit authorization exists.

After mutation, inspect the exact diff and status. Confirm that only allowed files changed and that no prior content disappeared unintentionally.

## Lifecycle states

Use project-defined states when available. Otherwise these generic states may be used:

- `PROPOSED`: Scope or approach is awaiting authorization or decision.
- `ACTIVE`: Authorized work is underway.
- `BLOCKED`: A documented blocker prevents progress.
- `IMPLEMENTED`: Defined implementation work is complete and evidenced, but later gates may remain.
- `AUDITED`: The identified target received a recorded audit verdict.
- `INTEGRATED`: The evidenced work is present on the intended protected or base branch.
- `SUPERSEDED`: A newer identified decision or dossier replaces this one.
- `ARCHIVED`: No active work remains and retention is intentional.

States reflect verified evidence, not intention. Record the evidence and date or commit boundary for each transition. Do not infer `AUDITED` from validation, `INTEGRATED` from a feature commit, or `ARCHIVED` from inactivity.

## Stop conditions

Stop and report when:

- Dossier authorization is absent or does not cover the requested action.
- The dossier path or task identifier is ambiguous.
- Repository branch, HEAD, or status contradicts assumptions.
- Existing dossier content conflicts with the requested work.
- The action requires a forbidden file or unrelated dossier.
- Public content would expose private information.
- Volatile state would be committed without explicit authorization.
- Claimed implementation, validation, audit, integration, or release state cannot be verified.
- Another task, branch, or owner already controls the dossier path.
- Required evidence or project convention is missing.

Report the observed state, blocked action, affected path, evidence gap, and minimum authorization or decision required. Do not resolve ambiguity by creating an alternate dossier path.

## Final report format

Produce exactly these sections:

1. `VERDICT`: completed, ready with warnings, blocked, or failed, with a concise basis.
2. `DOSSIER TARGET`: task identifier, exact path, prior state, and resulting lifecycle state.
3. `REPOSITORY STATE`: repository root, branch, HEAD, status, and relevant base.
4. `AUTHORIZATION BASIS`: sources and exact permissions for inspection, mutation, implementation, and commit.
5. `DOSSIER ACTIONS`: files inspected, created, appended, edited, superseded, or intentionally untouched.
6. `EVIDENCE CAPTURED`: facts, decisions, validation evidence, assumptions, and unresolved evidence gaps.
7. `OPEN QUESTIONS / RISKS`: blockers, privacy risks, volatile state, conflicting ownership, and stale evidence; write `none` when empty.
8. `FILES CHANGED`: exact paths and whether each was allowed.
9. `VALIDATION`: commands or inspections run, outcomes, skipped checks, and resulting limitations.
10. `NEXT ACTION`: exactly one authorized action or required decision.

Do not reduce the report to “dossier updated.” Identify the evidence boundary and every mutation actually performed.

## Anti-patterns

Do not:

- Create a dossier by default for every task.
- Use a dossier as a scratchpad, transcript, or general session log.
- Store volatile state in durable documentation without explicit policy.
- Mix private project bindings into public reusable documentation.
- Overwrite or silently delete prior decisions.
- Record assumptions, hypotheses, plans, or roadmap claims as facts.
- Claim implementation, audit, merge, push, tag, release, or production status without evidence.
- Use a dossier to bypass explicit file or action scope.
- Edit multiple dossiers when only one is authorized.
- Commit dossier changes without explicit authorization.

## Output contract

Return the required report with the dossier's verified lifecycle state, exact authorization basis, evidence boundary, changed-file scope, validation outcome, and one next action. If no dossier mutation is authorized, inspect and recommend only within the permitted read scope.
