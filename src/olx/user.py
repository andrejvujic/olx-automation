from .routes import LOGIN_ROUTE_PATH
from .session import Session

import requests
from bs4 import BeautifulSoup


class User:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        self.session = Session()

    def login(self) -> None:
        CSRF_TOKEN = self.session.get_CSRF_token()

        PAYLOAD = {
            "username": self.username,
            "password": self.password,
            "csrf_token": CSRF_TOKEN,
        }

        r = self.session.instance.post(
            LOGIN_ROUTE_PATH,
            data=PAYLOAD,
        )

        soup = BeautifulSoup(
            r.content,
            "html.parser",
        )

        print(
            soup.prettify(),
        )

        if not self.username in soup.text:
            raise BaseException(
                "Login attempt failed unexpectedly."
            )
