import requests
from bs4 import BeautifulSoup

from .routes import INDEX_ROUTE_PATH


class Session:
    def __init__(self) -> None:
        self.session = requests.session()
        self.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.3"

    def get_CSRF_token(self) -> None:
        HEADERS = {
            "User-Agent": self.user_agent,
        }

        r = self.session.get(
            INDEX_ROUTE_PATH,
            headers=HEADERS,
        )

        soup = BeautifulSoup(
            r.content,
            "html.parser",
        )

        print(soup.prettify())

        token = soup.find(
            "input",
            {
                "name": "csrf_token",
            },
        )["value"]

        return token
