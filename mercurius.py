#!/usr/bin/env python3

import os
import sys
import argparse
import threading

from mercurius.core.mercurius import Mercurius
from mercurius.utils.banners import Banners
from mercurius.utils.logger import Logger, LogTypes
from mercurius.utils.file_types import FileTypes

stop_workers = threading.Event()
logger = Logger(type=LogTypes.TO_COLORED_SCREEN)


def csv_list(string):
    return string.split(',')


def banner():
    banner_str = Banners.get_random_banner()

    print("\n" + banner_str)


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
    parser.add_argument('-o', dest='out_directory', action='store', help='Directory to save downloaded files.  DEFAULT is cwd, "."')
    parser.add_argument('-r', dest='number_of_threads', action='store', type=int, default=DEFAULT_NUM_OF_THREADS, help=f"Number of search threads.  DEFAULT: {DEFAULT_NUM_OF_THREADS}")
    parser.add_argument('-q', dest='quiet', action='store_true', default=False, help='In quiet mode, it doesn\'t download the files, it\'ll just viewing search results.')
    parser.add_argument('-l', dest='local', action='store_true', default=False, help='Performs the metadata search on local files only.')

    parser.add_argument('-e', dest='delay', action='store', type=float, default=DEFAULT_DELAY, help=f"Delay (in seconds) between searches.  If it\'s too small Google may block your IP, too big and your search may take a while.  DEFAULT: {DEFAULT_DELAY}")
    parser.add_argument('-i', dest='url_timeout', action='store', type=int, default=DEFAULT_URL_TIMEOUT, help=f"Number of seconds to wait before timeout for unreachable/stale pages.  DEFAULT: {DEFAULT_URL_TIMEOUT}")
    parser.add_argument('-s', dest='search_max', action='store', type=int, default=DEFAULT_SEARCH_MAX, help=f"Maximum results to search.  DEFAULT: {DEFAULT_SEARCH_MAX}")
    parser.add_argument('-n', dest='download_file_limit', default=DEFAULT_DOWNLOAD_FILE_LIMIT, action='store', type=int, help=f"Maximum number of files to download per filetype.  DEFAULT: {DEFAULT_DOWNLOAD_FILE_LIMIT}")

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
    mg2.go(is_local=args.local)
