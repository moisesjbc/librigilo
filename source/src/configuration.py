class Configuration:
    OUTPUT_FILEPATH_KEY = 'output-filepath'
    PREAMBLE_SECTIONS_KEY = 'preamble-sections'
    CHAPTERS_FILES_KEY = 'chapters-files'
    EPILOGUE_FILE_KEY = 'epilogue-file'
    

    @staticmethod
    def check_required_field(config, key):
        if not key in config:
            raise KeyError(key)

    @staticmethod
    def check_required_fields(config):
        required_keys = [
            Configuration.OUTPUT_FILEPATH_KEY,
            Configuration.PREAMBLE_SECTIONS_KEY,
            Configuration.CHAPTERS_FILES_KEY,
            Configuration.EPILOGUE_FILE_KEY
        ]

        for key in required_keys:
            Configuration.check_required_field(config, key)

        return True
