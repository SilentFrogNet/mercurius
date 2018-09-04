import logging
from colorama import init as colorama_init
from termcolor import colored, cprint


class LogTypes:
    TO_FILE = 0
    TO_SCREEN = 1
    TO_COLORED_SCREEN = 2


class Logger:
    PREFIX_INFO = "[*]"
    PREFIX_SUCCESS = "[+]"
    PREFIX_WARNING = "[!]"
    PREFIX_ERROR = "[-]"

    def __init__(self, type=LogTypes.TO_FILE):
        colorama_init()

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        self.type = type
        if self.type != LogTypes.TO_FILE \
                and self.type != LogTypes.TO_SCREEN \
                and self.type != LogTypes.TO_COLORED_SCREEN:
            self.type = LogTypes.TO_FILE

    def info(self, text):
        if self.type == LogTypes.TO_SCREEN:
            print(f"{self.PREFIX_INFO} {text}")
        elif self.type == LogTypes.TO_COLORED_SCREEN:
            cprint(colored(self.PREFIX_INFO), 'cyan', attrs=['bold'], end=' ')
            print(text)
        elif self.type == LogTypes.TO_FILE:
            self.logger.info(text)

    def success(self, text):
        if self.type == LogTypes.TO_SCREEN:
            print(f"{self.PREFIX_SUCCESS} {text}")
        elif self.type == LogTypes.TO_COLORED_SCREEN:
            cprint(colored(self.PREFIX_SUCCESS), 'green', attrs=['bold'], end=' ')
            print(text)
        elif self.type == LogTypes.TO_FILE:
            self.logger.info(text)

    def warning(self, text):
        if self.type == LogTypes.TO_SCREEN:
            print(f"{self.PREFIX_WARNING} {text}")
        elif self.type == LogTypes.TO_COLORED_SCREEN:
            cprint(colored(self.PREFIX_WARNING), 'yellow', attrs=['bold'], end=' ')
            print(text)
        elif self.type == LogTypes.TO_FILE:
            self.logger.warning(text)

    def error(self, text):
        if self.type == LogTypes.TO_SCREEN:
            print(f"{self.PREFIX_ERROR} {text}")
        elif self.type == LogTypes.TO_COLORED_SCREEN:
            cprint(colored(self.PREFIX_ERROR), 'red', attrs=['bold'], end=' ')
            print(text)
        elif self.type == LogTypes.TO_FILE:
            self.logger.error(text)
