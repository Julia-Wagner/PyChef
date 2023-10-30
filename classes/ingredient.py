from .sheet import SheetService


class Ingredient(SheetService):
    """"
    Class for ingredient
    """

    def __init__(self, ingredient_id, ingredient, recipe_id):
        self.ingredient_id = ingredient_id
        self.ingredient = ingredient
        self.recipe_id = recipe_id

    def add_ingredient_to_sheet(self):
        """
        Adds a new row with the data from the ingredient to the worksheet.
        """
        new_ingredient = [self.ingredient_id, self.ingredient, self.recipe_id]
        SheetService.add_entry_to_sheet("ingredients", new_ingredient)

    def delete_ingredient(self):
        """
        Get the worksheet row where the ingredient is saved and delete it.
        """
        self.console.print("\nDeleting ingredient...", style="info")
        ingredient_row = self.get_row("ingredients", 1, str(self.ingredient_id))
        self.delete_entry("ingredients", ingredient_row)
