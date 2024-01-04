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


JSON_PLC Module

This module defines a data class, JSON_PLC, to represent a generic Industrial Shields PLC that is
based on the Arduino framework in a format that PlatformIO can understand. It provides the following
methods:
    - generate_json(): Generates a JSON string based on the configured PLC parameters.
    - generate_file(boards_directory: str): Creates a JSON file with the PLC configuration in the
    given directory.
    - add_family_variants(file_name_suffix: str, name_suffix: str, family_flags: str,
    url: str) -> JSON_PLC: Returns a new JSON_PLC instance with the added family data.
"""
import json
from os import path
from dataclasses import dataclass

from typing import Self



@dataclass
class JSON_PLC:
    """
    Represents a PlatformIO configuration for an Industrial Shields PLC, in JSON format.
    """
    file_name: str # Represents the name of the file containing a given PLC configuration
    name: str # The name of the PLC
    variant: str # Represents the variant of the PLC (in the Arduino framework terms)
    extra_flags: str # Additional build flags of the PLC. Might denote a specific model or feature
    url: str # The URL associated to the product
    base_json: str # Base JSON configuration of the PLC


    def __init__(self, file_name: str, name: str, variant: str, extra_flags: str, url: str,
                 base_json: str) -> Self:
        """
        Method to initialize a JSON_PLC instance.

        Use "NOURL" as URL to specify an empty URL for the new JSON_PLC.
        """
        if url == "NOURL":
            url = ""
        self.file_name = file_name
        self.name = name
        self.variant = variant
        self.extra_flags = extra_flags
        self.url = url
        self.base_json = base_json


    def generate_json(self) -> str:
        """
        Generate a JSON string based on the configured PLC parameters.

        Returns:
            str: JSON string representing the PLC configuration.
        """
        new_json = json.loads(self.base_json)

        new_json["name"] = self.name
        new_json["build"]["variant"] = self.variant
        new_json["build"]["extra_flags"] += ' ' + self.extra_flags
        new_json["url"] = self.url

        return json.dumps(new_json, indent=4)


    def generate_file(self, boards_directory: str) -> None:
        """
        Create a JSON file with the PLC configuration in the specified directory.

        Args:
            boards_directory (str): The directory where the JSON file will be created.
        """
        file_directory = path.join(boards_directory, self.file_name + ".json")
        with open(file_directory, 'w', encoding="utf-8") as new_file:
            new_file.write(self.generate_json())


    def add_family_variants(self, file_name_suffix: str, name_suffix: str,
                            family_flags: str, url: str) -> Self:
        """
        Returns a new JSON_PLC instance with added family variants to the PLC configuration.

        Args:
            file_name_suffix (str): Suffix to be added to the file name.
            name_suffix (str): Suffix to be added to the name.
            family_flags (str): Additional flags for family variants.
            url (str, optional): URL associated with the family variant.
            Defaults to "SAMEURL" (indicating the same URL as the original JSON_PLC).
            Use "NOURL" to specify an empty URL for the new JSON_PLC.

        Returns:
            JSON_PLC: A new JSON_PLC instance with added family variants.
        """
        if url == "SAMEURL":
            url = self.url
        elif url == "NOURL":
            url = ""

        return JSON_PLC(self.file_name + file_name_suffix,
                        self.name + name_suffix,
                        self.variant,
                        self.extra_flags + f" {family_flags}",
                        url,
                        self.base_json)
