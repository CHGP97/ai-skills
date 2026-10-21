[English](README.md) | [简体中文](README.zh-CN.md)

# Armbian 硬件应用开发

版本：`V1.0.0` · 正式版
维护：Seeed AI Skills maintainers · 套件：`armbian-skills`

分析并扩展已有应用，或协助新手实现硬件功能；沿用项目语言、业务入口、构建方式和交付形态。

## 安装与使用

将完整的 `armbian-hardware-application/` 目录放入所用Agent支持的Skills目录。入口为[SKILL.md](SKILL.zh-CN.md)，版本与文件摘要见[reference-release.yaml](reference-release.yaml)。本Skill自包含，不依赖其他Armbian Skill或开发仓库的knowledge目录。

安装后可向助手提出：

> $armbian-hardware-application 在现有Go服务增加AHT20采集，接入原API，保留已有业务。

Claude Code中可用`/armbian-hardware-application`调用相同任务。提供已有项目位置、当前设备和实际需求；已有信息无需重复提供，未知项按任务补充。支持CLI、库、daemon、service或应用模块，语言由用户项目决定。

## 依赖与资料

本地资料匹配只需Python 3.9+标准库，无需pip依赖。可选只读probe仅随device-capabilities包提供，在目标Python 3执行。连接可用普通SSH或现有连接器，不要求特定MCP。工具链、SDK、runtime、权限与接线按实际应用准备。

资料入口为[references/INDEX.md](references/INDEX.md)。需要手工匹配时，从本Skill目录运行：

```bash
python3 scripts/reference-match/match.py --input /absolute/path/task-facts.json
```

输入格式见[匹配契约](references/common/reference-matching.md)。静态资料不能填补当前设备事实，也不直接授权输出电平或访问其他应用占用的资源。

当前资料覆盖reComputer RK3576/RK3588 DevKit；工作流按通用能力、SoC、载板/revision、实际软件栈与语言接入分层，支持继续增加平台。实际硬件、驱动/runtime、应用用户与部署环境需逐任务验证，未收录不等于不支持。

四包使用相同知识版本 `armbian-skills-v1.0.0`。本包包含静态硬件/API资料及验证方法，不附带开发方案、评估记录、设备快照、人工测量、SDK、模型或应用产物。版本记录见[CHANGELOG.md](CHANGELOG.zh-CN.md)。


默认入口为英文SKILL.md，中文为SKILL.zh-CN.md；references同样提供相邻中文版本，结构化硬件数据与资料ID共用。
