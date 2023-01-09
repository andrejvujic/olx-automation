from .routes import *
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

        with open("index.html", "w") as f:
            f.write(
                soup.prettify(),
            )

        if not r.status_code == 200 or not r.ok:
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
        images: list[str],
    ) -> Listing:
        SESSION_ID = self.session.get_SESSION_ID()

        for image in images:
            files = {
                "myfile": open(
                    image, "rb",
                ),
            }

            r = self.session.instance.post(
                ADD_IMAGE_TO_LISTING_ROUTE_PATH.replace(
                    "{SESSION_ID}",
                    SESSION_ID,
                ),
                files=files,
            )

            response = r.json()

            if response["status"] == 1:
                image_id = response["id"]
                image_url = response["slika"]

                print(
                    f"Upload done:\n   - ID: {image_id}\n   - URL: {image_url}",
                )
            else:
                print(
                    "Encountered issue when uploading."
                )

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
            CONFIRM_ADD_LISTING_PATH,
            data=PAYLOAD,
        )

        time.sleep(3)

        updated_all_listings = self.get_all_listings()

        listing = list(
            set(updated_all_listings) -
            set(all_listings),
        )[0]

        return listing

    def get_location(self) -> tuple:
        canton_id, city_id = None, None

        r = self.session.instance.get(
            PROFILE_SETTINGS_ROUTE_PATH,
        )

        soup = BeautifulSoup(
            r.content,
            "html.parser",
        )

        with open("index.html", "w") as f:
            f.write(
                soup.prettify(),
            )

        container = soup.find(
            "select",
            {
                "name": "kanton",
            }
        )

        options = container.find_all(
            "option",
        )

        for option in options:
            if "selected" in option.attrs:
                canton_id = option["value"]

        container = soup.find(
            "select",
            {
                "name": "grad",
            }
        )

        options = container.find_all(
            "option",
        )

        for option in options:
            if "selected" in option.attrs:
                city_id = option["value"]

        return (
            int(
                canton_id,
            ),
            int(
                city_id,
            ),
        )
