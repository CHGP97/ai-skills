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

# PWM application integration

Identify the actual provider/channel, connector electrical conditions, and owner. Use the PWM API available on the target. Do not take system resources such as thermal fans or backlights. Record period/duty/polarity and startup, stop, and failure behavior. Software configuration readback does not establish a waveform; measure frequency and duty cycle. Do not guarantee the level after disable without evidence.
