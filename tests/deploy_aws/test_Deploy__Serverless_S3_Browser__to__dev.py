import pytest
from unittest                                                               import TestCase

from osbot_serverless_s3_browser.utils.Version import version__osbot_serverless_s3_browser
from osbot_utils.utils.Misc import list_set

from osbot_fast_api_serverless.utils.Version                                import version__osbot_fast_api_serverless
from osbot_fast_api_serverless.deploy.Deploy__Serverless__Fast_API          import DEFAULT__ERROR_MESSAGE__WHEN_FAST_API_IS_OK
from osbot_serverless_s3_browser.utils.deploy.Deploy__Serverless_S3_Browser import Deploy__Serverless_S3_Browser, \
    LAMBDA_DEPENDENCIES__SERVERLESS_S3_BROWSER


class test_Deploy__Serverless_S3_Browser__to__dev__qa__prod(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.deploy_fast_api__dev  = Deploy__Serverless_S3_Browser(stage = 'dev')

        with cls.deploy_fast_api__dev as _:
            if _.aws_config.aws_configured() is False:
                pytest.skip("this test needs valid AWS credentials")

    def test_1__check_stages(self):
        assert self.deploy_fast_api__dev .stage == 'dev'

    def test_2__upload_dependencies(self):
        upload_results = self.deploy_fast_api__dev.upload_lambda_dependencies_to_s3()
        assert list_set(upload_results) == LAMBDA_DEPENDENCIES__SERVERLESS_S3_BROWSER

    def test_3__create(self):
        assert self.deploy_fast_api__dev .create() is True

    def test_4__invoke(self):
        assert self.deploy_fast_api__dev .invoke().get('errorMessage') == DEFAULT__ERROR_MESSAGE__WHEN_FAST_API_IS_OK

    def test_4__invoke__function_url(self):
        version = {'version': version__osbot_serverless_s3_browser}
        assert self.deploy_fast_api__dev .invoke__function_url('/info/version') == version

    # def test_4__delete(self):
    #     assert self.deploy_fast_api__dev .delete() is True