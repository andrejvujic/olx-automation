from bs4.element import Tag

from .session import Session


class Listing:
    def __init__(self, listing_element: Tag, session: Session) -> None:
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

    def __repr__(self) -> str:
        return f"""
    {self.title}
        - ID: {self.ID}
        - URL: {self.url}
    \n
    """
