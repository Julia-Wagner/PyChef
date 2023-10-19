# ----------------------------- IMPORTS -------------------------------
import gspread
from google.oauth2.service_account import Credentials
from pyfiglet import Figlet
from rich.console import Console
from rich.theme import Theme
import os

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

# ------------------------- STYLING THEMES ---------------------------
custom_theme = Theme({
    "error": "bold red",
    "heading": "bold underline",
    "option": "yellow"
})

console = Console(theme=custom_theme)

def clear_console():
    """
    Clear the console
    Code taken from https://www.delftstack.com/howto/python/python-clear-console/
    :return:
    """
    return os.system("cls" if os.name in ("nt", "dos") else "clear")

def show_welcome_message():
    clear_console()
    f = Figlet(font="big")
    console.print(f.renderText("PyChef"), style="blue")
    account_selection()

def account_selection():
    console.print("Select an option", style="heading")
    console.print("1 Log in to your account", style="option")
    console.print("2 Create an account", style="option")

    selection = input("\nEnter 1 or 2: \n")

    if selection == "1":
        print("1 selected")
    elif selection == "2":
        print("2 selected")
    else:
        print("Please select either 1 or 2")


show_welcome_message()
