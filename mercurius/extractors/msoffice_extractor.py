from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from hachoir.core import config as hachoir_config
from addict import Dict

from .base_extractor import IBaseExtractor
from mercurius.loaders.extractor_loader import extractors_foo
from mercurius.utils.file_types import FileTypes

hachoir_config.quiet = True


class MSOfficeExtractor(IBaseExtractor):
    extractor_name = "MSOfficeExtractor"

    def __init__(self, logger=None):
        super(MSOfficeExtractor, self).__init__(logger)

    @extractors_foo
    def parse_data(self, path, filetype, **kwargs):
        self.filename = path

        if filetype not in FileTypes.MS_OFFICE:
            return None

        if self.metadata:
            return self

        filename, realname = str(self.filename), self.filename
        try:
            parser = createParser(filename, realname)
        except Exception as e:
            self.logger.error(str(e))
            self.errors.append(str(e))
            return None
        try:
            metadata = extractMetadata(parser)
        except Exception as e:
            self.logger.error(str(e))
            self.errors.append(str(e))
            return None

        if metadata:
            metalist = metadata.exportPlaintext()
            meta = Dict()
            for item in metalist:
                self._parse_item(item, meta)

            self.metadata = meta

            for k, v in meta.items():
                if k == "Author":
                    self.users.append(v)
                elif k in ["Producer", "MIME type", "Endianness"]:
                    self.misc.append({k: v})
        return self

    def _parse_item(self, item, father=None):
        if father is None:
            father = Dict()
        tag, value = item.split(':', 1)
        value = value.strip()
        tag = tag.strip()
        if not value:
            return None

        vals = value.split(': ')
        if len(vals) > 1:
            value = self._parse_item(value)

        if tag.startswith('-'):
            tag = tag[2:]
        if tag in father:
            if not isinstance(father[tag], list):
                father[tag] = [father[tag]]
            father[tag].append(value)
        else:
            father[tag] = value

        return father
