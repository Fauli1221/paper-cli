"""
Test the PaperApi class
"""

import unittest
import requests_mock
from papercli.paperapi import PaperApi, Project
from papercli.requester import Requester

class TestApi(unittest.TestCase):
    # pylint: disable=missing-docstring

    def test_get_ids(self):
        ids: list[str]
        with requests_mock.Mocker() as mocker:
            mocker.get("https://papermc.io/api/v2/projects/", json = {
                "projects": ["paper", "other_project"]
            })
            ids = PaperApi().get_project_ids()

        self.assertIsInstance(ids, list)
        self.assertEqual(["paper", "other_project"], ids)

    def test_get_project(self):
        with requests_mock.Mocker() as mocker:
            mocker.get("https://papermc.io/api/v2/projects/paper", 
                       json = {"project_id":"paper","project_name":"Paper",
                               "version_groups":["1.8","1.18"],"versions":["1.17.1","1.18","1.18.1"]})
            proj = PaperApi().get_project("paper")

        self.assertIsInstance(proj, Project)
        self.assertIsInstance(proj.requester, Requester)
        self.assertEqual(proj.id, "paper")

    def test_get_project_ids(self):
        with requests_mock.Mocker() as mocker:
            mocker.get("https://papermc.io/api/v2/projects/", json = {"projects": ["paper", "velocity"]})
            projects = PaperApi().get_project_ids()

        self.assertIsInstance(projects, list)
        self.assertEqual(projects, ["paper", "velocity"])

    def test_get_projects(self):
        with requests_mock.Mocker() as mocker:
            mocker.get("https://papermc.io/api/v2/projects/",
                       json = {"projects": ["paper", "velocity"]})
            mocker.get("https://papermc.io/api/v2/projects/paper",
                       json = {"project_id":"paper","project_name":"Paper",
                               "version_groups":["1.8","1.18"],"versions":["1.17.1","1.18","1.18.1"]})
            mocker.get("https://papermc.io/api/v2/projects/velocity",
                       json = {"project_id":"velocity","project_name":"Velocity",
                               "version_groups":["1.8","1.18"],"versions":["1.17.1","1.18","1.18.1"]})
            projects = PaperApi().get_projects()

        self.assertIsInstance(projects, list)
        self.assertEqual([x.id for x in projects], ["paper", "velocity"])
        self.assertEqual(projects[0].requester, projects[1].requester)

if __name__ == "__main__":
    unittest.main()
