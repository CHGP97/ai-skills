[English](README.md) | [简体中文](README.zh-CN.md)

# Armbian hardware application Skills

For application engineers, system engineers, and beginners: discover device capabilities, extend existing applications, implement hardware features, deploy, and verify. Keep the user's language, business entry points, and build conventions. Deliverables may be a CLI, library, daemon, service, or existing application module.

Current release: `V1.0.0`, with reComputer RK3576/RK3588 DevKit profiles. Platform differences live in references; four Skills organize workflows so adding a platform does not require copying the workflows.

Start with [SSH-to-task quick start](QUICKSTART.md), using Codex or Claude Code. It covers installation, ordinary SSH, capability discovery, and prompts for existing-project extensions, GPIO commands, and NPU integration.

## Installable Skills

| Independent Skill | Purpose |
|---|---|
| [armbian-device-capabilities](skills/armbian-device-capabilities/README.md) | Identity, interfaces, electrical constraints, accelerators, and application prerequisites |
| [armbian-hardware-application](skills/armbian-hardware-application/README.md) | Extend an application, help beginners, or implement new features |
| [armbian-application-deploy](skills/armbian-application-deploy/README.md) | Artifacts, ABI, dependencies, permissions, readiness, and recovery |
| [armbian-application-verify](skills/armbian-application-verify/README.md) | Business regression, physical effects, actual backends, and lifecycle |

Install a complete armbian-skills/skills/{skill-name}/ directory. The suite parent is a maintenance directory, not a Skill entry point. Every package includes full references, matching helpers, and digests, so it works without sibling Skills or the source knowledge directory.

Local matching requires only Python 3.9+ standard library. The optional target read-only probe requires Python 3 and ships only with device-capabilities. Application toolchains, runtimes, device access, and wiring depend on the project; no specific MCP is required.

Install from the repository root for Codex, Claude Code, or both (Bash and Python3.9+):

```bash
bash armbian-skills/install.sh --agent codex
# Or --agent claude / --agent both
```

Use `--dry-run` to preview, `--skill` to select packages, `--scope project` for project installs, or `--dest` for an explicit skills root. Existing directories are protected by default; `--replace` backs them up before replacement. See the [quick start](QUICKSTART.md#2-install-skills-on-the-assistants-computer) for paths and update behavior.

## Maintenance layout

```text
armbian-skills/
├── README.md / README.zh-CN.md
├── QUICKSTART.md / QUICKSTART.zh-CN.md
├── install.sh                      # Codex / Claude Code installer
├── skills/                         # Four self-contained packages
├── knowledge/armbian/
│   ├── references/                 # Single active knowledge source
│   ├── release.yaml                # Reviewed files/helper lock
│   ├── scripts/                    # Generation, matching, probe implementations
│   ├── schemas/                    # Format constraints
│   ├── fixtures/                   # Synthetic matching inputs
│   └── tests/                      # Portable maintenance tests
├── scripts/                        # Installer and index/package entry points
├── requirements-dev.txt
└── dist/                           # Generated .skill/SHA256SUMS, Git-ignored
```

Update knowledge only in knowledge/armbian/references/, then generate identical copies in all packages. Maintain workflows and agents in skills/{skill-name}/. Suite-level scripts are entry points to the implementation beside the knowledge source, not a second implementation.

Run from the suite directory:

```bash
python3 scripts/refresh_catalog.py --check
python3 scripts/build_skills.py --check
python3 -m unittest discover -s knowledge/armbian/tests -v
```

Development checks use PyYAML/jsonschema from requirements-dev.txt; installed helpers do not. After reviewing knowledge changes, refresh the catalog and run build_skills.py --update-lock to freeze files, sync packages, and build ZIP-format dist/*.skill. With an unchanged lock, build_skills.py syncs/builds; --check is read-only. See [knowledge maintenance](knowledge/armbian/README.md).

## Languages and distribution scope

English .md files are default; adjacent .zh-CN.md files preserve independent Chinese documentation and workflow translations. Both languages share structured hardware data, original source images, IDs, and applicability. The matcher indexes canonical English references once, while package manifests cover both languages. Update both translations together; translation does not change electrical or compatibility claims.

The repository contains Skills, static hardware/API knowledge, installation/maintenance instructions, and necessary generation/checking code. Add future platforms through SoC, carrier/revision, and stack references while reusing the four workflows.

Proposals, release evaluations, hardware reports, device snapshots, user readings, task facts, credentials, SDKs, models, and application artifacts are excluded. docs/, evaluation/, evidence/, and dist/ remain ignored. Verification methods and automated maintenance tests remain available.

This release does not certify arbitrary pins, peripherals, accelerator models, GPU/VPU applications, or deployment environments. Confirm current identity, electrical conditions, mux/owner, actual application user, and functional results per task.
