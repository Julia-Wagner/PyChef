# ----------------------------- IMPORTS -------------------------------
import gspread
from google.oauth2.service_account import Credentials
from pyfiglet import Figlet
from colorama import Fore

# -------------------------- API CONNECTION ---------------------------
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("PyChef")

users = SHEET.worksheet("users")

def show_welcome_message():
    f = Figlet(font='big')
    print(Fore.BLUE + f.renderText('PyChef'))

show_welcome_message()
