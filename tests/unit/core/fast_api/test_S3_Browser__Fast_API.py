from unittest                                                    import TestCase
from fastapi                                                     import FastAPI
from osbot_utils.type_safe.Type_Safe                             import Type_Safe
from osbot_fast_api_serverless.fast_api.Serverless__Fast_API     import Serverless__Fast_API
from osbot_utils.utils.Objects                                   import base_types
from osbot_aws.testing.skip_tests                                import skip__if_not__in_github_actions
from osbot_fast_api.api.Fast_API                                 import ENV_VAR__FAST_API__AUTH__API_KEY__NAME, ENV_VAR__FAST_API__AUTH__API_KEY__VALUE, Fast_API
from osbot_local_stack.local_stack.Local_Stack                   import Local_Stack
from osbot_utils.utils.Env                                       import get_env
from starlette.testclient                                        import TestClient
from osbot_serverless_s3_browser.fast_api.S3_Browser__Fast_API   import S3_Browser__Fast_API
from osbot_serverless_s3_browser.fast_api.routes.Routes__Info    import ROUTES_PATHS__INFO
from osbot_serverless_s3_browser.utils.Version                   import version__osbot_serverless_s3_browser
from tests.s3_browser__objs_for_tests                            import setup__s3_browser_test_api, S3_Browser__Test_APIs

class test_S3_Browser__Fast_API(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.s3_browser_test_apis = setup__s3_browser_test_api()
        cls.fast_api             = cls.s3_browser_test_apis.fast_api
        cls.client               = cls.s3_browser_test_apis.fast_api__client

    def test__init__(self):
        with self.s3_browser_test_apis as _:
            assert type(_)                  is S3_Browser__Test_APIs
            assert type(_.fast_api        ) is S3_Browser__Fast_API
            assert base_types(_.fast_api  ) == [Serverless__Fast_API, Fast_API, Type_Safe, object]
            assert type(_.fast_api__app   ) is FastAPI
            assert type(_.fast_api__client) is TestClient
            assert type(_.local_stack     ) is Local_Stack
            assert self.fast_api            == _.fast_api
            assert self.client              == _.fast_api__client

    def test__client__root_path(self):
        path = '/info/version'
        response__no_auth = self.client.get(url=path)
        assert response__no_auth.status_code == 401
        assert response__no_auth.json()      == { 'data'   : None                                                                 ,
                                                  'error'  : None                                                                 ,
                                                  'message': 'Client API key is missing, you need to set it on a header or cookie',
                                                  'status' : 'error'                                                              }
        auth_key_name   = get_env(ENV_VAR__FAST_API__AUTH__API_KEY__NAME)
        auth_key_value = get_env(ENV_VAR__FAST_API__AUTH__API_KEY__VALUE)
        assert auth_key_name  is not None
        assert auth_key_value is not None
        headers = {auth_key_name:auth_key_value}
        response__with_auth = self.client.get(url=path, headers=headers)
        assert response__with_auth.json() == {'version': version__osbot_serverless_s3_browser }


    def test__check_if_local_stack_is_setup(self):
        skip__if_not__in_github_actions()
        with self.s3_browser_test_apis.local_stack as _:
            assert _.is_local_stack_configured_and_available() is True


    def test__config_fast_api_routes(self):
        assert self.fast_api.routes_paths() == ROUTES_PATHS__INFO

