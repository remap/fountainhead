import pdfkit

class PdfGenerator(object):
    def __init__(self):
        return 
    
    def run(self, inputFile, outputFile, options=None):
        if (options == None):
            # default rules hard-coded
            options = {
                'page-size': 'Letter',
                'margin-top': '0in',
                'margin-right': '0in',
                'margin-bottom': '0in',
                'margin-left': '0in'
            }
            
        pdfkit.from_url(inputFile, outputFile, options)
        return