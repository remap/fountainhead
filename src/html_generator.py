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

import re
import sys

from fountain_parser import ParserVersion
from regex_rules import *

class FountainHTMLGenerator(object):
    def __init__(self, script, cssFile = '', componentParent = 'components', version = ParserVersion.DEFAULT):
        self._script = script
        self._bodyText = ''
        self._cssFile = cssFile
        self._componentParent = componentParent.rstrip('/') + '/'
        
        self._version = version
        if self._version == ParserVersion.REMAP:
            self._fountainRegex = FountainRegexRemap()
            self.generateHtml = self.generateHtmlRemap
            self._componentList = []
            
            # Character list is a dictionary of <character names, character type> pairs
            self._characterList = dict()
            self._characterTypeList = []
            self._settingList = []
            
        elif self._version == ParserVersion.BASE:
            self._fountainRegex = FountainRegexBase()
            self.generateHtml = self.generateHtmlBase
        else:
            # Right now using remap as default; DEFAULT value was not really useful, 
            # since self._fountainRegex is using Remap class
            self._version == ParserVersion.DEFAULT
            self._fountainRegex = FountainRegexRemap()
            self.generateHtml = self.generateHtmlRemap
            self._componentList = []
                        
            self._characterList = dict()
            self._characterTypeList = []
            self._settingList = []
        return
    
    # HTML class is elementType with spaces replaced by dashes
    def htmlClassForType(self, str):
        # if the str only consists of uppercase letters, it is likely that
        # we don't want to replace each uppercase letter with dash and the letter
        if not (re.match('[A-Z\s]+', str)):
            str = re.sub('([A-Z])', r'-\1', str)
        str = re.sub(' ', '-', str.strip('-').lower())
        return re.sub('-+', '-', str)
    
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
        html = '<!DOCTYPE html>\n'
        html += '<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />\n'
        html += '<html>\n<head>\n'
        if (self._cssFile != ''):
            html += '<link rel=\"stylesheet\" type=\"text/css\" href=\"' + self._cssFile + '\">\n'
        # bodyForScript fills self._componentList; Right now, components are supposed to end with a .html
        for componentName in self._componentList:
            # Note: Right now web components are expected to be .htmls only.
            html += '<link rel=\"import\" href=\"' + self._componentParent + componentName + '.html\">\n'
        # Note: here a <section> tag is added by default.
        html += '</head>\n<body>\n<section>\n' + self._bodyText + '</section>\n</body>\n</html>\n'
        return html
    
    def bodyForScriptRemap(self):
        bodyText = ''
        # add title page
        titleElements = self._script._titlePageContents
        
        if titleElements:
            bodyText += '<div id=\'' + self._fountainRegex.TITLE_DIV + '\'>'
            
            # Titles
            bodyText += '<p class=\'' + self._fountainRegex.TITLE_TITLE_CLASS + '\'>'
            if titleElements[self._fountainRegex.TITLE_TITLE_STRING]:
                for temp in titleElements[self._fountainRegex.TITLE_TITLE_STRING]:
                    bodyText += temp + '<br>'
            else:
                bodyText += 'Untitled'
            bodyText += '</p>'
                
            # Credit
            bodyText += '<p class=\'' + self._fountainRegex.TITLE_CREDIT_CLASS + '\'>'
            if self._fountainRegex.TITLE_CREDIT_STRING in titleElements:
                for temp in titleElements[self._fountainRegex.TITLE_CREDIT_STRING]:
                    bodyText += temp + '<br>'
            else:
                bodyText += 'written by'
            bodyText += '</p>'
            
            # Authors
            bodyText += '<p class=\'' + self._fountainRegex.TITLE_AUTHOR_CLASS + '\'>'
            if self._fountainRegex.TITLE_AUTHOR_STRING in titleElements:
                for temp in titleElements[self._fountainRegex.TITLE_AUTHOR_STRING]:
                    bodyText += temp + '<br>'
            else:
                bodyText += 'Anonymous'
            bodyText += '</p>'
            
            # Sources
            if self._fountainRegex.TITLE_SOURCE_STRING in titleElements:
                bodyText += '<p class=\'' + self._fountainRegex.TITLE_SOURCE_CLASS + '\'>'
                for temp in titleElements[self._fountainRegex.TITLE_SOURCE_STRING]:
                    bodyText += temp + '<br>'
                bodyText += '</p>'
            
            # Draft date
            if self._fountainRegex.TITLE_DRAFT_DATE_STRING in titleElements:
                bodyText += '<p class=\'' + self._fountainRegex.TITLE_DRAFT_DATE_CLASS + '\'>'
                for temp in titleElements[self._fountainRegex.TITLE_DRAFT_DATE_STRING]:
                    bodyText += temp + '<br>'
                bodyText += '</p>'
            
            # Contact
            if self._fountainRegex.TITLE_CONTACT_STRING in titleElements:
                bodyText += '<p class=\'' + self._fountainRegex.TITLE_CONTACT_CLASS + '\'>'
                for temp in titleElements[self._fountainRegex.TITLE_CONTACT_STRING]:
                    bodyText += temp + '<br>'
                bodyText += '</p>'
            
            bodyText += '</div>'
            
        # Page breaks are not handled in current HTML output
        dialogueTypes = [self._fountainRegex.CHARACTER_TAG_PATTERN, self._fountainRegex.DIALOGUE_TAG_PATTERN, self._fountainRegex.PARENTHETICAL_TAG_PATTERN]
        ignoreTypes = [self._fountainRegex.BONEYARD_TAG_PATTERN, self._fountainRegex.COMMENT_TAG_PATTERN, self._fountainRegex.SYNOPSIS_TAG_PATTERN, self._fountainRegex.SECTION_HEADING_PATTERN]
        
        dualDialogueCharacterCount = 0
        
        elements = self._script._elements
        
        try:
            self._fountainRegex.COMPONENT_PATTERN
        except NameError:
            print('Fountain Regex pattern does not contain definition for Web component. Version mismatch?')
            sys.exit(0)
        else:
            self._componentList = []
            # Flag for whether we are in a component definition, if so, this element should not appear as normal ones
            inComponent = False
            # Flag for whether this component is ready for generation.
            generateComponent = False
            componentName = ''
            componentArgs = dict()
            componentDesc = ''
            
        prevTag = ''
        prevType = ''
            
        for element in elements:
            if (element._elementType in ignoreTypes):
                continue
            
            if (element._elementType == self._fountainRegex.PAGE_BREAK_TAG_PATTERN):
                bodyText += '</section>\n<section>\n'
                continue
            
            if (element._elementType == self._fountainRegex.CHARACTER_TAG_PATTERN and element._isDualDialogue):
                dualDialogueCharacterCount += 1
                if (dualDialogueCharacterCount == 1):
                    bodyText += '<div class=\'' + self._fountainRegex.DUAL_DIALOGUE_CLASS + '\'>\n'
                    bodyText += '<div class=\'' + self._fountainRegex.DUAL_DIALOGUE_LEFT_CLASS + '\'>\n'
                elif (dualDialogueCharacterCount == 2):
                    bodyText += '<div class=\'' + self._fountainRegex.DUAL_DIALOGUE_RIGHT_CLASS + '\'>\n'
            
            if (dualDialogueCharacterCount >= 2 and not (element._elementType in dialogueTypes)):
                dualDialogueCharacterCount = 0
                bodyText += '</div>\n</div>\n'
            
            text = ''
            if (element._elementType == self._fountainRegex.SCENE_HEADING_PATTERN and element._sceneNumber != None):
                text += '<span class=\'' + self._fountainRegex.SCENE_NUMBER_LEFT + '\'>' + element._sceneNumber + '</span>'
                text += element._elementText
                text += '<span class=\'' + self._fountainRegex.SCENE_NUMBER_RIGHT + '\'>' + element._sceneNumber + '</span>'
            else:
                text += element._elementText
                
                # Special generation step for CharacterTypes
                if (element._elementType == self._fountainRegex.CHARACTER_TYPE_CONTENT_PATTERN):
                    characterTypeDivId = self.htmlClassForType(element._elementType)
                    bodyText += '<div id=\"' + characterTypeDivId + '\">\n'
                    bodyText += '<table>'
                    
                    characterTypeStrs = re.findall(self._fountainRegex.META_TYPE_PATTERN, element._elementText)
                    for characterTypeStr in characterTypeStrs:
                        characterType = self.htmlClassForType(characterTypeStr[0])
                        self._characterTypeList.append(characterType)
                        
                        bodyText += '<td>\n'
                        # Note: here '-def' and '-desc' is hardcoded into the class output
                        bodyText += '<p class=\'' + characterType + '-def\'>' + characterTypeStr[0] + '</p>\n'
                        bodyText += '<p class=\'' + characterTypeDivId + '-desc\'>' + characterTypeStr[1] + '</p>\n'
                        bodyText += '</td>\n'
                        
                    bodyText += '</table>\n'
                    bodyText += '</div>\n'
                    
                    # We can continue after this special generation
                    continue
                
                # Special generation step for Characters
                if (element._elementType == self._fountainRegex.CHARACTER_CONTENT_PATTERN):
                    characterDivId = self.htmlClassForType(element._elementType)
                    bodyText += '<div id=\"' + characterDivId + '\">\n'
                    
                    characterStrs = re.findall(self._fountainRegex.META_NAME_TYPE_PATTERN, element._elementText)
                    for characterStr in characterStrs:
                        characterName = self.htmlClassForType(characterStr[0])
                        characterType = self.htmlClassForType(characterStr[1])
                        self._characterList[characterName] = characterType
                        
                        # Note: here '-def' and '-desc' is hardcoded into the class output
                        bodyText += '<p class=\'' + characterName + '-def\'>' + characterStr[0] + '</p>\n'
                        bodyText += '<p class=\'' + characterType + '-def\'>' + characterStr[1] + '</p>\n'
                        bodyText += '<p class=\'' + characterDivId + '-desc\'>' + characterStr[2] + '</p>\n'
                    
                    bodyText += '</div>\n'
                    continue
                
                # Special generation step for Settings
                if (element._elementType == self._fountainRegex.SETTING_CONTENT_PATTERN):
                    settingDivId = self.htmlClassForType(element._elementType)
                    bodyText += '<div id=\"' + settingDivId + '\">\n'
                    
                    settingStrs = re.findall(self._fountainRegex.META_TYPE_PATTERN, element._elementText)
                    for settingStr in settingStrs:
                        settingName = self.htmlClassForType(settingStr[0])
                        self._settingList.append(settingName)
                        
                        # Note: here '-def' and '-desc' is hardcoded into the class output
                        bodyText += '<p class=\'' + settingName + '-def\'>' + settingStr[0] + '</p>\n'
                        bodyText += '<p class=\'' + settingDivId + '-desc\'>' + settingStr[1] + '</p>\n'
                    
                    settingStrs = re.findall(self._fountainRegex.META_ORDINARY_PATTERN, element._elementText)
                    for settingStr in settingStrs:
                        bodyText += '<p class=\'' + settingDivId + '-desc\'>' + settingStr + '</p>\n'
                    
                    bodyText += '</div>\n'
                    continue
                
                # Special generation step for web component and arguments
                if (element._elementType == self._fountainRegex.COMPONENT_NAME_PATTERN):
                    if (not inComponent):
                        if (element._elementText in self._componentList):
                            pass
                        else:
                            self._componentList.append(element._elementText)
                        componentName = element._elementText
                        inComponent = True
                    else:
                        print('ERROR: Nested component definition in script. Not sure how to parse yet.')
                if (element._elementType == self._fountainRegex.COMPONENT_ARGUMENTS_PATTERN):
                    if (inComponent):
                        args = re.findall(self._fountainRegex.COMPONENT_ARGUMENTS_SPLIT, element._elementText)
                        for arg in args:
                            equalSign = arg.find('=')
                            if (equalSign > 0):
                                argName = arg[:equalSign].strip()
                                argValue = arg[equalSign + 1:].strip()
                                componentArgs[argName] = argValue
                            else:
                                print('WARNING: no equal sign found for component argument; on purpose?')
                if (element._elementType == self._fountainRegex.COMPONENT_DESCRIPTION_PATTERN):
                    if (inComponent):
                        generateComponent = True
                        componentDesc = element._elementText
                        
            if (element._elementType == self._fountainRegex.CHARACTER_TAG_PATTERN and element._isDualDialogue):
                text = re.sub(self._fountainRegex.DUAL_DIALOGUE_ANGLE_MARK_PATTERN, self._fountainRegex.EMPTY_REPLACEMENT, text)
            
            text = re.sub(self._fountainRegex.BOLD_ITALIC_UNDERLINE_PATTERN, self._fountainRegex.BOLD_ITALIC_UNDERLINE_TAG, text)
            text = re.sub(self._fountainRegex.BOLD_ITALIC_PATTERN, self._fountainRegex.BOLD_ITALIC_TAG, text)
            text = re.sub(self._fountainRegex.BOLD_UNDERLINE_PATTERN, self._fountainRegex.BOLD_UNDERLINE_TAG, text)
            text = re.sub(self._fountainRegex.ITALIC_UNDERLINE_PATTERN, self._fountainRegex.ITALIC_UNDERLINE_TAG, text)
            text = re.sub(self._fountainRegex.BOLD_PATTERN, self._fountainRegex.BOLD_TAG, text)
            text = re.sub(self._fountainRegex.ITALIC_PATTERN, self._fountainRegex.ITALIC_TAG, text)
            text = re.sub(self._fountainRegex.UNDERLINE_PATTERN, self._fountainRegex.UNDERLINE_TAG, text)
            text = re.sub(self._fountainRegex.FONT_EMPH_IGNORE_TAG, self._fountainRegex.EMPTY_REPLACEMENT, text)
            
            if (not inComponent):
                if (text != ''):
                    additionalClasses = ''
                    
                    if (element._isCentered):
                        additionalClasses += self._fountainRegex.CENTER_CLASS
                    
                    if (prevTag == self._fountainRegex.CHARACTER_TAG_PATTERN):
                        if prevType != '' and (element._elementType == self._fountainRegex.DIALOGUE_TAG_PATTERN or element._elementType == self._fountainRegex.PARENTHETICAL_TAG_PATTERN):
                            additionalClasses += ' ' + prevType
                        else:
                            prevTag = ''
                            prevType = ''
                            
                    if (element._elementType == self._fountainRegex.CHARACTER_TAG_PATTERN):
                        characterName = self.htmlClassForType(element._elementText)
                        additionalClasses += ' ' + characterName
                        if characterName in self._characterList:
                            additionalClasses += ' ' + self._characterList[characterName]
                            prevType = self._characterList[characterName]
                        prevTag = element._elementType
                    
                    # TODO: I see a lot of "THE ARCHIVE" appear throughout the script; 
                    #       I don't think the writers want them to be an ordinary 'action';
                    #       Shouldn't be too difficult to add parsing rules / CSS styles for those. (Their definitions already exist in # Settings)
                    #       Should resolve this with writers.
                    
                    bodyText += '<p class=\'' + self.htmlClassForType(element._elementType) + additionalClasses + '\'>' + text + '</p>\n'
            elif (generateComponent):
                bodyText += '<' + componentName
                for argName, argValue in componentArgs.items():
                    bodyText += ' ' + argName + '=' + argValue
                bodyText += '>' + componentDesc + '</' + componentName + '>\n'
                
                # TODO: styling for the component hyperlink
                bodyText += '<a href=\"' + self._componentParent + componentName + '.html\">' + componentName + '</a>\n'
                
                generateComponent = False
                inComponent = False
                componentName = ''
                componentArgs = dict()
                componentDesc = ''
                
        return bodyText
    
    def bodyForScriptBase(self):
        bodyText = ''
        # add title page
        titleElements = self._script._titlePageContents
        
        if titleElements:
            bodyText += '<div id=\'' + self._fountainRegex.TITLE_DIV + '\'>'
            
            # Titles
            bodyText += '<p class=\'' + self._fountainRegex.TITLE_TITLE_CLASS + '\'>'
            if titleElements[self._fountainRegex.TITLE_TITLE_STRING]:
                for temp in titleElements[self._fountainRegex.TITLE_TITLE_STRING]:
                    bodyText += temp + '<br>'
            else:
                bodyText += 'Untitled'
            bodyText += '</p>'
                
            # Credit
            bodyText += '<p class=\'' + self._fountainRegex.TITLE_CREDIT_CLASS + '\'>'
            if self._fountainRegex.TITLE_CREDIT_STRING in titleElements:
                for temp in titleElements[self._fountainRegex.TITLE_CREDIT_STRING]:
                    bodyText += temp + '<br>'
            else:
                bodyText += 'written by'
            bodyText += '</p>'
            
            # Authors
            bodyText += '<p class=\'' + self._fountainRegex.TITLE_AUTHOR_CLASS + '\'>'
            if self._fountainRegex.TITLE_AUTHOR_STRING in titleElements:
                for temp in titleElements[self._fountainRegex.TITLE_AUTHOR_STRING]:
                    bodyText += temp + '<br>'
            else:
                bodyText += 'Anonymous'
            bodyText += '</p>'
            
            # Sources
            if self._fountainRegex.TITLE_SOURCE_STRING in titleElements:
                bodyText += '<p class=\'' + self._fountainRegex.TITLE_SOURCE_CLASS + '\'>'
                for temp in titleElements[self._fountainRegex.TITLE_SOURCE_STRING]:
                    bodyText += temp + '<br>'
                bodyText += '</p>'
            
            # Draft date
            if self._fountainRegex.TITLE_DRAFT_DATE_STRING in titleElements:
                bodyText += '<p class=\'' + self._fountainRegex.TITLE_DRAFT_DATE_CLASS + '\'>'
                for temp in titleElements[self._fountainRegex.TITLE_DRAFT_DATE_STRING]:
                    bodyText += temp + '<br>'
                bodyText += '</p>'
            
            # Contact
            if self._fountainRegex.TITLE_CONTACT_STRING in titleElements:
                bodyText += '<p class=\'' + self._fountainRegex.TITLE_CONTACT_CLASS + '\'>'
                for temp in titleElements[self._fountainRegex.TITLE_CONTACT_STRING]:
                    bodyText += temp + '<br>'
                bodyText += '</p>'
            
            bodyText += '</div>'
            
        # Page breaks are not handled in current HTML output
        dialogueTypes = [self._fountainRegex.CHARACTER_TAG_PATTERN, self._fountainRegex.DIALOGUE_TAG_PATTERN, self._fountainRegex.PARENTHETICAL_TAG_PATTERN]
        ignoreTypes = [self._fountainRegex.BONEYARD_TAG_PATTERN, self._fountainRegex.COMMENT_TAG_PATTERN, self._fountainRegex.SYNOPSIS_TAG_PATTERN, self._fountainRegex.SECTION_HEADING_PATTERN]
        
        dualDialogueCharacterCount = 0
        
        elements = self._script._elements
        for element in elements:
            if (element._elementType in ignoreTypes):
                continue
            
            if (element._elementType == self._fountainRegex.PAGE_BREAK_TAG_PATTERN):
                bodyText += '</section>\n<section>\n'
                continue
            
            if (element._elementType == self._fountainRegex.CHARACTER_TAG_PATTERN and element._isDualDialogue):
                dualDialogueCharacterCount += 1
                if (dualDialogueCharacterCount == 1):
                    bodyText += '<div class=\'' + self._fountainRegex.DUAL_DIALOGUE_CLASS + '\'>\n'
                    bodyText += '<div class=\'' + self._fountainRegex.DUAL_DIALOGUE_LEFT_CLASS + '\'>\n'
                elif (dualDialogueCharacterCount == 2):
                    bodyText += '<div class=\'' + self._fountainRegex.DUAL_DIALOGUE_RIGHT_CLASS + '\'>\n'
            
            if (dualDialogueCharacterCount >= 2 and not (element._elementType in dialogueTypes)):
                dualDialogueCharacterCount = 0
                bodyText += '</div>\n</div>\n'
            
            text = ''
            if (element._elementType == self._fountainRegex.SCENE_HEADING_PATTERN and element._sceneNumber != None):
                text += '<span class=\'' + self._fountainRegex.SCENE_NUMBER_LEFT + '\'>' + element._sceneNumber + '</span>'
                text += element._elementText
                text += '<span class=\'' + self._fountainRegex.SCENE_NUMBER_RIGHT + '\'>' + element._sceneNumber + '</span>'
            else:
                text += element._elementText
                
            if (element._elementType == self._fountainRegex.CHARACTER_TAG_PATTERN and element._isDualDialogue):
                text = re.sub(self._fountainRegex.DUAL_DIALOGUE_ANGLE_MARK_PATTERN, self._fountainRegex.EMPTY_REPLACEMENT, text)
                
            text = re.sub(self._fountainRegex.BOLD_ITALIC_UNDERLINE_PATTERN, self._fountainRegex.BOLD_ITALIC_UNDERLINE_TAG, text)
            text = re.sub(self._fountainRegex.BOLD_ITALIC_PATTERN, self._fountainRegex.BOLD_ITALIC_TAG, text)
            text = re.sub(self._fountainRegex.BOLD_UNDERLINE_PATTERN, self._fountainRegex.BOLD_UNDERLINE_TAG, text)
            text = re.sub(self._fountainRegex.ITALIC_UNDERLINE_PATTERN, self._fountainRegex.ITALIC_UNDERLINE_TAG, text)
            text = re.sub(self._fountainRegex.BOLD_PATTERN, self._fountainRegex.BOLD_TAG, text)
            text = re.sub(self._fountainRegex.ITALIC_PATTERN, self._fountainRegex.ITALIC_TAG, text)
            text = re.sub(self._fountainRegex.UNDERLINE_PATTERN, self._fountainRegex.UNDERLINE_TAG, text)
            text = re.sub(self._fountainRegex.FONT_EMPH_IGNORE_TAG, self._fountainRegex.EMPTY_REPLACEMENT, text)
            
            if (text != ''):
                additionalClasses = ''
                if (element._isCentered):
                    additionalClasses += self._fountainRegex.CENTER_CLASS
                bodyText += '<p class=\'' + self.htmlClassForType(element._elementType) + additionalClasses + '\'>' + text + '</p>\n'
        
        return bodyText
   