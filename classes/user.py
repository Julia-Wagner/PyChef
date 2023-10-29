from .sheet import SheetService


class User(SheetService):
    """"
    Class for user
    """

    def __init__(self, user_id, username, password):
        self.user_id = user_id
        self.username = username
        self.password = password

    def add_user_to_sheet(self):
        """
        Adds a new row with the data from the user to the worksheet.
        """
        new_account = [self.user_id, self.username, self.password]
        SheetService.add_entry_to_sheet("users", new_account)

    @staticmethod
    def get_user(values):
        """
        Creates an instance of User and returns it.

        :param list values: the worksheet row with the users data
        :return: the user
        """
        user = User(int(values[0]), values[1], values[2])
        return user
