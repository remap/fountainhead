# fountainhead

This is a parser for Fountain-formatted scripts that will output "active documents" that incorporate dynamic, code-based elements and are also used for control of the show. 

This work is based on the obj-c fountain parser: https://github.com/nyousefi/Fountain

License: GPLv3

## Usage:
    python -O main.py -v <parser version tag> -i <inputfile> -c <css file: relevant to output file path> -o <output file> -f <component parent folder name, relevant to output file path> -n <include parent folder name, relevant to outputFile path>
    
Flags:
* v: Parser version tag, supported are 'base' and 'remap'
* i: Fountain input file path
* o: HTML output file path
* c: CSS file path (relative to output file path)
* f: component folder path (relative to output file path)
* n: include folder path (relative to output file path)
* h: Print help and exit
    
## Links:
Specification: http://redmine.remap.ucla.edu/projects/fountainhead/documents

Issue tracking: http://redmine.remap.ucla.edu/projects/fountainhead/

Bug report and contact: Zhehao <wangzhehao410305@gmail.com>
