# Customization

Public skills define reusable procedures. Adapt them to a private project without publishing the project's current state or infrastructure.

## Adoption patterns

### Use as-is

Copy a skill unchanged when its inputs can be supplied by the current task and no project-specific commands or policies are required. This keeps upstream comparison simple.

### Copy and specialize

Create a private derivative when the procedure itself must materially differ. Preserve the original safety properties, document the divergence, and review upstream changes deliberately.

### Base skill plus local overlay

Prefer an unchanged public base skill plus a private local overlay for branch names, paths, commands, terminology, infrastructure policy, and stricter checks. Load the project profile, selected public skill, and overlay after establishing the current task prompt.

Copy the templates into private project-controlled locations and customize the copies. For example:

```sh
cp templates/PROJECT_PROFILE.md path/to/project/PROJECT_PROFILE.md
cp templates/PROJECT_PROFILE.md path/to/project/.agents/PROJECT_PROFILE.md
cp templates/LOCAL_OVERLAY.md path/to/project/.skills-local/repo-state-audit.local.md
cp templates/LOCAL_OVERLAY.md path/to/project/.claude/skills/repo-state-audit/LOCAL_OVERLAY.md
```

These paths are examples, not requirements. Choose one profile location and one overlay convention appropriate to the agent integration, then reference them from the project's always-on instructions.

Apply this canonical model: current task prompt, project profile, selected public skill, local overlay, observed evidence, then hooks or scripts for deterministic enforcement. The first four layers provide instructions and project bindings. Observed state is evidence, not a lower-priority instruction; stop and report when it contradicts instructions or assumptions. Hooks and scripts enforce non-negotiable checks at execution time and are not advisory. An overlay may specialize the selected skill but must not weaken the skill, project profile, or current prompt unless the current task prompt explicitly authorizes an exception.

## What to customize

Customize the project profile with repository identity, protected and source-of-truth branches, dirty-file rules, local-only and forbidden paths, dependency policy, validation and release commands, remote execution and deployment policy, domain vocabulary, and reporting format. Customize overlays only where a particular skill needs additional project bindings.

Keep task-specific expected branch or HEAD, temporary authorization, active job identifiers, current incidents, and checkpoint state in the current prompt or session checkpoint.

## What not to publish

Do not put credentials, tokens, private repository names, personal names, machine paths, SSH aliases, internal hosts, unpublished research data, institution-specific infrastructure, current project state, or temporary exceptions in public skills. Do not encode volatile third-party software behavior as timeless fact; require verification at use time.
