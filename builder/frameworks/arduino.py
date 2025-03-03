"""
Copyright 2014-present PlatformIO <contact@platformio.org>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


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

def click_macros(click: str, number: int) -> str:
    if click == "GPRS":
        return f"-DEXPANSION_MODULE{number}_GPRS "
    elif click == "None":
        return f""
    else:
        raise(f"Unknown type of click: {click}, only valid"
        "values are: GPRS")

if (board.get("build.variant") == "esp32plc"):
    custom_version = int(env.GetProjectOption("custom_version"))
    custom_click1 = env.GetProjectOption("custom_click1")
    custom_click2 = env.GetProjectOption("custom_click2")

    build_flags = []

    if custom_version == 3:
        build_flags.append("-DESP32PLC_V3")
    elif custom_version == 1:
        build_flags.append("-DESP32PLC_V1")
    else:
        raise("You need to specify version '3' or '1' of the ESP32 PLC")

    build_flags.append(click_macros(custom_click1, 1))
    build_flags.append(click_macros(custom_click2, 2))

    boardsDirectory = DefaultEnvironment().PioPlatform().get_package_dir("framework-industrialshields-esp32")
    plcPeripheralsDirectory = join(boardsDirectory, "cores", "industrialshields", "plc-peripherals", "include")
    build_flags.append(f"-I{plcPeripheralsDirectory}")


    env.Append(CCFLAGS=build_flags)



if build_core == "mbcwb":
    SConscript(
        join(DefaultEnvironment().PioPlatform().get_package_dir(
            "framework-arduino-mbcwb"), "tools", "platformio-esp-build.py"))

elif "espidf" not in env.subst("$PIOFRAMEWORK"):
    SConscript(
        join(DefaultEnvironment().PioPlatform().get_package_dir(
            "framework-industrialshields-esp32"), "tools", "platformio-build.py"))
    env["INTEGRATION_EXTRA_DATA"].update({"application_offset": env.subst("$ESP32_APP_OFFSET")})

