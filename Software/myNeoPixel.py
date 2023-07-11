from machine import Pin
import neopixel
from utime import sleep
import colorHelper

import matrixArt as art
import matrixBuffer
PIXEL_ON = colorHelper.COLOR_WHITE
PIXEL_OFF = colorHelper.COLOR_BLACK
PIN_DIN = 28

class myNeoPixel():
    _width = 32
    _height = 8
    _getIndex = None
    # myGetIndex is a overwritten method for calculation the index
    # from a given (x,y) position
    def __init__(self, width = 32, height = 8, myGetIndex = None):
        self._width = width
        self._height = height
        self._getIndex = myGetIndex
        self._np = neopixel.NeoPixel(Pin(PIN_DIN), width * height)   
    
    def getIndex(self, x, y):
        if self._getIndex is not None:
            return self._getIndex(self, x,y)
        if x % 2 == 1:
            return (x + 1) * self._height - 1 - y
        return x * self._height + y
    
    #check if the index in invalis
    def _isInvalidIndex(self, index):
        if index is None or index < 0 or index >= len(self._np):
           return True
        return False
            
    def getColor(self, color):
        if color == True:
            return PIXEL_ON
        if color == False:
            return PIXEL_OFF
        if type(color) == int:
            return colorHelper.getRGBfromInt(color)
        return color
    
    #pos (x,y) and color(r,g,b)
    def showPixel(self, pos, color):        
        index = self.getIndex(pos[0], pos[1])
        self._showPixel(index, color)
    
    def _showPixel(self, index, color, now = True):
        if self._isInvalidIndex(index):
            return
        self._np[index] = self.getColor(color)
        if now:
            self._np.write()
        
    #list of positions (x,y)
    def showPixels(self, lstOfPositions, color, oneByOne = False):
        color = colorHelper.getColor(color)
        for x,y in lstOfPositions:
            index = self.getIndex(x, y)
            self._showPixel(index, color, oneByOne)
        if not oneByOne:
            self._np.write()

    #color and position (x,y) in one matrix
    def showMatrix(self, matrix, color = None):
        for y, row in enumerate(matrix):
            if y >= self._height:
                continue
            for x, element in enumerate(row):
                if x >= self._width:
                    continue
                index = self.getIndex(x, y)
                if color != None and element != 0:
                    element = color
                self._showPixel(index, element, False)
        self._np.write()

    def clear(self, color = False):
        self.showPixels(self.leftRight(), self.getColor(color))

    #list of positions (x,y)
    def hLine(self, xb, yb, xe):
        m = []
        if xb <= xe:
            while xb <= xe:
                m.append((xb, yb))
                xb += 1
        else:
            while xe <= xb:
                m.append((xb, yb))
                xb -= 1
        return m
    
    #list of positions (x,y)
    def vLine(self, xb, yb, ye):
        m = []
        if yb <= ye:
            while yb <= ye:
                m.append((xb, yb))
                yb += 1
        else:
            while ye <= yb:
                m.append((xb, yb))
                yb -= 1
        return m

    #list of positions (x,y)
    def rect(self, xStart, yStart, width, height):
        if width == 0 or height == 0:
            return []
        xEnd = xStart + width  - 1
        yEnd = yStart + height - 1
        m  = self.hLine(xStart,   yStart,      xEnd)
        m += self.vLine(xEnd,     yStart + 1,  yEnd)
        m += self.hLine(xEnd - 1, yEnd,        xStart + 1)
        m += self.vLine(xStart,   yEnd,        yStart + 1)        
        return m
                
    def upDown(self):
        pixels = []
        for x in range(self._width):
            for y in range(self._height):
                pixels.append((x,y))
        return pixels

    def leftRight(self):
        pixels = []
        for y in range(self._height):
            for x in range(self._width):
                pixels.append((x,y))
        return pixels
        
    def closingBox(self, delay = 0.2):
        x = 0
        while x < self._height // 2:
            pos = self.rect(x,x,self._width-x-x,self._height-x-x)
            self.showPixels(pos, colorHelper.randomColor)
            sleep(delay)
            self.showPixels(pos, PIXEL_OFF)
            x += 1

    def openingBox(self, delay = 0.2):
        x = self._height // 2
        while x >= 0:
            pos = self.rect(x,x,self._width-x-x,self._height-x-x)
            self.showPixels(pos, colorHelper.randomColor)
            sleep(delay)
            self.showPixels(pos, PIXEL_OFF)
            x -= 1
            
    def outerLoopLights(self, color):
        pos = self.rect(0,0,self._width,self._height)
        repeat = 5
        while repeat >= 0:
            self.showPixels(pos, color, True )
            self.showPixels(pos, PIXEL_OFF, True)
            repeat -= 1
            
    def outerBlinkLights(self, color):
        pos = self.rect(0,0,self._width,self._height)
        repeat = 20
        while repeat >= 0:
            self.showPixels(pos, color)
            self.showPixels(pos, PIXEL_OFF)
            repeat -= 1

    #tuple with pos (x,y) and color
    def toColorPosition(self, pos, color):
        return (pos, colorHelper.getColor(color))
    
    #list of positions (x,y) with color
    def listToColorPositions(self, posLst, color ):
        matrixPos = []
        for p in posLst:
            matrixPos.append(self.toColorPosition(p, color))
        return matrixPos
    
if __name__ == "__main__":
    def myGetIndex(self, x, y):
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
    
    np = myNeoPixel(32,32, myGetIndex)
    if False:
        #show all one by one
        for y in range(32):
              for x in range(32):
                  np.showPixel([x,y], PIXEL_ON)
    
    import matrix_16x24 as matrix
    import matrixHelper
    for x in range(9, -1, -1):
        txt = str("123456789")
        listMatrix = matrixHelper.elementsToMatrix(txt, matrix.MATRIX)
        completeMatrix1 = matrixHelper.appendMatrixHorizontal(listMatrix, 2)
        completeMatrix1 = matrixHelper.alignHorizontal(completeMatrix1, 32, 1)
        completeMatrix1 = matrixHelper.alignVertical(completeMatrix1, 32, 1)
        print(txt)
        matrixHelper.changeColor(completeMatrix1, 1, colorHelper.COLOR_RED)
        #matrixHelper.printMatrix(completeMatrix1)
        for _ in range(32): #
             completeMatrix1 = matrixHelper.moveMatrix(completeMatrix1, -1, -1)   
             np.showMatrix(completeMatrix1)
        #completeMatrix1.clear()

    np.clear()
#     np.clear(False)
#     np.openingBox()
#     np.closingBox()
#     np.outerBlinkLights(colorHelper.COLOR_RED)
#     np.outerLoopLights(colorHelper.COLOR_RED)
    









