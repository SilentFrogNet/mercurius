import os
import sys
import click
import validators

from colorama import init as colorama_init
from termcolor import colored, cprint
from click_shell import shell, make_click_shell

from mercurius.core.mercurius import Mercurius
from mercurius.utils.file_types import FileTypes
from mercurius.utils.logger import Logger, LogTypes

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

DEFAULT_DELAY = 30.0
DEFAULT_URL_TIMEOUT = 15
DEFAULT_SEARCH_MAX = 100
DEFAULT_DOWNLOAD_FILE_LIMIT = 100
DEFAULT_NUM_OF_THREADS = 8


class MercuriusConfig:
    logger = None

    working_dir = os.getcwd()
    verbose = False
    stealth = False
    file_types = []
    number_threads = DEFAULT_NUM_OF_THREADS
    domain = None

    search_max = DEFAULT_SEARCH_MAX
    download_limit = DEFAULT_DOWNLOAD_FILE_LIMIT
    delay = DEFAULT_DELAY
    url_timeout = DEFAULT_URL_TIMEOUT


with_context = click.make_pass_decorator(MercuriusConfig, ensure=True)

mypackage_root_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(mypackage_root_dir, 'VERSION')) as version_file:
    cli_version = version_file.read().strip()

colorama_init()

def echo_info(text, file=None):
    click.secho("[*] Info: ", fg='cyan', bold=True, nl="", file=file)
    click.echo(text, file=file)


def echo_warning(text, file=None):
    click.secho("[!] Warning: ", fg='yellow', bold=True, nl="", file=file)
    click.secho(text, fg='yellow', file=file)


def echo_error(text, file=None):
    click.secho("[-] Error: ", fg='red', bold=True, nl="", file=file)
    click.secho(text, fg='red', file=file)


def modify_usage_error():
    '''
        a method to append the help menu to an usage error

    :return: None
    '''

    from click._compat import get_text_stderr
    from click.utils import echo

    def show(self, file=None):
        import sys
        if file is None:
            file = get_text_stderr()
        if self.ctx is not None:
            color = self.ctx.color
            echo(self.ctx.get_usage() + '\n', file=file, color=color)
        echo_error(self.format_message(), file=file)
        sys.argv = [sys.argv[0]]

    click.exceptions.UsageError.show = show


modify_usage_error()


def csv_list(ctx, param, value):
    if value is None:
        return FileTypes.ALL
    types = value.split(',')

    out_types = []
    for t in types:
        if t in FileTypes.special_groups():
            out_types.extend(FileTypes.SPECIAL_GROUPS.get(t, []))
        else:
            if t in FileTypes.ALL:
                out_types.append(t)
            else:
                echo_warning(f"The file type \"{t}\" is unknown. Ignored.")

    return list(set(out_types))


def get_shell_prompt():
    return f"{colored('mercurius', 'red', attrs=['bold'])}> "


@shell(prompt=get_shell_prompt(), context_settings=CONTEXT_SETTINGS)
@click.option('--working-dir', '-w', default='.', metavar='PATH',
              help="Changes the working directory folder location.")
@click.option('--verbose', '-v', is_flag=True,
              help="Enables verbose mode.")
@click.option('--stealth', '-s', is_flag=True,
              help="Enables stealth mode. I'll just display found files, no downloads or analysis will be performed.")
@click.option('--file-types', '-t', metavar='TYPES', callback=csv_list, expose_value=True, is_eager=True,
              help=f"A comma-separated list of file types to search/analyze. Allowed values are [{FileTypes.to_string()}].\n"
                   f"Also the following special values are allowed: [{FileTypes.special_groups()}]")
@click.option('--number-threads', '-r', default=DEFAULT_NUM_OF_THREADS,
              help=f"Number of search threads. (DEFAULT: {DEFAULT_NUM_OF_THREADS})")
@click.option('--domain', '-d', type=click.STRING, metavar='DOMAIN',
              help="The domain to search into. It'll be used also for metadata extraction.")
@click.version_option(version=cli_version)
@click.pass_context
def cli(ctx, working_dir, verbose, stealth, file_types, number_threads, domain):
    """
    Mercurius is a command line tool to extract and collect metadata from local or remote files.
    """

    ctx.obj = MercuriusConfig()
    ctx.obj.working_dir = working_dir
    ctx.obj.verbose = verbose
    ctx.obj.stealth = stealth
    ctx.obj.file_types = file_types
    ctx.obj.number_threads = number_threads
    ctx.obj.domain = domain

    ctx.obj.logger = Logger(LogTypes.TO_COLORED_SCREEN)

    if ctx.obj.number_threads <= 0:
        echo_warning(f"Number of threads (-r) must be greater than 0. Set to default: {DEFAULT_NUM_OF_THREADS}")
        ctx.obj.number_threads = DEFAULT_NUM_OF_THREADS


@cli.command()
@with_context
def local(conf):
    if conf.domain and not validators.domain(conf.domain):
        echo_warning("Not a valid domain! In local mode will be ignored. May affect on extracting host/domain from metadata")

    if not os.path.exists(conf.working_dir):
        raise click.BadParameter(f"The \"working_dir\" parameter (\"{conf.working_dir}\") is not a valid folder")
    else:
        echo_info(f"Files will be parsed from \"{conf.working_dir}\"")

    merc = Mercurius(conf.domain, conf.file_types, os.path.abspath(conf.working_dir),
                     number_of_threads=conf.number_threads, verbose=conf.verbose, stealth=conf.stealth,
                     local=True, logger=conf.logger)

    merc.go()


@cli.command()
@click.option('--delay', '-d', default=DEFAULT_DELAY,
              help=f"Delay (in seconds) between searches. If it\'s too small Google may block your IP, "
                   f"too big and your search may take a while. (DEFAULT: {DEFAULT_DELAY})")
@click.option('--url-timeout', '-i', default=DEFAULT_URL_TIMEOUT,
              help=f"Number of seconds to wait before timeout for unreachable/stale pages. DEFAULT: ({DEFAULT_URL_TIMEOUT})")
@click.option('--search-max', '-s', default=DEFAULT_SEARCH_MAX,
              help=f"Maximum results to search. (DEFAULT: {DEFAULT_SEARCH_MAX})")
@click.option('--download-limit', '-n', default=DEFAULT_DOWNLOAD_FILE_LIMIT,
              help=f"Maximum number of files to download per filetype. (DEFAULT: {DEFAULT_DOWNLOAD_FILE_LIMIT})")
@with_context
def remote(conf, delay, url_timeout, search_max, download_limit):
    click.echo("remote")

    conf.search_max = search_max
    conf.download_limit = download_limit

    if not validators.domain(conf.domain):
        raise click.BadArgumentUsage("Not a valid domain!")

    if delay <= 0:
        echo_warning(f"Delay must be greater than 0. Set to default: {DEFAULT_DELAY}")
        conf.delay = DEFAULT_DELAY

    if url_timeout <= 0:
        echo_warning(f"URL timeout (-i) must be greater than 0. Set to default: {DEFAULT_URL_TIMEOUT}")
        conf.url_timeout = DEFAULT_URL_TIMEOUT

    if not os.path.exists(conf.working_dir):
        echo_warning(f"The folder \"{conf.working_dir}\" doesn't exists. Will be created.")
        os.mkdir(conf.working_dir)
    echo_info(f"Downloaded files will be saved here: {conf.working_dir}")

    merc = Mercurius(conf.domain, conf.file_types, os.path.abspath(conf.working_dir),
                     number_of_threads=conf.number_threads, verbose=conf.verbose, stealth=conf.stealth,
                     delay=conf.delay, url_timeout=conf.url_timeout, search_max=conf.search_max,
                     download_file_limit=conf.download_limit, local=False, logger=conf.logger)

    merc.go()


# FOR DEBUG PURPOSE ONLY
import sys
if __name__ == '__main__':
    cli(sys.argv[1:])
# FOR DEBUG PURPOSE ONLY
