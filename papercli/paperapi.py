"""
Declare PaperMC Api resources
"""

from __future__ import annotations
import os
from papercli.requester import Requester
import asyncio

class Project():
    """
    A class representing a PaperMC project, like `paper`
    """

    # pylint: disable=invalid-name
    def __init__(self, id: str, requester: Requester):
        self.id: str = id
        self.requester: Requester = requester

    def __repr__(self) -> str:
        return f"<PaperMC-project: \"{self.id}\">"

    def get_versions(self) -> list[str]:
        """
        Get all versions which are available for this Project
        """

        return self.requester.get(self.id)["versions"]

    def get_version_groups(self) -> list[str]:
        """
        Get all version groups which are available for this Project
        """

        return self.requester.get(self.id)["version_groups"]

    def get_build_numbers(self, mc_version: str) -> list[int]:
        """
        Get the numbers of all available builds for this project
        """

        return [int(num) for num in self.requester.get(f"{self.id}/versions/{mc_version}")["builds"]]

    # pylint: disable=redefined-outer-name
    def get_build(self, mc_version: str, build: int) -> Build:
        """
        Get a certain build as a Build instance
        """

        return Build.from_json(
            self.requester.get(f"{self.id}/versions/{mc_version}/builds/{build}"),
            self,
            self.requester
        )
    
    async def get_build_coro(self, mc_version: str, build: int) -> Build:
        """
        Get a certain build as a Build instance
        """

        return Build.from_json(
            self.requester.get(f"{self.id}/versions/{mc_version}/builds/{build}"),
            self,
            self.requester
        )

    def get_latest_build(self, mc_version: str) -> Build:
        """
        Get the latest Build from this Project
        """

        return self.get_build(mc_version, self.get_build_numbers(mc_version)[-1])

    async def get_all_builds_coro(self, mc_version: str, builds: list[Build], build_numbers: list[int] = None) -> list[Build]:
        """
        Coroutine for getting all builds
        """

        if not build_numbers:
            build_numbers = self.get_build_numbers(mc_version)

        coros = []
        for num in build_numbers:
            coros.append(self.get_build_coro(mc_version, num))
        builds += await asyncio.gather(*coros)
        return builds
    
    def get_all_builds(self, mc_version: str, build_numbers: list[int] = None) -> list[Build]:
        """
        Get all builds(requested asynchronously)

        mc_version (str): 
            your target minecraft version

        build_numbers (list[int]): 
            the numbers of the builds you want to get (default are all)
        """

        # Create a new empty list of Builds
        builds: list[Build] = []

        # Run the `get_all_builds` coroutine with the version, and the reference of the builds list
        asyncio.run(self.get_all_builds_coro(mc_version, builds, build_numbers))

        # Return the builds, after they were mutated by their reference
        return builds

class Build():
    """
    A class representing a certain Build from the PaperMC API
    """

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
        self.time: str = time.split("T")[0].replace("-", ".")
        self.channel = channel
        self.promoted = promoted
        self.changes = changes
        self.downloads = downloads

    def __repr__(self) -> str:
        return f"<PaperMC-build: {self.build}>"

    def __str__(self) -> str:
        return f"{self.build}, {self.channel}, {self.time}{', promoted' if self.promoted else ''}"

    def download(self, destination_path: str) -> None:
        """
        Download this build to the destination path

        Example 1:
        ```py
        my_build.download("./path/file.jar")
        ```
        Example 2:
        ```py
        my_build.download("./path/)
        ```
        """

        # pylint: disable=line-too-long
        self.requester.download(
                f"{self.project.id}/versions/{self.version}/builds/{self.build}/downloads/{self.downloads['application']['name']}",
                destination_path
                    if destination_path.endswith(".jar")
                    else os.path.join(destination_path, self.downloads["application"]["name"])
            )

    @classmethod
    def from_json(cls, data: dict, project: Project, requester: Requester) -> Build:
        """
        Create a new instance from a JSON object
        """

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
    """
    The class used to interact with the PaperMC API
    """

    def __init__(self, base_url: str = "https://papermc.io/api/v2/projects/") -> None:
        self.requester: Requester = Requester(base_url)

    def get_project_ids(self) -> list[str]:
        """
        Get all project ids
        """

        return self.requester.get(".")["projects"]

    def get_projects(self) -> list[Project]:
        """
        Get all projects as a list of Project instances
        """

        return [Project(x, self.requester) for x in self.get_project_ids()]

    # pylint: disable=invalid-name
    def get_project(self, id: str) -> Project:
        """
        Get a certain Project as a Project instance
        """

        return Project(id, self.requester)

    def latest_project(self) -> Project:
        """
        Get the latest Project

        DOES NOT have to be the newest, but the last one listed
        """

        return self.get_projects()[-1]

    def latest_build(self) -> Build:
        """
        Get the latest Build from the latest Project
        """

        project = self.latest_project()
        version = project.get_versions()[-1]
        return project.get_build(version, project.get_build_numbers(version)[-1])

if __name__ == "__main__":
    p = PaperApi()
    proj = p.get_projects()[0]
    print(proj.get_all_builds("1.18.1"))