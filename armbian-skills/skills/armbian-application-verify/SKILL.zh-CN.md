---
name: armbian-application-verify
description: 验证和诊断 Armbian 硬件应用的业务功能、真实硬件效果、加速后端、权限和生命周期。用于已有应用回归、服务运行但外设无响应、NPU/GPU/VPU 回退等任务；区分源码/模拟测试、当前设备观察和物理功能验收。
---

[English](SKILL.md) | [简体中文](SKILL.zh-CN.md)

# Armbian 应用验收

用可复现证据回答指定应用功能是否完成，并定位未通过条件。

## 对象与通过标准

读取已有计划、项目测试/部署约定、目标设备、源码/产物摘要、输入和实际用户/容器。按任务选择相关检查，不默认建立测试框架或运行全部硬件压力测试。

先读本包 [资料入口](references/INDEX.md)、`reference-release.yaml`、[四层证据](references/common/capability-evidence.md) 与 [验证指南](references/common/verification.md)。按 [匹配契约](references/common/reference-matching.md) 筛选 capability、board/revision、实际 stack 和语言：

```bash
python3 scripts/reference-match/match.py --input /path/to/task-facts.json
```

事实来自当前设备；历史报告或枚举不能升级为本次功能通过。资料匹配不是执行许可或支持声明；目标、runtime、用户/容器、应用或输入变化后复查受影响证据。

## 相关验证

- 源码/构建与业务：输入输出、配置、错误、超时、并发；新增功能进入原业务入口，同时回归受影响旧功能。持续硬件操作分别检查原业务在操作前/中/后、发起请求返回、业务取消与应用退出时的行为。
- 应用访问：在服务/容器真实环境检查库、设备、权限和资源所有权；root shell 样例不足以证明应用可访问。
- GPIO：先确认映射、电气、接线、mux 与授权，再测初始值、保持、结束/取消/失败和释放。软件回读不单独证明物理电压；request释放、方向/配置恢复和实际电压分别记录，按[恢复流程](references/stacks/linux-gpio-chardev/recovery.md)核对已知状态。按需读 [GPIO 验证](references/capabilities/gpio/verification.md)。
- 通信/摄像头/PWM：用已确认协议、真实对端/回环、帧或仪表判断，命令成功不证明功能成功。不扫描内部 I2C 或强占驱动/共享服务。
- NPU：固定模型/输入和预处理，检查正确性及真实执行设备/runtime。读 [NPU 验证](references/capabilities/npu/verification.md)。
- GPU：图形与计算分别核对 API、renderer/device/provider 和输出，识别软件回退。读 [GPU 验证](references/capabilities/gpu/verification.md)。
- VPU：编解码按 codec/profile/位深/分辨率分别核验输出与每阶段后端。功能列表/CPU 占用不能替代执行证据。读 [VPU 验证](references/capabilities/vpu/verification.md)。
- 生命周期/服务：就绪、取消、断连、依赖缺失、重启策略和恢复；功能测试有明确输入、时限、资源和停止方式。

## 记录与诊断

按硬件/接口、系统、应用访问、功能实测四层使用 available/needs-setup/busy/unsupported/unknown。测试结果分别写通过/失败/未测试/不确定，附目标、时间、方法、版本与证据。保留回退和部分成功，不继承整链路可用。

用户报告、软件检测、仪表/回环测量分开，不伪造人工动作。设备不可达仍可离线业务测试，明确实机未验证。分开诊断应用、权限、占用、配置和驱动，未知不等于不支持，不扩大无关底层改造。

交付通过项、失败原因/修复、相关回归、剩余条件和复现/恢复方式。本次证据先保存在项目，不自动改写共享矩阵或跨平台支持声明。
