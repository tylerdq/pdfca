import sys, os, PyPDF2, re, json

contents = []  # Preallocate empty dict for page contents per PDF

os.chdir('input')  # Change directory to location of PDFs
file = str(sys.argv[1])
read_pdf = PyPDF2.PdfFileReader(file)  # Name reader for current PDF
pnums = read_pdf.getNumPages()  # Count pages in current PDF
for pnum in range(pnums):  # Iterate through all pages in file
    text = read_pdf.getPage(pnum).extractText()  # Extract text
    textLower = text.lower()
    textStrip = textLower.strip()
    textSplit = re.split('; |, |\*|\n.', textStrip)
    textSplit = textStrip.split()
#    textStrip = text.strip('\n')
    contents.extend(textSplit)  # Write page text (merge with above?)
print(' - Extracted ' + str(pnums) + ' pages from ' + str(file))

[i.strip() for i in contents]

contentSet = set()
for item in contents:
    contentSet.add(item)

sortSet = sorted(contentSet)

print(sortSet)

#os.chdir('../output')  # Change to output directory
#with open
