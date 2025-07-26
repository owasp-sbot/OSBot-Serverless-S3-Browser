from unittest                                                               import TestCase
from osbot_aws.deploy.Deploy_Lambda                                         import Deploy_Lambda
from osbot_utils.utils.Objects                                              import __
from osbot_serverless_s3_browser.utils.deploy.Deploy__Serverless_S3_Browser import Deploy__Serverless_S3_Browser
from osbot_serverless_s3_browser.utils.deploy.Schema__AWS_Setup__Serverless_S3_Browser import \
    Schema__AWS_Setup__Serverless_S3_Browser
from tests.s3_browser__objs_for_tests                                       import setup_local_stack, S3_BROWSER__TEST__AWS_ACCOUNT_ID, S3_BROWSER__TEST__AWS_DEFAULT_REGION


class test_Deploy__Serverless_S3_Browser(TestCase):
    @classmethod
    def setUpClass(cls):
        setup_local_stack()                                                 # deploy lambda to localstack
        cls.deploy_s3_browser = Deploy__Serverless_S3_Browser()

    def test_deploy_lambda(self):
        with self.deploy_s3_browser.deploy_lambda() as _:
            assert type(_) is Deploy_Lambda
            assert _.lambda_name()     == 'serverless-s3-browser__dev'
            assert _.package.s3_bucket == '000022220000--osbot-lambdas--eu-west-2'
            assert _.package.s3_bucket == f'{S3_BROWSER__TEST__AWS_ACCOUNT_ID}--osbot-lambdas--{S3_BROWSER__TEST__AWS_DEFAULT_REGION}'

    # tests for main methods

    def test_1__setup_aws_environment(self):
        with self.deploy_s3_browser.setup_aws_environment() as _:
            assert type(_) is Schema__AWS_Setup__Serverless_S3_Browser
            assert _.obj() == __(bucket__osbot_lambdas__exists = True                                    ,
                                 bucket__osbot_lambdas__name   = '000022220000--osbot-lambdas--eu-west-2',
                                 current_aws_region            = 'eu-west-2'                             )

    def test_2__deploy(self):
        with self.deploy_s3_browser as _:
            assert _.lambda_function().exists() is False
            result = _.deploy()
            print(result)
            assert _.lambda_function().exists() is True
            assert _.lambda_function().delete() is True
            assert _.lambda_function().exists() is False

