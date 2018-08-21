import PyPDF2 as pyp
#import os
#import pandas

pages,digital,rhetoric = [], [], []
dfkeys = ['p#', 'digital#', 'rhetoric#']
words = ['digi', 'rhet']
wordvars = [digital, rhetoric]
worddict = dict(zip(words, wordvars))

file = ('r15d.pdf')
read_pdf = pyp.PdfFileReader(file)
pnums = read_pdf.getNumPages()

for pnum in range(pnums):
    page = read_pdf.getPage(pnum).extractText().split(" ")
    pages.append(page)
#print(pages[0])

counter = []

for p in pages:
    for k, i in worddict.items():
        i.append(p.count(k))

print(worddict)

#dvalues =

#result = dict(zip(dfkeys, ))

#for word in words:
#    (w, pages.count(w)) for w in set(pages)
#print
