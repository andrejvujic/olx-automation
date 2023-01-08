import json


class Credentials:
    def __init__(self, path: str) -> None:
        credentials = self.load(
            path,
        )
        self.username = credentials['username']
        self.password = credentials['password']

    @staticmethod
    def load(
        path: str,
        MODE: str = "r",
    ) -> dict:
        with open(path, MODE) as f:
            return json.load(
                f,
            )
