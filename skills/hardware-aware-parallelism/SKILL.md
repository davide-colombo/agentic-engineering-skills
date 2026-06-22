---
name: hardware-aware-parallelism
description: Design, audit, or review parallel execution, worker topology, resource allocation, hidden threading, memory pressure, I/O contention, and scaling behavior. Use when computational software or data-intensive pipelines need explicit resource budgets, safe concurrency, measurable scaling evidence, failure isolation, or production-readiness assessment across target hardware and runtime constraints.
---

# Hardware-Aware Parallelism

## Purpose

Determine whether parallel execution is correct, resource-bounded, observable, and appropriate for the target hardware and workload. Detect oversubscription, hidden threading, unsafe shared outputs, memory or I/O saturation, weak backpressure, and scaling claims unsupported by measurement.

## When to use

Use when designing or changing concurrency, reviewing worker or queue topology, diagnosing utilization or throughput, sizing production execution, integrating external parallel tools, or auditing whether runtime resource controls match declared configuration.

## When not to use

Do not use as authorization to tune system settings, change schedulers or containers, provision hardware, launch expensive workloads, or modify dependencies. Do not substitute it for correctness, configuration, resumability, security, or domain validation. When repository or configuration integrity is unknown, perform the applicable audit first.

## Required inputs

Obtain from the current prompt and authoritative project material:

- Task objective, selected task mode, allowed scope, and acceptance criteria.
- Supported entry points and the relevant execution, worker, queue, subprocess, and output-writing paths.
- Target hardware constraints and applicable operating-system or runtime constraints.
- Declared parallelism controls, resource limits, configuration precedence, and production caps.
- Unit-of-work definition and known CPU, memory, storage, network, accelerator, or external-tool demands.
- Expected validation commands and available measurement evidence.

If the objective, scope, execution boundary, target constraints, or resource authority cannot be established reliably, stop and report. Do not invent machine-specific assumptions absent from the current prompt, project profile, local overlay, on-disk documentation, or measurements from the target machine.

## Optional inputs

Use when supplied or discoverable within scope:

- Hardware inventory, runtime topology, scheduler or container limits, and storage layout.
- Profiles, benchmarks, utilization traces, queue metrics, failure logs, and throughput histories.
- Per-unit resource measurements, input-size distributions, and concurrency experiments.
- Runtime, numerical-library, compression, external-tool, and subprocess threading documentation.
- Temporary-directory policy, filesystem characteristics, accelerator topology, and network constraints.
- Service-level objectives, cost limits, latency targets, and expected workload variance.

Treat missing optional evidence as uncertainty, not as permission to assume safe scaling.

## Task modes

Choose exactly one mode and state it in the report:

- `PARALLELISM_DESIGN_REVIEW`: Evaluate a proposed concurrency model, resource budget, topology, isolation strategy, and observability before implementation.
- `RESOURCE_AUDIT`: Compare declared and actual CPU, memory, storage, network, accelerator, and runtime resource use against target limits.
- `OVERSUBSCRIPTION_AUDIT`: Trace explicit and hidden concurrency layers to determine whether aggregate threads, processes, memory, or I/O can exceed the budget.
- `PERFORMANCE_TRIAGE`: Diagnose measured throughput, latency, utilization, contention, or scaling behavior without assuming that utilization alone identifies the cause.
- `PRODUCTION_READINESS_AUDIT`: Assess caps, isolation, backpressure, failure behavior, observability, and evidence for sustained target operation.
- `POST_CHANGE_AUDIT`: Review implemented parallelism changes against scope, runtime consumption, resource safety, correctness contracts, and validation evidence.

A mode changes audit emphasis; it does not authorize edits, system changes, expensive execution, or work outside the allowed scope.

## Hardware model

Describe the target as constrained resources, not merely a machine label:

- Available physical CPU cores, logical hardware threads, affinity or quota restrictions, and shared-host uncertainty.
- Usable memory, per-process or container limits, expected resident working set, and swap or paging policy.
- Storage layout, capacity, bandwidth, latency, metadata behavior, and temporary-space limits when relevant.
- Network filesystem or remote I/O bandwidth, latency, request limits, and shared contention when relevant.
- Accelerator availability, usable memory, device sharing, transfer costs, and supported execution paths when relevant.
- Operating-system, runtime, scheduler, container, process, file-descriptor, and subprocess constraints when relevant.

Separate discovered capacity from allocated capacity and requested capacity. Use the lowest applicable enforceable limit as the usable budget. Record whether each fact is declared, observed, measured, or assumed.

## Workload model

Define the unit of work and classify each important phase using these terms:

- `CPU-bound workload`: Throughput is principally limited by compute capacity.
- `memory-bound workload`: Throughput is principally limited by memory capacity, bandwidth, locality, or allocation behavior.
- `I/O-bound workload`: Throughput is principally limited by local storage operations or filesystem behavior.
- `network-bound workload`: Throughput is principally limited by remote transfer, service, or network-filesystem behavior.
- `scheduler-bound workload`: Progress is principally limited by dispatch, queue, startup, synchronization, or coordination overhead.
- `single-threaded section`: A phase that can use at most one execution thread or equivalent serial resource.
- `embarrassingly parallel workload`: Units can execute independently without shared mutable state or cross-unit coordination during execution.
- `nested parallelism`: One concurrency layer launches work that is itself concurrent.
- `hidden threading`: A library, runtime, compressor, external tool, accelerator stack, or subprocess creates concurrency not represented by the top-level worker setting.
- `oversubscription`: Aggregate runnable work or resource demand exceeds the declared usable budget and causes unsafe pressure or harmful contention.
- `undersubscription`: Available resources remain unused despite runnable independent work and no justified limiting constraint.
- `memory pressure`: Working sets, buffers, caches, or duplication approach or exceed safe usable memory.
- `swap or paging risk`: Memory demand can trigger material paging, swapping, eviction, or equivalent performance collapse.
- `I/O contention`: Concurrent access competes for storage, metadata, network, or service capacity and degrades useful throughput or reliability.
- `unsafe shared output path`: Concurrent units can mutate, replace, append to, or clean the same output without proven isolation, atomicity, or locking.
- `worker-local failure`: A failure can be attributed to and contained within one worker or unit without invalidating independent completed work.
- `global resource failure`: Exhaustion or failure of a shared resource threatens multiple workers, shared state, or the entire run.
- `expected low utilization`: Low observed use is explained by the current phase, dependency, serial section, backpressure, or intentional cap.
- `pathological low utilization`: Low observed use contradicts runnable work and stated goals because of avoidable blocking, imbalance, starvation, serialization, or configuration failure.

For each phase, estimate or measure per-unit CPU, memory, local I/O, remote I/O, accelerator, subprocess, and temporary-space cost. State how cost changes with input size and concurrency.

## Parallelism model

Define all concurrency layers and their composition:

- Job-level thread count and number of concurrent jobs or workers.
- Maximum processes, threads, subprocesses, external-tool instances, and accelerator tasks per unit and per run.
- Process-versus-thread choice and its correctness, isolation, memory-sharing, runtime, and overhead implications.
- Worker lifecycle, initialization cost, reuse, teardown, cancellation, timeout, and leak behavior.
- Queue capacity, admission control, fairness, work stealing when present, and backpressure behavior.
- Nested parallelism and hidden-thread controls across libraries, runtimes, compression, external tools, and subprocesses.
- Worker-local state, temporary directories, output paths, logging identity, and failure boundaries.

Compute a defensible upper bound for each constrained resource. At minimum, account for `concurrent jobs × per-job explicit concurrency × hidden or nested concurrency`, plus coordinator and background overhead. Do not present the product as exact when layers overlap or runtime behavior is dynamic; state the bounding assumptions.

## Audit procedure

1. Restate the objective, scope, selected mode, entry points, target constraints, and material unknowns.
2. Trace every parallelism configuration value from declaration and precedence resolution to its actual runtime consumer. Flag accepted-but-unused controls and implicit defaults.
3. Map stages and phases to units of work, workload classifications, dependencies, shared state, and aggregation barriers.
4. Inventory every process, thread, task, external tool, runtime pool, library pool, subprocess, and accelerator execution layer.
5. Build CPU, memory, temporary-space, storage, network, accelerator, and descriptor budgets for the maximum admitted concurrency.
6. Inspect worker topology, lifecycle, queueing, backpressure, cancellation, timeouts, failure isolation, and cleanup.
7. Inspect temporary-directory placement and concurrent output behavior. Require isolation, atomic writes, or proven locking for mutable shared paths.
8. Evaluate hidden threading, nested parallelism, memory duplication, buffering, cache growth, and I/O fan-out.
9. Confirm resource limits and required tools are validated before expensive execution, and failures identify the responsible unit or shared resource.
10. Inspect per-worker or per-unit logs, progress reporting, throughput, latency, queue depth, memory, I/O, retry, and failure evidence.
11. Compare scaling claims with actual measurements when available. Explain expected low utilization by phase before treating it as a defect.
12. Classify findings, identify validation gaps, and select exactly one verdict.

## Resource-budget procedure

1. Record allocated CPU cores or threads, memory, storage, temporary space, network or remote-I/O capacity, accelerators, and applicable runtime limits.
2. Estimate or measure coordinator overhead and per-unit peak CPU, resident memory, temporary storage, file descriptors, local I/O, remote I/O, and accelerator use.
3. Calculate maximum concurrent demand from admitted jobs, explicit per-job parallelism, hidden threads, subprocesses, retries, buffering, and background work.
4. Add a stated safety margin for measurement variance, workload skew, runtime overhead, and shared-host uncertainty.
5. Compare maximum demand with enforceable limits. Classify oversubscription, memory pressure, swap or paging risk, I/O contention, and global resource failure paths.
6. Confirm configuration caps are actually consumed at runtime and invalid values fail before expensive work starts.
7. Do not increase worker counts without a resource budget. Prefer explicit resource caps over implicit runtime defaults.

## Worker-topology procedure

1. Map producers, queues, coordinators, workers, subprocesses, shared services, writers, and aggregation barriers.
2. Justify the process-versus-thread choice using workload, isolation, shared-state, runtime, and overhead evidence.
3. Inspect queue bounds and backpressure. An unbounded queue or producer can transfer pressure into memory, storage, remote services, or shutdown behavior.
4. Verify worker lifecycle, initialization, reuse, cancellation, graceful shutdown, cleanup, and recovery from worker-local failure.
5. Check load balance for variable unit cost, stragglers, affinity constraints, serial sections, and scheduler overhead.
6. Require unique worker or unit identity in logs, progress, temporary paths, and outputs.
7. Do not run multiple jobs into the same mutable output path unless isolation or locking is proven. Prefer isolated temporary directories for parallel units.

## Hidden-threading procedure

1. Inspect numerical libraries, runtimes, compression tools, external tools, subprocesses, accelerator stacks, and other components that may create threads or processes.
2. Determine each layer's default, configured cap, environment controls, inheritance behavior, and actual runtime consumption.
3. Combine top-level workers with nested and hidden concurrency to establish a safe upper bound.
4. Verify that child processes and external tools receive intended caps rather than ambient machine-wide defaults.
5. Exercise or inspect representative execution paths because import, discovery, or configuration parsing does not prove runtime thread control.
6. Do not allow nested parallelism to exceed the declared resource budget. Do not ignore hidden runtime or library threads.

## Memory and I/O procedure

1. Identify worker-private, shared, copied, buffered, cached, memory-mapped, and accelerator-resident data.
2. Estimate or measure peak memory across workers, coordinator, queues, retries, serialization, and external tools; include skew and overlapping phases.
3. Check for memory pressure and swap or paging risk before raising concurrency.
4. Map reads, writes, metadata operations, temporary files, remote requests, and aggregation to the actual storage and network layout.
5. Assess I/O contention, request amplification, burst behavior, bandwidth ceilings, metadata hot spots, and remote-service limits.
6. Verify temporary capacity, placement, cleanup, worker isolation, and behavior after interruption or failure.
7. Verify atomic output behavior and prohibit unsafe shared output paths without proven locking or isolation.

## Scaling and observability procedure

1. Define the baseline, workload size, target hardware, concurrency settings, warm-up policy, repetitions, and throughput or latency metric.
2. Compare useful throughput, elapsed time, efficiency, memory, I/O, queue depth, failures, retries, and output correctness across concurrency levels.
3. Distinguish startup, serial, compute, memory, I/O, network, synchronization, and aggregation phases before interpreting utilization.
4. Do not assume more workers make a workload faster. Identify saturation, overhead, contention, imbalance, and failure-rate changes.
5. Treat low CPU usage as expected only when the current phase or limiting resource explains it; otherwise investigate pathological low utilization.
6. Do not treat high CPU usage as efficient scaling without checking throughput, memory, I/O, and failure rate.
7. Require per-worker or per-unit identity, progress, durations, queue state, resource-cap reporting, and actionable failure context for production readiness.
8. Prefer measurable throughput evidence over intuition. Report measurements as environment-specific unless portability is established.

## Risk classification

Assign each finding one primary category and a severity of `BLOCKING` or `NON_BLOCKING`:

- `resource safety`: CPU, memory, storage, network, accelerator, descriptor, or temporary-space demand can exceed safe limits.
- `topology and coordination`: Worker lifecycle, queueing, backpressure, scheduling, cancellation, or synchronization threatens progress or correctness.
- `hidden or nested parallelism`: Undeclared concurrency defeats caps or creates oversubscription.
- `memory and I/O`: Memory pressure, paging, buffering, storage, metadata, or remote-I/O contention threatens reliability or throughput.
- `output integrity`: Concurrent writers, shared temporary state, cleanup, or non-atomic mutation can corrupt or misattribute results.
- `failure isolation`: Worker-local failures propagate globally, shared-resource failures are misclassified, or recovery cannot identify affected units.
- `scaling evidence`: Claims lack comparable measurements or confuse utilization with useful throughput.
- `observability`: Resource use, phase, progress, worker identity, queue state, or failures cannot be diagnosed adequately.
- `configuration/runtime parity`: Declared parallelism controls are ignored, overridden unexpectedly, or not validated before expensive execution.
- `scope violation`: Work or requested side effects exceed authorized scope.
- `non-blocking improvement`: A substantiated improvement that does not threaten correctness, safety, resource bounds, or the applicable contract.

Use `BLOCKING` for unsafe aggregate demand, unbounded pressure, ignored resource caps, unsafe shared output paths, uncontrolled nested parallelism, missing preflight limits, or evidence gaps that prevent a reliable production-readiness conclusion. Explain the observable consequence and minimum resolution.

## Stop-and-report triggers

Stop before mutation, expensive execution, system changes, or broader measurement when:

- The objective, scope, selected mode, target hardware, workload boundary, or authority cannot be established.
- Required resource limits are unknown or aggregate maximum demand cannot be bounded safely.
- Hidden or nested parallelism can exceed the declared budget.
- Concurrent units can mutate the same output or temporary state without proven isolation, atomicity, or locking.
- Memory pressure, paging risk, I/O contention, or a global resource failure can corrupt output or destabilize execution.
- Required validation would launch expensive work, contact external systems, modify scheduler, container, dependency, or system settings, or exceed authorization.
- Parallelism controls are accepted but not consumed at runtime, or invalid limits are not rejected before expensive execution.
- Production readiness is requested without clear resource caps, failure isolation, and observability.
- Available measurements cannot distinguish expected from pathological low utilization or support the claimed scaling behavior.

Report the trigger, evidence, affected phase or resource, likely impact, and minimum decision, measurement, or authorization required. Prefer fail-loud reporting over silent tuning.

## Output contract

Produce these sections:

1. `VERDICT`: exactly one verdict and a one-sentence rationale.
2. `MODE AND SCOPE`: selected mode, objective, allowed scope, entry points, target hardware, workload, and exclusions.
3. `HARDWARE MODEL`: declared, allocated, observed, and assumed CPU, memory, storage, network, accelerator, operating-system, and runtime constraints.
4. `WORKLOAD MODEL`: units, phases, dependencies, workload classifications, per-unit costs, shared state, and aggregation barriers.
5. `PARALLELISM MODEL`: jobs, workers, threads, processes, subprocesses, hidden concurrency, lifecycle, queues, backpressure, and maximum topology.
6. `RESOURCE BUDGET`: formulas, measurements, assumptions, safety margins, enforceable caps, and peak aggregate demand by resource.
7. `MEMORY, I/O, AND OUTPUT SAFETY`: pressure, paging risk, temporary placement, contention, shared paths, atomicity, locking, and cleanup.
8. `SCALING AND OBSERVABILITY EVIDENCE`: commands or experiments actually run, environment, throughput, utilization, queue behavior, failures, and limitations.
9. `FINDINGS`: blocking findings and non-blocking warnings with category, location or phase, evidence, consequence, and minimum resolution; write `none` for empty categories.
10. `VALIDATION GAPS`: checks not run, reasons, and impact on the verdict.
11. `NEXT STEP`: the minimum correction, measurement, authorization, or integration action supported by the verdict.

Do not report a limit, topology, measurement, scaling result, or target-machine fact as verified unless supporting evidence was inspected or executed.

## Allowed actions

- Read task instructions, project profiles, overlays, configuration, execution code, worker topology, manifests, logs, measurements, and target constraints within scope.
- Run local read-only inspection and explicitly authorized safe validation or bounded measurement commands.
- Query available runtime or hardware information when it is safe, relevant, and within scope.
- Calculate resource bounds, map concurrency layers, compare runtime consumption with declared controls, and assess scaling evidence.
- Propose corrections, caps, instrumentation, or experiments without applying them unless separately authorized.
- Report uncertainty, unrun validation, and the minimum evidence or authorization needed.

## Forbidden actions

- Increase worker counts or claim safe concurrency without a resource budget.
- Assume more workers improve performance or that utilization alone proves success or failure.
- Ignore hidden threads, nested parallelism, subprocesses, retries, buffering, or background work.
- Modify scheduler, container, dependency, runtime, firmware, operating-system, or system-level settings without explicit authorization.
- Launch expensive, production, remote, or externally consequential workloads without explicit authorization.
- Use machine-specific assumptions not supplied by the current prompt, project profile, local overlay, on-disk documentation, or target measurements.
- Permit multiple jobs to mutate one output path without proven isolation, atomicity, or locking.
- Conceal unsafe resource demand, memory pressure, paging risk, I/O contention, worker failures, ignored controls, or missing evidence.
- Claim production readiness without explicit caps, failure isolation, actionable observability, and sufficient validation evidence.
- Broaden scope or silently tune or repair findings during an audit.

## Verdict vocabulary

- `PARALLELISM_READY`: The selected mode's parallelism, resource bounds, output safety, failure isolation, observability, and validation evidence satisfy the applicable contracts with no remaining warnings.
- `PARALLELISM_READY_WITH_WARNINGS`: No blocking finding remains, but substantiated non-blocking limitations, measurement gaps, or residual risks are explicitly reported.
- `NEEDS_REVISION`: One or more correctable blocking topology, configuration, isolation, observability, or scaling findings prevent acceptance.
- `RESOURCE_UNSAFE`: Available evidence demonstrates that aggregate demand, contention, shared-state behavior, or uncontrolled concurrency violates safe resource or output constraints.
- `BLOCKED`: Missing inputs, inaccessible evidence, unsafe conditions, or unavailable essential validation prevent a reliable conclusion.
- `OUT_OF_SCOPE`: The requested audit, tuning, execution, system change, or material component exceeds authorized scope.

When several verdicts apply, use `OUT_OF_SCOPE` for unauthorized scope, `BLOCKED` when evidence cannot support a conclusion, `RESOURCE_UNSAFE` for demonstrated unsafe resource or output behavior, and `NEEDS_REVISION` for correctable blocking findings. Use a ready verdict only when no blocking finding remains and evidence is sufficient for the selected mode.
