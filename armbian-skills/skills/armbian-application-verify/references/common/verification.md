---
schema_version: '1'
id: common.verification
kind: common
applies_to: {}
required_refs:
- common.capability-evidence
preconditions: []
refines: []
excludes: []
related: []
sources: []
validation_refs: []
maturity: documented
owner: armbian-platform-maintainers
updated_at: '2026-10-19'
---

[English](verification.md) | [简体中文](verification.zh-CN.md)

# Task acceptance and evidence

Choose necessary source/build, business, target-access, physical-effect, actual-backend, lifecycle, and service-readiness checks from the user's goal. Regress affected old behavior when extending a project. A standalone hardware demo or simulation does not replace application integration.

Define inputs, duration, resources, stopping method, and pass criteria first. Record actual commands/method, target/time, user/container, artifact/dependencies, output, and evidence source. Separate not-tested, passed, failed, and uncertain results. Use `available/needs-setup/busy/unsupported/unknown` for each operation's four capability layers; process exit alone is not a physical pass.

Check GPIO ownership, normal exit/cancellation, busy resources, disconnection, and relevant failures. Software readback alone does not establish voltage; use an instrument, confirmed wiring, loopback, or specific user observation. Never invent physical actions or readings. Treat request release, direction/configuration restoration, and external-device state separately. Record known original state before restoration and follow [GPIO recovery](../stacks/linux-gpio-chardev/recovery.md); do not guess unknown settings.

For NPU/GPU/VPU, verify output correctness and actual execution backend. Identify CPU/software fallback, and assess video encode/decode and pipeline stages separately. Benchmarks, nominal performance, and CPU utilization cannot replace backend evidence.

When the device is unreachable, continue coding and offline business checks and mark physical validation unperformed. Recheck only affected evidence after environment/input changes. A new combination can receive a bounded test once conditions are known; keep results in the project first. Changes to shared support claims require separate review.

Deliver concise results: implementation/integration locations, build/run instructions, versions/changes, acceptance/regression results, unverified items/next steps, and deployment/recovery. Do not mechanically add an unrelated testing framework.
