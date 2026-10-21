---
schema_version: '1'
id: stack.rockchip-rknn.verification
kind: stack_guide
applies_to:
  capabilities:
  - npu
  stack_ids:
  - rockchip-rknn
  soc_ids:
  - rockchip.rk3576
  - rockchip.rk3588
required_refs: []
preconditions: []
refines: []
excludes: []
related: []
sources:
- source.local-kernel-config
- source.cached-vendor-dts
- source.rknn-project
validation_refs: []
maturity: documented
owner: armbian-platform-maintainers
updated_at: '2026-10-20'
---

[English](verification.md) | [简体中文](verification.zh-CN.md)

# Rockchip RKNPU + compatible RKNN runtime: verification

固定模型/输入与正确性标准，保留 runtime 设备执行证据和端到端/推理耗时。当前内核driver、用户态runtime、绑定、模型与功能就绪需在目标检查，静态资料不提供本次结果。

对比已知输出和误差界，再检查实际计算行的Target及非零cycles，而非API返回0或文本包含NPU。按阶段区分CPU输入/输出转换和CPU整模型回退；显式回退结果不计硬件通过。确认SDK真实打开哪个DRM/设备节点，所需权限以实际服务用户为准。结束/错误/取消后检查context/进程与FD，不能用power状态代替资源释放。
