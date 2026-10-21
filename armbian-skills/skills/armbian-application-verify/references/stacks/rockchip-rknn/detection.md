---
schema_version: '1'
id: stack.rockchip-rknn.detection
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
updated_at: '2026-10-19'
---

[English](detection.md) | [简体中文](detection.zh-CN.md)

# Rockchip RKNPU and compatible RKNN runtime: detection

Inspect platform driver, actual access nodes, runtime library, and package versions. Do not fix the device name to /dev/rknpu; discover the actual driver/runtime path.
