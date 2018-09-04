import string
import re

from bs4 import BeautifulSoup


class parser:
    def __init__(self, results, word=""):
        self.results = results
        self.word = word
        self.temp = []

    def hostnames(self, domain=None):
        if domain is None:
            domain = self.word
        reg_hosts = re.compile('[a-zA-Z0-9.-]*\.' + domain)
        hosts = self.unique(reg_hosts.findall(self.results))
        return hosts

    def hostnames_all(self):
        reg_hosts = re.compile('<cite>(.*?)</cite>')
        temp = reg_hosts.findall(self.results)
        for x in temp:
            if x.count(':'):
                res = x.split(':')[1].split('/')[2]
            else:
                res = x.split("/")[0]
            temp.append(res)
        hostnames = self.unique(temp)
        return hostnames

    def emails(self):
        reg_emails = re.compile('[a-zA-Z0-9.-_]+@[a-zA-Z0-9.-]+')
        emails = self.unique(reg_emails.findall(self.results))
        return emails

    @staticmethod
    def unique(lst):
        return list(set(lst))

    # def genericClean(self):
    #     self.results = re.sub('<em>', '', self.results)
    #     self.results = re.sub('<b>', '', self.results)
    #     self.results = re.sub('</b>', '', self.results)
    #     self.results = re.sub('</em>', '', self.results)
    #     self.results = re.sub('%2f', ' ', self.results)
    #     self.results = re.sub('%3a', ' ', self.results)
    #     self.results = re.sub('<strong>', '', self.results)
    #     self.results = re.sub('</strong>', '', self.results)
    #     self.results = re.sub('<w:t>', ' ', self.results)
    #
    #     for e in ('>', ':', '=', '<', '/', '\\', ';', '&', '%3A', '%3D', '%3C'):
    #         self.results = self.results.replace(e, ' ')

    def urlClean(self):
        self.results = re.sub('<em>', '', self.results)
        self.results = re.sub('</em>', '', self.results)
        self.results = re.sub('%2f', ' ', self.results)
        self.results = re.sub('%3a', ' ', self.results)
        for e in ('<', '>', ':', '=', ';', '&', '%3A', '%3D', '%3C'):
            self.results = self.results.replace(e, ' ')

    def fileurls(self, filetype=None):
        urls = []
        soup = BeautifulSoup(self.results, 'html.parser')
        links = [l.get('href', '') for l in soup.find_all('a', href=True)]
        allurls = self.unique(links)
        for z in allurls:
            y = z.replace('/url?q=', '')
            x = y.split('&')[0]
            if x.count('webcache') or x.count('google.com') or x.count('search?') or x.count('about.html') or x.count('privacy.html') or x.count('ads/') or x.count('services/') or x == "#" or x == "/":
                pass
            else:
                if filetype is not None and x.endswith(filetype):
                    urls.append(x)
        return urls

    def people_linkedin(self):
        reg_people = re.compile('">[a-zA-Z0-9._ -]* profiles | LinkedIn')

        self.temp = reg_people.findall(self.results)
        resul = []
        for x in self.temp:
            y = x.replace('  LinkedIn', '')
            y = y.replace(' profiles ', '')
            y = y.replace('LinkedIn', '')
            y = y.replace('"', '')
            y = y.replace('>', '')
            if y != " ":
                resul.append(y)
        return resul

    def profiles(self):
        reg_people = re.compile('">[a-zA-Z0-9._ -]* - <em>Google Profile</em>')
        self.temp = reg_people.findall(self.results)
        resul = []
        for x in self.temp:
            y = x.replace(' <em>Google Profile</em>', '')
            y = y.replace('-', '')
            y = y.replace('">', '')
            if y != " ":
                resul.append(y)
        return resul
