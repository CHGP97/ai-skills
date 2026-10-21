---
schema_version: '1'
id: stack.rockchip-rknn.verification
kind: stack_guide
applies_to:
  capabilities:
  - npu
  stack_ids:
  - rockchip-rknn
  soc_ids:
  - rockchip.rk3576
  - rockchip.rk3588
required_refs: []
preconditions: []
refines: []
excludes: []
related: []
sources:
- source.local-kernel-config
- source.cached-vendor-dts
- source.rknn-project
validation_refs: []
maturity: documented
owner: armbian-platform-maintainers
updated_at: '2026-10-20'
---

[English](verification.md) | [简体中文](verification.zh-CN.md)

# Rockchip RKNPU and compatible RKNN runtime: verification

Fix model/input and correctness criteria. Retain actual runtime/device execution evidence and separate end-to-end/inference timings. Establish current kernel driver, userspace runtime, binding, model, and functional readiness on the target; these are not supplied by static profiles.

Compare known output/error bounds, then inspect actual compute Target and nonzero cycles, not just API return 0 or the word NPU. Distinguish CPU I/O conversion from whole-model CPU fallback; explicit fallback does not count as hardware success. Check which DRM/device node the SDK really opens and permissions for the actual service user. After completion/error/cancellation inspect contexts/processes/FDs; power state is not proof of release.
