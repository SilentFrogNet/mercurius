import os
import unittest

from pprint import pprint

from mercurius.extractors import ImageExtractor

PROJECT_ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_FILES_PATH = os.path.join(PROJECT_ROOT_PATH, 'data')


class RootTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(RootTest, cls).setUpClass()
        cls.im = ImageExtractor()

        cls.wrong_file = {
            'path': os.path.join(PROJECT_FILES_PATH, "test.doc"),
            'filetype': 'doc'
        }
        cls.correct_file_jpg = {
            'path': os.path.join(PROJECT_FILES_PATH, "flowers.jpg"),
            'filetype': 'jpg'
        }
        cls.correct_file_jpeg = {
            'path': os.path.join(PROJECT_FILES_PATH, "flowers.jpeg"),
            'filetype': 'jpeg'
        }
        cls.correct_file_tif = {
            'path': os.path.join(PROJECT_FILES_PATH, "flowers.tif"),
            'filetype': 'tif'
        }
        cls.correct_file_tiff = {
            'path': os.path.join(PROJECT_FILES_PATH, "flowers.tiff"),
            'filetype': 'tiff'
        }
        cls.no_metadata_file = {
            'path': os.path.join(PROJECT_FILES_PATH, "no_metadata.jpg"),
            'filetype': 'jpg'
        }

    @classmethod
    def tearDownClass(cls):
        super(RootTest, cls).tearDownClass()


class TestImageExtractor(RootTest):

    def test_01_parse_wrong_file(self):
        result = self.im.parse_data(**self.wrong_file)
        self.assertIsNone(result)

    def test_02_parse_correct_file_jpg(self):
        result = self.im.parse_data(**self.correct_file_jpg)
        self.assertIsInstance(result, ImageExtractor)

    def test_03_parse_correct_file_jpeg(self):
        result = self.im.parse_data(**self.correct_file_jpeg)
        self.assertIsInstance(result, ImageExtractor)

    def test_04_parse_correct_file_tif(self):
        result = self.im.parse_data(**self.correct_file_tif)
        self.assertIsInstance(result, ImageExtractor)

    def test_05_parse_correct_file_tiff(self):
        result = self.im.parse_data(**self.correct_file_tiff)
        self.assertIsInstance(result, ImageExtractor)

    def test_06_parse_no_metadata_file(self):
        result = self.im.parse_data(**self.no_metadata_file)
        self.assertIsInstance(result, ImageExtractor)
        self.assertListEqual(result.get_emails(), [])
        self.assertListEqual(result.get_hosts(), [])
        self.assertListEqual(result.get_users(), [])

if __name__ == '__main__':
    unittest.main()
