import requests


class Response:
    def __init__(self, status_code):
        self.status_code = status_code


class MockRequests:
    _host_name = ""
    _last_response = None
    @staticmethod
    def put(url, data=None, **kwargs):
        if url == MockRequests._host_name:
            MockRequests._last_response = Response(200)
            return MockRequests._last_response
        MockRequests._last_response = Response(400)
        return MockRequests._last_response

    @staticmethod
    def load_host(host_name):
        MockRequests._host_name = host_name
