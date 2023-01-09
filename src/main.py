from credentials import Credentials
from olx.user import User

import time

CREDENTIALS_FILE_PATH = "./credentials.json"

credentials = Credentials(
    CREDENTIALS_FILE_PATH,
)

user = User(
    credentials.username,
    credentials.password,
)

user.login()

location = user.get_location()

while True:
    print(
        "[olx] Creating listing..."
    )

    listing = user.create_listing(
        31,
        "iPhone XS Max",
        "Ekstra stanje",
        location[0],
        location[1],
        "Telefon je u ekstra stanju\nNema nikava ostecenja\nPrvi vlasnik\n065/020-250",
        730,
        "koristeno",
    )

    print(
        "[olx] Listing created."
    )

    time.sleep(
        3600,
    )

    print(
        "[olx] Deleting listing...",
    )

    listing.delete()

    print(
        "[olx] Listing deleted.",
    )

    time.sleep(
        30,
    )
