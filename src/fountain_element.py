# -*- Mode:python c-file-style:"gnu" indent-tabs-mode:nil -*- */
#
# Copyright (C) 2014-2015 Regents of the University of California.
# Author: Zhehao Wang <wangzhehao410305gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# A copy of the GNU General Public License is in the file COPYING.

# This class contains the elements parsed from string input

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