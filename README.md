[![GitHub tag](https://img.shields.io/github/tag/SilentFrogNet/metagoofil2.svg?label=version)](https://github.com/SilentFrogNet/metagoofil2/releases)
[![GitHub license](https://img.shields.io/github/license/SilentFrogNet/metagoofil2.svg)](https://github.com/SilentFrogNet/metagoofil2/blob/master/LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Django.svg)](https://github.com/SilentFrogNet/metagoofil2)
[![GitHub issues](https://img.shields.io/github/issues/SilentFrogNet/metagoofil2.svg?colorB=yellow)](https://github.com/SilentFrogNet/metagoofil2/issues)

###################
# STILL A WORK IN PROGRESS... 
###################


# Metagoofil 2

Started as a fork of Christian Martorella's Metagoofil it has been completely refactored. So now it's _almost_ all new!

## Difference From original (Martorella's version)

  * Ported to Python 3.
  * Changed discovery module to use googlesearch library instead of http.client
  * Added Exif Metadata extractor for images


## What is this?

Metagoofil is a tool for extracting metadata of public documents (pdf, doc, xls, ppt,...) 
availables in the target websites.This information could be useful because you can 
get valid usernames, people names, for using later in bruteforce password 
attacks (vpn, ftp, webapps), the tool will also extracts interesting emails, hosts,...


## Supported file types

At the moment this tool supports:
  * Microsoft Office 97 documents (doc, xls, ppt)
  * Microsoft Office 2k+ documents (docx, xlsx, pptx)
  * OpenOffice documents (odt, ods, odp)
  * PDF (pdf)
  * Images with Exif data (jpg/jpeg, tiff)

## How it works?

The tool first perform a query in Google requesting different filetypes that can have 
useful metadata (pdf, doc, xls, ppt,...), then will download those documents to the disk and 
extracts the metadata of the file using specific libraries for parsing different file types (Hachoir, Pdfminer, etc)


## Dependencies:

All dependencies are excluded again, due to incompatibility with Python 3.

It depends on:
  * [**pdfminer.six**](https://github.com/pdfminer/pdfminer.six/)
  * [**hachoir3**](https://pypi.org/project/hachoir3/)
  * [**requests**](http://docs.python-requests.org/en/master/)
  * [**click**](http://click.pocoo.org/6/)
  * [**spinner**](https://github.com/SilentFrogNet/spinner)


## Changelog 1.0.0:
  - [x] Changed/Fixed Google Search
  - [x] Fixed downloader
  - [ ] Fixed/Enhanced page parser 
  - [ ] Fixed metadataMSOfficeXML extractor
  - [x] Added Image Exif metadata extractor
  - [x] Fixed metadataPDF extractor
  - [x] Removed external projects
  - [ ] Modified cli interface (use click)
