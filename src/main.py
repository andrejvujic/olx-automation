from credentials import Credentials
from olx.user import User

import time

CREDENTIALS_FILE_PATH = "../credentials.json"

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
        "iPhone XS Max Gold 512gb",
        "Ekstra stanje",
        location[0],
        location[1],
        "Telefon je u ekstra stanju\n\n\nNema nikava ostecenja\n\n\nPrvi vlasnik\n\n\n065/020-250",
        "PO DOGOVORU",
        "koristeno",
        images=[
             "/home/pi/Desktop/Images/image-1.jpg",
             "/home/pi/Desktop/Images/image-2.jpg",
             "/home/pi/Desktop/Images/image-3.jpg",
             "/home/pi/Desktop/Images/image-4.jpg",
             "/home/pi/Desktop/Images/image-5.jpg",
        ],
    )

    print(
        "[olx] Listing created."
    )

    time.sleep(
        300,
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
