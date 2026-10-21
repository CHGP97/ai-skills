[English](README.md) | [简体中文](README.zh-CN.md)

# Maintaining Armbian knowledge

This is the active source for the four Armbian Skills in ai-skills. references/ contains shared capabilities, SoCs, boards/revisions, software stacks, language integrations, and official/source evidence. Generate each package's copy from here rather than maintaining them independently. Knowledge release: armbian-skills-v1.0.0.

See the [suite README](../../README.md). Run these commands from ai-skills/armbian-skills/ without the outer Armbian workspace, device records, or cross-toolchains:

```bash
python3 scripts/refresh_catalog.py --check
python3 scripts/build_skills.py --check
python3 -m unittest discover -s knowledge/armbian/tests -v
```

Development checks require PyYAML/jsonschema from requirements-dev.txt. Installed matcher/probe use only Python standard library. Tests cover integrity, matching/conflicts/unknown conditions, read-only collection boundaries, independent installation, and schemas; they do not replace agent behavior or physical acceptance.

## Editing and packaging

1. Update canonical English references here, checking official sources, applicability, mappings, and scope. Maintain workflows/README/CHANGELOG in suite skills/.
2. Keep an adjacent .zh-CN.md translation for every Markdown document. Translations share metadata IDs and applicability but are not separate catalog entries. Shared YAML/hardware tables and original images remain single sources. Keep translations aligned without changing identifiers or schema keys.
3. Run refresh_catalog.py after reviewed changes to regenerate YAML/JSON indexes; update the generator's release identifier for a new knowledge version.
4. Run build_skills.py --update-lock to accept reviewed file/helper digests, sync four packages, and create archives. Ordinary builds reject unlocked knowledge/helper changes. Both language versions of workflow/README/CHANGELOG enter each package manifest.
5. Run read-only checks/tests and inspect dist/SHA256SUMS. Each .skill ZIP contains one independent top-level Skill directory that users can copy or extract.

--update-lock does not grant release approval or prove hardware acceptance. The lock/package manifests declare static-reference/workflow scope without historical trial/evaluation conclusions. Validate the actual target/application environment separately.

## Matching and independent installation

Use synthetic fixtures from the suite directory:

```bash
python3 knowledge/armbian/scripts/reference-match/match.py \
  --input knowledge/armbian/fixtures/rk3588-gpu.json --kind board
```

Fixtures do not establish current identity/electrical state. See the [matching contract](references/common/reference-matching.md). The matcher neither connects to targets nor requests GPIO/scans I2C. Required/refinement cycles are rejected, navigation cycles allowed, and unknown remains unknown.

The implementations live in scripts/build_skills.py and scripts/refresh_catalog.py; suite-root scripts expose common entry points. The matcher locates its local references in either source or installed layouts; copied helper implementations remain byte-identical. Runtime records, task facts, credentials, SDK/models, and user applications are not distributed.

Wiring examples are generated and checked against board electrical YAML and board-specific wiring-layout.yaml by scripts/render_wiring_examples.py. After relevant mapping edits, run `python3 knowledge/armbian/scripts/render_wiring_examples.py` from the suite directory before refreshing the catalog/packages; `--check` checks without rewriting. Rendering requires PyYAML only on the maintenance host; installed Skills use bundled examples without this script.
