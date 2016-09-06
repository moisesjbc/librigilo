from ..src.configuration import Configuration
from unittest import TestCase

class TestConfiguration(TestCase):

    TEST_OUTPUT_FILEPATH = 'book.pdf'
    TEST_PREAMBLE_SECTIONS = ['## Sinopsis', '## License', '## Acknowledgements']
    TEST_CHAPTERS_FILES = 'manuscript/chapter_*'
    TEST_EPILOGUE_FILES = ['manuscript/epilogue.md']

    TEMPLATE_CONFIG = {
        Configuration.OUTPUT_FILEPATH_KEY: TEST_OUTPUT_FILEPATH,
        Configuration.PREAMBLE_SECTIONS_KEY: TEST_PREAMBLE_SECTIONS,
        Configuration.CHAPTERS_FILES_KEY: TEST_CHAPTERS_FILES,
        Configuration.EPILOGUE_FILES_KEY: TEST_EPILOGUE_FILES
    }


    def test_check_constructor(self):
        config = Configuration(self.TEMPLATE_CONFIG)

        assert self.TEST_OUTPUT_FILEPATH == config.OUTPUT_FILEPATH
        assert self.TEST_PREAMBLE_SECTIONS == config.PREAMBLE_SECTIONS
        assert self.TEST_CHAPTERS_FILES == config.CHAPTERS_FILES
        assert self.TEST_EPILOGUE_FILES == config.EPILOGUE_FILES
        

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


    def test_check_required_fields_missing_epilogue_files(self):
        self.remove_key_then_assert_key_error(
            self.TEMPLATE_CONFIG, 
            Configuration.EPILOGUE_FILES_KEY)
