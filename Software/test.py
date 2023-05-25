import machine
from machine import Pin
import utime

from ColorSelector import ColorSelector
#see http://www.knutselaar.eu/WP/rotary-encoder/

color = ColorSelector()


# Pin definitions
BUTTON_ACCEPT_COLOR = Pin(2, Pin.IN, Pin.PULL_UP) # Blue

#encoder button time
ENCODER_1_A = Pin(0, Pin.IN, Pin.PULL_UP) # Red
ENCODER_1_B = Pin(1, Pin.IN, Pin.PULL_UP) # Orange
     
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

timeCounter = 90
def changeTime(pin):
    global timeCounter
    valueA = ENCODER_1_A.value()
    valueB = ENCODER_1_B.value()
    if valueA != valueB:
        timeCounter += 1
    else:
        timeCounter -= 1
    print(timeCounter)
    
def changeColor(pin):
    global counter
    valueA = ENCODER_1_A.value()
    valueB = ENCODER_1_B.value()
    if valueA != valueB:
        color.getNextColor()
    else:
        color.getPrevColor()
    print(counter, color.getSelectedColorName(), color.getAcceptedColorName())
    counter += 1
    
counter = 0
# Interrupt service routine for button presses
def selectColor(pin):
    global counter
    color.acceptColor()
    print(counter, color.getAcceptedColorName())
    counter += 1
    
    
# Attach interrupt handlers to buttons
BUTTON_ACCEPT_COLOR.irq(trigger=Pin.IRQ_FALLING, handler=selectColor)
ENCODER_1_A.irq(trigger=Pin.IRQ_FALLING, handler=changeTime)

# Main loop
while True:  
    machine.idle() # Delay to prevent excessive CPU usage
    

