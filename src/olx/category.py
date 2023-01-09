from bs4 import BeautifulSoup


class Category:
    def __init__(
        self,
        html: str,
    ) -> None:
        soup = BeautifulSoup(
            html,
            "html.parser",
        )

        self.element = soup.find(
            "a",
        )

        self.id = self.element.get(
            "id",
        ).replace(
            "prijedlog_kat_",
            "",
        )

        self.id = int(
            self.id,
        )

        self.name = self.element.get_text()
        _ = self.name.split("»")
        _ = [e.strip() for e in _]
        self.name = " > ".join(
            _,
        )
