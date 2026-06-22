# Deterministic Hook Examples

Hooks are for checks that must be enforced consistently and can be expressed deterministically. A skill may explain when and why a rule applies; a hook or script should block the prohibited transition with a clear, machine-checkable result.

Useful hook categories include:

- Block a release from a dirty working tree.
- Forbid committing machine-specific configuration.
- Require designated tests before a version bump.
- Validate version consistency across declared metadata files.
- Block unauthorized remote execution.
- Block destructive overwrite of existing outputs.

Keep hooks narrow, fast, auditable, and explicit about failure. Define their inputs and exit codes, test both allowed and blocked cases, and do not embed credentials or private infrastructure details in public examples.
