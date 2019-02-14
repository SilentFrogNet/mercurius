import os
import threading
import random
import googlesearch
import queue

from spinner import Spinner
from mercurius.utils.logger import Logger, LogTypes
from mercurius.core.meta_worker import MetaWorker
from mercurius.utils.item_store import ItemStore

stop_workers = threading.Event()


class Mercurius:
    DEFAULT_DELAY = 30
    DEFAULT_TIMEOUT = 15
    DEFAULT_SEARCH_MAX = 100
    DEFAULT_DOWNLOAD_LIMIT = 100

    def __init__(self, configs, domain, file_types, out_directory, number_of_threads=8, verbose=False, stealth=False, logger=None):
        self.configs = configs
        self.domain = domain
        self.file_types = file_types
        self.out_directory = out_directory
        self.verbose = verbose
        self.stealth = stealth
        if logger:
            self.logger = logger
        else:
            self.logger = Logger(type=LogTypes.TO_SCREEN)

        self.files = []
        self.all_users = []
        self.all_emails = []
        self.all_hosts = []

        if os.path.exists('user_agents.txt'):
            with open('user_agents.txt') as fp:
                self.random_user_agents = fp.read().splitlines()
        else:
            self.random_user_agents = [
                "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
                "Opera/9.80 (Windows NT 5.2; U; en) Presto/2.2.15 Version/10.00",
                "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; pl; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 FBSMTWB"
            ]

        self.number_of_threads = number_of_threads
        self.workers = []
        self.input_queue = queue.Queue()
        self.output_store = ItemStore()

    def go(self, is_local, delay=DEFAULT_DELAY, url_timeout=DEFAULT_TIMEOUT, search_max=DEFAULT_SEARCH_MAX, download_file_limit=DEFAULT_DOWNLOAD_LIMIT):
        for i in range(self.number_of_threads):
            w = MetaWorker(i, self.input_queue, self.output_store, stop_workers, self, is_local=is_local, logger=self.logger)
            w.start()
            self.workers.append(w)

        if is_local:
            self._local_go()
        else:
            self._remote_go(delay, url_timeout, search_max, download_file_limit)

        self._collect_results()

    def _local_go(self):
        self.logger.info("Starting local search...")

        if self.out_directory is None:
            self.logger.error("No directory specified. Abort!")
            return

        if self.stealth:
            # If stealth just display collected files.
            self.logger.info("List of files to analyze in \"{}\": ".format(self.out_directory))
            working_dir = os.path.realpath(self.out_directory)
            for file_name in os.listdir(working_dir):
                print("  * " + file_name)
        else:
            print_string = "Analyzing local files..."
            stop_spinner = None
            spin_thread = None
            if not self.logger.can_log():
                stop_spinner = threading.Event()
                spin_thread = Spinner(stop_spinner, prefix=print_string)
                spin_thread.start()

            working_dir = os.path.realpath(self.out_directory)
            for file in os.listdir(working_dir):
                self.input_queue.put(os.path.join(working_dir, file))

            self._finish_work()

            if not self.logger.can_log() and stop_spinner is not None and spin_thread is not None:
                stop_spinner.set()
                spin_thread.join()

            self.logger.success(print_string + "DONE")

    def _remote_go(self, delay, url_timeout, search_max, download_file_limit):
        self.logger.info("Starting remote search...")

        for filetype in self.file_types:
            self.files = []  # Stores URLs with files, clear out for each filetype.

            print_string = "Searching online for '{}' files in {}...".format(filetype, self.domain)
            stop_spinner = threading.Event()
            spin_thread = Spinner(stop_spinner, prefix="[*] Info: {}".format(print_string))
            spin_thread.start()

            self.files = self._get_docs_by_filetype(filetype, search_max)

            stop_spinner.set()
            spin_thread.join()
            self.logger.success(print_string + "DONE")

            if self.stealth:
                # If stealth just display collected files.
                self.logger.info("Results: {0} {1} files found".format(len(self.files), filetype))
                for file_name in self.files:
                    print("  * " + file_name)
            else:
                # Otherwise download and analyze them
                print_string = "Downloading and analyzing files..."
                stop_spinner = threading.Event()
                spin_thread = Spinner(stop_spinner, prefix="[*] Info: {}".format(print_string))
                spin_thread.start()

                # If it's not stealth mode download and analyze files
                if len(self.files) > download_file_limit:
                    self.files = self.files[:download_file_limit + 1]
                [self.input_queue.put(url) for url in self.files]

                stop_spinner.set()
                spin_thread.join()
                self.logger.success(print_string + "DONE")

        self._finish_work()

    def _finish_work(self):
        self.input_queue.join()
        stop_workers.set()
        for w in self.workers:
            w.join()
        self.workers = []

    def _get_docs_by_filetype(self, filetype, search_max):
        query = "filetype:{0} site:{1}".format(filetype, self.domain)
        user_agent = random.choice(self.random_user_agents)

        files = []

        for url in googlesearch.search(query, start=0, stop=search_max, num=100, extra_params={'filter': '0'}, user_agent=user_agent):  # TODO: check if pause=self.delay is needed
            files.append(url)

        # Since googlesearch.search method retrieves URLs in batches of 100, ensure the file list only contains the requested amount.
        if len(files) > search_max:
            files = files[:-(len(files) - search_max)]

        return files

    def _collect_results(self):
        if self.output_store.empty():
            self.logger.warning("No metadata found in files")
        else:
            for item in self.output_store.items():
                for res in item.get('results', []):
                    self.all_users.extend(res.get('users'))
                    self.all_emails.extend(res.get('emails'))
                    self.all_hosts.extend(res.get('hosts'))

            self.all_users = list(set(self.all_users))
            self.all_emails = list(set(self.all_emails))
            self.all_hosts = list(set(self.all_hosts))

        self._print_results()

    def _print_results(self):
        print("")
        print("--- USERS -----------------------")
        if self.all_users:
            for u in self.all_users:
                print("  * {}".format(u))
        else:
            self.logger.warning("No users found")
        print("")
        print("--- EMAILS ----------------------")
        if self.all_emails:
            for e in self.all_emails:
                print("  * {}".format(e))
        else:
            self.logger.warning("No emails found")
        print("")
        print("--- HOSTS -----------------------")
        if self.all_emails:
            for h in self.all_hosts:
                print("  * {}".format(h))
        else:
            self.logger.warning("No hosts found")
        print("\n")

    def download(self):
        counter = 1
        for url in self.files:
            if counter <= self.download_file_limit:
                self.input_queue.put(url)
                counter += 1

        self.input_queue.join()
