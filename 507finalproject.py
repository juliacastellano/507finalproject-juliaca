import requests
import json
import sys
import ssl
import sqlite3
from bs4 import BeautifulSoup
import plotly.plotly as py
import plotly.graph_objs as go

CACHE_FNAME = 'final_project_cache.json'
db_name = 'final_project_db.sqlite'

try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}

def get_unique_key(url):
  return url

def make_request_using_cache(url):
    unique_ident = get_unique_key(url)

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(url)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]


baseurl = 'http://calorielab.com'
index_end = '/index.html'

page_request = make_request_using_cache(baseurl + index_end)
page_soup = BeautifulSoup(page_request, 'html.parser')
# print(page_soup)

content_div = page_soup.find(id='food_directory_left')
table_rows = content_div.find_all(class_='directory_group')


category_dict = {}
for item in table_rows:
	# print(item.text)
    dt = item.find_all('dt')
    # for k in dt:
    #     print(k.text)

    dd = item.find_all('dd')
    for x in dd:
        x_text = x.text.strip(' |')
        url_end = x.find('a')['href']
        category_url = baseurl + url_end
        category_dict[x_text]= category_url


class Food():
    def __init__(self, f_url):
        self.f_url = f_url

        self.calories_title = "Calories"
        self.calories = 0
        self.calories_dv = 0

        self.fat_title = "Total Fat"
        self.fat = 0
        self.fat_dv = 0

        self.cholesterol_title = "Cholesterol"
        self.cholesterol = 0
        self.cholesterol_dv = 0

        self.sodium_title = "Sodium"
        self.sodium = 0
        self.sodium_dv = 0

        self.carbs_title = "Total Carbohydrates"
        self.carbs = 0
        self.carbs_dv = 0

        self.fiber_title = "Fiber"
        self.fiber = 0
        self.fiber_dv = 0

        self.sugar_title = "Sugar"
        self.sugar = 0
        self.sugar_dv = 0

        self.protein_title = "Protein"
        self.protein = 0
        self.protein_dv = 0

        self.vita_title = "Vitamin A"
        self.vita = 0
        self.vita_dv = 0

        self.vitc_title = "Vitamin C"
        self.vitc = 0
        self.vitc_dv = 0

        self.calcium_title = "Calcium"
        self.calcium = 0
        self.calcium_dv = 0

        self.potassium_title = "Potassium"
        self.potassium = 0
        self.potassium_dv = 0

        self.iron_title = "Iron"
        self.iron = 0
        self.iron_dv = 0


        individual_food_request = make_request_using_cache(f_url)
        individual_food_soup = BeautifulSoup(individual_food_request, 'html.parser')
        item_details = individual_food_soup.find_all(class_='item')
        food_name = individual_food_soup.find(id='results_heading')
        item = food_name.find(class_='item')
        serving = food_name.find(class_ = 'heading_serving')
        fn = item.find_all(class_='fn')

        for item in fn:
            self.name = item.text

        for item in serving:
            self.name += " (" + item + ")"

        for k in item_details:
            facts_split = k.text.split("\n")
            del(facts_split[0])
            del(facts_split[-1])
            # print(facts_split)

            if facts_split[0] == "Calories (%DV based on daily intake of 2,000 kcal)":
                if facts_split[1].strip('kcal') != "NA":
                    self.calories = facts_split[1].strip('kcal')
                if facts_split[2].strip('%') != "NA":
                    self.calories_dv = facts_split[2].strip('%')
            if facts_split[0] == "Total Fat (DRI 65 g)":
                if facts_split[1].strip('g') != "NA":
                    self.fat = facts_split[1].strip('g')
                if facts_split[2].strip('%') != "NA":
                    self.fat_dv = facts_split[2].strip('%')
            if facts_split[0] == "Cholesterol (DRI 300 mg)":
                if facts_split[1].strip('mg') != "NA":
                    self.cholesterol = facts_split[1].strip('mg')
                if facts_split[2].strip('%') != "NA":
                    self.cholesterol_dv = facts_split[2].strip('%')
            if facts_split[0] == "Sodium (DRI 2,400 mg)":
                if facts_split[1].strip('mg') != "NA":
                    self.sodium = facts_split[1].strip('mg')
                if facts_split[2].strip('%') != "NA":
                    self.sodium_dv = facts_split[2].strip('%')
            if facts_split[0] == "Total Carbohydrate (DRI 300 g)":
                if facts_split[1].strip('g') != "NA":
                    self.carbs = facts_split[1].strip('g')
                if facts_split[2].strip('%') != "NA":
                    self.carbs_dv = facts_split[2].strip('%')
            if facts_split[0] == "Dietary Fiber (DRI 25 g)":
                if facts_split[1].strip('g') != "NA":
                    self.fiber = facts_split[1].strip('g')
                if facts_split[2].strip('%') != "NA":
                    self.fiber_dv = facts_split[2].strip('%')
            if facts_split[0] == "Sugars (WHO recommended maximum daily intake 25 g)":
                if facts_split[1].strip('g') != "NA":
                    self.sugar = facts_split[1].strip('g')
                if facts_split[2].strip('%') != "NA":
                    self.sugar_dv = facts_split[2].strip('%')
            if facts_split[0] == "Protein (DRI 50 g)":
                if facts_split[1].strip('g') != "NA":
                    self.protein = facts_split[1].strip('g')
                if facts_split[2].strip('%') != "NA":
                    self.protein_dv = facts_split[2].strip('%')
            if facts_split[0] == "Vitamin A (DRI 5000 IU)":
                if facts_split[1].strip('IU') != "NA":
                    self.vita = facts_split[1].strip('IU')
                if facts_split[2].strip('%') != "NA":
                    self.vita_dv = facts_split[2].strip('%')
            if facts_split[0] == "Vitamin C (DRI 60 mg)":
                if facts_split[1].strip('mg') != "NA":
                    self.vitc = facts_split[1].strip('mg')
                if facts_split[2].strip('%') != "NA":
                    self.vitc_dv = facts_split[2].strip('%')
            if facts_split[0] == "Calcium (DRI 1000 mg)":
                if facts_split[1].strip('mg') != "NA":
                    self.calcium = facts_split[1].strip('mg')
                if facts_split[2].strip('%') != "NA":
                    self.calcium_dv = facts_split[2].strip('%')
            if facts_split[0] == "Potassium (DRI 3500)":
                if facts_split[1].strip('mg') != "NA":
                    self.potassium = facts_split[1].strip('mg')
                if facts_split[2].strip('%') != "NA":
                    self.potassium_dv = facts_split[2].strip('%')
            if facts_split[0] == "Iron (DRI 18 mg)":
                if facts_split[1].strip('mg') != "NA":
                    self.iron = facts_split[1].strip('mg')
                if facts_split[2].strip('%') != "NA":
                    self.iron_dv = facts_split[2].strip('%')



def get_food_data(food_name):
    food_class_list = []
    food_url = category_dict[food_name]
    # print(food_url)
    food_request = make_request_using_cache(food_url)
    food_soup = BeautifulSoup(food_request, 'html.parser')
    # print(food_soup)
    more_button = food_soup.find_all(class_='more')
    # print(more_button)
    for item in more_button:
        food_href = item.find('a')['href']
        individual_food_url = baseurl + food_href
        food_class_list.append(Food(individual_food_url))

    return food_class_list

def make_database(list_food):
    food_class_list = list_food
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    statement = '''
        DROP TABLE IF EXISTS 'Nutrition_Facts';
    '''
    cur.execute(statement)
    conn.commit()

    statement = '''
        CREATE TABLE 'Nutrition_Facts'(
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'Name' TEXT,
        'Calories' INTEGER,
        'CaloriesDV' INTEGER,
        'TotalFat' INTEGER,
        'TotalFatDV' INTEGER,
        'Cholesterol' INTEGER,
        'CholesterolDV' INTEGER,
        'Sodium' INTEGER,
        'SodiumDV' INTEGER,
        'TotalCarbohydrates' INTEGER,
        'TotalCarbohydratesDV' INTEGER,
        'Fiber' INTEGER,
        'FiberDV' INTEGER,
        'Sugar' INTEGER,
        'SugarDV' INTEGER,
        'Protein' INTEGER,
        'ProteinDV' INTEGER
        );
        '''
    cur.execute(statement)
    conn.commit()


    statement = '''
        DROP TABLE IF EXISTS 'Vitamins_and_Minerals';
    '''
    cur.execute(statement)
    conn.commit()

    statement = '''
        CREATE TABLE 'Vitamins_and_Minerals'(
        'Name' TEXT,
        'FoodId' INTEGER,
        'Calories' INTEGER,
        'VitaminA' INTEGER,
        'VitaminADV' INTEGER,
        'VitaminC' INTEGER,
        'VitaminCDV' INTEGER,
        'Calcium' INTEGER,
        'CalciumDV' INTEGER,
        'Potassium' INTEGER,
        'PotassiumDV' INTEGER,
        'Iron' INTEGER,
        'IronDV' INTEGER,
        FOREIGN KEY ('FoodId') REFERENCES 'Nutrition_Facts'('Id')
        FOREIGN KEY ('Calories') REFERENCES 'Nutrition_Facts'('Calories')
        );
        '''
    cur.execute(statement)
    conn.commit()

    for item in food_class_list:
        insertion = (None,item.name,item.calories,item.calories_dv,item.fat,item.fat_dv,
                    item.cholesterol,item.cholesterol_dv,item.sodium,item.sodium_dv,
                    item.carbs,item.carbs_dv,item.fiber,item.fiber_dv,item.sugar,
                    item.sugar_dv,item.protein,item.protein_dv)
        statement = 'INSERT INTO "Nutrition_Facts" '
        statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        cur.execute(statement, insertion)
        conn.commit()

        insertion = (item.name, None, None, item.vita,item.vita_dv,item.vitc,item.vitc_dv,
                    item.calcium,item.calcium_dv,item.potassium,item.potassium_dv,
                    item.iron,item.iron_dv)
        statement = 'INSERT INTO "Vitamins_and_Minerals" '
        statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        cur.execute(statement, insertion)
        conn.commit()

        statement = '''
        UPDATE Vitamins_and_Minerals
        SET FoodId = (
        SELECT Nutrition_Facts.Id
        FROM Nutrition_Facts
        WHERE Nutrition_Facts.Name = Vitamins_and_Minerals.Name
        )
        '''
        cur.execute(statement)
        conn.commit()

        statement = '''
        UPDATE Vitamins_and_Minerals
        SET Calories = (
        SELECT Nutrition_Facts.Calories
        FROM Nutrition_Facts
        WHERE Nutrition_Facts.Name = Vitamins_and_Minerals.Name
        )
        '''
        cur.execute(statement)
        conn.commit()

    conn.close()

def plotly_data(lst):
    plotly_list = []
    plotly_dict = {}
    i = 1

    for item in lst:
        plotly_dict['fat'] = float(item.fat)
        plotly_dict['protein'] = float(item.protein)
        plotly_dict['carbs'] = float(item.carbs)
        point_i = "point " + str(i)
        plotly_dict['label'] = point_i
        plotly_list.append(plotly_dict)
        i += 1
        plotly_dict = {}

    return plotly_list

def makeAxis(title, tickangle):
    return {
      'title': title,
      'titlefont': { 'size': 20 },
      'tickangle': tickangle,
      'tickfont': { 'size': 15 },
      'tickcolor': 'rgba(0,0,0,0)',
      'ticklen': 5,
      'showline': True,
      'showgrid': True
    }

def plot_ternary(lst):
    rawData = plotly_data(lst)

    data = [{
        'type': 'scatterternary',
        'mode': 'markers',
        'a': [i for i in map(lambda x: x['fat'], rawData)],
        'b': [i for i in map(lambda x: x['protein'], rawData)],
        'c': [i for i in map(lambda x: x['carbs'], rawData)],
        'text': [i for i in map(lambda x: x['label'], rawData)],
        'marker': {
            'symbol': 100,
            'color': '#DB7365',
            'size': 14,
            'line': { 'width': 2 }
        },
        }]

    layout = {
        'ternary': {
            'sum': 100,
            'aaxis': makeAxis('Fat', 0),
            'baxis': makeAxis('<br>Protein', 45),
            'caxis': makeAxis('<br>Carbs', -45)
        },
        'annotations': [{
          'showarrow': False,
          'text': 'Simple Ternary Plot with Markers',
            'x': 0.5,
            'y': 1.3,
            'font': { 'size': 15 }
        }]
    }

    fig = {'data': data, 'layout': layout}
    py.plot(fig, validate=False)


def stacked_bar_data():
    vit_list = []
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    statement = '''
    SELECT AVG(VitaminA), AVG(VitaminC), AVG(Calcium), AVG(Potassium), AVG(Iron)
    FROM Vitamins_and_Minerals
    '''
    cur.execute(statement)
    conn.commit()

    for item in cur:
        vita = round(item[0]/1000,2)
        vitc = round(item[1], 2)
        calc = round(item[2], 2)
        pot = round(item[3], 2)
        iron = round(item[4], 2)

    vit_list = [vita, vitc, iron, calc, pot]

    return vit_list

stacked_bar_data()
def make_stacked_bar():
    lst = stacked_bar_data()

    trace1 = go.Bar(
        x=['VitaminA(mg)', 'VitaminC(mg)', 'Iron(mg)', 'Calcium(mg)', 'Potassium(mg)'],
        y=lst,
        name='Vitamins and Minerals'
    )
    trace2 = go.Bar(
        x=['VitaminA(mg)', 'VitaminC(mg)', 'Iron(mg)', 'Calcium(mg)', 'Potassium(mg)'],
        y=[0.9, 90, 18, 1300, 4700],
        name='Recommended Daily Value of Vitamins and Minerals'
    )

    data = [trace1, trace2]
    layout = go.Layout(
        barmode='stack'
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='stacked-bar')

    # x = ['VitaminA(mg)', 'VitaminC(mg)', 'Iron(mg)']
    # y = lst
    # y2 = [0.9, 90, 18]
    #
    # trace1 = go.Bar(
    #     x=x,
    #     y=y,
    #     text=y,
    #     textposition = 'auto',
    #     marker=dict(
    #         color='rgb(158,202,225)',
    #         line=dict(
    #             color='rgb(8,48,107)',
    #             width=1.5),
    #         ),
    #     opacity=0.6
    # )
    #
    # trace2 = go.Bar(
    #     x=x,
    #     y=y2,
    #     text=y2,
    #     textposition = 'auto',
    #     marker=dict(
    #         color='rgb(58,200,225)',
    #         line=dict(
    #             color='rgb(8,48,107)',
    #             width=1.5),
    #         ),
    #     opacity=0.6
    # )
    #
    # data = [trace1,trace2]
    #
    # py.plot(data, filename='grouped-bar-direct-labels')

def get_nutrition_data():
    nut_list = []
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    statement = '''
    SELECT AVG(CaloriesDV), AVG(TotalFatDV), AVG(CholesterolDV), AVG(SodiumDV),
            AVG(TotalCarbohydratesDV), AVG(FiberDV), AVG(SugarDV), AVG(ProteinDV)
    FROM Nutrition_Facts
    '''
    cur.execute(statement)
    conn.commit()

    for item in cur:
        cals = round(item[0],2)
        fat = round(item[1], 2)
        chol = round(item[2], 2)
        sod = round(item[3], 2)
        carbs = round(item[4], 2)
        fib = round(item[5], 2)
        sug = round(item[6], 2)
        pro = round(item[7], 2)

    nut_list = [cals, fat, chol, sod, carbs, fib, sug, pro]
    print(nut_list)
    return nut_list

# get_nutrition_data()

def nutrition_bar_chart():
    lst = get_nutrition_data()

    trace1 = go.Bar(
    x=['CaloriesDV', 'TotalFatDV', 'CholesterolDV', 'SodiumDV', 'CarbohydratesDV', 'FiberDV', 'SugarDV', 'ProteinDV'],
    y=lst,
    name='Nutrition Fact Percentage of Daily Recommended Value'
    )
    trace2 = go.Bar(
        x=['CaloriesDV', 'TotalFatDV', 'CholesterolDV', 'SodiumDV', 'CarbohydratesDV', 'FiberDV', 'SugarDV', 'ProteinDV'],
        y=[100,100,100,100,100,100,100,100],
        name='Daily Recommended Value'
    )

    data = [trace1, trace2]
    layout = go.Layout(
        barmode='stack'
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='stacked-bar')

def get_pie_data():
    pie_list = []
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    statement = '''
    SELECT AVG(Calories), AVG(TotalFat), AVG(Cholesterol), AVG(Sodium),
            AVG(TotalCarbohydrates), AVG(Fiber), AVG(Sugar), AVG(Protein)
    FROM Nutrition_Facts
    '''
    cur.execute(statement)
    conn.commit()

    for item in cur:
        fat = round(item[1], 2)
        chol = round((item[2]/1000), 2)
        sod = round((item[3]/1000), 2)
        carbs = round(item[4], 2)
        fib = round(item[5], 2)
        sug = round(item[6], 2)
        pro = round(item[7], 2)

    pie_list = [fat, chol, sod, carbs, fib, sug, pro]
    # print(pie_list)
    return pie_list

def pie_chart():
    lst = get_pie_data()
    labels = ['TotalFat(g)', 'Cholesterol(g)', 'Sodium(g)', 'Carbohydrates(g)', 'Fiber(g)', 'Sugar(g)', 'Protein(g)']
    values = lst

    trace = go.Pie(labels=labels, values=values)

    py.plot([trace], filename='basic_pie_chart')

def ask_user():
    user_input = ""
    baked = []
    prompt_choices = """
            bread
            cake
            cookies
            pasta and rice
            alcohol
                (includes beer, spirits, cocktails, and wine)
            butter
                (includes butter and margarine)
            cooked fish
            fresh fish
            fruit
                (includes apples, apricots, berries, citrus, grapes, melons,
                peaches, pears, plums, tropical)
            Beef
            Lamb
            Pork
                 """

    while user_input != "exit":
        bread = []
        cake = []
        cookies = []
        pasta_rice = []
        alcohol = []
        butter = []
        cooked_fish = []
        fresh_fish = []
        fruit = []
        beef = []
        lamb = []
        pork = []

        if user_input == "":
            print(prompt_choices)
            user_input = input("Please choose one of the options above (or 'help' for options): ")
        elif user_input == "help":
            print(prompt_choices)
            user_input = input("Please choose one of the options above: ")
        elif user_input == "bread":
            bread = get_food_data("Bread")
            make_database(bread)
            user_input = input("Please choose one of the options above (or 'help' for options): ")
        elif user_input == "cake":
            cake = get_food_data("Cake")
            make_database(cake)
            user_input = input("Please choose one of the options above (or 'help' for options): ")
        elif user_input == "cookies":
            cookies = get_food_data("Cookies")
            make_database(cookies)
            user_input = input("Please choose one of the options above (or 'help' for options): ")
        elif user_input == "pasta and rice":
            pasta = get_food_data("Pasta & Noodles")
            rice = get_food_data("Rice")
            for item in pasta:
                pasta_rice.append(item)
            for k in rice:
                pasta_rice.append(k)
            make_database(pasta_rice)
            user_input = input("Please choose one of the options above (or 'help' for options): ")
        elif user_input == "alcohol":
            beer = get_food_data("Beer")
            spirits = get_food_data("Spirits & Cocktails")
            wine = get_food_data("Wine")
            for item in beer:
                alcohol.append(item)
            for k in spirits:
                alcohol.append(k)
            for x in wine:
                alcohol.append(x)
            make_database(alcohol)
            user_input = input("Please choose one of the options above (or 'help' for options): ")
        elif user_input == "butter":
            butter = get_food_data("Butter & Margarine")
            make_database(butter)
            user_input = input("Please choose one of the options above (or 'help' for options): ")
        elif user_input == "cooked fish":
            cooked_fish = get_food_data("Cooked Finfish")
            make_database(cooked_fish)
            user_input = input("Please choose one of the options above (or 'help' for options): ")
        elif user_input == "cooked fish":
            fresh_fish = get_food_data("Fresh Finfish")
            make_database(fresh_fish)
            user_input = input("Please choose one of the options above (or 'help' for options): ")
        elif user_input == "fruit":
            apples = get_food_data("Apples")
            apricots = get_food_data("Apricots")
            berries = get_food_data("Berries")
            citrus = get_food_data("Citrus")
            grapes = get_food_data("Grapes")
            melon = get_food_data("Melons")
            peaches = get_food_data("Peaches")
            pears = get_food_data("Pears")
            plums = get_food_data("Plums")
            tropical = get_food_data("Tropical")
            for a in apples:
                fruit.append(a)
            for k in apricots:
                fruit.append(k)
            for b in berries:
                fruit.append(b)
            for c in citrus:
                fruit.append(c)
            for g in grapes:
                fruit.append(g)
            for m in melon:
                fruit.append(m)
            for p in peaches:
                fruit.append(p)
            for z in pears:
                fruit.append(z)
            for y in plums:
                fruit.append(y)
            for t in tropical:
                fruit.append(t)
            make_database(fruit)
            user_input = input("Please choose one of the options above (or 'help' for options): ")
        elif user_input == "beef":
            beef = get_food_data("Beef")
            make_database(beef)
            user_input = input("Please choose one of the options above (or 'help' for options): ")
        elif user_input == "lamb":
            lamb = get_food_data("Lamb")
            make_database(lamb)
            user_input = input("Please choose one of the options above (or 'help' for options): ")
        elif user_input == "pork":
            pork = get_food_data("Pork")
            make_database(pork)
            user_input = input("Please choose one of the options above (or 'help' for options): ")
        else:
            print("Sorry, that is not a valid option")
            user_input = input("Please choose one of the options above (or 'help' for options): ")

    print("Bye!")

# ask_user()

# bread = get_food_data("Bread")
# plot_ternary(bread)
