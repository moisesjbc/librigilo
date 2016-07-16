import json

class Configuration:
    OUTPUT_FILEPATH_KEY = 'output-filepath'
    PREAMBLE_SECTIONS_KEY = 'preamble-sections'
    CHAPTERS_FILES_KEY = 'chapters-files'
    EPILOGUE_FILE_KEY = 'epilogue-file'
    BOOK_STYLE_KEY = 'book-style'

    def __init__(self, config_dict):
        Configuration.check_required_fields(config_dict)

        self.OUTPUT_FILEPATH = config_dict[Configuration.OUTPUT_FILEPATH_KEY]
        self.PREAMBLE_SECTIONS = config_dict[Configuration.PREAMBLE_SECTIONS_KEY]
        self.CHAPTERS_FILES = config_dict[Configuration.CHAPTERS_FILES_KEY]
        self.EPILOGUE_FILE = config_dict[Configuration.EPILOGUE_FILE_KEY]

        if self.BOOK_STYLE_KEY in config_dict:
            if config_dict[self.BOOK_STYLE_KEY] == "true":
                self.BOOK_STYLE = True
            else:
                self.BOOK_STYLE = False
        else:
            self.BOOK_STYLE = True


    @staticmethod
    def load_configurations_from_json_file(filepath):
        configurations = []
        with open(filepath) as file:   
            configuration_dicts = json.load(file)
            for configuration_dict in configuration_dicts:
                configuration = Configuration(configuration_dict)
                configurations.append(configuration)
            return configurations
    

    @staticmethod
    def check_required_field(config_dict, key):
        if not key in config_dict:
            raise KeyError(key)

    @staticmethod
    def check_required_fields(config_dict):
        required_keys = [
            Configuration.OUTPUT_FILEPATH_KEY,
            Configuration.PREAMBLE_SECTIONS_KEY,
            Configuration.CHAPTERS_FILES_KEY,
            Configuration.EPILOGUE_FILE_KEY
        ]

        for key in required_keys:
            Configuration.check_required_field(config_dict, key)

        return True
