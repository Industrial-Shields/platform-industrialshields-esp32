"""
Copyright (c) 2023 Boot&Work Corp., S.L. All rights reserved

This file is part of platform-industrialshields-esp32.

platform-industrialshields-esp32 is free software: you can redistribute
it and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

platform-industrialshields-esp32 is distributed in the hope that it will
be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


PLC Configuration Generator

This script generates all the configuration files that PlatformIO
needs for all the Industrial Shields PLCs based on ESP32 boards.
"""
from json_generator import JSON_PLC
import os
from itertools import chain



SCRIPT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
BOARDS_DIRECTORY = os.path.join(SCRIPT_DIRECTORY, "boards/")


esp32_basejson = """
{
  "build": {
    "arduino":{
      "ldscript": "esp32_out.ld"
    },
    "core": "industrialshields",
    "extra_flags": "",
    "f_cpu": "240000000L",
    "f_flash": "40000000L",
    "flash_mode": "dio",
    "mcu": "esp32",
    "variant": ""
  },
  "connectivity": [
    "wifi",
    "bluetooth",
    "ethernet"
  ],
  "frameworks": [
    "arduino"
  ],
  "name": "",
  "upload": {
    "flash_size": "4MB",
    "maximum_ram_size": 327680,
    "maximum_size": 1310720,
    "require_upload_port": true,
    "speed": 460800
  },
  "url": "",
  "vendor": "Industrial Shields"
}
"""



def E(file_name: str, name: str, variant: str, extra_flags: str, url: str) \
        -> JSON_PLC:
    """
    Create a JSON_PLC instance for ESP32 based PLCs.
    """
    return JSON_PLC(file_name, name, variant, extra_flags, url, esp32_basejson)



wifi_module = [E("wifi_module", "WiFi Module", "esp32plc", "-DWIFI_MODULE", "NOURL")]
    
esp32plcs = [E("esp32plc", "ESP32 PLC", "esp32plc", "-DESP32PLC", ""),
             E("esp32plc_19r", "ESP32 PLC 19R IO+", "esp32plc", "-DESP32PLC -DESP32PLC_19R", "www.industrialshields.com/shop/esp32-plc-21-2801"),
             E("esp32plc_21", "ESP32 PLC 21 IO+", "esp32plc", "-DESP32PLC -DESP32PLC_21", "www.industrialshields.com/shop/esp32-plc-19r-2905"),
             E("esp32plc_38ar", "ESP32 PLC 38AR IO+", "esp32plc", "-DESP32PLC -DESP32PLC_38AR", "www.industrialshields.com/shop/esp32-plc-38ar-2910"),
             E("esp32plc_38r", "ESP32 PLC 38R IO+", "esp32plc", "-DESP32PLC -DESP32PLC_38R", "www.industrialshields.com/shop/esp32-plc-38r-2906"),
             E("esp32plc_42", "ESP32 PLC 42 IO+", "esp32plc", "-DESP32PLC -DESP32PLC_42", "www.industrialshields.com/shop/esp32-plc-42-2907"),
             E("esp32plc_50rra", "ESP32 PLC 50RRA IO+", "esp32plc", "-DESP32PLC -DESP32PLC_50RRA", "www.industrialshields.com/shop/esp32-plc-50rra-2912"),
             E("esp32plc_53arr", "ESP32 PLC 53ARR IO+", "esp32plc", "-DESP32PLC -DESP32PLC_53ARR", "www.industrialshields.com/shop/esp32-plc-53arr-2913"),
             E("esp32plc_54ara", "ESP32 PLC 54ARA IO+", "esp32plc", "-DESP32PLC -DESP32PLC_54ARA", "www.industrialshields.com/shop/esp32-plc-54ara-2914"),
             E("esp32plc_57aar", "ESP32 PLC 57AAR IO+", "esp32plc","-DESP32PLC -DESP32PLC_57AAR", "www.industrialshields.com/shop/esp32-plc-57aar-2911"),
             E("esp32plc_57r", "ESP32 PLC 57R IO+", "esp32plc", "-DESP32PLC -DESP32PLC_57R", "www.industrialshields.com/shop/esp32-plc-57r-2908"),
             E("esp32plc_58", "ESP32 PLC 58 IO+", "esp32plc", "-DESP32PLC -DESP32PLC_58", "www.industrialshields.com/shop/esp32-plc-58-2909")]

_10iosplcs = [E("10iosplc_digital", "10 IOS PLC Digital", "10iosplc", "-DPLC10IOS -DPLC10IOS_DIGITAL", "www.industrialshields.com/shop/013002000100-i2c-10-i-o-s-digital-module-cpu-esp32-m-2977"),
              E("10iosplc_relay", "10 IOS PLC Relay", "10iosplc", "-DPLC10IOS -DPLC10IOS_RELAY", "www.industrialshields.com/shop/013002000200-i2c-10-i-o-s-relay-module-cpu-esp32-m-2978")]

_14iosplcs = [E("14iosplc_ma", "ESP32 PLC 14 (4-20 mA)", "14iosplc", "-DPLC14IOS -DPLC14IOS_MA", "NOURL"),
              E("14iosplc_v", "ESP32 PLC 14 (0-10 V)", "14iosplc", "-DPLC14IOS -DPLC14IOS_V", "NOURL")]


for plc in chain(wifi_module, esp32plcs, _10iosplcs, _14iosplcs):
    plc.generate_file(BOARDS_DIRECTORY)
