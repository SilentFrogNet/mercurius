import os
import re
import socket

from bs4 import BeautifulSoup


class DataParser:

    def hostnames(self, data):
        reg_hosts = re.compile(r'(((ht|f)tp(s)?:\/\/)?(w{0,3}\.)?[a-zA-Z0-9_\-\.\:\#\/\~\}]+(\.[a-zA-Z]{1,4})(\/[a-zA-Z0-9_\-\.\:\#\/\~\}]*)?)')
        h1 = [h[0] for h in reg_hosts.findall(data)]

        reg_hosts2 = re.compile(r'^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$')
        h2 = reg_hosts2.findall(data)

        reg_ips = re.compile(r'^([0-9]{1,3}.){3}[0-9]{1,3}($|\/([0-9]|[1-2][0-9]|3[0-2])$)')
        h3 = reg_ips.findall(data)

        return self.strip_unreachable_hosts(self.unique(h1 + h2 + h3))

    def emails(self, data):
        reg_emails = re.compile(r'(([\d\w]+[\.\w\d]*)\+?([\.\w\d]*)?@([\w\d]+[\.\w\d]*))')
        emails = self.unique([e[0] for e in reg_emails.findall(data)])
        return emails

    @staticmethod
    def unique(lst):
        return list(set(lst))

    @staticmethod
    def strip_unreachable_hosts(hosts):
        ret = []
        for h in hosts:
            try:
                socket.gethostbyname(h)
                ret.append(h)
            except socket.gaierror:
                pass
        return ret

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
    #     reg_people = re.compile(r'">[a-zA-Z0-9._ -]* profiles | LinkedIn')
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
    #     reg_people = re.compile(r'">[a-zA-Z0-9._ -]* - <em>Google Profile</em>')
    #     temp = reg_people.findall(data)
    #     resul = []
    #     for x in temp:
    #         y = x.replace(' <em>Google Profile</em>', '')
    #         y = y.replace('-', '')
    #         y = y.replace('">', '')
    #         if y != " ":
    #             resul.append(y)
    #     return resul
