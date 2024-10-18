import asyncio
from bleak import BleakClient, BleakScanner
import time
from threading import Thread


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

def end():
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
    time.sleep(0.1)
    threadCommand("reset")
    time.sleep(0.1)
    threadCommand("reset")
    time.sleep(0.1)

def cancelTasks() -> None:

    global later
    try:
        if later:
            later.cancel()
    except:
        pass

def setTime(t):
    if len(t) == 6 and t.isnumeric():
        hardReset()
        threadCommand("edit")
        time.sleep(0.1)
        for i in range(len(t)):
            threadCommand(t[i])
            time.sleep(0.1)
        threadCommand("enter")
        time.sleep(0.1)
        return True
    else:
        return False


def power():
    cancelTasks()
    threadCommand("power")

def reset():
    cancelTasks()
    hardReset()

def start():
    cancelTasks()
    threadCommand("start")

def stop():
    cancelTasks()
    threadCommand("stop")
