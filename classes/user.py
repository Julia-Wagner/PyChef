from .sheet import SheetService


class User(SheetService):
    """"
    Class for user
    """

    def __init__(self, user_id, username, password):
        self.user_id = user_id
        self.username = username
        self.password = password

    @classmethod
    def from_list(cls, user_list):
        """
        Alternative constructor to create a user from a list.

        :param list user_list: the list that contains the values
        :return: the created User instance
        """
        user_id, username, password = user_list
        return cls(int(user_id), username, password)

    def add_user_to_sheet(self):
        """
        Adds a new row with the data from the user to the worksheet.
        """
        new_account = [self.user_id, self.username, self.password]
        SheetService.add_entry_to_sheet("users", new_account)
