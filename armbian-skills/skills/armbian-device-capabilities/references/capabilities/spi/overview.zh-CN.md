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

# SPI 应用接入

确认外部器件、电压、CS、模式、位序和速率。按实际设备身份解析节点；read/write 与组合事务的片选行为不同，选择符合器件协议的接口。现有驱动占用时使用驱动提供接口，不强制重绑。无设备时 SPI 调用成功也可能没有有效回应，应校验对端协议、数据或明确回环。
