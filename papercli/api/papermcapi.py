from __future__ import annotations

import requests
from requester import Requester


class Project():
    def __init__(self, id: str, requester: Requester):
        self.id: str = id
        self.requester: Requester = requester

    def __repr__(self) -> str:
        return f"<PaperMC-project: \"{self.id}\">"

    def get_versions(self) -> list[str]:
        return self.requester.get(self.id)["versions"]

    def get_version_groups(self) -> list[str]:
        return self.requester.get(self.id)["version_groups"]

    def get_build_numbers(self, mc_version: str) -> list[str]:
        return self.requester.get(f"{self.id}/versions/{mc_version}")["builds"]

    def get_build(self, mc_version: str, build: int) -> Build:
        return Build.from_json(
            self.requester.get(f"{self.id}/versions/{mc_version}/builds/{build}"),
            self,
            self.requester
        )

class Build():
    def __init__(
        self, 
        project: Project,
        requester: Requester,
        version: str, 
        build: int, 
        time: str, 
        channel: str, 
        promoted: bool, 
        changes: list[dict[str, str]],
        downloads: dict[str, dict[str, str]]
        ) -> None:
        self.project = project
        self.requester = requester
        self.version = version
        self.build = build
        self.time = time
        self.channel = channel
        self.promoted = promoted
        self.changes = changes
        self.downloads = downloads
    
    def __repr__(self) -> str:
        return f"<PaperMC-build: {self.build}>"
    
    def download(self, destination_path: str) -> None:
        self.requester.download(f"{self.project.id}/versions/{self.version}/builds/{self.build}/downloads/{self.downloads['application']['name']}", destination_path)

    @classmethod
    def from_json(cls, data: dict, project: Project, requester: Requester) -> Build:
        return cls(
            project=project,
            requester=requester,
            version=data["version"],
            build=data["build"],
            time=data["time"],
            channel=data["channel"],
            promoted=data["promoted"],
            changes=data["changes"],
            downloads=data["downloads"]
        )

class PaperApi():
    def __init__(self, base_url: str = "https://papermc.io/api/v2/projects/") -> None:
        self.requester: Requester = Requester(base_url)
    
    def get_projects(self) -> list[Project]:
        projects = self.requester.get(".")["projects"]
        return [Project(x, self.requester) for x in projects]

if __name__ == "__main__":
    p = PaperApi()
    proj = p.get_projects()[0]
    print(proj.get_build("1.18.1", proj.get_build_numbers("1.18.1")[-1]).download("./test/test.jar"))