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

    def add_user_to_sheet(self):
        """
        Adds a new row with the data from the user to the worksheet.
        """
        new_account = [self.user_id, self.username, self.password]
        self.users.append_row(new_account)

    @staticmethod
    def get_user(values):
        """
        Creates an instance of User and returns it.

        :param list values: the worksheet row with the users data
        :return: the user
        """
        user = User(int(values[0]), values[1], values[2])
        return user
