import sys
import PyPDF2 as pyp
import os
#import pandas as pd
import itertools
import csv

word = sys.argv[1]
pdict = {}
os.chdir('input')
for file in os.listdir('.'):
    if file.endswith('.pdf'):
        f = file[:-4]
        pdict[f] = []
        read_pdf = pyp.PdfFileReader(file)
        pnum = read_pdf.getNumPages()

        for p in range(pnum):
            pages = []
            text = read_pdf.getPage(p).extractText().lower().split(" ")
            pages.append(text)
            for page in pages:
                pdict[f].append(sum(word in w for w in page))

os.chdir('../output')

with open('output_' + word + '.csv', mode='w') as outfile:
    out_writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    out_writer.writerow(pdict.keys())
    out_writer.writerows(itertools.zip_longest(*pdict.values()))

exit()
