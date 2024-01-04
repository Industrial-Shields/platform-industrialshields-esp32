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


// Include Industrial Shields libraries
#include <RS485.h>

//// IMPORTANT: check switches configuration

////////////////////////////////////////////////////////////////////////////////////////////////////
void setup() {
  // Begin serial port
  Serial.begin(9600);

  // Begin RS485 port
  RS485.begin(38400);
}

////////////////////////////////////////////////////////////////////////////////////////////////////
void loop() {
  // Wait bytes in the serial port
  if (Serial.available()) {
    byte tx = Serial.read();

    // Echo the byte to the serial port again
    Serial.write(tx);

    // And send it to the RS-485 port
    RS485.write(tx);
  }
}
