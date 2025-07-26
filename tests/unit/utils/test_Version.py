import osbot_serverless_s3_browser
from unittest                                 import TestCase
from osbot_utils.utils.Files                  import parent_folder, file_name
from osbot_serverless_s3_browser.utils.Version  import Version, version__osbot_serverless_s3_browser


class test_Version(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.version = Version()

    def test_path_code_root(self):
        assert self.version.path_code_root() == osbot_serverless_s3_browser.path

    def test_path_version_file(self):
        with self.version as _:
            assert parent_folder(_.path_version_file()) == osbot_serverless_s3_browser.path
            assert file_name    (_.path_version_file()) == 'version'

    def test_value(self):
        assert self.version.value() == version__osbot_serverless_s3_browser