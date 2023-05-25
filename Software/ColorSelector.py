class ColorSelector:
    COLOR_WHITE = (255,255,255)
    COLOR_RED   = (255,  0,  0)
    COLOR_BLUE  = (  0,  0,255)

    colors = { COLOR_WHITE : "Wit"
             , COLOR_RED   : "Rood"
             , COLOR_BLUE  : "Blauw"
             }
    _colorSequence = (COLOR_WHITE, COLOR_RED, COLOR_BLUE)
    _selectedIndex = 0
    _acceptedColor = None
    
    def __init__(self):
        None
        
    def acceptColor(self):
        self._acceptedColor = self._colorSequence[self._selectedIndex]
    
    def getAcceptedColor(self):
        return self._acceptedColor
    
    def getAcceptedColorName(self):
        return self.colors[self._acceptedColor]
     
    def getSelectedColor(self):
        return self._colorSequence[self._selectedIndex]
    def getSelectedColorName(self):
        return self.colors[self._colorSequence[self._selectedIndex]]
    
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
