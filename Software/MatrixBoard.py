import sys
sys.path.append('../Libraries/NeoPixel')
sys.path.append('../Libraries/General')
from machine import Pin
import matrix_16x24 as matrix
import matrixHelper
import matrixArt
import Config

#../Libraries/NeoPixel
from myNeoPixel import myNeoPixel

_currentMode = None
_currentTxt = None
def updateMatrix(mode, color, value):
    #print(f"updateMatrix({mode}, {color}, {value})")
    global _currentMode, _currentTxt
    if _currentMode == mode and mode == Config.PAUSE:
        return
    
    if mode == Config.PAUSE:
        matrixPause = matrixHelper.tuple2Matrix(matrixArt.PAUSE_32x32)        
        matrixHelper.lowerColorIntensity(matrixPause, 0.2)
        np.showMatrix(matrixPause)
        _currentMode = Config.PAUSE
        return
    
    txt = str(value)
    if _currentTxt == txt:
        return
    _currentTxt = txt
    listMatrix = matrixHelper.elementsToMatrix(txt, matrix.MATRIX)
    completeMatrix1 = matrixHelper.appendMatrixHorizontal(listMatrix, 2)
    completeMatrix1 = matrixHelper.alignHorizontal(completeMatrix1, 32, 1)
    completeMatrix1 = matrixHelper.alignVertical(completeMatrix1, 32, 1)
    matrixHelper.changeColor(completeMatrix1, 1, color)
    np.showMatrix(completeMatrix1)
    
def welcomeNeoPixels():
    np.openingBox(0.03)
    
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

if __name__ == "__main__":
    welcomeNeoPixels()
    updateMatrix(Config.PAUSE, (50, 50,  50), 99)
    updateMatrix(Config.TIME, (50, 50,  50), 99)
    updateMatrix(Config.ROUND, (50, 50,  50), 5)
    updateMatrix(Config.ROUND, (50, 50,  50), 5)