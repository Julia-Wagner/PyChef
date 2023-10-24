from .sheet import SheetService


class Ingredient(SheetService):
    """"
    Class for ingredient
    """
    ingredients = SheetService.get_worksheet("ingredients")

    def __init__(self, ingredient_id, ingredient, recipe_id):
        self.ingredient_id = ingredient_id
        self.ingredient = ingredient
        self.recipe_id = recipe_id

    def add_ingredient_to_sheet(self):
        """
        Adds a new row with the data from the ingredient to the worksheet.
        """
        new_ingredient = [self.ingredient_id, self.ingredient, self.recipe_id]
        self.ingredients.append_row(new_ingredient)
