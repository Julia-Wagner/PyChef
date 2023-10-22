from .mixins import ClearConsole, StyleConsole
from .sheet import SheetService
from .user import User
from .recipe import Recipe
from getpass import getpass


class Cookbook(ClearConsole, StyleConsole, SheetService):
    """
    Main Class to interact with the user and call other classes
    """
    console = StyleConsole.style()
    users = SheetService.get_worksheet("users")
    recipes = SheetService.get_worksheet("recipes")

    def __init__(self):
        self.clear_console()
        self.show_welcome_message()

    @classmethod
    def show_welcome_message(cls):
        cls.clear_console()

        cls.console.print("""  __________________   __________________
    .-/| ---------------- \ / ---------------- |\-.
    |||| ---------------- ||| ---------------- ||||
    |||| ---- PyChef ---- ||| ---------------- ||||
    |||| ---------------- ||| ---------------- ||||
    |||| ---------------- ||| ---------------- ||||
    |||| ---------------- ||| ---------------- ||||
    |||| ---------------- ||| ---------------- ||||
    |||| ---------------- ||| ---------------- ||||
    ||||_________________ ||| _________________||||
    ||/===================\|/===================\||
    `--------------------~___~-------------------''\n""", justify="center")

        cls.console.print("Welcome to your digital cookbook!", style="bold white on green", justify="center")

        cls.account_selection()

    @classmethod
    def account_selection(cls):
        cls.console.print("\nSelect an option\n", style="heading")
        cls.console.print("1 Log in to your account", style="option")
        cls.console.print("2 Create an account", style="option")

        # show until correct selection is made
        while True:
            try:
                selection = input("\nEnter 1 or 2: \n")

                if selection == "1":
                    print("login")
                    cls.login()
                    break
                elif selection == "2":
                    print("create")
                    cls.create_account()
                    break
                else:
                    raise ValueError

            except ValueError:
                cls.console.print("Please select either 1 or 2", style="error")

    @classmethod
    def login(cls, new_account = False):
        cls.clear_console()

        if new_account:
            cls.console.print("\nAccount created successfully!\nYou can now log in", style="success")

        # input username until correct
        while True:
            try:
                username = input("\nPlease enter your username: \n")

                if not cls.get_entry("users", username, 2):
                    raise ValueError("Username not found")

            except ValueError as e:
                cls.console.print(f"{e}, please enter the correct username", style="error")
                continue
            else:
                break

        user_row = cls.get_entry("users", username, 2).row
        row_values = cls.get_row_values("users", user_row)

        # input password until correct
        while True:
            try:
                cls.console.print("\nNote: for security reasons your password won´t be displayed while typing", style="info")
                password = getpass("Please enter your password: \n")

                if row_values[2] != password:
                    raise ValueError("Password incorrect")

            except ValueError as e:
                cls.console.print(f"{e}, please enter your password", style="error")
                continue
            else:
                break

        current_user = User.get_user(row_values)
        cls.view_create_selection(current_user)

    @classmethod
    def create_account(cls):
        cls.clear_console()
        cls.console.print("Please enter a username", style="heading")
        cls.console.print("Username must be at least 4 characters long", style="info")

        # input username until valid selection was made
        while True:
            try:
                username = input("\nUsername: \n")

                if len(username) < 4:
                    raise ValueError("Username must be at least 4 characters long")

                if cls.get_entry("users", username, 2):
                    raise ValueError("Username is already taken")

            except ValueError as e:
                cls.console.print(f"{e}, please choose another username", style="error")
                continue
            else:
                break

        cls.console.print("\nPlease enter a password", style="heading")
        cls.console.print("Password must be at least 6 characters long", style="info")

        # input password until valid selection was made
        while True:
            try:
                password = input("\nPassword: \n")

                if len(password) < 6:
                    raise ValueError("Password must be at least 4 characters long")

            except ValueError as e:
                cls.console.print(f"{e}, please choose another password", style="error")
                continue
            else:
                break

        cls.console.print("\nCreating account...", style="info")

        # create account and add it to worksheet in User class
        new_user = User(cls.increment_id("users"), username, password)
        new_user.add_user_to_sheet()

        cls.login(True)

    @classmethod
    def view_create_selection(cls, current_user):
        cls.clear_console()
        cls.console.print("Do you want to view or create a recipe?\n", style="heading")
        cls.console.print("1 View recipe", style="option")
        cls.console.print("2 Create a new recipe", style="option")

        # show until correct selection is made
        while True:
            try:
                selection = input("\nEnter 1 or 2: \n")

                if selection == "1":
                    cls.view_recipe(current_user)
                    break
                elif selection == "2":
                    cls.create_recipe(current_user)
                    break
                else:
                    raise ValueError

            except ValueError:
                cls.console.print("Please select either 1 or 2", style="error")

    @classmethod
    def view_recipe(cls, current_user, recipe = False):
        cls.clear_console()

        if not recipe:
            cls.console.print("What kind of recipe are you looking for?", style="heading")
            recipe_category = cls.choose_category()

        print(current_user.username)

    @classmethod
    def create_recipe(cls, current_user):
        cls.clear_console()

        cls.console.print("Please choose the category of your recipe", style="heading")
        recipe_category = cls.choose_category()
        recipe_name = cls.choose_name()
        recipe_instructions = input("\nPlease enter the instructions for your recipe: \n")

        cls.console.print("\nSaving recipe...", style="info")

        new_recipe = Recipe(cls.increment_id("recipes"), recipe_category, recipe_name, recipe_instructions, current_user.user_id)
        new_recipe.add_recipe_to_sheet()

        cls.view_recipe(current_user, new_recipe)

    @classmethod
    def choose_category(cls):
        cls.console.print("1 Vegetarian :avocado:", style="option")
        cls.console.print("2 Meat :poultry_leg:", style="option")
        cls.console.print("3 Fish :fish:", style="option")

        # input category until valid selection was made
        while True:
            try:
                category = input("\nCategory: \n")

                if category == "1":
                    category = "Vegetarian"
                    break
                elif category == "2":
                    category = "Meat"
                    break
                elif category == "3":
                    category = "Fish"
                    break
                else:
                    raise ValueError

            except ValueError:
                cls.console.print("Please select either 1, 2 or 3", style="error")
                continue

        cls.console.print(f"\nRecipe category: [underline]{category}[underline]", style="success")
        return category

    @classmethod
    def choose_name(cls):
        cls.console.print("\nPlease enter a name for your recipe", style="heading")
        cls.console.print("Name must be between 3 and 15 characters long", style="info")

        # input name until valid selection was made
        while True:
            try:
                recipe_name = input("\nName: \n")

                if len(recipe_name) < 3 or len(recipe_name) > 15:
                    raise ValueError("Name must be between 3 and 15 characters long")

            except ValueError as e:
                cls.console.print(f"{e}, please choose a valid name", style="error")
                continue
            else:
                break

        cls.console.print(f"\nRecipe name: [underline]{recipe_name}[underline]", style="success")
        return recipe_name
