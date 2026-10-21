---
schema_version: '1'
id: capability.camera
kind: capability
applies_to:
  capabilities:
  - camera
required_refs:
- common.capability-evidence
preconditions: []
refines: []
excludes: []
related: []
sources: []
validation_refs: []
maturity: documented
owner: armbian-platform-maintainers
updated_at: '2026-10-19'
---

[English](overview.md) | [简体中文](overview.zh-CN.md)

# Camera application development

Identify the sensor, CSI/USB interface, media graph, video node, output format, IQ/3A pipeline, and runtime permissions. Do not assume `/dev/video0`. Check sample frames for color, exposure, and content; capturing a frame alone does not establish correct imaging.

For an unlisted platform, continue with official interfaces and bounded tests. If essential wiring or compatibility is unknown, continue offline implementation and mark the dependent hardware steps unverified.
