import os
import sys
import argparse
import threading
import random
import googlesearch
import queue
import requests

from extractors import metadataExtractor, metadataMSOffice, metadataMSOfficeXML, metadataOpenOffice, metadataPDF
from utils import Spinner

stop_workers = threading.Event()


class MetaWorker(threading.Thread):

    def __init__(self, id, input_queue, mg, timeout=1):
        super(MetaWorker, self).__init__()
        self.daemon = True

        self.id = id
        self.name = "worker" + str(self.id)
        self.input_queue = input_queue
        self.mg = mg
        self.timeout = timeout

    def run(self):
        while not stop_workers.is_set():
            try:
                item = self.input_queue.get(True, self.timeout)
                if item:
                    self.do_work(item)
            except queue.Empty:
                # raised by queue.get if we reach the timeout on an empty queue
                continue
            self.input_queue.task_done()

    def do_work(self, url):
        dest_path = self.download_file(url)
        self.parse_file(dest_path)

    def download_file(self, url):
        # Strip any trailing /'s before extracting file name.
        filename = str(url.strip('/').split('/')[-1])
        dest_path = os.path.join(mg.save_directory, filename)

        try:
            headers = {
                'User-Agent': random.choice(self.mg.random_user_agents)
            }
            response = requests.get(url, headers=headers, verify=False, timeout=self.mg.url_timeout, stream=True)

            # Download the file.
            if response.status_code == requests.codes.ok:
                try:
                    size = int(response.headers["Content-Length"])
                except KeyError as e:
                    size = len(response.content)

                print("[*] Downloading file - [{0} bytes] {1}".format(size, url))

                with open(dest_path, "wb") as fh:
                    for chunk in response:
                        if chunk:
                            fh.write(chunk)

                print("[+] File {} downloaded.".format(url))
            else:
                print("[-] URL {0} returned HTTP code {1}".format(url, response.status_code))
        except requests.exceptions.RequestException as e:
            print("[-] Exception for url: {0} -- {1}".format(url, e))

        return dest_path

    def parse_file(self, path):
        raw = None
        users = []
        paths = []
        soft = None
        emails = []
        failedfiles = []

        working_dir = os.path.dirname(os.path.realpath(path))
        filename, filetype = os.path.splitext(os.path.basename(path))

        print("[*] Parsing file {}{}...".format(filename, filetype))

        if filetype == ".pdf":
            metaparser = metadataPDF.Metapdf(path)
        elif filetype == "doc" or filetype == "ppt" or filetype == "xls":
            metaparser = metadataMSOffice.MetaMs2k(path)
            if os.name == "posix":
                metaparserex = metadataExtractor.MetaExtractor(path)
        elif filetype == "docx" or filetype == "pptx" or filetype == "xlsx":
            metaparser = metadataMSOfficeXML.MetaInfoMS(path)

        if metaparserex:  # TODO: check
            metaparserex.getData()
            users = metaparserex.getUsers()
            paths = metaparserex.getPaths()

        res = metaparser.getData()
        if res == "ok":
            raw = metaparser.getRaw()
            users = metaparser.getUsers()
            paths = metaparser.getPaths()
            soft = metaparser.getSoftware()
            email = []
            if filetype == "pdf" or filetype == "docx":
                res = metaparser.getTexts()
                if res == "ok":
                    email = metaparser.getEmails()
                    for em in email:
                        emails.append(em)
                else:
                    email = []
                    failedfiles.append("{}{}:{}".format(filename,filetype,str(res)))
            # respack = [x, users, paths, soft, raw, email]
            # all.append(respack)
        else:
            failedfiles.append("{}{}:{}".format(filename,filetype,str(res)))
            print("\t [x] Error in the parsing process")  # A error in the parsing process


class Metagoofil(object):

    def __init__(self, domain, file_types, save_directory, delay=30, url_timeout=15, search_max=100, download_file_limit=100, number_of_threads=8, quiet=False, local=False):
        self.domain = domain
        self.file_types = file_types
        self.save_directory = save_directory
        self.delay = delay
        self.url_timeout = url_timeout
        self.search_max = search_max
        self.download_file_limit = download_file_limit
        self.quiet = quiet
        self.local = local
        self.files = []

        if os.path.exists('user_agents.txt'):
            with open('user_agents.txt') as fp:
                self.random_user_agents = fp.read().splitlines()
        else:
            self.random_user_agents = [
                "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
            ]

        self.number_of_threads = number_of_threads
        self.workers = []
        self.queue = queue.Queue()

    def go(self):
        if self.local:
            self.local_go()
        else:
            self.remote_go()

    def local_go(self):
        print("[*] Starting local search...")

        pass

    def remote_go(self):
        for i in range(self.number_of_threads):
            w = MetaWorker(i, self.queue, self)
            w.start()
            self.workers.append(w)

        for filetype in self.file_types:
            self.files = []  # Stores URLs with files, clear out for each filetype.

            print_string = "[*] Searching online for '{}' files for domain {}...".format(filetype, self.domain)
            stop_spinner = threading.Event()
            spin_thread = Spinner(stop_spinner, prefix=print_string)
            spin_thread.start()

            query = "filetype:{0} site:{1}".format(filetype, self.domain)
            user_agent = random.choice(self.random_user_agents)
            for url in googlesearch.search(query, start=0, stop=self.search_max, num=100, extra_params={'filter': '0'}, user_agent=user_agent):  # TODO: check if pause=self.delay is needed
                self.files.append(url)

            stop_spinner.set()
            spin_thread.join()
            print(print_string + "DONE")

            # Since googlesearch.search method retreives URLs in batches of 100, ensure the file list only contains the requested amount.
            if len(self.files) > self.search_max:
                self.files = self.files[:-(len(self.files) - self.search_max)]

            if self.quiet:
                # Otherwise, just display them.
                print("[*] Results: {0} {1} files found".format(len(self.files), filetype))
                for file_name in self.files:
                    print(file_name)
            else:
                print_string = "Downloading and analyzing files..."
                stop_spinner = threading.Event()
                spin_thread = Spinner(stop_spinner, prefix=print_string)
                spin_thread.start()

                # If it's not quiet mode download and analyze files
                if len(self.files) > self.download_file_limit:
                    self.files = self.files[:self.download_file_limit + 1]
                [self.queue.put(url) for url in self.files]

                self.queue.join()
                stop_workers.set()
                for w in self.workers:
                    w.join()

                stop_spinner.set()
                spin_thread.join()
                print(print_string + "DONE")

    def download(self):
        counter = 1
        for url in self.files:
            if counter <= self.download_file_limit:
                self.queue.put(url)
                counter += 1

        self.queue.join()


def csv_list(string):
    return string.split(',')


def banner():
    print("\n")
    print("******************************************************************")
    print("*     /\/\   ___| |_ __ _  __ _  ___   ___  / _(_) |   |__  \    *")
    print("*    /    \ / _ \ __/ _` |/ _` |/ _ \ / _ \| |_| | |      ) |    *")
    print("*   / /\/\ \  __/ || (_| | (_| | (_) | (_) |  _| | |     / /_    *")
    print("*   \/    \/\___|\__\__,_|\__, |\___/ \___/|_| |_|_|    |____|   *")
    print("*                         |___/                                  *")
    print("* Metagoofil 2  v1.0                                             *")
    print("* Fork of Christian Martorella's Metagoofil                      *")
    print("* Ilario Dal Grande                                              *")
    print("* SilentFrog.net                                                 *")
    print("* ilario.dalgrande_at_silentfrog.net                             *")
    print("******************************************************************")
    print("\n")


if __name__ == '__main__':
    banner()

    parser = argparse.ArgumentParser(description='Metagoofil - Search and download specific filtypes')
    parser.add_argument('-d', dest='domain', action='store', required=True, help='Domain to search.')
    parser.add_argument('-e', dest='delay', action='store', type=float, default=30.0, help='Delay (in seconds) between searches.  If it\'s too small Google may block your IP, too big and your search may take a while.  DEFAULT: 30.0')
    parser.add_argument('-i', dest='url_timeout', action='store', type=int, default=15, help='Number of seconds to wait before timeout for unreachable/stale pages.  DEFAULT: 15')
    parser.add_argument('-s', dest='search_max', action='store', type=int, default=100, help='Maximum results to search.  DEFAULT: 100')
    parser.add_argument('-n', dest='download_file_limit', default=100, action='store', type=int, help='Maximum number of files to download per filetype.  DEFAULT: 100')
    parser.add_argument('-o', dest='save_directory', action='store', default=os.getcwd(), help='Directory to save downloaded files.  DEFAULT is cwd, "."')
    parser.add_argument('-r', dest='number_of_threads', action='store', type=int, default=8, help='Number of search threads.  DEFAULT: 8')
    parser.add_argument('-t', dest='file_types', action='store', required=True, type=csv_list, help='file_types to download (pdf,doc,xls,ppt,odp,ods,docx,xlsx,pptx).')
    parser.add_argument('-q', dest='quiet', action='store_true', default=False, help='In quiet mode, it doesn\'t download the files, it\'ll just viewing search results.')
    parser.add_argument('-l', dest='local', action='store_true', default=False, help='Performs the metadata search on local files only.')

    args = parser.parse_args()

    if args.save_directory:
        print("[*] Downloaded files will be saved here: {0}".format(args.save_directory))
        if not os.path.exists(args.save_directory):
            print("[+] Creating folder: {0}".format(args.save_directory))
            os.mkdir(args.save_directory)
    if args.delay < 0:
        print("[!] Delay must be greater than 0")
        sys.exit()
    if args.url_timeout < 0:
        print("[!] URL timeout (-i) must be greater than 0")
        sys.exit()
    if args.number_of_threads < 0:
        print("[!] Number of threads (-n) must be greater than 0")
        sys.exit()

    mg = Metagoofil(**vars(args))
    mg.go()

    print("[+] Done!")
