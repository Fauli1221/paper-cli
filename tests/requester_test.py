"""
Test the Requester
"""

import unittest
import requests_mock
from papercli.requester import Requester
from papercli.exceptions import InternalServerError, ResourceNotFound

class TestRequester(unittest.TestCase):
    # pylint: disable=missing-docstring

    def test_request(self):
        requester = Requester("https://example.com/")
        with requests_mock.Mocker() as mocker:
            mocker.get("https://example.com/server-error", status_code=500)
            mocker.get("https://example.com/not-found", status_code=404)
            self.assertRaises(InternalServerError, lambda: requester.get("server-error"))
            self.assertRaises(ResourceNotFound, lambda: requester.get("not-found"))

if __name__ == "__main__":
    unittest.main()
