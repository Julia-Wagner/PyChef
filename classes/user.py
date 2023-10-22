from getpass import getpass
from .mixins import ClearConsole, StyleConsole
from .sheet import SheetService


class User(ClearConsole, StyleConsole, SheetService):
    """"
    Class for user
    """
    console = StyleConsole.style()
    users = SheetService.get_worksheet("users")

    def __init__(self, user_id, username, password):
        self.user_id = user_id
        self.username = username
        self.password = password

        self.add_user_to_sheet()

    def add_user_to_sheet(self):
        new_account = [self.user_id, self.username, self.password]
        self.users.append_row(new_account)
