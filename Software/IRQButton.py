from machine import Pin
from utime import sleep

class IRQButton():
    def __init__(self, pin, callbackPressed = None, pull = Pin.PULL_UP, debug = False):
        self._pin = Pin(pin,   Pin.IN, pull)
        self._callbackPressed = callbackPressed
        self._debug = debug
        if callbackPressed != None:
            self._pin.irq(trigger=Pin.IRQ_FALLING, handler=self._handler)
    
    def _handler(self, pin):
        self._pin.irq(handler=None)
        self._callbackPressed()
        sleep(0.3)
        if self._debug:
            print("Pressed", self._pinPressed.value())
        self._pin.irq(handler=self._handler)
    
if __name__ == "__main__":
    def pressed():
        print("Pressed")
    btn = IRQButton(21, pressed)
