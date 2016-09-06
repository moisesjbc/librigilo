import re
import os
import tempfile
from subprocess import call
from PyPDF2 import PdfFileMerger, PdfFileReader
from composed_markdown_file import ComposedMarkdownFile
from book_generators.book_generator import BookGenerator
from glob import glob


class PdfBookGenerator(BookGenerator):
    def process_chapter_markdown(self, markdown_content):
        # Remove number from chapter header.
        markdown_content = re.sub(r'^# ([0-9]+)\. (.*)', r'# \2', markdown_content)

        markdown_content = super().process_chapter_markdown(markdown_content)

        return markdown_content


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


    # FIXME: This is supposing sections are shorter than a page.
    def process_readme_section(self, section_content, book_style=True):
        if book_style:
            section_content = '\\mbox{}\n\n\\thispagestyle{empty}\n\n\\newpage\n\n' + section_content

        section_content += '\\mbox{}\n\n\\thispagestyle{empty}\n\n\\newpage\n\n' 
        
        return section_content


    def generate_readme_sections(self, book_style, section_headers):
        (_, temp_filepath) = tempfile.mkstemp()
        (_, readme_sections_pdf_filepath) = tempfile.mkstemp()
        readme_sections_pdf_filepath += '.pdf'

        markdown_content = ComposedMarkdownFile()
        markdown_content.append_string('\\pagenumbering{gobble}\n\n') # No page numbers.

        markdown_content.append_file_sections('README.md', section_headers, lambda x: self.process_readme_section(x, book_style))
        markdown_content.append_string('\\mbox{}\n\n\\thispagestyle{empty}\n\n\\newpage\n\n')

        with open(temp_filepath, 'w') as temp_file:
            temp_file.write(markdown_content.content())

        call(["pandoc"] + ["--from", "markdown-implicit_figures", "--output", readme_sections_pdf_filepath, temp_filepath])

        # Retrieve pages number
        readme_sections_pdf = PdfFileReader(open(readme_sections_pdf_filepath,'rb'))

        return (readme_sections_pdf_filepath, readme_sections_pdf.getNumPages())

    def generate_end_note(self, prologue_filepaths, page_offset):
        (_, temp_filepath) = tempfile.mkstemp()
        (_, end_note_pdf_filepath) = tempfile.mkstemp()
        end_note_pdf_filepath += '.pdf'

        for prologue_filepath in prologue_filepaths:
            with open(temp_filepath, 'a') as temp_file:
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
       
