[English](QUICKSTART.md) | [简体中文](QUICKSTART.zh-CN.md)

# 快速上手：从 SSH 连接到完成硬件应用

在电脑上运行 AI 助手，通过 SSH 操作 Armbian 设备，用 Skills 查询硬件能力、扩展应用、部署并验证。已有项目沿用原语言和构建方式；没有项目也可以从一个小应用开始。

本文以 Linux、macOS 或 Windows WSL 中的 **Codex CLI 和 Claude Code** 为例。两者使用同一套 Skills 文件，安装目录与调用语法不同。

## 1. 先连通设备

准备一台已启动 Armbian 的设备、可访问它的电脑，以及设备实际的 IP、SSH 用户和认证方式。电脑需要 Git、OpenSSH 客户端，以及已安装并登录的 Codex 或 Claude Code；安装见 [Codex 官方说明](https://learn.chatgpt.com/docs/codex/cli)或 [Claude Code 官方说明](https://code.claude.com/docs/en/quickstart)。Python 3.9+ 用于本地资料匹配，目标 Python 3 用于可选的只读采集；应用工具链按后续任务准备。

在**电脑终端**执行，将 `USER`、`DEVICE_IP` 替换为实际值：

```bash
ssh USER@DEVICE_IP
```

首次连接时核对设备的主机指纹，按提示完成认证。进入设备后可确认运行环境：

```bash
uname -a
exit
```

为减少后续重复输入，可以在电脑的 `~/.ssh/config` 中加入一个别名。下面的 IP 和用户名只是示例，请替换；已有同名配置时编辑原条目：

```sshconfig
Host armbian-dev
    HostName 192.168.1.100
    User YOUR_USER
    Port 22
```

在电脑终端确认：

```bash
ssh armbian-dev 'uname -a'
```

助手需要能够从自己的执行环境完成 SSH 认证。可使用已有 SSH 密钥和 ssh-agent；密码在终端的认证提示中输入，不写入仓库、提示词或命令参数。**另一个终端已登录，不代表助手自动共享该会话。** 两种助手都使用普通 SSH，按各自当前的命令执行和网络权限运行，不需要额外连接器。

## 2. 把 Skills 安装到运行助手的电脑

Skills 安装在运行 Codex 或 Claude Code 的电脑上；本流程无需在板上安装 AI 助手，也无需把整个知识源复制到设备。

克隆本仓库。使用其他 fork 时，替换下面的仓库地址；已有本地副本可直接进入该副本：

```bash
git clone https://github.com/Seeed-Studio/ai-skills.git
cd ai-skills
```

在仓库根目录选择下面一种安装命令：

**只安装到 Codex**（用户级 `~/.agents/skills`）：

```bash
bash armbian-skills/install.sh --agent codex
```

**只安装到 Claude Code**（用户级 `~/.claude/skills`）：

```bash
bash armbian-skills/install.sh --agent claude
```

**同时安装到两个助手**：

```bash
bash armbian-skills/install.sh --agent both
```

[安装脚本](install.sh)仅需 Bash 和 Python3.9+ 标准库；不安装助手、不下载依赖、不连接设备。默认复制四个完整 Skill 包，包含中英文资料和各自 references。脚本按自身位置查找源目录，可从其他工作目录调用，也支持带空格的路径。也可用 `python3 armbian-skills/scripts/install_skills.py` 直接调用，参数相同。

先预览安装计划，不创建任何目录：

```bash
bash armbian-skills/install.sh --agent both --dry-run
```

目标存在同名目录时，整批安装会在复制前停止。更新时先将仓库更新到需要的版本，再显式替换所选目录：

```bash
bash armbian-skills/install.sh --agent both --replace
```

更新会先暂存并核对新文件，再将旧目录移到对应 `skills/` 同级的 `armbian-skills-backups/` 时间戳目录，不进入 Skill 发现路径。脚本打印备份位置，批次失败时尝试恢复旧目录。确认更新可用后再自行处理备份；备份包含本地修改，新版按完整目录替换，不合并旧版残留文件。

其他用法按需选择：

```bash
# 只安装一个独立Skill；可重复 --skill 选择多个。
bash armbian-skills/install.sh --agent codex --skill armbian-device-capabilities

# 项目级安装：写入 /path/to/app/.agents/skills 与 /path/to/app/.claude/skills。
bash armbian-skills/install.sh --agent both --scope project --project-dir /path/to/app

# 兼容已有Codex旧版/自定义目录；指定目录时只能选一个助手。
bash armbian-skills/install.sh --agent codex --dest "${CODEX_HOME:-$HOME/.codex}/skills"

bash armbian-skills/install.sh --help
```

项目级未指定 `--project-dir` 时使用当前目录。`--dest` 指向 skills 根目录，不是项目根目录，不能与 `--agent both` 或项目级参数混用；Claude Code 的自定义 skills 目录也可用它指定。脚本拒绝替换已有 Skill 符号链接，也不允许目标与包源目录重叠。

不要只复制 `SKILL.md`，也不要把 `armbian-skills/` 整体当作一个 Skill；每个包均自包含，默认英文入口，相邻 `SKILL.zh-CN.md` 为中文说明。

安装与调用依据 [OpenAI Skills 官方文档](https://learn.chatgpt.com/docs/build-skills)和 [Claude Code Skills 官方文档](https://code.claude.com/docs/en/skills)。安装后若没有出现，可重新加载/启动助手，并检查是否在运行助手的同一用户与环境中；例如 WSL 内外不是同一目录。

Codex目录说明：脚本默认采用当前文档中的 `~/.agents/skills`。已有 `~/.codex/skills` 或 `CODEX_HOME/skills` 安装若已能被当前 Codex 发现，无需迁移，用 `--dest` 明确选择已有目录即可；避免两个目录重复安装同名Skill。

## 3. 在应用工作区启动助手

已有项目时，在**电脑终端**进入项目：

```bash
cd /path/to/your-application
```

没有项目时，先在电脑创建工作区：

```bash
mkdir -p ~/projects/armbian-demo
cd ~/projects/armbian-demo
```

然后选择一个助手启动。

**Codex：**

```bash
codex
```

**Claude Code：**

```bash
claude
```

Codex 可输入 `/skills` 查看；Claude Code 可输入 `/armbian-` 查看匹配的命令。两个助手的显式调用方式如下：

| 什么时候用 | Codex | Claude Code |
|---|---|---|
| 设备接口、40-pin、NPU/GPU/VPU 和使用条件 | `$armbian-device-capabilities` | `/armbian-device-capabilities` |
| 扩展已有项目，或完成新应用/CLI/daemon/service | `$armbian-hardware-application` | `/armbian-hardware-application` |
| 构建部署、依赖、实际用户权限、就绪和恢复 | `$armbian-application-deploy` | `/armbian-application-deploy` |
| 原业务回归、物理效果、真实后端与资源释放 | `$armbian-application-verify` | `/armbian-application-verify` |

这些调用都输入在**助手的交互界面**，不是 SSH 终端的 shell 命令。完整任务可以使用多个 Skill，也可以逐阶段调用。

## 4. 先问清设备能做什么

**Codex 示例**，将型号及连接信息换成实际情况：

```text
$armbian-device-capabilities

通过 SSH 别名 armbian-dev 检查我的 Armbian 设备。
产品是 reComputer RK3588 DevKit，PCB 丝印版本为 V1.0。
先只读检查，告诉我：
1. 设备具备哪些硬件接口，40-pin 有哪些已知接口及电气限制；
2. NPU、GPU、VPU 分别需要什么驱动、runtime 和应用条件；
3. 哪些信息已确认，哪些还需要补充。
暂不输出 GPIO、不扫描 I2C、不安装依赖或修改启动配置。
```

**Claude Code 示例：**

```text
/armbian-device-capabilities 通过 SSH 别名 armbian-dev 检查我的 Armbian 设备。
产品是 reComputer RK3588 DevKit，PCB 丝印版本为 V1.0。
先只读说明硬件接口、40-pin电气限制，以及NPU/GPU/VPU的使用条件和缺口。
暂不输出GPIO、不扫描I2C、不安装依赖或修改启动配置。
```

如果不知道产品或 revision，直接写“未知”，助手会先识别并标出缺口。切换设备后即使 IP 没变，也要重新确认身份。RK3576 的 J3 与 RK3588 的 J10 不可互换；同一 SoC 的另一载板也不能继承排针映射。

应得到“可以做什么、用哪个接口、准备什么”的说明。节点或库存在仅证明部分准备条件，不能代替传感器通信或实际加速执行。

## 5. 让助手完成应用任务

以下三个案例的任务正文适用于两个助手，示例首行使用 Codex 的 `$skill-name`。使用 Claude Code 时，在交互界面将该首行换成下面的调用，再接上相同任务正文发送：

```text
/armbian-hardware-application /armbian-application-deploy /armbian-application-verify
```

这里使用 Claude Code 交互提示中的多 Skill 调用；也可以分阶段单独调用，沿用前一步的项目上下文。

### 例一：给已有应用增加 AHT20 采集

先按当前板卡的官方资料确认外设协议、电压和接线。下列是两款参考设计的接线示例，**提供给助手的必须是你实际确认的接线**：

| AHT20 | RK3576 DevKit J3 | RK3588 DevKit V1.0 J10 |
|---|---|---|
| VCC | 1，标称3.3V | 1，标称3.3V |
| GND | 14 | 14 |
| SDA | 27 | 27 |
| SCL | 28 | 28 |

确认实际模块的供电、上拉和信号电平，再接线；排针物理编号不等于 Linux 总线编号。助手需从当前系统解析实际控制器与 adapter，不能直接复用另一设备的 `/dev/i2c-N`。

接好后，在项目的助手对话中输入（Claude Code 按上面的说明替换首行）：

```text
$armbian-hardware-application $armbian-application-deploy $armbian-application-verify

请在当前已有监测应用增加 AHT20 后台采集，接入原有状态 API。
保留项目原语言、业务接口与构建方式；先分析项目再决定集成位置。

目标：SSH 别名 armbian-dev，reComputer RK3588 DevKit，PCB V1.0。
实际接线：VCC→J10-1、GND→J10-14、SDA→J10-27、SCL→J10-28。
外设：AHT20 模块，3.3V 供电；请核对其协议和固定地址，不扫描共享总线。
部署：先在目标临时目录运行，不创建开机服务。

完成代码、原业务回归、目标部署和真实采样检查。
采集失败时标记 stale/error，保留最后成功样本，不影响原健康检查；
验证有界退出和资源释放，并给出运行、停止、恢复命令。
人工接线确认集中询问，已有信息不重复问；可自动完成的检查自行完成。
若必须拔线，请先说明目的，等我确认，不默认安排多轮人工重复。
```

如果项目使用 Rust、Go、JavaScript、Python 或 C/C++，在提示中说明即可，无需为了使用硬件改成另一种语言。项目只在设备上时，提供目标源码路径，并说明哪些目录可修改。

### 例二：没有项目，做一个有限时 GPIO 命令

```text
$armbian-hardware-application $armbian-application-deploy $armbian-application-verify

在当前空工作区用 Rust 写一个 GPIO CLI。
设备为 SSH 别名 armbian-dev，reComputer RK3588 DevKit，PCB V1.0。
希望控制 J10-15，保持高电平10秒后结束，支持取消和占用报错。

请先确认当前针脚映射、mux/owner及电气条件，并询问实际接线和负载；
条件满足后再做硬件输出。有限时运行，说明正常结束和取消后的真实状态，
不能把释放 request 等同于拉低或恢复 input。
完成源码、构建和目标运行；需要万用表时给出明确接法与一次测量窗口。
```

使用其他板卡时替换产品与实际连接器/针脚，让助手重新解析映射。不要把上述针脚当作所有 Armbian 设备的默认配置。

### 例三：给现有 JavaScript 应用接入 NPU

```text
$armbian-hardware-application $armbian-application-deploy $armbian-application-verify

在当前 JavaScript 应用接入 NPU 推理，保留原业务接口。
目标是 SSH 别名 armbian-dev；先核对实际 SoC、driver/runtime、应用用户与依赖。
模型和输入在项目 models/ 中，请读取其元数据；缺少转换模型或输入契约时说明缺口。

沿用项目技术栈，选择适合的绑定、FFI、native bridge 或已有服务接口。
先临时部署，检查实际 tensor 属性、已知输入的结果和真实 NPU 执行证据。
CPU 回退须明确标记，不计作 NPU 通过；不要从标称性能声称有加速比。
交付原业务回归、运行/停止命令和未验证项。
```

`models/` 是示例位置，需替换为实际文件；本套件不携带 SDK 或模型。GPU 图形/计算、VPU 编解码也可提出同类任务，由助手按当前软件栈与媒体/模型输入核对，不能从一种加速器成功推导另一种已可用。

## 6. 看结果并继续使用

任务结束时应拿到应用代码或修改、实际构建与部署位置、运行/停止命令、原业务回归，以及本次硬件结果和未验证项。进程运行、业务 ready、真实硬件效果要分开说明；有物理操作时，还要说明退出和资源释放后的状态。

需要正式服务时，再给出运行用户、安装目录和是否开机启动，调用 `armbian-application-deploy` 沿用项目部署方式。SSH 中断后先查询原任务状态，不直接重复输出命令。

记录与应用产物留在自己的项目中，无需提交到 ai-skills。当前套件版本为 V1.0.0，静态资料覆盖 RK3576/RK3588 DevKit；新增平台可继续用通用工作流调查，缺少某接口映射时只暂停依赖它的操作。

## 常见问题

| 现象 | 处理 |
|---|---|
| 找不到 Skill | 确认 Codex 使用 `~/.agents/skills/`、Claude Code 使用 `~/.claude/skills/`；检查完整目录与 `SKILL.md`，避免同名重复安装，必要时重启对应助手 |
| 我能 SSH，助手不能 | 确认助手在同一环境中使用同一 SSH 别名、可用的密钥/ssh-agent，以及所需命令执行与网络权限 |
| 设备没有 Python/Go/Rust/Node | 先区分采集工具与应用依赖；可只读手动检查、主机交叉构建或使用目标已有工具，按任务决定是否安装 |
| 有节点但应用不能用 | 检查实际运行用户、容器挂载、权限、驱动/runtime 和资源 owner |
| 设备切换后编号变化 | 重新确认 compatible、板卡/revision 与 sysfs 控制器关联，不继承 chip、I2C 或 DRM 编号 |
| 需要更新 Skills | 更新仓库后确认各包版本，保留旧安装或选择替换；四包一起安装时保持相同知识版本，避免混合目录 |

套件结构与维护命令见[README](README.zh-CN.md)，各 Skill 的依赖与入口见对应安装目录的 README。
