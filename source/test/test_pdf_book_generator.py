from ..src.book_generators.pdf_book_generator import PdfBookGenerator

class TestPdfBookGenerator:
    def test_process_chapter_markdown(self):
        src_content = \
            '# 1. Chapter title\n' + \
            '\n' + \
            'Great chapter!\n' + \
            '- With great dialogs! - he said\n' + \
            '- Yeah! great-and-awesome-dialogs!\n' + \
            '\n' + \
            '## Navegación\n' + \
            '\n' + \
            'Navigation content'
        expected_result_content = \
            '# Chapter title\n' + \
            '\n' + \
            'Great chapter!\n' + \
            '-- With great dialogs! -- he said\n' + \
            '-- Yeah! great-and-awesome-dialogs!\n' + \
            '\n'

        pdf_book_generator = PdfBookGenerator()
        assert expected_result_content == \
            pdf_book_generator.process_chapter_markdown(src_content)
