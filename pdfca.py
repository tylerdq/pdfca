import glob
import os
import re
import sys

import click
import pandas as pd
import pyarrow.feather as feather
import PyPDF2


def count(x, term):
    search = re.findall(term, x)
    num = len(search)
    return num


def load_df():
    """Open local Feather binary for manipulation with pandas"""
    global df
    df = feather.read_feather('pdfca.feather')


def save_df(data_frame):
    """Save dataframe to local Feather binary"""
    os.chdir(sys.path[0])
    feather.write_feather(df, 'pdfca.feather')


@click.group()
def cli():
    pass


@cli.command()
@click.argument('filename')
@click.confirmation_option(prompt='Are you sure you want to remove records?')
def cut(filename):
    """Remove all records pertaining to a reference from the dataframe.
    FILENAME must be the name of the PDF without its ".pdf" extension.\n
    NOTE: This operation is potentially destructive (use with care)."""
    load_df()
    if df['filename'].str.contains(filename).any():
        revised = df[df.filename != filename]
        save_df(revised)
    else:
        click.echo('No matching records in dataframe.')


@cli.command()
@click.confirmation_option(prompt='Will delete stored data (if any)! Proceed?')
def init():
    """Set up empty Feather binary for storing dataframe.\n
    NOTE: This will delete the existing binary, if any."""
    columns = ['filename', 'page', 'text']
    global df
    df = pd.DataFrame(columns=columns)
    save_df(df)


@cli.command()
# @click.option('--reftype', '-r', default='',
#               help='Specify a BibTeX entry type (book, article, etc.).')
def extract():
    """Scrape text from pages of files in "input" folder."""
    load_df()

    os.chdir('pdfs')
    # os.chdir(sys.path[0] + '\input')
    pdfs = glob.glob('*.pdf')
    if click.confirm(f'Ready to get text from {len(pdfs)} PDFs. Continue?'):
        for pdf in pdfs:
            filename = os.path.splitext(pdf)[0]
            if df['filename'].str.contains(filename).any():
                click.echo(f'{filename} already in dataframe, skipping.')
            else:
                click.echo(f'Extracting text from {filename}...')
                read_pdf = PyPDF2.PdfFileReader(pdf)
                pages = read_pdf.getNumPages()
                with click.progressbar(range(pages)) as bar:
                    for page in bar:
                        text = read_pdf.getPage(page).extractText()
                        df.loc[len(df)] = [filename, page + 1, text]
                print(f' - Extracted {pages} pages.')
        save_df(df)
    else:
        click.echo('Exiting without extracting text.')


@cli.command()
@click.argument('term')
@click.option('--search-type', '-st',
              type=click.Choice(['sum', 'max', 'min', 'mean']),
              help='Specify how to display the search results.')
@click.option('--group', '-g',
              type=click.Choice(['filename', 'page']),
              help='Choose attribute for grouping.')
@click.option('--truncate', '-t', is_flag=True,
              help='View specific number of rows in results.')
# @click.option('--search-level', '-sl',
              # type=click.Choice(['ref', 'page']))
def search(term, group, search_type, truncate):
    """Search the dataframe for a specific term provided as TERM.
    Default returns a sum of the counts of the term in each PDf.
    All search types return a grouped dataframe sorted by term
    frequencies in ascending order.\n
    NOTE: "min", "max", and "mean" apply on a terms-per-page basis,
    NOT on a terms-per-reference basis."""
    load_df()
    df[term] = df['text'].apply(count, term=term)
    if group:
        results = df.drop(['text'], axis=1).groupby([group])
    else:
        results = df.drop(['text'], axis=1).groupby(['filename'])
    if search_type:
        results = getattr(results, search_type)().sort_values(by=[term])
    else:
        results = results.sum().sort_values(by=[term])
    if truncate:
        n = click.prompt('How many records to show?', default=25)
        click.echo(results.tail(n))
    else:
        click.echo(results)


@cli.command()
@click.option('--deep', '-d', is_flag=True,
              help='Show descriptive statistics on a per-reference level.')
def view(deep):
    """View table with summary statistics from dataframe.
    By default, summarizes across all references."""
    load_df()
    if deep:
        click.echo(df.groupby(['filename']).describe())
    else:
        click.echo(df.describe())


if __name__ == '__main__':
    cli()
