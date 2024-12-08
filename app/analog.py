import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADS object and specify the gain
ads = ADS.ADS1115(i2c)
ads.gain = 1 
chan = AnalogIn(ads, ADS.P0)
rst = AnalogIn(ads, ADS.P1)

def analogRead(a0, a1):


    if a0 < 0.25:
        return "R"
    elif a0 < 0.75:
        return "U"
    elif a0 < 1.5:
        return "D"
    elif a0 < 2.5:
        return "L"
    elif a0 < 3.5:
        return "S"
    elif a1 < 0.5:
        return "E"
    else:
        return

def getInput():
    v0 = analogRead(chan.voltage, rst.voltage)
    if v0:
        time.sleep(0.001)
        v1 = analogRead(chan.voltage, rst.voltage)
        if v1 and v0 == v1:
            return v1
    return