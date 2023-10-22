from .mixins import ClearConsole, StyleConsole
from .sheet import SheetService


class Recipe(ClearConsole, StyleConsole, SheetService):
    """"
    Class for recipe
    """
    console = StyleConsole.style()
    recipes = SheetService.get_worksheet("recipes")

    def __init__(self, recipe_id, category, name, instructions, created_by_id):
        self.recipe_id = recipe_id
        self.category = category
        self.name = name
        self.instructions = instructions
        self.created_by_id = created_by_id

    def add_recipe_to_sheet(self):
        """
        Adds a new row with the data from the recipe to the worksheet
        """
        new_recipe = [self.recipe_id, self.category, self.name, self.instructions, self.created_by_id]
        self.recipes.append_row(new_recipe)
