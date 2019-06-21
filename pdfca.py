import glob
import os
import re
import sys
from pathlib import Path

import click
import pandas as pd
import pyarrow.feather as feather
import PyPDF2


def count(x, term):
    search = re.findall(term, x)
    num = len(search)
    return num


def load_df(binary):
    """Open local Feather binary for manipulation with pandas"""
    if not binary.endswith('.feather'):
        binary = f'{binary}.feather'
    binary = Path(binary)
    try:
        binary = binary.resolve(strict=True)
    except FileNotFoundError:
            click.echo('Binary not initialized! Run "pdfca.py init".')
    else:
        global df
        df = feather.read_feather(binary)


def save_df(data_frame, binary):
    """Save dataframe to local Feather binary"""
    os.chdir(sys.path[0])
    if not binary.endswith('.feather'):
        binary = f'{binary}.feather'
    binary = Path(binary)
    feather.write_feather(data_frame, binary)


def show_page(item):
    if item is not None:
        return '(Page #%d)' % item


@click.group()
@click.version_option(version=click.style('1.1.0', fg='bright_cyan'))
def cli():
    pass


@cli.command()
@click.argument('filename')
@click.option('--binary', '-b', default='pdfs',
              help='The name of the .feather file you wish to load.')
@click.confirmation_option(prompt=click.style('Are you sure you want to ' +
                           'remove records?', fg='bright_yellow'))
def cut(filename, binary):
    """Remove all dataframe records pertaining to a specific PDF.
    FILENAME must be the name of the PDF without its ".pdf" extension.\n
    NOTE: This operation is potentially destructive (use with care)."""
    load_df(binary)
    if df['filename'].str.contains(filename).any():
        revised = df[df.filename != filename]
        save_df(revised)
    else:
        click.secho('No matching records in dataframe.', fg='bright_red')


@cli.command()
@click.option('--binary', '-b', default='pdfs',
              help='The name of the .feather file you wish to initialize.')
@click.confirmation_option(prompt=click.style('May delete stored data! ' +
                           'Proceed?', fg='bright_yellow'))
def init(binary):
    """Set up empty .feather binary for storing data.\n
    NOTE: This will delete the existing binary, if any."""
    columns = ['filename', 'page', 'text']
    global df
    df = pd.DataFrame(columns=columns)
    save_df(df, binary)


@cli.command()
@click.argument('directory')
@click.option('--binary', '-b', default='pdfs',
              help='The name of the .feather file you wish to update.')
def extract(directory, binary):
    """Scrape text from pages of files in "input" folder.
    Requires DIRECTORY (whether relative or absolute)."""
    load_df(binary)
    os.chdir(directory)
    pdfs = glob.glob('*.pdf')
    if click.confirm(click.style(f'Ready to get text from {len(pdfs)} ' +
                     'PDFs. Continue?', fg='bright_yellow')):
        total = 0
        for pdf in pdfs:
            filename = os.path.splitext(pdf)[0]
            if df['filename'].str.contains(filename).any():
                click.secho(f'{filename} already in dataframe, skipping.',
                            fg='bright_yellow')
            else:
                click.secho(f'Extracting text from {filename}...', fg='cyan')
                read_pdf = PyPDF2.PdfFileReader(pdf)
                pages = read_pdf.getNumPages()
                # arrow = click.style('>', fg='bright_yellow')
                with click.progressbar(iterable=range(pages),
                                       fill_char='>',
                                       item_show_func=show_page) as bar:
                    for page in bar:
                        text = read_pdf.getPage(page).extractText()
                        df.loc[len(df)] = [filename, page + 1, text]
                        total = total + 1
        save_df(df, binary)
        click.secho(f'Extracted and saved {total} total pages.',
                    fg='bright_green')
    else:
        click.secho('Exiting without extracting text.', fg='bright_red')


@cli.command()
@click.argument('term')
@click.option('--binary', '-b', default='pdfs',
              help='The name of the .feather file you wish to load.')
@click.option('--search-type', '-st',
              type=click.Choice(['sum', 'max', 'min', 'mean']),
              help='Specify how to display the search results.')
@click.option('--group', '-g',
              type=click.Choice(['filename', 'page']),
              help='Choose attribute for grouping.')
@click.option('--truncate', '-t', is_flag=True,
              help='View specific number of rows in results.')
def search(term, binary, group, search_type, truncate):
    """Search the dataframe for a specific term provided as TERM.
    Default returns a sum of the counts of the term in each PDf.
    All search types return a grouped dataframe sorted by term
    frequencies in ascending order.\n
    NOTE: "min", "max", and "mean" apply on a terms-per-page basis,
    NOT on a terms-per-reference basis."""
    load_df(binary)
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
@click.option('--binary', '-b', default='pdfs',
              help='The name of the .feather file you wish to load.')
@click.option('--deep', '-d', is_flag=True,
              help='Show descriptive statistics on a per-reference level.')
def view(deep, binary):
    """View table with summary statistics from dataframe.
    By default, summarizes across all references."""
    load_df(binary)
    if deep:
        click.echo(df.groupby(['filename']).describe())
    else:
        click.echo(df.describe())


if __name__ == '__main__':
    cli()
