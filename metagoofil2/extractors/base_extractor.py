import abc


class IBaseExtractor:
    __metaclass__ = abc.ABCMeta

    metadata = ""
    content = ""
    users = []
    emails = []
    hosts = []
    misc = []
    errors = []

    @abc.abstractmethod
    def parse_data(self):
        raise NotImplementedError('Not yet implemented')

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
