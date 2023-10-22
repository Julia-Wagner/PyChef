import gspread
from google.oauth2.service_account import Credentials


class SheetService:
    """
    Class for Google Sheets functions
    """

    SCOPE = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
    ]

    CREDS = Credentials.from_service_account_file("creds.json")
    SCOPED_CREDS = CREDS.with_scopes(SCOPE)
    GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
    SHEET = GSPREAD_CLIENT.open("PyChef")

    @classmethod
    def get_worksheet(cls, sheet_name):
        """
        Get the needed worksheet
        :param string sheet_name: the name of the worksheet
        :return: worksheet to work with
        """
        worksheet = cls.SHEET.worksheet(sheet_name)
        return worksheet

    @classmethod
    def increment_id(cls, sheet_name):
        """
        Increment the id for the given worksheet
        :param string sheet_name: the name of the worksheet
        :return: incremented id
        """
        last_id = cls.get_worksheet(sheet_name).get_all_values()[-1][0]

        if last_id != "id":
            new_id = int(last_id) + 1
        else:
            new_id = 1
        return new_id

    @classmethod
    def get_entry(cls, sheet_name, value, column):
        """
        Check if the given value exists in the given column of a specific worksheet
        :param string sheet_name: the name of the worksheet
        :param string value: the value to search for in the worksheet
        :param int column: the column to look in
        :return: False or found entry
        """
        entry = cls.get_worksheet(sheet_name).find(value, in_column=column)
        if entry is None:
            return False
        return entry
