from datetime import datetime, timedelta
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
from analog import getInput

# Modify this if you have a different sized character LCD
lcd_columns = 16
lcd_rows = 2

# Raspberry Pi Pin Config:
lcd_rs = digitalio.DigitalInOut(board.D25)
lcd_en = digitalio.DigitalInOut(board.D24)
lcd_d7 = digitalio.DigitalInOut(board.D22)
lcd_d6 = digitalio.DigitalInOut(board.D21)
lcd_d5 = digitalio.DigitalInOut(board.D17)
lcd_d4 = digitalio.DigitalInOut(board.D23)
lcd_backlight = digitalio.DigitalInOut(board.D4)

# Initialise the lcd class
lcd = characterlcd.Character_LCD_Mono(
    lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight
)

# Open the serial port (replace '/dev/ttyUSB0' with your correct port)
#ser = serial.Serial('/dev/ttyUSB0', 9600)

class Display():
    
    def __init__(self) -> None:
        self.time = [0,0,0,0,0,0]
        self.editIndex = 0

    def updateTime(self, newTime):
        total_seconds = newTime.total_seconds()
        h = int(total_seconds // 3600)
        m = int((total_seconds % 3600) // 60)
        s = int(total_seconds % 60)
        self.time = [h//10, h%10, m//10, m%10, s//10, s%10]

    def convertTime(self):
        # for converting the edit mode time back into a real time
        h = self.time[0] * 10 + self.time[1]
        m = self.time[2] * 10 + self.time[3]
        s = self.time[4] * 10 + self.time[5]
        newTime = timedelta(hours=h, minutes=m, seconds=s)
        return newTime
    
    def timeString(self):
        # s = "".join([str(i) for i in self.time])

        s0 = "".join([str(i) for i in self.time])
        return (" " * 4) + s0[:2] + ":" + s0[2:4] + ":" + s0[4:]
    
    def pointer(self):
        return (" " * 4) + " " * (self.editIndex + self.editIndex//2) + "^"

    def text(self, editing, running, looping):
        top = self.timeString()

        if editing:
            bottom = self.pointer()
        else:
            if running:
                bottomLeft = "PLAY    "
            else:
                bottomLeft = "PAUSE   "

            if looping:
                bottomRight = "    AUTO"
            else:
                bottomRight = "  MANUAL"

            bottom = bottomLeft + bottomRight
        
        return top + '\n' + bottom
    
    def zero(self):
        self.time = [0,0,0,0,0,0]

    def moveCursor(self, val):
        self.editIndex = (self.editIndex + val) % 6

    def increment(self, value):

        if self.editIndex == 0:
            self.time[0] = (self.time[0] + value) % 3
            if self.time[0] == 2 and self.time[1] > 3:
                self.time[1] = 3
        elif self.editIndex == 1 and self.time[0] == 2:
            self.time[1] = (self.time[1] + value) % 4
        elif self.editIndex == 2 or self.editIndex == 4:
            self.time[self.editIndex] = (self.time[self.editIndex] + value) % 6
        else:
            self.time[self.editIndex] = (self.time[self.editIndex] + value) % 10


class Clock():

    def __init__(self) -> None:
        self.editing = False
        self.running = False
        self.looping = True
        self.ended = False
        self.baseTime = timedelta(hours=0, minutes=0, seconds=0) # time the clock was last set to manually
        self.startTime = datetime.now() # time that play was last pressed

        self.lastMessage = ""

        self.display = Display()

    def elapsedTime(self): # time since play was last pressed
        currentTime = datetime.now()
        return currentTime - self.startTime

    def displayTime(self): # time to display on both control module and clock
        return (self.baseTime + datetime.now() - self.startTime)

    def loop(self):

        if self.looping:
            self.looping = False
        else:
            self.looping = True

    def pause(self):

        if self.ended:
            self.ended = False
            self.display = Display()
            self.updateDisplay()
            self.running = True
            self.startTime = datetime.now()
            return "RESTART"

        elif self.running:
            print("pausing")
            lcd.clear()
            lcd.message = "     PAUSE"
            self.running = False
            self.baseTime = self.displayTime()
            return "STOP"
        else:
            lcd.clear()
            print("resuming")
            lcd.message = "     RESUME"
            self.running = True
            self.startTime = datetime.now()
            return "START"
    
    def normalMode(self, input):
        if input == "S":
            return self.pause()
        elif input == "E":
            self.loop()
        else:
            # arrow inputs open time editing mode
            print("entering edit mode")
            self.editing = True
            if self.running:
                return self.pause()
            
    def updateDisplay(self):
        newMessage = self.display.text(self.editing, self.running, self.looping)
        if newMessage != self.lastMessage:
            lcd.clear()
            lcd.message = newMessage
            self.lastMessage = newMessage

    def end(self):
        self.baseTime = timedelta(hours=0, minutes=0, seconds=0)
        if self.looping:
            self.startTime = datetime.now() # time that play was last pressed
            print("RESTARTING")
            return "RESTART"
            
        else:
            self.running = False
            self.display.updateTime(timedelta(hours=24, minutes=0, seconds=0))
            self.ended = True
            print("ENDING")
            return "END"


    def editMode(self, input):
        
        if input == "S":
            print("leaving edit mode")
            self.editing = False
            self.baseTime = self.display.convertTime()
            s = [str(i) for i in self.display.time]
            j = ''.join(s)
            return j
        
        else:

            if input == "E":
                self.display.zero()
            elif input == "L":
                # index -1
                self.display.moveCursor(-1)
            elif input == "R":
                # index +1
                self.display.moveCursor(1)
            elif input == "U":
                # time +1
                self.display.increment(1)
            elif input == "D":
                # time -1
                self.display.increment(-1)
            else:
                print("unknown input!")
                return
        
    def run(self):
        self.updateDisplay()
        input = getInput()

        # check if time limit is reached
        if self.running:
            if self.displayTime().total_seconds() >= 86400:
                print("ending")
                return self.end()
            
            # if not, update display
            else:
                self.display.updateTime(self.displayTime())
        
        if input:
            if self.editing:
                return self.editMode(input)
            else:
                return self.normalMode(input)
            

'''
def getInput():
    if ser.in_waiting > 0:  # Check if there's data available to read
        data = ser.readline().decode('utf-8').strip()  # Read and decode the data
        # print(f"Received: {data}")
        return data
    time.sleep(0.1)
'''