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
from regex_rules import FountainRegex
from fountain_element import FountainElement

class Parser(object):
    def __init__(self):
        return
    
    def bodyOfString(self, string):
        body = re.sub(FountainRegex.SLASH_N_PATTERN, FountainRegex.EMPTY_REPLACEMENT, string)
        
        # Find title page by looking for the first blank line, then checking the
        # text above it. If a title page is found we remove it, leaving only the
        # body content.
        
        firstBlankLine = body.find(FountainRegex.DOUBLE_NEWLINES_PATTERN)
        if firstBlankLine > 0:
            # TODO: check if the index is correct
            documentTop = body[:(firstBlankLine + 1)]
            documentTop += FountainRegex.NEWLINE_DEFAULT
            
            # check if this is a title page
            if re.search(FountainRegex.TITLE_PAGE_PATTERN, documentTop):
                # TODO: check if the index is correct
                body = body[firstBlankLine:]
                
        ret = FountainRegex.DOUBLE_NEWLINES_PATTERN + body + FountainRegex.DOUBLE_NEWLINES_PATTERN
        return ret
    
    def titlePageOfString(self, string):
        body = re.sub(FountainRegex.SLASH_N_PATTERN, FountainRegex.EMPTY_REPLACEMENT, string)
        
        # Find title page by looking for the first blank line, then checking the
        # text above it. If a title page is found we remove it, leaving only the
        # body content.
        
        firstBlankLine = body.find(FountainRegex.DOUBLE_NEWLINES_PATTERN)
        if firstBlankLine > 0:
            # TODO: check if the index is correct
            documentTop = body[:(firstBlankLine + 1)]
            documentTop += FountainRegex.NEWLINE_DEFAULT
            
            # check if this is a title page
            if re.search(FountainRegex.TITLE_PAGE_PATTERN, documentTop):
                documentTop = re.sub(FountainRegex.TITLE_NEWLINE_ENDING_PATTERN, FountainRegex.EMPTY_REPLACEMENT, documentTop)
                documentTop = re.sub(FountainRegex.TITLE_NOT_NEWLINE_PATTERN, FountainRegex.EMPTY_REPLACEMENT, documentTop)
                return documentTop
        return
            
    def parseBodyOfString(self, string):
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
        blockComments = re.search(FountainRegex.BLOCK_COMMENT_PATTERN, scriptContent)
        if blockComments:
            for blockComment in blockComments:
                modifiedBlock = blockComment.replace(FountainRegex.NEWLINE_DEFAULT, FountainRegex.NEWLINE_REPLACEMENT)
                scriptContent = scriptContent.replace(blockComment, modifiedBlock)
        
        # TODO: this tries to replace '\n' in bracket comments to '', but does not look smart
        bracketComments = re.search(FountainRegex.BRACKET_COMMENT_PATTERN, scriptContent)
        if bracketComments:
            for bracketComment in bracketComments:
                modifiedBlock = bracketComment.replace(FountainRegex.NEWLINE_DEFAULT, FountainRegex.NEWLINE_REPLACEMENT)
                scriptContent = scriptContent.replace(bracketComment, modifiedBlock)
            
        # Sanitize < and > chars for conversion to the markup
        # TODO: need to make sure &lt and &gt are not special objc characters
        scriptContent = scriptContent.replace(FountainRegex.LESS_THAN_PATTERN, FountainRegex.LESS_THAN_REPLACEMENT)
        scriptContent = scriptContent.replace(FountainRegex.MORE_THAN_PATTERN, FountainRegex.MORE_THAN_REPLACEMENT)
        scriptContent = scriptContent.replace(FountainRegex.DOT_DOT_PATTERN, FountainRegex.DOT_DOT_REPLACEMENT)
        
        # 2nd pass - Regexes
        # Blast the script with regexes. 
        # Make sure pattern and template regexes match up!
        
        patterns = [FountainRegex.UNIVERSAL_LINE_BREAKS_PATTERN, FountainRegex.BLOCK_COMMENT_PATTERN, 
                    FountainRegex.BRACKET_COMMENT_PATTERN, FountainRegex.SYNOPSIS_PATTERN, 
                    FountainRegex.PAGE_BREAK_PATTERN, FountainRegex.FALSE_TRANSITION_PATTERN, 
                    FountainRegex.FORCED_TRANSITION_PATTERN, FountainRegex.SCENE_HEADER_PATTERN, 
                    FountainRegex.FIRST_LINE_ACTION_PATTERN, FountainRegex.TRANSITION_PATTERN, 
                    FountainRegex.CHARACTER_CUE_PATTERN, FountainRegex.PARENTHETICAL_PATTERN, 
                    FountainRegex.DIALOGUE_PATTERN, FountainRegex.SECTION_HEADER_PATTERN,
                    FountainRegex.ACTION_PATTERN, FountainRegex.CLEANUP_PATTERN, FountainRegex.NEWLINE_REPLACEMENT]
        
        templates = [FountainRegex.UNIVERSAL_LINE_BREAKS_TEMPLATE, FountainRegex.BLOCK_COMMENT_TEMPLATE, 
                     FountainRegex.BRACKET_COMMENT_TEMPLATE, FountainRegex.SYNOPSIS_TEMPLATE, 
                     FountainRegex.PAGE_BREAK_TEMPLATE, FountainRegex.FALSE_TRANSITION_TEMPLATE, 
                     FountainRegex.FORCED_TRANSITION_TEMPLATE, FountainRegex.SCENE_HEADER_TEMPLATE, 
                     FountainRegex.FIRST_LINE_ACTION_TEMPLATE, FountainRegex.TRANSITION_TEMPLATE, 
                     FountainRegex.CHARACTER_CUE_TEMPLATE, FountainRegex.PARENTHETICAL_TEMPLATE, 
                     FountainRegex.DIALOGUE_TEMPLATE, FountainRegex.SECTION_HEADER_TEMPLATE,
                     FountainRegex.ACTION_TEMPLATE, FountainRegex.CLEANUP_TEMPLATE, FountainRegex.NEWLINE_RESTORE]
                     
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
            debugContent = re.sub(FountainRegex.MULTI_NEWLINES_PATTERN, FountainRegex.EMPTY_REPLACEMENT, scriptContent)
            debugContent = re.sub(FountainRegex.CLOSING_TAG_PATTERN, FountainRegex.CLOSING_TAG_REPLACEMENT, debugContent)
            print(debugContent)
            print('\n*** Individual elements from element array ***\n')
        
        # 3rd pass - Array construction
        tagMatching = re.findall(FountainRegex.TAG_PATTERN, scriptContent)
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
            cleanedText = cleanedText.replace(FountainRegex.LESS_THAN_REPLACEMENT, FountainRegex.LESS_THAN_PATTERN)
            cleanedText = cleanedText.replace(FountainRegex.MORE_THAN_REPLACEMENT, FountainRegex.MORE_THAN_PATTERN)
            cleanedText = cleanedText.replace(FountainRegex.DOT_DOT_REPLACEMENT, FountainRegex.DOT_DOT_PATTERN)
            
            # TODO: strip() strips white space characters by default, though original method was only stripping newline characters
            element = FountainElement(elementTypes[i], cleanedText.strip())
            
            # Deal with scene numbers if we are in a scene heading
            if (elementTypes[i] != FountainRegex.SCENE_HEADING_PATTERN):
                sceneMatching = re.search(FountainRegex.SCENE_NUMBER_PATTERN, cleanedText)
                # TODO: Index checking
                if sceneMatching:
                    fullSceneNumberText = sceneMatching.group(1)
                    sceneNumber = sceneMatching.group(2)
                    # TODO: if statement checking
                    if sceneNumber:
                        element._sceneNumber = sceneNumber
                        cleanedText = cleanedText.replace(fullSceneNumberText, FountainRegex.EMPTY_REPLACEMENT)
            
            # More refined processing of elements based on text/type
            if (re.search(FountainRegex.CENTERED_TEXT_PATTERN, element._elementText)):
                element._isCentered = True
                # TODO: index checking; Original code contains stringByTrimmingCharactersInSet:[NSCharacterSet whitespaceCharacterSet]
                element._elementText = re.search(FountainRegex.ELEMENT_TEXT_PATTERN, element._elementText).group(2).strip()
            
            if (element._elementType == FountainRegex.SCENE_HEADING_PATTERN):
                # TODO: index checking
                element._elementText = re.search(FountainRegex.ELEMENT_TEXT_WITH_SCENE_HEADING_PATTERN, element._elementText).group(1)
            
            if (element._elementType == FountainRegex.SECTION_HEADING_PATTERN):
                depthChars = re.search(FountainRegex.SECTION_HEADER_PATTERN, element._elementText).group(2)
                depth = len(depthChars)
                element._sectionDepth = depth
                element._elementText = re.search(FountainRegex.SECTION_HEADER_PATTERN, element._elementText).group(3)
                
            if (i > 1 and element._elementType == FountainRegex.CHARACTER_TAG_PATTERN and re.search(FountainRegex.DUAL_DIALOGUE_PATTERN, element._elementText)):
                element._isDualDialogue = True
                # clean the ^ mark
                element._elementText = re.replace(FountainRegex.CHARACTER_DUAL_DIALOGUE_PATTERN, FountainRegex.EMPTY_REPLACEMENT, element._elementText);
                # find the previous character cue
                j = i - 1
                
                # Replacement for original do-while loop
                while True:
                    previousElement = elementsArray[j]
                    if (previousElement._elementType == FountainRegex.CHARACTER_TAG_PATTERN):
                        previousElement._isDualDialogue = True
                        previousElement._elementText = re.replace(FountainRegex.DUAL_DIALOGUE_ANGLE_MARK_PATTERN, FountainRegex.EMPTY_REPLACEMENT, previousElement._elementText)
                    j -= 1
                    if (j < 0 or previousElement._elementType == FountainRegex.DIALOGUE_TAG_PATTERN or previousElement._elementType == FountainRegex.PARENTHETICAL_TAG_PATTERN):
                        break
            
            elementsArray.append(element)
            
            if __debug__:
                print(element._elementText)
                print(element._elementType + "\n")
        
        return elementsArray
        
    def parseBodyOfFile(self, path):        
        with open(path) as inputFile:
            data = inputFile.read()
            return self.parseBodyOfString(data)
        
    def parseTitlePageOfString(self, string):
        pageTitle = self.titlePageOfString(string)
        contents = {}
        openDirective = ''
        directiveData = []
        
        # Line by line parsing, split the title page with new lines
        lines = pageTitle.split('\n')
        for line in lines:
            # TODO: may want to use match instead of search here
            if re.match(FountainRegex.INLINE_DIRECTIVE_PATTERN, line):
                # if there's an open directive with data, save it
                if (openDirective != '' and len(directiveData) > 0):
                    contents[openDirective] = directiveData
                    directiveData = []
                openDirective = ''
                
                key = re.search(FountainRegex.INLINE_DIRECTIVE_PATTERN, line).group(1).lower()
                val = re.search(FountainRegex.INLINE_DIRECTIVE_PATTERN, line).group(2)
                
                if (key == 'author' or key == 'author(s)'):
                    key = FountainRegex.TITLE_AUTHOR_STRING
                
                # TODO: Is 'draft date' in two words a suitable Python key?
                #if (key == FountainRegex.TITLE_DRAFT_DATE_STRING):
                #    key = FountainRegex.TITLE_DRAFT_DATE_CLASS
                
                # TODO: check if this append is working correctly: here val is string directly converted to array, potentially wrong.
                contents[key] = [val]
            elif re.match(FountainRegex.MULTI_LINE_DIRECTIVE_PATTERN, line):
                # if there's an open directive with data, save it
                if (openDirective != '' and len(directiveData) > 0):
                    contents[openDirective] = directiveData
                    
                openDirective = re.match(FountainRegex.MULTI_LINE_DIRECTIVE_PATTERN, line).group(1).lower()
                directiveData = []
                
                if (openDirective == 'author' or openDirective == 'author(s)'):
                    openDirective = FountainRegex.TITLE_AUTHOR_STRING
            elif re.match(FountainRegex.MULTI_LINE_DATA_PATTERN, line):
                directiveData.append(re.match(FountainRegex.MULTI_LINE_DATA_PATTERN, line).group(2))
        
        if (openDirective != '' and len(directiveData) > 0):
            contents[openDirective] = directiveData
            
        return contents
        
    def parseTitlePageOfFile(self, path):
        with open(path) as inputFile:
            data = inputFile.read()
            return self.parseTitlePageOfString(data)