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

# This module defines the Parser class for fountain scripts.
# Ported to Python from objc in nyousefi/Fountain repository

import re        

from fountain_element import FountainElement
from regex_rules import *

class ParserVersion(object):
    DEFAULT = 'remap'
    BASE = 'base'
    REMAP = 'remap'
    
    Versions = [DEFAULT, BASE, REMAP]

# TODO: Parser should be versioned as well as Regex
#       Ideally each version of the parser should be a child class implementing an interface?
class Parser(object):
	# Right now each 'parser version tag' may correspond with a different function (largely duplicate of each other),
    # Though they don't necessarily need to: regex_rules are summarized in corresponding rule class variables.
    # Left here for future potential needs.
    def __init__(self, version = ParserVersion.DEFAULT):
        self._version = version
        if self._version == ParserVersion.REMAP:
            self._fountainRegex = FountainRegexRemap()
            self.parseBodyOfString = self.parseBodyOfStringRemap
            self.parseTitlePageOfString = self.parseTitlePageOfStringBase
        elif self._version == ParserVersion.BASE:
            self._fountainRegex = FountainRegexBase()
            self.parseBodyOfString = self.parseBodyOfStringBase
            self.parseTitlePageOfString = self.parseTitlePageOfStringBase
        else:
            # Right now using remap as default
            self._version == ParserVersion.DEFAULT
            self._fountainRegex = FountainRegexRemap()
            self.parseBodyOfString = self.parseBodyOfStringRemap
            self.parseTitlePageOfString = self.parseTitlePageOfStringBase
        return
    
    # Script separation methods: separate a given script to title and body
    
    def bodyOfString(self, string):
        body = re.sub(self._fountainRegex.SLASH_N_PATTERN, self._fountainRegex.EMPTY_REPLACEMENT, string)
        
        # Find title page by looking for the first blank line, then checking the
        # text above it. If a title page is found we remove it, leaving only the
        # body content.
        
        firstBlankLine = body.find(self._fountainRegex.DOUBLE_NEWLINES_PATTERN)
        if firstBlankLine > 0:
            # TODO: check if the index is correct
            documentTop = body[:(firstBlankLine + 1)]
            documentTop += self._fountainRegex.NEWLINE_DEFAULT
            
            # check if this is a title page
            if re.search(self._fountainRegex.TITLE_PAGE_PATTERN, documentTop):
                # TODO: check if the index is correct
                body = body[firstBlankLine:]
                
        ret = self._fountainRegex.DOUBLE_NEWLINES_PATTERN + body + self._fountainRegex.DOUBLE_NEWLINES_PATTERN
        return ret
    
    def titlePageOfString(self, string):
        body = re.sub(self._fountainRegex.SLASH_N_PATTERN, self._fountainRegex.EMPTY_REPLACEMENT, string)
        
        # Find title page by looking for the first blank line, then checking the
        # text above it. If a title page is found we remove it, leaving only the
        # body content.
        
        firstBlankLine = body.find(self._fountainRegex.DOUBLE_NEWLINES_PATTERN)
        if firstBlankLine > 0:
            # TODO: check if the index is correct
            documentTop = body[:(firstBlankLine + 1)]
            documentTop += self._fountainRegex.NEWLINE_DEFAULT
            
            # check if this is a title page
            if re.search(self._fountainRegex.TITLE_PAGE_PATTERN, documentTop):
                documentTop = re.sub(self._fountainRegex.TITLE_NEWLINE_ENDING_PATTERN, self._fountainRegex.EMPTY_REPLACEMENT, documentTop)
                documentTop = re.sub(self._fountainRegex.TITLE_NOT_NEWLINE_PATTERN, self._fountainRegex.EMPTY_REPLACEMENT, documentTop)
                return documentTop
        return
    
    # Shared function for script parsing; parseBodyOfBody -> extractElements
    
    def extractElements(self, scriptContent):
        tagMatching = re.findall(self._fountainRegex.TAG_PATTERN, scriptContent)
        if not tagMatching:
            print('WARNING: Tag patterns does not match scriptContent')
            return
        elementTexts = [temp[1] for temp in tagMatching]
        elementTypes = [temp[0] for temp in tagMatching]
        
        if (len(elementTexts) != len(elementTypes)):
            print('ERROR: Text and Type counts don\'t match.')
            return
        
        elementsArray = []
        
        for i in range(0, len(elementTypes)):
            # Convert <, > and ... back to normal
            cleanedText = elementTexts[i]
            cleanedText = cleanedText.replace(self._fountainRegex.LESS_THAN_REPLACEMENT, self._fountainRegex.LESS_THAN_PATTERN)
            cleanedText = cleanedText.replace(self._fountainRegex.MORE_THAN_REPLACEMENT, self._fountainRegex.MORE_THAN_PATTERN)
            cleanedText = cleanedText.replace(self._fountainRegex.DOT_DOT_REPLACEMENT, self._fountainRegex.DOT_DOT_PATTERN)
            
            # TODO: strip() strips white space characters by default, though original method was only stripping newline characters
            element = FountainElement(elementTypes[i], cleanedText.strip())
            
            # Deal with scene numbers if we are in a scene heading
            if (elementTypes[i] != self._fountainRegex.SCENE_HEADING_PATTERN):
                sceneMatching = re.search(self._fountainRegex.SCENE_NUMBER_PATTERN, cleanedText)
                # TODO: Index checking
                if sceneMatching:
                    fullSceneNumberText = sceneMatching.group(1)
                    sceneNumber = sceneMatching.group(2)
                    # TODO: if statement checking
                    if sceneNumber:
                        element._sceneNumber = sceneNumber
                        cleanedText = cleanedText.replace(fullSceneNumberText, self._fountainRegex.EMPTY_REPLACEMENT)
            
            # More refined processing of elements based on text/type
            if (re.search(self._fountainRegex.CENTERED_TEXT_PATTERN, element._elementText)):
                element._isCentered = True
                # TODO: index checking; Original code contains stringByTrimmingCharactersInSet:[NSCharacterSet whitespaceCharacterSet]
                element._elementText = re.search(self._fountainRegex.ELEMENT_TEXT_PATTERN, element._elementText).group(2).strip()
            
            if (element._elementType == self._fountainRegex.SCENE_HEADING_PATTERN):
                # TODO: index checking
                element._elementText = re.search(self._fountainRegex.ELEMENT_TEXT_WITH_SCENE_HEADING_PATTERN, element._elementText).group(1)
            
            if (element._elementType == self._fountainRegex.SECTION_HEADING_PATTERN):
                depthChars = re.search(self._fountainRegex.SECTION_HEADER_PATTERN, element._elementText).group(2)
                depth = len(depthChars)
                element._sectionDepth = depth
                element._elementText = re.search(self._fountainRegex.SECTION_HEADER_PATTERN, element._elementText).group(3)
                
            if (i > 1 and element._elementType == self._fountainRegex.CHARACTER_TAG_PATTERN and re.search(self._fountainRegex.DUAL_DIALOGUE_PATTERN, element._elementText)):
                element._isDualDialogue = True
                # clean the ^ mark
                element._elementText = re.sub(self._fountainRegex.CHARACTER_DUAL_DIALOGUE_PATTERN, self._fountainRegex.EMPTY_REPLACEMENT, element._elementText);
                # find the previous character cue
                j = i - 1
                
                # Replacement for original do-while loop
                while True:
                    previousElement = elementsArray[j]
                    
                    if (previousElement._elementType == self._fountainRegex.CHARACTER_TAG_PATTERN):
                        previousElement._isDualDialogue = True
                        previousElement._elementText = re.sub(self._fountainRegex.DUAL_DIALOGUE_ANGLE_MARK_PATTERN, self._fountainRegex.EMPTY_REPLACEMENT, previousElement._elementText)
                        # Note: This differs from the example parser's behavior, too; they don't break here
                        break
                        
                    j -= 1
                    if (j < 0 or (previousElement._elementType != self._fountainRegex.DIALOGUE_TAG_PATTERN and previousElement._elementType != self._fountainRegex.PARENTHETICAL_TAG_PATTERN)):
                        break
            
            elementsArray.append(element)
            
            if __debug__:
                print(element._elementText)
                print(element._elementType + "\n")
        return elementsArray
    
    def parseBodyOfBody(self, scriptContent):
        # Three-pass parsing. 
        # 1st we check for block comments, and manipulate them for regexes
        # 2nd we run regexes against the file to convert it into a marked up format 
        # 3rd we split the marked up elements, and loop through them adding each to 
        #   an our array of FNElements.
        #
        # The intermediate marked up format makes subsequent parsing very simple, 
        # even if it means less efficiency overall.
        
        # 1st pass - Block comments
        # The regexes aren't smart enough (yet) to deal with newlines in the
        # comments, so we need to convert them before processing.
        
        blockComments = re.findall(self._fountainRegex.BLOCK_COMMENT_PATTERN, scriptContent)
        if blockComments:
            for blockComment in blockComments:
                modifiedBlock = blockComment.replace(self._fountainRegex.NEWLINE_DEFAULT, self._fountainRegex.NEWLINE_REPLACEMENT)
                scriptContent = scriptContent.replace(blockComment, modifiedBlock)
        
        bracketComments = re.findall(self._fountainRegex.BRACKET_COMMENT_PATTERN, scriptContent)
        if bracketComments:
            for bracketComment in bracketComments:
                modifiedBlock = bracketComment.replace(self._fountainRegex.NEWLINE_DEFAULT, self._fountainRegex.NEWLINE_REPLACEMENT)
                scriptContent = scriptContent.replace(bracketComment, modifiedBlock)
            
        # Sanitize < and > chars for conversion to the markup
        # TODO: need to make sure &lt and &gt are not special objc characters
        scriptContent = scriptContent.replace(self._fountainRegex.LESS_THAN_PATTERN, self._fountainRegex.LESS_THAN_REPLACEMENT)
        scriptContent = scriptContent.replace(self._fountainRegex.MORE_THAN_PATTERN, self._fountainRegex.MORE_THAN_REPLACEMENT)
        scriptContent = scriptContent.replace(self._fountainRegex.DOT_DOT_PATTERN, self._fountainRegex.DOT_DOT_REPLACEMENT)
        
        # 2nd pass - Script body regex replacement
        
        patterns = self._fountainRegex._patterns
        templates = self._fountainRegex._templates
                     
        # Validate the array counts (protection purposes only)
        if (len(templates) != len(patterns)):
            print('Templates and patterns length mismatch')
            return
        
        if __debug__:
            print(scriptContent)
        
        for i in range(0, len(templates)):
            if __debug__:
                match = re.search(patterns[i], scriptContent)
                print(str(i) + ' ' + patterns[i])
                if match:
                    print('Body: match found for ' + patterns[i] + '\n')
            scriptContent = re.sub(patterns[i], templates[i], scriptContent)
            
        # For debug only: make the intermediate content human readable
        # TODO: Make sure this creates a copy of the string 'scriptContent'
        if __debug__:
            print('*** Parsed body string with elements ***\n')
            debugContent = re.sub(self._fountainRegex.MULTI_NEWLINES_PATTERN, self._fountainRegex.EMPTY_REPLACEMENT, scriptContent)
            debugContent = re.sub(self._fountainRegex.CLOSING_TAG_PATTERN, self._fountainRegex.CLOSING_TAG_REPLACEMENT, debugContent)
            print(debugContent)
            print('\n*** Individual elements from element array ***\n')
        
        # 3rd pass - Array construction
        return self.extractElements(scriptContent)
    
    # File wrappers for body and title parsing
    
    def parseBodyOfFile(self, path):        
        with open(path) as inputFile:
            data = inputFile.read()
            return self.parseBodyOfString(data)
    
    def parseTitlePageOfFile(self, path):
        with open(path) as inputFile:
            data = inputFile.read()
            return self.parseTitlePageOfString(data)
    
    # Shared function for title parsing
    
    def parseTitlePageOfStringBase(self, string):
        pageTitle = self.titlePageOfString(string)
        contents = {}
        
        if not pageTitle:
            return contents
            
        openDirective = ''
        directiveData = []
        
        # Line by line parsing, split the title page with new lines
        lines = pageTitle.split('\n')
        for line in lines:
            # TODO: may want to use match instead of search here
            if re.match(self._fountainRegex.INLINE_DIRECTIVE_PATTERN, line):
                # if there's an open directive with data, save it
                if (openDirective != '' and len(directiveData) > 0):
                    contents[openDirective] = directiveData
                    directiveData = []
                openDirective = ''
                
                key = re.search(self._fountainRegex.INLINE_DIRECTIVE_PATTERN, line).group(1).lower()
                val = re.search(self._fountainRegex.INLINE_DIRECTIVE_PATTERN, line).group(2)
                
                if (key == 'author' or key == 'author(s)'):
                    key = self._fountainRegex.TITLE_AUTHOR_STRING
                
                # TODO: Is 'draft date' in two words a suitable Python key?
                #if (key == self._fountainRegex.TITLE_DRAFT_DATE_STRING):
                #    key = self._fountainRegex.TITLE_DRAFT_DATE_CLASS
                
                # TODO: check if this append is working correctly: here val is string directly converted to array, potentially wrong.
                contents[key] = [val]
            elif re.match(self._fountainRegex.MULTI_LINE_DIRECTIVE_PATTERN, line):
                # if there's an open directive with data, save it
                if (openDirective != '' and len(directiveData) > 0):
                    contents[openDirective] = directiveData
                    
                openDirective = re.match(self._fountainRegex.MULTI_LINE_DIRECTIVE_PATTERN, line).group(1).lower()
                directiveData = []
                
                if (openDirective == 'author' or openDirective == 'author(s)'):
                    openDirective = self._fountainRegex.TITLE_AUTHOR_STRING
            elif re.match(self._fountainRegex.MULTI_LINE_DATA_PATTERN, line):
                directiveData.append(re.match(self._fountainRegex.MULTI_LINE_DATA_PATTERN, line).group(2))
        
        if (openDirective != '' and len(directiveData) > 0):
            contents[openDirective] = directiveData
            
        return contents
    
    # Base function for string parsing.
    # Used by base tag only
    
    def parseBodyOfStringBase(self, string):
        scriptContent = self.bodyOfString(string)
        return self.parseBodyOfBody(scriptContent)
    
    # Script body separation methods: separates a given script to meta and body; 
    # Used by remap parse tag only
    
    def metaOfBody(self, string):
        parts = re.split(self._fountainRegex.SCRIPT_BODY_PATTERN, string, 1)
        if len(parts) > 1:
            return parts[0] + self._fountainRegex.SCRIPT_BODY_ADDON_PATTERN
        return 
    
    def bodyOfBody(self, string):
        parts = re.split(self._fountainRegex.SCRIPT_BODY_PATTERN, string, 1)
        if len(parts) > 1:
            return parts[1]
        else:
            return parts[0]
        return
    
    # Remap functions for script body and meta parsing
    
    def parseBodyOfStringRemap(self, string):
        scriptContent = self.bodyOfString(string)
        # For remap script, before going into body parsing, we separate the script into
        # meta description and body
        scriptMeta = self.metaOfBody(scriptContent)
        scriptBody = self.bodyOfBody(scriptContent)
        
        elementsArray = []
        
        if not (scriptMeta is None):
            metaElements = self.parseMetaOfBody(scriptMeta)
            if not (metaElements is None):
                elementsArray += metaElements
        
        if not (scriptBody is None):
            bodyElements = self.parseBodyOfBody(scriptBody)
            if not (bodyElements is None):
                elementsArray += bodyElements
            
        return elementsArray
    
    def parseMetaOfBody(self, scriptContent):
        # Block comments are not recognized by the meta
        patterns = self._fountainRegex._metaPatterns
        templates = self._fountainRegex._metaTemplates
        
        for i in range(0, len(templates)):
            if __debug__:
                match = re.search(patterns[i], scriptContent)
                print(str(i) + ' ' + patterns[i])
                if match:
                    print('Meta: match found for ' + patterns[i] + '\n')
            scriptContent = re.sub(patterns[i], templates[i], scriptContent)
            
        if __debug__:
            print(scriptContent)
        
        return self.extractElements(scriptContent)
    