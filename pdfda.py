import sys
import PyPDF2 as pyp
import os
#import pandas as pd
#from collections import defaultdict as dfd
import itertools
import csv

#word = sys.argv[1]
ndict = {}  # Preallocate empty dict for number of pages per PDF
pdict = {}  # Preallocate empty dict for page contents per PDF
cdict = {}  # Preallocate empty dict for term counts per PDF
words = open(sys.argv[1], 'rt')  # Create variable for input file

os.chdir('input')  # Change directory to location of PDFs

#for word in words:
#    word = word.strip()
#    print('Searching for ' + '"' + word + '"' + ' in files...')
print('Looking for PDFs to scrape...')
for file in os.listdir('.'):  # Loop through all files in input folder
    if file.endswith('.pdf'):  # Filter only PDFs
        f = file[:-4]  # Trim extension from filename
        ndict[f] = []  # Create file keys in dict with empty list for each
        pdict[f] = {}  # Create file keys in dict with empty dict for each
        #cdict[f] = []
        read_pdf = pyp.PdfFileReader(file)  # Name reader for current PDF
        ndict[f] = read_pdf.getNumPages()  # Count pages in current PDF
        print('--- ' + str(ndict[f]) + ' pages in ' + str(file))  # Display progress

        for f in ndict.keys():
            for p in range(ndict[f]):  # Loop through pages to extract text
                #pdict[f][p] = []  # Preallocate empty list for page contents
                #text = read_pdf.getPage(p).extractText().lower().split(" ")
                pdict[f][p] = read_pdf.getPage(p).extractText().lower().strip().split(" ")  # Save extracted and split text

print(pdict)

#os.chdir('../output')  # Change directory to where csv will be saved

#print('Searching for words to count...')
#for word in words:  # Loop through words in input file
#    word = word.strip()  # Remove whitespace from words in input file
#    print('--- Counting ' + '"' + word + '"' + '...')
#    for k, v in pdict.items():  # Loop through page contents for each file
#        cdict[k] = []
#        for n, p in v.items():
#            cdict[k].append(sum(word in w for w in p))  # Count now
#        print('--- ' + 'Counted ' + word + ' in ' + k)  # Display progress
#        print(cdict[k])

#    with open('output_' + word + '.csv', mode='w') as outfile:  #
#        out_writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

#        out_writer.writerow(cdict.keys())  # Write the header row
#        out_writer.writerows(itertools.zip_longest(*cdict.values()))

print('Done!')

exit()
