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

# This module defines the regex rules, as well as class/tag constants for fountain scripts.
# Fountain syntax reference: http://fountain.io/syntax

import re

# TODO: Considering 'version selection' function from specified in the script
class FountainRegexBase(object):
    def __init__(self):
        # Summary of pattern definition
        self._patterns = [self.UNIVERSAL_LINE_BREAKS_PATTERN, self.BLOCK_COMMENT_PATTERN, 
                self.BRACKET_COMMENT_PATTERN, self.SYNOPSIS_PATTERN, 
                self.PAGE_BREAK_PATTERN, self.FALSE_TRANSITION_PATTERN, 
                self.FORCED_TRANSITION_PATTERN, self.SCENE_HEADER_PATTERN, 
                self.FIRST_LINE_ACTION_PATTERN, self.TRANSITION_PATTERN, 
                self.CHARACTER_CUE_PATTERN, self.PARENTHETICAL_PATTERN, 
                self.DIALOGUE_PATTERN, self.SECTION_HEADER_PATTERN,
                self.ACTION_PATTERN, self.CLEANUP_PATTERN, self.NEWLINE_REPLACEMENT]
    
        # Summary of template definition
        self._templates = [self.UNIVERSAL_LINE_BREAKS_TEMPLATE, self.BLOCK_COMMENT_TEMPLATE, 
                 self.BRACKET_COMMENT_TEMPLATE, self.SYNOPSIS_TEMPLATE, 
                 self.PAGE_BREAK_TEMPLATE, self.FALSE_TRANSITION_TEMPLATE, 
                 self.FORCED_TRANSITION_TEMPLATE, self.SCENE_HEADER_TEMPLATE, 
                 self.FIRST_LINE_ACTION_TEMPLATE, self.TRANSITION_TEMPLATE, 
                 self.CHARACTER_CUE_TEMPLATE, self.PARENTHETICAL_TEMPLATE, 
                 self.DIALOGUE_TEMPLATE, self.SECTION_HEADER_TEMPLATE,
                 self.ACTION_TEMPLATE, self.CLEANUP_TEMPLATE, self.NEWLINE_RESTORE]
        return
    #------------------------------------------------------------------------------
    # Rule string
    
    UNIVERSAL_LINE_BREAKS_PATTERN  = '\\r\\n|\\r|\\n'
    UNIVERSAL_LINE_BREAKS_TEMPLATE = '\n'

    # Note: This is different from the sample, for scenes starting directly with characters and dialogues
    SCENE_HEADER_PATTERN       = '(?<=\\n)(([iI][nN][tT]|[eE][xX][tT]|[^\\w][eE][sS][tT]|\\.|[iI]\\.?\\/[eE]\\.?)([^\\n]+))(?=\\n)'
    ACTION_PATTERN             = '([^<>]*?)(\\n{2}|\\n<)'
    MULTI_LINE_ACTION_PATTERN  = '\n{2}(([^a-z\\n:]+?[\\.\\?,\\s!\\*_]*?)\n{2}){1,2}'
    
    # Note: This is different from the sample, for lines like "STOP IT"
    CHARACTER_CUE_PATTERN      = '(?<=\\n\\n)([ \\t]*[^<>a-z\\s\\/\\n][^<>a-z:!\\?\\n]*[^<>a-z\\(!\\?:,\\n\\.][ \\t]?)\\n(?!\\n)'
    DIALOGUE_PATTERN           = '(<(Character|Parenthetical)>[^<>\\n]+<\\/(Character|Parenthetical)>)([^<>]*?)(?=\\n{2}|\\n{1}<Parenthetical>)'
    # Note: Newline is enforced in order for something to be recognized as parenthetical.
    #       What's the point of a parenthetical, anyway? How is it different from action?
    PARENTHETICAL_PATTERN      = '\\n(\\([^<>]*?\\)[\\s]?)\\n'
    TRANSITION_PATTERN         = '\\n([\\*_]*([^<>\\na-z]*TO:|FADE TO BLACK\\.|FADE OUT\\.|CUT TO BLACK\\.)[\\*_]*)\\n'

    FORCED_TRANSITION_PATTERN  = '\\n((&gt|>)\\s*[^<>\\n]+)\\n'     
    # need to look for &gt pattern because we run this regex against marked up content
    FALSE_TRANSITION_PATTERN   = '\\n((&gt|>)\\s*[^<>\\n]+(&lt\\s*))\\n'     
    # need to look for &gt pattern because we run this regex against marked up content

    PAGE_BREAK_PATTERN         = '(?<=\\n)(\\s*[\\=\\-\\_]{3,8}\\s*)\\n{1}'
    CLEANUP_PATTERN            = '<Action>\\s*<\\/Action>'
    FIRST_LINE_ACTION_PATTERN  = '^\\n\\n([^<>\\n#]*?)\\n'
    SCENE_NUMBER_PATTERN       = '(\\#([0-9A-Za-z\\.\\)-]+)\\#)'
    # Note: In order to make #{something} work in other parts of the script, 
    #       for example, the argument passed 
    SECTION_HEADER_PATTERN     = '((#+)(\\s+[^\\n]*))\\n?'

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
    
    ELEMENT_TEXT_WITH_SCENE_HEADING_PATTERN = '^\\.?(.+)'
    
    CHARACTER_DUAL_DIALOGUE_PATTERN  = '\\s*\\^$'
    DUAL_DIALOGUE_ANGLE_MARK_PATTERN = '^'
        
    # Title parsing replace pattern
    
    TITLE_NOT_NEWLINE_PATTERN     = '^\n+'
    TITLE_NEWLINE_ENDING_PATTERN  = '\n+$'
    
    # Should consider moving this to another class, something like 'fountain elements'
    # Title element names consts
    
    TITLE_TITLE_STRING            = 'title'
    TITLE_AUTHOR_STRING           = 'authors'
    TITLE_SOURCE_STRING           = 'source'
    TITLE_CREDIT_STRING           = 'credit'
    TITLE_DRAFT_DATE_STRING       = 'draft date'
    TITLE_CONTACT_STRING          = 'contact'
    
    # Corresponding div/class ids; 
    # Class IDs are the same as the strings defined above
    
    TITLE_DIV                     = 'script-title'
    TITLE_TITLE_CLASS             = 'title'
    TITLE_AUTHOR_CLASS            = 'authors'
    TITLE_SOURCE_CLASS            = 'source'
    TITLE_CREDIT_CLASS            = 'credit'
    TITLE_DRAFT_DATE_CLASS        = 'draft-date'
    TITLE_CONTACT_CLASS           = 'contact'
    
    # Fountain element names
    
    SCENE_HEADING_PATTERN          = 'Scene Heading'
    # Rendered in html by default
    CHARACTER_TAG_PATTERN          = 'Character'
    DIALOGUE_TAG_PATTERN           = 'Dialogue'
    PARENTHETICAL_TAG_PATTERN      = 'Parenthetical'
    PAGE_BREAK_TAG_PATTERN         = 'Page Break'
    # Ignored in html by default
    BONEYARD_TAG_PATTERN           = 'Boneyard'
    COMMENT_TAG_PATTERN            = 'Comment'
    SYNOPSIS_TAG_PATTERN           = 'Synopsis'
    SECTION_HEADING_PATTERN        = 'Section Heading'
    
    # Fountain element classes
    
    DUAL_DIALOGUE_CLASS            = 'dual-dialogue'
    DUAL_DIALOGUE_LEFT_CLASS       = 'dual-dialogue-left'
    DUAL_DIALOGUE_RIGHT_CLASS      = 'dual-dialogue-right'
    
    SCENE_NUMBER_CLASS             = 'scene-number'
    SCENE_NUMBER_LEFT_CLASS        = 'scene-number-left'
    SCENE_NUMBER_RIGHT_CLASS       = 'scene-number-right'
    
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
    
    # Corresponding HTML styling replacements
    
    BOLD_ITALIC_UNDERLINE_TAG          = r'<strong><em><u>\2</strong></em></u>'
    BOLD_ITALIC_TAG                    = r'<strong><em>\2</strong></em>'
    BOLD_UNDERLINE_TAG                 = r'<strong><u>\2</u></strong>'
    ITALIC_UNDERLINE_TAG               = r'<em><u>\2</em></u>'
    BOLD_TAG                           = r'<strong>\2</strong>'
    ITALIC_TAG                         = r'<em>\2</em>'
    UNDERLINE_TAG                      = r'<u>\2</u>'
    CENTER_CLASS                       = ' center'
    
    # TODO: don't know what this is yet
    FONT_EMPH_IGNORE_TAG               = '\\[{2}(.*?)\\]{2}'
    
# Child class for selecting which version of the parser, as well as defining remap specific tags 
class FountainRegexRemap(FountainRegexBase):
    # Spec name: Web component
    # Spec syntax: <<@componentA[(arg1=val1,arg2=val2...)] text-description>> 
    #              (only appears in Action); componentA: 1st, arg=val,...: 2nd, text-description: third
    # HTML output: <link rel="import" href="components/componentA.html"> <!-- once per file -->
    #              <componentA arg1="val1" arg2="val2">text description</component>
    # Description: Web component pattern from Fountain spec document
    WEB_COMPONENT_PATTERN              = '&lt&lt\\s?@([^<>]*?)\\(([^<>]*)\\)[\\s]?([^<>]*)&gt&gt'
    COMPONENT_ARGUMENTS_PATTERN        = 'CompArg'
    COMPONENT_NAME_PATTERN             = 'CompName'
    COMPONENT_DESCRIPTION_PATTERN      = 'CompDesc'
    COMPONENT_PATTERN                  = 'Component'
    WEB_COMPONENT_TEMPLATE             = r'<' + COMPONENT_PATTERN + '><' + COMPONENT_NAME_PATTERN + r'>\1</' + COMPONENT_NAME_PATTERN + '><' + COMPONENT_ARGUMENTS_PATTERN + r'>\2</' + COMPONENT_ARGUMENTS_PATTERN + r'><' + COMPONENT_DESCRIPTION_PATTERN + r'>\3</' + COMPONENT_DESCRIPTION_PATTERN + r'></' + COMPONENT_PATTERN + '>'
    # TODO: This regex keeps us from nesting the same expressions, like function1(function2(arg)), which (probably) should be allowed
    # Note: right now, we don't do double quotes; This split rule is only used in the generator, which does another pass + generation
    COMPONENT_ARGUMENTS_SPLIT          = '(?:[^,[(\']|\\[[^]]*\\]|\\([^)]*\\)|\'[^\']*\')+'
    
    
    # Spec name: Character header
    # Spec syntax: # Character ... # next part
    # Description: Character header is used specifically to decide characters definition; 
    #              since character was a special type of script meta info, 
    # Note: Currently "# or <>" symbols are not expected in "...".
    META_CHARACTER_HEADER_PATTERN       = r'(#\s?[Cc][Hh][Aa][Rr][Aa][Cc][Tt][Ee][Rr][Ss]?\n)([^#<]+)'
    CHARACTER_CONTENT_PATTERN           = 'CharacterContent'
    META_CHARACTER_HEADER_TEMPLATE      = '<' + CHARACTER_CONTENT_PATTERN + r'>\n\2</' + CHARACTER_CONTENT_PATTERN + '>'
    
    # Spec name: Character type header
    # Spec syntax: # CharacterType ... # next part
    META_CHARACTER_TYPE_HEADER_PATTERN  = r'(#\s?[Cc][Hh][Aa][Rr][Aa][Cc][Tt][Ee][Rr][Tt][Yy][Pp][Ee][Ss]?\n)([^#<]+)'
    CHARACTER_TYPE_CONTENT_PATTERN      = 'CharacterTypeContent'
    META_CHARACTER_TYPE_HEADER_TEMPLATE = '<' + CHARACTER_TYPE_CONTENT_PATTERN + r'>\n\2</' + CHARACTER_TYPE_CONTENT_PATTERN + '>'
    
    # Spec name: Setting header
    # Spec syntax: # Setting ... # next part
    # Description: Setting is a type of meta, which according to Jeff's suggestion, 
    #              should not be applied with td tags in html
    # Note: Currently "# or <>" symbols are not expected in "...".
    META_SETTING_HEADER_PATTERN         = r'(#\s?[Ss][Ee][Tt][Tt][Ii][Nn][Gg][Ss]?)([^#<]+)'
    SETTING_CONTENT_PATTERN             = 'SettingContent'
    META_SETTING_HEADER_TEMPLATE        = '<' + SETTING_CONTENT_PATTERN + r'>\n\2</' + SETTING_CONTENT_PATTERN + '>'
    
    # Spec name: Environment header
    # Spec syntax: # Environment ... # next part
    # Description: Environment is type of javascript metadata, whose definitions can be used by the web components used in the script.
    # Note: Right now the script has some built-in definitions, such as 'include', and 'face', which should be formalized in a more ideal way.
    META_ENVIRONMENT_HEADER_PATTERN     = r'(#\s?[Ee][Nn][Vv][Ii][Rr][Oo][Nn][Mm][Ee][Nn][Tt][Ss]?)([^#<]+)' 
    ENVIRONMENT_CONTENT_PATTERN         = 'EnvironmentContent'
    META_ENVIRONMENT_HEADER_TEMPLATE    = '<' + ENVIRONMENT_CONTENT_PATTERN + r'>\n\2</' + ENVIRONMENT_CONTENT_PATTERN + '>'
    ENVIRONMENT_INCLUDE_PATTERN         = 'include'
    
    # TODO: These should be handled by 'plugins' to this parser
    # NDN specific environment declarations...
    ENVIRONMENT_PREFIX_PATTERN          = 'prefix'
    ENVIRONMENT_FACE_PATTERN            = 'face'
    
    # XMPP specific environment declarations...
    # Note: Right now this pattern should come after all XMPP related definitions are finished
    ENVIRONMENT_XMPP_HTTP_HOST_PATTERN  = 'hostXMPPHttpBind'
    
    # Spec addon: 
    # Spec syntax: (Name + class, such as a character description)Appeared name [class] description \n
    #              (Class, defines a class) [Class name] description \n
    #              (Ordinary, does nothing and gets rendered) Ordinary string with no brackets \n
    # Description: 
    # Note: We don't support multiline character description yet; for a new character, a new line is expected.
    META_NAME_TYPE_PATTERN              = r'([^\[\]\n]+)\s\[([^\[\]\n]+)\]\s([^\n]+)'
    META_TYPE_PATTERN                   = r'\[([^\[\]\n]+)\]\s([^\n]+)'
    META_ORDINARY_PATTERN               = r'\n([^\[\]\n<]+)'
    
    # Spec name: Script body tag
    # Spec syntax: # Body ...
    # Description: Everything after body will be matched against _patterns, and replaced with _templates.
    SCRIPT_BODY_PATTERN                   = '# [Bb][Oo][Dd][Yy]'
    
    
    # TODO: Argument parsing. Right now we don't do nested Component/CompArg definition
    def __init__(self):
        FountainRegexBase.__init__(self)
        # Summary of pattern definition
        self._patterns.append(self.WEB_COMPONENT_PATTERN)
        # Summary of template definition
        self._templates.append(self.WEB_COMPONENT_TEMPLATE)
        
        self._metaPatterns = [self.META_CHARACTER_HEADER_PATTERN, self.META_SETTING_HEADER_PATTERN, 
                              self.META_CHARACTER_TYPE_HEADER_PATTERN, self.META_ENVIRONMENT_HEADER_PATTERN]
        self._metaTemplates = [self.META_CHARACTER_HEADER_TEMPLATE, self.META_SETTING_HEADER_TEMPLATE,
                               self.META_CHARACTER_TYPE_HEADER_TEMPLATE, self.META_ENVIRONMENT_HEADER_TEMPLATE]
        
        return
    