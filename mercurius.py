#!/usr/bin/env python3

import os
import sys
import argparse
import threading
import random
import googlesearch
import queue

from spinner import Spinner
from metagoofil2.utils.logger import Logger, LogTypes
from metagoofil2.core.meta_worker import MetaWorker
from metagoofil2.utils.item_store import ItemStore
from metagoofil2.utils.file_types import FileTypes

stop_workers = threading.Event()
logger = Logger(type=LogTypes.TO_COLORED_SCREEN)


class Mercurius:

    def __init__(self, domain, file_types, out_directory, delay=30, url_timeout=15, search_max=100, download_file_limit=100, number_of_threads=8, quiet=False, local=False):
        self.domain = domain
        self.file_types = file_types
        self.out_directory = out_directory
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
        self.input_queue = queue.Queue()
        self.output_store = ItemStore()

    def go(self):
        for i in range(self.number_of_threads):
            w = MetaWorker(i, self.input_queue, self.output_store, stop_workers, self, logger=logger)
            w.start()
            self.workers.append(w)

        if self.local:
            self.local_go()
        else:
            self.remote_go()

        if self.output_store.empty():
            logger.warning("No metadata found in files")
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
                logger.warning("No users found")
            print("\n")
            print("--- EMAILS ----------------------")
            if all_emails:
                for e in all_emails:
                    print(f"  * {e}")
            else:
                logger.warning("No emails found")
            print("\n")
            print("--- HOSTS -----------------------")
            if all_emails:
                for h in all_hosts:
                    print(f"  * {h}")
            else:
                logger.warning("No hosts found")
            print("\n")

    def local_go(self):
        logger.info("Starting local search...")

        if self.out_directory is None:
            logger.error("No directory specified. Abort!")
            return

        print_string = "Analyzing local files..."
        stop_spinner = None
        spin_thread = None
        if not logger.can_log():
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

        if not logger.can_log() and stop_spinner is not None and spin_thread is not None:
            stop_spinner.set()
            spin_thread.join()

        logger.success(print_string + "DONE")

    def remote_go(self):
        logger.info("Starting remote search...")

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
            logger.success(print_string + "DONE")

            # Since googlesearch.search method retreives URLs in batches of 100, ensure the file list only contains the requested amount.
            if len(self.files) > self.search_max:
                self.files = self.files[:-(len(self.files) - self.search_max)]

            if self.quiet:
                # Otherwise, just display them.
                logger.info("Results: {0} {1} files found".format(len(self.files), filetype))
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
                logger.success(print_string + "DONE")

    def download(self):
        counter = 1
        for url in self.files:
            if counter <= self.download_file_limit:
                self.input_queue.put(url)
                counter += 1

        self.input_queue.join()


def csv_list(string):
    return string.split(',')


def banner():
    banner_str = "\n" \
                 "*********************************************************\n" \
                 "*      _    _                          _                *\n" \
                 "*     |  \/  |                        (_)               *\n" \
                 "*     | .  . | ___ _ __ ___ _   _ _ __ _ _   _ ___      *\n" \
                 "*     | |\/| |/ _ \ '__/ __| | | | '__| | | | / __|     *\n" \
                 "*     | |  | |  __/ | | (__| |_| | |  | | |_| \__ \     *\n" \
                 "*     \_|  |_/\___|_|  \___|\__,_|_|  |_|\__,_|___/     *\n" \
                 "*                                                       *\n" \
                 "* Mercurius  v1.0.0                                     *\n" \
                 "* Ilario Dal Grande                                     *\n" \
                 "* http://silentfrog.net                                 *\n" \
                 "* ilario.dalgrande@silentfrog.net                       *\n" \
                 "*********************************************************\n"

    print(banner_str)


DEFAULT_DELAY = 30.0
DEFAULT_URL_TIMEOUT = 15
DEFAULT_SEARCH_MAX = 100
DEFAULT_DOWNLOAD_FILE_LIMIT = 100
DEFAULT_NUM_OF_THREADS = 8

if __name__ == '__main__':
    banner()

    parser = argparse.ArgumentParser(description='Mercurius - Search and download files from a target domain and extract metadata')
    parser.add_argument('-d', dest='domain', action='store', help='Domain to search.')
    parser.add_argument('-t', dest='file_types', action='store', type=csv_list, help=f"File types to download ({FileTypes.to_string()}).")
    parser.add_argument('-e', dest='delay', action='store', type=float, default=DEFAULT_DELAY, help=f"Delay (in seconds) between searches.  If it\'s too small Google may block your IP, too big and your search may take a while.  DEFAULT: {DEFAULT_DELAY}")
    parser.add_argument('-i', dest='url_timeout', action='store', type=int, default=DEFAULT_URL_TIMEOUT, help=f"Number of seconds to wait before timeout for unreachable/stale pages.  DEFAULT: {DEFAULT_URL_TIMEOUT}")
    parser.add_argument('-s', dest='search_max', action='store', type=int, default=DEFAULT_SEARCH_MAX, help=f"Maximum results to search.  DEFAULT: {DEFAULT_SEARCH_MAX}")
    parser.add_argument('-n', dest='download_file_limit', default=DEFAULT_DOWNLOAD_FILE_LIMIT, action='store', type=int, help=f"Maximum number of files to download per filetype.  DEFAULT: {DEFAULT_DOWNLOAD_FILE_LIMIT}")
    parser.add_argument('-o', dest='out_directory', action='store', help='Directory to save downloaded files.  DEFAULT is cwd, "."')
    parser.add_argument('-r', dest='number_of_threads', action='store', type=int, default=DEFAULT_NUM_OF_THREADS, help=f"Number of search threads.  DEFAULT: {DEFAULT_NUM_OF_THREADS}")
    parser.add_argument('-q', dest='quiet', action='store_true', default=False, help='In quiet mode, it doesn\'t download the files, it\'ll just viewing search results.')
    parser.add_argument('-l', dest='local', action='store_true', default=False, help='Performs the metadata search on local files only.')

    args = parser.parse_args()
    has_parsing_errors = False

    if not args.domain and not args.local:
        logger.error("Missing mandatory parameter \"domain\" (-d)")
        has_parsing_errors = True
    if not args.file_types and not args.local:
        logger.error("Missing mandatory parameter \"file_types\" (-t)")
        has_parsing_errors = True
    if args.out_directory:
        if not args.local:
            logger.info(f"Downloaded files will be saved here: {args.out_directory}")
            if not os.path.exists(args.out_directory):
                logger.success(f"Creating folder: {args.out_directory}")
                os.mkdir(args.out_directory)
        else:
            if not os.path.exists(args.out_directory):
                logger.error(f"The \"out_directory\" parameter (\"{args.out_directory}\") is not a valid folder")
                has_parsing_errors = True
            else:
                logger.info(f"Files will be parsed from here: {args.out_directory}")
    else:
        logger.error("Missing mandatory parameter \"out_directory\" (-o)")
        has_parsing_errors = True

    if args.delay < 0:
        logger.warning(f"Delay must be greater than 0. Set to default: {DEFAULT_DELAY}")
        args.delay = DEFAULT_DELAY
    if args.url_timeout < 0:
        logger.warning(f"URL timeout (-i) must be greater than 0. Set to default: {DEFAULT_URL_TIMEOUT}")
        args.url_timeout = DEFAULT_URL_TIMEOUT
    if args.number_of_threads < 0:
        logger.warning(f"Number of threads (-n) must be greater than 0. Set to default: {DEFAULT_NUM_OF_THREADS}")
        args.number_of_threads = DEFAULT_NUM_OF_THREADS

    if has_parsing_errors:
        sys.exit()

    mg2 = Mercurius(**vars(args))
    mg2.go()
