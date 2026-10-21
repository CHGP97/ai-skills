---
schema_version: '1'
id: platform.rockchip.rk3588.peripherals
kind: platform_guide
applies_to:
  soc_ids:
  - rockchip.rk3588
required_refs:
- platform.rockchip.rk3588
preconditions: []
refines: []
excludes: []
related: []
sources:
- source.local-rk3588-board
- source.local-rk3588-dts
validation_refs: []
maturity: documented
owner: armbian-platform-maintainers
updated_at: '2026-10-19'
---

[English](peripherals.md) | [简体中文](peripherals.zh-CN.md)

# rk3588 外设资料边界

控制器能力不等于载板实际引出。GPIO/I2C 复用通用 Linux API 接入方法，当前目标仍需解析驱动、adapter/controller 身份和权限；没有已审核的物理映射时不操作排针。
