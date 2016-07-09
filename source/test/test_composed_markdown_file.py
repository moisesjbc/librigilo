from ..src.composed_markdown_file import ComposedMarkdownFile

class TestComposedMarkdownFile:
    def test_empty_file(self):
        file = ComposedMarkdownFile()
        assert '' == file.content()
