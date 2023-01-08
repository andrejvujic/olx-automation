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
