import os
import click
import validators

from colorama import init as colorama_init
from termcolor import colored
from click_shell import shell, add_shell_only_command
from configobj import ConfigObj

from mercurius.core.mercurius import Mercurius
from mercurius.utils import to_int
from mercurius.utils.file_types import FileTypes
from mercurius.utils.logger import Logger, LogTypes
from mercurius.utils.banners import Banners

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

DEFAULT_DELAY = 30.0
DEFAULT_URL_TIMEOUT = 15
DEFAULT_SEARCH_MAX = 100
DEFAULT_DOWNLOAD_FILE_LIMIT = 100
DEFAULT_NUM_OF_THREADS = 8

ALLOWED_CONFIG_SET_COMMANDS = ['working_dir', 'verbose', 'stealth', 'file_types', 'number_threads', 'domain']

project_configs = ConfigObj('configs.ini')

class MercuriusConfig:

    def __init__(self):
        self.set_default_configs()
        self.mercurius = None
        self.configs = project_configs

    def set_default_configs(self):
        self.logger = None

        self.working_dir = os.getcwd()
        self.verbose = False
        self.stealth = False
        self.file_types = []
        self.number_threads = DEFAULT_NUM_OF_THREADS
        self.domain = None

        self.search_max = DEFAULT_SEARCH_MAX
        self.download_limit = DEFAULT_DOWNLOAD_FILE_LIMIT
        self.delay = DEFAULT_DELAY
        self.url_timeout = DEFAULT_URL_TIMEOUT


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
        return []
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


def parse_ctx_config_set(ctx, param, value):
    if not value:
        return None

    vals = value.split("=")
    if len(vals) != 2:
        return None

    cmd = vals[0].strip()
    val = vals[1].strip()

    if cmd in ALLOWED_CONFIG_SET_COMMANDS:
        return {
            'option': cmd,
            'value': val
        }

    return None


def get_shell_prompt():
    return f"{colored('mercurius', 'red', attrs=['bold'])}> "


def get_shell_intro():
    return "Loading Mercurius..."


def get_history_file():
    return project_configs.get('DEFAULT',{}).get('support_directory', '~/.click-history')


@shell(prompt=get_shell_prompt(), intro=get_shell_intro(), hist_file=get_history_file(), context_settings=CONTEXT_SETTINGS)
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
def local(ctx_conf):
    """
    Perform an analysis on local files.
    """

    if ctx_conf.domain and not validators.domain(ctx_conf.domain):
        echo_warning("Not a valid domain! In local mode will be ignored. May affect on extracting host/domain from metadata")

    if not os.path.exists(ctx_conf.working_dir):
        raise click.BadParameter(f"The \"working_dir\" parameter (\"{ctx_conf.working_dir}\") is not a valid folder")
    else:
        echo_info(f"Files will be parsed from \"{ctx_conf.working_dir}\"")

    if not ctx_conf.mercurius:
        ctx_conf.mercurius = Mercurius(ctx_conf.configs, ctx_conf.domain, ctx_conf.file_types, os.path.abspath(ctx_conf.working_dir), number_of_threads=ctx_conf.number_threads,
                                       verbose=ctx_conf.verbose, stealth=ctx_conf.stealth, logger=ctx_conf.logger)
    else:
        ctx_conf.mercurius.domain = ctx_conf.domain
        ctx_conf.mercurius.file_types = ctx_conf.file_types
        ctx_conf.mercurius.working_dir = os.path.abspath(ctx_conf.working_dir)
        ctx_conf.mercurius.number_of_threads = ctx_conf.number_threads
        ctx_conf.mercurius.verbose = ctx_conf.verbose
        ctx_conf.mercurius.stealth = ctx_conf.stealth
        ctx_conf.mercurius.local = True

    ctx_conf.mercurius.go(True)


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
def remote(ctx_conf, delay, url_timeout, search_max, download_limit):
    """
    Perform a remote search on the specified domain, grab files and perform analysis.
    """

    ctx_conf.search_max = search_max
    ctx_conf.download_limit = download_limit

    if not validators.domain(ctx_conf.domain):
        raise click.BadArgumentUsage("Not a valid domain!")

    if delay <= 0:
        echo_warning(f"Delay must be greater than 0. Set to default: {DEFAULT_DELAY}")
        ctx_conf.delay = DEFAULT_DELAY

    if url_timeout <= 0:
        echo_warning(f"URL timeout (-i) must be greater than 0. Set to default: {DEFAULT_URL_TIMEOUT}")
        ctx_conf.url_timeout = DEFAULT_URL_TIMEOUT

    if not os.path.exists(ctx_conf.working_dir):
        echo_warning(f"The folder \"{ctx_conf.working_dir}\" doesn't exists. Will be created.")
        os.mkdir(ctx_conf.working_dir)
    echo_info(f"Downloaded files will be saved here: {ctx_conf.working_dir}")

    if not ctx_conf.mercurius:
        ctx_conf.mercurius = Mercurius(ctx_conf.configs, ctx_conf.domain, ctx_conf.file_types, os.path.abspath(ctx_conf.working_dir),
                                       number_of_threads=ctx_conf.number_threads, verbose=ctx_conf.verbose, stealth=ctx_conf.stealth, logger=ctx_conf.logger)
    else:
        ctx_conf.mercurius.domain = ctx_conf.domain
        ctx_conf.mercurius.file_types = ctx_conf.file_types
        ctx_conf.mercurius.working_dir = os.path.abspath(ctx_conf.working_dir)
        ctx_conf.mercurius.number_of_threads = ctx_conf.number_threads
        ctx_conf.mercurius.verbose = ctx_conf.verbose
        ctx_conf.mercurius.stealth = ctx_conf.stealth
        ctx_conf.mercurius.local = False
        ctx_conf.mercurius.url_timeout = ctx_conf.url_timeout
        ctx_conf.mercurius.search_max = ctx_conf.search_max
        ctx_conf.mercurius.download_file_limit = ctx_conf.download_file_limit

    ctx_conf.mercurius.go(False, delay=ctx_conf.delay, url_timeout=ctx_conf.url_timeout,
                          search_max=ctx_conf.search_max, download_file_limit=ctx_conf.download_limit)


@cli.command()
def banner():
    """
    Prints a random banner of the application
    """
    banner_str = Banners.get_random_banner(version="2.1.3")
    print("\n" + banner_str)


@click.command('config')
@click.option('--view/--set', '-v/-s', is_flag=True, default=True,
              help='Define if is in view or in set mode.')
@click.option('--reset', is_flag=True, default=False,
              help='If set will purge all, removing also all recovered metadata.')
@click.argument('settings', callback=parse_ctx_config_set, expose_value=True, is_eager=True, required=False)
@with_context
def config_cmd(ctx_conf, view, reset, settings):
    """
    Set the common ctx_configurations.
    """

    '''
    You can set:
        working_dir PATH    Changes the working directory folder location.
        verbose             Enables verbose mode.
        stealth             Enables stealth mode. I'll just display found files, no downloads or analysis will be performed.
        file_types  TYPES   A comma-separated list of file types to search/analyze. Allowed values are [pdf, doc, xls, ppt, docx, xlsx, pptx, odt, ods, odp, jpg, jpeg, tiff].
                            Also the following special values are allowed: [ALL, OFFICE, XOFFICE, OPEN_OFFICE, IMAGES]
        number_threads      Number of search threads. (DEFAULT: 8)
        domain  DOMAIN      The domain to search into. It'll be used also for metadata extraction.
    '''

    if reset:
        ctx_conf.set_default_configs()
    else:
        if view:
            for attr in ALLOWED_CONFIG_SET_COMMANDS:
                val = getattr(ctx_conf, attr, None)
                if val is not None:
                    print(f"  {attr} = {val}")
        else:
            if settings:
                val = settings['value']
                if settings['option'] == 'file_types':
                    val = csv_list(ctx_conf, None, val)
                if settings['option'] == 'working_dir':
                    val = os.path.abspath(val)
                elif settings['option'] == 'number_threads':
                    val = to_int(val)
                setattr(ctx_conf, settings['option'], val)

                if ctx_conf.number_threads <= 0:
                    echo_warning(f"Number of threads (-r) must be greater than 0. Set to default: {DEFAULT_NUM_OF_THREADS}")
                    ctx_conf.number_threads = DEFAULT_NUM_OF_THREADS
            else:
                raise click.BadParameter("Missing setting to configure")


@click.command('purge')
@with_context
def purge_cmd(ctx_conf):
    """
    Will reset all the configurations to default.
    """
    ctx_conf.mercurius = None


add_shell_only_command(cli, config_cmd, 'config')
add_shell_only_command(cli, purge_cmd, 'purge')

# FOR DEBUG PURPOSE ONLY
import sys
if __name__ == '__main__':
    cli(sys.argv[1:])
# FOR DEBUG PURPOSE ONLY
