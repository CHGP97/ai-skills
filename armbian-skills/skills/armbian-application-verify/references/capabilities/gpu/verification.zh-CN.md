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

# GPU 验证

按实际图形或计算 API 分别测试，记录 renderer/device/provider、上下文创建路径和输出。软件 renderer 或 CPU fallback 不计硬件通过；渲染成功不推导 OpenCL/Vulkan 计算可用。桌面用户通过不等于 headless 服务通过。
