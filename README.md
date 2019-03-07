[![Travis build](https://travis-ci.org/SilentFrogNet/mercurius.svg?branch=master)](https://travis-ci.org/SilentFrogNet/mercurius/builds)
[![codecov](https://codecov.io/gh/SilentFrogNet/mercurius/branch/master/graph/badge.svg)](https://codecov.io/gh/SilentFrogNet/mercurius)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Django.svg)](https://github.com/SilentFrogNet/mercurius)
[![GitHub license](https://img.shields.io/github/license/SilentFrogNet/mercurius.svg)](https://github.com/SilentFrogNet/mercurius/blob/master/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/SilentFrogNet/mercurius.svg?colorB=yellow)](https://github.com/SilentFrogNet/mercurius/issues)
<!-- [![GitHub tag](https://img.shields.io/github/tag/SilentFrogNet/mercurius.svg?label=version)](https://github.com/SilentFrogNet/mercurius/releases) -->


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
  * Images with Exif data (jpg/jpeg, tif/tiff)
  * OpenOffice documents (odt, ods, odp)  **<- _NOT YET_**
  * Apple Office documents (pages, numbers, key)  **<- _NOT YET_**


## Available extractors

Those are the available extractors:
  * [x] PDFExtractor
  * [x] ImageExtractor
  * [x] MSOfficeExtractor
  * [x] MSOfficeXMLExtractor
  * [ ] OpenOfficeExtractor
  * [ ] AppleOfficeExtractor
  
The tool implements a plugin architecture though [pluggy system](https://pluggy.readthedocs.io/en/latest/).

To enable a new plugin it must be put in the `mercurius/extractors` folder and then enabled through the configuration file with an entry like `<plugin_file_name>=<class_extractor_name>`.
  
  
## Quick start
  

## Working on features (_for the future_):

  * [ ] Integrate [Bing Search](https://docs.microsoft.com/it-it/azure/cognitive-services/bing-web-search/quickstarts/python)
  * [ ] Integrate [Exalead Search](https://www.exalead.com/search/)
  * [ ] Make it python-agnostic? (working both on python 2 and 3) with [**six**](https://github.com/benjaminp/six)
  * [ ] Manage applications's context
    * [ ] Keep track of already downloaded files
    * [x] Keep domain context
      * [ ] Further searches on the same domain will extend data
      * [ ] if domain is changed or local analysis is performed, ask to cleanup or extend
  * [ ] Change plugin system...move from "_pick from folder_" to "_get through setuptools_"


## Changelog 1.0.0:

  * [x] Changed/Fixed Google Search
  * [x] Fixed downloader
  * [ ] Fixed/Enhanced page parser 
  * [ ] Fixed metadataMSOfficeXML extractor
  * [x] Added Image Exif metadata extractor
  * [x] Fixed metadataPDF extractor
  * [x] Removed external projects
  * [x] Modified _cli_ interface (using click)
  * [x] Added _shell_ interface (using a modified version of click-shell) 
  * [x] Ascii Art random banner like metasploit ;)
  * [ ] Other little fixes
  * [x] Move all dependencies to setup.py file
  * [x] Setup a plugin architecture for the extractors with [**pluggy**](https://github.com/pytest-dev/pluggy)
