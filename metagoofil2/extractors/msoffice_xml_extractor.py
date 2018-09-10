import zipfile
import re
import os
import random
from metagoofil2.core import myparser

from .base_extractor import IBaseExtractor


class MSOfficeXMLExtractor(IBaseExtractor):

    def __init__(self, filepath=None):
        super(MSOfficeXMLExtractor, self).__init__()
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

        if filepath is None:
            self.userscomments = ""
            self.comments = True
            self.text = ""
        else:
            rnd = str(random.randrange(0, 1001, 3))
            working_dir = os.path.dirname(os.path.realpath(filepath))
            filename, file_extension = os.path.splitext(os.path.basename(filepath))
            self.app_filepath = os.path.join(working_dir, "app{}.xml".format(rnd))
            self.core_filepath = os.path.join(working_dir, "core{}.xml".format(rnd))
            self.docu_filepath = os.path.join(working_dir, "docu{}.xml".format(rnd))
            self.comments_filepath = os.path.join(working_dir, "comments{}.xml".format(rnd))
            self.shared_strings_filepath = os.path.join(working_dir, "shared_strings{}.xml".format(rnd))

            with zipfile.ZipFile(filepath, 'r') as z:
                open(self.app_filepath, 'wb').write(z.read('docProps/app.xml'))
                open(self.core_filepath, 'wb').write(z.read('docProps/core.xml'))
                if file_extension == ".docx":
                    self._extract_docx_xmls(z)
                elif file_extension == ".pptx":
                    self._extract_pptx_xmls(z)
                elif file_extension == ".xlsx":
                    self._extract_xlsx_xmls(z)

            # parse app info
            with open(self.app_filepath, 'rb') as f:
                app = f.read()
                self.parse_app(app)

            # parse comments
            if self.comments:
                with open(self.comments_filepath, 'rb') as f:
                    comm = f.read()
                    self.parse_comments(comm)

            # parse document content
            with open(self.docu_filepath, 'rb') as f:
                docu = f.read()
                self.text = docu

            # parse core info
            with open(self.core_filepath, 'rb') as f:
                core = f.read()
                self.parse_core(core)

            # Remove temporary files
            os.remove(self.app_filepath)
            os.remove(self.core_filepath)
            os.remove(self.comments_filepath)
            os.remove(self.docu_filepath)
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

    def toString(self):
        print("--- Metadata app ---")
        print(" template: " + str(self.template))
        print(" totalTime: " + str(self.totalTime))
        print(" pages: " + str(self.pages))
        print(" words: " + str(self.words))
        print(" characters: " + str(self.characters))
        print(" application: " + str(self.application))
        print(" docSecurity: " + str(self.docSecurity))
        print(" lines: " + str(self.lines))
        print(" paragraphs: " + str(self.paragraphs))
        print(" scaleCrop: " + str(self.scaleCrop))
        print(" company: " + str(self.company))
        print(" linksUpToDate: " + str(self.linksUpToDate))
        print(" charactersWithSpaces: " + str(self.charactersWithSpaces))
        print(" shareDoc:" + str(self.shareDoc))
        print(" hyperlinksChanged:" + str(self.hyperlinksChanged))
        print(" appVersion:" + str(self.appVersion))

        print("\n --- Metadata core ---")
        print(" title:" + str(self.title))
        print(" subject:" + str(self.subject))
        print(" creator:" + str(self.creator))
        print(" keywords:" + str(self.keywords))
        print(" lastModifiedBy:" + str(self.lastModifiedBy))
        print(" revision:" + str(self.revision))
        print(" createdDate:" + str(self.createdDate))
        print(" modifiedDate:" + str(self.modifiedDate))

    def parse_comments(self, data):
        try:
            p = re.compile('w:author="(.*?)" w')
            self.userscomments = p.findall(data)
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

    def parse_data(self):
        return "ok"

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
        res = myparser.parser(self.text)
        return res.emails()

    def getPaths(self):
        res = []
        # res.append(self.revision)
        return res

    def getSoftware(self):
        res = []
        res.append(self.application)
        return res
