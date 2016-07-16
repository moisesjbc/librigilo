#!/usr/bin/python3

import os
import argparse
import sys

from book_generators.pdf_book_generator import PdfBookGenerator
from book_generators.epub_book_generator import EpubBookGenerator
from configuration import Configuration


if __name__ == "__main__":   
    parser = \
        argparse.ArgumentParser(description='Turns a Markdown book into a PDF and/or Epub one')
    parser.add_argument(
        '--config-file', 
        dest='config_filepath', action='store',
        help='Configuration file')
    args = parser.parse_args()

    if args.config_filepath is None:
        print("ERROR: expected --config-file")
        sys.exit(1)

    configurations = \
        Configuration.load_configurations_from_json_file(args.config_filepath)

    for configuration in configurations:
        if configuration.OUTPUT_FILEPATH.endswith('.pdf'):
            book_generator = PdfBookGenerator()
        elif configuration.OUTPUT_FILEPATH.endswith('.epub'):
            book_generator = EpubBookGenerator()
        else:
            raise RuntimeError('Output filename must end in .pdf or .epub')

        book_generator.generate_book(configuration)

    sys.exit(0)
