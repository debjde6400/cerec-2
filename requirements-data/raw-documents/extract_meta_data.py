import glob
from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
#from pdfminer.high_level import extract_text

def getNumLines(fileName):
    output_string = StringIO()
    with open(fileName, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        numPages = 0
        for pageNumber, page in enumerate(PDFPage.create_pages(doc)):
            numPages = numPages + 1
    return numPages


metaDataFileName = "pages.txt"
maxNumPages = 0
minNumPages = 10000000
averageNumPages = 0
reqFileNames = glob.glob("*.pdf") # get all pdf files

with open(metaDataFileName, "w") as metaFile:
    for fileName in reqFileNames:
        numPages = getNumLines(fileName) # process file
        maxNumPages = max(maxNumPages, numPages)
        minNumPages = min(minNumPages, numPages)
        averageNumPages = averageNumPages + numPages
        print("Done with " + fileName)
        metaFile.write(fileName + ": " + str(numPages) + "\n")
    metaFile.write("--------\n")
    metaFile.write("Max Pages: " + str(maxNumPages) + "\n")
    metaFile.write("Min Pages: " + str(minNumPages) + "\n")
    metaFile.write("Average: " + str((averageNumPages / len(reqFileNames))))

print("-> max num pages: " + str(maxNumPages))
print("-> min num pages: " + str(minNumPages))
print("-> average num pages: " + str((averageNumPages / len(reqFileNames))))
