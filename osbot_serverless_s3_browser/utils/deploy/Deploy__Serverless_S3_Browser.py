from osbot_aws.AWS_Config                                                               import AWS_Config
from osbot_aws.deploy.Deploy_Lambda                                                     import Deploy_Lambda
from osbot_utils.decorators.methods.cache_on_self                                       import cache_on_self
from osbot_utils.helpers.Safe_Id                                                        import Safe_Id
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe
from osbot_serverless_s3_browser.lambdas.handler                                        import handler
from osbot_serverless_s3_browser.utils.deploy.Schema__AWS_Setup__Serverless_S3_Browser  import Schema__AWS_Setup__Serverless_S3_Browser

BASE__LAMBDA_NAME  = 'serverless-s3-browser'

class Deploy__Serverless_S3_Browser(Type_Safe):
    stage : Safe_Id = Safe_Id('dev')

    @cache_on_self
    def aws_config(self):
        return AWS_Config()

    @cache_on_self
    def s3(self):
        return self.lambda_function().s3()

    @cache_on_self
    def deploy_lambda(self):
        deploy_lambda = Deploy_Lambda(handler, lambda_name=self.lambda_name())
        return deploy_lambda

    # main methods

    def deploy(self):
        with self.deploy_lambda() as _:
            result = _.update()
            if result != "Successful":
                raise Exception(f"Lambda update failed: {result}")
            return True

    def lambda_name(self):
        return f'{BASE__LAMBDA_NAME}__{self.stage}'

    def lambda_function(self):
        return self.deploy_lambda().lambda_function()

    def lambda_files_bucket_name(self):
        return self.lambda_function().s3_bucket

    def setup_aws_environment(self):

        kwargs = dict(bucket__osbot_lambdas__exists = self.s3().bucket_exists(self.lambda_files_bucket_name()),
                      bucket__osbot_lambdas__name   = self.lambda_files_bucket_name(),
                      current_aws_region            = self.aws_config().region_name())

        aws_setup = Schema__AWS_Setup__Serverless_S3_Browser(**kwargs)
        with aws_setup as _:
            if _.bucket__osbot_lambdas__exists is False:
                result = self.s3().bucket_create(_.bucket__osbot_lambdas__name, _.current_aws_region)
                if result.get('status') == 'ok':
                    _.bucket__osbot_lambdas__exists = True
        return aws_setup
