# Project Profile

Replace every placeholder. Keep stable private project facts here; put current task state in the task prompt or session checkpoint. Store the customized copy at a project-defined private location; `PROJECT_PROFILE.md` and `.agents/PROJECT_PROFILE.md` are examples, not required paths.

## Identity

- Project name: `[PROJECT_NAME]`
- Repository root: `[REPOSITORY_ROOT]`
- Source-of-truth branch: `[SOURCE_OF_TRUTH_BRANCH]`
- Protected branches and restrictions: `[PROTECTED_BRANCH_POLICY]`

## Repository state policy

- Allowed dirty files or patterns: `[ALLOWED_DIRTY_FILES]`
- Local-only files or patterns: `[LOCAL_ONLY_FILES]`
- Forbidden paths or patterns: `[FORBIDDEN_PATHS]`

Define whether patterns use exact paths, shell globs, or another documented syntax.

## Commands and environment

- Dependency manager and lockfile policy: `[DEPENDENCY_MANAGER]`
- Test commands: `[TEST_COMMANDS]`
- Build commands: `[BUILD_COMMANDS]`
- Release commands: `[RELEASE_COMMANDS]`

## Execution and deployment

- Remote execution policy: `[REMOTE_EXECUTION_POLICY]`
- Deployment policy: `[DEPLOYMENT_POLICY]`

State required approvals, permitted targets, credential boundaries, data restrictions, and destructive-operation rules without embedding secrets.

## Domain and reporting

- Domain vocabulary: `[DOMAIN_VOCABULARY]`
- Required reporting format: `[REPORTING_FORMAT]`
