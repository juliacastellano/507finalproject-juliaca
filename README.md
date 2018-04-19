Data sources used, including instructions for a user to access the data sources
(e.g., API keys or client secrets needed, along with a pointer to instructions on
how to obtain these and instructions for how to incorporate them into your program (e.g., secrets.py file format))
  - I used http://calorielab.com/index.html, there are no API keys or client secrets needed
  to run the program.

Any other information needed to run the program (e.g., pointer to getting started info for plotly)
  - N/A

Brief description of how your code is structured, including the names of significant data processing functions
(just the 2-3 most important functions--not a complete list) and class definitions. If there are large data structures (e.g., lists, dictionaries) that you create to organize your data for presentation, briefly describe them.
  - get_food_data() is a function that gets the nutrition information for each food in a category and makes a
    Food object using this data. It then puts these Food instances into a list that is used to make the database.
  - plotly_data(), stacked_bar_data(), get_nutrition_data(), and get_pie_data() grab data from the database in order
    to make the different plotly graphs.
  - The Food class holds all of the nutrition information for each food and is used to make the database.

Brief user guide, including how to run the program and how to choose presentation options.
  - To run this program, please start by choosing a food category. This will populate the database and open a plotly table
    so that you can see the averages for the different nutrition facts. Then you can either choose one of four graph options
    to see the data visualized in plotly or choose a different food category. You can type "help" to see the options and "exit" to exit the program at any time. The different food category and graph options can be seen below:

    Food Choices:
            bread
            cake
            cookies and pastry
            pasta and rice
            cheese
            fruit
                (includes apples, apricots, berries, citrus, grapes, melons,
                peaches, pears, plums, tropical)
            candy
            salty snacks
                (includes popcorn, pretzels, chips)
            ice cream
                (includes ice cream, custard, pudding)
            alcohol
                (includes beer, spirits, cocktails, and wine)
        ----------------------------------------------------------------------------
    Graph Choices:
            ternary
                graph of fat, protein, and carbs as three points of triangle for
                each food within the category
            vitamins
                bar graph of the average vitamins and minerals for the food category
                compared to the daily recommended values
            nutrition
                bar graph of the average percent daily values of general nutrition
                facts compared to the daily recommended values for the food category
            pie
                pie chart of the averages of the general nutrition facts for the
                food category
