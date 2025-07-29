from unittest                                                               import TestCase
from osbot_fast_api_serverless.deploy.Deploy__Serverless__Fast_API          import DEFAULT__ERROR_MESSAGE__WHEN_FAST_API_IS_OK
from osbot_serverless_s3_browser.utils.Version                              import version__osbot_serverless_s3_browser
from osbot_utils.utils.Misc                                                 import list_set
from osbot_serverless_s3_browser.utils.deploy.Deploy__Serverless_S3_Browser import Deploy__Serverless_S3_Browser, LAMBDA_DEPENDENCIES__SERVERLESS_S3_BROWSER
from tests.s3_browser__objs_for_tests                                       import setup_local_stack


class test_Deploy__Serverless_S3_Browser__to__dev(TestCase):

    @classmethod
    def setUpClass(cls):
        skip__if_not__in_github_actions()
        setup_local_stack()
        cls.deploy_fast_api__dev  = Deploy__Serverless_S3_Browser(stage = 'dev')

    def test_1__check_stages(self):
        assert self.deploy_fast_api__dev .stage == 'dev'

    def test_2__upload_dependencies(self):                                                  # add support for Lambda_Layer_Create.remove_preinstalled_packages_in_lambda_environment
        upload_results = self.deploy_fast_api__dev.upload_lambda_dependencies_to_s3()
        assert list_set(upload_results) == LAMBDA_DEPENDENCIES__SERVERLESS_S3_BROWSER

    def test_3__create(self):
        assert self.deploy_fast_api__dev .create() is True

    def test_4__invoke(self):
        assert self.deploy_fast_api__dev .invoke().get('errorMessage') == DEFAULT__ERROR_MESSAGE__WHEN_FAST_API_IS_OK

    def test_5__invoke__function_url(self):
        version = {'version': version__osbot_serverless_s3_browser}
        assert self.deploy_fast_api__dev .invoke__function_url('/info/version') == version

    def test_6__delete(self):
        assert self.deploy_fast_api__dev .delete() is True
