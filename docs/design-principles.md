# Design Principles

## Reproducibility

Record inputs, configuration, environment assumptions, commands, and outputs needed to reproduce a result. Prefer versioned configuration over undocumented session state.

## Inspectability

Make decisions, state transitions, validation evidence, and failure conditions visible. An operator should be able to determine what an agent observed and why it acted.

## Resumability

Design long or failure-prone work around checkpoints, idempotent stages, explicit completion markers, and safe restart behavior.

## Explicit state

Inspect branch, revision, filesystem state, configuration, data location, and authorization rather than inferring them from convention.

## Fail loud over silent repair

Stop and report unexpected state. Do not hide mismatches by silently cleaning, rewriting, retrying with broader permissions, or changing configuration.

## Deterministic validation

Move non-negotiable checks into hooks or scripts with stable inputs and machine-checkable outcomes. Use agent judgment for interpretation, not enforcement that can be deterministic.

## Hardware-aware execution

Match concurrency, memory, storage, accelerator, and scheduler choices to observed resources. Avoid fixed assumptions about a local machine or compute environment.

## Data integrity

Verify identity, completeness, checksums, schema, provenance, and overwrite policy at data boundaries. Treat transfer completion and analytical validity as separate claims.

## Minimal always-on context

Keep always-loaded instructions short, stable, and task-agnostic. Load specialized procedures and project bindings only when relevant.

## Project-specific privacy

Keep private paths, infrastructure, credentials, unpublished data, current project state, and internal policy out of public skills. Bind public procedures to those facts in private profiles and overlays.
