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

# This module defines the script class, which takes a file name, and constructs
# elements structure by calling the parser.
# Ported to Python from objc in nyousefi/Fountain repository

from fountain_parser import Parser

class FountainScript(object):
    def __init__(self, fileName = ''):
        if (fileName == ''):
            return
        self._fileName = fileName
        
        # This parser is not optimized
        parser = Parser()
        self._elements = parser.parseBodyOfFile(self._fileName)
        self._titlePageContents = parser.parseTitlePageOfFile(self._fileName)
        
        return
        