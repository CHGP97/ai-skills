---
schema_version: '1'
id: stack.rockchip-rknn.integration
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

[English](integration.md) | [简体中文](integration.zh-CN.md)

# Rockchip RKNPU + compatible RKNN runtime: integration

先核对当前目标 driver/runtime 与模型目标，再按用户语言选已有绑定、C ABI/FFI 或原服务接口。转换、校准和运行分别处理；不直接套用外接 RK182x 案例。

使用官方仓库的明确tag/文件摘要，记录模型由哪个Toolkit版本转换、目标SoC、实际runtime/header/driver与应用架构。master或最新版本不代表设备安装版本；缺runtime时可在任务临时目录准备匹配依赖，无需先替换系统驱动或安装通用控制服务。已有模型/绑定优先沿用项目，示例版本不成为未来组合白名单。

运行时query真实输入输出数量/shape/layout/dtype，不用原ONNX属性盲填RKNN输入；pass_through、输入归一化和输出float转换明确。保留原业务入口，持续应用按语言异步生命周期管理，释放output/context，错误/取消检查实际owner退出。
