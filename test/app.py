#from flask import Flask, render_template, request, redirect
from quart import Quart, render_template, request, redirect
import asyncio
from bleak import BleakClient, BleakScanner
import nest_asyncio

#nest_asyncio.apply()

TIMER_NAME = "GxTimer_31A0"
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
                    print("Timer Found")
                    return d.address

async def main():
    address = await discover()
    while True:
        try:
            async with BleakClient(address) as client:

                await client.pair()

                app = Quart(__name__)

                @app.route('/')
                def index():
                    return render_template('index.html')

                @app.route('/power', methods=['POST'])
                def power():
                    #loop = asyncio.get_event_loop()
                    #print(loop)
                    #asyncio.run_coroutine_threadsafe(sendCommand(client, "power"), loop)
                    #await client.write_gatt_char(IO_UUID, COMMANDS['power'])
                    return redirect('/')

                if __name__ == '__main__':
                    await app.run_task(debug=False, host='0.0.0.0')
                    #app.run(debug=False, host='0.0.0.0') # nothing after this will execute

        except Exception as e:
            print(e)


asyncio.run(main())
