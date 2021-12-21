import unittest

from papercli.requester import Requester
from papercli.exceptions import InternalServerError, ResourceNotFound
import requests_mock

class TestRequester(unittest.TestCase):
    def test_request(self):
        r = Requester("https://example.com/")
        with requests_mock.Mocker() as m:
            m.get("https://example.com/server-error", status_code=500)
            m.get("https://example.com/not-found", status_code=404)
            self.assertRaises(InternalServerError, lambda: r.get("server-error"))
            self.assertRaises(ResourceNotFound, lambda: r.get("not-found"))

if __name__ == "__main__":
    unittest.main()