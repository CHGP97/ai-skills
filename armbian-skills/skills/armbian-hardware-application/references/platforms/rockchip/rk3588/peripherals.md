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

# RK3588 peripheral reference boundaries

Controller capability does not establish carrier exposure. Reuse generic Linux GPIO/I2C integration methods while resolving actual driver, adapter/controller identity, and permissions. Do not operate header pins without reviewed physical mapping.
