import sys
import PyPDF2 as pyp
import os
#import pandas as pd
import csv

word = sys.argv[1]

pages = []
#pages,digit,rhetor = [], [], []
head = ['p#']
words = ['digit', 'rhetor']
#wordvars = [digit, rhetor]
#worddict = dict(zip(words, wordvars))

#file = ('r15d.pdf')
for file in os.listdir(os.getcwd()):
    if file.endswith(".pdf"):
        head.append(file[:-4])
        read_pdf = pyp.PdfFileReader(file)
        pnum = read_pdf.getNumPages()
        pnums = []
print(head)

#    for p in range(pnum):
#        text = read_pdf.getPage(p).extractText().split(" ")
#        pages.append(text)
#        pnums.append(p+1)
    #print(pages[0])

#    for page in pages:
#        for k, i in worddict.items():
#            i.append(sum(k in w for w in page))

dfvalues = [pnums, digit, rhetor]

result = dict(zip(head, dfvalues))

with open('output.csv', mode='w') as outfile:
    out_writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    out_writer.writerow(head)
    out_writer.writerows(zip(*result.values()))

exit()

#result = dict(zip(head, dfvalues))
#df = pd.DataFrame(data=result)
#print(df)
