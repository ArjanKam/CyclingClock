import machine
from machine import Pin
import utime

#see http://www.knutselaar.eu/WP/rotary-encoder/
COLOR_WHITE = (255,255,255)
COLOR_RED   = (255,  0,  0)
COLOR_BLUE  = (  0,  0,255)

# Pin definitions for LCD display
LCD_RS = Pin(16, Pin.OUT) #4
LCD_E  = Pin(17, Pin.OUT) #5
LCD_D4 = Pin(18, Pin.OUT)
LCD_D5 = Pin(19, Pin.OUT)
LCD_D6 = Pin(21, Pin.OUT)
LCD_D7 = Pin(22, Pin.OUT)

# Pin definitions
BUTTON_PAUZE = Pin(2, Pin.IN, Pin.PULL_UP) # Start / Pauze
BUTTON_2     = Pin(3, Pin.IN, Pin.PULL_UP) # DOWN
BUTTON_3     = Pin(4, Pin.IN, Pin.PULL_UP) # WHITE
BUTTON_4     = Pin(5, Pin.IN, Pin.PULL_UP) # RED
BUTTON_5     = Pin(6, Pin.IN, Pin.PULL_UP) # GREEN

SWITCH_SHOW  = Pin(11, Pin.IN, Pin.PULL_DOWN) # SHOW TIME OR ROUNDS
SWITCH_START = Pin(12, Pin.IN, Pin.PULL_DOWN) # START / STOP TIME

#encoder button time
ENCODER_1_A = Pin(7, Pin.IN, Pin.PULL_DOWN) # Time
ENCODER_1_B = Pin(8, Pin.IN, Pin.PULL_DOWN) 

#encoder button rounds
ENCODER_2_A = Pin(9,  Pin.IN, Pin.PULL_DOWN) # Rounds
ENCODER_2_B = Pin(10, Pin.IN, Pin.PULL_DOWN)

VALUE = 1
PIN2 = 2
MIN_VALUE = 3
MAX_VALUE = 4
SET_VALUE = 5

ENCODER_1 = 1
ENCODER_2 = 2

_modesPauze = False
def changeModePauze():
    if not _modesStart:
        return
    global _modesPauze
    _modesPauze = not _modesPauze
    updateDisplays()

_modesStart = False
def toggleStartStop():
    global _modesStart, _modesPauze
    _modesPauze = False
    _modesStart = not _modesStart
    if _modesStart:
        global start_time
        start_time = uTime.time()
    encoderPin[ENCODER_1_A][VALUE] = encoderPin[ENCODER_1_A][SET_VALUE]
    encoderPin[ENCODER_2_A][VALUE] = encoderPin[ENCODER_1_A][SET_VALUE]
    
    updateDisplays()
    
def decreaseRound():
    value = encoderPin[ENCODER_2_A][VALUE]
    minValue = encoderPin[ENCODER_2_A][MIN_VALUE]
    if value <= minValue:
        value = minValue
    else:
        value -= 1
    encoderPin[ENCODER_2_A][VALUE] = value
    updateDisplays()

displayColor = COLOR_WHITE
def setColorWhite():
    global displayColor
    displayColor = COLOR_WHITE
    updateDisplays()
    
def setColorRed():
    global displayColor
    displayColor = COLOR_RED
    updateDisplays()
    
def setColorBlue():
    global displayColor
    displayColor = COLOR_BLUE
    updateDisplays()
    
displayTime = True
def setToggleShow():
    global displayTime
    displayTime = not displayTime
    updateDisplays()
    
# Function to read encoder position and direction
def read_encoder(pin1):
    pin2 = encoderPin[pin1][PIN2]
    value = encoderPin[pin1][VALUE]
    #check the values of pinA and B 
    if pin1.value() != pin2.value():
        value += 1
    else:
        value -= 1
    
    encoderPin[pin1][VALUE] = max(encoderPin[pin1][MIN_VALUE], min(encoderPin[pin1][MAX_VALUE], value))
    encoderPin[pin1][SET_VALUE] = encoderPin[pin1][VALUE]
    
    updateDisplays()
    
# Interrupt service routine for button presses
def button_isr(pin):
    print(pin)
    #buttonAction[pin]()

encoderPin = { ENCODER_1:  {PIN2      : ENCODER_1_B,
                              VALUE     : 90,
                              SET_VALUE : 90,                             
                              MIN_VALUE : 0,
                              MAX_VALUE : 99},
               ENCODER_2:  {PIN2      : ENCODER_2_B,
                              VALUE     : 3,
                              SET_VALUE : 3,
                              MIN_VALUE : 0,
                              MAX_VALUE : 99}
             }

buttons = (BUTTON_PAUZE, BUTTON_2, BUTTON_3, BUTTON_4, BUTTON_5, SWITCH_SHOW, SWITCH_START)
buttonAction = (changeModePauze,decreaseRound,setColorWhite,setColorRed,setColorBlue,toggleStartStop)

# Attach interrupt handlers to buttons
BUTTON_PAUZE.irq(trigger=Pin.IRQ_FALLING, handler=button_isr)
BUTTON_2.irq(trigger=Pin.IRQ_FALLING, handler=button_isr)
BUTTON_3.irq(trigger=Pin.IRQ_FALLING, handler=button_isr)
BUTTON_4.irq(trigger=Pin.IRQ_FALLING, handler=button_isr)
BUTTON_5.irq(trigger=Pin.IRQ_FALLING, handler=button_isr)

ENCODER_1_A.irq(trigger=Pin.IRQ_FALLING, handler=read_encoder)
ENCODER_2_A.irq(trigger=Pin.IRQ_FALLING, handler=read_encoder)

lcd = machine.hd44780(HD44780_LCD_WIDTH, HD44780_LCD_HEIGHT, LCD_RS, LCD_E, LCD_D4, LCD_D5, LCD_D6, LCD_D7)
lcd.clear()
def showOnLcd(txt, clear = False):
    if clear:
        lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr(txt)
    
def updateDisplays():
    if displayTime:
        None
    value = encoderPin[ENCODER_1_A][VALUE]
    showOnLcd("Time left: %d s" % value)
        
# Define interrupt timer function
_prev_time = uTime.time()
def timer_callback(timer):
    global _prev_time
    time = uTime.time()
    if _modesPauze or not _modesStart:
        _prev_time = time
        return
    dt = (time - prev_time) // 60 # 
    if dt >= 1:
        _prev_time = time
        encoderPin[ENCODER_1_A][VALUE] -= dt
    
    updateDisplays()
    

# Create an interrupt timer to update the countdown time every second
timer = machine.Timer(0)
timer.init(period=1000, mode=machine.Timer.PERIODIC, callback=timer_callback)

# Main loop
while True:  
    machine.idle() # Delay to prevent excessive CPU usage
    