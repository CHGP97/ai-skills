---
schema_version: '1'
id: stack.linux-gpio-chardev.detection
kind: stack_guide
applies_to:
  capabilities:
  - gpio
  stack_ids:
  - linux-gpio-chardev
required_refs: []
preconditions: []
refines: []
excludes: []
related:
- stack.linux-gpio-chardev.recovery
sources:
- source.cached-vendor-dts
- source.linux-gpio-api
validation_refs: []
maturity: documented
owner: armbian-platform-maintainers
updated_at: '2026-10-19'
---

[English](detection.md) | [简体中文](detection.zh-CN.md)

# Identifying GPIO controllers and lines

Inspect metadata only: do not request GPIOs or change direction. Separate physical pin, SoC pad, controller identity, and bank-local offset before resolving the current device. Vendor PIN_* labels, bank numbers, and old gpiochip numbers do not directly identify wiring.

Where Linux exposes them, correlate `/sys/bus/gpio/devices/gpiochip*/of_node` or the parent device with the profile's controller. Use gpiodetect/GET_CHIPINFO labels and line counts to establish a unique candidate, then use the actual `/dev/gpiochip*` path. Sysfs layout varies by platform/kernel; missing fields remain unknown. Use available device relationships, udev, or chip info instead. An RK address or 32-line assumption is not universal.

A label need not be an identifier accepted by the CLI. Check current tool help/API and distinguish label, name, and path. Resolve of_node to the real chip. Preserve multiple/conflicting candidates rather than choosing the first.

Read metadata with gpioinfo or GPIO_GET_CHIPINFO/GPIO_V2_GET_LINEINFO, and separately inspect pinmux/consumer. Clear USED/consumer metadata does not prove mux availability or eliminate request races. gpioget/gpioset request lines, and gpioget may force input; neither is passive inventory. Record CLI/libgpiod and kernel UAPI versions separately.
