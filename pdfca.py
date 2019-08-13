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
    search = re.findall(term.strip().lower(), x.strip().lower())
    num = len(search)
    return num


def file_spec(func):
    func = click.option('--binary', '-b', default='pdfs',
                        help='Binary filename to operate on.')(func)
    func = click.option('--form', '-f', type=click.Choice(['.feather',
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
        click.secho(f'Binary not found! Check name or run "pdfca init".',
                    fg='bright_red')
        sys.exit()


@click.group()
@click.version_option(version=click.style('2.1.0', fg='bright_cyan'))
def cli():
    pass


@cli.command()
@click.argument('binary')
def convert(binary):
    """Convert binary file to its opposite format (.parquet/.feather). Leaves the original binary intact. Requires BINARY as a complete filename ending in ".parquet" or ".feather".\n
    NOTE: This operation is potentially destructive (use with care)."""
    form = os.path.splitext(binary)[1]
    pref = os.path.splitext(binary)[0]
    binary = pref + form
    load_df(binary)
    if form == '.parquet':
        form = '.feather'
        binary = pref + form
        if os.path.isfile(binary):
            if not click.confirm(click.style('Binary exists! Overwrite?',
                                             fg='bright_red')):
                sys.exit()
        save_df(df, binary)
    elif form == '.feather':
        form = '.parquet'
        binary = pref + form
        if os.path.isfile(binary):
            if not click.confirm(click.style('Binary exists! Overwrite?',
                                             fg='bright_red')):
                sys.exit()
        save_df(df, binary)
    else:
        click.secho('Invalid file extension (must be .feather or .parquet).',
                    fg='bright_red')


@cli.command()
@click.argument('name')
@file_spec
@click.confirmation_option(prompt=click.style('Really remove records?',
                           fg='bright_yellow'))
def cut(name, binary, form):
    """Remove all dataframe records pertaining to a specific PDF.
    NAME must be a PDF file without its ".pdf" extension.\n
    NOTE: This operation is potentially destructive (use with care)."""
    binary = binary + form
    load_df(binary)
    if df['filename'].str.contains(re.escape(name)).any():
        revised = df[df.filename != name]
        save_df(revised, binary)
        reduction = len(df.index) - len(revised.index)
        click.echo(f'Removed {reduction} records from dataframe.')
    else:
        click.secho('No matching records in dataframe.', fg='bright_red')


@cli.command()
@click.argument('directory')
@click.option('--incremental', '-i', is_flag=True,
              help='Save dataframe between each file (safer but slower).')
@click.option('--report', '-r', is_flag=True,
              help='Show status report after export (asks to save as .csv).')
@file_spec
def extract(directory, binary, form, incremental, report):
    """Scrape text from pages of files in "input" folder.
    Requires DIRECTORY (whether relative or absolute).
    Use "./" as DIRECTORY to process files in the current directory."""
    binary = binary + form
    load_df(binary)
    cwd = os.getcwd()
    os.chdir(directory)
    results = {}
    pdfs = glob.glob('*.pdf')
    saved = list(df['filename'].unique())
    for s in saved:
        results[s] = 'Skipped'
        s = s + '.pdf'
        pdfs.remove(s)
    if click.confirm(click.style(f'Ready to get text from {len(pdfs)} ' +
                     'unscraped PDFs. Continue?', fg='bright_yellow')):
        total = 0
        results = pd.DataFrame(columns=['status', 'erpg'], index=pdfs)
        for pdf in pdfs:
            filename = os.path.splitext(pdf)[0]
            results.at[pdf, 'status'] = 'success'
            click.secho(f'Extracting text from {filename}...',
                        fg='bright_magenta')
            read_pdf = PyPDF2.PdfFileReader(pdf)
            try:
                pages = read_pdf.getNumPages()
            except:
                results.at[pdf, 'status'] = 'fail'
                click.secho(f'Error reading file.', fg='bright_yellow')
                continue
            with click.progressbar(iterable=range(pages),
                                   fill_char='>',
                                   item_show_func=show_page) as bar:
                fails = []
                for page in bar:
                    try:
                        text = read_pdf.getPage(page).extractText()
                        df.loc[len(df)] = [filename, page + 1, text]
                        total += 1
                    except:
                        text = ''
                        fails.append(page)
            if fails:
                click.secho(f'{len(fails)} failed pages.', fg='bright_yellow')
                results.at[pdf, 'status'] = 'partial'
                results.at[pdf, 'erpg'] = fails
            if incremental:
                save_df(df, f'{cwd}\\{binary}')
        if not incremental:
            save_df(df, f'{cwd}\\{binary}')
        click.secho(f'Extracted and saved {total} total pages.',
                    fg='bright_green')
        if report:
            results['erpgs'] = results['erpg'].str.len()
            click.echo(f"Results summary:\n{results.describe(include='all')}")
            if click.confirm('Export detailed results to file?'):
                report = click.prompt('Enter name for .csv file to export')
                results.to_csv(f'{cwd}\\{report}.csv', index=True)
    else:
        click.secho('Exiting without extracting text.', fg='bright_red')


@cli.command()
@file_spec
def init(binary, form):
    """Set up empty binary file for storing data.\n
    NOTE: This will delete the existing binary, if any."""
    binary = binary + form
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
def search(term, binary, form, group, search_type, truncate):
    """Search the dataframe for a specific term provided as TERM.
    Default returns a sum of the counts of the term in each PDf.
    All search types return a grouped dataframe sorted by term
    frequencies in ascending order.\n
    NOTE: "min", "max", and "mean" apply on a terms-per-page basis,
    NOT on a terms-per-reference basis."""
    binary = binary + form
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
def summarize(deep, binary, form):
    """Show table with summary statistics from dataframe.
    By default, summarizes across all references."""
    binary = binary + form
    load_df(binary)
    if deep:
        click.echo(df.groupby(['filename']).describe())
    else:
        click.echo(df.describe())


@cli.command()
@file_spec
@click.option('--head', '-h', type=int)
@click.option('--tail', '-t', type=int)
def view(binary, form, head, tail):
    """View dataframe records."""
    binary = binary + form
    load_df(binary)
    if head:
        click.echo(df.head(head))
    elif tail:
        click.echo(df.tail(tail))
    else:
        click.echo(df)


if __name__ == '__main__':
    cli()
