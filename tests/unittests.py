import unittest

from requests_mock.mocker import Mocker
from papercli.paperapi import PaperApi, Project
from papercli.requester import Requester
from papercli.exceptions import InternalServerError, ResourceNotFound
import requests_mock


class TestApi(unittest.TestCase):
    def test_get_ids(self):
        ids: list[str]
        with requests_mock.Mocker() as m:
            m.get("https://papermc.io/api/v2/projects/", json = {
                "projects": ["paper", "other_project"]
            })
            ids = PaperApi().get_project_ids()

        self.assertIsInstance(ids, list)
        self.assertEqual(["paper", "other_project"], ids)
    
    def test_get_project(self):
        with requests_mock.Mocker() as m:
            m.get("https://papermc.io/api/v2/projects/paper", json = {"project_id":"paper","project_name":"Paper","version_groups":["1.8","1.18"],"versions":["1.17.1","1.18","1.18.1"]})
            proj = PaperApi().get_project("paper")
        
        self.assertIsInstance(proj, Project)
        self.assertIsInstance(proj.requester, Requester)
        self.assertEqual(proj.id, "paper")
    
    def test_get_project_ids(self):
        with requests_mock.Mocker() as m:
            m.get("https://papermc.io/api/v2/projects/", json = {"projects": ["paper", "velocity"]})
            projects = PaperApi().get_project_ids()
        
        self.assertIsInstance(projects, list)
        self.assertEqual(projects, ["paper", "velocity"])
    
    def test_get_projects(self):
        with requests_mock.Mocker() as m:
            m.get("https://papermc.io/api/v2/projects/", json = {"projects": ["paper", "velocity"]})
            m.get("https://papermc.io/api/v2/projects/paper", json = {"project_id":"paper","project_name":"Paper","version_groups":["1.8","1.18"],"versions":["1.17.1","1.18","1.18.1"]})
            m.get("https://papermc.io/api/v2/projects/velocity", json = {"project_id":"velocity","project_name":"Velocity","version_groups":["1.8","1.18"],"versions":["1.17.1","1.18","1.18.1"]})
            projects = PaperApi().get_projects()
        
        self.assertIsInstance(projects, list)
        self.assertEqual([x.id for x in projects], ["paper", "velocity"])
        self.assertEqual(projects[0].requester, projects[1].requester)

class TestRequester(unittest.TestCase):
    def test_request(self):
        r = Requester("https://example.com/")
        with requests_mock.Mocker() as m:
            m.get("https://example.com/server-error", status_code=500)
            m.get("https://example.com/not-found", status_code=404)
            self.assertRaises(InternalServerError, lambda: r.get("server-error"))
            self.assertRaises(ResourceNotFound, lambda: r.get("not-found"))

class TestProject(unittest.TestCase):
    def test_init(self):
        r = Requester("https://example.com")
        proj = Project("paper", r)

        self.assertIsInstance(proj, Project)
        self.assertEqual(proj.id, "paper")
        self.assertEqual(proj.requester, r)
    
    def test_get_versions(self):
        with requests_mock.Mocker() as m:
            m.get("https://papermc.io/api/v2/projects/paper", json = {"project_id":"paper","project_name":"Paper","version_groups":["1.8","1.18"],"versions":["1.17.1","1.18","1.18.1"]})
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

class TestBuild(unittest.TestCase):
    def test_from_json(self):
        pass # Test not implemented yet

if __name__ == "__main__":
    unittest.main()