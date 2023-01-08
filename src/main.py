from credentials import Credentials
from olx.user import User

CREDENTIALS_FILE_PATH = "./credentials.json"

credentials = Credentials(
    CREDENTIALS_FILE_PATH,
)

user = User(
    credentials.username,
    credentials.password,
)

user.login()
user.create_listing(
    31,
    "Samsung Galaxy A50",
    "Telefon bukvalno nov",
    14,
    21,
    "Super stanje!",
    300,
    "koristeno",
)
