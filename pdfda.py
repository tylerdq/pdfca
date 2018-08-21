import PyPDF2 as pyp
#import os
#import pandas as pd
import csv

pages,digit,rhetor = [], [], []
dfkeys = ['p#', 'digit#', 'rhetor#']
words = ['digit', 'rhetor']
wordvars = [digit, rhetor]
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

dfvalues = [pnums, digit, rhetor]

result = dict(zip(dfkeys, dfvalues))

with open('output.csv', mode='w') as outfile:
    out_writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    out_writer.writerow(dfkeys)
    out_writer.writerows(zip(*result.values()))

exit()

#result = dict(zip(dfkeys, dfvalues))
#df = pd.DataFrame(data=result)
#print(df)
