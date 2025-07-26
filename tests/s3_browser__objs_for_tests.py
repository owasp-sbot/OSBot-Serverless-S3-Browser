from fastapi                                                        import FastAPI
from osbot_utils.utils.Env                                          import set_env
from osbot_aws.testing.Temp__Random__AWS_Credentials                import Temp_AWS_Credentials
from osbot_local_stack.local_stack.Local_Stack                      import Local_Stack
from osbot_utils.type_safe.Type_Safe                                import Type_Safe
from starlette.testclient                                           import TestClient
from osbot_serverless_s3_browser.core.fast_api.S3_Browser__Fast_API import S3_Browser__Fast_API

S3_BROWSER__TEST__AWS_ACCOUNT_ID = '000022220000'

class S3_Browser__Test_APIs(Type_Safe):
    fast_api        : S3_Browser__Fast_API  = None
    fast_api__app   : FastAPI            = None
    fast_api__client: TestClient         = None
    local_stack     : Local_Stack        = None
    setup_completed : bool               = False

s3_browser_test_api = S3_Browser__Test_APIs()


def setup_local_stack() -> Local_Stack:                                 # todo: refactor this to the OSBot_Local_Stack code base
    Temp_AWS_Credentials().set_vars()
    set_env('AWS_ACCOUNT_ID', S3_BROWSER__TEST__AWS_ACCOUNT_ID)         # todo: fix the Temp_AWS_Credentials so that we don't need use this set_env
    local_stack = Local_Stack().activate()
    return local_stack

def setup__s3_browser_test_api():
        with s3_browser_test_api as _:
            if s3_browser_test_api.setup_completed is False:
                _.fast_api         = S3_Browser__Fast_API().setup()
                _.fast_api__app    = _.fast_api.app()
                _.fast_api__client = _.fast_api.client()
                _.local_stack      = setup_local_stack()
                _.setup_completed  = True
        return s3_browser_test_api
