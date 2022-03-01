from flask import Flask, render_template, request, redirect
#from quart import Quart, render_template, request, redirect
import asyncio
from bleak import BleakClient
from bleak import BleakScanner
import time

TIMER_NAME = "GxTimer_31A0"
address = "BA:03:C4:2F:31:A0"
IO_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"

def stringToSeconds(t):
    # takes a time in format "HHMMSS" and converts it into seconds
    hours = int(t[:2])
    minutes = int(t[2:4])
    seconds = int(t[4:])

    return ((hours * 3600) + (minutes * 60) + seconds)

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

async def cycle(client, startTime, maxTime):
    # starts clock at startTime, runs until max time is reached, then starts over
    await setTime(client, startTime)
    await asyncio.sleep(0.5)
    await sendCommand(client, "start")
    now = time.time()
    print(now)
    cycleLength = stringToSeconds(maxTime)
    startTimeSeconds = stringToSeconds(startTime)
    endTime = now + cycleLength - startTimeSeconds
    while True:
        await asyncio.sleep(0.1)
        now = time.time()
        if now > endTime:
            print("resetting...")
            await sendCommand(client, "stop")
            await asyncio.sleep(0.1)
            await sendCommand(client, "reset")
            await asyncio.sleep(0.1)
            await sendCommand(client, "reset")
            await asyncio.sleep(0.1)
            await sendCommand(client, "start")
            endTime = now + cycleLength


async def setTime(client, t):
    # time should be string in format "HHMMSS"
    if len(t) == 6 and t.isnumeric():
        await sendCommand(client, "stop")
        await sendCommand(client, "reset")
        await sendCommand(client, "reset")
        await sendCommand(client, "edit")
        for i in range(len(t)):
            await sendCommand(client, t[i])
        await sendCommand(client, "enter")
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
                    return d.address

async def run(address):
    while True:
        try:
            async with BleakClient(address) as client:
                print("Pairing with " + address)
                paired = await client.pair()
                print("Paired with timer.")
                
                await sendCommand(client, "power")
                await asyncio.sleep(1)
                await sendCommand(client, "power")
                
                #app = Quart(__name__)
                app = Flask(__name__)
                
                print("app created")

                @app.route('/')
                def index():
                    return render_template('index.html')
                    
                @app.route('/test', methods=['POST'])
                async def test():
                    print("test")
                    return redirect('/')

                @app.route('/power', methods=['POST'])
                async def power():
                    await client.write_gatt_char(IO_UUID, COMMANDS["power"])
                    #await sendCommand(client, "power")
                    return redirect('/')

                @app.route('/reset', methods=['POST'])
                async def reset():
                    await sendCommand(client, "reset")
                    return redirect('/')

                @app.route('/start', methods=['POST'])
                async def start():
                    await sendCommand(client, "start")
                    return redirect('/')

                @app.route('/stop', methods=['POST'])
                async def stop():
                    await sendCommand(client, "stop")
                    return redirect('/')

                @app.route('/set-time', methods=['POST'])
                async def time():
                    t = request.form['time']
                    await setTime(client, t)
                    return redirect('/')

                @app.route('/cycle', methods=['POST'])
                async def c():
                    start = request.form['startTime']
                    end = request.form['maxTime']
                    await setTime(client, start)
                    await cycle(client, start, end)
                    return redirect('/')

                if __name__ == '__main__':
                    await app.run(debug=False, host='0.0.0.0') # nothing after this will execute
                    
        except Exception as e:
            print(e)


async def main():
    print("finding address...")
    address = await discover()
    print("running...")
    await run(address)

#async def setTime()

asyncio.run(main())
