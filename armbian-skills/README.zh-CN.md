[English](README.md) | [简体中文](README.zh-CN.md)

# Armbian 硬件应用 Skills 套件

面向应用工程师、系统工程师和应用新手，帮助识别设备能力、扩展已有应用、实现硬件功能、部署和验证。沿用用户项目的语言、业务入口和构建方式，交付可以是 CLI、库、daemon、service 或现有应用模块。

当前为 `V1.0.0` 正式版，资料覆盖 reComputer RK3576 / RK3588 DevKit。多平台差异放在 references 中，四个 Skill 按工作流分工；新增平台不需要复制整套工作流。

第一次使用请看[快速上手：从 SSH 连接到完成硬件应用](QUICKSTART.zh-CN.md)，以 Codex 和 Claude Code 为例，包含安装、普通 SSH 连接、设备能力查询，以及已有应用扩展、GPIO CLI 和 NPU 集成的可复制提示。

## 安装入口

| 独立 Skill | 职责 |
|---|---|
| [armbian-device-capabilities](skills/armbian-device-capabilities/README.zh-CN.md) | 身份、接口、电气、加速器和应用准备条件 |
| [armbian-hardware-application](skills/armbian-hardware-application/README.zh-CN.md) | 扩展已有应用，协助新手或实现新功能 |
| [armbian-application-deploy](skills/armbian-application-deploy/README.zh-CN.md) | 构建产物、ABI、依赖、权限、就绪和恢复 |
| [armbian-application-verify](skills/armbian-application-verify/README.zh-CN.md) | 业务回归、物理效果、实际后端和生命周期 |

从本仓库安装时，选取 `armbian-skills/skills/{skill-name}/` 下的完整目录。`armbian-skills/` 是开发管理目录，安装入口是四个带 `SKILL.md` 的子目录。每个包都有完整 references、匹配辅助和文件摘要，独立安装后不依赖其他 Skill 或套件知识源；安装时无需复制整个套件。

本机资料匹配仅需 Python 3.9+ 标准库；可选目标只读 probe 使用 Python 3，仅随能力查询包提供。应用的工具链、runtime、设备权限和接线按实际项目准备，不要求特定 MCP。

从仓库根目录安装到 Codex、Claude Code 或两者（Bash、Python3.9+）：

```bash
bash armbian-skills/install.sh --agent codex
# 或 --agent claude / --agent both
```

支持 `--dry-run` 预览、`--skill` 单包选择、`--scope project` 项目级安装、`--dest` 自定义目录。默认不覆盖已有目录；更新用 `--replace` 自动备份后替换。参数与更新步骤见[快速上手](QUICKSTART.zh-CN.md#2-把-skills-安装到运行助手的电脑)。

## 维护结构

```text
armbian-skills/
├── README.md
├── QUICKSTART.md                   # 安装、SSH连接与任务使用指南
├── install.sh                      # Codex / Claude Code 安装入口
├── skills/                         # 四个自包含发布目录
├── knowledge/armbian/
│   ├── references/                 # 唯一活动知识源
│   ├── release.yaml                # 已审核资料/辅助文件锁
│   ├── scripts/                    # 生成、匹配、probe 的维护实现
│   ├── schemas/                    # 格式约束
│   ├── fixtures/                   # 合成测试输入
│   └── tests/                      # 可在本套件独立执行的开发测试
├── scripts/                        # 安装、索引检查、同步与打包入口
├── requirements-dev.txt
└── dist/                           # 本地产生的 .skill 与 SHA256SUMS，Git忽略
```

在 `knowledge/armbian/references/` 修改平台、板卡和软件栈资料，审核后由构建流程复制到四个包；不要分别修改包内 references。工作流入口及 agents 在对应 `skills/{skill-name}/` 内维护。维护实现放在知识源旁，顶层 scripts 是统一命令入口，没有第二套实现。

从套件目录运行：

```bash
python3 scripts/refresh_catalog.py --check
python3 scripts/build_skills.py --check
python3 -m unittest discover -s knowledge/armbian/tests -v
```

开发校验需要 `requirements-dev.txt` 中的 PyYAML、jsonschema；安装后的 Skill 不需要这些第三方包。修改资料并审核后，运行 `refresh_catalog.py` 更新索引，运行 `build_skills.py --update-lock` 更新锁、同步四包并生成 ZIP 格式的 `dist/*.skill`。锁未变化时，直接运行 `build_skills.py` 同步和打包；`--check` 只读校验。详细步骤见[知识库维护说明](knowledge/armbian/README.zh-CN.md)。

## 发布范围

本套件只提交Skills、静态硬件与API资料、安装/维护说明及必要的生成校验代码。当前资料覆盖reComputer RK3576/RK3588 DevKit；未来平台通过新增SoC、载板/revision与软件栈资料接入，共用四个工作流。

开发方案、发布评估、实机报告、设备快照、用户测量、当前任务事实、凭据、SDK、模型与应用产物不进入仓库或Skill安装包。`docs/`、`evaluation/`、`evidence/`与`dist/`在本套件忽略；验证方法和自动化测试代码保留，供维护知识完整性、匹配及独立安装。

本版本不承诺任意针脚、器件、加速模型、GPU/VPU应用或部署环境已通过验证。静态资料用于确定接入方案，当前身份、电气、mux/owner、实际应用用户与功能结果仍需任务现场确认。


## 文档语言

默认.md文件为英文，同目录.zh-CN.md为独立中文版本。中英文共用结构化硬件数据、原始资料图片、引用ID与适用条件，索引只匹配英文规范入口，文件摘要覆盖两种语言。同步维护双语说明，不因翻译改变电气或兼容性结论。
