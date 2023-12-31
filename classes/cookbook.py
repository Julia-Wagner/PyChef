from getpass import getpass
from .mixins import ClearConsole, StyleConsole
from .sheet import SheetService
from .user import User
from .recipe import Recipe
from .ingredient import Ingredient


class Cookbook(ClearConsole, StyleConsole, SheetService):
    """
    Main Class to interact with the user and call other classes
    """
    console = StyleConsole.style()

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

        # using a raw string to avoid the W605 warning from Flake8
        cls.console.print(r"""  __________________   __________________
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
    `--------------------~___~-------------------''""", justify="center")

        cls.console.print("\nWelcome to your digital cookbook!\n",
                          style="center_heading", justify="center")

        cls.account_selection()

    @classmethod
    def exit_cookbook(cls):
        """
        Shows the input to exit the cookbook
        and calls the method to show the welcome screen.
        """
        input("Press Enter to restart...\n")
        cls.show_welcome_message()

    @classmethod
    def account_selection(cls):
        """
        Lets the user select whether they want to log in or create an account
        and calls the according method.
        """
        cls.console.print("\nSelect an option\n", style="heading")
        cls.console.print("1 Log in to your account", style="option")
        cls.console.print("2 Create an account", style="option")

        # show until correct selection is made
        while True:
            try:
                selection = input("\nEnter 1 or 2: \n").strip()

                if selection == "1":
                    cls.login()
                    break
                elif selection == "2":
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

        :param bool new_account: show message True, default is False
        """
        cls.clear_console()
        cls.console.print("Login", style="center_heading", justify="center")
        cls.print_exit_info()

        if new_account:
            cls.console.print("\nAccount created successfully!\n"
                              "You can now log in", style="success")

        # input username until correct
        while True:
            try:
                username = input(
                    "\nPlease enter your username:\n").lower().strip()

                if username == "exit":
                    cls.exit_cookbook()
                    break

                # check if username exists
                if not cls.get_entry("users", username, 2):
                    raise ValueError("Username not found")

            except ValueError as e:
                cls.console.print(f"{e}, please enter the correct username",
                                  style="error")
                continue
            else:
                break

        # get the users data to ensure the correct password is entered
        user_row = cls.get_row("users", 2, username)
        row_values = cls.get_row_values("users", user_row)

        cls.console.print("\nNote: for security reasons your password "
                          "won´t be displayed while typing", style="info")

        # input password until correct
        while True:
            try:
                # use getpass to hide the input while typing
                password = getpass("Please enter your password: \n").strip()

                if password == "exit":
                    cls.exit_cookbook()
                    break

                if row_values[2] != password:
                    raise ValueError("Password incorrect")

            except ValueError as e:
                cls.console.print(f"{e}, please enter your password",
                                  style="error")
                continue
            else:
                break

        # get the currently logged in user and give it to called methods
        current_user = User.from_list(row_values)
        cls.view_create_selection(current_user)

    @classmethod
    def create_account(cls):
        """
        Shows username and password input and checks if they are valid, creates
        a new User object and stores the data in the worksheet if they are.
        Calls the next method in the program flow.
        """
        cls.clear_console()
        cls.console.print("Create Account", style="center_heading",
                          justify="center")
        cls.print_exit_info()

        cls.console.print("\nPlease enter a username", style="heading")
        cls.console.print("Username must be at least 4 characters long",
                          style="info")

        # input username until valid selection was made
        while True:
            try:
                username = input("\nUsername: \n").lower().strip()

                if username == "exit":
                    cls.exit_cookbook()
                    break

                if len(username) < 4:
                    raise ValueError("Username must be at least 4 "
                                     "characters long")

                # check if username is taken
                if cls.get_entry("users", username, 2):
                    raise ValueError("Username is already taken")

            except ValueError as e:
                cls.console.print(f"{e}, please choose another username",
                                  style="error")
                continue
            else:
                break

        cls.console.print("\nPlease enter a password", style="heading")
        cls.console.print("Password must be at least 6 characters long",
                          style="info")

        # input password until valid selection was made
        while True:
            try:
                password = input("\nPassword: \n").strip()

                if password == "exit":
                    cls.exit_cookbook()
                    break

                if len(password) < 6:
                    raise ValueError("Password must be at least 6 "
                                     "characters long")

            except ValueError as e:
                cls.console.print(f"{e}, please choose another password",
                                  style="error")
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
        Lets the user select whether they want to view or create a recipe
        and calls the according method.

        :param User current_user: the user that is currently logged in
        """
        cls.clear_console()

        cls.console.print("Do you want to view or create a recipe?\n",
                          style="heading")
        cls.console.print("1 View recipe", style="option")
        cls.console.print("2 Create a new recipe", style="option")
        cls.console.print("3 Log out", style="option")

        # show until correct selection is made
        while True:
            try:
                selection = input("\nEnter 1, 2 or 3: \n").strip()

                if selection == "1":
                    cls.select_recipe(current_user)
                    break
                elif selection == "2":
                    cls.create_recipe(current_user)
                    break
                elif selection == "3":
                    cls.exit_cookbook()
                    break
                else:
                    raise ValueError

            except ValueError:
                cls.console.print(
                    "Please select either 1, 2 or 3",
                    style="error")

    @classmethod
    def select_recipe(cls, current_user):
        """
        Calls the method for the category selection to view a recipe.
        Shows available recipes for the selected category,
        handles the selection of a recipe and calls the method to view it.

        :param User current_user: the user that is currently logged in
        """
        cls.clear_console()
        cls.console.print("View recipe", style="center_heading",
                          justify="center")

        cls.console.print("\nWhat kind of recipe are you looking for?",
                          style="heading")

        # select the recipe category to view
        recipe_category = cls.choose_category()

        cls.console.print("\nLooking for recipes...", style="info")

        # get available recipes in the selected category for the current user
        available_recipes = cls.get_available_recipes(recipe_category,
                                                      current_user.user_id)

        # redirect to create_recipe if no recipes are available
        if not available_recipes:
            cls.console.print(f"\nYou did not add any {recipe_category} "
                              "recipes to your cookbook yet", style="error")
            input("Press Enter to create a recipe...\n")
            cls.create_recipe(current_user)

        cls.clear_console()
        cls.console.print("Select a recipe", style="center_heading",
                          justify="center")
        cls.console.print(f"\nAvailable {recipe_category} recipes\n",
                          style="heading")

        # loop through available recipes and show them as an ordered list
        possible_numbers = {}
        for number, recipe in enumerate(available_recipes, start=1):
            possible_numbers[str(number)] = recipe
            cls.console.print(f"{number} {recipe['name']}", style="option")

        # show until correct selection is made
        while True:
            try:
                selection = input("\nEnter the number of the recipe you "
                                  "want to view: \n").strip()

                if possible_numbers.get(selection) is None:
                    raise ValueError
                else:
                    # create and show recipe from valid selection
                    selected_recipe = Recipe.from_dictionary(
                        possible_numbers[selection])
                    cls.view_recipe(current_user, selected_recipe)

            except ValueError:
                cls.console.print(f"Please select a number between "
                                  f"{next(iter(possible_numbers.keys()))} and "
                                  f"{next(reversed(possible_numbers.keys()))}",
                                  style="error")

    @classmethod
    def view_recipe(cls, current_user, recipe):
        """
        Shows all added details for the given recipe.
        Lets the user decide if they want to continue or delete the recipe,
        handles deletion and calls the according method to continue.

        :param User current_user: the user that is currently logged in
        :param Recipe recipe: the recipe to view
        """
        cls.clear_console()
        cls.console.print(f"{recipe.name}", style="center_heading",
                          justify="center")
        cls.console.print(f"\nSelected recipe: "
                          f"[underline]{recipe.name}[/underline]",
                          style="option")
        cls.console.print(f"\nInstructions: {recipe.instructions}",
                          style="option")

        recipe_ingredients = cls.get_ingredients_for_recipes(recipe.recipe_id)

        if recipe_ingredients:
            cls.console.print("\nIngredients:", style="heading")
            for ingredient in recipe_ingredients:
                cls.console.print(f"- {ingredient['ingredient']}",
                                  style="option")

        cls.console.print("\nPlease enter [reverse]c[/reverse] to "
                          "continue or [reverse]delete[/reverse]"
                          " to delete this recipe", style="info")
        # input until valid selection was made
        while True:
            try:
                next_step = (input("Do you want to continue or delete?\n")
                             .strip())

                if next_step == "c":
                    cls.view_create_selection(current_user)
                    break
                elif next_step == "delete":
                    cls.delete_recipe(recipe, recipe_ingredients, current_user)
                    break
                else:
                    raise ValueError

            except ValueError:
                cls.console.print("Please enter either 'c' or 'delete'",
                                  style="error")
                continue

        cls.view_create_selection(current_user)

    @classmethod
    def delete_recipe(cls, recipe, recipe_ingredients, current_user):
        """
        Delete all ingredients and the recipe.

        :param Recipe recipe: the recipe to delete
        :param list recipe_ingredients: the ingredients of the recipe
        :param User current_user: the user that is currently logged in
        """
        while True:
            confirm = (input("Do you want to delete the recipe? (y/n)\n")
                       .lower().strip())

            if confirm == "y":
                # delete all ingredients for this recipe
                if recipe_ingredients:
                    for ingredient in recipe_ingredients:
                        ingredient_instance = Ingredient.from_dictionary(
                            ingredient)
                        ingredient_instance.delete_ingredient()
                # delete the recipe
                recipe.delete_recipe()
                break
            elif confirm == "n":
                cls.view_recipe(current_user, recipe)
                break
            else:
                cls.console.print("Please enter either y or n", style="error")

    @classmethod
    def create_recipe(cls, current_user):
        """
        Calls according methods to show category, name and instructions input
        and checks if they are valid, creates a new Recipe object
        and stores the data in the worksheet if they are.
        Calls the next method in the program flow.

        :param User current_user: the user that is currently logged in
        """
        cls.clear_console()
        cls.console.print("Create a new recipe", style="center_heading",
                          justify="center")
        cls.print_exit_info()

        # let the user choose a category for the recipe
        cls.console.print("\nPlease choose the category of your recipe",
                          style="heading")
        recipe_category = cls.choose_category()

        cls.console.print("Create a new recipe", style="center_heading",
                          justify="center")
        cls.print_exit_info()
        cls.console.print(f"\nRecipe category: "
                          f"[underline]{recipe_category}[/underline]",
                          style="success")

        # let the user choose a name for the recipe
        recipe_name = cls.choose_name()

        # let the user enter instructions for the recipe
        recipe_instructions = cls.choose_instructions()

        cls.console.print("\nSaving recipe...", style="info")

        # create a new Recipe instance and save recipe in worksheet
        new_recipe = Recipe(cls.increment_id("recipes"),
                            recipe_category, recipe_name,
                            recipe_instructions, current_user.user_id)
        new_recipe.add_recipe_to_sheet()

        cls.clear_console()
        cls.console.print("Create a new recipe", style="center_heading",
                          justify="center")
        cls.print_exit_info()

        # let the user enter ingredients for the recipe
        cls.console.print("\nPlease enter the ingredients for your recipe",
                          style="heading")
        cls.console.print("\nEnter one ingredient at the time, "
                          "you can enter more as long as you want to",
                          style="info")
        more = True
        while more:
            ingredient = input("\nIngredient: \n").strip()

            if ingredient == "exit":
                cls.exit_cookbook()

            while not ingredient:
                cls.console.print("Please enter an ingredient", style="error")
                ingredient = input("\nIngredient: \n").strip()

            cls.console.print("\nSaving ingredient...", style="info")

            # create a new Ingredient instance
            new_ingredient = Ingredient(cls.increment_id("ingredients"),
                                        ingredient, new_recipe.recipe_id)
            new_ingredient.add_ingredient_to_sheet()

            while True:
                enter_more = input("Do you want to add another ingredient? "
                                   "(y/n)\n").lower().strip()

                if enter_more == "exit":
                    cls.exit_cookbook()
                    break
                elif enter_more == "y":
                    more = True
                    break
                elif enter_more == "n":
                    more = False
                    break
                else:
                    cls.console.print("Please enter either y or n",
                                      style="error")

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

                if category == "exit":
                    cls.exit_cookbook()
                    break
                elif category == "1":
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
                cls.console.print("Please select either 1, 2 or 3",
                                  style="error")
                continue

        cls.clear_console()

        return category

    @classmethod
    def choose_name(cls):
        """
        Shows name input and checks if valid.

        :return: selected name
        """
        cls.console.print("\nPlease enter a name for your recipe",
                          style="heading")
        cls.console.print("Name must be between 3 and 35 characters long",
                          style="info")

        # input name until valid selection was made
        while True:
            try:
                recipe_name = input("\nName: \n").strip()

                if recipe_name == "exit":
                    cls.exit_cookbook()
                    break

                if len(recipe_name) < 3 or len(recipe_name) > 35:
                    raise ValueError("Name must be between 3 and 35 "
                                     "characters long")

            except ValueError as e:
                cls.console.print(f"{e}, please choose a valid name",
                                  style="error")
                continue
            else:
                break

        cls.clear_console()
        cls.console.print("Create a new recipe", style="center_heading",
                          justify="center")
        cls.print_exit_info()
        cls.console.print(f"\nRecipe name: "
                          f"[underline]{recipe_name}[/underline]",
                          style="success")

        return recipe_name

    @classmethod
    def choose_instructions(cls):
        """
        Shows instructions input and checks if valid.

        :return: selected instructions
        """
        recipe_instructions = input("\nPlease enter the instructions "
                                    "for your recipe: \n").strip()

        if recipe_instructions == "exit":
            cls.exit_cookbook()

        while not recipe_instructions:
            cls.console.print("Please enter instructions", style="error")
            recipe_instructions = input("\nPlease enter the instructions "
                                        "for your recipe: \n")

        return recipe_instructions

    @classmethod
    def print_exit_info(cls):
        """
        Prints the information 'To exit the cookbook simply enter exit'
        """
        cls.console.print("To exit the cookbook simply enter "
                          "[underline]exit[/underline]", style="info")
