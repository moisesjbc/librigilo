# librigilo

A tool for creating PDF and/or Epub books from a Markdown manuscript.

## Installing dependencies (Ubuntu)

        sudo apt-get install pandoc texlive-latex-base texlive-fonts-recommended texlive-lang-spanish unoconv texlive-latex-extra
        sudo pip3 install pypdf2


## Using the tool

### Configuration file

**Librigilo needs a JSON configuration file** for generating one or more PDF/Epub books.

        [
            {
                "output-filepath": "book.pdf",
                "book-style": "true",
                "chapters-files": "manuscript/c*",
                "epilogue-files": ["manuscript/end-note.md"],
                "preamble-sections": ["## Sinopsis", "## Licencia", "## Agradecimientos"]
            }
            {
                "output-filepath": "book.pdf",
                "book-style": "false",
            ...
        ]

Parameters:

- `output-filepath`: Path for the generated PDF or Epub book.
- `book-style` (only useful for PDF books): when True, Pandoc is told to generate the book with the "documentclass=book" value. Among other effects, this causes "left" or "right" pages to have a different style.
- `chapters-files`: regular expression specifying the location of the chapters files.
- `epilogue-files`: path to the file to be appended at the end of the book.
- `preamble-sections`: defines a list of sections in the README.md file to be included in the book before the chapters.


### Notes

Right now the tool isn't fully configurable and some conditions must be met in order for it to work properly.

1. Filepaths specified in the configuration file are relative to the path from within librigilo is being run.
2. The sections listed in `preamble-sections` must exist in a *README.md* file. This file must be in the same directory as the configuration file and the one where the tools is being run.
3. If the chapters files contain links to previous / next chapters and you want them to be removed from the resulting book, those should be placed in a section `## Navegación` (Navigation) at the end of the chapter file.
4. (Only for Epub books) A file *epub_metadata.txt* must exist along with configuration file with the following structure:

        ---
        title: Book title
        author: Book author
        rights: Book license
        language: Book language
        ...

**I am working** towards making the tool more configurable, but right now I wanted to warn you :).

### Usage

So, if you still want to use the tool, go to the directory of your novel and simply run

        python3 <path-to-main.py> --config-file <path-to-configuration-file>

## Testing

In order to run unit tests *nosetests* and *pytest* are needed. It can be installed using pip

        sudo apt-get install python3-nose
        pip3 install pytest
        

Run the tests

        nosetests3

