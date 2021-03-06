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

# This is used for special character and dialogue generation
# 'the-guide': chat-control-muc
# 'the-observatory': chat-control-muc                            
specialGenerationTags = {
    'the-guide': ['chat-control-muc', 'guide@conference.archive-dev.remap.ucla.edu', 'THE GUIDE'],
    'the-observatory': ['chat-control-muc', 'observatory@conference.archive-dev.remap.ucla.edu', 'THE OBSERVATORY']
}

specialGenerationPatterns = {
    r'\*[oO][lL][fF]:(.*)\*': [r'description="OLF: \1"', 'olf'],
    r'\*[Vv][Qq] *\#([^ ]*) *- *([^\n]*)\*': [r't="VQ #\1" cid="\1" desc="\2"', 'cue-publisher']
}

class FountainHTMLGenerator(object):
    def __init__(self, script, cssFile = '', componentParent = 'components', includeParent = 'includes', version = ParserVersion.DEFAULT, special = False):
        self._script = script
        self._bodyText = ''
        self._indentLevel = 0
        self._cssFile = cssFile
        self._sceneHeadings = []
        self._parseSpecial = special
        
        self._version = version
        if self._version == ParserVersion.REMAP:
            self._fountainRegex = FountainRegexRemap()
            self.generateHtml = self.generateHtmlRemap
            self._componentList = []
            
            # Character list is a dictionary of <character names, character type> pairs
            self._characterList = dict()
            self._characterTypeList = []
            self._settingList = []
            
            self._componentParent = componentParent.rstrip('/') + '/'
            self._includeParent = includeParent.rstrip('/') + '/'
        elif self._version == ParserVersion.BASE:
            self._fountainRegex = FountainRegexBase()
            self.generateHtml = self.generateHtmlBase
            if (self._parseSpecial == True):
                print('WARNING: --parse-special flag may not be existent for BASE tag')
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
            
            self._componentParent = componentParent.rstrip('/') + '/'
            self._includeParent = includeParent.rstrip('/') + '/'
        return
    
    def sanitizeElementText(self, strText):
        strText = strText.replace('<', '&lt;').replace('>', '&gt;').replace('\"', '&#34;').replace('\'', '&#39;')
        strText = re.sub(r'\s+', '&#32;', strText).strip()
        return strText
    
    # HTML class is elementType with spaces replaced by dashes
    def htmlClassForType(self, strType):
        # if the str only consists of uppercase letters, it is likely that
        # we don't want to replace each uppercase letter with dash and the letter
        if not (re.match('[A-Z\s]+', strType)):
            strType = re.sub('([A-Z])', r'-\1', strType)
        strType = re.sub(' ', '-', strType.strip('-').lower())
        return re.sub('-+', '-', strType)
    
    def generateHtmlBase(self):
        self._indentLevel = 0
        html = '<!DOCTYPE html>\n<html>\n<head>\n'
        
        self._indentLevel += 1
        if (self._bodyText == ''):
            self._bodyText = self.bodyForScriptBase()
        
        if (self._cssFile != ''):
            html += self.prependIndentLevel() + '<link rel=\"stylesheet\" type=\"text/css\" href=\"' + self._cssFile + '\">\n'
        html += '</head>\n<body>\n<section>\n'
        html += self._bodyText 
        self._indentLevel -= 1
        html += self.prependIndentLevel() + '</body>\n</html>\n</section>\n'
        return html
    
    def generateHtmlRemap(self):
        self._indentLevel = 0
        html = '<!DOCTYPE html>\n'
        html += '<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />\n'
        html += '<html>\n<head>\n'
        
        self._indentLevel += 1
        if (self._bodyText == ''):
            self._bodyText = self.bodyForScriptRemap()
        
        if (self._cssFile != ''):
            html += self.prependIndentLevel() + '<link rel=\"stylesheet\" type=\"text/css\" href=\"' + self._cssFile + '\">\n'
        
        html += '</head>\n<body>\n<section>\n'
        
        html += self._bodyText 
        self._indentLevel -= 1
        html += '</section>\n</body>\n</html>\n'
        return html
    
    def prependIndentLevel(self, level = -1):
        if (level == -1):
            return self._indentLevel * 2 * ' '
        else:
            return level * 2 * ' '
            
    def bodyForScriptRemap(self):
        bodyText = ''
        
        # inScriptBody is the flag that separates meta from actual script body
        inScriptBody = False
        # add title page
        titleElements = self._script._titlePageContents
        
        if titleElements:
            bodyText += self.prependIndentLevel() + '<div id=\'' + self._fountainRegex.TITLE_DIV + '\'>\n'
            self._indentLevel += 1
            
            # Titles
            bodyText += self.prependIndentLevel() + '<p class=\'' + self._fountainRegex.TITLE_TITLE_CLASS + '\'>'
            if titleElements[self._fountainRegex.TITLE_TITLE_STRING]:
                for temp in titleElements[self._fountainRegex.TITLE_TITLE_STRING]:
                    bodyText += temp + '<br>'
            else:
                bodyText += 'Untitled'
            bodyText += '</p>\n'
                
            # Credit
            bodyText += self.prependIndentLevel() + '<p class=\'' + self._fountainRegex.TITLE_CREDIT_CLASS + '\'>'
            if self._fountainRegex.TITLE_CREDIT_STRING in titleElements:
                for temp in titleElements[self._fountainRegex.TITLE_CREDIT_STRING]:
                    bodyText += temp + '<br>'
            else:
                bodyText += 'written by'
            bodyText += '</p>\n'
            
            # Authors
            bodyText += self.prependIndentLevel() + '<p class=\'' + self._fountainRegex.TITLE_AUTHOR_CLASS + '\'>'
            if self._fountainRegex.TITLE_AUTHOR_STRING in titleElements:
                for temp in titleElements[self._fountainRegex.TITLE_AUTHOR_STRING]:
                    bodyText += temp + '<br>'
            else:
                bodyText += 'Anonymous'
            bodyText += '</p>\n'
            
            # Sources
            if self._fountainRegex.TITLE_SOURCE_STRING in titleElements:
                bodyText += self.prependIndentLevel() + '<p class=\'' + self._fountainRegex.TITLE_SOURCE_CLASS + '\'>'
                for temp in titleElements[self._fountainRegex.TITLE_SOURCE_STRING]:
                    bodyText += temp + '<br>'
                bodyText += '</p>\n'
            
            # Draft date
            if self._fountainRegex.TITLE_DRAFT_DATE_STRING in titleElements:
                bodyText += self.prependIndentLevel() + '<p class=\'' + self._fountainRegex.TITLE_DRAFT_DATE_CLASS + '\'>'
                for temp in titleElements[self._fountainRegex.TITLE_DRAFT_DATE_STRING]:
                    bodyText += temp + '<br>'
                bodyText += '</p>\n'
            
            # Contact
            if self._fountainRegex.TITLE_CONTACT_STRING in titleElements:
                bodyText += self.prependIndentLevel() + '<p class=\'' + self._fountainRegex.TITLE_CONTACT_CLASS + '\'>'
                for temp in titleElements[self._fountainRegex.TITLE_CONTACT_STRING]:
                    bodyText += temp + '<br>'
                bodyText += '</p>\n'
            
            self._indentLevel -= 1
            bodyText += self.prependIndentLevel() + '</div>\n'
            
        # Page breaks are not handled in current HTML output
        # Note: dialogueTypes is set to remove Character pattern, for more reasonable ending condition
        dialogueTypes = [self._fountainRegex.DIALOGUE_TAG_PATTERN, self._fountainRegex.PARENTHETICAL_TAG_PATTERN]
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
            
        # Previous tag and type try to apply the character type class (such as 'travelers') 
        # of a character to the character's parenthetical or dialogue
        prevTag = ''
        prevType = ''
        sceneCnt = 0
        
        # If true, skip ordinary <p class='...'> + '...' + </p> generation, 
        # and (probably) switch to web component generation
        # Right now used by special web component generation for the-guide/observatory
        skipOrdinaryGeneration = False
        
        skipDualDialogueEnd = False
        
        componentImportInsertionPoint = -1
        componentImportInsertionIndent = -1
        
        menuInsertionPoint = -1
        menuInsertionIndent = -1
        
        for element in elements:
            skipDualDialogueEnd = False
            
            # TODO: skipOrdinaryGeneration should be better handled
            skipOrdinaryGeneration = False
                    
            if (element._elementType in ignoreTypes):
                continue
            
            if (element._elementType == self._fountainRegex.PAGE_BREAK_TAG_PATTERN):
                bodyText += self.prependIndentLevel() + '</section>\n<section>\n'
                continue
            
            # Special handling for < and > characters for not messing up with html elements
            # TODO: check if this would mess up with anything
            element._elementText = element._elementText.replace('<', '&lt;')
            element._elementText = element._elementText.replace('>', '&gt;')
            
            if (element._elementType == self._fountainRegex.CHARACTER_TAG_PATTERN and element._isDualDialogue):
                dualDialogueCharacterCount += 1
                if (dualDialogueCharacterCount == 1):
                    bodyText += self.prependIndentLevel() + '<div class=\'' + self._fountainRegex.DUAL_DIALOGUE_CLASS + '\'>\n'
                    self._indentLevel += 1
                    bodyText += self.prependIndentLevel() + '<div class=\'' + self._fountainRegex.DUAL_DIALOGUE_LEFT_CLASS + '\'>\n'
                    self._indentLevel += 1
                elif (dualDialogueCharacterCount == 2):
                    self._indentLevel -= 1
                    bodyText += self.prependIndentLevel() + '</div>\n'
                    bodyText += self.prependIndentLevel() + '<div class=\'' + self._fountainRegex.DUAL_DIALOGUE_RIGHT_CLASS + '\'>\n'
                    self._indentLevel += 1
                    skipDualDialogueEnd = True
            
            # Note: this part differs from our example in ObjC, since theirs would include all following dual dialogues in right div
            if ((not skipDualDialogueEnd) and dualDialogueCharacterCount >= 2 and (not (element._elementType in dialogueTypes))):
                self._indentLevel -= 1
                bodyText += self.prependIndentLevel() + '</div>\n'
                self._indentLevel -= 1
                bodyText += self.prependIndentLevel() + '</div>\n'
                
                # For dual dialogues followed by dual dialogues
                if dualDialogueCharacterCount == 3:
                    bodyText += self.prependIndentLevel() + '<div class=\'' + self._fountainRegex.DUAL_DIALOGUE_CLASS + '\'>\n'
                    self._indentLevel += 1
                    bodyText += self.prependIndentLevel() + '<div class=\'' + self._fountainRegex.DUAL_DIALOGUE_LEFT_CLASS + '\'>\n'
                    self._indentLevel += 1
                    dualDialogueCharacterCount = 1
                else:
                    dualDialogueCharacterCount = 0
                
            text = ''
            if (element._elementType == self._fountainRegex.SCENE_HEADING_PATTERN and element._sceneNumber != None):
                text += '<span class=\'' + self._fountainRegex.SCENE_NUMBER_LEFT + '\'>' + element._sceneNumber + '</span>'
                text += element._elementText
                text += '<span class=\'' + self._fountainRegex.SCENE_NUMBER_RIGHT + '\'>' + element._sceneNumber + '</span>'
            else:
                text += element._elementText
                
                # Special generation step for Environments (and temporarily, for the floating menu)
                if (element._elementType == self._fountainRegex.ENVIRONMENT_CONTENT_PATTERN):
                    
                    # Special generation step for Floating Menu, left here temporarily
                    # TODO: remove/customize this, as it does not fit in here currently
                    menuInsertionPoint = len(bodyText)
                    menuInsertionIndent = self._indentLevel
                    
                    bodyText += self.prependIndentLevel() + '<script>\n'
                    
                    environmentDeclarations = re.findall(self._fountainRegex.META_TYPE_PATTERN, element._elementText)
                    for (environmentDeclaration) in environmentDeclarations:
                        environmentName = environmentDeclaration[0]
                        environmentValue = environmentDeclaration[1]
                        
                        # Note: Right now tha parser 'just knows' to deal with 'includes' differently, 
                        # and the writer 'just knows' that when ndn-js is included, a Face can be created with [uri:port], and ndn-init should be included.
                        # TODO: This should probably be handled by 'plugins' to this parser.
                        if (environmentName == self._fountainRegex.ENVIRONMENT_INCLUDE_PATTERN):
                            bodyText += self.prependIndentLevel() + '</script>\n' + self.prependIndentLevel() + '<script src=\"' + self._includeParent + environmentValue + '\"></script>\n' + self.prependIndentLevel() + '<script>\n'
                        else:
                            bodyText += 'var ' + environmentName + ' = ' + environmentValue + ';\n'
                            
                    bodyText += self.prependIndentLevel() + '</script>\n'
                    componentImportInsertionPoint = len(bodyText)
                    componentImportInsertionIndent = self._indentLevel
                    
                    continue
                    
                # Special generation step for CharacterTypes
                if (element._elementType == self._fountainRegex.CHARACTER_TYPE_CONTENT_PATTERN):
                    characterTypeDivId = self.htmlClassForType(element._elementType)
                    bodyText += self.prependIndentLevel() + '<div id=\"' + characterTypeDivId + '\">\n'
                    self._indentLevel += 1
                    
                    bodyText += self.prependIndentLevel() + '<table>\n'
                    
                    characterTypeStrs = re.findall(self._fountainRegex.META_TYPE_PATTERN, element._elementText)
                    for characterTypeStr in characterTypeStrs:
                        characterType = self.htmlClassForType(characterTypeStr[0])
                        self._characterTypeList.append(characterType)
                        
                        bodyText += self.prependIndentLevel() + '<td>\n'
                        self._indentLevel += 1
                        # Note: here '-def' and '-desc' is hardcoded into the class output
                        bodyText += self.prependIndentLevel() + '<p class=\'' + characterType + '-def\'>' + characterTypeStr[0] + '</p>\n'
                        bodyText += self.prependIndentLevel() + '<p class=\'' + characterTypeDivId + '-desc\'>' + characterTypeStr[1] + '</p>\n'
                        self._indentLevel -= 1
                        bodyText += self.prependIndentLevel() + '</td>\n'
                        
                    bodyText += self.prependIndentLevel() + '</table>\n'
                    
                    self._indentLevel -= 1
                    bodyText += self.prependIndentLevel() + '</div>\n'
                    
                    # We can continue after this special generation
                    continue
                
                # Special generation step for Characters
                if (element._elementType == self._fountainRegex.CHARACTER_CONTENT_PATTERN):
                    characterDivId = self.htmlClassForType(element._elementType)
                    bodyText += self.prependIndentLevel() + '<div id=\"' + characterDivId + '\">\n'
                    self._indentLevel += 1
                    
                    characterStrs = re.findall(self._fountainRegex.META_NAME_TYPE_PATTERN, element._elementText)
                    for characterStr in characterStrs:
                        characterName = self.htmlClassForType(characterStr[0])
                        characterType = self.htmlClassForType(characterStr[1])
                        self._characterList[characterName] = characterType
                        
                        # Note: here '-def' and '-desc' is hardcoded into the class output
                        bodyText += self.prependIndentLevel() + '<p class=\'' + characterName + '-def\'>' + characterStr[0] + '</p>\n'
                        # According to Zoe's edits, the following line that generates 'character
                        # type of character' line does not seem necessary
                        #bodyText += self.prependIndentLevel() + '<p class=\'' + characterType + '-def\'>' + characterStr[1] + '</p>\n'
                        bodyText += self.prependIndentLevel() + '<p class=\'' + characterDivId + '-desc\'>' + characterStr[2] + '</p>\n'
                    
                    self._indentLevel -= 1
                    bodyText += self.prependIndentLevel() + '</div>\n'
                    continue
                
                # Special generation step for Settings
                if (element._elementType == self._fountainRegex.SETTING_CONTENT_PATTERN):
                    settingDivId = self.htmlClassForType(element._elementType)
                    bodyText += self.prependIndentLevel() + '<div id=\"' + settingDivId + '\">\n'
                    self._indentLevel += 1
                    
                    settingStrs = re.findall(self._fountainRegex.META_TYPE_PATTERN, element._elementText)
                    for settingStr in settingStrs:
                        settingName = self.htmlClassForType(settingStr[0])
                        self._settingList.append(settingName)
                        
                        # Note: here '-def' and '-desc' is hardcoded into the class output
                        bodyText += self.prependIndentLevel() + '<p class=\'' + settingName + '-def\'>' + settingStr[0] + '</p>\n'
                        bodyText += self.prependIndentLevel() + '<p class=\'' + settingDivId + '-desc\'>' + settingStr[1] + '</p>\n'
                    
                    settingStrs = re.findall(self._fountainRegex.META_ORDINARY_PATTERN, element._elementText)
                    for settingStr in settingStrs:
                        bodyText += self.prependIndentLevel() + '<p class=\'' + settingDivId + '-desc\'>' + settingStr + '</p>\n'
                    
                    self._indentLevel -= 1
                    bodyText += self.prependIndentLevel() + '</div>\n'
                    continue
                
                # Special generation step for the beginning of the actual script 'body'
                if (element._elementType == self._fountainRegex.SCRIPT_BODY_CONTENT_PATTERN):
                    inScriptBody = True
                    bodyText += self.prependIndentLevel() + '<div id=\"' + self.htmlClassForType(self._fountainRegex.SCRIPT_BODY_CONTENT_PATTERN) + '\">\n'
                    self._indentLevel += 1
                    continue
                
                # Special generation step for scene headings to provide the table of content for jumping
                if (element._elementType == self._fountainRegex.SCENE_HEADING_PATTERN):
                    self._sceneHeadings.append(element._elementText)
                    bodyText += self.prependIndentLevel() + '<p id=\'toc' + str(sceneCnt) + '\' class=\'' + self.htmlClassForType(element._elementType) + '\'>' + element._elementText + '</p>\n'
                    sceneCnt += 1
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
                                argValue = self.sanitizeElementText(arg[equalSign + 1:].strip())
                                
                                componentArgs[argName] = argValue
                            else:
                                print('WARNING: no equal sign found for web component argument; Parsing result may be unexpected')
                                print('Related element text: ' + element._elementText)
                                print('arg: ' + arg)
                                
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
                    
                    # This tries to parse special dialogues when parseSpecial is present
                    # TODO: possibly not handled correctly when both parenthetical and dialogues are present after a character tag
                    if (prevTag == self._fountainRegex.CHARACTER_TAG_PATTERN):
                        if (element._elementType == self._fountainRegex.DIALOGUE_TAG_PATTERN or element._elementType == self._fountainRegex.PARENTHETICAL_TAG_PATTERN):
                            additionalClasses += ' ' + prevType
                            if (self._parseSpecial and prevType in specialGenerationTags):
                                # For Parentheticals that come after a specially treated character, we ignore it
                                if (element._elementType == self._fountainRegex.PARENTHETICAL_TAG_PATTERN):
                                    continue
                                bodyText += '\n' + self.prependIndentLevel() + '<' + self.componentNameToTag(specialGenerationTags[prevType][0])
                                # TODO: for this type of special generation, we need to decide whether to sanitize the parameters here or not.
                                bodyText += ' message=\"' + self.sanitizeElementText(element._elementText) + '\" roomJID=\"' + specialGenerationTags[prevType][1] + '\" fromNickName=\"' + specialGenerationTags[prevType][2] + '\">'
                                bodyText += '\n' + self.prependIndentLevel() + '</' + self.componentNameToTag(specialGenerationTags[prevType][0]) + '>'
                                # Commented out intentionally because of the potential dual-dialogue link generation confusion
                                # bodyText += self.prependIndentLevel() + '<a target=\"_blank\" href=\"' + self._componentParent + specialGenerationTags[prevType] + '.html\" class=\"' + self._fountainRegex.COMPONENT_LINK_CLASS + '\">' + specialGenerationTags[prevType] + '</a>\n'
                                continue
                        else:
                            prevTag = ''
                            prevType = ''
                    
                    # For 'Actions', there may be special generation step for olfs when parseSpecial flag is present
                    # Note: for now, we've only tested with one 'special' pattern treatment, which is olf
                    if (element._elementType == self._fountainRegex.ACTION_TAG_PATTERN):
                        if (self._parseSpecial):
                            matchKey = None
                            for key in specialGenerationPatterns:
                                if re.match(key, element._elementText):
                                    matchKey = key
                                    bodyText += '\n' + self.prependIndentLevel() + '<' + self.componentNameToTag(specialGenerationPatterns[key][1])
                                    bodyText += ' ' + re.sub(key, specialGenerationPatterns[key][0], element._elementText) + '>'
                                    bodyText += '\n' + self.prependIndentLevel() + '</' + self.componentNameToTag(specialGenerationPatterns[key][1]) + '>'
                                    # Note: We only try for one potential special pattern matches now
                                    break
                                
                            if matchKey:
                                if not (specialGenerationPatterns[matchKey][1] in self._componentList):
                                    self._componentList.append(specialGenerationPatterns[matchKey][1])
                                continue
                    
                    if (element._elementType == self._fountainRegex.CHARACTER_TAG_PATTERN):
                        characterName = self.htmlClassForType(element._elementText)
                        additionalClasses += ' ' + characterName
                        if characterName in self._characterList:
                            additionalClasses += ' ' + self._characterList[characterName]
                            prevType = self._characterList[characterName]
                        prevTag = element._elementType
                        
                        # TODO: For parseSpecial flag, hardcoding this (without basic generalization) is not preferable.
                        if self._parseSpecial:
                            # For losatlantis, the-guide and the-observatory are specially handled:
                            # they do not generate elementText_, and skip ordinary generation; instead they create
                            # web component code with remap syntax...
                            if characterName in specialGenerationTags:
                                prevType = characterName
                                # skipOrdinaryGeneration = True
                                # Do not forget to add this web component to the imported list
                                if (not specialGenerationTags[characterName][0] in self._componentList):
                                    self._componentList.append(specialGenerationTags[characterName][0])
                                continue
                        
                    # Special generation step for text marked with specific classes
                    specificClasses = re.findall(self._fountainRegex.SPECIFIC_CSS_ADDON_PATTERN, text)
                    
                    for specificClass in specificClasses:
                        className = self.htmlClassForType(specificClass[0])
                        classText = specificClass[1]
                        replacement = self.prependIndentLevel() + '<p class=\'' + className + '\'>' + classText + '</p>'
                        text = re.sub(self._fountainRegex.SPECIFIC_CSS_ADDON_PATTERN, replacement, text, 1)
                        
                    if not (skipOrdinaryGeneration and self._parseSpecial):
                        bodyText += self.prependIndentLevel() + '<p class=\'' + self.htmlClassForType(element._elementType) + additionalClasses + '\'>' + text + '</p>\n'
            elif (generateComponent):
                # Note: The "com-" is mandatorily prepended to the component name at this moment, may want to change in the future
                componentTagName = self.componentNameToTag(componentName)
                
                bodyText += '<' + componentTagName
                for argName, argValue in componentArgs.items():
                    bodyText += ' ' + argName + '=' + argValue
                bodyText += '>' + componentDesc + '</' + componentTagName + '>\n'
                
                bodyText += self.prependIndentLevel() + '<a target=\"_blank\" href=\"' + self._componentParent + componentName + '.html\" class=\"' + self._fountainRegex.COMPONENT_LINK_CLASS + '\">' + componentName + '</a>\n'
                
                generateComponent = False
                inComponent = False
                componentName = ''
                componentArgs = dict()
                componentDesc = ''
        
        if (inScriptBody):
            self._indentLevel -= 1
            bodyText += self.prependIndentLevel() + '</div>'
        
        # Special insertion step for web component imports
        # At this point, self._componentList is filled, 
        # and we append the import links after all scripts are included
        if (componentImportInsertionPoint != -1):
            importInsertion = ''
            for componentName in self._componentList:
                # Note: Right now web components are expected to be .htmls only.
                # Note: here the parser is assumed to know the load error callback, which is not ideal
                importInsertion += self.prependIndentLevel(componentImportInsertionIndent) + '<link rel=\"import\" href=\"' + self._componentParent + componentName + '.html\" onerror=\"onImportError(event)\">\n'
        
            bodyText = bodyText[:componentImportInsertionPoint] + importInsertion + bodyText[componentImportInsertionPoint:]
        
        # Special generation step for floating menu
        # TODO: reconsider this; should remove/customize along with the menuInsertionPoint assignment
        if (menuInsertionPoint != -1):
            menuInsertion = ''
        
            menuInsertion += self.prependIndentLevel(menuInsertionIndent) + '<div id="floating-menu">\n'
            menuInsertion += self.prependIndentLevel(menuInsertionIndent + 1) + '<h3>Menu (Press \'t\' to show/hide)</h3>\n'
            
            # TODO: remove hard-coded direct Javascript call from here; maybe implement the menu as a separate component or included html (rather than JS only includes that we have now)?
            menuInsertion += self.prependIndentLevel(menuInsertionIndent + 1) + '<a id="floating-menu-toggle-olf" href="#" onclick="scriptControl.toggleClassVisibility(\'olf\');return false;">Show/hide OLF</a>\n'
            
            menuInsertion += self.prependIndentLevel(menuInsertionIndent + 1) + '<br><hr>\n'
            menuInsertion += self.prependIndentLevel(menuInsertionIndent + 1) + '<h3>Table of Contents</h3>\n'
            
            tocCnt = 0
            for menuItem in self._sceneHeadings:
                menuInsertion += self.prependIndentLevel(menuInsertionIndent + 1) + '<a href=\"#toc' + str(tocCnt) + '\">' + menuItem + '</a>\n'
                tocCnt += 1
                
            menuInsertion += self.prependIndentLevel(menuInsertionIndent) + '</div>\n'
            
            bodyText = bodyText[:menuInsertionPoint] + menuInsertion + bodyText[menuInsertionPoint:]
            
        return bodyText
    
    def componentNameToTag(self, componentName):
        tagName = 'com-' + componentName
        tagName = tagName.lower().replace('/', '-')
        return tagName
    
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
        dialogueTypes = [self._fountainRegex.DIALOGUE_TAG_PATTERN, self._fountainRegex.PARENTHETICAL_TAG_PATTERN]
        ignoreTypes = [self._fountainRegex.BONEYARD_TAG_PATTERN, self._fountainRegex.COMMENT_TAG_PATTERN, self._fountainRegex.SYNOPSIS_TAG_PATTERN, self._fountainRegex.SECTION_HEADING_PATTERN]
        
        dualDialogueCharacterCount = 0
        
        elements = self._script._elements
        for element in elements:
            if (element._elementType in ignoreTypes):
                continue
            
            if (element._elementType == self._fountainRegex.PAGE_BREAK_TAG_PATTERN):
                self._indentLevel -= 1
                if (self._indentLevel < 0):
                    self._indentLevel = 0
                bodyText += self.prependIndentLevel() + '</section>\n<section>\n'
                self._indentLevel += 1
                continue
            
            if (element._elementType == self._fountainRegex.CHARACTER_TAG_PATTERN and element._isDualDialogue):
                dualDialogueCharacterCount += 1
                
                if (dualDialogueCharacterCount == 1):
                    bodyText += '<div class=\'' + self._fountainRegex.DUAL_DIALOGUE_CLASS + '\'>\n'
                    bodyText += '<div class=\'' + self._fountainRegex.DUAL_DIALOGUE_LEFT_CLASS + '\'>\n'
                elif (dualDialogueCharacterCount == 2):
                    bodyText += '</div>\n<div class=\'' + self._fountainRegex.DUAL_DIALOGUE_RIGHT_CLASS + '\'>\n'
            
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
   