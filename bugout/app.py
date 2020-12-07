from .data import Method
from .calls import ApiCalls


class Bugout:
    def __init__(self, url, port) -> None:
        self.url = url
        self.port = port

    def _call(self, method: Method, path: str, **kwargs):
        url = f"{self.url.rstrip('/')}:{self.port}/{path.rstrip('/')}"

        result = ApiCalls.make_request(method=method, url=url, **kwargs)

        return result
