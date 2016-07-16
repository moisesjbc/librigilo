import re
import os
from configuration import Configuration

class BookGenerator():
    def process_chapter_markdown(self, markdown_content):
        # Remove number from chapter header.
        markdown_content = re.sub(r'^# ([0-9]+)\. (.*)', r'# \2', markdown_content)

        # Replace dialog '-'s with '--'s
        markdown_content = re.sub(r'(?<!\w)-(?!-)', '--', markdown_content)

        # Remove Navigation section
        markdown_content = re.sub(r'(.*)## Navegación(.*)', r'\1', markdown_content, flags=re.DOTALL)

        return markdown_content


    def generate_chapters(self, page_offset, book_style, chapters_files):
        raise NotImplementedError

    def generate_readme_sections(self, book_style, section_headers):
        raise NotImplementedError

    def generate_end_note(self, page_offset):
        raise NotImplementedError

    def generate_cover(self):
        raise NotImplementedError

    def merge_book_parts(self, part_filepaths, output_filepath):
        raise NotImplementedError


    def generate_book(self, configuration):
        assert isinstance(configuration, Configuration)

        cover_pdf_filepath = self.generate_cover()
        (readme_sections_pdf_filepath, readme_sections_pdf_n_pages) = \
            self.generate_readme_sections(
                book_style=configuration.BOOK_STYLE,
                section_headers=configuration.PREAMBLE_SECTIONS)
        page_offset = readme_sections_pdf_n_pages + 1
        if not configuration.BOOK_STYLE:
            # Previous PDF in not book style mode includes an empty page not 
            # taken into account
            page_offset += 1
        (chapters_pdf_filepath, chapters_pdf_n_pages) = self.generate_chapters(
            page_offset=page_offset, 
            book_style=configuration.BOOK_STYLE, 
            chapters_files_regex=configuration.CHAPTERS_FILES
        )
        page_offset += chapters_pdf_n_pages - 1
        
        end_note_pdf_filepath = \
            self.generate_end_note(prologue_filepath=configuration.EPILOGUE_FILE,          
                                    page_offset=page_offset)
            
        book_parts_paths = [
            cover_pdf_filepath,
            readme_sections_pdf_filepath,
            chapters_pdf_filepath,
            end_note_pdf_filepath
        ]
        book_filepath = configuration.OUTPUT_FILEPATH
        self.merge_book_parts(book_parts_paths, book_filepath)
