import string
import http.client, sys
import myparser
import re
import time

import requests


class SearchGoogle:

    def __init__(self, word, limit, start, filetype):
        self.word = word
        self.results = ""
        self.totalresults = ""
        self.filetype = filetype
        self.server = "www.google.com"
        self.hostname = "www.google.com"
        self.userAgent = "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"
        self.quantity = "100"
        self.limit = limit
        self.counter = start

    def do_search_files(self):
        url = "https://{server}/search?num={quantity}&start={counter}&hl=en&meta=&q=filetype:{filetype}%20site:{site}&filter=0".format(
            server=self.server,
            quantity=self.quantity,
            counter=self.counter,
            filetype=self.filetype,
            site=self.word
        )
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            self.results = r.text
        self.totalresults += self.results

    def get_emails(self):
        rawres = myparser.parser(self.totalresults, self.word)
        return rawres.emails()

    def get_hostnames(self):
        rawres = myparser.parser(self.totalresults, self.word)
        return rawres.hostnames()

    def get_files(self):
        rawres = myparser.parser(self.totalresults, self.word)
        return rawres.fileurls(self.filetype)

    def process_files(self):
        while self.counter < self.limit:
            self.do_search_files()
            time.sleep(1)
            self.counter += 100
            print("\tSearching " + str(self.counter) + " results...")
