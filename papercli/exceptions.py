class InternalServerError(Exception):
    def __init__(self, status_code: int) -> None:
        super().__init__(f"received a {status_code} - something is wrong with the server. Try again later")

class ResourceNotFound(Exception):
    def __init__(self) -> None:
        super().__init__("the requested resource was not found")