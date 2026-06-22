---
name: prompt-crafting-for-coding-agents
description: Use when writing bounded, repository-aware prompts for coding-agent implementation, audit, review, debugging, validation, handoff, integration, documentation, or authorized operational work.
---

# Prompt Crafting for Coding Agents

## Purpose

Produce prompts that define one operational objective, exact repository scope, explicit mutation rights, observable evidence, stop conditions, and a deterministic reporting contract. Make authorization and on-disk verification explicit so the agent cannot treat assumptions, technical capability, or vague language as permission.

## Use cases

Use this procedure to craft prompts for:

- Implementation tasks.
- Strict read-only audits.
- Code review and test audit.
- Bug investigation and diagnosis.
- Validation-only work.
- Repository integration and release steps.
- Failure recovery.
- Long-running job launch or monitoring when separately authorized by the applicable skill or project profile.
- Cross-session handoff.
- Documentation-only changes.

Select one primary objective per prompt. Split implementation, independent audit, integration, and long-running completion verification into separate prompts.

## Required prompt inputs

Specify:

- Repository path.
- Current branch assumption.
- Expected base or protected branch.
- Target branch name when implementation is authorized.
- Task objective and explicit completion criterion.
- Exact scope.
- Allowed files and directories.
- Forbidden files and directories.
- Allowed actions.
- Forbidden actions.
- Exact validation commands and expected results.
- Exact commit message when committing is authorized.
- Final report format and permitted verdict vocabulary.
- Stop conditions.
- Known dirty or local-only files.
- Dependency installation, network, remote, and SSH authorization.
- Whether merge, push, and tag actions are forbidden or separately authorized.

Treat an unknown value as unknown, not as permission. Obtain stable rules from repository instructions, a project profile, or a selected skill. Put volatile branch, commit, process, and task state in the current prompt. Never invent repository state.

## Prompt-crafting procedure

1. State the repository and one primary objective in the opening lines.
2. Select the prompt type and applicable supporting skill or profile.
3. Record expected repository state and require inspection before action.
4. Define allowed and forbidden scope using explicit lists.
5. Define each mutation category as authorized or forbidden.
6. Specify an ordered procedure with stop gates before consequential actions.
7. Provide exact, bounded validation commands and success criteria.
8. Define the commit, merge, push, tag, cleanup, and remote policy independently.
9. Require a structured final report with a binary verdict and observed evidence.
10. Scan the prompt for conflicting instructions, private details, implicit permissions, combined independent objectives, and claims not grounded in supplied or discoverable evidence.

Do not compensate for a missing decision with broad autonomy. Ask for the decision or encode a stop condition.

## Prompt types

### Implementation prompt

Authorize a bounded change on a named target branch. State allowed files, whether new files and tests are permitted, validation, exact commit policy, and every forbidden remote or release action. Require the agent to implement and validate, but not to serve as the final independent auditor of its own work.

### Read-only audit prompt

Name the immutable audit target, expected base, allowed inspection commands, required evidence, verdicts, and report format. Explicitly forbid file creation, edits, staging, commits, checkout that changes state, dependency installation, network access, merge, push, tags, cleanup, and remediation. Run the audit in a separate prompt from implementation.

### Review/fix prompt

Choose one mode explicitly:

- Review-only: inspect and report findings without mutation.
- Fix-authorized: apply corrections for a supplied finding set within a narrow allowlist, then validate.

Do not ask the same agent to discover findings, implement unrestricted fixes, and grant final independent approval in one prompt. Use a new read-only audit prompt after remediation when independent acceptance is required.

### Validation-only prompt

Authorize only named validation commands and read-only inspection. State whether commands may create controlled artifacts, whether broad suites are allowed, and how to handle failure. Forbid edits, auto-fix, dependency installation, and cleanup unless each is separately authorized.

### Integration/merge prompt

Supply the audited commit or range and audit verdict. Require fresh ancestry and repository checks, fast-forward-only policy when applicable, and separate authorization for local merge, branch deletion, protected-branch push, tag creation, tag push, and release publication.

### Handoff prompt

Provide observed repository state, completed work, exact remaining objective, validation already run, unresolved failures, active processes, artifacts, and authorization boundaries. Require the receiving agent to re-check volatile state rather than trust the handoff blindly.

Implementation prompts and audit prompts must remain separate. A self-check may validate implementation mechanics, but it is not an independent audit verdict.

## Repository-state assumptions

Require every repository prompt to inspect before acting:

- Repository root and identity.
- Current branch.
- Exact HEAD.
- Status, including staged, unstaged, and untracked paths.
- Relevant commit or comparison range.
- Changed files.
- Upstream or tracking state when relevant and authorized to inspect.

State expected values when known. Require stop-and-report when observed state contradicts the prompt, when a supplied commit is not reachable as expected, or when remote-tracking evidence may be stale and current remote state is material.

Do not instruct the agent to silently stash, reset, clean, switch, pull, fetch, or repair a mismatch.

## Scope control

State explicitly:

- Exact files or directories that may be changed.
- Exact files or directories that must not be changed.
- Whether new files or directories may be created.
- Whether tests may be created or edited.
- Whether documentation may be edited.
- Whether generated outputs may be produced and where.
- Whether existing artifacts may be overwritten.
- Whether deletion, cleanup, rename, or movement is authorized.

Use an exact allowlist for narrow tasks. If patterns are necessary, define their matching semantics. Do not use phrases such as “any relevant files” when the intended scope can be named.

## Authorization boundaries

Set each category to authorized or forbidden:

- Editing or creating files.
- Staging changes.
- Committing.
- Merging or rebasing.
- Pushing branches or tags.
- Creating, moving, or deleting tags.
- Installing or updating dependencies.
- Network access.
- SSH or other remote access.
- Synchronization or transfer.
- Deleting, moving, overwriting, or cleaning files.
- Running production or long-running jobs.
- Killing, restarting, or signaling processes.
- Modifying real configuration, credentials, secrets, or production state.

If the prompt does not explicitly authorize an action, forbid it. Authorization for one category does not imply another: commit does not imply push; remote read does not imply remote write; merge does not imply branch deletion; tag creation does not imply tag push.

## Validation specification

For each validation command, specify:

- Exact command and working directory.
- Bounded test or inspection scope.
- Expected output, exit status, artifact, or success criterion.
- Whether failure requires immediate stop, bounded diagnosis, or an authorized correction cycle.
- Whether broad tests or expensive checks are allowed.
- Whether generated test artifacts are allowed, where they may be written, and whether cleanup is authorized.
- Whether third-party dependencies may be installed; default to forbidden.

Require the final report to distinguish commands actually run from commands skipped or merely recommended. Require failures, filtered tests, missing tools, and environmental limitations to be disclosed.

## Stop conditions

Include stop-and-report conditions for:

- Unexpected dirty working tree.
- Wrong branch, HEAD, repository, or base.
- Missing required files, commits, commands, or artifacts.
- Ambiguous objective or scope.
- Required evidence unavailable.
- Implementation requiring forbidden files or actions.
- Validation failure under the stated failure policy.
- Required dependency installation that is not authorized.
- Required network, SSH, or remote access that is not authorized.
- Destructive, overwrite, deletion, or cleanup risk outside authorization.
- Any mismatch between prompt assumptions and on-disk state.

Require the report to identify the evidence, affected action, consequence, and minimum decision or correction needed. Do not use “stop if anything looks wrong” as a substitute for explicit triggers.

## Final report contract

Require these sections, adapted only when a section is genuinely inapplicable:

1. `VERDICT`: one binary or small-vocabulary outcome defined by the prompt.
2. `REPOSITORY STATE`: branch, HEAD, status, base, and relevant range.
3. `FILES CHANGED`: changed files and scope status; for read-only work, state `none` and list the inspected target separately.
4. `IMPLEMENTATION / AUDIT SUMMARY`: completed work or audit conclusion without unsupported claims.
5. `VALIDATION EVIDENCE`: exact commands run, exit statuses, results, skipped checks, and impact.
6. `WARNINGS / DEFERRED ITEMS`: only substantiated unresolved items; write `none` when empty.
7. `NEXT RECOMMENDED STEP`: exactly one action supported by the verdict.

Avoid vague requests such as “summarize what you did.” Name sections, required facts, and the permitted verdicts.

## Prompt quality rules

Make every prompt:

- Operational: use ordered actions and observable checks.
- Bounded: define one objective, files, actions, and completion boundary.
- Evidence-driven: require commands, outputs, and observed state for claims.
- Explicit about mutation rights and non-rights.
- Explicit about stop conditions and validation failure behavior.
- Public-safe when targeting a public repository; exclude private paths, hosts, repositories, datasets, credentials, and infrastructure details.
- Free of invented branch, commit, runtime, or remote state.
- Small enough to avoid multiple independent objectives.
- Concrete instead of phrases such as “try to,” “be careful,” “as needed,” or “use best judgment” without checks and limits.
- Synchronous and completion-bounded; do not ask an agent to perform unspecified background or asynchronous work.

Keep commands and placeholders internally consistent. Do not present optional commands in a way that implies authorization to run them.

## Anti-patterns

Do not:

- Combine launch and final validation of a long-running job in one prompt. Use separate launch, monitor, and completion-validation prompts.
- Treat an agent's audit of its own unreviewed implementation as final independent authority.
- Allow “any relevant files” when a narrow allowlist is possible.
- Omit branch, HEAD, and status checks.
- Omit forbidden paths or action categories.
- Omit validation commands or success criteria.
- Allow dependency installation by implication.
- Request merge, push, or tag actions without separate explicit authorization.
- Hide important constraints in narrative prose instead of explicit lists.
- Put private paths or project-specific operational state in public reusable skill files.
- Ask for open-ended monitoring, background execution, or a future result without a defined monitoring handoff.

## Example skeletons

Replace every placeholder and remove inapplicable fields rather than leaving ambiguity.

### Implementation prompt skeleton

```text
Repository: <repo>
Expected start: <branch> at <head>; base <base>
Target branch: <target-branch>
Objective: <single implementation objective>
Allowed files: <files>
Forbidden files: <files>
Authorized actions: inspect, edit <scope>, validate <commands>, <stage/commit policy>
Forbidden actions: <push/tag/merge/network/install/delete/etc.>
Before editing: verify root, branch, HEAD, status, range, and changed files; stop on mismatch.
Validation: <commands and success criteria>; on failure: <stop or bounded action>
Commit message: <message or forbidden>
Final report: VERDICT; REPOSITORY STATE; FILES CHANGED; IMPLEMENTATION SUMMARY; VALIDATION EVIDENCE; WARNINGS / DEFERRED ITEMS; NEXT RECOMMENDED STEP.
```

### Read-only audit prompt skeleton

```text
Repository: <repo>
Audit target: <commit/range/output/report>
Expected base and branch: <base>; <branch>
Objective: determine <acceptance question>
Allowed actions: read files; run <read-only commands>
Forbidden actions: all edits, creation, staging, commit, merge, push, tag, install, network, cleanup, and remediation.
Scope: inspect <files>; forbidden paths <files>
Evidence: <required commands, outputs, and criteria>
Stop conditions: state mismatch, dirty tree, unclear scope, missing evidence, or any required mutation.
Final report: <binary verdicts and named sections>.
```

### Validation-only prompt skeleton

```text
Repository: <repo>; expected branch/HEAD: <branch>/<head>
Objective: run only <validation commands>
Allowed writes: <none or controlled artifact paths>
Forbidden actions: edit, auto-fix, install, network, stage, commit, merge, push, tag, cleanup.
Success criteria: <exit status/output/artifact contract>
Failure policy: <stop and report or bounded diagnosis>
Final report: VERDICT; REPOSITORY STATE; FILES CHANGED; VALIDATION EVIDENCE; WARNINGS / DEFERRED ITEMS; NEXT RECOMMENDED STEP.
```

### Integration prompt skeleton

```text
Repository: <repo>
Protected branch: <protected-branch>; feature branch: <feature-branch>
Audited range and verdict: <range>; <verdict>
Objective: <local fast-forward integration or separately authorized closure step>
Before acting: verify clean state, exact heads, merge base, ancestry, commit count, audited range, and changed files.
Authorized actions: <switch/ff-only merge/local deletion/protected push/tag creation/tag push>
Forbidden actions: every integration or remote action not listed above.
Commands: <exact inspection and authorized mutation commands>
Stop conditions: stale audit, moved protected branch, unexpected commits, non-fast-forward state, dirty tree, or missing authorization.
Final report: <integration verdicts and named evidence sections>.
```

## Output contract

Return the completed prompt with placeholders resolved from authoritative inputs, followed by a short `UNRESOLVED INPUTS` list. If any unresolved input affects scope, authorization, validation, or safety, do not present the prompt as execution-ready.
