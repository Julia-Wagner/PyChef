# **PyChef**

[Link to live project](https://pychef-6ee49d35b68f.herokuapp.com/)

**PyChef** is a digital cookbook developed as a terminal application. To test the application use the following user data to log in:
- *username*: **Test**
- *password*: **123456**

The test user already contains recipes to view for each category. Of course, you can also create a new user and add your own recipes.

![Recipe Screenshot](docs/screenshots/recipe.png)

## **Planning**

### **Target Audience**

- People who want to save recipes into a digital cookbook.
- People who want to look at different recipes in a digital cookbook.
- People who want to revisit their digital cookbook and look up the recipes they saved.

### **User Stories**

- As a user, I want to create an account and log in.
- As a user, I want to create a digital cookbook with my recipes.
- As a user, I want to save my recipes in different categories.
- As a user, I want to look up my recipes after saving them.
- As a user, I want to clearly see the ingredients and instructions for each recipe.
- As a user, I want to get clear feedback from the application.

- As the site owner, I want to ensure the users have a good experience using the digital cookbook.
- As the site owner, I want to provide the users with helpful feedback.
- As the site owner, I want to be able to differentiate between users and show them the according recipes.

### **Features to achieve the goals**

- Users can create an account with a username and password and log in to their account.
- The application represents a digital cookbook where each user can save multiple recipes.
- Each recipe has to be assigned to a category.
- Users can search for recipes after logging in.
- Each recipe is presented in a nice layout showing the according ingredients and instructions.
- User errors are handled accordingly and clear feedback will be given to the user.

- To ensure a good user experience there will be a well-planned layout, as well as clear feedback to the users.
- Only recipes that belong to the logged-in user are shown for them.

### **Flowchart**

To visualize the necessary steps to create my cookbook, I created a flowchart using [Lucidchart](https://lucid.app/lucidchart/11478dde-0293-49ef-95b3-c7f9f842cd13/edit?viewport_loc=-61%2C227%2C2994%2C1412%2C0_0&invitationId=inv_b097e12e-4e66-440b-bf17-5d18fb3dd66d).

![Flow Chart](docs/screenshots/flowchart.png)

There were some changes to this flowchart during the development of the application. To better visualize them I decided to create a new flowchart showing the actual result instead of adapting the original flowchart.

I decided to let the user add the instructions for a new recipe before the ingredients. This was necessary due to my object-oriented approach as *Recipe* and *Ingredient* are two different classes and I wanted to finish and save the recipe instance before adding ingredients.

Another change is the feature of deleting a recipe I added after finishing the first version of my application. When viewing a recipe, the user can decide whether they want to continue or delete the recipe.

Finally, I removed the **End** step in my flowchart as the application keeps looping as long as the user wants to. It is possible for the user to exit the program at different steps, which always takes them back to the welcome screen (Log in or create user).

![Flow Chart Result](docs/screenshots/flowchart_result.png)

## **Features**

### **Welcome Screen**
On the welcome screen, ASCII Art with a book and the name of the application is displayed. Underneath the welcome message, the user can decide whether they want to log in or create a new account. The input is validated to be either **1** or **2**.

![Welcome Screen](docs/screenshots/welcome_screen.png)

(Note: my screen recorder for some reason changes the color of the ASCII Art, it is all white in the application.)

### **Create Account**
Users have to create an account in order to be able to store and view their personal recipes. A username and password have to be entered. After validation, they are stored in a *Google Sheets* worksheet and the user is redirected to the Login.

The username is validated to have at least 4 characters. Furthermore, the method ensures that the username is not taken. The password has to be at least 6 characters long. The user can enter **exit** instead of the username or password to get back to the welcome screen instead of creating an account.

![Create Account](docs/screenshots/create_account.gif)

### **Login**
A user that already created an account can log in by entering their username and password. The method validates the input by checking if the username exists in the *users* worksheet and if the password that is entered is identical to the one stored.

For security reasons, I used *getpass* to hide the input while typing in the password. The user can enter **exit** instead of the username or password to get back to the welcome screen instead of logging in.

![Login](docs/screenshots/login.gif)

### **Create Recipe**
Users can create recipes. In order to create a recipe they have to be logged in. For each recipe, a category has to be chosen. Then a recipe name and instructions for the recipe have to be entered. There has to be at least one ingredient, but it is possible to add as many ingredients as the user wants to.

The user can enter **exit** instead of the recipe details and ingredients to get back to the welcome screen instead of creating a recipe.

![Create Recipe](docs/screenshots/create_recipe.gif)

### **View Recipe**
To view a recipe the user first has to choose a category. After this, all the available recipes for this category are shown and a recipe to view can be chosen.

To show available recipes, the category selection and the logged-in user are used. Input validation is used to make sure the number of an existing recipe is selected.

After a recipe is selected, the name, instructions and ingredients for this recipe are shown.

![View Recipe](docs/screenshots/view_recipe.gif)

### **Delete Recipe**
A recipe can also be deleted by the user who created it. If this option is chosen, all ingredients and the recipe itself are deleted.

![Delete Recipe](docs/screenshots/delete_recipe.gif)

## **Future Enhancements**
Some features I would like to this application in the future are:

- Connect the project to a real database instead of the worksheets.
- Give the users the possibility to edit a recipe. I thought about adding that but decided not to as it is not necessary for the scope of this project. I do not think I could implement this with a good user experience without having the possibility of clicking and using arrow controls to navigate the information to edit.

## **Classes**

I decided to use object-oriented programming and only use classes and methods in my code. Here is a brief overview of my classes and methods.

- **Cookbook**
  - The main class that interacts with the user and calls other classes.
  - Methods handle user input and call the necessary classes throughout the program.
- **User**
  - attributes: user_id, username, password
  - Creates a user instance when a user logs in or creates an account. User data is stored in and fetched from the worksheet.
- **Recipe**
  - attributes: recipe_id, category, name, instructions, created_by_id
  - Creates a recipe instance when called and has an alternative constructor to create an instance from a dictionary.
  - Stores and deletes recipe data in the worksheet.
- **Ingredient**
  - attributes: ingredient_id, ingredient, recipe_id
  - Creates an ingredient instance when called and has an alternative constructor to create an instance from a dictionary.
  - Stores and deletes ingredient data in the worksheet.

To reduce code repetition and make the code more readable and maintainable I added these classes.

- **Mixins** (ClearConsole, StyleConsole, RestartProgram)
  - **ClearConsole**: Mixin containing a method to easily clear the console.
  - **StyleConsole**: Mixin containing a method that creates a custom theme for the rich package.
  - **RestartProgram**: Mixin containing a method to easily restart the program in case of an error or if the user wants to exit.
- **SheetService**
  - A service class to handle all methods regarding Google Sheets.
  - The connection to the API and error handling regarding this connection is handled here.
  - Contains methods to get, store and delete entries from worksheets.

## **Credits**

### **Content**

- I used the [Python OOP series](https://www.youtube.com/watch?v=ZDa-Z5JzLYM&feature=youtu.be) by Corey Schafer for reference regarding object-oriented programming.
- The [Code Institute Template](https://github.com/Code-Institute-Org/p3-template) was used for this project to have a fake terminal in the browser.
- I used the walkthrough project from Code Institute as a reference on how to connect my project to Google Sheets.
- The method to clear the console is from [DelftStack](https://www.delftstack.com/howto/python/python-clear-console/).

### **Media and Design**

- [Lucidchart](https://lucid.app/lucidchart/11478dde-0293-49ef-95b3-c7f9f842cd13/edit?viewport_loc=807%2C506%2C1664%2C785%2C0_0&invitationId=inv_b097e12e-4e66-440b-bf17-5d18fb3dd66d) was used to create the flowcharts.
- The background image was taken from [Pexels](https://www.pexels.com/photo/assorted-vegetables-on-brown-wooden-table-1414651/).
- The image for the favicon was taken from [Pixabay](https://pixabay.com/de/vectors/sieden-k%C3%BCche-pfanne-topf-1300607/).
- ASCII Art was taken and adapted from the [ASCII Art Archive](https://www.asciiart.eu/books/books).