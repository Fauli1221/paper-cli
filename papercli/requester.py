"""
Declare the Requester class
"""

from urllib.parse import urljoin
import requests
from papercli.exceptions import InternalServerError, ResourceNotFound

class Requester(requests.Session):
    """
    A simple Requester used for fetching data
    """

    def __init__(self, base_url: str) -> None:
        """
        Create a new Requester using a certain `base_url`

        Example:
        ```py
        Requester("https://example.com")
        ```
        """
        self.base_url: str = base_url
        super().__init__()

    @staticmethod
    def process_response(response: requests.Response) -> dict:
        """
        Can raise:
        -   `InternalServerError`
        -   `ResourceNotFound`
        """
        status_code = response.status_code
        if str(status_code)[0] == "5":
            raise InternalServerError(status_code)
        if status_code == 404:
            raise ResourceNotFound()

        return response.json()

    def get(self, path: str) -> dict:
        """
        Perform a `get` request to a certain `path` of the `base_url` with the `data`

        Example:
        ```py
        my_requester.get("useful/api/resource")
        ```
        """
        return self.process_response(super().get(urljoin(self.base_url, path)))

    def download(self, path: str, destination: str):
        """
        Download a file from the `path` to the local `destination`

        Example:
        ```py
        my_requester.download("useful/file.jar", "myDir/file.jar")
        ```
        """
        with super().get(urljoin(self.base_url, path), stream=True) as res:
            with open(destination, "wb") as file:
                for chunk in res.iter_content(chunk_size=16*1024):
                    file.write(chunk)
