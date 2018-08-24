import sys, os, PyPDF2, itertools, csv

pdict = {}  # Preallocate empty dict for page contents per PDF
with open(sys.argv[1], 'rt') as input_file:  # Create variable for input file
    words = input_file.read().splitlines()  # Create list with all input words

os.chdir('input')  # Change directory to location of PDFs

print('Looking for PDFs to scrape...')
for file in os.listdir('.'):  # Loop through all files in input folder
    if file.endswith('.pdf'):  # Filter only PDFs
        file_stem = file[:-4]  # Trim extension from filename
        filename = str(file)
        pdict[filename] = {}  # Create empty sub-dict for each file
        read_pdf = PyPDF2.PdfFileReader(file)  # Name reader for current PDF
        pnums = read_pdf.getNumPages()  # Count pages in current PDF
        print('--- ' + str(pnums) + ' pages in ' + str(file))

        for pnum in range(pnums):
            text = read_pdf.getPage(pnum).extractText().strip().lower().split(" ")  # Extract and pre-process text
            pdict[filename][pnum] = text  # Write page text (merge with above?)

os.chdir('../output')  # Change to output directory

output = {}

print('Searching for words to count...')
for filename, contents in pdict.items():
    output[filename] = {}

    for page_number, words_list in contents.items():
        output[filename][page_number] = {}

        for word in words:
            word_stripped = word.strip()
            output[filename][page_number][word_stripped] = sum(word_stripped in sub_word for sub_word in words_list)

text = 'file,page,term,count\n'
for filename in output:
    pageData = output[filename]
    for page in pageData:
        termCount = pageData[page]
        for term in termCount:
            count = termCount[term]
            text += filename + ',' + str(page) + ',' + term + ',' + str(count) + '\n'

f = open('output.csv', 'w')
f.write(text)
f.close()

#print(output)

#for word in words:
#    with open(word + '.csv', mode='wb') as outfile:
#        out_writer = csv.DictWriter(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

#        out_writer.writerow(output.keys())  # Write the header row
#        out_writer.writerows(itertools.zip_longest(*output.values()))

print('Done!')

exit()
