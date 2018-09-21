import threading


class ItemStore(object):
    def __init__(self):
        self.lock = threading.Lock()
        self._items = []

    def push(self, item):
        with self.lock:
            self._items.append(item)

    def empty(self):
        return len(self._items) == 0

    def items(self):
        return self._items
