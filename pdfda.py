import PyPDF2 as pyp
#import os

pages = []
words = ['digital','rhetoric']

file = ('r15d.pdf')
read_pdf = pyp.PdfFileReader(file)
pnums = read_pdf.getNumPages()

for pnum in range(pnums):
    page = read_pdf.getPage(pnum).extractText().split(" ")
    pages.append(page)
#print(pages[0])

counter = []

for p in pages:
    for word in words:
        counter.append(p.count(word))

print(counter)

#for word in words:
#    (w, pages.count(w)) for w in set(pages)
#print
