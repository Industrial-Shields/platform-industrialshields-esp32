# Industrial Shields ESP32 PLCs: development platform for [PlatformIO](https://platformio.org)

This repository contains the configurations and examples to use PlatformIO with
Industrial Shields PLCs based on ESP32 open-source hardware. Check [our
website](https://www.industrialshields.com/industrial-esp32-plc-products-family-ideal-for-iot-solutions)
for the full product family.

## Quick Start

1. [Install PlatformIO](https://platformio.org)
2. Create a `platformio.ini` in your project (or use `pio init` to create it),
   and add the following contents:

```ini
[env:my_plc]
platform = https://github.com/Industrial-Shields/platform-industrialshields-esp32
framework = arduino
board = esp32plc_cpu
custom_version = 3
custom_click1 = None
custom_click2 = None
```

3. Build: `pio run -e my_plc`

## Board Configuration Reference

### ESP32 PLC Family

Boards: `esp32plc_cpu`, `esp32plc_19r`, `esp32plc_21`, `esp32plc_38ar`, `esp32plc_38r`, `esp32plc_42`, `esp32plc_50rra`, `esp32plc_53arr`, `esp32plc_54ara`, `esp32plc_57aar`, `esp32plc_57r`, `esp32plc_58`

| Option           | Default | Values                                                                                                      |
|------------------|---------|-------------------------------------------------------------------------------------------------------------|
| `custom_version` | 3       | `3` or `1` (legacy)                                                                                         |
| `custom_click1`  | None    | `None`, `GPRS`, `NB`, `LTE`, `CAN`, `LORA_EU`, `LORA_EUROPA`, `LORA_AMERICA`, `LORA_ASIA`, `GPS_1`, `GPS_4` |
| `custom_click2`  | None    | same as `custom_click1`                                                                                     |

```ini
[env:esp32plc_example]
platform = https://github.com/Industrial-Shields/platform-industrialshields-esp32
framework = arduino
board = esp32plc_cpu
custom_version = 3
custom_click1 = NB
custom_click2 = LORA_EU
```

### 14 IOs PLC Family

Boards: `14iosplc_ma`, `14iosplc_v`

| Option           | Default | Values                                                                                                             |
|------------------|---------|--------------------------------------------------------------------------------------------------------------------|
| `custom_version` | 4       | `4` or `1` (legacy)                                                                                                |
| `custom_click`   | None    | `None`, `NB`, `LTE`, `DALI`, `CAN`, `LORA_EU`, `LORA_EUROPA`, `LORA_AMERICA`, `LORA_ASIA`, `GPS_1`, `GPS_4`, `RTC` |

```ini
[env:14ios_example]
platform = https://github.com/Industrial-Shields/platform-industrialshields-esp32
framework = arduino
board = 14iosplc_ma
custom_version = 4
custom_click = DALI
```

### 10 IOs PLC Family

Boards: `10iosplc_digital`, `10iosplc_relay`

No extra options required.

```ini
[env:10ios_example]
platform = https://github.com/Industrial-Shields/platform-industrialshields-esp32
framework = arduino
board = 10iosplc_relay
```

### WiFi Module

Board: `wifi_module`

No extra options required.

```ini
[env:wifi_example]
platform = https://github.com/Industrial-Shields/platform-industrialshields-esp32
framework = arduino
board = wifi_module
```

## Available Boards

| Board ID                | Description                      |
|-------------------------|----------------------------------|
| `esp32plc_cpu`          | ESP32 PLC                        |
| `esp32plc_19r`          | ESP32 PLC 19R IO+                |
| `esp32plc_21`           | ESP32 PLC 21 IO+                 |
| `esp32plc_38ar`         | ESP32 PLC 38AR IO+               |
| `esp32plc_38r`          | ESP32 PLC 38R IO+                |
| `esp32plc_42`           | ESP32 PLC 42 IO+                 |
| `esp32plc_50rra`        | ESP32 PLC 50RRA IO+              |
| `esp32plc_53arr`        | ESP32 PLC 53ARR IO+              |
| `esp32plc_54ara`        | ESP32 PLC 54ARA IO+              |
| `esp32plc_57aar`        | ESP32 PLC 57AAR IO+              |
| `esp32plc_57r`          | ESP32 PLC 57R IO+                |
| `esp32plc_58`           | ESP32 PLC 58 IO+                 |
| `esp32plc` (deprecated) | ESP32 PLC (use `esp32plc_cpu`)   |
| `14iosplc_ma`           | 14 IOS PLC (4-20 mA)             |
| `14iosplc_v`            | 14 IOS PLC (0-10 V)              |
| `10iosplc_digital`      | 10 IOS PLC Digital               |
| `10iosplc_relay`        | 10 IOS PLC Relay                 |
| `wifi_module`           | WiFi Module                      |

## Platform Packages

You must specify a boards version in `platform_packages`:

```ini
[env]
platform_packages =
   framework-industrialshields-esp32@https://apps.industrialshields.com/main/arduino/boards/industrialshields-boards-esp32-2.6.1.tar.bz2
```

Check all available versions at https://apps.industrialshields.com/main/arduino/boards/
(versions below 2.1.6 do NOT support PlatformIO).

## Examples

Pre-configured examples are in the `examples/` directory:

| Example           | Description                        |
|-------------------|------------------------------------|
| blink             | Blink an LED                       |
| hello-world       | Serial hello world                 |
| rs232-receive     | Receive data through RS232         |
| rs232-send        | Send data through RS232            |
| rs485-receive     | Receive data through RS485         |
| rs485-send        | Send data through RS485            |

Build an example:

```bash
pio run -d examples/blink -e esp32plc_cpu_v3
```

## Partition Scheme

All boards with 16MB flash default to `default_16MB` scheme (two 6.25MB app
partitions for OTA and a ~3.5 MB SPIFFS data partition) that comes with the
boards. You can override it with:

```ini
board_build.partitions = my_partitions.csv
```

## Upload Protocols

Default protocol is `esptool` (serial). Other options:

| Protocol      | Description                      |
|---------------|----------------------------------|
| `esptool`     | Serial upload (default)          |
| `espota`      | Over-the-air (WiFi) upload       |
| `custom`      | Custom upload command            |

To make an OTA you need to write the IP/hostname you want to upload it to:

```ini
upload_protocol = espota
upload_port = 192.168.1.100
```
