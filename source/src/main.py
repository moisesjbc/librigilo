#!/usr/bin/python3

import os

from book_generators.pdf_book_generator import PdfBookGenerator
from book_generators.epub_book_generator import EpubBookGenerator


if __name__ == "__main__":
    configurations = [
        {
            'file_name': 'libro-cuarto-poder.pdf',
            'book_style': True,
            'chapters_directory': 'manuscrito',
            'section_headers': ['## Sinopsis', '## Licencia', '## Agradecimientos']
        },
        {
            'file_name': 'cuarto-poder.pdf',
            'book_style': False,
            'chapters_directory': 'manuscrito',
            'section_headers': ['## Sinopsis', '## Licencia', '## Agradecimientos']
        },
        {
            'file_name': 'libro-cuarto-poder.epub',
            'book_style': True,
            'chapters_directory': 'manuscrito',
            'section_headers': ['## Sinopsis', '## Licencia', '## Agradecimientos']
        }
    ]

    if not os.path.isdir('build'):
        os.mkdir('build')

    for configuration in configurations:
        if configuration['file_name'].endswith('.pdf'):
            book_generator = PdfBookGenerator()
        elif configuration['file_name'].endswith('.epub'):
            book_generator = EpubBookGenerator()
        else
            raise RuntimeError('Output filename must end in .pdf or .epub')

        book_generator.generate_book(configuration)
