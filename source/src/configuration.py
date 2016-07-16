class Configuration:
    OUTPUT_FILEPATH_KEY = 'output-filepath'
    PREAMBLE_SECTIONS_KEY = 'preamble-sections'
    CHAPTERS_FILES_KEY = 'chapters-files'
    EPILOGUE_FILE_KEY = 'epilogue-file'


    def __init__(self, config_dict):
        Configuration.check_required_fields(config_dict)

        self.OUTPUT_FILEPATH = config_dict[Configuration.OUTPUT_FILEPATH_KEY]
        self.PREAMBLE_SECTIONS = config_dict[Configuration.PREAMBLE_SECTIONS_KEY]
        self.CHAPTERS_FILES = config_dict[Configuration.CHAPTERS_FILES_KEY]
        self.EPILOGUE_FILE = config_dict[Configuration.EPILOGUE_FILE_KEY]
    

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
