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

    @staticmethod
    def get_worksheet(sheet_name):
        worksheet = SheetService.SHEET.worksheet(sheet_name)
        return worksheet

    @staticmethod
    def increment_id(sheet_name):
        last_id = SheetService.get_worksheet(sheet_name).get_all_values()[-1][0]

        if last_id != "id":
            new_id = int(last_id) + 1
        else:
            new_id = 1
        return new_id
