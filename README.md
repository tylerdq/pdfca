# pdfda
pdfda can assist with the early stages of discourse analysis by facilitating the location of a-priori terms across a series of PDF works. It counts the occurrence of one or more terms for each page of every PDF it is given, allowing for rapid identification of not only comparisons of relative term prevalence per work, but where throughout each work every term appears.

## Usage
Install [Python 3](https://www.python.org/downloads/). Then [download](https://github.com/tylerdq/pdfda/archive/master.zip) or clone this repository and from the command line (Terminal, PowerShell, cmd, etc.) [`cd`](https://www.git-tower.com/learn/git/ebook/en/command-line/appendix/command-line-101) into the downloaded/cloned directory and run:

`python pdfda.py <terms_file>`

### Preparing Input Files
#### PDFs
When input PDFs have been assembled, place them in the "Input" folder of the repository. The names of the files will become table headers for term counts, so ensure that the filenames are as descriptive but short as is feasible. The script does not edit or overwrite input PDFs, meaning the script can be run multiple times on the same dataset.

To be searchable, text in input PDFs must have been processed using [Optical Character Recognition](https://en.wikipedia.org/wiki/Optical_character_recognition) (OCR). A simple test for this is to open a PDF in a reader program (Adobe Reader or similar) and attempt to highlight text on several pages. If the text can be highlighted, the PDF should be ready. OCR can have variable results, and a file that has a low-quality page image or that has been processed using less-capable OCR software may have inaccurately-recognized text. To test for this, copy the text from multiple pages to a text file and check for errors. pdfda can only search for the text it is provided, and the accuracy of its results depends on the quality of the OCR process.

pdfda searches each page in each PDF, meaning that if your search must begin with real page numbers (skipping front matter of a book, for example), you will need to trim your PDF file so it only contains the pages you wish to search. This can be done with Adobe Acrobat or another similar piece of software.

#### Search Terms
Search terms can be any piece of text, including complete or partial words. Enter each term on a separate line of a plain-text (.txt) file. A sample file is provided in the base folder of the repository for testing purposes.

### Running the script
`<terms file>` in the script command should be replaced by the actual name of the input file in the base directory of the repository. If using the test file or an updated version of it, type "words.txt" here (without the quotes). Another file can be used if this portion of the command is updated accordingly.

### Processing Output
pdfda produces one output comma-separated values (.csv) file for each search term. These files appear in the "Output" directory once the script has run. These files can be opened in a plain-text editor or spreadsheet software such as Microsoft Excel or Google Sheets. The .csv files do not contain a column for page numbers as the counts are presented sequentially by page (including pages with a count of 0); as such page numbers can easily be added post-hoc by the user if needed.

Sample output files are provided with the respository. These will be overwritten if the script is run again with the same search terms.