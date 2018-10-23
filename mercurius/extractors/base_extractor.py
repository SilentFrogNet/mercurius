from mercurius.utils.logger import Logger, LogTypes


class IBaseExtractor:
    extractor_name = "IBaseExtractor"

    def __init__(self, logger=None):
        self.metadata = ""
        self.content = ""
        self.users = []
        self.emails = []
        self.hosts = []
        self.misc = []
        self.errors = []
        if logger:
            self.logger = logger
        else:
            self.logger = Logger(type=LogTypes.TO_SCREEN)

    def get_users(self):
        return self.users

    def get_emails(self):
        return self.emails

    def get_hosts(self):
        return self.hosts

    def get_misc(self):
        return self.misc

    def get_raw_metadata(self):
        return self.metadata

    def get_content(self):
        return self.content

    def get_errors(self):
        return self.errors

    def get_recap(self):
        out = {
            'users': self.users,
            'emails': self.emails,
            'hosts': self.hosts,
            'misc': self.misc,
            'metadata': self.metadata,
            'content': self.content,
            'errors': self.errors
        }
        return out

    @staticmethod
    def unique(lst):
        return list(set(lst))

    def __repr__(self):
        return self.extractor_name
