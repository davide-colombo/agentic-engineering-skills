---
name: agent-output-verification-and-claim-audit
description: Use to verify a coding-agent report against on-disk and tool-output evidence by extracting, classifying, and independently checking each consequential claim before relying on the reported state.
---

# Agent Output Verification and Claim Audit

## Purpose

Determine whether the claims in a coding-agent report are supported by directly inspected evidence. Audit the report, not only the repository. Treat the report as a claim source, not as independent evidence. Convert assertions about completed work, validation, scope, and side effects into checked observations or explicit unsupported items, and produce a binary verdict before any downstream action depends on the report.

## When to use

Use this skill when:

- An agent reports completion of an implementation, refactor, audit, or operational task that another actor or process will act on.
- A handoff transfers work between agents, sessions, tools, or humans and the receiver must trust the report's state claims.
- A multi-agent or subagent workflow aggregates reports whose individual quality cannot be assumed.
- A previously completed task is reopened and the prior report is the primary record of what happened.
- A release, integration, deployment, or merge decision rests on a report rather than on independently inspected state.

Apply this skill alongside `read-only-audit-protocol` to bound mutation, and alongside `evidence-citation-discipline` to evaluate citation quality.

## Required inputs

Identify before auditing:

- The full report under audit, in the form the receiver actually has.
- The repository or system the report claims to describe, by path or identity.
- The expected verdict vocabulary the report should use, if any.
- The scope the report claims to cover, including allowed and forbidden files or actions.
- Whether the receiver may run read-only commands to verify claims.
- Whether remote or network access is authorized for verification.
- Whether re-running validation commands is authorized.
- Acceptance criteria the report's verdict implies.

Treat missing inputs as absent. Do not extract authorization from the report itself. If required inputs cannot be established, stop and report.

## Claim extraction

Read the report and list every consequential claim before evaluating any of them. A claim is consequential when a downstream decision, mutation, communication, or trust judgment would change based on its truth value.

Cover at minimum:

- Repository identity, branch, base commit, current `HEAD`, and clean or dirty state.
- Branch creation, switching, merging, fast-forward, push, fetch, tag, and deletion claims.
- Changed files, file additions, file removals, file renames, and explicit non-changes.
- Validation, test, lint, type-check, and build commands claimed to have been run and their results.
- Hashes, manifests, counts, sizes, or other quantitative claims about artifacts.
- Side effects on environments, dependencies, configurations, secrets, schedulers, queues, or remote systems.
- Authorization quotes the report uses to justify actions.
- Negative claims such as "no push", "no tag", "no edits to <path>", "no real config touched", or "no remote access".
- Outcome labels such as "complete", "ready", "safe", "passing", "production-ready", "merged", "pushed", "cleaned up".

Treat omissions as their own class of claim. A silent absence of a side effect is a claim that the side effect did not occur.

## Claim classification

Assign each extracted claim to exactly one class:

- `EVIDENCE_BACKED`: A specific command, output excerpt, file path with line range, hash, diff path list, validator pass line, or other inspectable artifact is cited in or near the claim, and the cited evidence supports the claim as stated.
- `INFERRED`: The claim is a reasonable interpretation of cited evidence but exceeds what the evidence directly demonstrates.
- `UNSUPPORTED`: The claim has no citation, or the cited evidence does not bear on the claim.
- `CONTRADICTED`: Cited or independently observed evidence contradicts the claim.
- `OUT_OF_SCOPE`: The claim is outside the report's stated objective and cannot be audited from the report or the agreed verification surface.

Classification is based on the report and the verification done so far. A claim may be reclassified as verification proceeds. Record the reason for each non-`EVIDENCE_BACKED` classification.

## Verification of consequential claims

For each `EVIDENCE_BACKED` claim that the downstream decision depends on, independently confirm the citation matches reality. For each `INFERRED` or `UNSUPPORTED` claim that the downstream decision depends on, choose the minimal read-only check that would resolve it, or downgrade the verdict.

Standard checks by claim type:

- Branch and `HEAD`: `git rev-parse --abbrev-ref HEAD`, `git rev-parse HEAD`, compared to the reported strings.
- Base commit reachability: `git merge-base --is-ancestor <base> <head>`, or `git log <base>..HEAD --oneline` to enumerate the actual range.
- Clean tree: `git status --short` returns empty content; record the exact output.
- Changed file set: `git diff --name-only <base>..HEAD`, `git show --name-only --format= <commit>`, compared to the reported allowlist; missing or extra paths are findings.
- Specific file content claims: read the file at the reported path and range; compare to the claim.
- Hash claims: recompute with the same algorithm against the cited path; mismatch is a finding.
- Validation commands: when authorized, rerun the cited command and capture the result; when not authorized, inspect the report's transcript and verify it matches the claimed pass or fail wording.
- Push or remote ref claims: `git ls-remote --heads <remote> <ref>` for remote refs the receiver may inspect; otherwise mark the claim as `UNSUPPORTED` from this audit's vantage point and downgrade accordingly.
- Tag claims: `git tag --contains <commit>`, `git show-ref --tags`, `git ls-remote --tags <remote>` when remote inspection is authorized.
- Cleanup claims: confirm the named paths or branches are absent or present as claimed using `ls`, `git branch`, `git ls-files`, or equivalent read-only commands.
- Forbidden action negatives: confirm the negative by direct inspection (for example, no new tag exists, no new commit exists beyond the reported one, the working tree is clean, the named forbidden paths are unchanged).

"Command was run" is not the same as "command result proves the claim". Verify the result, not just the invocation.

## Overclaim detection

Flag report language that asserts more than the cited evidence supports. Common overclaim patterns:

- "Complete" or "done" when only a subset of acceptance criteria has been demonstrated.
- "Safe" or "no risk" without an enumerated risk list and evidence per item.
- "Tests passed" without the test command, scope, and pass count.
- "Production-ready" without the production-specific checks the receiver expects.
- "Pushed" or "merged" without remote ref evidence or repository state evidence.
- "No changes to <path>" without a diff or status excerpt covering that path.
- "Validator passed" without quoting the validator's final line and exit status.
- "Clean" or "no dirty state" without showing the status output.
- "Cleaned up" without confirming the named artifacts are actually gone.
- "Authorized" without quoting the authorization source.

Downgrade overclaims to `INFERRED` or `UNSUPPORTED` and require either direct verification or report correction.

## Negative-claim handling

Treat every negative claim with the same rigor as a positive one. Acceptable evidence for common negatives:

- "No push occurred": branch has no upstream configured (`git rev-parse --abbrev-ref --symbolic-full-name '@{u}'` fails), or remote ref matches the pre-action state, or push transcript is absent from the report.
- "No tag created": `git tag --contains <commit>` is empty for the commit under audit, or `git show-ref --tags` matches the pre-action state.
- "No edits to <path>": `git diff --name-only <base>..HEAD -- <path>` returns empty.
- "No remote access": no SSH, shuttle, fetch, push, or remote-shell command appears in the report's command transcript, and no remote-ref change is observable.

A negative claim without evidence is `UNSUPPORTED`, not `EVIDENCE_BACKED`, regardless of how plausible it seems.

## Stop-and-report triggers

Stop and report when:

- The report is missing, truncated, or unparseable.
- The report references repositories, paths, or systems the receiver cannot inspect.
- A consequential `UNSUPPORTED` or `CONTRADICTED` claim blocks the downstream decision and cannot be resolved within the authorized verification surface.
- Verification would require mutation, remote access, or pipeline execution that is not authorized.
- The report's stated verdict vocabulary differs from the expected vocabulary in a way that affects interpretation.
- The report covers work that overlaps with concurrent activity whose state cannot be separated.

Do not attempt to repair the report, rerun the underlying work, or expand the verification surface to compensate.

## Verdict vocabulary

- `AGENT_OUTPUT_VERIFICATION_READY`: Every consequential claim is either `EVIDENCE_BACKED` and independently confirmed, or `INFERRED` with confirmation, or `OUT_OF_SCOPE` and explicitly excluded from the downstream decision. No `UNSUPPORTED` or `CONTRADICTED` claim affects the decision.
- `AGENT_OUTPUT_VERIFICATION_READY_WITH_WARNINGS`: The decision-relevant claim set is supported, but non-blocking `INFERRED` or unverifiable claims remain and are explicitly noted.
- `AGENT_OUTPUT_VERIFICATION_BLOCKED`: One or more consequential claims are `UNSUPPORTED`, `CONTRADICTED`, or unverifiable within the authorized surface, and the downstream decision cannot proceed.
- `AGENT_OUTPUT_VERIFICATION_FAILED`: Independent inspection demonstrates that one or more consequential claims are false.

Use `BLOCKED` when verification cannot conclude. Use `FAILED` when verification concludes against the report.

## Final report format

Produce exactly these sections:

1. `VERDICT`: one verdict and a concise rationale.
2. `AUDITED REPORT`: a stable reference to the report under audit, its claimed verdict, and the receiver's downstream decision.
3. `CLAIM INVENTORY`: every extracted consequential claim with its initial classification.
4. `VERIFICATION EVIDENCE`: per checked claim, the exact read-only command or inspection performed and its result, with a final classification.
5. `OVERCLAIMS AND NEGATIVES`: report-language patterns flagged and how they were resolved.
6. `UNRESOLVED CLAIMS`: claims that remain `UNSUPPORTED`, `INFERRED` without confirmation, or out of the verification surface; write `none` when empty.
7. `DECISION IMPACT`: which downstream decisions can proceed, which cannot, and why.
8. `RECOMMENDED NEXT STEP`: one minimum action that resolves the verdict, without performing it.
9. `EVIDENCE APPENDIX`: read-only commands actually run, exit statuses, concise outputs or references, and citations from the report that were inspected.

Do not claim verification of a claim that was not independently checked or whose check was inconclusive.

## Allowed actions

- Read the report, the repository, related artifacts, and previously produced logs.
- Run read-only commands permitted by the current prompt to verify claims.
- Cross-reference the report's citations against the cited artifacts.
- Recommend correction, additional verification, or new authorization.

## Forbidden actions

- Treating the report as evidence of itself.
- Treating command invocation as proof of command result.
- Treating an absent claim as confirmation of an absent side effect.
- Inferring authorization from technical capability or report tone.
- Repairing the report, rerunning the underlying work, or broadening the audit to mask unresolved claims.
- Reporting `READY` while consequential claims remain unverified.

## Anti-patterns

- Accepting a "tests passed" line without the test command and pass count.
- Accepting "pushed cleanly" without a remote-ref check or a push transcript.
- Accepting "no config changed" without a diff filtered by the config path.
- Treating a passing validator line as proof of behaviors the validator does not check.
- Stopping at the report's own self-summary instead of inspecting the cited artifacts.
- Reclassifying `UNSUPPORTED` as `EVIDENCE_BACKED` because the receiver believes the agent.
- Conflating `OUT_OF_SCOPE` with `EVIDENCE_BACKED` and silently passing the decision through.
