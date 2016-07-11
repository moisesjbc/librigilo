import re
import os

class BookGenerator():
    def process_chapter_markdown(self, markdown_content):
        # Remove number from chapter header.
        markdown_content = re.sub(r'^# ([0-9]+)\. (.*)', r'# \2', markdown_content)

        # Replace dialog '-'s with '--'s
        markdown_content = re.sub(r'(?<!\w)-(?!-)', '--', markdown_content)

        # Remove Navigation section
        markdown_content = re.sub(r'(.*)## Navegación(.*)', r'\1', markdown_content, flags=re.DOTALL)

        return markdown_content


    def generate_chapters(self, page_offset, book_style, chapters_directory):
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
        cover_pdf_filepath = self.generate_cover()
        (readme_sections_pdf_filepath, readme_sections_pdf_n_pages) = \
            self.generate_readme_sections(
                book_style=configuration['book_style'],
                section_headers=configuration['section_headers'])
        page_offset = readme_sections_pdf_n_pages + 1
        if not configuration['book_style']:
            # Previous PDF in not book style mode includes an empty page not 
            # taken into account
            page_offset += 1
        (chapters_pdf_filepath, chapters_pdf_n_pages) = self.generate_chapters(
            page_offset=page_offset, 
            book_style=configuration['book_style'], 
            chapters_directory=configuration['chapters_directory']
        )
        page_offset += chapters_pdf_n_pages - 1
        
        end_note_pdf_filepath = self.generate_end_note(page_offset=page_offset)
            
        book_parts_paths = [
            cover_pdf_filepath,
            readme_sections_pdf_filepath,
            chapters_pdf_filepath,
            end_note_pdf_filepath
        ]
        book_filepath = os.path.join('build', configuration['file_name'])
        self.merge_book_parts(book_parts_paths, book_filepath)
