[![GitHub tag](https://img.shields.io/github/tag/SilentFrogNet/mercurius.svg?label=version)](https://github.com/SilentFrogNet/mercurius/releases)
[![GitHub license](https://img.shields.io/github/license/SilentFrogNet/mercurius.svg)](https://github.com/SilentFrogNet/mercurius/blob/master/LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Django.svg)](https://github.com/SilentFrogNet/mercurius)
[![GitHub issues](https://img.shields.io/github/issues/SilentFrogNet/mercurius.svg?colorB=yellow)](https://github.com/SilentFrogNet/mercurius/issues)


###################
# STILL A WORK IN PROGRESS... 
###################

# Mercurius

Started as a fork of Christian Martorella's Metagoofil it has been completely refactored. 
So now it's **_almost_** all new!


## Install

  * From git

    `pip install git+git://github.com/SilentFrogNet/mercurius.git`


## Origin of the Name

The name **Mercurius** is inspired from the greek god Hermes. Among the others he is the god of _luck_, _trickery_ and _thieves_.

He is also known as the "keeper of the boundaries" for his role as bridge between the upper and lower worlds. 


## What is this?

Mercurius is a tool for extracting metadata of public documents 
(pdf, doc, xls, ppt, docx, xlsx, pptx, odt, ods, odp, jpg, jpeg, tiff) 
availables in the target websites.This information could be useful because you can 
get valid usernames, people names, hosts, emails,... for using later in bruteforce password 
attacks (vpn, ftp, webapps).


## How it works?

The tool first perform a query in Google requesting different file types that can have 
useful metadata (pdf, doc, xls, ppt,...), then will download those documents to the disk and 
extracts the metadata of the file using specific libraries for parsing different file types (Hachoir, Pdfminer, etc)


## Supported file types

At the moment this tool can parse and extract metadata from:
  * Microsoft Office 97 documents (doc, xls, ppt)
  * Microsoft Office 2k+ documents (docx, xlsx, pptx)
  * PDF (pdf)
  * Images with Exif data (jpg/jpeg, tiff)
  * OpenOffice documents (odt, ods, odp)  <- NOT YET
  * Apple Office documents (pages, numbers, key)  <- NOT YET


## Difference From original (Martorella's version)

  * Ported to Python 3.
  * Changed discovery module to use googlesearch library instead of http.client
  * Added Exif Metadata extractor for images
  * Fixed MSOfficeXMLExtractor to work also with xlsx and pptx
  * Refactored MyParser to extract more data
  * Modernized a bit...


## Dependencies:

All dependencies are excluded again, due to incompatibility with Python 3.

It depends on:
  * [**pdfminer.six**](https://github.com/pdfminer/pdfminer.six/)
  * [**hachoir3**](https://pypi.org/project/hachoir3/)
  * [**requests**](http://docs.python-requests.org/en/master/)
  * [**Pillow**](https://pillow.readthedocs.io/en/latest/)
  * [**bs4**](https://www.crummy.com/software/BeautifulSoup/)
  * [**click**](http://click.pocoo.org/6/)
  * [**termcolor**](https://pypi.org/project/termcolor/)
  * [**colorama**](https://github.com/tartley/colorama)
  * [**spinner**](https://github.com/SilentFrogNet/spinner)
  * [**addict**](https://github.com/mewwts/addict)


## Working extractors:

  * [x] PDFExtractor
  * [x] ImageExtractor
  * [x] MSOfficeExtractor
  * [ ] MSOfficeXMLExtractor
  * [ ] OpenOfficeExtractor
  * [ ] AppleOfficeExtractor


## Changelog 1.0.0:

  * [x] Changed/Fixed Google Search
  * [ ] Integrated [Bing Search](https://docs.microsoft.com/it-it/azure/cognitive-services/bing-web-search/quickstarts/python)
  * [ ] Integrated Exalead Search (?????)
  * [x] Fixed downloader
  * [ ] Fixed/Enhanced page parser 
  * [ ] Fixed metadataMSOfficeXML extractor
  * [x] Added Image Exif metadata extractor
  * [x] Fixed metadataPDF extractor
  * [x] Removed external projects
  * [x] Modified cli interface (use click)
    * [x] Manage context application
        * [ ] keep track of already downloaded files
        * [x] keep domain context
        * [ ] further searches on the same domain will extend data
        * [ ] if domain is changed or local analysis is performed, ask to cleanup or extend 
  * [x] Ascii Art random banner like metasploit ;)
  * [ ] Other little fixes
  * [ ] Does make it python-agnostic? (working both on python 2 and 3) with [**six**](https://github.com/benjaminp/six)
  * [ ] Move all dependencies to setup.py file
  * [x] Setup a plugin architecture for the extractors with [**pluggy**](https://github.com/pytest-dev/pluggy)
