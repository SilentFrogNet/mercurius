import os
import requests
import threading
import queue
import random

from mercurius.utils.logger import Logger, LogTypes
from mercurius.utils.file_types import FileTypes
from mercurius.utils import pretty_size
from mercurius.core.exceptions import NotSupportedFileFormat
from mercurius.extractors import MSOfficeExtractor, MSOfficeXMLExtractor, OpenOfficeExtractor, PDFExtractor, ImageExtractor
from mercurius.loaders.extractor_loader import ExtractorLoader


class MetaWorker(threading.Thread):

    def __init__(self, tid, input_queue, output_store, stop_event, merc, is_local, logger=None, timeout=1):
        super(MetaWorker, self).__init__()
        self.daemon = True

        self.id = tid
        self.name = "worker" + str(self.id)
        self.input_queue = input_queue
        self.output_store = output_store
        self.stop_event = stop_event
        self.merc = merc
        self.timeout = timeout
        self.is_local = is_local
        if logger:
            self.logger = logger
        else:
            self.logger = Logger(type=LogTypes.TO_SCREEN)
        self.extractor_loader = ExtractorLoader(self.merc.configs)
        self.extractor_loader.register_plugins()
        self.plugin_manager = self.extractor_loader.get_plugin_manager()

    def run(self):
        while not self.stop_event.is_set():
            try:
                item = self.input_queue.get(True, self.timeout)
                if item:
                    self.do_work(item)
            except queue.Empty:
                # raised by queue.get if we reach the timeout on an empty queue
                continue
            self.input_queue.task_done()

    def do_work(self, url):
        if self.is_local:
            dest_path = url
        else:
            dest_path = self._download_file(url)
        self._parse_file(dest_path)

    def _download_file(self, url):
        # TODO: move to downloader
        # Strip any trailing /'s before extracting file name.
        filename = str(url.strip('/').split('/')[-1])
        dest_path = os.path.join(self.merc.out_directory, filename)

        try:
            headers = {
                'User-Agent': random.choice(self.merc.random_user_agents)
            }
            response = requests.get(url, headers=headers, verify=False, timeout=self.merc.url_timeout, stream=True)

            # Download the file.
            if response.status_code == requests.codes.ok:
                try:
                    size = int(response.headers["Content-Length"])
                except KeyError:
                    size = len(response.content)

                self.logger.info(f"Downloading file - [{pretty_size(size)}] {url}")

                with open(dest_path, "wb") as fh:
                    for chunk in response:
                        if chunk:
                            fh.write(chunk)

                self.logger.success("File {} downloaded.".format(url))
            else:
                self.logger.error("URL {0} returned HTTP code {1}".format(url, response.status_code))
        except requests.exceptions.RequestException as e:
            self.logger.error("Exception for url: {0} -- {1}".format(url, e))

        return dest_path

    def _parse_file(self, path):
        working_dir = os.path.dirname(os.path.realpath(path))
        filename, filetype = os.path.splitext(os.path.basename(path))
        filetype = filetype[1:].lower()

        out = {
            'working_dir': working_dir,
            'filename': filename,
            'filetype': filetype,
            'results': []
        }

        self.logger.info("Parsing file \"{}.{}\"...".format(filename, filetype))

        try:
            meta_out, errors = self._parse_metadata(path, filetype)

            if meta_out:
                for parser_out in meta_out:
                    out['results'].append(parser_out.get_recap())

                if errors:
                    self.logger.warning("File \"{}.{}\" parsed with some warnings: {}".format(filename, filetype, ", ".join(errors)))
                else:
                    self.logger.success("File \"{}.{}\" parsed correctly".format(filename, filetype))
                self.output_store.push(out)
            else:
                self.logger.error("Error in the parsing of \"{}.{}\":{}".format(filename, filetype, ", ".join(errors)))
        except NotSupportedFileFormat as e:
            self.logger.error("Unsupported file format for file \"{}.{}\"".format(filename, filetype))

    def _parse_metadata(self, path, filetype):
        res = self.plugin_manager.hook.parse_data(path=path, filetype=filetype, configs=self.merc.configs)

        if len(res) == 0:
            raise NotSupportedFileFormat("Unsupported file format {}".format(filetype.upper()))

        errors = []
        for r in res:
            if r:
                errors.extend(r.get_errors())

        return res, errors

