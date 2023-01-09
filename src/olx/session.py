import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

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

    def pick_location(self) -> tuple:
        r = self.instance.get(
            PROFILE_SETTINGS_ROUTE_PATH,
        )

        soup = BeautifulSoup(
            r.content,
            "html.parser",
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

        def parse(
            option: Tag,
        ) -> tuple:
            if not option["value"] or not int(
                option["value"],
            ):
                return None

            return (
                option["value"],
                option.get_text(),
            )

        options = [parse(o) for o in options]

        for option in options:
            if not option:
                continue

            canton_id = option[0]
            canton_title = option[1]

            _ = f"{canton_id}".ljust(
                10,
            )

            print(
                f"{_} - {canton_title}",
            )

        canton_id = input(
            "\n\n\nPick ID of canton: "
        )

        r = self.instance.get(
            CITIES_IN_CANTON_ROUTE_PATH.replace(
                "{CANTON_ID}",
                canton_id,
            ),
        )

        soup = BeautifulSoup(
            r.content,
            "html.parser",
        )

        options = soup.find_all(
            "option",
        )

        options = [parse(o) for o in options]

        print(
            "\n\n\n",
        )

        for option in options:
            if not option:
                continue

            city_id = option[0]
            city_title = option[1]

            _ = f"{city_id}".ljust(
                10,
            )

            print(
                f"{_} - {city_title}",
            )

        city_id = input(
            "\n\n\nPick ID of city: "
        )

        return (
            canton_id,
            city_id,
        )
