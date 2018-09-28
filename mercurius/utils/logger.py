import logging
from colorama import init as colorama_init
from termcolor import colored, cprint


class LogTypes:
    NO_LOG = 0
    TO_FILE = 1
    TO_SCREEN = 2
    TO_COLORED_SCREEN = 3


class Logger:
    PREFIX_INFO = "[*] Info:"
    PREFIX_SUCCESS = "[+] Success:"
    PREFIX_WARNING = "[!] Warning:"
    PREFIX_ERROR = "[-] Error:"

    def __init__(self, type=LogTypes.NO_LOG):
        colorama_init()

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        self.type = type
        if self.type != LogTypes.TO_FILE \
                and self.type != LogTypes.TO_SCREEN \
                and self.type != LogTypes.TO_COLORED_SCREEN:
            self.type = LogTypes.TO_FILE

    def can_log(self):
        return self.type != LogTypes.NO_LOG

    def info(self, text):
        if self.type == LogTypes.NO_LOG:
            return

        if self.type == LogTypes.TO_SCREEN:
            print(f"{self.PREFIX_INFO} {text}")
        elif self.type == LogTypes.TO_COLORED_SCREEN:
            cprint(colored(self.PREFIX_INFO), 'cyan', attrs=['bold'], end=' ')
            print(text)
        elif self.type == LogTypes.TO_FILE:
            self.logger.info(text)

    def success(self, text):
        if self.type == LogTypes.NO_LOG:
            return

        if self.type == LogTypes.TO_SCREEN:
            print(f"{self.PREFIX_SUCCESS} {text}")
        elif self.type == LogTypes.TO_COLORED_SCREEN:
            cprint(colored(self.PREFIX_SUCCESS), 'green', attrs=['bold'], end=' ')
            print(text)
        elif self.type == LogTypes.TO_FILE:
            self.logger.info(text)

    def warning(self, text):
        if self.type == LogTypes.NO_LOG:
            return

        if self.type == LogTypes.TO_SCREEN:
            print(f"{self.PREFIX_WARNING} {text}")
        elif self.type == LogTypes.TO_COLORED_SCREEN:
            cprint(colored(self.PREFIX_WARNING), 'yellow', attrs=['bold'], end=' ')
            print(text)
        elif self.type == LogTypes.TO_FILE:
            self.logger.warning(text)

    def error(self, text):
        if self.type == LogTypes.NO_LOG:
            return

        if self.type == LogTypes.TO_SCREEN:
            print(f"{self.PREFIX_ERROR} {text}")
        elif self.type == LogTypes.TO_COLORED_SCREEN:
            cprint(colored(self.PREFIX_ERROR), 'red', attrs=['bold'], end=' ')
            print(text)
        elif self.type == LogTypes.TO_FILE:
            self.logger.error(text)
