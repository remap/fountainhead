# -*- Mode:python c-file-style:'gnu' indent-tabs-mode:nil -*- */
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

# This module defines the regex rules for fountain scripts.

import re

class FountainRegex(object):
    #------------------------------------------------------------------------------
    # Rule string
    
    UNIVERSAL_LINE_BREAKS_PATTERN  = '\\r\\n|\\r|\\n'
    UNIVERSAL_LINE_BREAKS_TEMPLATE = '\n'

    SCENE_HEADER_PATTERN       = '(?<=\\n)(([iI][nN][tT]|[eE][xX][tT]|[^\\w][eE][sS][tT]|\\.|[iI]\\.?\\/[eE]\\.?)([^\\n]+))\\n'
    ACTION_PATTERN             = '([^<>]*?)(\\n{2}|\\n<)'
    MULTI_LINE_ACTION_PATTERN  = '\n{2}(([^a-z\\n:]+?[\\.\\?,\\s!\\*_]*?)\n{2}){1,2}'
    CHARACTER_CUE_PATTERN      = '(?<=\\n)([ \\t]*[^<>a-z\\s\\/\\n][^<>a-z:!\\?\\n]*[^<>a-z\\(!\\?:,\\n\\.][ \\t]?)\\n{1}(?!\\n)'
    DIALOGUE_PATTERN           = '(<(Character|Parenthetical)>[^<>\\n]+<\\/(Character|Parenthetical)>)([^<>]*?)(?=\\n{2}|\\n{1}<Parenthetical>)'
    PARENTHETICAL_PATTERN      = '(\\([^<>]*?\\)[\\s]?)\n'
    TRANSITION_PATTERN         = '\\n([\\*_]*([^<>\\na-z]*TO:|FADE TO BLACK\\.|FADE OUT\\.|CUT TO BLACK\\.)[\\*_]*)\\n'

    FORCED_TRANSITION_PATTERN  = '\\n((&gt|>)\\s*[^<>\\n]+)\\n'     
    # need to look for &gt pattern because we run this regex against marked up content
    FALSE_TRANSITION_PATTERN   = '\\n((&gt|>)\\s*[^<>\\n]+(&lt\\s*))\\n'     
    # need to look for &gt pattern because we run this regex against marked up content

    PAGE_BREAK_PATTERN         = '(?<=\\n)(\\s*[\\=\\-\\_]{3,8}\\s*)\\n{1}'
    CLEANUP_PATTERN            = '<Action>\\s*<\\/Action>'
    FIRST_LINE_ACTION_PATTERN  = '^\\n\\n([^<>\\n#]*?)\\n'
    SCENE_NUMBER_PATTERN       = '(\\#([0-9A-Za-z\\.\\)-]+)\\#)'
    SECTION_HEADER_PATTERN     = '((#+)(\\s*[^\\n]*))\\n?'

    # Templates (TODO: Not yet sure if it's the correct usage of 'raw' marker)

    SCENE_HEADER_TEMPLATE      = '\n' + r'<Scene Heading>\1</Scene Heading>'
    ACTION_TEMPLATE            = r'<Action>\1</Action>\2'
    MULTI_LINE_ACTION_TEMPLATE = '\n' + r'<Action>\2</Action>'
    CHARACTER_CUE_TEMPLATE     = r'<Character>\1</Character>'
    DIALOGUE_TEMPLATE          = r'\1<Dialogue>\4</Dialogue>'
    PARENTHETICAL_TEMPLATE     = r'<Parenthetical>\1</Parenthetical>'
    TRANSITION_TEMPLATE        = '\n' + r'<Transition>\1</Transition>'
    FORCED_TRANSITION_TEMPLATE = '\n' + r'<Transition>\1</Transition>'
    FALSE_TRANSITION_TEMPLATE  = '\n' + r'<Action>\1</Action>'
    PAGE_BREAK_TEMPLATE        = '\n<Page Break></Page Break>\n'
    CLEANUP_TEMPLATE           = ''
    FIRST_LINE_ACTION_TEMPLATE = r'<Action>\1</Action>' + '\n'
    SECTION_HEADER_TEMPLATE    = r'<Section Heading>\1</Section Heading>'

    # Block Comments

    BLOCK_COMMENT_PATTERN      = '\\n\\/\\*([^<>]+?)\\*\\/\\n'
    BRACKET_COMMENT_PATTERN    = '\\n\\[{2}([^<>]+?)\\]{2}\\n'

    SYNOPSIS_PATTERN           = '\\n={1}([^<>=][^<>]+?)\\n'     
    # we need to make sure we don't catch ==== as a synopsis

    BLOCK_COMMENT_TEMPLATE     = r'\n<Boneyard>\1</Boneyard>\n'
    BRACKET_COMMENT_TEMPLATE   = r'\n<Comment>\1</Comment>\n'
    SYNOPSIS_TEMPLATE          = r'\n<Synopsis>\1</Synopsis>\n'

    NEWLINE_REPLACEMENT        = '@@@@'
    NEWLINE_RESTORE            = '\n'
    NEWLINE_DEFAULT            = '\n'

    # Title Page

    TITLE_PAGE_PATTERN             = '^([^\\n]+:(([ \\t]*|\\n)[^\\n]+\\n)+)+\\n'
    # TODO: The original line contains \xc2 (/\\s-{circle C}\\*), 
    # not sure how to make python recognize take circle-C(Copyright mark) yet
    INLINE_DIRECTIVE_PATTERN       = '^([\\w\\s&]+):\\s*([^\\s][\\w&,\\.\\?!:\\(\\)\\/\\s\\*\\_]+)$'
    MULTI_LINE_DIRECTIVE_PATTERN   = '^([\\w\\s&]+):\\s*$'
    MULTI_LINE_DATA_PATTERN        = '^([ ]{2,8}|\\t)([^<>]+)$'

    # Misc

    DUAL_DIALOGUE_PATTERN          = '\\^\\s*$'
    CENTERED_TEXT_PATTERN          = '^>[^<>\\n]+<'
    
    # Sanitizing <, >, and ...
    
    LESS_THAN_PATTERN              = '<'
    MORE_THAN_PATTERN              = '>'
    LESS_THAN_REPLACEMENT          = '&lt'
    MORE_THAN_REPLACEMENT          = '&gt'
    DOT_DOT_PATTERN                = '...'
    DOT_DOT_REPLACEMENT            = '::trip::'
    
    # For constructing arrays from tags; added so that constant string does not exist in Parsers
    
    TAG_PATTERN                    = '<([a-zA-Z\\s]+)>([^<>]*)<\\/[a-zA-Z\\s]+>'
    CLOSING_TAG_PATTERN            = '(<\\/[a-zA-Z\\s]+>)'
    CLOSING_TAG_REPLACEMENT        = r'\1' + '\n'
    # TODO: rename this
    MULTI_NEWLINES_PATTERN         = '\\n+'
    EMPTY_REPLACEMENT              = ''
    # TODO: rename this
    SLASH_N_PATTERN                = '^\\n'
    DOUBLE_NEWLINES_PATTERN        = '\n\n'
    ELEMENT_TEXT_PATTERN           = '(>?)\\s*([^<>\\n]*)\\s*(<?)'
    
    SCENE_HEADING_PATTERN          = 'Scene Heading'
    ELEMENT_TEXT_WITH_SCENE_HEADING_PATTERN = '^\\.?(.+)'
        
    SECTION_HEADING_PATTERN        = 'Section Heading'
    
    CHARACTER_TAG_PATTERN          = 'Character'
    CHARACTER_DUAL_DIALOGUE_PATTERN = '\\s*\\^$'
    DIALOGUE_TAG_PATTERN           = 'Dialogue'
    PARENTHETICAL_TAG_PATTERN      = 'Parenthetical'
    DUAL_DIALOGUE_ANGLE_MARK_PATTERN = '^'
        
    # Title parsing replace pattern
    
    TITLE_NOT_NEWLINE_PATTERN     = '^\n+'
    TITLE_NEWLINE_ENDING_PATTERN  = '\n+$'
    
    #------------------------------------------------------------------------------
    # The following regexes aren't used by the code here, but may be useful

    # Styling for FDX

    BOLD_ITALIC_UNDERLINE_PATTERN  = '(_\\*{3}|\\*{3}_)([^<>]+)(_\\*{3}|\\*{3}_)'
    BOLD_ITALIC_PATTERN            = '(\\*{3})([^<>]+)(\\*{3})'
    BOLD_UNDERLINE_PATTERN         = '(_\\*{2}|\\*{2}_)([^<>]+)(_\\*{2}|\\*{2}_)'
    ITALIC_UNDERLINE_PATTERN       = '(_\\*{1}|\\*{1}_)([^<>]+)(_\\*{1}|\\*{1}_)'
    BOLD_PATTERN                   = '(\\*{2})([^<>]+)(\\*{2})'
    ITALIC_PATTERN                 = '(?<!\\\\)(\\*{1})([^<>]+)(\\*{1})'
    UNDERLINE_PATTERN              = '(_)([^<>_]+)(_)'

    # Styling templates

    BOLD_ITALIC_UNDERLINE_TEMPLATE = 'Bold+Italic+Underline'
    BOLD_ITALIC_TEMPLATE           = 'Bold+Italic'
    BOLD_UNDERLINE_TEMPLATE        = 'Bold+Underline'
    ITALIC_UNDERLINE_TEMPLATE      = 'Italic+Underline'
    BOLD_TEMPLATE                  = 'Bold'
    ITALIC_TEMPLATE                = 'Italic'
    UNDERLINE_TEMPLATE             = 'Underline'
    