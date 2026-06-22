# Scientific Software Agent Skills

This repository contains reusable, project-agnostic procedures for coding agents working on scientific software, bioinformatics pipelines, reproducible computation, large-data workflows, and remote or HPC execution. It is intended for researchers, research software engineers, data engineers, and maintainers who need agents to operate against explicit engineering controls.

The repository addresses a recurring problem: an agent needs reliable operating procedures, but each project has different branches, commands, infrastructure, data restrictions, and current state. Mixing all of that into one large prompt makes instructions hard to inspect, reuse, update, and enforce. Small skills are better engineering units: each has a bounded purpose, explicit inputs, stop conditions, permitted actions, and an output contract.

This is an engineering method, not a prompt collection. Procedures belong in skills; stable project facts belong in private profiles; temporary state belongs in the current task; and hard controls belong in deterministic hooks or scripts.

## Instruction layers

| Layer | Contains | Lifetime |
| --- | --- | --- |
| Current task prompt | Immediate objective, authorized actions, task-specific constraints, and temporary state | One task or session |
| Project profile | Stable project policy, commands, terminology, and repository conventions | Persistent within one private project |
| Public base skill | General procedure, checks, verdicts, and action boundaries | Reusable across projects |
| Private local overlay | Skill-specific project bindings, stricter checks, and approved specialization | Persistent within one private project |
| On-disk reality or observed evidence | Actual repository, filesystem, runtime, and validation state | Must be checked for each task |
| Hook or deterministic script | Machine-enforced checks that must not depend on agent judgment | Persistent enforcement |

Always-on files such as `AGENTS.md` and `CLAUDE.md` should remain short and task-agnostic. They should point to the relevant profile or skill rather than duplicate detailed procedures. Volatile software behavior should be checked against the installed version or current official documentation when the skill is used.

## Install and use a skill

Copy the complete skill directory into the target project, preserving its relative structure. For example:

```sh
mkdir -p path/to/project/skills
cp -R skills/repo-state-audit path/to/project/skills/
```

Then instruct the coding agent to load `skills/repo-state-audit/SKILL.md` before it changes repository state. If the agent platform has a native skill directory or import mechanism, place or reference the skill there instead.

Copy and customize the project templates as private bindings. These destinations are examples, not required paths:

```sh
cp templates/PROJECT_PROFILE.md path/to/project/PROJECT_PROFILE.md
cp templates/PROJECT_PROFILE.md path/to/project/.agents/PROJECT_PROFILE.md
cp templates/LOCAL_OVERLAY.md path/to/project/.skills-local/repo-state-audit.local.md
cp templates/LOCAL_OVERLAY.md path/to/project/.claude/skills/repo-state-audit/LOCAL_OVERLAY.md
```

Choose one appropriate destination for each file and record those locations in the project's always-on agent instructions. Do not copy both examples unless the project deliberately maintains multiple agent integrations.

After installation, customize the private project profile and, when needed, a local overlay. Define protected and source-of-truth branches, permitted dirty or local-only files, forbidden paths, test and build commands, dependency policy, remote execution rules, deployment rules, domain terms, and reporting requirements. Do not modify the public base procedure merely to record current branch state, temporary exceptions, machine paths, credentials, or other volatile or private facts.

Use this canonical model: current task prompt, project profile, selected public skill, local overlay, observed evidence, then hooks or scripts for deterministic enforcement. The first four layers provide instructions and project bindings. On-disk reality is evidence, not a lower-priority instruction; if it contradicts instructions or assumptions, stop and report. Hooks and scripts enforce non-negotiable checks at execution time and are not advisory. A local overlay may specialize the selected skill but must not weaken the skill, project profile, or current prompt unless the current task prompt explicitly authorizes the exception.

## Recommended first skill

Start with [`repo-state-audit`](skills/repo-state-audit/SKILL.md). It establishes whether the repository and current authorization are safe and aligned before an agent edits files, installs dependencies, contacts remotes, starts long jobs, or performs destructive operations.

Use [`code-review-and-test-audit`](skills/code-review-and-test-audit/SKILL.md) for strict review and test-quality assessment before implementation, after changes, or before integration.

Use [`resumable-pipeline-design`](skills/resumable-pipeline-design/SKILL.md) to design or audit checkpointed multi-step workflows, failure recovery, and safe resume behavior.

Use [`configuration-and-environment-integrity`](skills/configuration-and-environment-integrity/SKILL.md) to audit configuration behavior, runtime parity, dependency setup, tool discovery, and reproducible environments.

Use [`hardware-aware-parallelism`](skills/hardware-aware-parallelism/SKILL.md) to audit worker topology, resource budgets, hidden threading, contention, and scaling behavior.

Use [`data-transfer-and-integrity`](skills/data-transfer-and-integrity/SKILL.md) to audit transfers, manifests, checksums, partial state, archives, and provenance before downstream use.

Use [`read-only-audit-protocol`](skills/read-only-audit-protocol/SKILL.md) for strict non-mutating audits of commits, branches, patches, generated outputs, validation evidence, agent reports, and integration or release readiness.

Use [`git-integration-and-release-workflow`](skills/git-integration-and-release-workflow/SKILL.md) to integrate audited branches with fast-forward controls, separate local merges from pushes, clean up local branches, and close authorized tag or release workflows.

Use [`prompt-crafting-for-coding-agents`](skills/prompt-crafting-for-coding-agents/SKILL.md) to write bounded, repository-aware prompts for implementation, audit, review, validation, handoff, integration, documentation, and authorized operational work.

Use [`cross-session-handoff-and-continuity`](skills/cross-session-handoff-and-continuity/SKILL.md) to preserve verified repository state, evidence, blockers, decisions, and one executable next action across chats, tools, and coding-agent runs.

Use [`task-dossier-lifecycle`](skills/task-dossier-lifecycle/SKILL.md) to manage optional, project-authorized task dossiers as durable records of decisions, evidence, plans, acceptance criteria, risks, and lifecycle state.

Use [`production-run-launch-and-monitoring`](skills/production-run-launch-and-monitoring/SKILL.md) to plan, authorize, launch, monitor, intervene in, and validate long-running production jobs with explicit resource, observability, and evidence controls.

Use [`failure-recovery-and-rerun-planning`](skills/failure-recovery-and-rerun-planning/SKILL.md) to classify failed or partial state, preserve evidence, and plan safe recovery, resume, or rerun boundaries.

## v0.1 core skills

- `repo-state-audit`
- `code-review-and-test-audit`
- `resumable-pipeline-design`
- `configuration-and-environment-integrity`
- `hardware-aware-parallelism`
- `data-transfer-and-integrity`

## v0.2 skills

- `read-only-audit-protocol`
- `git-integration-and-release-workflow`
- `prompt-crafting-for-coding-agents`
- `cross-session-handoff-and-continuity`
- `task-dossier-lifecycle`
- `production-run-launch-and-monitoring`
- `failure-recovery-and-rerun-planning`

See [design principles](docs/design-principles.md), [customization guidance](docs/customization.md), and the [volatile documentation policy](docs/volatile-documentation-policy.md) for the repository-wide rules.

Contribution guidelines will be added before external contributions are accepted.
