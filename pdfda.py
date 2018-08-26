import sys, os, PyPDF2, json, itertools, csv, pandas

pdict = {}  # Preallocate empty dict for page contents per PDF
output = {}  # Preallocate empty dict for word counts per PDF
with open(sys.argv[1], 'rt') as input_file:  # Create variable for input file
    words = input_file.read().splitlines()  # Create list with all input words

os.chdir('input')  # Change directory to location of PDFs

print('Extracting PDF contents...')
for file in os.listdir('.'):  # Loop through all files in input folder
    if file.endswith('.pdf'):  # Filter only PDFs
        file_stem = file[:-4]  # Trim extension from filename
        filename = str(file)
        pdict[filename] = {}  # Create empty sub-dict for each file
        read_pdf = PyPDF2.PdfFileReader(file)  # Name reader for current PDF
        pnums = read_pdf.getNumPages()  # Count pages in current PDF

        for pnum in range(pnums):
            text = read_pdf.getPage(pnum).extractText().strip().lower().split(" ")  # Extract and pre-process text
            pdict[filename][pnum] = text  # Write page text (merge with above?)
        print(' - Extracted ' + str(pnums) + ' pages from ' + str(file))

os.chdir('../output')  # Change to output directory

print('Counting words per page...')

for word in words:
    word_stripped = word.strip()

    for filename, file_contents in pdict.items():
        output[filename] = {}

        for page_number, page_contents in file_contents.items():
            output[filename][page_number] = sum(word_stripped in sub_word for sub_word in page_contents)

    df = pandas.DataFrame(output)

    df = df.rename(columns=output[filename])

    df.to_csv(word + '.csv', index=False)

#    text = 'file,\n'
#    for filename in output:
#        pageData = output[filename]
#        for page in pageData:
#            termCount = pageData[page]
#            for term in termCount:
#                count = termCount[term]
#                text += filename + ',' + str(page) + ',' + term + ',' + str(count) + '\n'

#    f = open(word + '.csv', 'w')
#    f.write(text)
#    f.close()

#print(output)

#    with open(word + '.csv', mode='wb') as outfile:
#        out_writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

#        out_writer.writerow(output.keys())  # Write the header row
#        out_writer.writerows(itertools.zip_longest(*output.values()))

print('Saving output...')

print('Done!')

exit()
