class ValueSelector:
    _callbackSelected = None
    _callbackAccepted = None
    
    def __init__(self, minValue, maxValue, default, callbackSelected = None, callbackAccepted = None):
        self._minValue = minValue
        self._maxValue = maxValue        
        self.setSelectedValue(default)
        self._acceptedValue = self._selectedValue
        self._callbackSelected = callbackSelected
        self._callbackAccepted = callbackAccepted
        
    def accept(self):
        self._acceptedValue = self._selectedValue
        if self._callbackAccepted != None:
            self._callbackAccepted()
            
    def getAccepted(self):
        return self._acceptedValue
    
    def getAcceptedName(self):
        return str(self._selectedValue)
     
    def getSelected(self):
        return self._selectedValue
    
    def getSelectedName(self):
        return str(self._selectedValue)
    
    def getPrev(self):
        self.setSelectedValue(self._selectedValue - 1)
        return self._selectedValue
    
    def getNext(self):
        self.setSelectedValue(self._selectedValue + 1)
        return self._selectedValue
    
    def setSelectedValue(self, value):
        self._selectedValue = min(self._maxValue, max(value, self._minValue))
        if self._callbackSelected != None:
            self._callbackSelected()
            
if __name__ == "__main__":
    value = ValueSelector(10, 30, 20)
    print(20, value.getSelected())
    value = ValueSelector(10, 30, 99)
    print(30, value.getSelected())
    value = ValueSelector(10, 30, 5)
    print(10, value.getSelected())
    value.getNext()
    print(11, value.getSelected())
    value.accept()
    value.getNext()
    print(12, value.getSelected())
    value.getNext()
    print(13, value.getSelected())
    print(13, value.getSelected())
    value.setSelectedValue(29)
    print(29, value.getSelected())
    value.getNext()
    print(30, value.getSelected())
    value.getNext()
    print(30, value.getSelected())
    