import machine
from machine import I2C, Pin
from pico_i2c_lcd import I2cLcd
from utime import sleep
from IRQButton import IRQButton

from RoterySwitch import RoterySwitch
from ValueSelector import ValueSelector
from ListSelector import ListSelector

BUTTON_1 = 22
BUTTON_2 = 26
BUTTON_3 = 27
BUTTON_RED		= 21
BUTTON_WHITE		= 20
BUTTON_GREEN		= 19
BUTTON_BLUE		= 18
ENCODER_1A      = 14
ENCODER_1B      = 15
ENCODER_2A      = 12
ENCODER_2B      = 13
ENCODER_3A      = 10
ENCODER_3B      = 11

def infoColors():
    print(colors.getSelectedName(), colors.getAcceptedName())
def infoTime():
    print(time.getSelectedName(), time.getAcceptedName())
def infoRounds():
    print(rounds.getSelectedName(), rounds.getAcceptedName())

#init Colors
COLOR_WHITE = (255,255,255)
COLOR_RED   = (255,  0,  0)
COLOR_BLUE  = (  0,  0,255)
COLOR_GREEN = (  0,255,  0)
lst = (COLOR_WHITE, COLOR_RED, COLOR_BLUE, COLOR_GREEN)
names = ("Wit", "Rood", "Blauw", "Groen")
colors = ListSelector( lst, names, infoColors, infoColors )

time   = ValueSelector(0, 99, 90, infoTime, infoTime)
rounds = ValueSelector(0, 99, 3, infoRounds, infoRounds)

def pressRed():
    print("Red")
def pressWhite():
    print("White")
def pressGreen():
    print("Green")
def pressBlue():
    print("Blue")
    
buttonRed   = IRQButton(BUTTON_RED, pressRed)
buttonWhite = IRQButton(BUTTON_WHITE, pressWhite)
buttonGreen = IRQButton(BUTTON_GREEN, pressGreen)
buttonBlue  = IRQButton(BUTTON_BLUE, pressBlue)

colorChanger    = RoterySwitch(ENCODER_1A, ENCODER_1B, colors.getPrev, colors.getNext, BUTTON_1, colors.accept)
#timeChanger     = RoterySwitch(ENCODER_2A, ENCODER_2B, time.getPrev, time.getNext, BUTTON_2, time.accept)
#roundsChanger   = RoterySwitch(ENCODER_3A, ENCODER_3B, rounds.getPrev, rounds.getNext, BUTTON_3, rounds.accept)

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)
lcd.clear()

def showOnLcd(txt, clear = False):
    if clear:
        lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr(txt)
    
def updateDisplays():
    print(".", end="")
    showOnLcd("Time left: %d s" % value)
    None
    
# Define interrupt timer function
_modesPauze = False
_modesStart = True
_prev_time = utime.time()
def timer_callback(timer):
    global _prev_time
    time = utime.time()
    if _modesPauze or not _modesStart:
        _prev_time = time
        return
    dt = (time - _prev_time) // 60 # 
    if dt >= 1:
        _prev_time = time
        print(dt)
    
    updateDisplays()
    
timer = machine.Timer()
timer.init(period=1000, mode=machine.Timer.PERIODIC, callback=timer_callback)

# Main loop
while True:
    print(I2C_ADDR)
    machine.idle() # Delay to prevent excessive CPU usage
    

