# Industrial Shields ESP32 PLCs: development platform for [PlatformIO](https://platformio.org)

This repository contains the configurations and examples to use the PlatformIO ecosystem with our Industrial Shields PLCs based on ESP32 open-source hardware. You can check the documentation of our ESP32-based PLCs in our [web page](https://www.industrialshields.com/industrial-esp32-plc-products-family-ideal-for-iot-solutions).


# Usage

1. [Install PlatformIO](https://platformio.org)
2. Create PlatformIO project and configure a platform option in [platformio.ini](https://docs.platformio.org/page/projectconf.html) file:

``` ini
[env]
platform_packages =
   ; You need to put a version instead of "X.X.X". The last one when this README was updated is 2.2.0
   framework-industrialshields-esp32@https://apps.industrialshields.com/main/arduino/boards/industrialshields-boards-esp32-X.X.X.tar.bz2

[env:board]
platform = https://github.com/Industrial-Shields/platform-industrialshields-esp32.git
board = ...
; You don't need these lines for 10 IOs, 14 IOs or the WiFi module
custom_version = 3 ; or 1
custom_click1 = None ; or GPRS
custom_click2 = None ; or GPRS
...
```

You can check all the available versions in https://apps.industrialshields.com/main/arduino/boards/ (all versions below 2.1.6 do NOT support PlatformIO).
