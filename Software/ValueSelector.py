class ValueSelector:
    _callbackSelected = None
    _callbackAccepted = None
    _selectedValue = None
    _acceptedValue = None
    
    def __init__(self, minValue, maxValue, default, callbackSelected = None, callbackAccepted = None):
        self._minValue = minValue
        self._maxValue = maxValue        
        self.setSelected(default)
        self._acceptedValue = self._selectedValue
        self._callbackSelected = callbackSelected
        self._callbackAccepted = callbackAccepted
        
    def accept(self):
        changed = self._acceptedValue != self._selectedValue
        self._acceptedValue = self._selectedValue
        if self._callbackAccepted != None and changed:
            self._callbackAccepted()
            
    def getAccepted(self):
        return self._acceptedValue
    
    def getAcceptedName(self):
        return str(self._acceptedValue)
     
    def getSelected(self):
        return self._selectedValue
    
    def getSelectedName(self):
        return str(self._selectedValue)
    
    def getPrev(self):
        self.setSelected(self._selectedValue - 1)
        return self._selectedValue
    
    def getNext(self):
        self.setSelected(self._selectedValue + 1)
        return self._selectedValue
    
    def setSelected(self, value):
        newValue = min(self._maxValue, max(value, self._minValue))
        changed = self._selectedValue != newValue
        self._selectedValue = newValue
        if self._callbackSelected != None and changed:
            self._callbackSelected()
    
    def setAccepted(self, value):
        newValue = min(self._maxValue, max(value, self._minValue))
        changed = self._acceptedValue != newValue
        self._acceptedValue = newValue
        if self._callbackAccepted != None and changed:
            self._callbackAccepted()
            
if __name__ == "__main__":
    print("ValueSelector : Begin tests")
    value = ValueSelector(10, 30, 20)
    assert 20 == value.getSelected()
    value = ValueSelector(10, 30, 99)
    assert 30 == value.getSelected()
    value = ValueSelector(10, 30, 5)
    assert 10 == value.getSelected()
    value.getNext()
    assert 11 == value.getSelected()
    value.accept()
    value.getNext()
    assert 12 == value.getSelected()
    value.getNext()
    assert 13 == value.getSelected()
    value.setSelected(29)
    assert 29 == value.getSelected()
    value.getNext()
    assert 30 == value.getSelected()
    value.getNext()
    assert 30 == value.getSelected()
    value.setAccepted(25)
    assert 25 == value.getAccepted()
    print("ValueSelector : All tests OK")
    