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

    JPG = "jpg"
    JPEG = "jpeg"
    TIFF = "tiff"

    MS_OFFICE = [DOC, XLS, PPT]
    MS_OFFICE_XML = [DOCX, XLSX, PPTX]
    OPEN_OFFICE = [ODT, ODS, ODP]
    IMAGES = [JPG, JPEG, TIFF]

    ALL = [PDF] + MS_OFFICE + MS_OFFICE_XML + OPEN_OFFICE + IMAGES

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
