import random

COLOR_BLACK = (0, 0, 0)
COLOR_RED = (100, 0, 0)
COLOR_BLUE = (0, 0, 100)
COLOR_GREEN = (0, 100, 0)
COLOR_BROWN = (160, 82, 45)
COLOR_YELLOW = (255, 255, 0)
COLOR_ORANGE = (255, 165, 0)
COLOR_WHITE = (255, 255, 255)

COLORS = (COLOR_WHITE, COLOR_RED, COLOR_BLUE, COLOR_GREEN, COLOR_BROWN, COLOR_YELLOW, COLOR_ORANGE, COLOR_BLACK)


def randomColor(maxColor=255):
    return (random.randint(0, maxColor),
            random.randint(0, maxColor),
            random.randint(0, maxColor))


def text2Color(textString):
    textString = textString.replace("(", "")
    textString = textString.replace(")", "")
    textString = textString.strip()
    color = []
    for x in textString.split(","):
        color.append(int(x))
    return tuple(color)


def getRGBfromInt(RGBint):
    blue = RGBint & 255
    green = (RGBint >> 8) & 255
    red = (RGBint >> 16) & 255
    return red, green, blue


def getIntFromRGB(rgb):
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]
    rgb = (red << 16) + (green << 8) + blue
    return rgb


# determine if color is a function or direct color
def getColor(color):
    if callable(color):
        return color()
    else:
        return color

class ColorSelector:
    _colorNames = { COLOR_WHITE : "Wit"
             , COLOR_RED   : "Rood"
             , COLOR_BLUE  : "Blauw"                  
             , COLOR_GREEN : "Groen"
             , COLOR_BROWN : "Bruin"
             , COLOR_YELLOW :"Geel"
             , COLOR_ORANGE : "Oranje"
             }
    _colorSequence = (COLOR_WHITE, COLOR_RED, COLOR_BLUE, COLOR_GREEN, COLOR_BROWN, COLOR_YELLOW, COLOR_ORANGE)
    _selectedIndex = 1
    _acceptedColor = None
    
    def __init__(self):
        self.acceptColor()
        
    def acceptColor(self):
        self._acceptedColor = self._colorSequence[self._selectedIndex]
    
    def getAcceptedColor(self):
        return self._acceptedColor
    
    def getAcceptedColorName(self):
        return self._colorNames[self._acceptedColor]
     
    def getSelectedColor(self):
        return self._colorSequence[self._selectedIndex]
    def getSelectedColorName(self):
        return self._colorNames[self._colorSequence[self._selectedIndex]]
    
    def getPrevColor(self):
        self._selectedIndex -= 1
        if self._selectedIndex < 0:
            self._selectedIndex = len(self._colorSequence) - 1
        return self.getSelectedColor()
    
    def getNextColor(self):
        self._selectedIndex += 1
        if self._selectedIndex >= len(self._colorSequence):
            self._selectedIndex = 0
        return self.getSelectedColor()


if "__main__" == __name__:
    assert len(randomColor()) == 3, "RBG color"
    assert getRGBfromInt(123) == (0, 0, 123), "Some kind of blue"
    assert getIntFromRGB((0, 0, 123)) == 123, "Some kind of blue"
    assert text2Color("(234,18,98)") == (234, 18, 98)

