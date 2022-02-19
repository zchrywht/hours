import asyncio
from bleak import BleakClient
from bleak import BleakScanner

TIMER_NAME = "GxTimer_31A0"
address = "BA:03:C4:2F:31:A0"

async def discover():
    devices = await BleakScanner.discover()
    for d in devices:
        if d.name == TIMER_NAME:
            for property, value in vars(d).items():
                print(property, ':', value)
            address = d.address

asyncio.run(discover())

async def connect(address):
    async with BleakClient(address) as client:
        print("client is connected")

        for service in client.services:
            print(service)

        client.disconnect()

asyncio.run(connect(address))