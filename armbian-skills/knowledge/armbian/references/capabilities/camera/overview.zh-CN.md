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

# CAMERA 应用开发

识别 sensor、CSI/USB、media graph、video node、输出格式、IQ/3A 与运行权限。不要固定 /dev/video0。样帧验证颜色/曝光和内容，单纯可抓帧不足以验证正确图像。

未收录平台可继续核对官方接口并做有界测试；关键接线或兼容性未知时，继续离线实现并将相关实机步骤标为未验证。
