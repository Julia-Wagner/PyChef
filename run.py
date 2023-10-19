# ----------------------------- IMPORTS -------------------------------
import gspread
from google.oauth2.service_account import Credentials
from pyfiglet import Figlet
from rich.console import Console
from rich.theme import Theme
from getpass import getpass
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
    "option": "yellow",
    "info": "dim",
    "success": "bold green"
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
        login()
    elif selection == "2":
        create_account()
    else:
        console.print("Please select either 1 or 2", style="error")

def login():
    # input username until correct
    while True:
        try:
            username = input("\nPlease enter your username: \n")

            if users.find(username, in_column=2) is None:
                raise ValueError("Username not found")

        except ValueError as e:
            console.print(f"{e}, please enter the correct username", style="error")
            continue
        else:
            break

    user_row = users.find(username, in_column=2).row
    row_values = users.row_values(user_row)

    # input password until correct
    while True:
        try:
            console.print("\nNote: for security reasons your password won´t be displayed while typing", style="info")
            password = getpass("Please enter your password: \n")

            if row_values[2] != password:
                raise ValueError("Password incorrect")

        except ValueError as e:
            console.print(f"{e}, please enter your password", style="error")
            continue
        else:
            break

    console.print("\nYour are logged in!", style="success")

def create_account():
    clear_console()
    console.print("Please enter a username", style="heading")
    console.print("Username must be at least 4 characters long", style="info")

    # input username until valid selection was made
    while True:
        try:
            username = input("\nUsername: \n")

            if len(username) < 4:
                raise ValueError("Username must be at least 4 characters long")

            if users.find(username, in_column=2):
                raise ValueError("Username is already taken")

        except ValueError as e:
            console.print(f"{e}, please choose another username", style="error")
            continue
        else:
            break

    console.print("\nPlease enter a password", style="heading")
    console.print("Password must be at least 6 characters long", style="info")

    # input password until valid selection was made
    while True:
        try:
            password = input("\nPassword: \n")

            if len(password) < 6:
                raise ValueError("Password must be at least 4 characters long")

        except ValueError as e:
            console.print(f"{e}, please choose another password", style="error")
            continue
        else:
            break

    console.print("\nCreating account...", style="info")

    new_account = [increment_id(users), username, password]
    users.append_row(new_account)

    console.print("\nAccount created successfully!", style="success")

def increment_id(sheet):
    last_id = sheet.get_all_values()[-1][0]

    if last_id != "id":
        new_id = int(last_id) + 1
    else:
        new_id = 1
    return new_id

show_welcome_message()
