# Fountainhead

This is a parser for Fountain-formatted scripts that will output "active documents" that incorporate dynamic, code-based elements and are also used for control of the show. 

This work is based on the obj-c fountain parser: https://github.com/nyousefi/Fountain

License: GPLv3

## Usage:
    python -O main.py -v <parser version tag> -i <inputfile> -c <css file: relevant to output file path> -o <output file> -f <component parent folder name, relevant to output file path> -n <include parent folder name, relevant to outputFile path> -s <special generation flag>
    
Flags:
* -v/--version: Parser version tag, supported are 'base' and 'remap'
* -i/--ifile: Fountain input file path
* -o/--ofile: HTML output file path
* -c/--cfile: CSS file path (relative to output file path)
* -f/--compfolder: Component folder path (relative to output file path)
* -n/--incfolder: Include folder path (relative to output file path)
* -s/--special-generation: Special generation flag
* -h/: Print help and exit
    
Please refer to [remap-syntax.md](https://github.com/remap/fountainhead/blob/master/remap-syntax.md) for added syntax for version tag "remap", and added functions for "special generation flag".
    
For a quick test run, please go to the root directory

    cd src
    python -O main.py -s
    
This will overwrite html-test/sample.html with the parser output from html-test/los-atlantis-latest.fountain.

Or run
    
    cd src
    python -O main.py -i ../html-test/your-fountain-file -o ../html-test/your-target-html-output -s

## Contributing:
For guide on scripting your own web components, please refer to [contributing.md](https://github.com/remap/fountainhead/blob/master/contributing.md)

## Links:
Active script: http://the-archive.la/script/fountainhead/html-test/sample.html

(For Firefox, please [enable web components](https://developer.mozilla.org/en-US/docs/Web/Web_Components#Enabling_Web_Components_In_Firefox))

Specification: http://redmine.remap.ucla.edu/projects/fountainhead/documents

Issue tracking: http://redmine.remap.ucla.edu/projects/fountainhead/

Bug report and contact: Zhehao <wangzhehao410305@gmail.com>
