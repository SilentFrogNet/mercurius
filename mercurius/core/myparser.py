import string
import re

from bs4 import BeautifulSoup


class DataParser:

    def __init__(self, domain=None):
        self.domain = domain

    def hostnames(self, data, domain=None):
        if domain is None:
            domain = self.domain
        reg_hosts = re.compile('[a-zA-Z0-9.-]*\.' + domain)
        hosts = self.unique(reg_hosts.findall(data))
        return hosts

    def hostnames_all(self, data):
        reg_hosts = re.compile('<cite>(.*?)</cite>')
        temp = reg_hosts.findall(data)
        for x in temp:
            if x.count(':'):
                res = x.split(':')[1].split('/')[2]
            else:
                res = x.split("/")[0]
            temp.append(res)
        hostnames = self.unique(temp)
        return hostnames

    def emails(self, data):
        reg_emails = re.compile('[a-zA-Z0-9.-_]+@[a-zA-Z0-9.-]+')
        emails = self.unique(reg_emails.findall(data))
        return emails

    @staticmethod
    def unique(lst):
        return list(set(lst))

    # def genericClean(self):
    #     data = re.sub('<em>', '', data)
    #     data = re.sub('<b>', '', data)
    #     data = re.sub('</b>', '', data)
    #     data = re.sub('</em>', '', data)
    #     data = re.sub('%2f', ' ', data)
    #     data = re.sub('%3a', ' ', data)
    #     data = re.sub('<strong>', '', data)
    #     data = re.sub('</strong>', '', data)
    #     data = re.sub('<w:t>', ' ', data)
    #
    #     for e in ('>', ':', '=', '<', '/', '\\', ';', '&', '%3A', '%3D', '%3C'):
    #         data = data.replace(e, ' ')

    # def urlClean(self):
    #     data = re.sub('<em>', '', data)
    #     data = re.sub('</em>', '', data)
    #     data = re.sub('%2f', ' ', data)
    #     data = re.sub('%3a', ' ', data)
    #     for e in ('<', '>', ':', '=', ';', '&', '%3A', '%3D', '%3C'):
    #         data = data.replace(e, ' ')
    #
    # def fileurls(self, filetype=None):
    #     urls = []
    #     soup = BeautifulSoup(data, 'html.DataParser')
    #     links = [l.get('href', '') for l in soup.find_all('a', href=True)]
    #     allurls = self.unique(links)
    #     for z in allurls:
    #         y = z.replace('/url?q=', '')
    #         x = y.split('&')[0]
    #         if x.count('webcache') or x.count('google.com') or x.count('search?') or x.count('about.html') or x.count('privacy.html') or x.count('ads/') or x.count('services/') or x == "#" or x == "/":
    #             pass
    #         else:
    #             if filetype is not None and x.endswith(filetype):
    #                 urls.append(x)
    #     return urls
    #
    # def people_linkedin(self):
    #     reg_people = re.compile('">[a-zA-Z0-9._ -]* profiles | LinkedIn')
    #
    #     temp = reg_people.findall(data)
    #     resul = []
    #     for x in temp:
    #         y = x.replace('  LinkedIn', '')
    #         y = y.replace(' profiles ', '')
    #         y = y.replace('LinkedIn', '')
    #         y = y.replace('"', '')
    #         y = y.replace('>', '')
    #         if y != " ":
    #             resul.append(y)
    #     return resul
    #
    # def profiles(self):
    #     reg_people = re.compile('">[a-zA-Z0-9._ -]* - <em>Google Profile</em>')
    #     temp = reg_people.findall(data)
    #     resul = []
    #     for x in temp:
    #         y = x.replace(' <em>Google Profile</em>', '')
    #         y = y.replace('-', '')
    #         y = y.replace('">', '')
    #         if y != " ":
    #             resul.append(y)
    #     return resul
