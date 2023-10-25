from .mixins import ClearConsole, StyleConsole
from .sheet import SheetService
from .user import User
from .recipe import Recipe
from .ingredient import Ingredient
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
        """
        Shows ASCII Art and a welcome message.
        Calls the next method in the program flow.
        """
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
        """
        Lets the user select whether they want to log in or create an account
        and calls the according method
        """
        cls.console.print("\nSelect an option\n", style="heading")
        cls.console.print("1 Log in to your account", style="option")
        cls.console.print("2 Create an account", style="option")

        # show until correct selection is made
        while True:
            try:
                selection = input("\nEnter 1 or 2: \n").strip()

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
    def login(cls, new_account=False):
        """
        Shows username and password input and checks if they are correct,
        creates a new User object if they are.
        Calls the next method in the program flow.

        :param bool new_account: Show message if this is True, default is False
        """
        cls.clear_console()

        if new_account:
            cls.console.print("Account created successfully!\nYou can now log in\n", style="success")

        # input username until correct
        while True:
            try:
                username = input("Please enter your username: \n").strip()

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
                cls.console.print("\nNote: for security reasons your password won´t be displayed while typing",
                                  style="info")
                password = getpass("Please enter your password: \n").strip()

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
        """
        Shows username and password input and checks if they are valid,
        creates a new User object and stores the data in the worksheet if they are.
        Calls the next method in the program flow.
        """
        cls.clear_console()
        cls.console.print("Please enter a username", style="heading")
        cls.console.print("Username must be at least 4 characters long", style="info")

        # input username until valid selection was made
        while True:
            try:
                username = input("\nUsername: \n").strip()

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
                password = input("\nPassword: \n").strip()

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
        """
        Let the user select whether they want to view or create a recipe
        and calls the according method
        """
        cls.clear_console()
        cls.console.print("Do you want to view or create a recipe?\n", style="heading")
        cls.console.print("1 View recipe", style="option")
        cls.console.print("2 Create a new recipe", style="option")

        # show until correct selection is made
        while True:
            try:
                selection = input("\nEnter 1 or 2: \n").strip()

                if selection == "1":
                    cls.select_recipe(current_user)
                    break
                elif selection == "2":
                    cls.create_recipe(current_user)
                    break
                else:
                    raise ValueError

            except ValueError:
                cls.console.print("Please select either 1 or 2", style="error")

    @classmethod
    def select_recipe(cls, current_user):
        cls.clear_console()

        cls.console.print("What kind of recipe are you looking for?", style="heading")
        recipe_category = cls.choose_category()

        cls.console.print("\nLooking for recipes...", style="info")

        available_recipes = cls.get_available_recipes(recipe_category, current_user.user_id)

        if not available_recipes:
            cls.console.print(f"\nYou did not add any {recipe_category} recipes to your cookbook yet", style="error")
            input("Press Enter to create a recipe...\n")
            cls.create_recipe(current_user)

        cls.clear_console()
        cls.console.print(f"Available {recipe_category} recipes\n", style="heading")

        for number, recipe in enumerate(available_recipes, start=1):
            cls.console.print(f"{number} {recipe['name']}", style="option")

    @classmethod
    def view_recipe(cls, current_user, recipe):
        cls.clear_console()

        print(recipe.name)

    @classmethod
    def create_recipe(cls, current_user):
        """
        Calls according methods to show category, name and instructions input
        and checks if they are valid, creates a new Recipe object and stores the data in the worksheet if they are.
        Calls the next method in the program flow.

        :param User current_user: The user that is currently logged in
        """
        cls.clear_console()

        # let the user choose a category for the recipe
        cls.console.print("Please choose the category of your recipe", style="heading")
        recipe_category = cls.choose_category()

        # let the user choose a name for the recipe
        recipe_name = cls.choose_name()

        # let the user enter instructions for the recipe
        recipe_instructions = input("\nPlease enter the instructions for your recipe: \n").strip()

        while not recipe_instructions:
            cls.console.print("Please enter instructions", style="error")
            recipe_instructions = input("\nPlease enter the instructions for your recipe: \n")

        cls.console.print("\nSaving recipe...", style="info")

        # create a new Recipe instance and save recipe in worksheet
        new_recipe = Recipe(cls.increment_id("recipes"), recipe_category, recipe_name, recipe_instructions,
                            current_user.user_id)
        new_recipe.add_recipe_to_sheet()

        cls.clear_console()

        # let the user enter ingredients for the recipe
        cls.console.print("Please enter the ingredients for your recipe", style="heading")
        cls.console.print("\nEnter one ingredient at the time, you can enter more as long as you want to", style="info")
        more = True
        while more:
            ingredient = input("\nIngredient: \n").strip()

            while not ingredient:
                cls.console.print("Please enter an ingredient", style="error")
                ingredient = input("\nIngredient: \n").strip()

            cls.console.print("\nSaving ingredient...", style="info")

            # create a new Ingredient instance
            new_ingredient = Ingredient(cls.increment_id("ingredients"), ingredient, new_recipe.recipe_id)
            new_ingredient.add_ingredient_to_sheet()

            while True:
                enter_more = input("Do you want to add another ingredient? (y/n)\n").lower().strip()

                if enter_more == "y":
                    more = True
                    break
                elif enter_more == "n":
                    more = False
                    break
                else:
                    cls.console.print("Please enter either y or n", style="error")

        cls.view_recipe(current_user, new_recipe)

    @classmethod
    def choose_category(cls):
        """
        Shows category input and checks if valid.

        :return: selected category
        """
        cls.console.print("1 Vegetarian :avocado:", style="option")
        cls.console.print("2 Meat :poultry_leg:", style="option")
        cls.console.print("3 Fish :fish:", style="option")

        # input category until valid selection was made
        while True:
            try:
                category = input("\nCategory: \n").strip()

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

        cls.clear_console()
        cls.console.print(f"Recipe category: [underline]{category}[underline]", style="success")
        return category

    @classmethod
    def choose_name(cls):
        """
        Shows name input and checks if valid.

        :return: selected name
        """
        cls.console.print("\nPlease enter a name for your recipe", style="heading")
        cls.console.print("Name must be between 3 and 15 characters long", style="info")

        # input name until valid selection was made
        while True:
            try:
                recipe_name = input("\nName: \n").strip()

                if len(recipe_name) < 3 or len(recipe_name) > 15:
                    raise ValueError("Name must be between 3 and 15 characters long")

            except ValueError as e:
                cls.console.print(f"{e}, please choose a valid name", style="error")
                continue
            else:
                break

        cls.clear_console()
        cls.console.print(f"Recipe name: [underline]{recipe_name}[underline]", style="success")
        return recipe_name
