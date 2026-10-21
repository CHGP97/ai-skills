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

# GPIO 控制器与 line 识别

这里只枚举元数据，不申请GPIO、不改变方向。先区分物理针脚、SoC pad、控制器身份和bank内offset，再核对当前GPIO设备。不能从vendor PIN_*标签、bank编号或旧gpiochip编号直接得到接线。

Linux有对应sysbus接口时，将 `/sys/bus/gpio/devices/gpiochip*/of_node` 或设备父节点关联到板级profile声明的控制器；结合gpiodetect/GET_CHIPINFO的label和line数核验唯一候选，最终使用实际 `/dev/gpiochip*` 路径。sysfs布局因平台/内核而异，缺少字段不能补成成功读数；改用可用的设备关系、udev或芯片信息继续查证。不能把某个RK地址或32-line假设用于所有平台。

label不一定是CLI接受的chip标识。使用当前CLI接受的name/path，结合of_node确认实际gpiochip设备。先查当前工具help/API，label、name、path分别处理。多个候选或矛盾时保留歧义，不取第一个。

用gpioinfo或GPIO_GET_CHIPINFO/GPIO_V2_GET_LINEINFO读取元数据，另检查当前pinmux/consumer。USED或consumer为空不证明mux可用，也不消除实际申请的竞争。gpioget/gpioset会申请line，gpioget还可能强制input，均不作为被动inventory。CLI/libgpiod版本和kernel UAPI版本分别记录。
