# librigilo

A tool for creating a PDF book from a Markdown manuscript

## Installing dependencies (Ubuntu)

        sudo apt-get install pandoc texlive-latex-base texlive-fonts-recommended texlive-lang-spanish unoconv texlive-latex-extra
        sudo pip3 install pypdf2


## Using the tool

Right now the tool is tightly coupled with my spanish novel [Cuarto Poder](https://github.com/moisesjbc/cuarto-poder), so multiple requirements are expected on the directory where the tool is executed.

1. It must contain a *README.md* with the following sections: `## Sinopsis`, `## Licencia` (License), `## Agradecimientos` (acknowledgments).
2. It must contain a *manuscrito* (manuscript) subdirectory containing a file for every chapter. The name of every chapter must start by 'c' (ie. c01_first-chapter).
    - If the chapter file contains links to previous / next chapters and you want them to be removed from the resulting book, those should be placed in a section `## Navegación` (Navigation) at the end of the file.
3. A file *manuscrito/nota-final.md* ("manuscript/end-note") must exist.
4. A file *epub_metadata.txt* must exist with the following structure:

        ---
        title: Cuarto Poder
        author: Moisés J. Bonilla Caraballo
        rights: Reconocimiento-NoComercial-CompartirIgual 4.0 Internacional de Creative Commons
        language: es-ES
        ...

Also because of this big coupling with my novel, the output files will be named as follows:

- build/libro-cuarto-poder.pdf
- build/cuarto-poder.pdf

**I am working** towards making the tool more configurable, but right now I wanted to warn you :).

So, if you still want to use the tool, go to the directory of your novel and simply run

        python3 <path-to-main.py>

## Testing

In order to run unit tests *nosetests* and *pytest* are needed. It can be installed using pip

        sudo apt-get install python3-nose
        pip3 install pytest
        

Run the tests

        nosetests3

