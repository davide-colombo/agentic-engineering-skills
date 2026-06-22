---
name: git-integration-and-release-workflow
description: Use when integrating audited feature work into a protected branch, verifying fast-forward safety, separating merge from push, cleaning local branches, or closing an authorized tag and release workflow.
---

# Git Integration and Release Workflow

## Purpose

Move audited work from a feature branch into a protected branch without introducing unaudited commits, accidental merge commits, unauthorized pushes, premature tags, or unsupported release claims. Treat local merge, branch cleanup, remote push, tag creation, and tag push as separate authorization boundaries.

## Use cases

Use this workflow to:

- Integrate an audited feature branch into a protected branch.
- Verify fast-forward eligibility and avoid accidental merge commits.
- Separate a local merge from a remote push.
- Delete a local feature branch after a successful merge.
- Decide whether a tag or release action is appropriate and authorized.
- Close an implementation and audit cycle with exact evidence.
- Prepare exact generic commands for an authorized human or agent to run.

This skill governs integration actions; it does not replace repository-state inspection, code review, or the audit that establishes the accepted commit range.

## Required inputs

Identify before any integration action:

- Repository path.
- Current branch.
- Protected or base branch.
- Feature branch.
- Audited commit or exact commit range.
- Audit verdict and the evidence that produced it.
- Whether protected-branch push is authorized.
- Whether tag creation and release work are authorized.
- Expected tag name, if any.
- Remote name, if push is authorized.
- Local dirty-state policy.
- Local and remote branch deletion policy.

Treat absent authorization as not authorized. Obtain stable policy from the project profile or repository instructions and current authority from the task prompt. Do not infer authorization from credentials, remote configuration, prior tasks, or technical capability.

## Workflow

1. Restate the repository, protected branch, feature branch, audited commit range, audit verdict, dirty-state policy, and separate authorizations for merge, deletion, push, tag creation, and tag push.
2. Run all pre-integration checks before switching branches or merging.
3. Confirm the audit verdict permits integration and still applies to the exact feature branch content and protected-branch base.
4. Stop if any check contradicts the audit basis or would require broader mutation than authorized.
5. When authorized, switch to the protected branch and immediately repeat the material repository, status, HEAD, and ancestry checks.
6. Integrate using `git merge --ff-only` with the verified feature branch.
7. Verify the protected branch now points to the expected audited commit and the working tree is clean.
8. Perform separately authorized local branch deletion, protected-branch push, tag creation, or tag push only after their individual preconditions pass.
9. Report actions actually performed, actions not authorized, exact resulting references, and one next step.

Never combine authorization gates merely because commands can be chained.

## Pre-integration repository checks

Verify and record:

- Repository root and that the path is a Git working tree.
- Clean working tree under the stated dirty-state policy, including staged, unstaged, and untracked paths.
- Current branch and exact HEAD.
- Protected branch existence and exact HEAD.
- Feature branch existence and exact HEAD.
- Upstream or tracking state when relevant, using local references unless remote access is authorized.
- Merge base between protected and feature branches.
- Whether the protected branch is an ancestor of the feature branch.
- Exact commits present on the feature branch but not the protected branch.
- Whether those commits are exactly the audited commits and contain no merge commit.
- Whether the feature branch can fast-forward the protected branch.
- Whether the audited commit equals feature branch HEAD or the supplied range has the expected endpoints.

An audit becomes stale when the feature branch gains, loses, or rewrites commits, or when the protected branch moves away from the audited base in a way the audit did not cover. Re-audit the new range before integration.

## Fast-forward merge policy

- Prefer and use `git merge --ff-only` for authorized branch integration.
- Block a normal merge commit unless the current prompt explicitly authorizes it and applicable policy permits it.
- Block a squash merge unless explicitly authorized; a squash creates a new commit not covered by a commit-hash audit.
- Block rebase after audit unless explicitly authorized. Require a new audit of the rewritten commits before integration.
- Never merge a commit that is outside the accepted audited range.
- Never merge when the protected branch has moved in a way that invalidates the audit basis.
- Do not use pull as a substitute for explicit protected-branch inspection and merge control.

After the merge, verify the protected branch HEAD, ancestry, commit range, working-tree state, and absence of an unintended merge commit before any cleanup or remote action.

## Push separation

Local integration and remote push are separate decisions:

- Do not push a feature branch unless the current prompt explicitly requests that exact push.
- Do not push the protected branch without explicit authorization.
- Before pushing, verify the local protected branch contains the expected audited commit and no unexpected additional commit.
- Confirm the intended remote and refspec. Do not infer them from a default remote.
- If remote state must be inspected, require authorization for network access and state whether local remote-tracking references may be stale.
- After pushing, verify remote state only when required by the workflow and authorized. Do not repeat a full audit when verified local state is sufficient for the requested closure.

Authorization to merge locally does not authorize a push. Authorization to push one branch does not authorize feature-branch pushes, force pushes, tags, or release publication.

## Branch deletion

- Delete only the local feature branch after the fast-forward merge succeeds, the protected branch points to the expected commit, and the working tree is clean.
- Do not delete a feature branch while it is the current branch.
- Do not delete a branch containing commits not merged into the protected branch.
- Use safe local deletion rather than forced deletion unless an explicit exceptional policy authorizes otherwise.
- Do not delete a remote branch unless the current prompt explicitly authorizes that separate remote mutation.
- Report the branch name, local or remote scope, command outcome, and retained unmerged state if deletion is blocked.

Branch deletion is cleanup, not evidence that integration succeeded.

## Tag and release closure

- Treat tag creation, tag push, and release publication as separate actions from merge and protected-branch push.
- Do not create a tag unless the current prompt explicitly authorizes it.
- Verify repository versioning and release policy, expected tag name, release commit, validation evidence, and required documentation before tagging.
- Tag only the protected-branch commit intended for release.
- Verify an existing tag's target before claiming a release exists; do not silently move or replace a tag.
- Do not claim a release or tag exists unless the applicable tag is present in the inspected state.
- Do not push a tag without explicit authorization for that tag and remote.
- Distinguish local tag creation from remote tag push in commands and reports.

A local tag does not establish a remote release. A pushed tag does not establish publication through a separate release service unless that state is independently verified.

## Stop-and-report triggers

Stop before the next state-changing action when:

- The repository path is missing or is not a Git repository.
- Dirty state violates or is not covered by the supplied policy.
- The observed current, protected, or expected branch state contradicts the task.
- The feature branch is missing.
- The merge base is missing, unexpected, or inconsistent with the audit basis.
- The protected branch is not an ancestor of the feature branch for a required fast-forward integration.
- The feature branch contains unexpected, unaudited, rewritten, or merge commits.
- The audit verdict is absent, failed, blocked, warning-bearing without an accepted risk decision, or stale.
- A fast-forward merge would fail.
- A required push, tag, tag push, remote deletion, or release action lacks explicit authorization.
- Remote state is material but ambiguous and authorized inspection is unavailable.
- A command would mutate state beyond its exact authorization.
- The protected branch moved after verification or the audited commit no longer identifies the expected feature branch state.

Report the observed evidence, blocked action, consequence, and minimum new audit, correction, or authorization required. Do not rebase, squash, force, reset, merge normally, fetch, push, delete, or retag to bypass a stop condition.

## Command patterns

Substitute values from verified inputs. Run commands individually so each result can be checked before the next mutation.

Inspect repository and references:

```sh
git rev-parse --show-toplevel
git status --short --branch --untracked-files=all
git branch --show-current
git rev-parse HEAD
git rev-parse <protected-branch>
git rev-parse <feature-branch>
git branch -vv
```

Verify ancestry, range, and fast-forward eligibility:

```sh
git merge-base <protected-branch> <feature-branch>
git merge-base --is-ancestor <protected-branch> <feature-branch>
git rev-list --count <protected-branch>..<feature-branch>
git log --format='%H %P %s' <protected-branch>..<feature-branch>
git diff --name-status <protected-branch>..<feature-branch>
```

Perform an authorized local fast-forward merge and verify it:

```sh
git switch <protected-branch>
git merge --ff-only <feature-branch>
git rev-parse HEAD
git status --short --branch --untracked-files=all
```

Delete an authorized merged local branch:

```sh
git branch -d <feature-branch>
```

Optionally push the protected branch when separately authorized:

```sh
git push <remote> <protected-branch>
```

Optionally create and push an authorized tag:

```sh
git tag -a <tag-name> <release-commit> -m '<release-message>'
git push <remote> <tag-name>
```

Do not run optional patterns merely because they are documented. Confirm current state and authorization immediately before each mutating command.

## Final report format

Produce exactly these sections:

1. `VERDICT`: exactly one verdict and a concise rationale.
2. `REPOSITORY STATE`: root, current branch, protected and feature branch HEADs, working-tree state, tracking state, and final HEAD.
3. `AUDIT BASIS`: audit verdict, audited commit or range, expected base, evidence source, freshness, and accepted warnings.
4. `INTEGRATION CHECKS`: merge base, ancestry, expected commits, unexpected commits, merge commits, and fast-forward eligibility.
5. `ACTIONS PERFORMED`: exact local state-changing actions and outcomes; write `none` when no action was authorized or performed.
6. `PUSH / TAG STATUS`: protected and feature branch push state, local and remote tag state, release status, authorizations, and actions not performed.
7. `BRANCH CLEANUP`: local and remote branch retention or deletion, safety checks, and outcomes.
8. `RISKS / WARNINGS`: stale references, accepted audit warnings, ambiguous remote state, deferred actions, and other residual risk; write `none` when empty.
9. `NEXT STEP`: one minimum authorized action or required decision supported by the verdict.
10. `COMMANDS / EVIDENCE APPENDIX`: exact commands actually run, exit statuses, concise results, and commands prepared but not run.

Do not report a merge, push, deletion, tag, or release as complete without directly observed supporting evidence.

## Verdict vocabulary

- `GIT_INTEGRATION_READY`: The audit is current, the exact expected commits are fast-forwardable into the protected branch, required checks pass, and every proposed action is within explicit authorization with no warning remaining.
- `GIT_INTEGRATION_READY_WITH_WARNINGS`: No blocking condition remains and the authorized integration is safe, but substantiated non-blocking limitations, accepted audit warnings, or deferred separately authorized actions remain.
- `GIT_INTEGRATION_BLOCKED`: Missing inputs, stale or insufficient audit evidence, ambiguous state, absent authorization, or a failed prerequisite prevents a reliable or authorized integration decision.
- `GIT_INTEGRATION_FAILED`: Inspected evidence demonstrates unexpected commits, invalid ancestry, an unsafe or non-fast-forward integration, unauthorized mutation, incorrect cleanup, or a false push, tag, or release claim.

Use `GIT_INTEGRATION_BLOCKED` when integration cannot be evaluated or performed safely under current authority. Use `GIT_INTEGRATION_FAILED` when sufficient evidence establishes a workflow violation or unsafe target. Use a ready verdict only when the audit basis remains valid and no blocking condition exists.
