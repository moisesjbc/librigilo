import re
import os
import tempfile
from subprocess import call
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

            pandoc_options = ["-t", "markdown", "-V", "lang=es", "--from", "markdown+hard_line_breaks", "--toc", "--chapters"]
            if book_style:
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

        with open(temp_filepath, 'w') as temp_file:
            #temp_file.write('\\pagenumbering{gobble}\n\n') # No page numbers.
            with open('README.md', 'rU') as readme_file:
                copy_line = False
                for line in readme_file:
                    if line.startswith('#'):
                        copy_line = line[:-1] in section_headers

                    if copy_line:
                        if line.startswith('#'):
                            temp_file.write(line[1:]) # Make header top level.
                        else:
                            temp_file.write(line)

        call(["pandoc", "-t", "markdown", "--from", "markdown-implicit_figures", "--output", readme_sections_epub_filepath, temp_filepath])

        # TODO: Return real number of pages.
        return (readme_sections_epub_filepath, 1)

    def generate_end_note(self, page_offset):
        (_, dst_end_note_epub_filepath) = tempfile.mkstemp()
        dst_end_note_epub_filepath += '.md'

        with open('manuscrito/nota-final.md', 'rU') as src_end_note_file, open(dst_end_note_epub_filepath, 'w') as dst_end_note_epub_file:
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
