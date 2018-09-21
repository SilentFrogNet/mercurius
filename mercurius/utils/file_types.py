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

    @classmethod
    def to_string(cls):
        return ", ".join([cls.PDF] + cls.MS_OFFICE + cls.MS_OFFICE_XML + cls.OPEN_OFFICE + cls.IMAGES)
