import zipfile
import re
import os
import random

from .base_extractor import IBaseExtractor
from mercurius.loaders.extractor_loader import extractors_foo
from mercurius.utils.file_types import FileTypes


class OpenOfficeExtractor(IBaseExtractor):
    extractor_name = "OpenOfficeExtractor"

    def __init__(self, logger=None):
        super(OpenOfficeExtractor, self).__init__(logger)

    @extractors_foo
    def parse_data(self, path, filetype, **kwargs):
        self.filename = path

        if filetype not in FileTypes.OPEN_OFFICE:
            return None

        rnd = str(random.randrange(0, 1001, 3))
        working_dir = os.path.dirname(os.path.realpath(self.filename))
        filename, file_extension = os.path.splitext(os.path.basename(self.filename))
        meta_filename = os.path.join(working_dir, "meta{}.xml".format(rnd))
        with zipfile.ZipFile(self.filename, 'r') as z:
            open(meta_filename, 'wb').write(z.read('meta.xml'))

        with open(meta_filename, 'rb') as f:
            self.metadata = f.read().decode('utf-8')
        os.remove('meta' + rnd + '.xml')

        self._parse_meta()

    def _parse_meta(self):
        p = re.compile('office:version="([\d.]*)"><office:meta>')
        matches = p.findall(self.metadata)
        if matches and len(matches) > 0:
            self.misc.append({'version': str(matches[0])})

        p = re.compile('<meta:generator>(.*)</meta:generator>')
        matches = p.findall(self.metadata)
        if matches:
            self.misc.append({'generator': str(matches[0])})

        p = re.compile('<meta:creation-date>(.*)</meta:creation-date>')
        matches = p.findall(self.metadata)
        if matches:
            self.misc.append({'creationDate': str(matches[0])})

        p = re.compile('<dc:date>(.*)</dc:date>')
        matches = p.findall(self.metadata)
        if matches:
            self.misc.append({'date': str(matches[0])})

        p = re.compile('<dc:language>(.*)</dc:language>')
        matches = p.findall(self.metadata)
        if matches:
            self.misc.append({'language': str(matches[0])})

        p = re.compile('<meta:editing-cycles>(.*)</meta:editing-cycles>')
        matches = p.findall(self.metadata)
        if matches:
            self.misc.append({'editingCycles': str(matches[0])})

        p = re.compile('<meta:editing-duration>(.*)</meta:editing-duration>')
        matches = p.findall(self.metadata)
        if matches:
            self.misc.append({'editingDuration': str(matches[0])})

        p = re.compile('meta:table-count="(\d*)"')
        matches = p.findall(self.metadata)
        if matches:
            self.misc.append({'tableCount': str(matches[0])})

        p = re.compile('meta:image-count="(\d*)"')
        matches = p.findall(self.metadata)
        if matches:
            self.misc.append({'imageCount': str(matches[0])})

        p = re.compile('meta:object-count="(\d*)"')
        matches = p.findall(self.metadata)
        if matches:
            self.misc.append({'objectCount': str(matches[0])})

        p = re.compile('meta:page-count="(\d*)"')
        matches = p.findall(self.metadata)
        if matches:
            self.misc.append({'pageCount': str(matches[0])})

        p = re.compile('meta:paragraph-count="(\d*)"')
        matches = p.findall(self.metadata)
        if matches:
            self.misc.append({'paragraphCount': str(matches[0])})

        p = re.compile('meta:word-count="(\d*)"')
        matches = p.findall(self.metadata)
        if matches:
            self.misc.append({'wordCount': str(matches[0])})

        p = re.compile('meta:character-count="(\d*)"')
        matches = p.findall(self.metadata)
        if matches:
            self.misc.append({'characterCount': str(matches[0])})

        p = re.compile('<meta:initial-creator>(.*)</meta:initial-creator>')
        matches = p.findall(self.metadata, re.DOTALL)
        if matches:
            self.misc.append({'initialCreator': str(matches[0])})

        p = re.compile('<dc:creator>(.*)</dc:creator>')
        matches = p.findall(self.metadata, re.DOTALL)
        if matches:
            self.users.append(str(matches[0]))

        p = re.compile('<dc:title>(.*)</dc:title>')
        matches = p.findall(self.metadata)
        if matches:
            self.misc.append({'title': str(matches[0])})

        p = re.compile('<dc:description>(.*)</dc:description>')
        matches = p.findall(self.metadata)
        if matches:
            self.misc.append({'description': str(matches[0])})

        p = re.compile('<dc:subject>(.*)</dc:subject>')
        matches = p.findall(self.metadata)
        if matches:
            self.misc.append({'subject': str(matches[0])})

        p = re.compile('<meta:printed-by>(.*)</meta:printed-by>')
        matches = p.findall(self.metadata)
        if matches:
            self.misc.append({'printedBy': str(matches[0])})

        p = re.compile('<meta:print-date>(.*)</meta:print-date>')
        matches = p.findall(self.metadata)
        if matches:
            self.misc.append({'printDate': str(matches[0])})
