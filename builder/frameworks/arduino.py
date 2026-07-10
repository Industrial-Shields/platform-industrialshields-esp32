# Copyright 2014-present PlatformIO <contact@platformio.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Copyright (c) 2023 Boot&Work Corp., S.L. All rights reserved
#
# This file is part of platform-industrialshields-esp32.
#
# platform-industrialshields-esp32 is free software: you can redistribute
# it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# platform-industrialshields-esp32 is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Arduino

Arduino Wiring-based Framework allows writing cross-platform software to
control devices attached to a wide range of Arduino boards to create all
kinds of creative coding, interactive objects, spaces or physical experiences.

http://arduino.cc/en/Reference/HomePage
"""

from os.path import join

from SCons.Script import DefaultEnvironment, SConscript

env = DefaultEnvironment()
board = env.BoardConfig()
build_core = board.get("build.core", "").lower()

SConscript("_embed_files.py", exports="env")


# Industrial Shields custom logic

build_flags = []

boardsDirectory = DefaultEnvironment().PioPlatform().get_package_dir("framework-industrialshields-esp32")
plcPeripheralsDirectory = join(boardsDirectory, "cores", "industrialshields", "plc-peripherals", "include")
build_flags.append(f"-I{plcPeripheralsDirectory}")

ESP32PLC_CLICK_FLAGS = {
    "GPRS":          ["GPRS"],
    "NB":            ["NB"],
    "LTE":           ["LTE"],
    "CAN":           ["CAN"],
    "LORA_EUROPA":   ["LORA", "LORA_EUROPA"],
    "LORA_EU":       ["LORA", "LORA_EUROPA"],
    "LORA_AMERICA":  ["LORA", "LORA_AMERICA"],
    "LORA_ASIA":     ["LORA", "LORA_ASIA"],
}

def click_macros_esp32plc(click: str, number: int) -> None:
    if number != 1 and number != 2:
        raise RuntimeError(f"Number {number} is incorrect. It should either be 1 or 2.")

    if click == "None":
        # "None" click is being used, do not add any flags
        return

    if click not in ESP32PLC_CLICK_FLAGS.keys():
        raise ValueError(f"Unknown type of click: {click}, only valid "
                         f"values are: {', '.join(ESP32PLC_CLICK_FLAGS)}")

    build_flags.append(f"-DEXPANSION_MODULE{number}")
    for suffix in ESP32PLC_CLICK_FLAGS[click]:
        build_flags.append(f"-DEXPANSION_MODULE{number}_{suffix}")


PLC14IOS_CLICK_FLAGS = {
    "NB": "NB",
    "LTE": "LTE",
    "DALI": "DALI",
    "LORA_EUROPA": "LORA_EUROPA",
    "LORA_EU": "LORA_EUROPA",
    "LORA_AMERICA": "LORA_AMERICA",
    "LORA_ASIA": "LORA_ASIA",
}

def click_macros_14iosplc(click: str) -> None:
    if click == "None":
        return

    if click not in PLC14IOS_CLICK_FLAGS.keys():
        raise ValueError(f"Unknown type of click: {click}, only valid "
                         f"values are: {', '.join(PLC14IOS_CLICK_FLAGS)}")

    suffix = PLC14IOS_CLICK_FLAGS[click]
    build_flags.append("-DEXPANSION_MODULE")
    build_flags.append(f"-DEXPANSION_MODULE_{suffix}")


if (board.get("build.variant") == "esp32plc"):
    custom_version = int(env.GetProjectOption("custom_version", default = "3"))
    if custom_version == 3:
        build_flags.append("-DESP32PLC_V3")
    elif custom_version == 1:
        build_flags.append("-DESP32PLC_V1")
    else:
        raise Exception("You need to specify version '3' or '1' of the ESP32 PLC")

    click_macros_esp32plc(env.GetProjectOption("custom_click1", default = "None"), 1)
    click_macros_esp32plc(env.GetProjectOption("custom_click2", default = "None"), 2)

elif (board.get("build.variant") == "14iosplc"):
    click_macros_14iosplc(env.GetProjectOption("custom_click", default = "None"))

env.Append(CCFLAGS=build_flags)


if "espidf" not in env.subst("$PIOFRAMEWORK"):
    SConscript(
        join(DefaultEnvironment().PioPlatform().get_package_dir(
            "framework-industrialshields-esp32"), "tools", "platformio-build.py"))
    env["INTEGRATION_EXTRA_DATA"].update({"application_offset": env.subst("$ESP32_APP_OFFSET")})
