import re
import os
import tempfile
from subprocess import call
from PyPDF2 import PdfFileMerger, PdfFileReader
from composed_markdown_file import ComposedMarkdownFile
from book_generators.book_generator import BookGenerator
from glob import glob


class PdfBookGenerator(BookGenerator):
    def generate_chapters(self, page_offset, book_style, chapters_files_regex):
        chapters_markdown_file = ComposedMarkdownFile()
        chapters_markdown_file.append_string('\n\n\\setcounter{page}{%s}\n\n' % page_offset)
        for filepath in sorted(glob(chapters_files_regex)):
            chapters_markdown_file.append_file(filepath, self.process_chapter_markdown)

        (_, monolithic_filepath) = tempfile.mkstemp()
        with open(monolithic_filepath, 'w') as monolithic_file:
            monolithic_file.write(chapters_markdown_file.content())

            pandoc_options = ["-V", "lang=es", "--from", "markdown+hard_line_breaks", "--toc", "--chapters"]
            if book_style == True:
                pandoc_options += ["-V", "documentclass=book"]
            else:
                pandoc_options += ["-V", "documentclass=report"]

            (_, chapters_pdf_filepath) = tempfile.mkstemp()
            chapters_pdf_filepath += '.pdf'
            call(["pandoc"] + pandoc_options + ["--output", chapters_pdf_filepath, monolithic_filepath])

            pdf = PdfFileReader(open(chapters_pdf_filepath,'rb'))

            return (chapters_pdf_filepath, pdf.getNumPages())


    def generate_readme_sections(self, book_style, section_headers):
        (_, temp_filepath) = tempfile.mkstemp()
        (_, readme_sections_pdf_filepath) = tempfile.mkstemp()
        readme_sections_pdf_filepath += '.pdf'

        with open(temp_filepath, 'w') as temp_file:
            temp_file.write('\\pagenumbering{gobble}\n\n') # No page numbers.
            with open('README.md', 'rU') as readme_file:
                copy_line = False
                for line in readme_file:
                    if line.startswith('#'):
                        temp_file.write('\\newpage')
                        if line[:-1] in section_headers:
                            if book_style:
                                temp_file.write('\\mbox{}\n\n\\thispagestyle{empty}\n\n\\newpage\n\n')
                        copy_line = line[:-1] in section_headers

                    if copy_line:
                        if line.startswith('#'):
                            temp_file.write(line[1:]) # Make header top level.
                        else:
                            temp_file.write(line)

            temp_file.write('\\mbox{}\n\n\\thispagestyle{empty}\n\n\\newpage\n\n')

        call(["pandoc"] + ["--from", "markdown-implicit_figures", "--output", readme_sections_pdf_filepath, temp_filepath])

        # Retrieve pages number
        readme_sections_pdf = PdfFileReader(open(readme_sections_pdf_filepath,'rb'))

        return (readme_sections_pdf_filepath, readme_sections_pdf.getNumPages())

    def generate_end_note(self, prologue_filepath, page_offset):
        (_, temp_filepath) = tempfile.mkstemp()
        (_, end_note_pdf_filepath) = tempfile.mkstemp()
        end_note_pdf_filepath += '.pdf'

        with open(temp_filepath, 'w') as temp_file:
            with open(prologue_filepath, 'rU') as src_file:
                temp_file.write('\n\n\\setcounter{page}{%s}\n\n' % page_offset)
                for line in src_file:
                    if line == '## Navegación\n':
                        break
                    temp_file.write(line)

        call(["pandoc"] + ["--output", end_note_pdf_filepath, temp_filepath])

        return end_note_pdf_filepath

    def generate_cover(self):
        (_, cover_pdf_filepath) = tempfile.mkstemp()
        cover_pdf_filepath += '.pdf'

        call(["unoconv"] + ["--output", cover_pdf_filepath, 'portada.odt'])

        return cover_pdf_filepath


    def merge_book_parts(self, part_filepaths, output_filepath):
        pdf_merger = PdfFileMerger()

        for part_filepath in part_filepaths:
            pdf_merger.append(PdfFileReader(open(part_filepath, 'rb')))

        pdf_merger.write(output_filepath)
       
