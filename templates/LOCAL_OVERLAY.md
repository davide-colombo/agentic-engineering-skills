# Local Skill Overlay

This private overlay binds a public skill to one project. Load it after the public skill and the project profile. Keep the public skill unchanged so upstream improvements remain reviewable and reusable. Store the customized copy at a project-defined private location; `.skills-local/<skill-name>.local.md` and `.claude/skills/<skill-name>/LOCAL_OVERLAY.md` are examples, not required paths.

## Applies to

- Base skill: `[PUBLIC_SKILL_NAME_AND_VERSION]`
- Project profile: `[PROJECT_PROFILE_PATH]`
- Overlay scope: `[TASKS_OR_DIRECTORIES]`

## Project-specific bindings

- Command substitutions: `[PROJECT_COMMANDS]`
- Path and branch bindings: `[PROJECT_PATHS_AND_BRANCHES]`
- Additional required checks: `[ADDITIONAL_CHECKS]`
- Stricter stop conditions: `[STRICTER_STOP_CONDITIONS]`
- Domain terminology: `[DOMAIN_TERMS]`
- Reporting additions: `[REPORTING_ADDITIONS]`

## Constraints

An overlay may supply missing project values or impose stricter controls. It must not weaken platform rules, the current task, always-on instructions, protected-branch policy, forbidden-path policy, or the base skill's safety boundaries. Keep credentials, secrets, transient state, machine-specific paths, and current job details out of the overlay.
