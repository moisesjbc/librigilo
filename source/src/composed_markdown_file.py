class ComposedMarkdownFile:
    def __init__(self):
        self.content_ = ''

    def content(self):
        return self.content_

    def append_file(self, file_path):
        with open(file_path, 'rU') as file:
            self.content_ += file.read()
