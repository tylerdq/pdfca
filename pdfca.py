import glob
import os
import re
import sys
from pathlib import Path

import click
import pandas as pd
import pyarrow as pa
import pyarrow.feather as feather
import pyarrow.parquet as pq
import PyPDF2


def count(x, term):
    search = re.findall(term.lower(), x.lower())
    num = len(search)
    return num


def file_spec(func):
    func = click.option('--binary', '-b', default='pdfs',
                        help='Binary filename to operate on.')(func)
    func = click.option('--format', '-f', type=click.Choice(['.feather',
                        '.parquet']), default='.parquet',
                        help='Binary format to use.')(func)
    return func


def load_df(binary):
    """Open local Feather binary for manipulation with pandas"""
    global df
    if binary.endswith('.feather'):
        verify(binary)
        click.secho(f'Loading "{binary}"...', fg='cyan')
        df = feather.read_feather(binary)
    elif binary.endswith('.parquet'):
        verify(binary)
        click.secho(f'Loading "{binary}"...', fg='cyan')
        table = pq.read_table(binary)
        df = table.to_pandas()


def save_df(data_frame, binary):
    """Save dataframe to local Feather binary"""
    os.chdir(sys.path[0])
    if binary.endswith('.feather'):
        click.secho(f'Saving "{binary}"...', fg='cyan')
        feather.write_feather(data_frame, binary)
    elif binary.endswith('.parquet'):
        click.secho(f'Saving "{binary}"...', fg='cyan')
        table = pa.Table.from_pandas(data_frame)
        pq.write_table(table, binary)


def show_page(item):
    if item is not None:
        return '(Page #%d)' % item


def verify(binary):
    try:
        binary = Path(binary).resolve(strict=True)
    except FileNotFoundError:
        click.secho(f'Binary not found! Check name or run "pdfca.py init".',
                    fg='bright_red')
        sys.exit()


@click.group()
@click.version_option(version=click.style('2.0.0', fg='bright_cyan'))
def cli():
    pass


@cli.command()
@click.argument('name')
@file_spec
@click.confirmation_option(prompt=click.style('Really remove records?',
                           fg='bright_yellow'))
def cut(name, binary, format):
    """Remove all dataframe records pertaining to a specific PDF.
    NAME must be a PDF file without its ".pdf" extension.\n
    NOTE: This operation is potentially destructive (use with care)."""
    binary = binary + format
    load_df(binary)
    if df['filename'].str.contains(re.escape(name)).any():
        revised = df[df.filename != name]
        save_df(revised, binary)
    else:
        click.secho('No matching records in dataframe.', fg='bright_red')
    reduction = len(df.index) - len(revised.index)
    click.echo(f'Removed {reduction} lines from dataframe.')


@cli.command()
@click.argument('directory')
@file_spec
def extract(directory, binary, format):
    """Scrape text from pages of files in "input" folder.
    Requires DIRECTORY (whether relative or absolute)."""
    binary = binary + format
    load_df(binary)
    os.chdir(directory)
    pdfs = glob.glob('*.pdf')
    if click.confirm(click.style(f'Ready to get text from {len(pdfs)} ' +
                     'PDFs. Continue?', fg='bright_yellow')):
        total = 0
        for pdf in pdfs:
            exceptions = []
            filename = os.path.splitext(pdf)[0]
            if df['filename'].str.contains(re.escape(filename)).any():
                click.secho(f'{filename} already in dataframe, skipping.',
                            fg='bright_yellow')
            else:
                click.secho(f'Extracting text from {filename}...',
                            fg='bright_magenta')
                read_pdf = PyPDF2.PdfFileReader(pdf)
                pages = read_pdf.getNumPages()
                with click.progressbar(iterable=range(pages),
                                       fill_char='>',
                                       item_show_func=show_page) as bar:
                    for page in bar:
                        try:
                            text = read_pdf.getPage(page).extractText()
                        except:
                            exceptions.append(page)
                            text = ''
                        df.loc[len(df)] = [filename, page + 1, text]
                        total = total + 1
                    print(f'Errors with text on {len(exceptions)} pages.')
            save_df(df, binary)
            os.chdir(directory)
        click.secho(f'Extracted and saved {total} total pages.',
                    fg='bright_green')
    else:
        click.secho('Exiting without extracting text.', fg='bright_red')


@cli.command()
@file_spec
def init(binary, format):
    """Set up empty binary file for storing data.\n
    NOTE: This will delete the existing binary, if any."""
    binary = binary + format
    if os.path.isfile(binary):
        if not click.confirm(click.style('Binary exists! Overwrite?',
                                         fg='bright_red')):
            sys.exit()
    columns = ['filename', 'page', 'text']
    df = pd.DataFrame(columns=columns)
    save_df(df, binary)


@cli.command()
@click.argument('term')
@file_spec
@click.option('--search-type', '-st',
              type=click.Choice(['sum', 'max', 'min', 'mean']),
              help='Specify how to display the search results.')
@click.option('--group', '-g',
              type=click.Choice(['filename', 'page']),
              help='Choose attribute for grouping.')
@click.option('--truncate', '-t', is_flag=True,
              help='View specific number of rows in results.')
def search(term, binary, format, group, search_type, truncate):
    """Search the dataframe for a specific term provided as TERM.
    Default returns a sum of the counts of the term in each PDf.
    All search types return a grouped dataframe sorted by term
    frequencies in ascending order.\n
    NOTE: "min", "max", and "mean" apply on a terms-per-page basis,
    NOT on a terms-per-reference basis."""
    binary = binary + format
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
@file_spec
@click.option('--deep', '-d', is_flag=True,
              help='Show descriptive statistics on a per-reference level.')
def summarize(deep, binary, format):
    """Show table with summary statistics from dataframe.
    By default, summarizes across all references."""
    binary = binary + format
    load_df(binary)
    if deep:
        click.echo(df.groupby(['filename']).describe())
    else:
        click.echo(df.describe())


@cli.command()
@file_spec
def view(binary, format):
    """View dataframe."""
    binary = binary + format
    load_df(binary)
    click.echo(df)


if __name__ == '__main__':
    cli()
