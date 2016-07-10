#!/usr/bin/python3

import os

from book_generators.pdf_book_generator import PdfBookGenerator

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
    ]

    if not os.path.isdir('build'):
        os.mkdir('build')

    for configuration in configurations:
        pdf_book_generator = PdfBookGenerator()
        pdf_book_generator.generate_book(configuration)
