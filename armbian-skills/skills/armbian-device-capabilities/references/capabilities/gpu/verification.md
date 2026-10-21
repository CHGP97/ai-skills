---
schema_version: '1'
id: capability.gpu.verification
kind: capability_guide
applies_to:
  capabilities:
  - gpu
required_refs:
- capability.gpu
- common.verification
preconditions: []
refines: []
excludes: []
related: []
sources: []
validation_refs: []
maturity: documented
owner: armbian-platform-maintainers
updated_at: '2026-10-19'
---

[English](verification.md) | [简体中文](verification.zh-CN.md)

# GPU verification

Test each graphics or compute API separately. Record renderer/device/provider, context creation, and output. Software rendering and CPU fallback do not count as hardware passes. Successful rendering does not establish OpenCL/Vulkan compute support; a desktop-user result does not establish headless-service access.
