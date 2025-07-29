from osbot_aws.aws.lambda_.boto3__lambda import load_dependencies
#
LAMBDA_DEPENDENCIES =  ['osbot-fast-api-serverless']

load_dependencies(LAMBDA_DEPENDENCIES)

from osbot_serverless_s3_browser.fast_api.S3_Browser__Fast_API import S3_Browser__Fast_API

with S3_Browser__Fast_API() as _:
    _.setup()
    handler = _.handler()
    app     = _.app()

def run(event, context=None):
    return handler(event, context)