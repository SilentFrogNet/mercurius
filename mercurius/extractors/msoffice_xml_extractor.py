import zipfile
import re
import os
import random
from mercurius.core import data_parser

from .base_extractor import IBaseExtractor
from mercurius.loaders.extractor_loader import extractors_foo
from mercurius.utils.file_types import FileTypes


class MSOfficeXMLExtractor(IBaseExtractor):
    extractor_name = "MSOfficeXMLExtractor"

    def __init__(self, logger=None):
        super(MSOfficeXMLExtractor, self).__init__(logger)
        self.template = ""
        self.totalTime = ""
        self.pages = ""
        self.words = ""
        self.characters = ""
        self.application = ""
        self.docSecurity = ""
        self.lines = ""
        self.paragraphs = ""
        self.scaleCrop = ""
        self.company = ""
        self.linksUpToDate = ""
        self.charactersWithSpaces = ""
        self.shareDoc = ""
        self.hyperlinksChanged = ""
        self.appVersion = ""
        self.title = ""
        self.subject = ""
        self.creator = ""
        self.keywords = ""
        self.lastModifiedBy = ""
        self.revision = ""
        self.createdDate = ""
        self.modifiedDate = ""
        self.filename = None
        self.docu_filepath = None
        self.comments_filepath = None
        self.shared_strings_filepath = None

    @extractors_foo
    def parse_data(self, path, filetype, **kwargs):
        self.filename = path

        if filetype not in FileTypes.MS_OFFICE_XML:
            return None

        rnd = str(random.randrange(0, 1001, 3))
        tmp_dir = kwargs.get('configs', {}).get('tmp_directory', os.path.dirname(os.path.realpath(self.filename)))
        filename, file_extension = os.path.splitext(os.path.basename(self.filename))
        app_filepath = os.path.join(tmp_dir, "app{}.xml".format(rnd))
        core_filepath = os.path.join(tmp_dir, "core{}.xml".format(rnd))
        self.docu_filepath = os.path.join(tmp_dir, "docu{}.xml".format(rnd))
        self.comments_filepath = os.path.join(tmp_dir, "comments{}.xml".format(rnd))
        self.shared_strings_filepath = os.path.join(tmp_dir, "shared_strings{}.xml".format(rnd))

        with zipfile.ZipFile(self.filename, 'r') as z:
            open(app_filepath, 'wb').write(z.read('docProps/app.xml'))
            open(core_filepath, 'wb').write(z.read('docProps/core.xml'))
            if file_extension == ".docx":
                self._extract_docx_xmls(z)
            elif file_extension == ".pptx":
                self._extract_pptx_xmls(z)
            elif file_extension == ".xlsx":
                self._extract_xlsx_xmls(z)

        # parse app info
        if os.path.exists(app_filepath):
            with open(app_filepath, 'rb') as f:
                app = f.read()
                self.parse_app(app)

        # parse comments
        if os.path.exists(self.comments_filepath):
            with open(self.comments_filepath, 'rb') as f:
                comm = f.read()
                self.parse_comments(comm)

        # parse document content
        if os.path.exists(self.docu_filepath):
            with open(self.docu_filepath, 'rb') as f:
                docu = f.read()
                self.text = docu

        # parse core info
        if os.path.exists(core_filepath):
            with open(core_filepath, 'rb') as f:
                core = f.read()
                self.parse_core(core)

        # Remove temporary files
        if os.path.exists(app_filepath):
            os.remove(app_filepath)
        if os.path.exists(core_filepath):
            os.remove(core_filepath)
        if os.path.exists(self.comments_filepath):
            os.remove(self.comments_filepath)
        if os.path.exists(self.docu_filepath):
            os.remove(self.docu_filepath)
        if os.path.exists(self.shared_strings_filepath):
            os.remove(self.shared_strings_filepath)

    def _extract_docx_xmls(self, z):
        open(self.docu_filepath, 'wb').write(z.read('word/document.xml'))
        try:
            open(self.comments_filepath, 'wb').write(z.read('word/comments.xml'))
            self.comments = True
        except:
            self.comments = False

    def _extract_xlsx_xmls(self, z):
        for fxml in z.filelist:
            if fxml.filename.startswith('xl/worksheets'):
                open(self.docu_filepath, 'ab').write(z.read(fxml.filename))
        open(self.shared_strings_filepath, 'wb').write(z.read('xl/sharedStrings.xml'))

    def _extract_pptx_xmls(self, z):
        for fxml in z.filelist:
            if fxml.filename.startswith('pt/sildes'):
                open(self.docu_filepath, 'ab').write(z.read(fxml.filename))

    def parse_comments(self, data):
        try:
            p = re.compile('w:author="(.*?)" w')
            # self.userscomments = p.findall(data)
            self.users.append(p.findall(data))
        except:
            pass

    def parse_app(self, data):
        try:
            p = re.compile('<Template>(.*)</Template>')
            self.template = str(p.findall(data)[0])
        except:
            pass

        try:
            p = re.compile('<TotalTime>(.*)</TotalTime>')
            self.totalTime = str(p.findall(data)[0])
        except:
            pass

        try:
            p = re.compile('<Pages>(.*)</Pages>')
            self.pages = str(p.findall(data)[0])
        except:
            pass

        try:
            p = re.compile('<Words>(.*)</Words>')
            self.words = str(p.findall(data)[0])
        except:
            pass

        try:
            p = re.compile('<Characters>(.*)</Characters>')
            self.characters = str(p.findall(data)[0])
        except:
            pass

        try:
            p = re.compile('<Application>(.*)</Application>')
            self.application = str(p.findall(data)[0])
        except:
            pass

        try:
            p = re.compile('<DocSecurity>(.*)</DocSecurity>')
            self.docSecurity = str(p.findall(data)[0])
        except:
            pass

        try:
            p = re.compile('<Lines>(.*)</Lines>')
            self.lines = str(p.findall(data)[0])
        except:
            pass

        try:
            p = re.compile('<Paragraphs>(.*)</Paragraphs>')
            self.paragraphs = str(p.findall(data)[0])
        except:
            pass

        try:
            p = re.compile('<ScaleCrop>(.*)</ScaleCrop>')
            self.scaleCrop = str(p.findall(data)[0])
        except:
            pass

        try:
            p = re.compile('<Company>(.*)</Company>')
            self.company = str(p.findall(data)[0])
        except:
            pass

        try:
            p = re.compile('<LinksUpToDate>(.*)</LinksUpToDate>')
            self.linksUpToDate = str(p.findall(data)[0])
        except:
            pass

        try:
            p = re.compile('<CharactersWithSpaces>(.*)</CharactersWithSpaces>')
            self.charactersWithSpaces = str(p.findall(data)[0])
        except:
            pass

        try:
            p = re.compile('<SharedDoc>(.*)</SharedDoc>')
            self.sharedDoc = str(p.findall(data)[0])
        except:
            pass

        try:
            p = re.compile('<HyperlinksChanged>(.*)</HyperlinksChanged>')
            self.hyperlinksChanged = str(p.findall(data)[0])
        except:
            pass

        try:
            p = re.compile('<AppVersion>(.*)</AppVersion>')
            self.appVersion = str(p.findall(data)[0])
        except:
            pass

    def parse_core(self, data):
        try:
            p = re.compile('<dc:title>(.*)</dc:title>')
            self.title = str(p.findall(data)[0])
        except:
            pass

        try:
            p = re.compile('<dc:subject>(.*)</dc:subject>')
            self.subject = str(p.findall(data)[0])
        except:
            pass

        try:
            p = re.compile('<dc:creator>(.*)</dc:creator>')
            self.creator = str(p.findall(data)[0])
        except:
            pass

        try:
            p = re.compile('<cp:keywords>(.*)</cp:keywords>')
            self.keywords = str(p.findall(data)[0])
        except:
            pass

        try:
            p = re.compile('<cp:lastModifiedBy>(.*)</cp:lastModifiedBy>')
            self.lastModifiedBy = str(p.findall(data)[0])
        except:
            pass

        try:
            p = re.compile('<cp:revision>(.*)</cp:revision>')
            self.revision = str(p.findall(data)[0])
        except:
            pass

        try:
            p = re.compile('<dcterms:created xsi:type=".*">(.*)</dcterms:created>')
            self.createdDate = str(p.findall(data)[0])
        except:
            pass

        try:
            p = re.compile('<dcterms:modified xsi:type=".*">(.*)</dcterms:modified>')
            self.modifiedDate = str(p.findall(data)[0])
        except:
            pass

    def getTexts(self):
        return "ok"

    def getRaw(self):
        raw = "Not implemented yet"
        return raw

    def getUsers(self):
        res = []
        temporal = []
        res.append(self.creator)
        res.append(self.lastModifiedBy)
        if self.comments == True:
            res.extend(self.userscomments)
        else:
            pass
        for x in res:
            if temporal.count(x) == 0:
                temporal.append(x)
            else:
                pass
        return temporal

    def getEmails(self):
        res = data_parser.DataParser(self.text)
        return res.emails()

    def getPaths(self):
        res = []
        # res.append(self.revision)
        return res

    def getSoftware(self):
        res = []
        res.append(self.application)
        return res
