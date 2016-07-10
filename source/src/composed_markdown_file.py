class ComposedMarkdownFile:
    def __init__(self):
        self.content_ = ''

    def content(self):
        return self.content_

    def append_file(self, file_path, content_processing_callback=None):
        with open(file_path, 'rU') as file:
            if content_processing_callback is not None:
                self.content_ += content_processing_callback(file.read())
            else:
                self.content_ += file.read()

    def append_string(self, string):
        self.content_ += string
