import gspread
from google.oauth2.service_account import Credentials
from .mixins import StyleConsole, RestartProgram


class SheetService:
    """
    Class for Google Sheets functions
    """
    console = StyleConsole.style()

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
        Gets the needed worksheet.

        :param string sheet_name: the name of the worksheet
        :return: worksheet to work with
        """
        try:
            worksheet = cls.SHEET.worksheet(sheet_name)
            return worksheet

        except gspread.exceptions.APIError:
            cls.console.print("An error occurred connecting Google Sheets. "
                              "Please restart the program", style="error")
            input("Press Enter to restart...\n")
            RestartProgram.restart()

        except Exception:
            cls.console.print("An error occurred. Please restart the program",
                              style="error")
            input("Press Enter to restart...\n")
            RestartProgram.restart()

    @classmethod
    def increment_id(cls, sheet_name):
        """
        Increments the id for the given worksheet.

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
        Checks if the given value exists in the given column
        of a specific worksheet.
        If yes the cell is returned.

        :param string sheet_name: the name of the worksheet
        :param string value: the value to search for in the worksheet
        :param int column: the column to look in
        :return: False or found entry
        """
        entry = cls.get_worksheet(sheet_name).find(value, in_column=column)
        if entry is None:
            return False
        return entry

    @classmethod
    def get_available_recipes(cls, category, user_id):
        """
        Gets all recipes with the given category
        that where created by the given user.

        :param string category: the category of the recipe to look for
        :param int user_id: the id of the user trying to get the recipes
        :return: False or available recipes
        """
        all_recipes = cls.get_worksheet("recipes").get_all_records()
        available_recipes = [recipe for recipe in all_recipes
                             if recipe['category'] == category and
                             recipe['created_by_id'] == user_id]

        if not available_recipes:
            return False
        return available_recipes

    @classmethod
    def get_ingredients_for_recipes(cls, recipe_id):
        """
        Gets all ingredients for the given recipe.

        :param int recipe_id: the id of the recipe
        :return: False or available ingredients
        """
        all_ingredients = cls.get_worksheet("ingredients").get_all_records()
        recipe_ingredients = [ingredient for ingredient in all_ingredients
                              if ingredient['recipe_id'] == recipe_id]

        if not recipe_ingredients:
            return False
        return recipe_ingredients

    @classmethod
    def get_row(cls, sheet_name, column, entry):
        """
        Gets the row number for the given entry
        
        :param sheet_name:
        :param column:
        :param entry:
        :return:
        """
        row = cls.get_entry(sheet_name, entry, column).row
        return row

    @classmethod
    def get_row_values(cls, sheet_name, row):
        """
        Gets the values of a specific row in the given worksheet.

        :param string sheet_name: the name of the worksheet
        :param int row: the row to look in
        :return: False or found entry
        """
        row_values = cls.get_worksheet(sheet_name).row_values(row)
        if not row_values:
            return False
        return row_values

    @classmethod
    def add_entry_to_sheet(cls, sheet_name, entry):
        """
        Adds a new row with the given data to the given worksheet.

        :param string sheet_name: the name of the worksheet
        :param list entry: the entry to add
        """
        worksheet = cls.get_worksheet(sheet_name)
        worksheet.append_row(entry)

    @classmethod
    def delete_entry(cls, sheet_name, row):
        """
        Delete the entry of the given row.

        :param string sheet_name: the name of the worksheet
        :param int row: the row to delete
        """
        worksheet = cls.get_worksheet(sheet_name)
        worksheet.delete_row(row)
