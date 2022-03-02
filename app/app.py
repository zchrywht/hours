import asyncio
from bleak import BleakClient, BleakScanner
import time
from threading import Thread
from flask import Flask, render_template, request, redirect

TIMER_NAME = "GxTimer_31A0"

async def sendCommand(command):

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

    time.sleep(0.1)

    await client.write_gatt_char(IO_UUID, COMMANDS[command])

    time.sleep(0.1)
    
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

async def pair():
    client =  BleakClient(address)
    while True:
        try:
            if not client.is_connected:
                print("connecting...")
                await client.connect()
                print("connected")
            print("pairing...")
            await client.pair()
            print("paired.")
            return client
        except Exception as e:
            print("pairing failed, retrying...")
            pass

def stop():
    disconnected = asyncio.run_coroutine_threadsafe(client.disconnect(), loop).result()
    loop.call_soon_threadsafe(loop.stop)
    while True:
        if not loop.is_running():
            loop.close()
            return

def start_background_loop(loop: asyncio.AbstractEventLoop) -> None:
    asyncio.set_event_loop(loop)
    loop.run_forever()

def begin() -> None:
    # create new event loop, assign to "background" thread, start
    global loop
    loop = asyncio.new_event_loop()
    t = Thread(target=start_background_loop, args=(loop,))
    t.start()

    # find timer and pair with it
    global address
    address_future = asyncio.run_coroutine_threadsafe(discover(), loop)
    address = address_future.result()

    global client
    client_future = asyncio.run_coroutine_threadsafe(pair(), loop)
    client = client_future.result()

# commands

def stringToSeconds(t):
    # takes a time in format "HHMMSS" and converts it into seconds
    hours = int(t[:2])
    minutes = int(t[2:4])
    seconds = int(t[4:])

    return ((hours * 3600) + (minutes * 60) + seconds)

def threadCommand(command) -> None:
    asyncio.run_coroutine_threadsafe(sendCommand(command), loop)

def hardReset() -> None:
    threadCommand("stop")
    threadCommand("reset")
    threadCommand("reset")

def cancelTasks() -> None:
    allTasks = asyncio.all_tasks(loop)
    print(allTasks)
    for task in allTasks:
        task.cancel()

def setTime(t):
    if len(t) == 6 and t.isnumeric():
        threadCommand("stop")
        threadCommand("reset")
        threadCommand("reset")
        threadCommand("edit")
        for i in range(len(t)):
            threadCommand(t[i])
        threadCommand("enter")
        return True
    else:
        return False

def runReset(startTime, maxTime):

    print("setting time: " + startTime)
    setTime(startTime)
    print("starting...")
    time.sleep(0.5)
    threadCommand("start")
    cycleLengthSeconds = stringToSeconds(maxTime)
    startTimeSeconds = stringToSeconds(startTime)
    timeRemaining = cycleLengthSeconds - startTimeSeconds
    print("sleeping for " + str(timeRemaining) + " seconds")
    loop.call_later(timeRemaining + 1.5, hardReset)

    return

def cycle(startTime, maxTime):
    while True:
        runReset(startTime, maxTime)

# define app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# basic commands 

@app.route('/power', methods=['POST'])
def power():
    threadCommand("power")
    return redirect('/')

@app.route('/reset', methods=['POST'])
def reset():
    hardReset()
    return redirect('/')

@app.route('/start', methods=['POST'])
def start():
    threadCommand("start")
    return redirect('/')

@app.route('/stop', methods=['POST'])
def stop():
    threadCommand("stop")
    return redirect('/')

# routines

@app.route('/set', methods=['POST'])
def set():
    t = request.form['time']
    setTime(t)
    return redirect('/')

@app.route('/run', methods=['POST'])
def run():
    start = request.form['startTime']
    end = request.form['maxTime']
    runReset(start, end)
    return redirect('/')

@app.route('/cycle', methods=['POST'])
def cyc():
    start = request.form['startTime']
    end = request.form['maxTime']
    cycle(start, end)
    return redirect('/')

if __name__ == "__main__":
    begin()
    app.run(debug=False, host='0.0.0.0') # nothing after this will execute
    stop()
