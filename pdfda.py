import PyPDF2 as pyp
#import os
#import pandas as pd
import csv

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

with open('output.csv', mode='w') as outfile:
    out_writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    out_writer.writerow(dfkeys)
    for d in result.items():
        out_writer.writerow(d)

file.close()
outfile.close()
exit()

#result = dict(zip(dfkeys, dfvalues))
#df = pd.DataFrame(data=result)
#print(df)
