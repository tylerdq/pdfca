import PyPDF2 as pyp
import glob

pdfs = []
pnums = []
for filename in glob.glob("*.pdf"):
    with open(filename, 'rb') as f:
        pdfs.append(f)
        pdfReader = pyp.PdfFileReader(f)
        pnums.append(pdfReader.getNumPages)
#for f in pdfs:
#    pdfFileObj = open(filename, 'rb')
#    pdfReader = pyp.PdfFileReader(pdfFileObj)
#    pnums.append(pdfFileObj.getNumPages)

print(pnums)

#for pnum in range(pnums):   # use xrange in Py2
#    page = read_pdf.getPage(page_number).extractText().split(" ")  # Extract page wise text then split based on spaces as required by you
#    pages.append(page)
#print(pages[0])
