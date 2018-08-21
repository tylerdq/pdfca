import PyPDF2 as pyp
#import os
import pandas as pd

pages,digi,rhet = [], [], []
dfkeys = ['p#', 'digital#', 'rhetoric#']
words = ['digi', 'rhet']
wordvars = [digi, rhet]
worddict = dict(zip(words, wordvars))

file = ('r15d.pdf')
read_pdf = pyp.PdfFileReader(file)
pnum = read_pdf.getNumPages()
pnums = []

for p in range(pnum):
    text = read_pdf.getPage(p).extractText().split(" ")
    pages.append(text)
    pnums.append(p+1)
#print(pages[0])

for page in pages:
    for k, i in worddict.items():
        i.append(sum(k in w for w in page))

dfvalues = [pnums, digi, rhet]

result = dict(zip(dfkeys, dfvalues))
df = pd.DataFrame(data=result)
print(df)

#for word in words:
#    (w, pages.count(w)) for w in set(pages)
#print
