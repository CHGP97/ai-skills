[English](README.md) | [简体中文](README.zh-CN.md)

# Armbian application deployment

Version: `V1.0.0` · Stable release

Maintainer: Seeed AI Skills maintainers · Suite: armbian-skills

Check architecture, ABI, runtime, device access, readiness, and recovery for the actual target using project deployment conventions.

## Installation and use

Install the complete armbian-application-deploy/ directory into your agent's supported Skills location. Read [SKILL.md](SKILL.md) for the workflow and [reference-release.yaml](reference-release.yaml) for versions/digests. This package is self-contained and needs neither other Armbian Skills nor the development knowledge source.

Example in Codex:

> $armbian-application-deploy Deploy this hardware application to the current Armbian target and check dependencies and access as the actual service user.

In Claude Code, invoke /armbian-application-deploy with the same task. Provide the existing project location, current target, and actual goal. Reuse known information and fill only relevant gaps. Deliverables may be a CLI, library, daemon, service, or application module in the user's chosen language.

## Dependencies and references

Local matching requires Python 3.9+ standard library, with no pip dependencies. Only device-capabilities includes an optional read-only probe, executed with target Python 3. Use ordinary SSH or an existing authorized connector; no specific MCP is required. Toolchains, SDKs, runtimes, permissions, and wiring depend on the application.

Start at [references/INDEX.md](references/INDEX.md). To match manually, run from this Skill directory:

```bash
python3 scripts/reference-match/match.py --input /absolute/path/task-facts.json
```

See the [matching contract](references/common/reference-matching.md). Static knowledge cannot fill current device facts or authorize output/access to another application's resources.

Current profiles cover reComputer RK3576/RK3588 DevKit. Shared capabilities, SoC, carrier/revision, actual software stack, and language layers allow more platforms to be added. Check real hardware, driver/runtime, application user, and deployment per task; unlisted does not mean unsupported.

All packages use knowledge version armbian-skills-v1.0.0. English is default, with adjacent .zh-CN.md workflow/reference translations sharing structured data and IDs. The package contains static hardware/API material and verification methods, not proposals, evaluation records, device snapshots, user readings, SDKs, models, or application artifacts. See [CHANGELOG.md](CHANGELOG.md).
