import re

class BookGenerator():
    def process_chapter_markdown(self, markdown_content):
        # Remove number from chapter header.
        markdown_content = re.sub(r'^# ([0-9]+)\. (.*)', r'# \2', markdown_content)

        # Replace dialog '-'s with '--'s
        markdown_content = re.sub(r'(?<!\w)-(?!-)', '--', markdown_content)

        # Remove Navigation section
        markdown_content = re.sub(r'(.*)## Navegación(.*)', r'\1', markdown_content, flags=re.DOTALL)

        return markdown_content
