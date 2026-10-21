# Contributing Guide

Thank you for your interest in the Seeed AI Skills project! This document explains how to contribute new skills or improve existing skills in this repository.

## Skill Directory Structure Standard

Each skill should follow this directory structure:

```
skills/{skill-name}/
├── SKILL.md                  # Main skill definition file (required)
├── README.md                 # Skill overview and usage guide (required)
├── CHANGELOG.md              # Version history (required)
├── LICENSE                   # License file (required)
├── .skillrc                  # Skill configuration file (optional)
├── references/               # Detailed reference documentation (recommended)
│   └── *.md                 # Detailed docs for each module
└── scripts/                  # Automation scripts (optional)
    └── *.sh, *.py           # Maintenance and validation scripts
```

### Armbian suite

The Armbian family is maintained under `armbian-skills/`, with four independent installable directories at `armbian-skills/skills/{skill-name}/`. The parent is a maintenance suite, not a skill entry point. See [the suite README](armbian-skills/README.md) for the exact layout and commands.

Maintain Armbian references in `armbian-skills/knowledge/armbian/references/` and generate the complete copies in each skill. Run the suite index/package checks and portable tests before submitting changes. Keep raw device captures, SDKs, models, user applications and build artifacts outside the tracked suite; generated archives belong in its ignored `dist/`.

For an Armbian contribution, use the nested skill path in root README links and installation instructions. Changes to repository paths do not change the skill's name or its independent installation contract. Other skills keep the existing `skills/{skill-name}/` layout.

### Required Files Description

#### SKILL.md
- Core skill definition file containing key information needed by AI assistants
- Should include: capability descriptions, quick reference, API index, usage examples
- Use progressive disclosure: core workflows + links to detailed API references

#### README.md
- Developer-facing overview documentation
- Should include: skill introduction, supported products, main features, installation methods, quick start examples
- Clearly state maintainer information and repository address

#### CHANGELOG.md
- Record all version change history
- Use semantic versioning (vX.Y.Z)
- Each version entry should include: version number, release date, categorized changes (Added/Fixed/Improved/Breaking Changes)

#### LICENSE
- Each skill should have its own license file
- MIT License is recommended
- If based on other projects, acknowledge original authors and retain original copyright notices

## Skill Naming Conventions

- **Function-oriented naming**: Focus on functionality or technology, e.g., `cv181x-media`, `grove-sensors`
- Use lowercase letters and hyphens: `skill-name`, avoid underscores or camelCase
- Avoid product-specific prefixes unless there's a clear need for product line differentiation

## Version Management Guidelines

### Semantic Versioning

Follow [Semantic Versioning 2.0.0](https://semver.org/):

- **MAJOR** (X.0.0): Incompatible API changes
- **MINOR** (x.Y.0): Backward-compatible functionality additions
- **PATCH** (x.y.Z): Backward-compatible bug fixes

### Git Tag Format

Each skill uses an independent tag namespace:

```bash
skills/{skill-name}/vX.Y.Z
```

Examples:
```bash
skills/cv181x-media/v2.3.0
skills/grove-sensors/v1.0.0
```

Creating tags:
```bash
git tag -a skills/cv181x-media/v3.0.0 -m "Release cv181x-media v3.0.0"
git push origin skills/cv181x-media/v3.0.0
```

## Contribution Workflow

1. **Fork the repository**: Click the Fork button in the top right corner

2. **Clone locally**:
   ```bash
   git clone https://github.com/YOUR-USERNAME/ai-skills.git
   cd ai-skills
   ```

3. **Create a branch**:
   ```bash
   git checkout -b feature/your-skill-name
   ```

4. **Add or modify skills**:
   - Create a new skill directory under `skills/`; for the Armbian suite, use `armbian-skills/skills/`
   - Follow the directory structure standard above
   - Ensure all required files are complete

5. **Update root README**:
   - Add the new skill to the skills list in `README.md`
   - Format: `- **[skill-name](skills/skill-name/README.md)** - Brief description`; use `armbian-skills/skills/skill-name/README.md` for an Armbian entry.

6. **Commit changes**:
   ```bash
   git add .
   git commit -m "Add new skill: skill-name"
   ```

7. **Push branch**:
   ```bash
   git push origin feature/your-skill-name
   ```

8. **Create Pull Request**:
   - Visit your forked repository page
   - Click "Compare & pull request"
   - Fill in the PR description explaining what was added or modified

## Skill Quality Requirements

- **Completeness**: Include all required files with comprehensive documentation
- **Accuracy**: Technical information is accurate, code examples are runnable
- **Clarity**: Documentation structure is clear, easy to understand and navigate
- **Practicality**: Provide real-world application scenarios and complete examples
- **Maintainability**: Code and documentation are easy to update and maintain

## Getting Help

If you have any questions:
- Ask in GitHub Issues
- Contact Seeed Studio technical support team

Thank you for your contributions! 🎉
