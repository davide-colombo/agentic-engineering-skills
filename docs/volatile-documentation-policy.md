# Volatile Documentation Policy

Stable engineering principles, durable interfaces, and version-independent procedures may be documented persistently. Facts that can change independently of the repository require verification.

When software behavior, command syntax, service policy, API capability, scheduler behavior, or dependency semantics may have changed, inspect the installed version and consult current official documentation at use time. Record the version and source used for consequential decisions. Do not rely on memory or an undated example.

Public skills must not embed project-specific current state such as active branches, commit identifiers, temporary exceptions, running jobs, deployment status, data locations, or incident details. Put that state in the current task prompt or a session checkpoint, and keep private bindings in project profiles or local overlays.

Cached summaries can help navigation but are non-authoritative unless they identify their source, version or retrieval date, and have been verified for the current task. Mark unverified summaries explicitly and do not use them as the sole basis for destructive, remote, release, or data-integrity decisions.
