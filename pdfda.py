import sys
import PyPDF2 as pyp
import os
#import pandas as pd
#from collections import defaultdict as dfd
import itertools
import csv

pdict = {}  # Preallocate empty dict for later use
os.chdir('input')  # Change directory to location of PDFs

#word = sys.argv[1]

#words = open(sys.argv[1], 'rt')

#for word in words:
#    word = word.strip()
#    print(word)

for file in os.listdir('.'):  # Loop through all files in input folder
    if file.endswith('.pdf'):  # Filter only PDFs
        f = file[:-4]  # Trim extension from filename
        pdict[f] = {}  # Create file keys in dict with empty list for each
        read_pdf = pyp.PdfFileReader(file)  # Name reader for current PDF
        pnum = read_pdf.getNumPages()  # Count pages in current PDF
        print(str(pnum) + ' pages in ' + str(file))  # Display progress

        for p in range(pnum):  # Loop through pages to extract text
            pages = []  # Preallocate empty list for page contents
            text = read_pdf.getPage(p).extractText().lower().split(" ")
            pages.append(text)  # Save extracted and split text
            for page in pages:  # NOTE - can this loop be merged with above?
                pset = set(page)  # Create a set of all words on page
                for s in pset:  # Loop through unique words in the page
                    pdict[f][s] = []
                    pdict[f][s].append(sum(s in w for w in page))
                #pdict[f].append(sum(word in w for w in page))
        print('Extracted text from ' + str(file)) # Display progress

#os.chdir('../output')  # Change directory to where csv will be saved

#allset =

#for _ in asdf:
#    with open('output_' + s + '.csv', mode='w') as outfile:  #
#        out_writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

#        out_writer.writerow(pdict.keys())  # Write the header row
#        out_writer.writerows(itertools.zip_longest(*pdict[f].values()))

#print('Done!')

exit()
