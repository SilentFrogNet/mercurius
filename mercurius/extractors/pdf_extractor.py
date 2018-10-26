import os
import logging

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdftypes import PDFObjRef, resolve1
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

from .base_extractor import IBaseExtractor
from mercurius.core.data_parser import DataParser
from mercurius.utils.file_types import FileTypes
from mercurius.loaders.extractor_loader import extractors_foo

logging.getLogger('pdfminer').setLevel(logging.ERROR)


class PDFExtractor(IBaseExtractor):
    extractor_name = "PDFExtractor"

    CODEC = 'utf-8'

    def __init__(self, logger=None):
        super(PDFExtractor, self).__init__(logger)
        self.parser = DataParser()

    @extractors_foo
    def parse_data(self, path, filetype, **kwargs):
        self.filename = path
        self.metadata = {}

        if not filetype == FileTypes.PDF:
            return None

        with open(self.filename, 'rb') as fp:
            parser = PDFParser(fp)
            doc = PDFDocument(parser)

            if doc:
                try:
                    for xref in doc.xrefs:
                        info_ref = xref.trailer.get('Info')
                        info = None
                        if info_ref:
                            info = resolve1(info_ref)
                        self.metadata = info
                        for k, v in info.items():
                            if isinstance(v, PDFObjRef):
                                self.metadata[k] = resolve1(v)
                        break
                    if not self.metadata:
                        self.errors.append('No metadata found')
                        out = None
                    else:
                        self._parse_data()
                        out = self
                except Exception as e:
                    self.logger.error(str(e))
                    self.errors.append(str(e))
                    out = None
            else:
                self.errors.append('Cannot parse document')

            parser.close()
        return out

    def _parse_content(self):
        pagenos = set()
        maxpages = 0
        caching = True
        laparams = LAParams()
        rsrcmgr = PDFResourceManager(caching=caching)
        outfp = open('temppdf.txt', 'w')
        device = TextConverter(rsrcmgr, outfp, codec=self.CODEC, laparams=laparams)
        with open(self.filename, 'rb') as fp:
            self._process_pdf(rsrcmgr, device, fp, pagenos, maxpages=maxpages, caching=caching, check_extractable=True)
        device.close()
        outfp.close()
        with open('temppdf.txt', 'rb') as infp:
            self.content = self._decode_string(infp.read())
        os.remove('temppdf.txt')

        self.emails.extend(self.parser.emails(self.content))
        self.emails = self.unique(self.emails)
        self.hosts.extend(self.parser.hostnames(self.content))
        self.hosts = self.unique(self.hosts)

    def _parse_data(self):
        self._parse_meta()

        metatext = ""
        for v in self.metadata.values():
            if isinstance(v, list):
                v = " ".join(v)
            metatext += self._decode_string(v) + " "
        self.emails.extend(self.parser.emails(metatext))
        self.hosts.extend(self.parser.hostnames(metatext))

        self._parse_content()

    def _parse_meta(self):
        author = self.metadata.get('Author', None)
        if author:
            self.users.append(self._decode_string(author))

        company = self.metadata.get('Company', None)
        if company:
            self.users.append(self._decode_string(company))

        title = self.metadata.get('Title', None)
        if title:
            self.misc.append({'title': self._decode_string(title)})

        vendor = self.metadata.get('Producer', None)
        if vendor:
            self.misc.append({'vendor': self._decode_string(vendor)})

        creator = self.metadata.get('Creator', None)
        if creator:
            self.misc.append({'creator': self._decode_string(creator)})

    @staticmethod
    def _process_pdf(rsrcmgr, device, fp, pagenos=None, maxpages=0, caching=True, check_extractable=True):
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, caching=caching, check_extractable=check_extractable):
            interpreter.process_page(page)
        return

    def _decode_string(self, text, decoder=CODEC):
        try:
            out = text.decode(decoder)
        except AttributeError as e:
            out = str(text)

        return out
