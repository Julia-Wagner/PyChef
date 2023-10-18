# ----------------------------- IMPORTS -------------------------------
import gspread
from google.oauth2.service_account import Credentials
from pyfiglet import Figlet
from rich.console import Console
from rich.theme import Theme

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

def show_welcome_message():
    f = Figlet(font="big")
    console.print(f.renderText("PyChef"), style="blue")
    console.print("Select an option", style="heading")

show_welcome_message()
