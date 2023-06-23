import machine
import sys
sys.path.append('../Libraries/General')
sys.path.append('../Libraries/Buttons')

from machine import Pin
from utime import sleep
import utime
from IRQButton import IRQButton
import Config
import LCDDisplay
import MatrixBoard

from RoterySwitch import RoterySwitch
from ValueSelector import ValueSelector
from ListSelector import ListSelector

#../Libraries/General
import colorHelper

TIME_INTERVAL = 60 #should be 60
CLOCK_UPDATE_INTERVAL = 1000

def infoColorSelector():
    updateDisplays()
def infoTime():
    updateDisplays()
def infoRounds():
    updateDisplays()


#init colorSelector
COLOR_WHITE = (50, 50,  50)
COLOR_RED   = (100,  0,  0)
COLOR_BLUE  = (  0,  0,100)
COLOR_GREEN = (  0,100,  0)
lst = (COLOR_RED, COLOR_BLUE, COLOR_GREEN, COLOR_WHITE)
names = ("Rood", "Blauw", "Groen", "Wit")
colorSelector = ListSelector( lst, names, infoColorSelector, infoColorSelector )

timeSelector   = ValueSelector(0, 99, 80, infoTime, infoTime)
roundsSelector = ValueSelector(0, 99, 3, infoRounds, infoRounds)

buzzer = Pin(Config.PIN_16, Pin.OUT)

def pressRed():
    while buttonRed.value() == 0:
        sleep(0.3)
    roundsSelector.setAccepted(roundsSelector.getSelected() )

def pressGreen():
    while buttonGreen.value() == 0:
        sleep(0.3)
    roundsSelector.setAccepted(roundsSelector.getAccepted() - 1 )
    
def pressBlue():
    beep(3)

def pressTimeRound(data):
    print(f"pressTimeRound({data})")
    setCurrentMode()
    updateDisplays()
    
def beep(numberOfBeeps = 1, timeInSeconds = 1):
    while numberOfBeeps > 0:
        sleep(timeInSeconds)
        buzzer.high()
        sleep(timeInSeconds)
        buzzer.low()
        numberOfBeeps -= 1
        
buttonTime  = IRQButton(Config.PIN_26,  pressTimeRound, 1, notifyAllChanges = True)
buttonRound = IRQButton(Config.PIN_27, pressTimeRound, 2, notifyAllChanges = True)

buttonRed   = IRQButton(Config.PIN_04, pressRed)
buttonGreen = IRQButton(Config.PIN_03, pressGreen)
buttonBlue  = IRQButton(Config.PIN_02, pressBlue)

timeChanger     = RoterySwitch(Config.PIN_06, Config.PIN_07, timeSelector.getPrev, timeSelector.getNext, Config.PIN_05, timeSelector.accept)
roundsChanger   = RoterySwitch(Config.PIN_09, Config.PIN_10, roundsSelector.getPrev, roundsSelector.getNext, Config.PIN_08, roundsSelector.accept)
colorChanger    = RoterySwitch(Config.PIN_12, Config.PIN_13, colorSelector.getPrev, colorSelector.getNext, Config.PIN_11, colorSelector.accept)

_currentMode = Config.PAUSE
def setCurrentMode():
    global _currentMode
    roundSelected = buttonRound.value() == 0
    timeSelected = buttonTime.value() == 0
    if timeSelected:
        _currentMode = Config.ROUND
    elif roundSelected:
        _currentMode = Config.TIME
    else:
        _currentMode = Config.PAUSE

def updateDisplays():
    txtMode = Config.MODEDICT[_currentMode]
    acceptedRound = roundsSelector.getAccepted()
    selectedRound = roundsSelector.getSelected()
    acceptedTime  = timeSelector.getAccepted()
    selectedTime  = timeSelector.getSelected()
    acceptedColor = colorSelector.getAcceptedName()
    selectedColor = colorSelector.getSelectedName()
    LCDDisplay.updateLCD(acceptedRound, selectedRound, acceptedTime, selectedTime, acceptedColor, selectedColor, txtMode )
    
    color = colorSelector.getAccepted()
    txt = ""
    if _currentMode == Config.TIME:
        txt = timeSelector.getAcceptedName()
    elif _currentMode == Config.ROUND:
        txt = roundsSelector.getAcceptedName()
    MatrixBoard.updateMatrix(_currentMode, color, txt)

# Define interrupt timer function
_prevTime    = utime.time()
_currentTime = utime.time()
def timer_callback(timer):
    global _prevTime, _currentTime, _currentMode
    _currentTime = utime.time()
    LCDDisplay.updateLCDSeconds(_currentMode, _currentTime)
    if _currentMode == Config.PAUSE:
        _prevTime = _currentTime
        return
    
    dt = (_currentTime - _prevTime) // TIME_INTERVAL # There can be a slight difference because we reset the time every time
    if dt == 0:
        return
    _prevTime = _currentTime
    newValue = timeSelector.getAccepted() - dt
    timeSelector.setAccepted(newValue)

def startDisplays():
    LCDDisplay.welcomeLCD()
    MatrixBoard.welcomeNeoPixels()
    LCDDisplay.initLCD()
    setCurrentMode()
    updateDisplays()
startDisplays()

timer = machine.Timer()
timer.init(period=CLOCK_UPDATE_INTERVAL, mode=machine.Timer.PERIODIC, callback=timer_callback)
# Main loop
while True:
    machine.idle() # Delay to prevent excessive CPU usage
    


