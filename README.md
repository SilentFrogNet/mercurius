<pre>
**********************************************
* Metagoofil 2  v1.0                         *
* Coded by Ilario Dal Grande                 *
* Fork of Christian Martorella's Metagoofil  *
* www.silentfrog.net                         *
* ilario.dalgrande@silentfrog.net            *
**********************************************
</pre>

## Difference From original (Martorella's version)

  * Ported to Python 3.
  * Changed googlesearch module to use requests library instead of http.client


## What is this?

Metagoofil is a tool for extracting metadata of public documents (pdf,doc,xls,ppt,etc) availables in the target websites.This information could be useful because you can get valid usernames, people names, for using later in bruteforce password attacks (vpn, ftp, webapps), the tool will also extracts interesting "paths" of the documents, where we can get shared resources names, server names, etc.

This new version will also extract emails addresses from PDF and Word documents content.


## How it works?

The tool first perform a query in Google requesting different filetypes that can have useful metadata (pdf, doc, xls,ppt,etc), then will download those documents to the disk and extracts the metadata of the file using specific libraries for parsing different file types (Hachoir, Pdfminer, etc)


## Dependencies:

All dependencies are excluded again, due to incompatibility with Python 3.

It depends on:
  * pdfminer.six
  * hachoir3
  * requests


## Changelog 1.0:
  - Changed/Fixed Google Search
  - Fixed downloader
  - Fixed/Enhanced page parser 
  - Fixed metadataMSOfficeXML parser
  - Fixed metadataPDF parser
  - Removed external projects
  - Added Image Exif metadata extractor
  - Modified cli interface
