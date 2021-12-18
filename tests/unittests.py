import unittest
from papercli.paperapi import PaperApi
import requests_mock

class TestApi(unittest.TestCase):
    def test_get_ids(self):
        ids: list[str]
        with requests_mock.Mocker() as m:
            m.get("https://papermc.io/api/v2/projects/", json = {
                "projects": ["paper"]
            })
            ids = PaperApi().get_project_ids()

        self.assertIsInstance(ids, list)
        self.assertEqual(ids[0], "paper")

if __name__ == "__main__":
    unittest.main()