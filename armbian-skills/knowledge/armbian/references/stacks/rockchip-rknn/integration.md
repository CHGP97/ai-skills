---
schema_version: '1'
id: stack.rockchip-rknn.integration
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

[English](integration.md) | [简体中文](integration.zh-CN.md)

# Rockchip RKNPU and compatible RKNN runtime: integration

Check current driver/runtime and model target, then choose an existing binding, C ABI/FFI, or service API in the user's language. Treat conversion, calibration, and execution separately; do not directly reuse an external RK182x example.

Use explicit official tags/file digests. Record conversion Toolkit version, target SoC, actual runtime/header/driver, and application architecture. Master/latest is not the installed version. If runtime is missing, suitable task-local dependencies may be enough without replacing drivers or installing a generic control service. Preserve existing models/bindings; an example version is not a future compatibility whitelist.

Query actual input/output counts, shape/layout/dtype instead of filling RKNN inputs from original ONNX attributes. Define pass_through, normalization, and output-float conversion. Preserve business entry points and use the language's async lifecycle for persistent work. Release outputs/context, and verify actual owner exit after errors/cancellation.
