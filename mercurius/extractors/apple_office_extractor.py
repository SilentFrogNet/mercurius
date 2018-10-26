import os

from .base_extractor import IBaseExtractor
from mercurius.loaders.extractor_loader import extractors_foo
from mercurius.utils.file_types import FileTypes


class AppleOfficeExtractor(IBaseExtractor):
    extractor_name = "AppleOfficeExtractor"

    def __init__(self, logger=None):
        super(AppleOfficeExtractor, self).__init__(logger)

    @extractors_foo
    def parse_data(self, path, filetype, **kwargs):
        self.filename = path

        if filetype not in FileTypes.APPLE_OFFICE:
            return None

        if self.metadata:
            return self

        for root, dirs, files in os.walk(self.filename):
            for file in files:
                print(os.path.join(root, file))
