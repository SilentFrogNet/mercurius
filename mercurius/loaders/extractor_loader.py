import pluggy
from .loader import PluginLoader

EXTRACTOR_PROJECT_NAME = "extractors"

extractors_hookspec = pluggy.HookspecMarker(EXTRACTOR_PROJECT_NAME)
extractors_foo = pluggy.HookimplMarker(EXTRACTOR_PROJECT_NAME)


class ExtractorLoader(PluginLoader):
    DEFAULT_PLUGINS_PATH = 'mercurius/extractors'
    DEFAULT_PLUGINS_PACKAGE = 'mercurius.extractors'

    def __init__(self, configs):
        super(ExtractorLoader, self).__init__(EXTRACTOR_PROJECT_NAME,
                                              ExtractorHookSpec,
                                              configs,
                                              plugin_path=self.DEFAULT_PLUGINS_PATH,
                                              plugin_package=self.DEFAULT_PLUGINS_PACKAGE)

    def get_enabled_plugins(self):
        section = self.configs.get('EXTRACTORS', {}).get('ENABLED', {})
        return dict(section)


class ExtractorHookSpec:
    """
    A hook specification namespace for the extractors.
    """

    @extractors_hookspec
    def parse_data(self, path, filetype, **kwargs):
        """
        The hook to be costumized to implement an extractor plugin.

        1. Check if the file has the correct data type
        2. Has to populate all the BaseExtractor variables:
              * metadata: is a string representation of the metadata
              * content: is the content of the file, if any
              * users: is a list of all the collected users
              * emails: is a list of all the collected emails
              * hosts: is a list of all the collected hosts
              * misc: is a list of all the collected additional information
              * errors: is a list of all the errors during the parsing, if any
        3. Must return the parser itself, None otherwise
        """
        return None
