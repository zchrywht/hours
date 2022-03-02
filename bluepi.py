#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  bluepi.py
#  
#  Copyright 2022  <pi@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import asyncio
from bleak import BleakClient
from bleak import BleakScanner

IO_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"

COMMANDS = {
    "power" : bytes.fromhex("1F30 4145 09"),
    "reset" : bytes.fromhex("1F30 414F 09"),
    "start" : bytes.fromhex("1F30 4151 09"),
    "stop" : bytes.fromhex("1F30 4150 09"),
    "edit" : bytes.fromhex("1F30 4146 09"),
    "left" : bytes.fromhex("1F30 4148 09"),
    "right" : bytes.fromhex("1F30 4149 09"),
    "enter" : bytes.fromhex("1F30 4152 09"),
    "0" : bytes.fromhex("1F30 4130 09"),
    "1" : bytes.fromhex("1F30 4131 09"),
    "2" : bytes.fromhex("1F30 4132 09"),
    "3" : bytes.fromhex("1F30 4133 09"),
    "4" : bytes.fromhex("1F30 4134 09"),
    "5" : bytes.fromhex("1F30 4135 09"),
    "6" : bytes.fromhex("1F30 4136 09"),
    "7" : bytes.fromhex("1F30 4137 09"),
    "8" : bytes.fromhex("1F30 4138 09"),
    "9" : bytes.fromhex("1F30 4139 09"),
}

async def sendCommand(client, command):
    await client.write_gatt_char(IO_UUID, COMMANDS[command])
    return


async def discover():
    while True:
        print("Searching for timer...")
        devices = await BleakScanner.discover()
        for d in devices:
            if d.name:
                print(d.name)
                if "GxTimer_" in d.name:
                    print("Timer Found at " + d.address)
                    while True:
                        try:
                            async with BleakClient(d.address) as client:
                                print("Pairing with " + d.address)
                                paired = await client.pair()
                                print("Paired with timer.")
                                await sendCommand(client, "power")
                                return d.address
                        except:
                            print("pairing failed, retrying...")

async def run(address):
    async with BleakClient(address) as client:
        print("Pairing with " + address)
        paired = await client.pair()
        print("Paired with timer.")

async def main():
    address = await discover()
    #await run(address)
    
asyncio.run(main())
