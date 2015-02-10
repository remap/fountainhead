class FountainElement(object):
    def __init__(self, elementType = '', elementText = ''):
        self._isDualDialogue = False
        self._isCentered = False
        self._sceneNumber = None
        self._sectionDepth = 0
        
        self._elementType = elementType
        self._elementText = elementText
        
        return
        
    def description(self):
        textOutput = self._elementText
        typeOutput = self._elementType
        
        # Seems element can only have one of these attributes
        if (self._isCentered):
            typeOutput += ' (centered)'
        elif (self._isDualDialogue):
            typeOutput += ' (dual)'
        elif (self.__sectionDepth):
            typeOutput += (' (' + str(self._sectionDepth) + ')')
        
        ret = typeOutput + ": " + textOutput
        return ret