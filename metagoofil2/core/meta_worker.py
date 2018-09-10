import os
import requests
import threading
import queue
import random

from metagoofil2.utils.logger import Logger, LogTypes
from metagoofil2.utils.file_types import FileTypes
from metagoofil2.extractors import MSOfficeExtractor, MSOfficeXMLExtractor, OpenOfficeExtractor, PDFExtractor


class MetaWorker(threading.Thread):

    def __init__(self, tid, input_queue, output_store, stop_event, mg, logger=None, timeout=1):
        super(MetaWorker, self).__init__()
        self.daemon = True

        self.id = tid
        self.name = "worker" + str(self.id)
        self.input_queue = input_queue
        self.output_store = output_store
        self.stop_event = stop_event
        self.mg = mg
        self.timeout = timeout
        self.is_local = self.mg.local
        if logger:
            self.logger = logger
        else:
            self.logger = Logger(type=LogTypes.TO_SCREEN)

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
        # Strip any trailing /'s before extracting file name.
        filename = str(url.strip('/').split('/')[-1])
        dest_path = os.path.join(self.mg.save_directory, filename)

        try:
            headers = {
                'User-Agent': random.choice(self.mg.random_user_agents)
            }
            response = requests.get(url, headers=headers, verify=False, timeout=self.mg.url_timeout, stream=True)

            # Download the file.
            if response.status_code == requests.codes.ok:
                try:
                    size = int(response.headers["Content-Length"])
                except KeyError:
                    size = len(response.content)

                self.logger.info("Downloading file - [{0} bytes] {1}".format(size, url))

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
        filetype = filetype[1:]

        out = {
            'working_dir': working_dir,
            'filename': filename,
            'filetype': filetype
        }

        self.logger.info("Parsing file \"{}{}\"...".format(filename, filetype))

        metaparser = None
        if filetype == FileTypes.PDF:
            metaparser = PDFExtractor(path)
        if filetype in FileTypes.MS_OFFICE:
            metaparser = MSOfficeExtractor(path)
        # if filetype in FileTypes.MS_OFFICE_XML:
        #     metaparser = MSOfficeXMLExtractor(path)
        # if filetype in FileTypes.OPEN_OFFICE:
        #     metaparser = OpenOfficeExtractor(path)

        if metaparser:
            if metaparser.parse_data():
                out.update(metaparser.get_recap())

                self.logger.success("File \"{}{}\" parsed correctly".format(filename, filetype))
                self.output_store.push(out)
            else:
                self.logger.error("Error in the parsing {}{}:{}".format(filename, filetype, " ".join(metaparser.get_errors())))
        else:
            self.logger.error("Unsupported file format for file {}{}".format(filename, filetype))
