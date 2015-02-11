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

# TODO: add version parsing before importing FountainRegex;
import re
from fountain_parser import ParserVersion
from regex_rules import *

class FountainHTMLGenerator(object):
    def __init__(self, script, cssFile = '', version = ParserVersion.DEFAULT):
        self._script = script
        self._bodyText = ''
        self._cssFile = cssFile
        
        self._version = version
        if self._version == ParserVersion.REMAP:
            self.FountainRegex = FountainRegexRemap()
            self.generateHtml = self.generateHtmlRemap
        elif self._version == ParserVersion.BASE:
            self.FountainRegex = FountainRegexBase()
            self.generateHtml = self.generateHtmlBase
        else:
            # Right now using remap as default
            self._version == ParserVersion.DEFAULT
            self.FountainRegex = FountainRegexRemap()
            self.generateHtml = self.generateHtmlRemap
        return
    
    # HTML class is elementType with spaces replaced by dashes
    def htmlClassForType(self, elementType):
        return re.sub(" ", "-", elementType.lower())
    
    def generateHtmlBase(self):
        if (self._bodyText == ''):
            self._bodyText = self.bodyForScriptBase()
        html = '<!DOCTYPE html>\n<html>\n<head>\n'
        if (self._cssFile != ''):
            html += '<link rel=\"stylesheet\" type=\"text/css\" href=\"' + self._cssFile + '\">\n'
        # Note: here a <section> tag is added by default.
        html += '</head>\n<body>\n<section>\n' + self._bodyText + '</section>\n</body>\n</html>\n'
        return html
    
    def generateHtmlRemap(self):
        if (self._bodyText == ''):
            self._bodyText = self.bodyForScriptRemap()
        html = '<!DOCTYPE html>\n<html>\n<head>\n'
        if (self._cssFile != ''):
            html += '<link rel=\"stylesheet\" type=\"text/css\" href=\"' + self._cssFile + '\">\n'
        # Note: here a <section> tag is added by default.
        html += '</head>\n<body>\n<section>\n' + self._bodyText + '</section>\n</body>\n</html>\n'
        return html
    
    def bodyForScriptRemap(self):
        bodyText = ''
        # add title page
        titleElements = self._script._titlePageContents
        
        if titleElements:
            bodyText += '<div id=\'' + self.FountainRegex.TITLE_DIV + '\'>'
            
            # Titles
            bodyText += '<p class=\'' + self.FountainRegex.TITLE_TITLE_CLASS + '\'>'
            if titleElements[self.FountainRegex.TITLE_TITLE_STRING]:
                for temp in titleElements[self.FountainRegex.TITLE_TITLE_STRING]:
                    bodyText += temp + '<br>'
            else:
                bodyText += 'Untitled'
            bodyText += '</p>'
                
            # Credit
            bodyText += '<p class=\'' + self.FountainRegex.TITLE_CREDIT_CLASS + '\'>'
            if self.FountainRegex.TITLE_CREDIT_STRING in titleElements:
                for temp in titleElements[self.FountainRegex.TITLE_CREDIT_STRING]:
                    bodyText += temp + '<br>'
            else:
                bodyText += 'written by'
            bodyText += '</p>'
            
            # Authors
            bodyText += '<p class=\'' + self.FountainRegex.TITLE_AUTHOR_CLASS + '\'>'
            if self.FountainRegex.TITLE_AUTHOR_STRING in titleElements:
                for temp in titleElements[self.FountainRegex.TITLE_AUTHOR_STRING]:
                    bodyText += temp + '<br>'
            else:
                bodyText += 'Anonymous'
            bodyText += '</p>'
            
            # Sources
            if self.FountainRegex.TITLE_SOURCE_STRING in titleElements:
                bodyText += '<p class=\'' + self.FountainRegex.TITLE_SOURCE_CLASS + '\'>'
                for temp in titleElements[self.FountainRegex.TITLE_SOURCE_STRING]:
                    bodyText += temp + '<br>'
                bodyText += '</p>'
            
            # Draft date
            if self.FountainRegex.TITLE_DRAFT_DATE_STRING in titleElements:
                bodyText += '<p class=\'' + self.FountainRegex.TITLE_DRAFT_DATE_CLASS + '\'>'
                for temp in titleElements[self.FountainRegex.TITLE_DRAFT_DATE_STRING]:
                    bodyText += temp + '<br>'
                bodyText += '</p>'
            
            # Contact
            if self.FountainRegex.TITLE_CONTACT_STRING in titleElements:
                bodyText += '<p class=\'' + self.FountainRegex.TITLE_CONTACT_CLASS + '\'>'
                for temp in titleElements[self.FountainRegex.TITLE_CONTACT_STRING]:
                    bodyText += temp + '<br>'
                bodyText += '</p>'
            
            bodyText += '</div>'
            
        # Page breaks are not handled in current HTML output
        dialogueTypes = [self.FountainRegex.CHARACTER_TAG_PATTERN, self.FountainRegex.DIALOGUE_TAG_PATTERN, self.FountainRegex.PARENTHETICAL_TAG_PATTERN]
        ignoreTypes = [self.FountainRegex.BONEYARD_TAG_PATTERN, self.FountainRegex.COMMENT_TAG_PATTERN, self.FountainRegex.SYNOPSIS_TAG_PATTERN, self.FountainRegex.SECTION_HEADING_PATTERN]
        
        dualDialogueCharacterCount = 0
        
        elements = self._script._elements
        for element in elements:
            if (element._elementType in ignoreTypes):
                continue
            
            if (element._elementType == self.FountainRegex.PAGE_BREAK_PATTERN):
                bodyText += '</section>\n<section>\n'
                continue
            
            if (element._elementType == self.FountainRegex.CHARACTER_TAG_PATTERN and element._isDualDialogue):
                dualDialogueCharacterCount += 1
                if (dualDialogueCharacterCount == 1):
                    bodyText += '<div class=\'' + self.FountainRegex.DUAL_DIALOGUE_CLASS + '\'>\n'
                    bodyText += '<div class=\'' + self.FountainRegex.DUAL_DIALOGUE_LEFT_CLASS + '\'>\n'
                elif (dualDialogueCharacterCount == 2):
                    bodyText += '<div class=\'' + self.FountainRegex.DUAL_DIALOGUE_RIGHT_CLASS + '\'>\n'
            
            if (dualDialogueCharacterCount >= 2 and not (element._elementType in dialogueTypes)):
                dualDialogueCharacterCount = 0
                bodyText += '</div>\n</div>\n'
            
            text = ''
            if (element._elementType == self.FountainRegex.SCENE_HEADING_PATTERN and element._sceneNumber != None):
                text += '<span class=\'' + self.FountainRegex.SCENE_NUMBER_LEFT + '\'>' + element._sceneNumber + '</span>'
                text += element._elementText
                text += '<span class=\'' + self.FountainRegex.SCENE_NUMBER_RIGHT + '\'>' + element._sceneNumber + '</span>'
            else:
                text += element._elementText
                
            if (element._elementType == self.FountainRegex.CHARACTER_TAG_PATTERN and element._isDualDialogue):
                re.sub(self.FountainRegex.DUAL_DIALOGUE_ANGLE_MARK_PATTERN, self.FountainRegex.EMPTY_REPLACEMENT, text)
                
            re.sub(self.FountainRegex.BOLD_ITALIC_UNDERLINE_PATTERN, self.FountainRegex.BOLD_ITALIC_UNDERLINE_TEMPLATE, text)
            re.sub(self.FountainRegex.BOLD_ITALIC_PATTERN, self.FountainRegex.BOLD_ITALIC_TEMPLATE, text)
            re.sub(self.FountainRegex.BOLD_UNDERLINE_PATTERN, self.FountainRegex.BOLD_UNDERLINE_TEMPLATE, text)
            re.sub(self.FountainRegex.ITALIC_UNDERLINE_PATTERN, self.FountainRegex.ITALIC_UNDERLINE_TEMPLATE, text)
            re.sub(self.FountainRegex.BOLD_PATTERN, self.FountainRegex.BOLD_TEMPLATE, text)
            re.sub(self.FountainRegex.ITALIC_PATTERN, self.FountainRegex.ITALIC_TEMPLATE, text)
            re.sub(self.FountainRegex.UNDERLINE_PATTERN, self.FountainRegex.UNDERLINE_TEMPLATE, text)
            re.sub(self.FountainRegex.FONT_EMPH_IGNORE_TAG, self.FountainRegex.EMPTY_REPLACEMENT, text)
            
            if (text != ''):
                additionalClasses = ''
                if (element._isCentered):
                    additionalClasses += self.FountainRegex.CENTER_CLASS
                bodyText += '<p class=\'' + self.htmlClassForType(element._elementType) + additionalClasses + '\'>' + text + '</p>\n'
        
        return bodyText
    
    def bodyForScriptBase(self):
        bodyText = ''
        # add title page
        titleElements = self._script._titlePageContents
        
        if titleElements:
            bodyText += '<div id=\'' + self.FountainRegex.TITLE_DIV + '\'>'
            
            # Titles
            bodyText += '<p class=\'' + self.FountainRegex.TITLE_TITLE_CLASS + '\'>'
            if titleElements[self.FountainRegex.TITLE_TITLE_STRING]:
                for temp in titleElements[self.FountainRegex.TITLE_TITLE_STRING]:
                    bodyText += temp + '<br>'
            else:
                bodyText += 'Untitled'
            bodyText += '</p>'
                
            # Credit
            bodyText += '<p class=\'' + self.FountainRegex.TITLE_CREDIT_CLASS + '\'>'
            if self.FountainRegex.TITLE_CREDIT_STRING in titleElements:
                for temp in titleElements[self.FountainRegex.TITLE_CREDIT_STRING]:
                    bodyText += temp + '<br>'
            else:
                bodyText += 'written by'
            bodyText += '</p>'
            
            # Authors
            bodyText += '<p class=\'' + self.FountainRegex.TITLE_AUTHOR_CLASS + '\'>'
            if self.FountainRegex.TITLE_AUTHOR_STRING in titleElements:
                for temp in titleElements[self.FountainRegex.TITLE_AUTHOR_STRING]:
                    bodyText += temp + '<br>'
            else:
                bodyText += 'Anonymous'
            bodyText += '</p>'
            
            # Sources
            if self.FountainRegex.TITLE_SOURCE_STRING in titleElements:
                bodyText += '<p class=\'' + self.FountainRegex.TITLE_SOURCE_CLASS + '\'>'
                for temp in titleElements[self.FountainRegex.TITLE_SOURCE_STRING]:
                    bodyText += temp + '<br>'
                bodyText += '</p>'
            
            # Draft date
            if self.FountainRegex.TITLE_DRAFT_DATE_STRING in titleElements:
                bodyText += '<p class=\'' + self.FountainRegex.TITLE_DRAFT_DATE_CLASS + '\'>'
                for temp in titleElements[self.FountainRegex.TITLE_DRAFT_DATE_STRING]:
                    bodyText += temp + '<br>'
                bodyText += '</p>'
            
            # Contact
            if self.FountainRegex.TITLE_CONTACT_STRING in titleElements:
                bodyText += '<p class=\'' + self.FountainRegex.TITLE_CONTACT_CLASS + '\'>'
                for temp in titleElements[self.FountainRegex.TITLE_CONTACT_STRING]:
                    bodyText += temp + '<br>'
                bodyText += '</p>'
            
            bodyText += '</div>'
            
        # Page breaks are not handled in current HTML output
        dialogueTypes = [self.FountainRegex.CHARACTER_TAG_PATTERN, self.FountainRegex.DIALOGUE_TAG_PATTERN, self.FountainRegex.PARENTHETICAL_TAG_PATTERN]
        ignoreTypes = [self.FountainRegex.BONEYARD_TAG_PATTERN, self.FountainRegex.COMMENT_TAG_PATTERN, self.FountainRegex.SYNOPSIS_TAG_PATTERN, self.FountainRegex.SECTION_HEADING_PATTERN]
        
        dualDialogueCharacterCount = 0
        
        elements = self._script._elements
        for element in elements:
            if (element._elementType in ignoreTypes):
                continue
            
            if (element._elementType == self.FountainRegex.PAGE_BREAK_PATTERN):
                bodyText += '</section>\n<section>\n'
                continue
            
            if (element._elementType == self.FountainRegex.CHARACTER_TAG_PATTERN and element._isDualDialogue):
                dualDialogueCharacterCount += 1
                if (dualDialogueCharacterCount == 1):
                    bodyText += '<div class=\'' + self.FountainRegex.DUAL_DIALOGUE_CLASS + '\'>\n'
                    bodyText += '<div class=\'' + self.FountainRegex.DUAL_DIALOGUE_LEFT_CLASS + '\'>\n'
                elif (dualDialogueCharacterCount == 2):
                    bodyText += '<div class=\'' + self.FountainRegex.DUAL_DIALOGUE_RIGHT_CLASS + '\'>\n'
            
            if (dualDialogueCharacterCount >= 2 and not (element._elementType in dialogueTypes)):
                dualDialogueCharacterCount = 0
                bodyText += '</div>\n</div>\n'
            
            text = ''
            if (element._elementType == self.FountainRegex.SCENE_HEADING_PATTERN and element._sceneNumber != None):
                text += '<span class=\'' + self.FountainRegex.SCENE_NUMBER_LEFT + '\'>' + element._sceneNumber + '</span>'
                text += element._elementText
                text += '<span class=\'' + self.FountainRegex.SCENE_NUMBER_RIGHT + '\'>' + element._sceneNumber + '</span>'
            else:
                text += element._elementText
                
            if (element._elementType == self.FountainRegex.CHARACTER_TAG_PATTERN and element._isDualDialogue):
                re.sub(self.FountainRegex.DUAL_DIALOGUE_ANGLE_MARK_PATTERN, self.FountainRegex.EMPTY_REPLACEMENT, text)
                
            re.sub(self.FountainRegex.BOLD_ITALIC_UNDERLINE_PATTERN, self.FountainRegex.BOLD_ITALIC_UNDERLINE_TEMPLATE, text)
            re.sub(self.FountainRegex.BOLD_ITALIC_PATTERN, self.FountainRegex.BOLD_ITALIC_TEMPLATE, text)
            re.sub(self.FountainRegex.BOLD_UNDERLINE_PATTERN, self.FountainRegex.BOLD_UNDERLINE_TEMPLATE, text)
            re.sub(self.FountainRegex.ITALIC_UNDERLINE_PATTERN, self.FountainRegex.ITALIC_UNDERLINE_TEMPLATE, text)
            re.sub(self.FountainRegex.BOLD_PATTERN, self.FountainRegex.BOLD_TEMPLATE, text)
            re.sub(self.FountainRegex.ITALIC_PATTERN, self.FountainRegex.ITALIC_TEMPLATE, text)
            re.sub(self.FountainRegex.UNDERLINE_PATTERN, self.FountainRegex.UNDERLINE_TEMPLATE, text)
            re.sub(self.FountainRegex.FONT_EMPH_IGNORE_TAG, self.FountainRegex.EMPTY_REPLACEMENT, text)
            
            if (text != ''):
                additionalClasses = ''
                if (element._isCentered):
                    additionalClasses += self.FountainRegex.CENTER_CLASS
                bodyText += '<p class=\'' + self.htmlClassForType(element._elementType) + additionalClasses + '\'>' + text + '</p>\n'
        
        return bodyText
   