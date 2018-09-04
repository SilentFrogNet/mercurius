import os
import requests


class Downloader(object):
    def __init__(self, url, dir):
        self.url = url
        self.dir = dir
        self.filename = str(url.split("/")[-1])

    def down(self):
        dest_path = os.path.join(self.dir, self.filename)
        if os.path.exists(dest_path):
            pass
        else:
            r = requests.get(self.url, stream=True)
            if r.status_code == requests.codes.ok:
                with open(dest_path, 'wb') as f:
                    for chunk in r:
                        f.write(chunk)
            else:
                print("\t [x] Error downloading " + self.url)
                self.filename = ""

    def name(self):
        return self.filename
