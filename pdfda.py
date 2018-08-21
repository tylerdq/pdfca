import sys
import PyPDF2 as pyp
import os
from collections import defaultdict
#import pandas as pd
import csv

word = str(sys.argv[1])

pdict = {}
#wordvars = [digit, rhetor]
#worddict = dict(zip(words, wordvars))

#file = ('r15d.pdf')
for file in os.listdir(os.getcwd()):
    if file.endswith(".pdf"):
        f = file[:-4]
        pdict[f] = []
        read_pdf = pyp.PdfFileReader(file)
        pnum = read_pdf.getNumPages()

        for p in range(pnum):
            pages = []
            text = read_pdf.getPage(p).extractText().split(" ")
            pages.append(text)

        for page in pages:
            pdict[f].append(sum(word in w for w in page))
#            for k, i in worddict.items():
#                i.append(sum(k in w for w in page))

print(pdict)

#dfvalues = [pnums, digit, rhetor]

#result = dict(zip(head, dfvalues))

#with open('output.csv', mode='w') as outfile:
#    out_writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

#    out_writer.writerow(head)
#    out_writer.writerows(zip(*result.values()))

exit()
