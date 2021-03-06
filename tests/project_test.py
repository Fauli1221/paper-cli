"""
Test the Project class
"""

import unittest
import requests_mock
from papercli.paperapi import PaperApi, Project
from papercli.requester import Requester

class TestProject(unittest.TestCase):
    # pylint: disable=missing-docstring

    def test_init(self):
        requester = Requester("https://example.com")
        proj = Project("paper", requester)

        self.assertIsInstance(proj, Project)
        self.assertEqual(proj.id, "paper")
        self.assertEqual(proj.requester, requester)

    def test_get_versions(self):
        with requests_mock.Mocker() as mocker:
            mocker.get(
                "https://papermc.io/api/v2/projects/paper", 
                json = {"project_id":"paper","project_name":"Paper",
                        "version_groups":["1.8","1.18"],"versions":["1.17.1","1.18","1.18.1"]})
            version_groups = PaperApi().get_project("paper").get_version_groups()
            versions = PaperApi().get_project("paper").get_versions()

        self.assertEqual(version_groups, ["1.8", "1.18"])
        self.assertEqual(versions, ["1.17.1","1.18","1.18.1"])

    def test_get_build(self):
        pass # Test not implemented yet

    def test_get_builds(self):
        pass # Test not implemented yet

    def test_get_build_numbers(self):
        pass # Test not implemented yet

    def test_get_latest_build(self):
        pass # Test not implemented yet

if __name__ == "__main__":
    unittest.main()
