---
schema_version: '1'
id: capability.spi
kind: capability
applies_to:
  capabilities:
  - spi
required_refs:
- common.linux-device-access
preconditions: []
refines: []
excludes: []
related: []
sources:
- source.linux-spidev
validation_refs: []
maturity: documented
owner: armbian-platform-maintainers
updated_at: '2026-10-19'
---

[English](overview.md) | [简体中文](overview.zh-CN.md)

# SPI application integration

Confirm the external device, voltage, chip select, mode, bit order, and speed. Resolve nodes from actual device identity. Read/write and combined transactions have different chip-select behavior; choose the interface required by the device protocol. Use an existing driver's interface rather than forcibly rebinding it. A successful SPI call can occur without a device response: check peer protocol/data or an explicit loopback.
