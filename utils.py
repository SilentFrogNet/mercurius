import threading
import time


class Spinner(threading.Thread):

    def __init__(self, stop_event, prefix=None, spinner_string=None):
        super(Spinner, self).__init__()
        self.daemon = True
        self.stop_event = stop_event
        self.prefix = prefix if prefix else ""
        self.spinner_string = spinner_string if spinner_string else '|/-\\'

    def run(self):
        while True:
            for cursor in self.spinner_string:
                print(f"\r{self.prefix}{cursor}", end='\r')
                time.sleep(0.1)  # adjust this to change the speed
                if self.stop_event.is_set():
                    clean_str = " " * 50
                    print(f"\r{clean_str}", end='\r')
                    return
