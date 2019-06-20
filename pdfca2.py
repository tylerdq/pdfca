import os
import json
import glob

import click
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import PyPDF2

cwd = os.getcwd()
columns = ['book', 'page', 'text']
with open('conditions.txt') as cond_file:
    conditions = json.load(cond_file)
wl = conditions.get('whitelist')
ex = conditions.get('extracted')
bl = conditions.get('blacklist')

# df = pd.DataFrame(columns=columns)
table = pq.read_table('books.parquet')
df = table.to_pandas()

os.chdir('C:/Users/tdq11/Dropbox/eBooks/Research PDFs/books/sorted')
files = glob.glob('*.pdf')
for file in files:
    filename = str(file[:-4])
    if filename in wl and filename not in bl and filename not in ex:
        click.echo(f'Extracting text from {filename}...')
        read_pdf = PyPDF2.PdfFileReader(file)
        pages = read_pdf.getNumPages()
        with click.progressbar(range(pages)) as bar:
            for page in bar:  # Iterate through all pages in file
                text = read_pdf.getPage(page).extractText()
                df.loc[len(df)] = [filename, page + 1, text]
        print(f' - Extracted {pages} pages.')

os.chdir(cwd)
# df.to_csv('books.tsv', header=True, sep='\t', index=False)
table = pa.Table.from_pandas(df)
pq.write_table(table, 'books.parquet')
