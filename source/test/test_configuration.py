from ..src.configuration import Configuration
from unittest import TestCase

class TestConfiguration(TestCase):

    TEMPLATE_CONFIG = {
        Configuration.OUTPUT_FILEPATH_KEY: 'book.pdf',
        Configuration.PREAMBLE_SECTIONS_KEY: ['## Sinopsis', '## License', '## Acknowledgements'],
        Configuration.CHAPTERS_FILES_KEY: 'manuscript/chapter_*',
        Configuration.EPILOGUE_FILE_KEY: 'manuscript/epilogue.md'
    }

    def test_check_required_fields_ok(self):
        assert True == Configuration.check_required_fields(self.TEMPLATE_CONFIG)


    def remove_key_then_assert_key_error(self, template_config, key):
        config = template_config.copy()
        del config[key]
        self.assert_key_error(config, key)


    def assert_key_error(self, config, key):
        try:
            Configuration.check_required_fields(config)
            self.fail('Expected KeyError for key %s' % key)
        except KeyError as error:
            self.assertTrue(key == error.args[0])


    def test_check_required_fields_missing_output_filepath(self):
        self.remove_key_then_assert_key_error(
            self.TEMPLATE_CONFIG, 
            Configuration.OUTPUT_FILEPATH_KEY)


    def test_check_required_fields_missing_preamble_sections(self):
        self.remove_key_then_assert_key_error(
            self.TEMPLATE_CONFIG, 
            Configuration.PREAMBLE_SECTIONS_KEY)


    def test_check_required_fields_missing_chapters_files(self):
        self.remove_key_then_assert_key_error(
            self.TEMPLATE_CONFIG, 
            Configuration.CHAPTERS_FILES_KEY)


    def test_check_required_fields_missing_epilogue_file(self):
        self.remove_key_then_assert_key_error(
            self.TEMPLATE_CONFIG, 
            Configuration.EPILOGUE_FILE_KEY)
