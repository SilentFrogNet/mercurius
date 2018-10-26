class FileTypes:
    PDF = "pdf"

    DOC = "doc"
    XLS = "xls"
    PPT = "ppt"

    DOCX = "docx"
    XLSX = "xlsx"
    PPTX = "pptx"

    ODT = "odt"
    ODS = "ods"
    ODP = "odp"

    PAGES = "pages"
    NUMBERS = "numbers"
    KEY = "key"

    JPG = "jpg"
    JPEG = "jpeg"
    TIF = "tif"
    TIFF = "tiff"

    MS_OFFICE = [DOC, XLS, PPT]
    MS_OFFICE_XML = [DOCX, XLSX, PPTX]
    OPEN_OFFICE = [ODT, ODS, ODP]
    APPLE_OFFICE = [PAGES, NUMBERS, KEY]
    IMAGES = [JPG, JPEG, TIF, TIFF]

    ALL = [PDF] + MS_OFFICE + MS_OFFICE_XML + OPEN_OFFICE + IMAGES + APPLE_OFFICE

    SPECIAL_GROUPS = {
        "ALL": ALL,
        "OFFICE": MS_OFFICE,
        "XOFFICE": MS_OFFICE_XML,
        "OPEN_OFFICE": OPEN_OFFICE,
        "IMAGES": IMAGES
    }

    @classmethod
    def to_string(cls):
        return ", ".join(cls.ALL)

    @classmethod
    def special_groups(cls):
        return ", ".join(cls.SPECIAL_GROUPS.keys())
