---
schema_version: '1'
kind: stack_guide
applies_to:
  capabilities:
  - gpu
  soc_ids:
  - rockchip.rk3588
  stack_ids:
  - mesa-panthor
required_refs:
- stack.mesa-panthor
preconditions: []
refines: []
excludes: []
related: []
sources:
- source.local-rk3588-board
validation_refs: []
maturity: documented
owner: armbian-platform-maintainers
updated_at: '2026-10-19'
id: stack.mesa-panthor.verification
---

[English](verification.md) | [简体中文](verification.zh-CN.md)

# Panthor / Mesa verification

记录实际 renderer/device/provider 与输出并识别软件渲染；图形/计算分别验收。当前没有 RK3588 实机或应用结果，不能从构建配置宣称功能通过。
