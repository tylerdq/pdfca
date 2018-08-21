import PyPDF2 as pyp
#import os

pages = []

file = ('r15d.pdf')
read_pdf = pyp.PdfFileReader(file)
pnums = read_pdf.getNumPages()

for pnum in range(pnums):
    page = read_pdf.getPage(pnum).extractText().split(" ")
    pages.append(page)
print(pages[0])
