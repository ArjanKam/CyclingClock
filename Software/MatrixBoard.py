import matrix_16x24 as matrix
import matrixHelper
import matrixArt
import Config

#../Libraries/NeoPixel
from myNeoPixel import myNeoPixel

_currentMode = None
_currentTxt = None
_currentColor = None
def updateMatrix(mode, color, value):
    print(f"updateMatrix({mode}, {color}, {value})")
    global _currentMode, _currentTxt, _currentColor
    if _currentMode == mode and mode in {Config.PAUSE, Config.EXIT}:
        return
    
    if mode == Config.PAUSE:       
        np.showMatrix(matrixArt.PAUSE_32x32, 65280)
        _currentMode = Config.PAUSE
        return
    elif mode == Config.EXIT:             
        np.showMatrix(matrixArt.EXIT_32x32, color)
        _currentMode = Config.EXIT
        return
    
    txt = str(value)
    if _currentTxt == txt and _currentColor == color and _currentMode == mode:
        return
    _currentTxt = txt
    _currentColor = color
    _currentMode = mode
    listMatrix = matrixHelper.elementsToMatrix(txt, matrix.MATRIX)
    completeMatrix1 = matrixHelper.appendMatrixHorizontal(listMatrix, 2)
    completeMatrix1 = matrixHelper.alignHorizontal(completeMatrix1, 32, 1)
    completeMatrix1 = matrixHelper.alignVertical(completeMatrix1, 32, 1)
    np.showMatrix(completeMatrix1, color)
    
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
