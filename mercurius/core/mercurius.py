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

    def __init__(self, domain, file_types, out_directory, delay=30, url_timeout=15, search_max=100, download_file_limit=100, number_of_threads=8, quiet=False, local=False, logger=None):
        self.domain = domain
        self.file_types = file_types
        self.out_directory = out_directory
        self.delay = delay
        self.url_timeout = url_timeout
        self.search_max = search_max
        self.download_file_limit = download_file_limit
        self.quiet = quiet
        self.local = local
        if logger:
            self.logger = logger
        else:
            self.logger = Logger(type=LogTypes.TO_SCREEN)
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
        self.input_queue = queue.Queue()
        self.output_store = ItemStore()

    def go(self):
        for i in range(self.number_of_threads):
            w = MetaWorker(i, self.input_queue, self.output_store, stop_workers, self, logger=self.logger)
            w.start()
            self.workers.append(w)

        if self.local:
            self.local_go()
        else:
            self.remote_go()

        if self.output_store.empty():
            self.logger.warning("No metadata found in files")
        else:
            all_users = []
            all_emails = []
            all_hosts = []
            for item in self.output_store.items():
                all_users.extend(item.get('users'))
                all_emails.extend(item.get('emails'))
                all_hosts.extend(item.get('hosts'))

            all_users = list(set(all_users))
            all_emails = list(set(all_emails))
            all_hosts = list(set(all_hosts))

            print("\n\n")
            print("--- USERS -----------------------")
            if all_users:
                for u in all_users:
                    print(f"  * {u}")
            else:
                self.logger.warning("No users found")
            print("\n")
            print("--- EMAILS ----------------------")
            if all_emails:
                for e in all_emails:
                    print(f"  * {e}")
            else:
                self.logger.warning("No emails found")
            print("\n")
            print("--- HOSTS -----------------------")
            if all_emails:
                for h in all_hosts:
                    print(f"  * {h}")
            else:
                self.logger.warning("No hosts found")
            print("\n")

    def local_go(self):
        self.logger.info("Starting local search...")

        if self.out_directory is None:
            self.logger.error("No directory specified. Abort!")
            return

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

        self.input_queue.join()
        stop_workers.set()
        for w in self.workers:
            w.join()

        if not self.logger.can_log() and stop_spinner is not None and spin_thread is not None:
            stop_spinner.set()
            spin_thread.join()

        self.logger.success(print_string + "DONE")

    def remote_go(self):
        self.logger.info("Starting remote search...")

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
            self.logger.success(print_string + "DONE")

            # Since googlesearch.search method retreives URLs in batches of 100, ensure the file list only contains the requested amount.
            if len(self.files) > self.search_max:
                self.files = self.files[:-(len(self.files) - self.search_max)]

            if self.quiet:
                # Otherwise, just display them.
                self.logger.info("Results: {0} {1} files found".format(len(self.files), filetype))
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
                [self.input_queue.put(url) for url in self.files]

                self.input_queue.join()
                stop_workers.set()
                for w in self.workers:
                    w.join()

                stop_spinner.set()
                spin_thread.join()
                self.logger.success(print_string + "DONE")

    def download(self):
        counter = 1
        for url in self.files:
            if counter <= self.download_file_limit:
                self.input_queue.put(url)
                counter += 1

        self.input_queue.join()
