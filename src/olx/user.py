from .routes import LOGIN_ROUTE_PATH, USERS_LISTINGS_ROUTE_PATH
from .session import Session
from .listing import Listing

import time
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

        if not self.username in soup.text:
            raise BaseException(
                "Login attempt failed unexpectedly."
            )

    def get_all_listings(self) -> list[Listing]:
        r = self.session.instance.get(
            USERS_LISTINGS_ROUTE_PATH.replace(
                "{USERNAME}",
                self.username,
            )
        )

        soup = BeautifulSoup(
            r.content,
            "html.parser",
        )

        listings = soup.find_all(
            "div",
            {
                "class": "artikal",
            }
        )

        listings = [Listing(l, session=self.session) for l in listings]

        return listings

    def create_listing(
        self,
        category: int,
        title: str,
        subtitle: str,
        location_1: int,
        location_2: int,
        description: str,
        price: int,
        state: str,
    ) -> Listing:
        SESSION_ID = self.session.get_SESSION_ID()

        all_listings = self.get_all_listings()

        PAYLOAD = {
            "kategorija": category,
            "sesija": SESSION_ID,
            "naslovartikla": title,
            "podnaslovartikla": subtitle,
            "oglas-kanton": location_1,
            "oglas-grad": location_2,
            "opis": description,
            "cijena": price,
            "stanje": state,
        }

        self.session.instance.post(
            "https://www.olx.ba/objava/zavrsi",
            data=PAYLOAD,
        )

        time.sleep(3)

        updated_all_listings = self.get_all_listings()

        listing = list(
            set(updated_all_listings) -
            set(all_listings),
        )[0]

        return listing
