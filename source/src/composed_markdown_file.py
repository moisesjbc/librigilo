import re

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

    @staticmethod
    def default_processing_callback(string):
        return string

    def append_file_sections(self, 
                             file_path, 
                             section_headers,
                             content_processing_callback=None):

        
        if content_processing_callback is None:
            content_processing_callback = ComposedMarkdownFile.default_processing_callback

        with open(file_path, 'rU') as file:
            file_content = file.read()
            for section_header in section_headers:
                regex_str = '^%s$(.*?)^#' % section_header
                regex = re.compile(regex_str, flags=re.DOTALL | re.MULTILINE)
                match = regex.search(file_content)
                section_header = '#' + section_header.lstrip('#')
                if match is not None:
                    self.content_ += content_processing_callback(section_header + '\n' + match.group(1))
