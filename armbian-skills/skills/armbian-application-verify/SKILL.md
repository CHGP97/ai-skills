---
name: armbian-application-verify
description: 'Verify and diagnose Armbian hardware applications: business behavior, physical effects, actual acceleration
  backends, permissions, and lifecycle. Use for existing-project regression, services with unresponsive peripherals,
  and NPU/GPU/VPU fallback. Distinguish source/mock tests, current observations, and physical acceptance.'
---

[English](SKILL.md) | [简体中文](SKILL.zh-CN.md)

# Armbian application verification

Use reproducible evidence to determine whether the requested application feature works and identify unmet conditions.

## Subject and acceptance criteria

Read the existing plan, project test/deployment conventions, target, source/artifact digests, inputs, and actual user/container. Choose relevant checks rather than automatically introducing a framework or running every hardware stress test.

Start with this package's [index](references/INDEX.md), reference-release.yaml, [four evidence layers](references/common/capability-evidence.md), and [verification guide](references/common/verification.md). Select capability, board/revision, actual stack, and language using the [matching contract](references/common/reference-matching.md):

```bash
python3 scripts/reference-match/match.py --input /path/to/task-facts.json
```

Use current device facts. Historical reports/inventory cannot establish this task's functional pass. Reference matching is neither execution permission nor a support claim. Refresh affected evidence after target/runtime/user/container/application/input changes.

## Relevant checks

- Source/build and business: input/output, configuration, errors, timeout, concurrency. Integrate new behavior through original entry points and regress affected old functions. For persistent operations, check before/during/after behavior, initiating-request completion, business cancellation, and shutdown.
- Application access: check libraries, devices, permissions, and owners in the actual service/container environment. Root-shell examples do not establish application access.
- GPIO: confirm mapping, electrical conditions, wiring, mux, and authorization before testing initial values, hold, end/cancel/failure, and release. Readback alone is not voltage evidence. Separate request release, direction/configuration restoration, and measured voltage. Follow [known-state recovery](references/stacks/linux-gpio-chardev/recovery.md) and relevant [GPIO checks](references/capabilities/gpio/verification.md).
- Communication/camera/PWM: use confirmed protocols, real peers/loopback, frames, or instruments. Command success does not prove function. Do not scan internal I2C or seize drivers/shared services.
- NPU: fix model/input/preprocessing and check correctness plus actual execution device/runtime. Read [NPU verification](references/capabilities/npu/verification.md).
- GPU: check graphics/compute APIs, renderer/device/provider, and output separately, identifying software fallback. Read [GPU verification](references/capabilities/gpu/verification.md).
- VPU: verify encode/decode by codec/profile/bit depth/resolution, output, and each stage's backend. Feature lists/CPU use do not replace execution evidence. Read [VPU verification](references/capabilities/vpu/verification.md).
- Lifecycle/services: readiness, cancellation, disconnection, missing dependencies, restart policy, and recovery. Functional checks need explicit inputs, bounds, resources, and stopping methods.

## Record and diagnose

Use available/needs-setup/busy/unsupported/unknown for hardware/interfaces, system, application access, and functional layers. Record test results as passed/failed/not-tested/uncertain with target, time, method, version, and evidence. Preserve fallback and partial outcomes without declaring the whole pipeline available.

Separate user reports, software observations, and instrument/loopback measurements. Never invent physical actions. If the target is unreachable, continue offline business tests and state hardware remains unverified. Distinguish application, permissions, ownership, configuration, and driver faults. Unknown is not unsupported, and diagnosis does not justify unrelated low-level changes.

Deliver passed checks, failure causes/fixes, relevant regression, remaining conditions, and reproduction/recovery steps. Save evidence in the project first; do not automatically rewrite shared matrices or cross-platform support claims.
