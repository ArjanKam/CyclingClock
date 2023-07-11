from pico_i2c_lcd import I2cLcd
from machine import I2C, Pin
import Config

LCD_WIDTH = 20
LCD_HEIGHT= 4

i2c = I2C(0, sda=Pin(Config.PIN_00), scl=Pin(Config.PIN_01), freq=400000)
I2C_ADDR = i2c.scan()[0]
print("LCD i2c address :", I2C_ADDR)
lcd = I2cLcd(i2c, I2C_ADDR, LCD_HEIGHT, LCD_WIDTH)
lcd.clear()
lcd.hide_cursor()

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
    lcd.putstr("Time  :      /")
    lcd.move_to(0, 1)
    lcd.putstr("Round :      /")
    lcd.move_to(0, 2)
    lcd.putstr("Color :      /")
    lcd.move_to(0, 3)
    lcd.putstr("Show  : ")

DOTS = (". ", " .", "||")
_currentData = None
def updateLCDSeconds(mode, value):
    global _currentData
    if mode == Config.PAUSE:
        data = DOTS[2]
    else:
        data = DOTS[value % 2]
        
    if _currentData == data:
        return
    _currentData = data
    lcd.move_to(18, 3)
    lcd.putstr(data)


_acceptRound = None
_selectRound = None
_acceptTime = None
_selectTime = None
_acceptColor = None
_selectColor = None
_mode = None
def updateLCD(acceptRound, selectRound, acceptTime, selectTime, acceptColor, selectColor, mode):
    global _mode, _acceptTime, _selectTime, _acceptRound, _selectRound, _acceptColor, _selectColor
    if _acceptTime != acceptTime:
        lcd.move_to(8, 0)
        lcd.putstr(f"{acceptTime:<5}")
        _acceptTime = acceptTime
        
    if _selectTime != selectTime:
        lcd.move_to(14, 0)
        lcd.putstr(f"{selectTime:>6}")
        _selectTime = selectTime
        
    if _acceptRound != acceptRound:
        lcd.move_to(8, 1)
        lcd.putstr(f"{acceptRound:<5}")
        _acceptRound = acceptRound
    
    if _selectRound != selectRound:
        lcd.move_to(14, 1)
        lcd.putstr(f"{selectRound:>6}")
        _selectRound = selectRound

    if _acceptColor != acceptColor:
        lcd.move_to(8, 2)
        lcd.putstr(f"{acceptColor:<5}")
        _acceptColor = acceptColor
    
    if _selectColor != selectColor:
        lcd.move_to(14, 2)
        lcd.putstr(f"{selectColor:>6}")
        _selectColor = selectColor
        
    if _mode != mode:
        lcd.move_to(8, 3)
        lcd.putstr(f"{mode:<9}")
        _mode = mode

if __name__ == "__main__":
    from utime import sleep
    
    welcomeLCD()
    sleep(1)
    initLCD()
    updateLCD(4, 90, 80, 99, "Wit", "Rood", "PAUZE")
    updateLCDSeconds(Config.PAUSE, 1)
    sleep(1)
    updateLCDSeconds(Config.TIME, 2)
    sleep(1)
    updateLCDSeconds(Config.TIME, 3)
    sleep(1)
    updateLCDSeconds(Config.TIME, 4)
    sleep(1)
    updateLCDSeconds(Config.TIME, 5)
    sleep(1)
    updateLCD(4, 90, 80, 99, "Wit", "Rood", "PAUZE")
    updateLCDSeconds(Config.PAUSE, 6)