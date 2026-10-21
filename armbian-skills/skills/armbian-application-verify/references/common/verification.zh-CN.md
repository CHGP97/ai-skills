---
schema_version: '1'
id: common.verification
kind: common
applies_to: {}
required_refs:
- common.capability-evidence
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

# 任务验收与证据记录

按用户目标选择源码/构建、业务、目标访问、硬件效果、真实后端、生命周期和服务就绪的必要检查。现有项目扩展同时回归相关旧功能，独立硬件 demo 或模拟测试不替代应用集成。

预先确定输入、时限、资源、停止方式与通过标准。记录实际命令/方法、目标与时间、运行用户/容器、产物/依赖、输出及证据来源。区分未测试、通过、失败、结果不确定；四层能力按具体操作使用 available/needs-setup/busy/unsupported/unknown，不以进程正常退出直接写物理功能通过。

GPIO request 持有、正常退出/取消、资源忙、断连及失败路径需要针对性检查。回读软件值不能单独证明外部电压；采用仪表、已知接线、回环或具体用户观察。不能伪造人工动作或测量结果。request释放、方向/配置恢复和外部器件状态分别判断；需要恢复时先记录已知原状态，按[GPIO恢复流程](../stacks/linux-gpio-chardev/recovery.zh-CN.md)核对，不用未知配置猜测。

NPU/GPU/VPU 同时检查输出正确性及实际后端。识别 CPU/软件渲染回退，视频编解码和各阶段分别验收。benchmark、标称性能或 CPU 占用不能代替后端证据。

设备不可达时继续代码和离线业务验证，明确实机未验证。环境或应用输入变化只复查受影响证据。未收录组合可在条件明确时开展有界测试，结果先保存在项目；共享支持矩阵需要另行审核，不能自动扩大正式支持。

交付简短结果：实现/接入位置；构建运行方式；版本与更改；验收/回归结果；未验证和下一步；部署/恢复方法。无需机械创建与任务无关的测试框架。
