import os
import logging

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdftypes import resolve1
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from mercurius.core import myparser
from mercurius.utils.logger import Logger, LogTypes
from .base_extractor import IBaseExtractor

logging.getLogger('pdfminer').setLevel(logging.ERROR)


class PDFExtractor(IBaseExtractor):

    def __init__(self, fname, password=None, logger=None):
        super(PDFExtractor, self).__init__()
        self.fname = fname
        self.password = password
        if logger:
            self.logger = logger
        else:
            self.logger = Logger(type=LogTypes.TO_SCREEN)
        self.parser = None

    def _parse_content(self):
        pagenos = set()
        maxpages = 0
        codec = 'utf-8'
        caching = True
        laparams = LAParams()
        rsrcmgr = PDFResourceManager(caching=caching)
        outfp = open('temppdf.txt', 'w')
        device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams)
        with open(self.fname, 'rb') as fp:
            self._process_pdf(rsrcmgr, device, fp, pagenos, maxpages=maxpages, password=self.password, caching=caching, check_extractable=True)
        device.close()
        outfp.close()
        with open('temppdf.txt', 'rb') as infp:
            self.content = infp.read().decode('utf-8')
        os.remove('temppdf.txt')

        mp = myparser.parser(self.content)
        self.emails.extend(mp.emails())
        self.emails = self.unique(self.emails)
        self.hosts.extend(mp.hostnames_all())
        self.hosts = self.unique(self.hosts)

    def parse_data(self):
        with open(self.fname, 'rb') as fp:
            parser = PDFParser(fp)
            doc = PDFDocument(parser)
            parser.close()

        if doc:
            try:
                for xref in doc.xrefs:
                    info_ref = xref.trailer.get('Info')
                    info = None
                    if info_ref:
                        info = resolve1(info_ref)
                    self.metadata = info
                    break
                if not self.metadata:
                    self.errors.append('No metadata found')
                    return False
                else:
                    self._parse_data()
                    return True
            except Exception as e:
                self.logger.error(str(e))
                self.errors.append(str(e))
                return False

    def _parse_data(self):
        self._parse_meta()

        metatext = ""
        for v in self.metadata.values():
            metatext += v.decode("utf-8") + " "
        self.parser = myparser.parser(metatext)
        self.emails.extend(self.parser.emails())
        self.hosts.extend(self.parser.hostnames_all())

        self._parse_content()

    def _parse_meta(self):
        author = self.metadata.get('Author', None)
        if author:
            self.users.append(author.decode("utf-8"))

        company = self.metadata.get('Company', None)
        if company:
            self.users.append(company.decode("utf-8"))

        title = self.metadata.get('Title', None)
        if title:
            self.misc.append({'title': title.decode("utf-8")})

        vendor = self.metadata.get('Producer', None)
        if vendor:
            self.misc.append({'vendor': vendor.decode("utf-8")})

        creator = self.metadata.get('Creator', None)
        if creator:
            self.misc.append({'creator': creator.decode("utf-8")})

    @staticmethod
    def _process_pdf(rsrcmgr, device, fp, pagenos=None, maxpages=0, password='', caching=True, check_extractable=True):
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,
                                      caching=caching, check_extractable=check_extractable):
            interpreter.process_page(page)
        return
