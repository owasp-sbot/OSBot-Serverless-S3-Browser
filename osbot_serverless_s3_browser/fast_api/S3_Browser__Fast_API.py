from osbot_fast_api_serverless.fast_api.Serverless__Fast_API  import Serverless__Fast_API
from osbot_serverless_s3_browser.fast_api.routes.Routes__Info import Routes__Info


class S3_Browser__Fast_API(Serverless__Fast_API):

    def setup_routes(self):
        self.add_routes(Routes__Info)