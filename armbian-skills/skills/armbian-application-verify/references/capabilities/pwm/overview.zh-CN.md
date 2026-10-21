---
schema_version: '1'
id: capability.pwm
kind: capability
applies_to:
  capabilities:
  - pwm
required_refs:
- common.linux-device-access
preconditions: []
refines: []
excludes: []
related: []
sources:
- source.linux-pwm
validation_refs: []
maturity: documented
owner: armbian-platform-maintainers
updated_at: '2026-10-19'
---

[English](overview.md) | [简体中文](overview.zh-CN.md)

# PWM 应用接入

识别实际 provider/channel、连接器电气和占用，使用系统实际提供的 PWM API。不得占用热管理风扇/背光等系统资源。记录 period/duty/polarity、启动/停止和异常行为；软件配置读回不等于实际波形，输出频率与占空比需测量。disabled 后的电平不能无依据保证。
