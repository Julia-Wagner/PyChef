from .sheet import SheetService


class Recipe(SheetService):
    """"
    Class for recipe
    """

    def __init__(self, recipe_id, category, name, instructions, created_by_id):
        self.recipe_id = recipe_id
        self.category = category
        self.name = name
        self.instructions = instructions
        self.created_by_id = created_by_id

    @classmethod
    def from_dictionary(cls, dictionary):
        """
        Alternative constructor to create a recipe from a dictionary.

        :param dictionary: the dictionary that contains the values
        :return: the created Recipe instance
        """
        recipe_id, category, name, instructions, created_by_id = (
            list(dictionary.values()))
        return cls(recipe_id, category, name, instructions, created_by_id)

    def add_recipe_to_sheet(self):
        """
        Adds a new row with the data from the recipe to the worksheet.
        """
        new_recipe = [self.recipe_id, self.category, self.name,
                      self.instructions, self.created_by_id]
        SheetService.add_entry_to_sheet("recipes", new_recipe)

    def delete_recipe(self):
        """
        Gets the worksheet row where the recipe is saved and deletes it.
        """
        self.console.print("\nDeleting recipe...", style="info")
        recipe_row = self.get_row("recipes", 1, str(self.recipe_id))
        self.delete_entry("recipes", recipe_row)
