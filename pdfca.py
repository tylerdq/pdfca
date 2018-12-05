import sys, os, PyPDF2, json, itertools, csv, pandas, xlwt

pdict = {}  # Preallocate empty dict for page contents per PDF
output = {}  # Preallocate empty dict for word counts per PDF
with open(sys.argv[1], 'rt') as input_file:  # Create variable for input file
#with open('words.txt', 'rt') as input_file:  # Use standard input filename
    words = input_file.read().splitlines()  # Create list with all input words

print('Extracting PDF contents...')
os.chdir('input')  # Change directory to location of PDFs
for file in os.listdir('.'):  # Iterate through all files in input folder
    if file.endswith('.pdf'):  # Filter only PDFs
        file_stem = file[:-4]  # Trim extension from filename
        filename = str(file_stem)  # NEW THING - CHECK TO SEE IF '.pdf' IS GONE
        pdict[filename] = {}  # Create empty sub-dict for each file
        read_pdf = PyPDF2.PdfFileReader(file)  # Name reader for current PDF
        pnums = read_pdf.getNumPages()  # Count pages in current PDF
        for pnum in range(pnums):  # Iterate through all pages in file
            text = read_pdf.getPage(pnum).extractText().strip().lower().split(" ")  # Extract and pre-process text
            pdict[filename][pnum] = text  # Write page text (merge with above?)
        print(' - Extracted ' + str(pnums) + ' pages from ' + str(file))

print('Counting words...')
os.chdir('../output')  # Change to output directory
for word in words:  # Iterate through words in words list
    word_stripped = word.strip()  # Remove any whitespace from word
    for filename, file_contents in pdict.items():  # Iterate through pdict
        output[filename] = {}
        for page_number, page_contents in file_contents.items():  # Count now
            output[filename][page_number] = sum(word_stripped in sub_word for sub_word in page_contents)
    df = pandas.DataFrame(output)
    df = df.rename(columns=output[filename])
    df.to_csv(word + '.csv', index=False)  # Save individual csv file
    print(' - Saved ' + word + '.csv in Output folder')


def float_if_possible(strg):  # Function to check if cell contents can be converted to a number, and if so does it
    try:
        return float(strg)
    except ValueError:
        return strg  # Keep as string if can't convert to number


if sys.argv[2] == 'ex':  # Excel wrapper subscript
    print('Saving all outputs to Excel file...')
    wb = xlwt.Workbook()
    for filename in os.listdir('.'):  # Iterate through output csv files
        if filename.endswith('.csv'):
            file_stem = filename[:-4]
            sheetname = str(file_stem)
            print('Writing ' + sheetname)
            ws = wb.add_sheet(sheetname)
            csvReader = csv.reader(open(filename, 'r'))
            for rowx, row in enumerate(csvReader):
                for colx, value in enumerate(row):
                    ws.write(rowx, colx, float_if_possible(value))  # Write the values to cells, function writes numbers if possible
    wb.save('output.xls')  # Save wrapped Excel file

print('Done!')
exit()
