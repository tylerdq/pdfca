# pdfca

[![DOI](https://zenodo.org/badge/145485474.svg)](https://zenodo.org/badge/latestdoi/145485474)

pdfca (PDF Content Analysis) can assist with basic textual characterization of a PDF corpus. It provides various commands for managing and interacting with such a corpus through [Pandas dataframes](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) stored locally via [Apache Arrow .feather](https://github.com/wesm/feather) binaries, which the user can then pass to other software (including languages such as R) for further analysis.

## Installation, setup, and help
Install [Python 3](https://www.python.org/downloads/). Then [download](https://github.com/tylerdq/pdfca/archive/master.zip) or clone this repository and from the command line (Terminal, PowerShell, cmd, etc.) [`cd`](https://www.git-tower.com/learn/git/ebook/en/command-line/appendix/command-line-101) into the downloaded/cloned directory and run:

`pip3 install -r requirements.txt` (only once per machine)

and then:

`python pdfca.py init` (to initialize an empty .feather binary file for data storage)

For more information on the program and its commands, run:

`python pdfca.py --help` for an overview or use the `--help` flag on any command.

## Usage

Run `python pdfca.py extract` to pull text from PDF files (see below notes about preparing data for extraction). The program will not extract text from PDFs that are already listed in the loaded .feather file. To re-extract text from certain files, run `python pdfca cut FILE` for each file to be removed, then re-run the `extract` command.

*The terminal may print the following error while parsing PDFs: `PdfReadWarning: Xref table not zero-indexed. ID numbers for objects will be corrected. [pdf.py:1736]`. This is a [known issue](https://github.com/mstamy2/PyPDF2/issues/36) with the dependency PyPDF2 and will likely not impact the search.*

## Preparing PDFs
Collect PDFs in the desired folder (such as a temporary subfolder of the repository). The names of the files will identify each file in the dataframe, so it's advisable for them to be as descriptive but short as is feasible (with no duplicate filenames). The program does not edit or overwrite input PDFs, meaning it can be run multiple times on the same set of files.

For successful text extraction, input PDFs must have been processed using [Optical Character Recognition](https://en.wikipedia.org/wiki/Optical_character_recognition) (OCR). A simple test for this is to open a PDF in a reader program (Adobe Reader or similar) and attempt to highlight text on several pages. If the text can be highlighted, the PDF should be ready. OCR can have variable results, and a file that has a low-quality page image or that has been processed using less-capable OCR software may have inaccurately-recognized text. To test this, copy text from multiple pages to a text file and check for errors. pdfca can only search the text it is provided, and the accuracy of its results depends on the quality of the OCR process.

pdfca extracts each individual page in each PDF, meaning that for use cases where records must be labelled with *real* page numbers, PDFs may need to be trimmed to the desired page range. This could be done with Adobe Acrobat or a similar piece of software.

## Notes on stored data
- For analysis beyond the basic `view` and `search` commands included, generated data may be imported to any software or language that supports the Feather storage format.
- Please note that the .feather files are not currently designed for long-term data storage.
- For more information, explore the [Apache Arrow](https://arrow.apache.org/) documentation.
