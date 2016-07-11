import re
import os
import tempfile
from subprocess import call
from PyPDF2 import PdfFileMerger, PdfFileReader
from composed_markdown_file import ComposedMarkdownFile
from book_generators.book_generator import BookGenerator


class EpubBookGenerator(BookGenerator):
    def generate_chapters(self, page_offset, book_style, chapters_directory):
        chapters_markdown_file = ComposedMarkdownFile()
        #chapters_markdown_file.append_string('\n\n\\setcounter{page}{%s}\n\n' % page_offset)
        for filename in sorted(os.listdir(chapters_directory)):
            if filename.startswith('c'):
                filepath = os.path.join(chapters_directory, filename)
                chapters_markdown_file.append_file(filepath, self.process_chapter_markdown)

        (_, monolithic_filepath) = tempfile.mkstemp()
        with open(monolithic_filepath, 'w') as monolithic_file:
            monolithic_file.write(chapters_markdown_file.content())

            pandoc_options = ["-t", "epub", "-V", "lang=es", "--from", "markdown+hard_line_breaks", "--toc", "--chapters"]
            if book_style:
                pandoc_options += ["-V", "documentclass=book"]
            else:
                pandoc_options += ["-V", "documentclass=report"]

            (_, chapters_epub_filepath) = tempfile.mkstemp()
            chapters_epub_filepath += '.epub'
            call(["pandoc"] + pandoc_options + ["--output", chapters_epub_filepath, monolithic_filepath])

            # TODO: Return real number of pages.
            return (chapters_epub_filepath, 1)


    def generate_readme_sections(self, book_style, section_headers):
        return ('foo', -1)

    def generate_end_note(self, page_offset):
        return ('foo', 1)

    def generate_cover(self):
        return ('foo', 1)


    def merge_book_parts(self, part_filepaths, output_filepath):
        call(['cp', part_filepaths[2], output_filepath])
