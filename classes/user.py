from mixins import ClearConsole, StyleConsole
from getpass import getpass


class User(ClearConsole, StyleConsole):
    """"
    Class for user
    """
    console = StyleConsole.style()

    def __init__(self, user_id, username, password):
        self.user_id = user_id,
        self.username = username,
        self.password = password

    def login(self, new_account=False):
        self.clear_console()

        if new_account:
            User.console.print("\nAccount created successfully!\nYou can now log in", style="success")

        # input username until correct
        while True:
            try:
                username = input("\nPlease enter your username: \n")

                if users.find(username, in_column=2) is None:
                    raise ValueError("Username not found")

            except ValueError as e:
                User.console.print(f"{e}, please enter the correct username", style="error")
                continue
            else:
                break

        user_row = users.find(username, in_column=2).row
        row_values = users.row_values(user_row)

        # input password until correct
        while True:
            try:
                User.console.print("\nNote: for security reasons your password won´t be displayed while typing",
                              style="info")
                password = getpass("Please enter your password: \n")

                if row_values[2] != password:
                    raise ValueError("Password incorrect")

            except ValueError as e:
                User.console.print(f"{e}, please enter your password", style="error")
                continue
            else:
                break


    def create_account(self):
        self.clear_console()
        User.console.print("Please enter a username", style="heading")
        User.console.print("Username must be at least 4 characters long", style="info")

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

        User.console.print("\nPlease enter a password", style="heading")
        User.console.print("Password must be at least 6 characters long", style="info")

        # input password until valid selection was made
        while True:
            try:
                password = input("\nPassword: \n")

                if len(password) < 6:
                    raise ValueError("Password must be at least 4 characters long")

            except ValueError as e:
                User.console.print(f"{e}, please choose another password", style="error")
                continue
            else:
                break

        User.console.print("\nCreating account...", style="info")

        new_account = [increment_id(users), username, password]
        users.append_row(new_account)

        self.login(True)
