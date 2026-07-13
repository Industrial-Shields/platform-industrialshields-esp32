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


Script to generate the PlatformIO configuration for ESP32-based PLCs.
The generated configuration file is saved in the same location from
which the script is called.
"""

import os
from os import path
from itertools import chain



SCRIPT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
BOARDS_DIRECTORY = os.path.join(SCRIPT_DIRECTORY, "../boards/")

# base content of the PlatformIO configuration file
BASE_PLATFORMIO_INI = \
"""
; PlatformIO Project Configuration File
;
;   Build options: build flags, source filter
;   Upload options: custom upload port, speed and extra flags
;   Library options: dependencies, extra library storages
;   Advanced options: extra scripting
;
; Please visit documentation for the other options and examples
; https://docs.platformio.org/page/projectconf.html

[env]
platform_packages =
   framework-industrialshields-esp32@https://apps.industrialshields.com/main/arduino/boards/industrialshields-boards-esp32-2.3.1-hf.tar.bz2

"""

# Base content of a generic environment for ESP32-based boards
BASE_ENV = \
"""
[env:{}]
platform = https://github.com/Industrial-Shields/platform-industrialshields-esp32
framework = arduino
board = {}
"""

# Base content of a generic environment for ESP32 PLCs v1 and v3 boards
ESP32_ENV = \
"""
[env:{}_v{}]
platform = https://github.com/Industrial-Shields/platform-industrialshields-esp32
framework = arduino
board = {}
custom_version = {} ; 3, or 1 (legacy)
custom_click1 = None ; or GPRS, NB, LTE, CAN, LORA_EUROPA/LORA_EU, LORA_AMERICA, LORA_ASIA, GPS_1, GPS_4
custom_click2 = None ; or GPRS, NB, LTE, CAN, LORA_EUROPA/LORA_EU, LORA_AMERICA, LORA_ASIA, GPS_1, GPS_4
"""

# Base content of a generic environment for 14 IOS PLCs v1 and v4 boards
PLC14IOS_ENV = \
"""
[env:{}_v{}]
platform = https://github.com/Industrial-Shields/platform-industrialshields-esp32
framework = arduino
board = {}
custom_version = {} ; 4, or 1 (legacy)
custom_click = None ; or NB, LTE, DALI, CAN, LORA_EUROPA/LORA_EU, LORA_AMERICA, LORA_ASIA, GPS_1, GPS_4, RTC
"""


EXAMPLE_DIRS = [
    "blink",
    "hello-world",
    "rs232-receive",
    "rs232-send",
    "rs485-receive",
    "rs485-send",
]

EXAMPLE_FILTERS = {
    "hello-world": None,
    "blink": {"esp32plc_variant", "14ios", "10ios"},
    "rs232-send": {"esp32plc_cpu", "esp32plc_variant"},
    "rs232-receive": {"esp32plc_cpu", "esp32plc_variant"},
    "rs485-receive": {"esp32plc_cpu", "esp32plc_variant", "14ios", "10ios"},
    "rs485-send": {"esp32plc_cpu", "esp32plc_variant", "14ios", "10ios"},
}


def board_category(board_name: str) -> str:
    if board_name == "esp32plc":
        return "esp32plc_base"
    elif board_name == "esp32plc_cpu":
        return "esp32plc_cpu"
    elif board_name.startswith("esp32plc_"):
        return "esp32plc_variant"
    elif board_name.startswith("14ios"):
        return "14ios"
    elif board_name.startswith("10ios"):
        return "10ios"
    elif board_name == "wifi_module":
        return "wifi"
    return "other"


def separate_if_discriminator(strings_list: list[str, ...], discriminator: str) \
        -> (list[str, ...], list[str, ...]):
    complying_boards_names, noncomplying_boards_names = [], []

    for board in strings_list:
        if discriminator in board:
            complying_boards_names.append(board)
        else:
            noncomplying_boards_names.append(board)

    return complying_boards_names, noncomplying_boards_names


# Generate a list of board names by removing ".json" extension from files in the boards directory
boards_names = [f.replace(".json", "") for f in os.listdir(BOARDS_DIRECTORY)
                if path.isfile(path.join(BOARDS_DIRECTORY, f)) and f != "esp32plc.json"]


for example_dir in EXAMPLE_DIRS:
    filter_set = EXAMPLE_FILTERS.get(example_dir)
    if filter_set is None:
        filtered_boards = boards_names
    else:
        filtered_boards = [b for b in boards_names if board_category(b) in filter_set]

    # Separate first the ESP32 PLCs
    esp32plcs_boards, leftover_boards_names = separate_if_discriminator(filtered_boards, 'esp32plc')
    # Ensure esp32plc_cpu remains first in the list
    esp32plcs_boards.sort(key=lambda x: x != "esp32plc_cpu")

    # Separate the 14 IOs from the leftovers
    _14ios_boards, leftover_boards_names = separate_if_discriminator(leftover_boards_names, "14ios")

    # Separate the 10 IOs from the leftovers
    _10ios_boards, leftover_boards_names = separate_if_discriminator(leftover_boards_names, "10ios")

    filepath = path.join(SCRIPT_DIRECTORY, example_dir, "platformio.ini")
    with open(filepath, 'w', encoding="utf-8") as new_file:
        new_file.write(BASE_PLATFORMIO_INI)

        # ESP32 PLC boards v3
        for board_name in esp32plcs_boards:
            new_file.write(ESP32_ENV.format(board_name, 3, board_name, 3))

        # 14 IOs boards v4
        for board_name in _14ios_boards:
            new_file.write(PLC14IOS_ENV.format(board_name, 4, board_name, 4))

        # 14 IOs boards v1 (legacy)
        for board_name in _14ios_boards:
            new_file.write(PLC14IOS_ENV.format(board_name, 1, board_name, 1))

        # ESP32 PLC boards v1
        for board_name in esp32plcs_boards:
            new_file.write(ESP32_ENV.format(board_name, 1, board_name, 1))

        # Other boards
        for board_name in chain(_10ios_boards, leftover_boards_names):
            new_file.write(BASE_ENV.format(board_name, board_name))
