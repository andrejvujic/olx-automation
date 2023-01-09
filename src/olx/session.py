import requests
from bs4 import BeautifulSoup

from .routes import *
from .category import Category


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

    def get_SESSION_ID(self) -> None:
        r = self.instance.get(
            ADD_LISTING_ROUTE_PATH,
        )

        soup = BeautifulSoup(
            r.content,
            "html.parser",
        )

        session_id = soup.find(
            "input",
            {
                "name": "sesija",
            },
        )["value"]

        return session_id

    def get_list_of_categories(
        self,
        title: str,
    ) -> list[Category]:
        r = self.instance.get(
            SUGGEST_CATEGORY_FOR_LISTING_ROUTE_PATH.replace(
                "{TITLE}",
                title,
            )
        )

        response = r.json()

        if response["status"] == 1:
            suggestions = response["prijedlozi"]
            suggestions = [Category(s) for s in suggestions]

            return suggestions

        return None
