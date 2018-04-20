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
except:
    CACHE_DICTION = {}

def get_unique_key(url):
  return url

def make_request_using_cache(url):
    unique_ident = get_unique_key(url)

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        # print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        # print("Making a request for new data...")
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

content_div = page_soup.find(id='food_directory_left')
table_rows = content_div.find_all(class_='directory_group')

category_dict = {}
for item in table_rows:
    dt = item.find_all('dt')
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
    food_request = make_request_using_cache(food_url)
    food_soup = BeautifulSoup(food_request, 'html.parser')
    more_button = food_soup.find_all(class_='more')

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

def plotly_data():
    plotly_list = []
    plotly_dict = {}
    i = 1

    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    statement = '''
    SELECT TotalFat, Protein, TotalCarbohydrates
    FROM Nutrition_Facts
    '''
    cur.execute(statement)
    conn.commit()

    for item in cur:
        plotly_dict['fat'] = float(item[0])
        plotly_dict['protein'] = float(item[1])
        plotly_dict['carbs'] = float(item[2])
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

def plot_ternary():
    rawData = plotly_data()

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

def vitamin_stacked_bar():
    lst = stacked_bar_data()
    lst2 = [0.9, 90, 18, 1300, 4700]
    lst3 = []
    i = 0
    for item in lst:
        if lst2[i]-item < 0:
            lst3.append(0)
        else:
            lst3.append(lst2[i]-item)
        i += 1


    trace1 = go.Bar(
    y=['VitaminA(mg)', 'VitaminC(mg)', 'Iron(mg)', 'Calcium(mg)', 'Potassium(mg)'],
    x=lst,
    name='Average Vitamins and Minerals',
    orientation = 'h',
    marker = dict(
        color = 'rgba(158,202,225)',
        line = dict(
            color = 'rgba(8,48,107)',
            width = 3)
            )
    )
    trace2 = go.Bar(
        y=['VitaminA(mg)', 'VitaminC(mg)', 'Iron(mg)', 'Calcium(mg)', 'Potassium(mg)'],
        x=lst3,
        name='Mg Needed to Meet Daily Recommended Value',
        orientation = 'h',
        marker = dict(
            color = 'rgba(58, 71, 80, 0.6)',
            line = dict(
                color = 'rgba(58, 71, 80, 1.0)',
                width = 3)
            )
        )

    data = [trace1, trace2]
    layout = go.Layout(
        barmode='stack'
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='marker-h-bar')

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
    return nut_list

def nutrition_bar_chart():
    lst = get_nutrition_data()
    lst2 = [100,100,100,100,100,100,100,100]
    lst3 = []
    i = 0
    for item in lst:
        if lst2[i]-item < 0:
            lst3.append(0)
        else:
            lst3.append(lst2[i]-item)
        i += 1

    trace1 = go.Bar(
    x=['CaloriesDV', 'TotalFatDV', 'CholesterolDV', 'SodiumDV', 'CarbohydratesDV', 'FiberDV', 'SugarDV', 'ProteinDV'],
    y=lst,
    name='Average Percentage of Daily Recommended Value'
    )
    trace2 = go.Bar(
        x=['CaloriesDV', 'TotalFatDV', 'CholesterolDV', 'SodiumDV', 'CarbohydratesDV', 'FiberDV', 'SugarDV', 'ProteinDV'],
        y=lst3,
        name='Percent Needed to Meet Recommended Daily Value'
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
        cals = round(item[0], 2)
        fat = round(item[1], 2)
        chol = round((item[2]/1000), 2)
        sod = round((item[3]/1000), 2)
        carbs = round(item[4], 2)
        fib = round(item[5], 2)
        sug = round(item[6], 2)
        pro = round(item[7], 2)

    pie_list = [cals, fat, chol, sod, carbs, fib, sug, pro]
    return pie_list

def pie_chart():
    lst1 = get_pie_data()
    lst = lst1[1:]
    labels = ['TotalFat(g)', 'Cholesterol(g)', 'Sodium(g)', 'Carbohydrates(g)', 'Fiber(g)', 'Sugar(g)', 'Protein(g)']
    values = lst

    trace = go.Pie(labels=labels, values=values)

    py.plot([trace], filename='basic_pie_chart')

def make_table():
    list1 = ["Calories (kcal)", "Fat (g)", "Cholesterol (mg)", "Sodium (mg)", "Carbohydrates (g)", "Fiber (g)", "Sugar (g)", "Protein (g)"]
    list2 = ["Vitamin A (IU)", "Vitamin C (mg)", "Iron (mg)", "Calcium (mg)", "Potassium (mg)"]
    list3 = get_pie_data()
    list4 = stacked_bar_data()

    title_list = list1 + list2
    num_list = list3 + list4

    trace = go.Table(
    header=dict(values=['Nutrition Fact', 'Average'],
                line = dict(color='#7D7F80'),
                fill = dict(color='#a1c3d1'),
                align = ['left'] * 5),
    cells=dict(values=[title_list,
                num_list],
               line = dict(color='#7D7F80'),
               fill = dict(color='#EDFAFF'),
               align = ['left'] * 5))

    layout = dict(width=500, height=300)
    data = [trace]
    fig = dict(data=data, layout=layout)
    py.plot(fig, filename = 'styled_table')

def ask_user():
    user_input = ""
    bread = []
    cake = []
    cookies_pastry = []
    pasta_rice = []
    alcohol = []
    butter = []
    candy_agg = []
    salty = []
    fruit = []
    ice = []
    cheese = []
    prompt_choices = """
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
                 """

    graph_choices = """
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

    """

    food_graph = prompt_choices + graph_choices

    while user_input != "exit":
        if user_input == "":
            print(prompt_choices)
            user_input = input("Please choose one of the options above (or 'help' for options): ")
        elif user_input.lower() == "help":
            print(prompt_choices)
            user_input = input("Please choose one of the options above: ")
        elif user_input.lower() == "bread":
            bread = get_food_data("Bread")
            make_database(bread)
            make_table()
            print(graph_choices)
            user_input = input("Please choose a graph above to display the data: ")
        elif user_input.lower() == "cake":
            cake = get_food_data("Cake")
            make_database(cake)
            make_table()
            print(graph_choices)
            user_input = input("Please choose a graph above to display the data: ")
        elif user_input.lower() == "cookies and pastry":
            cookies = get_food_data("Cookies")
            pastry = get_food_data("Pastry")
            for item in cookies:
                cookies_pastry.append(item)
            for p in pastry:
                cookies_pastry.append(p)
            make_database(cookies_pastry)
            make_table()
            print(graph_choices)
            user_input = input("Please choose a graph above to display the data: ")
        elif user_input.lower() == "pasta and rice":
            pasta = get_food_data("Pasta & Noodles")
            rice = get_food_data("Rice")
            for item in pasta:
                pasta_rice.append(item)
            for k in rice:
                pasta_rice.append(k)
            make_database(pasta_rice)
            make_table()
            print(graph_choices)
            user_input = input("Please choose a graph above to display the data: ")
        elif user_input.lower() == "alcohol":
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
            make_table()
            print(graph_choices)
            user_input = input("Please choose a graph above to display the data: ")
        elif user_input.lower() == "candy":
            candy = get_food_data("Candies")
            candy_bars = get_food_data("Candy Bars")
            chocolate = get_food_data("Chocolate Candies")
            for item in candy:
                candy_agg.append(item)
            for k in candy_bars:
                candy_agg.append(k)
            for x in chocolate:
                candy_agg.append(x)
            make_database(candy_agg)
            make_table()
            print(graph_choices)
            user_input = input("Please choose a graph above to display the data: ")
        elif user_input.lower() == "salty snacks":
            chips = get_food_data("Chips")
            popcorn = get_food_data("Popcorn")
            pretzels = get_food_data("Pretzels")
            snacks = get_food_data("Salty Snacks")
            for item in chips:
                salty.append(item)
            for k in popcorn:
                salty.append(k)
            for x in pretzels:
                salty.append(x)
            for s in snacks:
                salty.append(s)
            make_database(salty)
            make_table()
            print(graph_choices)
            user_input = input("Please choose a graph above to display the data: ")
        elif user_input.lower() == "fruit":
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
            make_table()
            print(graph_choices)
            user_input = input("Please choose a graph above to display the data: ")
        elif user_input.lower() == "ice cream":
            custard = get_food_data("Custards")
            ice_cream = get_food_data("Ice Cream & Frozen")
            pudding = get_food_data("Pudding & Gelatin")
            for item in custard:
                ice.append(item)
            for k in ice_cream:
                ice.append(k)
            for x in pudding:
                ice.append(x)
            make_database(ice)
            make_table()
            print(graph_choices)
            user_input = input("Please choose a graph above to display the data: ")
        elif user_input.lower() == "cheese":
            natural = get_food_data("Natural Cheese")
            processed = get_food_data("Processed Cheese")
            for item in natural:
                cheese.append(item)
            for k in processed:
                cheese.append(k)
            make_database(cheese)
            make_table()
            print(graph_choices)
            user_input = input("Please choose a graph above to display the data: ")
        elif user_input.lower() == "ternary":
            try:
                plot_ternary()
                print(food_graph)
                user_input = input("Please choose one of the options above (or 'help' for options): ")
            except:
                print(prompt_choices)
                user_input = input("Please choose one of the options above (or 'help' for options): ")
        elif user_input.lower() == "vitamins":
            try:
                vitamin_stacked_bar()
                print(food_graph)
                user_input = input("Please choose one of the options above (or 'help' for options): ")
            except:
                print(prompt_choices)
                user_input = input("Please choose one of the options above (or 'help' for options): ")
        elif user_input.lower() == "nutrition":
            try:
                nutrition_bar_chart()
                print(food_graph)
                user_input = input("Please choose one of the options above (or 'help' for options): ")
            except:
                print(prompt_choices)
                user_input = input("Please choose one of the options above (or 'help' for options): ")
        elif user_input.lower() == "pie":
            try:
                pie_chart()
                print(food_graph)
                user_input = input("Please choose one of the options above (or 'help' for options): ")
            except:
                print(prompt_choices)
                user_input = input("Please choose one of the options above (or 'help' for options): ")
        else:
            print("Sorry, that is not a valid option")
            print(prompt_choices)
            user_input = input("Please choose one of the options above (or 'help' for options): ")

    print("Bye!")

if __name__ == "__main__":
    ask_user()
