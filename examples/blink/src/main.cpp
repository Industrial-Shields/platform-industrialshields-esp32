/*
   Copyright (c) 2023 Boot&Work Corp., S.L. All rights reserved

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <Arduino.h>

#define OUTPUT_PIN Q0_1

void setup() {
    pinMode(OUTPUT_PIN, OUTPUT);
    Serial.begin(115200);

    Serial.println("Hello World");
}

void loop() {
    digitalWrite(OUTPUT_PIN, HIGH);
    delay(1000);
    digitalWrite(OUTPUT_PIN, LOW);
    delay(1000);
}