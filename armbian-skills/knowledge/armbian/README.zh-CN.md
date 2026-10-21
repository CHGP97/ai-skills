[English](README.md) | [简体中文](README.zh-CN.md)

# Armbian 知识源维护

本目录是 ai-skills 仓库中四个 Armbian Skill 的活动维护源。`references/` 保存通用能力、SoC、板卡/revision、软件栈、语言接入和官方/源码依据；四包的本地 references 由此生成，不能分别手工维护。当前 release 为 `armbian-skills-v1.0.0`。

套件入口见[README](../../README.zh-CN.md)。以下命令从 `ai-skills/armbian-skills/` 运行，不需要外层 Armbian 开发仓库、原始设备记录或交叉工具链。

```bash
python3 scripts/refresh_catalog.py --check
python3 scripts/build_skills.py --check
python3 -m unittest discover -s knowledge/armbian/tests -v
```

开发环境需要 PyYAML、jsonschema；可在自己的开发环境安装 `requirements-dev.txt`。安装后的 matcher/probe 仅用 Python 标准库。tests 检查目录/文件完整性、匹配与冲突/未知规则、只读采集边界、独立安装及格式约束，不能替代 Agent 行为或硬件验收。

## 修改与发布

1. 只在本目录的 references 中更新知识；核对官方来源、适用条件、硬件映射及证据范围。工作流、README、CHANGELOG 在套件 skills 下维护。
2. 有审核后的知识变更时，运行 `python3 scripts/refresh_catalog.py` 更新同源 YAML/JSON 索引，检查差异。需要新知识版本时，同步调整生成器中的版本定义。
3. 运行 `python3 scripts/build_skills.py --update-lock` 明确接受审核后的文件/摘要与辅助版本，同时同步四个包并打包。普通构建拒绝未冻结的知识/辅助变更；README、CHANGELOG 也纳入每包文件清单。
4. 运行上述只读检查与测试，检查 `dist/SHA256SUMS`。每个 `.skill` ZIP 顶层为一个独立 Skill 目录，用户可直接复制目录或解压归档安装。

`--update-lock` 用于维护者审核后的锁更新，不代表自动完成发布审批或实机验收。`release.yaml`与包内清单只声明静态资料及工作流的分发范围，不附带历史实测或评估结论。硬件功能需在当前目标与实际应用环境验证。

## 资料选择与独立安装

在套件目录可用合成输入检查匹配逻辑：

```bash
python3 knowledge/armbian/scripts/reference-match/match.py \
  --input knowledge/armbian/fixtures/rk3588-gpu.json --kind board
```

fixtures 不代表当前设备身份或电气状态。输入契约见[reference-matching](references/common/reference-matching.zh-CN.md)；匹配器不连接设备，不申请 GPIO，不扫描 I2C。必要依赖/细化循环会被拒绝，导航互链允许，未知保持未知。

生成器由 `scripts/build_skills.py` 实现，索引生成由 `scripts/refresh_catalog.py` 实现；套件根 scripts 提供入口。开发源中的 matcher 路径与包内路径各自能找到本地 references，复制到包内后实现字节保持一致。原始运行记录、当前任务事实、凭据、SDK/模型和用户应用不在该发布集合中。


英文.md为规范入口，相邻.zh-CN.md保留中文说明。翻译文件使用相同ID与适用条件，不作为独立索引条目；两种语言都进入包文件清单。硬件YAML与官方原图不复制翻译，修改文档时同步维护两种语言。

接线示例由 `scripts/render_wiring_examples.py` 从板卡电气YAML及板级wiring-layout.yaml核对并生成。修改相关映射后，先运行 `python3 knowledge/armbian/scripts/render_wiring_examples.py` 生成两板AHT20图，再更新索引和包；使用 `--check` 只读检查图与当前资料一致。此命令从套件目录运行，仅开发机需要PyYAML，用户安装包无需该渲染脚本。
