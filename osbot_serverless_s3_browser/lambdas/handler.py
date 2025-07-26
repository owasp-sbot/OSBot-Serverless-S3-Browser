LAMBDA_DEPENDENCIES =  ['osbot-fast-api==0.7.32', 'mangum'] #'fastapi',

from osbot_aws.Dependencies import load_dependencies

load_dependencies(LAMBDA_DEPENDENCIES)

from osbot_serverless_s3_browser.core.fast_api.S3_Browser__Fast_API import S3_Browser__Fast_API

with S3_Browser__Fast_API() as _:
    _.setup()
    handler = _.handler()
    app     = _.app()

def run(event, context=None):
    return handler(event, context)