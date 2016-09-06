import re
import os
import tempfile
from subprocess import call
from composed_markdown_file import ComposedMarkdownFile
from book_generators.book_generator import BookGenerator
from glob import glob


class EpubBookGenerator(BookGenerator):
    def generate_chapters(self, page_offset, book_style, chapters_files_regex):
        chapters_markdown_file = ComposedMarkdownFile()
        #chapters_markdown_file.append_string('\n\n\\setcounter{page}{%s}\n\n' % page_offset)
        for filepath in sorted(glob(chapters_files_regex)):
            chapters_markdown_file.append_file(filepath, self.process_chapter_markdown)

        (_, monolithic_filepath) = tempfile.mkstemp()
        with open(monolithic_filepath, 'w') as monolithic_file:
            monolithic_file.write(chapters_markdown_file.content())

            pandoc_options = ["-t", "markdown", "-V", "lang=es", "--from", "markdown+hard_line_breaks", "--toc", "--chapters"]
            if book_style == True:
                pandoc_options += ["-V", "documentclass=book"]
            else:
                pandoc_options += ["-V", "documentclass=report"]

            (_, chapters_epub_filepath) = tempfile.mkstemp()
            chapters_epub_filepath += '.md'
            call(["pandoc"] + pandoc_options + ["-t", "markdown", "--output", chapters_epub_filepath, monolithic_filepath])

            # TODO: Return real number of pages.
            return (chapters_epub_filepath, 1)


    def generate_readme_sections(self, book_style, section_headers):
        (_, temp_filepath) = tempfile.mkstemp()
        (_, readme_sections_epub_filepath) = tempfile.mkstemp()
        readme_sections_epub_filepath += '.md'

        markdown_content = ComposedMarkdownFile()

        markdown_content.append_file_sections('README.md', section_headers)

        with open(temp_filepath, 'w') as temp_file:
            temp_file.write(markdown_content.content())

        call(["pandoc", "-t", "markdown", "--from", "markdown-implicit_figures", "--output", readme_sections_epub_filepath, temp_filepath])

        # TODO: Return real number of pages.
        return (readme_sections_epub_filepath, 1)

    def generate_end_note(self, prologue_filepaths, page_offset):
        (_, dst_end_note_epub_filepath) = tempfile.mkstemp()
        dst_end_note_epub_filepath += '.md'

        for prologue_filepath in prologue_filepaths:
            with open(prologue_filepath, 'rU') as src_end_note_file, open(dst_end_note_epub_filepath, 'a') as dst_end_note_epub_file:
                for line in src_end_note_file:
                    if line == '## Navegación\n':
                        break
                    dst_end_note_epub_file.write(line)

        return dst_end_note_epub_filepath


    def generate_cover(self):
        (_, cover_epub_filepath) = tempfile.mkstemp()
        cover_epub_filepath += '.md'

        with open('epub_metadata.txt', 'rU') as epub_metadata_file, open(cover_epub_filepath, 'w') as cover_epub_file:
            cover_epub_file.write(epub_metadata_file.read())

        return cover_epub_filepath


    def merge_book_parts(self, part_filepaths, output_filepath):
        call(['pandoc', '-S', '-s', '--from', 'markdown', '--output', output_filepath] + part_filepaths)
