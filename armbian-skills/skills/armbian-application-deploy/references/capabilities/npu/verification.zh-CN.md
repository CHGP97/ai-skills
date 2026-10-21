---
schema_version: '1'
id: capability.npu.verification
kind: capability_guide
applies_to:
  capabilities:
  - npu
required_refs:
- capability.npu
- common.verification
preconditions: []
refines: []
excludes: []
related: []
sources: []
validation_refs: []
maturity: documented
owner: armbian-platform-maintainers
updated_at: '2026-10-20'
---

[English](verification.md) | [简体中文](verification.zh-CN.md)

# NPU 验证

固定模型摘要/目标、输入 shape/layout/dtype、量化和预处理，使用已知输入与期望结果比较。记录 driver/runtime、真实设备/执行后端和语言桥接的 ABI。宿主示例通过后仍需测试实际服务/容器；CPU fallback 单独记录。

转换前ONNX属性与实际runtime属性分别记录；query后决定输入布局/转换，不以一个量化枚举代替dtype与数据解释。SDK返回成功也可能伴随转换错误，须检查日志及已知数值；出现“NPU”字样不等于计算在NPU，按算子Target/实际cycles和设备关联作证。输入/输出胶合或预处理在CPU应单独说明，不混同全模型CPU回退。
