import PyPDF2 as pyp
#import os
#import pandas

pages,digi,rhet = [], [], []
dfkeys = ['p#', 'digital#', 'rhetoric#']
words = ['digi', 'rhet']
wordvars = [digi, rhet]
worddict = dict(zip(words, wordvars))

file = ('r15d.pdf')
read_pdf = pyp.PdfFileReader(file)
pnums = read_pdf.getNumPages()

for pnum in range(pnums):
    text = read_pdf.getPage(pnum).extractText().split(" ")
    pages.append(text)
#print(pages[0])

counter = []

for page in pages:
    for k, i in worddict.items():
        i.append(sum(k in w for w in page))

print(worddict)

#dvalues =

#result = dict(zip(dfkeys, ))

#for word in words:
#    (w, pages.count(w)) for w in set(pages)
#print
