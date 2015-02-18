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

# This module defines the paginator, which takes a Script and produces a list of pages

import re
import sys

from fountain_parser import ParserVersion
from regex_rules import *

class Paginator:
    def __init__(self, script):
        self._pages = []
        self._script = script
        return
        
    def paginate(self):
        # default US letter size in pixels:  612, 792
        # paginateForSize(pageSize)
        return
        
    # paginateForSize takes two dimension size
    def paginateForSize(pageSize):
        return
    
    def numberOfPages():
        return len(self._pages)
    
    def pageAtIndex(index):
        return
        
    # Helper class methods
    @classmethod
    def widthForElement():
        return
    
    @classmethod
    def heightForString():
        return
        
    @classmethod
    def leftMarginForElement():
        return
        
    @classmethod
    def spaceBeforeForElement():
        return
        
    