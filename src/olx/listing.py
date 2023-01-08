from bs4.element import Tag

from .session import Session
from .routes import DELETE_LISTING_ROUTE_PATH


class Listing:
    def __init__(
        self,
        listing_element: Tag,
        session: Session,
    ) -> None:
        self.ID = listing_element.get(
            "id",
        ).replace(
            "art_",
            "",
        )

        self.url = listing_element.find(
            "a",
        ).get(
            "href",
        )

        self.title = listing_element.find(
            "p",
            {
                "class": "na",
            }
        ).get_text()

        self.element = listing_element
        self.session = session

    def delete(self) -> None:
        PAYLOAD = {
            "id": self.ID,
        }

        self.session.instance.post(
            DELETE_LISTING_ROUTE_PATH,
            data=PAYLOAD,
        )

    def __repr__(self) -> str:
        return f"""
    {self.title}
        - ID: {self.ID}
        - URL: {self.url}
    \n
    """
