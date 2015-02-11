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
#       As of right now, the remap update will make it unable to work with FountainRegexBase
#       
#       Ideally each version of the parser should be a child class implementing an interface;
#       Though right now they are crammed in this one class;
class Parser(object):
    def __init__(self, version = ParserVersion.DEFAULT):
        self._version = version
        if self._version == ParserVersion.REMAP:
            self.FountainRegex = FountainRegexRemap()
            self.parseBodyOfFile = self.parseBodyOfFileRemap
            self.parseTitlePageOfFile = self.parseTitlePageOfFileRemap
        elif self._version == ParserVersion.BASE:
            self.FountainRegex = FountainRegexBase()
            self.parseBodyOfFile = self.parseBodyOfFileBase
            self.parseTitlePageOfFile = self.parseTitlePageOfFileRemap
        else:
            # Right now using remap as default
            self._version == ParserVersion.DEFAULT
            self.FountainRegex = FountainRegexRemap()
            self.parseBodyOfFile = self.parseBodyOfFileRemap
            self.parseTitlePageOfFile = self.parseTitlePageOfFileRemap
        return
    
    def bodyOfString(self, string):
        body = re.sub(self.FountainRegex.SLASH_N_PATTERN, self.FountainRegex.EMPTY_REPLACEMENT, string)
        
        # Find title page by looking for the first blank line, then checking the
        # text above it. If a title page is found we remove it, leaving only the
        # body content.
        
        firstBlankLine = body.find(self.FountainRegex.DOUBLE_NEWLINES_PATTERN)
        if firstBlankLine > 0:
            # TODO: check if the index is correct
            documentTop = body[:(firstBlankLine + 1)]
            documentTop += self.FountainRegex.NEWLINE_DEFAULT
            
            # check if this is a title page
            if re.search(self.FountainRegex.TITLE_PAGE_PATTERN, documentTop):
                # TODO: check if the index is correct
                body = body[firstBlankLine:]
                
        ret = self.FountainRegex.DOUBLE_NEWLINES_PATTERN + body + self.FountainRegex.DOUBLE_NEWLINES_PATTERN
        return ret
    
    def titlePageOfString(self, string):
        body = re.sub(self.FountainRegex.SLASH_N_PATTERN, self.FountainRegex.EMPTY_REPLACEMENT, string)
        
        # Find title page by looking for the first blank line, then checking the
        # text above it. If a title page is found we remove it, leaving only the
        # body content.
        
        firstBlankLine = body.find(self.FountainRegex.DOUBLE_NEWLINES_PATTERN)
        if firstBlankLine > 0:
            # TODO: check if the index is correct
            documentTop = body[:(firstBlankLine + 1)]
            documentTop += self.FountainRegex.NEWLINE_DEFAULT
            
            # check if this is a title page
            if re.search(self.FountainRegex.TITLE_PAGE_PATTERN, documentTop):
                documentTop = re.sub(self.FountainRegex.TITLE_NEWLINE_ENDING_PATTERN, self.FountainRegex.EMPTY_REPLACEMENT, documentTop)
                documentTop = re.sub(self.FountainRegex.TITLE_NOT_NEWLINE_PATTERN, self.FountainRegex.EMPTY_REPLACEMENT, documentTop)
                return documentTop
        return
            
    def parseBodyOfStringBase(self, string):
        # Three-pass parsing method. 
        # 1st we check for block comments, and manipulate them for regexes
        # 2nd we run regexes against the file to convert it into a marked up format 
        # 3rd we split the marked up elements, and loop through them adding each to 
        #   an our array of FNElements.
        #
        # The intermediate marked up format makes subsequent parsing very simple, 
        # even if it means less efficiency overall.
        #
        
        scriptContent = self.bodyOfString(string)
        
        # 1st pass - Block comments
        # The regexes aren't smart enough (yet) to deal with newlines in the
        # comments, so we need to convert them before processing.
        
        # TODO: this tries to replace '\n' in block comments to '', but does not look smart
        blockComments = re.search(self.FountainRegex.BLOCK_COMMENT_PATTERN, scriptContent)
        if blockComments:
            for blockComment in blockComments:
                modifiedBlock = blockComment.replace(self.FountainRegex.NEWLINE_DEFAULT, self.FountainRegex.NEWLINE_REPLACEMENT)
                scriptContent = scriptContent.replace(blockComment, modifiedBlock)
        
        # TODO: this tries to replace '\n' in bracket comments to '', but does not look smart
        bracketComments = re.search(self.FountainRegex.BRACKET_COMMENT_PATTERN, scriptContent)
        if bracketComments:
            for bracketComment in bracketComments:
                modifiedBlock = bracketComment.replace(self.FountainRegex.NEWLINE_DEFAULT, self.FountainRegex.NEWLINE_REPLACEMENT)
                scriptContent = scriptContent.replace(bracketComment, modifiedBlock)
            
        # Sanitize < and > chars for conversion to the markup
        # TODO: need to make sure &lt and &gt are not special objc characters
        scriptContent = scriptContent.replace(self.FountainRegex.LESS_THAN_PATTERN, self.FountainRegex.LESS_THAN_REPLACEMENT)
        scriptContent = scriptContent.replace(self.FountainRegex.MORE_THAN_PATTERN, self.FountainRegex.MORE_THAN_REPLACEMENT)
        scriptContent = scriptContent.replace(self.FountainRegex.DOT_DOT_PATTERN, self.FountainRegex.DOT_DOT_REPLACEMENT)
        
        # 2nd pass - Regexes
        # Blast the script with regexes. 
        # Make sure pattern and template regexes match up!
        
        patterns = [self.FountainRegex.UNIVERSAL_LINE_BREAKS_PATTERN, self.FountainRegex.BLOCK_COMMENT_PATTERN, 
                    self.FountainRegex.BRACKET_COMMENT_PATTERN, self.FountainRegex.SYNOPSIS_PATTERN, 
                    self.FountainRegex.PAGE_BREAK_PATTERN, self.FountainRegex.FALSE_TRANSITION_PATTERN, 
                    self.FountainRegex.FORCED_TRANSITION_PATTERN, self.FountainRegex.SCENE_HEADER_PATTERN, 
                    self.FountainRegex.FIRST_LINE_ACTION_PATTERN, self.FountainRegex.TRANSITION_PATTERN, 
                    self.FountainRegex.CHARACTER_CUE_PATTERN, self.FountainRegex.PARENTHETICAL_PATTERN, 
                    self.FountainRegex.DIALOGUE_PATTERN, self.FountainRegex.SECTION_HEADER_PATTERN,
                    self.FountainRegex.ACTION_PATTERN, self.FountainRegex.CLEANUP_PATTERN, self.FountainRegex.NEWLINE_REPLACEMENT]
        
        templates = [self.FountainRegex.UNIVERSAL_LINE_BREAKS_TEMPLATE, self.FountainRegex.BLOCK_COMMENT_TEMPLATE, 
                     self.FountainRegex.BRACKET_COMMENT_TEMPLATE, self.FountainRegex.SYNOPSIS_TEMPLATE, 
                     self.FountainRegex.PAGE_BREAK_TEMPLATE, self.FountainRegex.FALSE_TRANSITION_TEMPLATE, 
                     self.FountainRegex.FORCED_TRANSITION_TEMPLATE, self.FountainRegex.SCENE_HEADER_TEMPLATE, 
                     self.FountainRegex.FIRST_LINE_ACTION_TEMPLATE, self.FountainRegex.TRANSITION_TEMPLATE, 
                     self.FountainRegex.CHARACTER_CUE_TEMPLATE, self.FountainRegex.PARENTHETICAL_TEMPLATE, 
                     self.FountainRegex.DIALOGUE_TEMPLATE, self.FountainRegex.SECTION_HEADER_TEMPLATE,
                     self.FountainRegex.ACTION_TEMPLATE, self.FountainRegex.CLEANUP_TEMPLATE, self.FountainRegex.NEWLINE_RESTORE]
                     
        # Validate the array counts (protection purposes only)
        if (len(templates) != len(patterns)):
            print('Templates and patterns length mismatch')
            return
        
        for i in range(0, len(templates)):
            scriptContent = re.sub(patterns[i], templates[i], scriptContent)
        
        # For debug only: make the intermediate content human readable
        # TODO: Make sure this creates a copy of the string 'scriptContent'
        if __debug__:
            print('*** Parsed body string with elements ***\n')
            debugContent = re.sub(self.FountainRegex.MULTI_NEWLINES_PATTERN, self.FountainRegex.EMPTY_REPLACEMENT, scriptContent)
            debugContent = re.sub(self.FountainRegex.CLOSING_TAG_PATTERN, self.FountainRegex.CLOSING_TAG_REPLACEMENT, debugContent)
            print(debugContent)
            print('\n*** Individual elements from element array ***\n')
        
        # 3rd pass - Array construction
        tagMatching = re.findall(self.FountainRegex.TAG_PATTERN, scriptContent)
        if not tagMatching:
            print('Tag patterns does not match scriptContent')
            return
        elementTexts = [temp[1] for temp in tagMatching]
        elementTypes = [temp[0] for temp in tagMatching]
        
        if (len(elementTexts) != len(elementTypes)):
            print('Text and Type counts don\'t match.')
            return
        
        elementsArray = []
        
        for i in range(0, len(elementTypes)):
            # Convert <, > and ... back to normal
            cleanedText = elementTexts[i]
            cleanedText = cleanedText.replace(self.FountainRegex.LESS_THAN_REPLACEMENT, self.FountainRegex.LESS_THAN_PATTERN)
            cleanedText = cleanedText.replace(self.FountainRegex.MORE_THAN_REPLACEMENT, self.FountainRegex.MORE_THAN_PATTERN)
            cleanedText = cleanedText.replace(self.FountainRegex.DOT_DOT_REPLACEMENT, self.FountainRegex.DOT_DOT_PATTERN)
            
            # TODO: strip() strips white space characters by default, though original method was only stripping newline characters
            element = FountainElement(elementTypes[i], cleanedText.strip())
            
            # Deal with scene numbers if we are in a scene heading
            if (elementTypes[i] != self.FountainRegex.SCENE_HEADING_PATTERN):
                sceneMatching = re.search(self.FountainRegex.SCENE_NUMBER_PATTERN, cleanedText)
                # TODO: Index checking
                if sceneMatching:
                    fullSceneNumberText = sceneMatching.group(1)
                    sceneNumber = sceneMatching.group(2)
                    # TODO: if statement checking
                    if sceneNumber:
                        element._sceneNumber = sceneNumber
                        cleanedText = cleanedText.replace(fullSceneNumberText, self.FountainRegex.EMPTY_REPLACEMENT)
            
            # More refined processing of elements based on text/type
            if (re.search(self.FountainRegex.CENTERED_TEXT_PATTERN, element._elementText)):
                element._isCentered = True
                # TODO: index checking; Original code contains stringByTrimmingCharactersInSet:[NSCharacterSet whitespaceCharacterSet]
                element._elementText = re.search(self.FountainRegex.ELEMENT_TEXT_PATTERN, element._elementText).group(2).strip()
            
            if (element._elementType == self.FountainRegex.SCENE_HEADING_PATTERN):
                # TODO: index checking
                element._elementText = re.search(self.FountainRegex.ELEMENT_TEXT_WITH_SCENE_HEADING_PATTERN, element._elementText).group(1)
            
            if (element._elementType == self.FountainRegex.SECTION_HEADING_PATTERN):
                depthChars = re.search(self.FountainRegex.SECTION_HEADER_PATTERN, element._elementText).group(2)
                depth = len(depthChars)
                element._sectionDepth = depth
                element._elementText = re.search(self.FountainRegex.SECTION_HEADER_PATTERN, element._elementText).group(3)
                
            if (i > 1 and element._elementType == self.FountainRegex.CHARACTER_TAG_PATTERN and re.search(self.FountainRegex.DUAL_DIALOGUE_PATTERN, element._elementText)):
                element._isDualDialogue = True
                # clean the ^ mark
                element._elementText = re.replace(self.FountainRegex.CHARACTER_DUAL_DIALOGUE_PATTERN, self.FountainRegex.EMPTY_REPLACEMENT, element._elementText);
                # find the previous character cue
                j = i - 1
                
                # Replacement for original do-while loop
                while True:
                    previousElement = elementsArray[j]
                    if (previousElement._elementType == self.FountainRegex.CHARACTER_TAG_PATTERN):
                        previousElement._isDualDialogue = True
                        previousElement._elementText = re.replace(self.FountainRegex.DUAL_DIALOGUE_ANGLE_MARK_PATTERN, self.FountainRegex.EMPTY_REPLACEMENT, previousElement._elementText)
                    j -= 1
                    if (j < 0 or previousElement._elementType == self.FountainRegex.DIALOGUE_TAG_PATTERN or previousElement._elementType == self.FountainRegex.PARENTHETICAL_TAG_PATTERN):
                        break
            
            elementsArray.append(element)
            
            if __debug__:
                print(element._elementText)
                print(element._elementType + "\n")
        
        return elementsArray
    
    def parseBodyOfStringRemap(self, string):
        # Three-pass parsing method. 
        # 1st we check for block comments, and manipulate them for regexes
        # 2nd we run regexes against the file to convert it into a marked up format 
        # 3rd we split the marked up elements, and loop through them adding each to 
        #   an our array of FNElements.
        #
        # The intermediate marked up format makes subsequent parsing very simple, 
        # even if it means less efficiency overall.
        #
        
        scriptContent = self.bodyOfString(string)
        
        # 1st pass - Block comments
        # The regexes aren't smart enough (yet) to deal with newlines in the
        # comments, so we need to convert them before processing.
        
        # TODO: this tries to replace '\n' in block comments to '', but does not look smart
        blockComments = re.search(self.FountainRegex.BLOCK_COMMENT_PATTERN, scriptContent)
        if blockComments:
            for blockComment in blockComments:
                modifiedBlock = blockComment.replace(self.FountainRegex.NEWLINE_DEFAULT, self.FountainRegex.NEWLINE_REPLACEMENT)
                scriptContent = scriptContent.replace(blockComment, modifiedBlock)
        
        # TODO: this tries to replace '\n' in bracket comments to '', but does not look smart
        bracketComments = re.search(self.FountainRegex.BRACKET_COMMENT_PATTERN, scriptContent)
        if bracketComments:
            for bracketComment in bracketComments:
                modifiedBlock = bracketComment.replace(self.FountainRegex.NEWLINE_DEFAULT, self.FountainRegex.NEWLINE_REPLACEMENT)
                scriptContent = scriptContent.replace(bracketComment, modifiedBlock)
            
        # Sanitize < and > chars for conversion to the markup
        # TODO: need to make sure &lt and &gt are not special objc characters
        scriptContent = scriptContent.replace(self.FountainRegex.LESS_THAN_PATTERN, self.FountainRegex.LESS_THAN_REPLACEMENT)
        scriptContent = scriptContent.replace(self.FountainRegex.MORE_THAN_PATTERN, self.FountainRegex.MORE_THAN_REPLACEMENT)
        scriptContent = scriptContent.replace(self.FountainRegex.DOT_DOT_PATTERN, self.FountainRegex.DOT_DOT_REPLACEMENT)
        
        # 2nd pass - Regexes
        # Blast the script with regexes. 
        # Make sure pattern and template regexes match up!
        
        patterns = [self.FountainRegex.UNIVERSAL_LINE_BREAKS_PATTERN, self.FountainRegex.BLOCK_COMMENT_PATTERN, 
                    self.FountainRegex.BRACKET_COMMENT_PATTERN, self.FountainRegex.SYNOPSIS_PATTERN, 
                    self.FountainRegex.PAGE_BREAK_PATTERN, self.FountainRegex.FALSE_TRANSITION_PATTERN, 
                    self.FountainRegex.FORCED_TRANSITION_PATTERN, self.FountainRegex.SCENE_HEADER_PATTERN, 
                    self.FountainRegex.FIRST_LINE_ACTION_PATTERN, self.FountainRegex.TRANSITION_PATTERN, 
                    self.FountainRegex.CHARACTER_CUE_PATTERN, self.FountainRegex.PARENTHETICAL_PATTERN, 
                    self.FountainRegex.DIALOGUE_PATTERN, self.FountainRegex.SECTION_HEADER_PATTERN,
                    self.FountainRegex.ACTION_PATTERN, self.FountainRegex.CLEANUP_PATTERN, self.FountainRegex.NEWLINE_REPLACEMENT]
        
        templates = [self.FountainRegex.UNIVERSAL_LINE_BREAKS_TEMPLATE, self.FountainRegex.BLOCK_COMMENT_TEMPLATE, 
                     self.FountainRegex.BRACKET_COMMENT_TEMPLATE, self.FountainRegex.SYNOPSIS_TEMPLATE, 
                     self.FountainRegex.PAGE_BREAK_TEMPLATE, self.FountainRegex.FALSE_TRANSITION_TEMPLATE, 
                     self.FountainRegex.FORCED_TRANSITION_TEMPLATE, self.FountainRegex.SCENE_HEADER_TEMPLATE, 
                     self.FountainRegex.FIRST_LINE_ACTION_TEMPLATE, self.FountainRegex.TRANSITION_TEMPLATE, 
                     self.FountainRegex.CHARACTER_CUE_TEMPLATE, self.FountainRegex.PARENTHETICAL_TEMPLATE, 
                     self.FountainRegex.DIALOGUE_TEMPLATE, self.FountainRegex.SECTION_HEADER_TEMPLATE,
                     self.FountainRegex.ACTION_TEMPLATE, self.FountainRegex.CLEANUP_TEMPLATE, self.FountainRegex.NEWLINE_RESTORE]
                     
        # Validate the array counts (protection purposes only)
        if (len(templates) != len(patterns)):
            print('Templates and patterns length mismatch')
            return
        
        for i in range(0, len(templates)):
            scriptContent = re.sub(patterns[i], templates[i], scriptContent)
        
        # For debug only: make the intermediate content human readable
        # TODO: Make sure this creates a copy of the string 'scriptContent'
        if __debug__:
            print('*** Parsed body string with elements ***\n')
            debugContent = re.sub(self.FountainRegex.MULTI_NEWLINES_PATTERN, self.FountainRegex.EMPTY_REPLACEMENT, scriptContent)
            debugContent = re.sub(self.FountainRegex.CLOSING_TAG_PATTERN, self.FountainRegex.CLOSING_TAG_REPLACEMENT, debugContent)
            print(debugContent)
            print('\n*** Individual elements from element array ***\n')
        
        # 3rd pass - Array construction
        tagMatching = re.findall(self.FountainRegex.TAG_PATTERN, scriptContent)
        if not tagMatching:
            print('Tag patterns does not match scriptContent')
            return
        elementTexts = [temp[1] for temp in tagMatching]
        elementTypes = [temp[0] for temp in tagMatching]
        
        if (len(elementTexts) != len(elementTypes)):
            print('Text and Type counts don\'t match.')
            return
        
        elementsArray = []
        
        for i in range(0, len(elementTypes)):
            # Convert <, > and ... back to normal
            cleanedText = elementTexts[i]
            cleanedText = cleanedText.replace(self.FountainRegex.LESS_THAN_REPLACEMENT, self.FountainRegex.LESS_THAN_PATTERN)
            cleanedText = cleanedText.replace(self.FountainRegex.MORE_THAN_REPLACEMENT, self.FountainRegex.MORE_THAN_PATTERN)
            cleanedText = cleanedText.replace(self.FountainRegex.DOT_DOT_REPLACEMENT, self.FountainRegex.DOT_DOT_PATTERN)
            
            # TODO: strip() strips white space characters by default, though original method was only stripping newline characters
            element = FountainElement(elementTypes[i], cleanedText.strip())
            
            # Deal with scene numbers if we are in a scene heading
            if (elementTypes[i] != self.FountainRegex.SCENE_HEADING_PATTERN):
                sceneMatching = re.search(self.FountainRegex.SCENE_NUMBER_PATTERN, cleanedText)
                # TODO: Index checking
                if sceneMatching:
                    fullSceneNumberText = sceneMatching.group(1)
                    sceneNumber = sceneMatching.group(2)
                    # TODO: if statement checking
                    if sceneNumber:
                        element._sceneNumber = sceneNumber
                        cleanedText = cleanedText.replace(fullSceneNumberText, self.FountainRegex.EMPTY_REPLACEMENT)
            
            # More refined processing of elements based on text/type
            if (re.search(self.FountainRegex.CENTERED_TEXT_PATTERN, element._elementText)):
                element._isCentered = True
                # TODO: index checking; Original code contains stringByTrimmingCharactersInSet:[NSCharacterSet whitespaceCharacterSet]
                element._elementText = re.search(self.FountainRegex.ELEMENT_TEXT_PATTERN, element._elementText).group(2).strip()
            
            if (element._elementType == self.FountainRegex.SCENE_HEADING_PATTERN):
                # TODO: index checking
                element._elementText = re.search(self.FountainRegex.ELEMENT_TEXT_WITH_SCENE_HEADING_PATTERN, element._elementText).group(1)
            
            if (element._elementType == self.FountainRegex.SECTION_HEADING_PATTERN):
                depthChars = re.search(self.FountainRegex.SECTION_HEADER_PATTERN, element._elementText).group(2)
                depth = len(depthChars)
                element._sectionDepth = depth
                element._elementText = re.search(self.FountainRegex.SECTION_HEADER_PATTERN, element._elementText).group(3)
                
            if (i > 1 and element._elementType == self.FountainRegex.CHARACTER_TAG_PATTERN and re.search(self.FountainRegex.DUAL_DIALOGUE_PATTERN, element._elementText)):
                element._isDualDialogue = True
                # clean the ^ mark
                element._elementText = re.replace(self.FountainRegex.CHARACTER_DUAL_DIALOGUE_PATTERN, self.FountainRegex.EMPTY_REPLACEMENT, element._elementText);
                # find the previous character cue
                j = i - 1
                
                # Replacement for original do-while loop
                while True:
                    previousElement = elementsArray[j]
                    if (previousElement._elementType == self.FountainRegex.CHARACTER_TAG_PATTERN):
                        previousElement._isDualDialogue = True
                        previousElement._elementText = re.replace(self.FountainRegex.DUAL_DIALOGUE_ANGLE_MARK_PATTERN, self.FountainRegex.EMPTY_REPLACEMENT, previousElement._elementText)
                    j -= 1
                    if (j < 0 or previousElement._elementType == self.FountainRegex.DIALOGUE_TAG_PATTERN or previousElement._elementType == self.FountainRegex.PARENTHETICAL_TAG_PATTERN):
                        break
            
            elementsArray.append(element)
            
            if __debug__:
                print(element._elementText)
                print(element._elementType + "\n")
        
        return elementsArray
    
    def parseBodyOfFileBase(self, path):        
        with open(path) as inputFile:
            data = inputFile.read()
            return self.parseBodyOfStringBase(data)
        
    def parseBodyOfFileRemap(self, path):
        with open(path) as inputFile:
            data = inputFile.read()
            return self.parseBodyOfStringRemap(data)
        
    def parseTitlePageOfStringBase(self, string):
        pageTitle = self.titlePageOfString(string)
        contents = {}
        openDirective = ''
        directiveData = []
        
        # Line by line parsing, split the title page with new lines
        lines = pageTitle.split('\n')
        for line in lines:
            # TODO: may want to use match instead of search here
            if re.match(self.FountainRegex.INLINE_DIRECTIVE_PATTERN, line):
                # if there's an open directive with data, save it
                if (openDirective != '' and len(directiveData) > 0):
                    contents[openDirective] = directiveData
                    directiveData = []
                openDirective = ''
                
                key = re.search(self.FountainRegex.INLINE_DIRECTIVE_PATTERN, line).group(1).lower()
                val = re.search(self.FountainRegex.INLINE_DIRECTIVE_PATTERN, line).group(2)
                
                if (key == 'author' or key == 'author(s)'):
                    key = self.FountainRegex.TITLE_AUTHOR_STRING
                
                # TODO: Is 'draft date' in two words a suitable Python key?
                #if (key == self.FountainRegex.TITLE_DRAFT_DATE_STRING):
                #    key = self.FountainRegex.TITLE_DRAFT_DATE_CLASS
                
                # TODO: check if this append is working correctly: here val is string directly converted to array, potentially wrong.
                contents[key] = [val]
            elif re.match(self.FountainRegex.MULTI_LINE_DIRECTIVE_PATTERN, line):
                # if there's an open directive with data, save it
                if (openDirective != '' and len(directiveData) > 0):
                    contents[openDirective] = directiveData
                    
                openDirective = re.match(self.FountainRegex.MULTI_LINE_DIRECTIVE_PATTERN, line).group(1).lower()
                directiveData = []
                
                if (openDirective == 'author' or openDirective == 'author(s)'):
                    openDirective = self.FountainRegex.TITLE_AUTHOR_STRING
            elif re.match(self.FountainRegex.MULTI_LINE_DATA_PATTERN, line):
                directiveData.append(re.match(self.FountainRegex.MULTI_LINE_DATA_PATTERN, line).group(2))
        
        if (openDirective != '' and len(directiveData) > 0):
            contents[openDirective] = directiveData
            
        return contents
        
    def parseTitlePageOfStringRemap(self, string):
        pageTitle = self.titlePageOfString(string)
        contents = {}
        openDirective = ''
        directiveData = []
        
        # Line by line parsing, split the title page with new lines
        lines = pageTitle.split('\n')
        for line in lines:
            # TODO: may want to use match instead of search here
            if re.match(self.FountainRegex.INLINE_DIRECTIVE_PATTERN, line):
                # if there's an open directive with data, save it
                if (openDirective != '' and len(directiveData) > 0):
                    contents[openDirective] = directiveData
                    directiveData = []
                openDirective = ''
                
                key = re.search(self.FountainRegex.INLINE_DIRECTIVE_PATTERN, line).group(1).lower()
                val = re.search(self.FountainRegex.INLINE_DIRECTIVE_PATTERN, line).group(2)
                
                if (key == 'author' or key == 'author(s)'):
                    key = self.FountainRegex.TITLE_AUTHOR_STRING
                
                # TODO: Is 'draft date' in two words a suitable Python key?
                #if (key == self.FountainRegex.TITLE_DRAFT_DATE_STRING):
                #    key = self.FountainRegex.TITLE_DRAFT_DATE_CLASS
                
                # TODO: check if this append is working correctly: here val is string directly converted to array, potentially wrong.
                contents[key] = [val]
            elif re.match(self.FountainRegex.MULTI_LINE_DIRECTIVE_PATTERN, line):
                # if there's an open directive with data, save it
                if (openDirective != '' and len(directiveData) > 0):
                    contents[openDirective] = directiveData
                    
                openDirective = re.match(self.FountainRegex.MULTI_LINE_DIRECTIVE_PATTERN, line).group(1).lower()
                directiveData = []
                
                if (openDirective == 'author' or openDirective == 'author(s)'):
                    openDirective = self.FountainRegex.TITLE_AUTHOR_STRING
            elif re.match(self.FountainRegex.MULTI_LINE_DATA_PATTERN, line):
                directiveData.append(re.match(self.FountainRegex.MULTI_LINE_DATA_PATTERN, line).group(2))
        
        if (openDirective != '' and len(directiveData) > 0):
            contents[openDirective] = directiveData
            
        return contents
        
    def parseTitlePageOfFileBase(self, path):
        with open(path) as inputFile:
            data = inputFile.read()
            return self.parseTitlePageOfStringBase(data)
            
    def parseTitlePageOfFileRemap(self, path):
        with open(path) as inputFile:
            data = inputFile.read()
            return self.parseTitlePageOfStringRemap(data)