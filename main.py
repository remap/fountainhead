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

# main script for debugging

from fountain_script import FountainScript
from html_generator import FountainHTMLGenerator
from fountain_parser import ParserVersion

import sys, getopt

def usage():
    print('main.py -v <parser version tag> -i <inputfile> -c <cssfile: relevant to outputFile path> -o <outputfile> -f <component parent folder name, relevant to outputFile path>')

def main(argv):
    parserVersion = ParserVersion.DEFAULT
    inputFile = 'html-test/remap-script.txt'
    outputFile = 'html-test/debug.html'
    cssFile = 'ScriptCSS.css'
    componentParent = 'components'
    
    try:
        opts, args = getopt.getopt(argv, 'hv:i:c:o:f:', ['version=', 'ifile=', 'cssfile=', 'ofile=', 'compfolder='])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ('-i', '--ifile'):
            inputFile = arg
        elif opt in ('-o', '--ofile'):
            outputFile = arg
        elif opt in ('-v', '--version'):
            parserVersion = arg.lower()
        elif opt in ('-c', '--cfile'):
            cssFile = arg
        elif opt in ('-f', '--compfolder'):
            componentParent = arg
            
    print('fountainhead: Input file is \'' + inputFile + '\'')
    print('fountainhead: Output file is \'' + outputFile + '\'')
    print('fountainhead: CSS file is \'' + cssFile + '\' (relevant to output file path)')
    print('fountainhead: Component html parent folder is \'' + componentParent + '\' (relevant to output file path)')
    
    if parserVersion in ParserVersion.Versions:
        print('fountainhead: Parser version tag is \'' + parserVersion + '\'')
    else:
        print('WARNING: Unknown version tag \'' + parserVersion + '\'; using default version \'' + ParserVersion.DEFAULT + '\' instead')
        parserVersion = ParserVersion.DEFAULT
        
    fountainScript = FountainScript(inputFile, parserVersion)
    fountainHTML = FountainHTMLGenerator(fountainScript, cssFile, componentParent, parserVersion)
    htmlOutput = fountainHTML.generateHtml()
    
    # write html to file
    file = open(outputFile, 'w')
    file.write(htmlOutput)
    
    print('SUCCESS: HTML file written to ' + outputFile)
    
if __name__ == "__main__":
    main(sys.argv[1:])