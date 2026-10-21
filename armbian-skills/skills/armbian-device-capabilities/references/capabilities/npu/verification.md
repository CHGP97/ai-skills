---
schema_version: '1'
id: capability.npu.verification
kind: capability_guide
applies_to:
  capabilities:
  - npu
required_refs:
- capability.npu
- common.verification
preconditions: []
refines: []
excludes: []
related: []
sources: []
validation_refs: []
maturity: documented
owner: armbian-platform-maintainers
updated_at: '2026-10-20'
---

[English](verification.md) | [简体中文](verification.zh-CN.md)

# NPU verification

Pin the model digest/target, input shape/layout/dtype, quantization, and preprocessing. Compare known inputs against expected results. Record driver/runtime, actual execution device/backend, and the language bridge ABI. A host example does not replace testing the actual service/container; record CPU fallback separately.

Keep original ONNX attributes separate from runtime attributes. Query the latter before choosing layout/conversion; a quantization enum alone does not establish dtype or data interpretation. SDK success can coexist with conversion errors, so inspect logs and known numerical results. The word "NPU" is not execution evidence: use per-operator Target/cycles and device correlation. Explain CPU I/O glue or preprocessing separately from whole-model CPU fallback.
