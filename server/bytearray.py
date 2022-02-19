import sys
import platform
import asyncio
import logging

from bleak import BleakClient
from bleak import BleakScanner

# these are the write values associated with inputs, as logged from iOS
hex_power = "1F30 4145 09"
hex_reset = "1F30 414F 09"
hex_start = "1F30 4151 09"
hex_stop = "1F30 4150 09"

ba_power = bytes.fromhex(hex_power)
ba_reset = bytes.fromhex(hex_reset)
ba_start = bytes.fromhex(hex_start)
ba_stop = bytes.fromhex(hex_stop)

io_uuid = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"

TIMER_NAME = "GxTimer_31A0"
address = "BA:03:C4:2F:31:A0"

async def discover():
    devices = await BleakScanner.discover()
    for d in devices:
        if d.name == TIMER_NAME:
            print("Timer Found")
            for property, value in vars(d).items():
                print(property, ':', value)
            address = d.address

async def main(address):
    async with BleakClient(address) as client:
        print("Pairing...")
        paired = await client.pair()
        print(paired)
        await client.write_gatt_char(io_uuid, ba_power)
        await asyncio.sleep(3.0)
        await client.write_gatt_char(io_uuid, ba_power)

asyncio.run(discover())
asyncio.run(main(address))