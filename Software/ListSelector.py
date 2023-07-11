class ListSelector:
    _callbackSelected = None
    _callbackAccepted = None
    
    def __init__(self, itemsList, namesDict, callbackSelected = None, callbackAccepted = None):
        self._items = itemsList
        self._names = namesDict
        self._elements = len(self._items)
        self._selectedIndex = 0
        self._acceptedIndex = 0
        self._callbackSelected = callbackSelected
        self._callbackAccepted = callbackAccepted
        
    def accept(self):
        newValue = self._selectedIndex
        changed = newValue != self._acceptedIndex
        self._acceptedIndex = newValue
        if self._callbackAccepted != None and changed:
            self._callbackAccepted()
            
    def getAccepted(self):
        return self._items[self._acceptedIndex]
    
    def getAcceptedName(self):
        return self._names[self._acceptedIndex]
     
    def getSelected(self):
        return self._items[self._selectedIndex]
    
    def getSelectedName(self):
        return self._names[self._selectedIndex]
    
    def getPrev(self):
        self._selectedIndex = (self._selectedIndex - 1) % self._elements
        if self._callbackSelected != None:
            self._callbackSelected()
        return self.getSelected()
    
    def getNext(self):
        self._selectedIndex = (self._selectedIndex + 1) % self._elements
        if self._callbackSelected != None:
            self._callbackSelected()
        return self.getSelected()

if __name__ == "__main__":
    COLOR_WHITE = (255,255,255)
    COLOR_RED   = (255,  0,  0)
    COLOR_BLUE  = (  0,  0,255)
    lst = (COLOR_WHITE, COLOR_RED, COLOR_BLUE)
    names = ("Wit", "Rood", "Blauw")
    colors = ListSelector( lst, names )
    print("Wit", colors.getSelectedName())
    colors.getNext()
    print("Rood", colors.getSelectedName())
    colors.getNext()
    print("Blauw", colors.getSelectedName())
    colors.accept()
    colors.getNext()
    print("Wit", colors.getSelectedName())
    colors.getPrev()
    print("Blauw",colors.getSelectedName())
    colors.getPrev()
    print("Rood",colors.getSelectedName())
    colors.getPrev()
    print("Wit",colors.getSelectedName())
    print("Blauw",colors.getAcceptedName())
    