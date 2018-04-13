import requests
import json
import sys
import ssl
import secrets
import sqlite3
from bs4 import BeautifulSoup
import plotly.plotly as py
import csv

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
        'FoodId' INTEGER,
        FOREIGN KEY ('FoodId') REFERENCES 'Nutrition_Facts'('Id')
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

        insertion = (item.name,item.vita,item.vita_dv,item.vitc,item.vitc_dv,
                    item.calcium,item.calcium_dv,item.potassium,item.potassium_dv,
                    item.iron,item.iron_dv, None)
        statement = 'INSERT INTO "Vitamins_and_Minerals" '
        statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
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

    conn.close()

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
            pasta_rice = []
            pasta = get_food_data("Pasta & Noodles")
            rice = get_food_data("Rice")
            for item in pasta:
                pasta_rice.append(item)
            for k in rice:
                pasta_rice.append(k)
            make_database(pasta_rice)
            user_input = input("Please choose one of the options above (or 'help' for options): ")
        elif user_input == "alcohol":
            alcohol = []
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
            fruit = []
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

ask_user()
# bread = get_food_data("Bread")
# # for item in bread:
# #     print(item.vita)
# make_database(bread)
