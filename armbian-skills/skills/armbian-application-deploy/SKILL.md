---
name: armbian-application-deploy
description: Deploy or update hardware applications on Armbian, checking artifacts, target ABI, dependencies, device
  access, service readiness, and recovery. Use for one-shot programs, existing applications, daemons/services, and
  containers; preserve project deployment conventions without installing a generic control service.
---

[English](SKILL.md) | [简体中文](SKILL.zh-CN.md)

# Armbian application deployment

Deliver the correct artifact to the correct device using the project's deployment model, verifying business readiness and required hardware access.

## Recover context

Read existing integration plans, deployment conventions, source/user edits, artifact digests, and build conditions. Identify workspace, build host, runtime target, deployment directory, actual user/container, and existing authorization.

Start with this package's [index](references/INDEX.md), reference-release.yaml, and [deployment guide](references/common/deployment.md). Select actual dependencies using the [matching contract](references/common/reference-matching.md):

```bash
python3 scripts/reference-match/match.py --input /path/to/task-facts.json
```

Read matching stack/language references and board restrictions without depending on another Skill or development checkout. Historical nodes/versions are traceability only; confirm current target/invalidation conditions rather than inferring compatibility from branch names.

## Prepare and execute

- Verify artifact provenance, target architecture, dynamic linker/ABI, libraries, and configuration. A host build is not target execution evidence.
- Preserve affected original versions/configuration and prepare staging, validation, switching, and executable recovery. A test-directory run is not a system installation. Finish preparation and proceed within existing authorization.
- Follow project directories, packages, containers, or actual service managers. Modify only project scope and preserve user configuration. Limit permissions to required devices/users, without globally writable nodes or unrestricted passwordless root.
- Service configuration includes user, working directory, environment/dependencies, logs, readiness, stop timeout, and suitable restart policy. Check isolation that hides devices/libraries and repeated output after crashes. Create systemd configuration only when the task needs it.
- Install overlays/drivers/runtimes or restart services only when necessary, compatible, impact/recovery understood, and authorized. Canceling a task does not stop a shared service. Assess whole-device reboot separately for necessity and authorization.
- After SSH loss/timeout, inspect the original operation before retrying. Do not blindly replay hardware transactions. A request ID does not guarantee deduplication; report uncertainty when state cannot be confirmed.

## Verify and deliver

Check dependencies/permissions as the actual user/container using [device access](references/common/linux-device-access.md). Follow [acceptance](references/common/verification.md) to distinguish process, manager running, business ready, and hardware function. Verify boot behavior when requested, without rebooting for unrelated checks.

Diagnose/recover at the failure's scope; external hardware recovery requires separate evidence. Deliver artifact version/digest, file/configuration changes, execution location, readiness/hardware results, and recovery steps. If only preparation is complete or the target is unreachable, state not-deployed/not-physically-verified rather than claiming deployment success.
