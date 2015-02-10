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

# This module defines the HTML generator class for parsed fountain scripts.
# Ported to Python from objc in nyousefi/Fountain repository

# For HTML output, paginator is ignored right now.

class FountainHTMLGenerator(object):
    def __init__(self, script = '', cssFile = ''):
        self._script = script
        self._bodyText = ''
        self._cssFile = cssFile
        return
    
    def generateHtml(self):
        if (self._bodyText == ''):
            self._bodyText = self.bodyForScript()
        html = '<!DOCTYPE html>\n' + 
               '<html>\n' +
               '<head>\n'
        if (self._cssFile != ''):
            html += '<link rel=\"stylesheet\" type=\"text/css\" href=\"' + 
                    self._cssFile + 
                    '\">\n'
        html += '</head>\n' +
                '<body>\n' + 
                self._bodyText +
                '</body>\n' +
                '</html>\n'
        return html
    
    def bodyForScript(self):
        # add title page
        