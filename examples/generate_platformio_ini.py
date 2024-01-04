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
   framework-industrialshields-esp32@https://apps.industrialshields.com/main/arduino/boards/industrialshields-boards-esp32-2.1.6.tar.bz2

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
build_flags = !python extra_build_flags.py -v {} ;--click1 GPRS ; --click2 GPRS
"""


def separate_if_discriminator(strings_list: list[str, ...], discriminator: str) \
        -> (list[str, ...], list[str, ...]):
    """
    Separates a list of strings based on the presence of a discriminator.

    Args:
        strings_list (list): List of strings to be separated.
        discriminator (str): Discriminator string for separation.

    Returns:
        tuple: Two lists, one containing strings with the discriminator, and the other without.
    """
    complying_boards_names, noncomplying_boards_names = [], []

    for board in strings_list:
        if discriminator in board:
            complying_boards_names.append(board)
        else:
            noncomplying_boards_names.append(board)

    return complying_boards_names, noncomplying_boards_names



# Generate a list of board names by removing ".json" extension from files in the boards directory
boards_names = [f.replace(".json", "") for f in os.listdir(BOARDS_DIRECTORY)
                if path.isfile(path.join(BOARDS_DIRECTORY, f))]


# Separate first the ESP32 PLCs
esp32plcs_boards, leftover_boards_names = separate_if_discriminator(boards_names, 'esp32plc')

# Separate the 14 IOs from the leftovers
_14ios_boards, leftover_boards_names = separate_if_discriminator(leftover_boards_names, "14ios")

# Separate the 10 IOs from the leftovers
_10ios_boards, leftover_boards_names = separate_if_discriminator(leftover_boards_names, "10ios")


# Write the PlatformIO configuration to a new file
with open("platformio.ini", 'w', encoding="utf-8") as new_file:

    new_file.write(BASE_PLATFORMIO_INI)

    # ESP32 PLC boards v3
    for board_name in esp32plcs_boards:
        new_file.write(ESP32_ENV.format(board_name, 3, board_name, 3))

    # 14 IOs
    for board_name in _14ios_boards:
        new_file.write(BASE_ENV.format(board_name, board_name))

    # ESP32 PLC boards v1
    for board_name in esp32plcs_boards:
        new_file.write(ESP32_ENV.format(board_name, 1, board_name, 1))

    # Other boards
    for board_name in chain(_10ios_boards, leftover_boards_names):
        new_file.write(BASE_ENV.format(board_name, board_name))
