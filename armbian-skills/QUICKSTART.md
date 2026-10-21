[English](QUICKSTART.md) | [简体中文](QUICKSTART.zh-CN.md)

# Quick start: from SSH access to a working hardware application

Run an AI assistant on your computer and use SSH to work on an Armbian device. Skills help discover capabilities, extend applications, deploy, and verify. Keep an existing project's language/build model or start with a small new application.

This guide uses **Codex CLI and Claude Code** on Linux, macOS, or Windows WSL. They use the same Skill files with different installation directories and invocation syntax.

## 1. Connect to the device

Prepare a booted Armbian device, a computer that can reach it, and the actual IP, SSH username, and authentication method. The computer needs Git, OpenSSH, and an installed/signed-in Codex or Claude Code. See the [Codex setup](https://learn.chatgpt.com/docs/codex/cli) or [Claude Code quickstart](https://code.claude.com/docs/en/quickstart). Local matching needs Python 3.9+; the optional target probe needs Python 3. Prepare application toolchains as the task requires.

In a **computer terminal**, replace USER and DEVICE_IP:

```bash
ssh USER@DEVICE_IP
```

Check the device's host fingerprint on first connection and authenticate. On the device, inspect the environment, then return to your computer:

```bash
uname -a
exit
```

Optionally add an alias to your computer's ~/.ssh/config. Replace the example address/user; edit an existing entry rather than adding a duplicate:

```sshconfig
Host armbian-dev
    HostName 192.168.1.100
    User YOUR_USER
    Port 22
```

Check from the computer:

```bash
ssh armbian-dev 'uname -a'
```

The assistant must authenticate SSH from its own execution environment. Existing keys/ssh-agent can be used; enter passwords in terminal authentication prompts, never in the repository, task prompt, or command arguments. Logging in from another terminal does not automatically share that session with the assistant. Both examples use ordinary SSH and the agent's actual command/network permissions, without an additional connector.

## 2. Install Skills on the assistant's computer

Install where Codex or Claude Code runs. You do not need an AI assistant on the board or a copy of the whole knowledge source there.

Clone the repository, replacing the URL for a different fork, or enter your existing checkout:

```bash
git clone https://github.com/Seeed-Studio/ai-skills.git
cd ai-skills
```

Choose one installation command from the repository root:

**Codex only** (user-level `~/.agents/skills`):

```bash
bash armbian-skills/install.sh --agent codex
```

**Claude Code only** (user-level `~/.claude/skills`):

```bash
bash armbian-skills/install.sh --agent claude
```

**Both agents**:

```bash
bash armbian-skills/install.sh --agent both
```

The [installer](install.sh) needs Bash and Python3.9+ standard library only; it does not install either agent, download dependencies or connect to a board. It copies the four complete packages, including both languages and local references. Its source path is relative to the script, so the checkout can be elsewhere and paths may contain spaces. Python users can call `python3 armbian-skills/scripts/install_skills.py` with the same options.

Preview an installation without creating any directories:

```bash
bash armbian-skills/install.sh --agent both --dry-run
```

Existing same-name destinations cause the whole batch to stop before installation. To update, pull the desired repository revision and explicitly replace the selected directories:

```bash
bash armbian-skills/install.sh --agent both --replace
```

Replacement stages and checks the new files first. Existing directories move to a timestamped `armbian-skills-backups/` folder beside the relevant `skills/` directory, outside Skill discovery. The script prints backup paths and attempts to restore previous directories if a batch fails. Keep backups until you are satisfied with the update. Backups include local edits; updates replace complete directories rather than merging stale files.

Additional examples (choose those needed):

```bash
# Install one self-contained Skill; repeat --skill to select several.
bash armbian-skills/install.sh --agent codex --skill armbian-device-capabilities

# Project scope: writes /path/to/app/.agents/skills and /path/to/app/.claude/skills.
bash armbian-skills/install.sh --agent both --scope project --project-dir /path/to/app

# Explicit skills root for a legacy/custom Codex setup; select a single agent.
bash armbian-skills/install.sh --agent codex --dest "${CODEX_HOME:-$HOME/.codex}/skills"

bash armbian-skills/install.sh --help
```

Project scope uses the current directory if `--project-dir` is omitted. `--dest` is a skills root, not a project root, and cannot be combined with `--agent both` or project scope. It can also select a custom Claude Code skills root. The script rejects existing Skill symlinks and destinations overlapping its source packages.

Do not copy only SKILL.md or install the suite parent as a Skill. Each package includes English and Chinese documentation; SKILL.md is the default English entry point, with SKILL.zh-CN.md as its Chinese counterpart.

Installation/invocation follow the [OpenAI Skills documentation](https://learn.chatgpt.com/docs/build-skills) and [Claude Code Skills documentation](https://code.claude.com/docs/en/skills). If new Skills do not appear, reload/restart the agent and verify the same runtime user/environment: WSL and its host do not share a home directory.

Codex path note: the script defaults to the current documented `~/.agents/skills` user directory. Existing installations under `~/.codex/skills` or `CODEX_HOME/skills` need not be moved if your installed Codex already discovers them; choose that existing root explicitly with `--dest`. Do not install the same names into both locations.

## 3. Start in the application workspace

For an existing project, enter it in your **computer terminal**:

```bash
cd /path/to/your-application
```

For a new project, create a workspace:

```bash
mkdir -p ~/projects/armbian-demo
cd ~/projects/armbian-demo
```

Start one agent.

**Codex:**

```bash
codex
```

**Claude Code:**

```bash
claude
```

In Codex, use /skills to browse. In Claude Code, type /armbian- to see matching commands.

| Purpose | Codex | Claude Code |
|---|---|---|
| Interfaces,40-pin header, NPU/GPU/VPU, prerequisites | $armbian-device-capabilities | /armbian-device-capabilities |
| Existing-project extension or new CLI/daemon/service | $armbian-hardware-application | /armbian-hardware-application |
| Build/deploy, dependencies, actual-user access, readiness/recovery | $armbian-application-deploy | /armbian-application-deploy |
| Business regression, physical effect, actual backend/lifecycle | $armbian-application-verify | /armbian-application-verify |

Enter these in the **agent's interactive prompt**, not the SSH shell. A task can use several Skills together or proceed stage by stage.

## 4. Discover what the device can do

**Codex example:** replace identity/connection facts with your actual target.

```text
$armbian-device-capabilities

Inspect my Armbian device through SSH alias armbian-dev.
The product is reComputer RK3588 DevKit, PCB silkscreen V1.0.
Start with read-only checks and explain:
1. Hardware interfaces and known 40-pin functions/electrical constraints.
2. Driver, runtime, and application prerequisites for NPU, GPU, and VPU.
3. Confirmed facts and remaining gaps.
Do not drive GPIO, scan I2C, install dependencies, or change boot settings yet.
```

**Claude Code example:**

```text
/armbian-device-capabilities Inspect my Armbian device through SSH alias armbian-dev.
The product is reComputer RK3588 DevKit, PCB silkscreen V1.0.
First explain interfaces, 40-pin electrical constraints, and NPU/GPU/VPU prerequisites/gaps read-only.
Do not drive GPIO, scan I2C, install dependencies, or change boot settings yet.
```

If product/revision is unknown, say so. The assistant should identify candidates and gaps. Recheck identity after changing devices even if the IP is unchanged. RK3576 J3 and RK3588 J10 are not interchangeable, nor is another carrier's pinout for the same SoC.

Expect an explanation of possible features, interfaces, and prerequisites. A node/library only establishes some readiness; it does not prove sensor communication or accelerator execution.

## 5. Complete an application task

The following task bodies work with either agent. Examples use Codex's $skill-name first line. In Claude Code's interactive prompt, replace that line with this invocation and append the same task body:

```text
/armbian-hardware-application /armbian-application-deploy /armbian-application-verify
```

This is interactive multi-Skill invocation; you can also call each stage separately with the existing project context.

### Example A: add AHT20 collection to an existing application

Confirm protocol, voltages, and wiring from the actual board/module documents first. These reference-design connections are examples: provide only wiring you have actually confirmed.

| AHT20 | RK3576 DevKit J3 | RK3588 DevKit V1.0 J10 |
|---|---|---|
| VCC |1, nominal 3.3V |1, nominal 3.3V |
| GND |14 |14 |
| SDA |27 |27 |
| SCL |28 |28 |

Confirm module supply, pullups, and signal levels before wiring. Physical pin numbers are not Linux bus numbers. Resolve the current controller/adapter rather than copying another board's /dev/i2c-N.

After wiring, send this in the project's agent conversation, changing the first line for Claude Code as described above:

```text
$armbian-hardware-application $armbian-application-deploy $armbian-application-verify

Add AHT20 background collection to the current monitoring application through its original status API.
Preserve its language, business interfaces, and build model. Inspect the project before choosing extension points.

Target: SSH alias armbian-dev; reComputer RK3588 DevKit; PCB V1.0.
Confirmed wiring: VCC→J10-1, GND→J10-14, SDA→J10-27, SCL→J10-28.
Peripheral: AHT20 module, 3.3V supply. Check protocol/fixed address without scanning the shared bus.
Deployment: run in a temporary target directory first; do not create a boot-time service.

Implement code, regress original business behavior, deploy, and check real samples.
On collection failure, expose stale/error and retain the last good sample without breaking health checks.
Verify bounded shutdown/resource release and provide run, stop, and recovery commands.
Bundle necessary wiring questions; do not ask again for known facts. Automate independent checks.
If physical unplugging is needed, explain its purpose and wait for confirmation; do not assume repeated manual rounds.
```

State whether the project uses Rust, Go, JavaScript, Python, or C/C++; hardware access does not require changing language. If source exists only on the target, provide its path and which directories may be changed.

### Example B: create a bounded GPIO command without an existing project

```text
$armbian-hardware-application $armbian-application-deploy $armbian-application-verify

Create a Rust GPIO CLI in this empty workspace.
Target: SSH alias armbian-dev; reComputer RK3588 DevKit; PCB V1.0.
Use J10-15, hold HIGH for 10 seconds, then exit; support cancellation and busy errors.

First verify pin mapping, current mux/owner, and electrical conditions, and ask for actual wiring/load.
Only drive output after those conditions are confirmed. Bound execution and explain actual state after completion/cancellation.
Do not treat request release as driving LOW or restoring input.
Deliver source, build, and target execution. If a multimeter is needed, give exact connections and one measurement window.
```

For another board, replace product/connector/pin and resolve the mapping again. This pin is not a default for all Armbian devices.

### Example C: integrate NPU inference into an existing JavaScript application

```text
$armbian-hardware-application $armbian-application-deploy $armbian-application-verify

Integrate NPU inference into the current JavaScript application, preserving original business interfaces.
Target: SSH alias armbian-dev. Check actual SoC, driver/runtime, runtime user, and dependencies first.
Models and inputs are in project models/. Read their metadata and report missing converted models/input contracts.

Keep the project stack and select a suitable binding, FFI, native bridge, or existing service API.
Deploy temporarily first. Check actual tensor attributes, known-input results, and genuine NPU execution evidence.
Explicitly label CPU fallback and exclude it from NPU passes. Nominal performance does not prove a speedup.
Deliver original-business regression, run/stop commands, and unverified scope.
```

models/ is an example: substitute actual files. SDKs/models are not included. GPU graphics/compute and VPU encode/decode can follow similar tasks, checking their actual stacks and inputs rather than inheriting success from another accelerator.

## 6. Review the result and continue

Expect code/changes, actual build/deployment locations, run/stop commands, original-business regression, hardware results, and unverified scope. Process running, business ready, and physical effect are separate claims. For physical operations, also explain state after exit and resource release.

For a persistent service, provide runtime user, installation directory, and boot-start requirement, then use armbian-application-deploy with existing project conventions. After SSH loss, inspect the original operation before replaying output.

Keep task records/artifacts in your own project, not ai-skills. V1.0.0 includes static RK3576/RK3588 DevKit profiles. Investigate additional platforms through shared workflows; pause only operations dependent on missing mappings.

## Troubleshooting

| Symptom | Action |
|---|---|
| Skill missing | Check Codex ~/.agents/skills or Claude Code ~/.claude/skills, complete directories, and SKILL.md. For existing Codex legacy installs, check /skills first. Avoid duplicate names; restart the agent if needed. |
| I can SSH but the agent cannot | Check the same environment/alias, usable keys/ssh-agent, and actual command/network permissions. |
| Python/Go/Rust/Node missing on the board | Separate inspection tools from application dependencies. Use available read-only interfaces, host cross-builds, or existing tools; decide installation per task. |
| Nodes exist but the application fails | Check actual runtime user, container mounts, permissions, driver/runtime, and resource owner. |
| Device numbering changed | Recheck compatible, board/revision, and sysfs correlation. Do not inherit chip, I2C, or DRM numbers. |
| Updating Skills | Update the checkout, inspect versions, and preserve or explicitly replace old packages. Keep the same knowledge version across packages and avoid mixed directories. |

See the [suite README](README.md) for structure/maintenance and each installed Skill's README for its dependencies and entry point.
