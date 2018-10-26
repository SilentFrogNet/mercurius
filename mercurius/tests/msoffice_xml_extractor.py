import os

from unittest.case import TestCase
from pprint import pprint

from mercurius.extractors import MSOfficeXMLExtractor
from mercurius.tests.utils import compare_unordered_lists

PROJECT_ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_FILES_PATH = os.path.join(PROJECT_ROOT_PATH, 'data')


class RootTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super(RootTest, cls).setUpClass()
        cls.im = MSOfficeXMLExtractor()

        cls.wrong_file = {
            'path': os.path.join(PROJECT_FILES_PATH, "letter.pdf"),
            'filetype': 'pdf'
        }
        # cls.with_user_file = {
        #     'path': os.path.join(PROJECT_FILES_PATH, "with_user.pdf"),
        #     'filetype': 'pdf'
        # }
        # cls.with_user_file_data = {
        #     'users': ['empi0771']
        # }
        # cls.with_all = {
        #     'path': os.path.join(PROJECT_FILES_PATH, "letter.pdf"),
        #     'filetype': 'pdf'
        # }
        # cls.with_all_data = {
        #     'emails': ['info@mysuperhost.com', 'renew@mysuperhost.com'],
        #     'hosts': ['www.example.com', 'mysuperhost.com']
        # }

    @classmethod
    def tearDownClass(cls):
        super(RootTest, cls).tearDownClass()


class TestMSOfficeXMLExtractor(RootTest):

    def test_01_parse_wrong_file(self):
        result = self.im.parse_data(**self.wrong_file)
        self.assertIsNone(result)

    # def test_02_parse_with_user_file(self):
    #     result = self.im.parse_data(**self.with_user_file)
    #     self.assertIsInstance(result, MSOfficeXMLExtractor)
    #     self.assertListEqual(result.get_users(), self.with_user_file_data['users'])
    #
    # def test_03_parse_with_all_file(self):
    #     result = self.im.parse_data(**self.with_all)
    #     self.assertIsInstance(result, MSOfficeXMLExtractor)
    #     compare_unordered_lists(self, result.get_hosts(), self.with_all_data['hosts'])
    #     compare_unordered_lists(self, result.get_emails(), self.with_all_data['emails'])
