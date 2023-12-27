import json
import os

base_json = """
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


FILE_NAME = 0
NAME = 1
VARIANT = 2
EXTRA_FLAGS = 3
URL = 4


def generate_json(plc: tuple[str, str, str, str, str]) -> str:
    new_json = json.loads(base_json)

    new_json["name"] = plc[NAME]
    new_json["build"]["variant"] = plc[VARIANT]
    new_json["build"]["extra_flags"] += ' ' + plc[EXTRA_FLAGS]
    new_json["url"] = plc[URL]
    
    return json.dumps(new_json, indent=4)

SCRIPT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
BOARDS_DIRECTORY = os.path.join(SCRIPT_DIRECTORY, "boards/")
def generate_file(plc: tuple[str, str, str, str, str]) -> None:    
    file_directory = BOARDS_DIRECTORY + plc[FILE_NAME] + ".json"
    with open(file_directory, 'w') as f:
        f.write(generate_json(plc))


wifi_module = [("wifi_module", "WiFi Module", "esp32plc", "-DWIFI_MODULE", "")]

esp32plcs = [("esp32plc", "ESP32 PLC", "esp32plc", "-DESP32PLC", ""),
             ("esp32plc_19r", "ESP32 PLC 19R IO+", "esp32plc", "-DESP32PLC -DESP32PLC_19R", "www.industrialshields.com/shop/esp32-plc-21-2801"),
             ("esp32plc_21", "ESP32 PLC 21 IO+", "esp32plc", "-DESP32PLC -DESP32PLC_21", "www.industrialshields.com/shop/esp32-plc-19r-2905"),
             ("esp32plc_38ar", "ESP32 PLC 38AR IO+", "esp32plc", "-DESP32PLC -DESP32PLC_38AR", "www.industrialshields.com/shop/esp32-plc-38ar-2910"),
             ("esp32plc_38r", "ESP32 PLC 38R IO+", "esp32plc", "-DESP32PLC -DESP32PLC_38R", "www.industrialshields.com/shop/esp32-plc-38r-2906"),
             ("esp32plc_42", "ESP32 PLC 42 IO+", "esp32plc", "-DESP32PLC -DESP32PLC_42", "www.industrialshields.com/shop/esp32-plc-42-2907"),
             ("esp32plc_50rra", "ESP32 PLC 50RRA IO+", "esp32plc", "-DESP32PLC -DESP32PLC_50RRA", "www.industrialshields.com/shop/esp32-plc-50rra-2912"),
             ("esp32plc_53arr", "ESP32 PLC 53ARR IO+", "esp32plc", "-DESP32PLC -DESP32PLC_53ARR", "www.industrialshields.com/shop/esp32-plc-53arr-2913"),
             ("esp32plc_54ara", "ESP32 PLC 54ARA IO+", "esp32plc", "-DESP32PLC -DESP32PLC_54ARA", "www.industrialshields.com/shop/esp32-plc-54ara-2914"),
             ("esp32plc_57aar", "ESP32 PLC 57AAR IO+", "esp32plc","-DESP32PLC -DESP32PLC_57AAR", "www.industrialshields.com/shop/esp32-plc-57aar-2911"),
             ("esp32plc_57r", "ESP32 PLC 57R IO+", "esp32plc", "-DESP32PLC -DESP32PLC_57R", "www.industrialshields.com/shop/esp32-plc-57r-2908"),
             ("esp32plc_58", "ESP32 PLC 58 IO+", "esp32plc", "-DESP32PLC -DESP32PLC_58", "www.industrialshields.com/shop/esp32-plc-58-2909")]

_10iosplcs = [("10iosplc_digital", "10 IOS PLC Digital", "10iosplc", "-DPLC10IOS -DPLC10IOS_DIGITAL", "www.industrialshields.com/shop/013002000100-i2c-10-i-o-s-digital-module-cpu-esp32-m-2977"),
             ("10iosplc_relay", "10 IOS PLC Relay", "10iosplc", "-DPLC10IOS -DPLC10IOS_RELAY", "www.industrialshields.com/shop/013002000200-i2c-10-i-o-s-relay-module-cpu-esp32-m-2978")]

_14iosplcs = [("14iosplc_ma", "ESP32 PLC 14 (4-20 mA)", "14iosplc", "-DPLC14IOS -DPLC14IOS_MA", ""),
             ("14iosplc_v", "ESP32 PLC 14 (0-10 V)", "14iosplc", "-DPLC14IOS -DPLC14IOS_V", "")]


if __name__ == "__main__":
    from itertools import chain
    
    for plc in chain(wifi_module, esp32plcs, _10iosplcs, _14iosplcs):
        generate_file(plc)
