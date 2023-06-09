import machine
import sys
sys.path.append('../Libraries/NeoPixel')
sys.path.append('../Libraries/General')
sys.path.append('../Libraries/LCD')
sys.path.append('../Libraries/Buttons')

from machine import I2C, Pin
from pico_i2c_lcd import I2cLcd
from utime import sleep
import utime
from IRQButton import IRQButton

from RoterySwitch import RoterySwitch
from ValueSelector import ValueSelector
from ListSelector import ListSelector

#../Libraries/General
import colorHelper
import matrix_16x24 as matrix
import matrixHelper
import matrixArt

#../Libraries/NeoPixel
from myNeoPixel import myNeoPixel

TIME_INTERVAL = 10 #should be 60
CLOCK_UPDATE_INTERVAL = 1000
LCD_WIDTH = 20

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

def infoColorSelector():
    updateDisplays()
def infoTime():
    updateDisplays()
def infoRounds():
    updateDisplays()


#init colorSelector
COLOR_WHITE = (50, 50,  50)
COLOR_RED   = (150,  0,  0)
COLOR_BLUE  = (  0,  0,150)
COLOR_GREEN = (  0,150,  0)
lst = (COLOR_RED, COLOR_BLUE, COLOR_GREEN, COLOR_WHITE)
names = ("Rood", "Blauw", "Groen", "Wit")
colorSelector = ListSelector( lst, names, infoColorSelector, infoColorSelector )

timeSelector   = ValueSelector(0, 99, 90, infoTime, infoTime)
roundsSelector = ValueSelector(0, 99, 3, infoRounds, infoRounds)

def pressRed():
    global _currentMode
    roundsSelector.setAccepted(roundsSelector.getSelected())
    if _currentMode == TIME:
        _currentMode = PAUSE
        updateLCDSeconds()
    elif _currentMode == ROUND:
        _currentMode = TIME
    else:
        _currentMode = TIME
    updateDisplays()
    
def pressWhite():
    global _currentMode
    if _currentMode == TIME or _currentMode == PAUSE:
        _currentMode = ROUND
    elif _currentMode == ROUND:
        roundsSelector.setAccepted(roundsSelector.getAccepted() - 1)
    updateDisplays()
    
def pressGreen():
    print("Green, not implemented yet")
def pressBlue():
    print("Blue, not implemented yet")
    
buttonRed   = IRQButton(BUTTON_RED, pressRed)
buttonWhite = IRQButton(BUTTON_WHITE, pressWhite)
buttonGreen = IRQButton(BUTTON_GREEN, pressGreen)
buttonBlue  = IRQButton(BUTTON_BLUE, pressBlue)

colorChanger    = RoterySwitch(ENCODER_1A, ENCODER_1B, colorSelector.getPrev, colorSelector.getNext, BUTTON_1, colorSelector.accept)
#timeChanger     = RoterySwitch(ENCODER_2A, ENCODER_2B, time.getPrev, time.getNext, BUTTON_2, time.accept)
#roundsChanger   = RoterySwitch(ENCODER_3A, ENCODER_3B, rounds.getPrev, rounds.getNext, BUTTON_3, rounds.accept)

PAUSE = 0
TIME = 1
ROUND = 2
_modeDict = {PAUSE: "Pauze",
             TIME: "Time",
             ROUND: "Round"
             }

_currentMode = PAUSE

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
I2C_ADDR = i2c.scan()[0]
print("LCD i2c address :", I2C_ADDR)
lcd = I2cLcd(i2c, I2C_ADDR, 4, LCD_WIDTH)
lcd.clear()
lcd.hide_cursor()

def updateDisplays():
    updateLCD()
    updateMatrix()

def updateMatrix():
    if _currentMode == PAUSE:
        matrixPause = matrixHelper.tuple2Matrix(matrixArt.PAUSE_32x32)        
        matrixHelper.lowerColorIntensity(matrixPause, 0.2)
        np.showMatrix(matrixPause)
        return
    
    if _currentMode == TIME:
        txt = timeSelector.getAcceptedName()
    elif _currentMode == ROUND:
        txt = roundsSelector.getAcceptedName()
    else:          
        txt = ""
        
    listMatrix = matrixHelper.elementsToMatrix(txt, matrix.MATRIX)
    completeMatrix1 = matrixHelper.appendMatrixHorizontal(listMatrix, 2)
    completeMatrix1 = matrixHelper.alignHorizontal(completeMatrix1, 32, 1)
    completeMatrix1 = matrixHelper.alignVertical(completeMatrix1, 32, 1)
    matrixHelper.changeColor(completeMatrix1, 1, colorSelector.getAccepted())
    np.showMatrix(completeMatrix1)
    
def welcomeNeoPixels():
    np.openingBox()
    
def welcomeLCD():
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr("DRC de Mol".center(LCD_WIDTH))
    lcd.move_to(0, 1)
    lcd.putstr("Cycling clock".center(LCD_WIDTH))
    lcd.move_to(0, 2)
    lcd.putstr("(c) 2023".center(LCD_WIDTH))
    lcd.move_to(0, 3)
    lcd.putstr("Arjan Kamberg".center(LCD_WIDTH))
    
def initLCD():
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr(f"Time  : ")
    lcd.move_to(0, 1)
    lcd.putstr(f"Round : ")
    lcd.move_to(0, 2)
    lcd.putstr(f"Color : ")
    lcd.move_to(0, 3)
    lcd.putstr(f"Show  : ")
    
def updateLCD():
    lcd.move_to(8, 0)
    lcd.putstr(f"{timeSelector.getAccepted():<5}/{timeSelector.getSelected():>6}")
    lcd.move_to(8, 1)
    lcd.putstr(f"{roundsSelector.getAccepted():<5}/{roundsSelector.getSelected():>6}")
    lcd.move_to(8, 2)
    lcd.putstr(f"{colorSelector.getAcceptedName():<5}/{colorSelector.getSelectedName():>6}")
    lcd.move_to(8, 3)
    lcd.putstr(f"{_modeDict[_currentMode]:<9}")
    
def updateLCDSeconds():
    lcd.move_to(18, 3)
    if _currentMode == PAUSE:
        lcd.putstr("  ")
    elif _currentTime % 2 == 0:
        lcd.putstr(". ")
    else:
        lcd.putstr(" .")
    
def neoPixel32x32Indexer(self, x, y):
    if y < 8:
        if (x % 2 == 1): #oneven
            return 255 - (x * 8) - y
        return 255 - ((x + 1) * 8)  + 1 + y
    if y < 16:
        return 256 + self.getIndex(x, y-8)
    if y < 24:
        return 512 + self.getIndex(x, y-16)
    #inv: y >= 24
    return 768 + self.getIndex(x, y-24)

np = myNeoPixel(32,32, neoPixel32x32Indexer)

# Define interrupt timer function
_prevTime    = utime.time()
_currentTime = utime.time()
def timer_callback(timer):
    global _prevTime, _currentTime, _currentMode
    _currentTime = utime.time()
    if _currentMode == PAUSE:
        _prevTime = _currentTime
        return
    dt = (_currentTime - _prevTime) // TIME_INTERVAL # There can be a slight difference because we reset the time every time
    if dt >= 1:
        _prevTime = _currentTime
        newValue = timeSelector.getAccepted() - dt
        timeSelector.setAccepted(newValue)
        print()
        
    if _currentMode == TIME and timeSelector.getAccepted() == 0:
        _currentMode = PAUSE
    
    updateLCDSeconds()
    
timer = machine.Timer()
timer.init(period=CLOCK_UPDATE_INTERVAL, mode=machine.Timer.PERIODIC, callback=timer_callback)

welcomeLCD()
welcomeNeoPixels()

initLCD()
updateDisplays()
# Main loop
while True:
    machine.idle() # Delay to prevent excessive CPU usage
    

