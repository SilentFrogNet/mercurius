[![GitHub tag](https://img.shields.io/github/tag/SilentFrogNet/metagoofil2.svg?label=version)](https://github.com/SilentFrogNet/metagoofil2/releases)
[![GitHub license](https://img.shields.io/github/license/SilentFrogNet/metagoofil2.svg)](https://github.com/SilentFrogNet/metagoofil2/blob/master/LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Django.svg)](https://github.com/SilentFrogNet/metagoofil2)
[![GitHub issues](https://img.shields.io/github/issues/SilentFrogNet/metagoofil2.svg?colorB=yellow)](https://github.com/SilentFrogNet/metagoofil2/issues)

###################
# STILL A WORK IN PROGRESS... 
###################

# Mercurius

Started as a fork of Christian Martorella's Metagoofil it has been completely refactored. 
So now it's **_almost_** all new!

## Difference From original (Martorella's version)

  * Ported to Python 3.
  * Changed discovery module to use googlesearch library instead of http.client
  * Added Exif Metadata extractor for images
  * Fixed MSOfficeXMLExtractor to work also with xlsx and pptx
  * Refactored MyParser to extract more data
  * Modernized a bit...


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
  * OpenOffice documents (odt, ods, odp)
  * PDF (pdf)
  * Images with Exif data (jpg/jpeg, tiff)


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


## Changelog 1.0.0:

  * [x] Changed/Fixed Google Search
  * [x] Fixed downloader
  * [ ] Fixed/Enhanced page parser 
  * [ ] Fixed metadataMSOfficeXML extractor
  * [x] Added Image Exif metadata extractor
  * [x] Fixed metadataPDF extractor
  * [x] Removed external projects
  * [ ] Modified cli interface (use click)
  * [ ] Other little fixes



---

## Possible names

Parole chiave usate nella ricerca: saggio, saggezza, segreto, ladro, 

### Mitologia Norrena

 * KVASIR: Il più saggio tra gli dèi; nacque dagli sputi degli Asi e dei Vani, testimoniando con la sua esistenza la pace raggiunta tra le due famiglie divine; viene ucciso da Fialarr e Gallar che dal suo sangue ricaveranno il prezioso idromele della saggezza.
 * ALVIT: La "molto saggia"; appellativo della valchiria amata da Volund.

### Mitologia Egizia
 * THOT: Dio della saggezza e della sapienza inventore della scrittura e patrono degli scribi e delle fasi lunari.
 
### Ladri 
 * CELEO: (in greco antico Κελεός) era un personaggio della mitologia greca, abitante dell'isola di Creta e famoso ladro ardito, di cui si raccontano le gesta.
 * **MERCURIO**: (Mercurius, nome latino del dio greco Hermes, Ερμής) è il protettore dell'eloquenza, del commercio e dei ladri, nella mitologia greca e romana. Essendo il messaggero degli dei viene spesso raffigurato con le ali ai piedi. Viene raffigurato come figlio di Giove e della pleiade Maia.
 * PASSALO: (conosciuto anche come Basala o Olo o Sillo), nella mitologia greca era uno dei due Cercopi. Figlio di Oceano e Tia, era insieme al fratello gemello Acmone uno dei più grandi imbroglioni, ladri e impostori della mitologia greca
 * ACMONE: (in greco antico Ἄsκμων) e conosciuto anche come Euribato o Triballo o Aclemone od Atlanto), nella mitologia greca era uno dei due Cercopi. Figlio di Oceano e Tia, era insieme al fratello gemello Passalo uno dei più grandi imbroglioni, ladri e impostori della mitologia greca 
 
 