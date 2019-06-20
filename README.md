# pdfca

[![DOI](https://zenodo.org/badge/145485474.svg)](https://zenodo.org/badge/latestdoi/145485474)

pdfca (PDF Content Analysis) can assist with basic textual characterization of a PDF corpus. It provides various commands for managing and interacting with such a corpus through a [Pandas dataframe](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) stored locally as an [Apache Arrow .feather](https://github.com/wesm/feather) binary file, which the user can then pass to other software (including languages such as R) for further analysis.

## Usage
Install [Python 3](https://www.python.org/downloads/). Then [download](https://github.com/tylerdq/pdfca/archive/master.zip) or clone this repository and from the command line (Terminal, PowerShell, cmd, etc.) [`cd`](https://www.git-tower.com/learn/git/ebook/en/command-line/appendix/command-line-101) into the downloaded/cloned directory and run:

`pip3 install -r requirements.txt` (only once per machine)

and then:

`python pdfca.py init` (to initialize an empty .feather binary file for data storage)

For more information on the program and its commands, run:

`python pdfca.py --help` for an overview or use the `--help` flag on any command.

### Preparing Input Files
#### PDFs
When input PDFs have been assembled, place them in the "pdfs" folder of the repository. The names of the files will become identifiers for each file in the dataframe, so ensure that they are as descriptive but short as is feasible (with no duplicate filenames). The program does not edit or overwrite input PDFs, meaning it can be run multiple times on the same set of files.

To be extracted, text in input PDFs must have been processed using [Optical Character Recognition](https://en.wikipedia.org/wiki/Optical_character_recognition) (OCR). A simple test for this is to open a PDF in a reader program (Adobe Reader or similar) and attempt to highlight text on several pages. If the text can be highlighted, the PDF should be ready. OCR can have variable results, and a file that has a low-quality page image or that has been processed using less-capable OCR software may have inaccurately-recognized text. To test this, copy text from multiple pages to a text file and check for errors. pdfca can only search the text it is provided, and the accuracy of its results depends on the quality of the OCR process.

pdfca searches each page in each PDF, meaning that if you requre the text to be linked with *real* page numbers (not the page number of the PDF *file*), you will need to trim your PDFs so they only contain the pages you wish to search. This can be done with Adobe Acrobat or a similar piece of software.

### Managing the dataframe

Run `python pdfca.py extract` any time you want to add PDF text to the dataframe (see notes about adding files below). The command will not extract text from PDFs with filenames that are already present in the database. To re-extract text from certain files, run `python pdfca cut` for each file you wish to remove, then re-run the `extract` command.

*Your terminal may print the following error while parsing PDFs: `PdfReadWarning: Xref table not zero-indexed. ID numbers for objects will be corrected. [pdf.py:1736]`. This is a [known issue](https://github.com/mstamy2/PyPDF2/issues/36) with the dependency PyPDF2 and will likely not impact the search.*

### Notes on stored data
- For analysis beyond the basic `view` and `search` commands, you may use the .feather file with any software or language that supports this format.
- Please note that the Feather format is not yet intended for long-term data storage.
- For more information, explore the [Apache Arrow](https://arrow.apache.org/) documentation. 