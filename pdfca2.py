import os
import json
import glob

import click
import pandas as pd
import PyPDF2

cwd = os.getcwd()
columns = ['book', 'page', 'text']
with open('conditions.txt') as cond_file:
    conditions = json.load(cond_file)
df = pd.DataFrame(columns=columns)

os.chdir('S:/Dropbox/eBooks/Research PDFs/books/sorted')
files = glob.glob('*.pdf')
for file in files:
    filename = str(file[:-4])
    if filename in conditions.get('whitelist'):
        click.echo(f'Extracting text from {filename}...')
        read_pdf = PyPDF2.PdfFileReader(file)
        pages = read_pdf.getNumPages()
        with click.progressbar(range(pages)) as bar:
            for page in bar:  # Iterate through all pages in file
                text = read_pdf.getPage(page).extractText().split()
                df.loc[len(df)] = [filename, page + 1, text]
        print(f' - Extracted {pages} pages.')

os.chdir(cwd)
df.to_csv('books.tsv', header=True, sep='\t', index=False)
