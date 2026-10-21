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

# Rockchip RKNPU + compatible RKNN runtime: detection

检查 platform driver、实际设备访问节点、runtime 库和包版本。节点名不能固定为 /dev/rknpu；以实际 driver/runtime 发现为准。
