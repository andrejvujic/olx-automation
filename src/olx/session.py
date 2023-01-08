import requests
from bs4 import BeautifulSoup

from .routes import INDEX_ROUTE_PATH


class Session:
    def __init__(self) -> None:
        self.instance = requests.session()

        HEADERS = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.3",
        }
        self.instance.headers = HEADERS

    def get_CSRF_token(self) -> None:
        r = self.instance.get(
            INDEX_ROUTE_PATH,
        )

        soup = BeautifulSoup(
            r.content,
            "html.parser",
        )

        token = soup.find(
            "input",
            {
                "name": "csrf_token",
            },
        )["value"]

        return token
