from ..src.composed_markdown_file import ComposedMarkdownFile
import os

class TestComposedMarkdownFile:
    @staticmethod
    def asset_path(asset_name):
        return os.path.join(os.path.dirname(__file__), 'assets', asset_name)


    def test_empty_file(self):
        file = ComposedMarkdownFile()
        assert '' == file.content()


    def test_append_one_file(self):
        src_file_path = TestComposedMarkdownFile.asset_path('src_file_1.md')

        dst_file = ComposedMarkdownFile()
        dst_file.append_file(src_file_path)
 
        with open(src_file_path, 'r') as src_file:
            assert src_file.read() == dst_file.content()


    def test_append_multiple_files(self):
        src_file_paths = [
            TestComposedMarkdownFile.asset_path('src_file_1.md'),
            TestComposedMarkdownFile.asset_path('src_file_2.md')
        ]
        expected_file_path = \
            TestComposedMarkdownFile.asset_path('raw_composed_file_1_2.md')

        dst_file = ComposedMarkdownFile()
        for src_file_path in src_file_paths:
            dst_file.append_file(src_file_path)
 
        with open(expected_file_path, 'r') as expected_file:
            assert expected_file.read() == dst_file.content()


    def test_append_file_sections(self):
        src_file_path = \
            TestComposedMarkdownFile.asset_path('src_file_with_multiple_sections.md')
        expected_file_path = \
            TestComposedMarkdownFile.asset_path('dst_file_with_multiple_sections.md')

        dst_file = ComposedMarkdownFile()
        dst_file.append_file_sections(src_file_path, ['### Section 3', '## Section 2'])
 
        with open(expected_file_path, 'r') as expected_file:
            assert expected_file.read() == dst_file.content()
