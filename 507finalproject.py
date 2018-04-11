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

# print(category_dict.keys())
# # for item in category_dict:
# #     print(item.keys())
class Food():
    def __init__(self, f_url):
        self.f_url = f_url

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


        # individual_food_request = make_request_using_cache(individual_food_url)
        # individual_food_soup = BeautifulSoup(individual_food_request, 'html.parser')
        # item_details = individual_food_soup.find_all(class_='item')
        # print(item_details)

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
        # print(fn.text)
        # for item in food_name:
        #     print(item)
        # print(food_name)
        # print(item_details)
        for k in item_details:
            facts_split = k.text.split("\n")
            del(facts_split[0])
            del(facts_split[-1])
            # print(facts_split)

            if facts_split[0] == "Calories (%DV based on daily intake of 2,000 kcal)":
                self.calories_title = "Calories"
                self.calories = facts_split[1].strip('kcal')
                self.calories_dv = facts_split[2].strip('%')
            if facts_split[0] == "Total Fat (DRI 65 g)":
                self.fat_title = "Total Fat"
                self.fat = facts_split[1].strip('g')
                self.fat_dv = facts_split[2].strip('%')
            if facts_split[0] == "Cholesterol (DRI 300 mg)":
                self.cholesterol_title = "Cholesterol"
                self.cholesterol = facts_split[1].strip('mg')
                self.cholesterol_dv = facts_split[2].strip('%')
            if facts_split[0] == "Sodium (DRI 2,400 mg)":
                self.sodium_title = "Sodium"
                self.sodium = facts_split[1].strip('mg')
                self.sodium_dv = facts_split[2].strip('%')
            if facts_split[0] == "Total Carbohydrate (DRI 300 g)":
                self.carbs_title = "Total Carbohydrates"
                self.carbs = facts_split[1].strip('g')
                self.carbs_dv = facts_split[2].strip('%')
            if facts_split[0] == "Dietary Fiber (DRI 25 g)":
                self.fiber_title = "Fiber"
                self.fiber = facts_split[1].strip('g')
                self.fiber_dv = facts_split[2].strip('%')
            if facts_split[0] == "Sugars (WHO recommended maximum daily intake 25 g)":
                self.sugar_title = "Sugar"
                self.sugar = facts_split[1].strip('g')
                self.sugar_dv = facts_split[2].strip('%')
            if facts_split[0] == "Protein (DRI 50 g)":
                self.protein_title = "Protein"
                self.protein = facts_split[0].strip('g')
                self.protein_dv = facts_split[1].strip('%')
            if facts_split[0] == "Vitamin A (DRI 5000 IU)":
                self.vita_title = "Vitamin A"
                self.vita = facts_split[1].strip('IU')
                self.vita_dv = facts_split[2].strip('%')
            if facts_split[0] == "Vitamin C (DRI 60 mg)":
                self.vitc_title = "Vitamin C"
                self.vitc = facts_split[1].strip('mg')
                self.vitc_dv = facts_split[2].strip('%')
            if facts_split[0] == "Calcium (DRI 1000 mg)":
                self.calcium_title = "Calcium"
                self.calcium = facts_split[1].strip('mg')
                self.calcium_dv = facts_split[2].strip('%')
            if facts_split[0] == "Potassium (DRI 3500)":
                self.potassium_title = "Potassium"
                self.potassium = facts_split[1].strip('mg')
                self.potassium_dv = facts_split[2].strip('%')
            if facts_split[0] == "Iron (DRI 18 mg)":
                self.iron_title = "Iron"
                self.iron = facts_split[1].strip('mg')
                self.iron_dv = facts_split[2].strip('%')


            # insertion = (self.name,self.calories,self.calories_dv,self.fat,self.fat_dv,
            #             self.cholesterol,self.cholesterol_dv,self.sodium,self.sodium_dv,
            #             self.carbs,self.carbs_dv,self.fiber,self.fiber_dv,self.sugar,
            #             self.sugar_dv,self.protein,self.protein_dv)
            # statement = 'INSERT INTO "Nutrition Facts" '
            # statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            # cur.execute(statement, insertion)
            # conn.commit()


        conn.close()



food_class_list = []
def get_food_data(food_name):
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
        # print(individual_food_url)
        # individual_food_request = make_request_using_cache(individual_food_url)
        # individual_food_soup = BeautifulSoup(individual_food_request, 'html.parser')
        # item_details = individual_food_soup.find_all(class_='item')
        # # print(item_details)
        # for k in item_details:
        #     print(k.text.split("\n"))
            # if "Calories " == k.text[:9]:
            #     print(k.text)
        #     deets = k.find(class_='value cals')
        #     print(deets)
            # if k[0].text == "Total Fat":
    #         #     print(k[0].text)

    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

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

get_food_data("Bread")






# for item in table_rows:
#     print(item.text)
# food_tags_dict = {}
# food_url = ""
# for item in table_rows:
#     url_end = item.find('a')['href']
#     food_url = baseurl + url_end
#     food_tags_dict[item.text] = food_url
#     # print(food_url)
#
# chicken_end = food_tags_dict["chicken"]
# chicken_url = baseurl + chicken_end
# # print(chicken_url)
# chicken_request = make_request_using_cache(chicken_url)
# chicken_text = chicken_request.text
# chicken_soup = BeautifulSoup(chicken_request,'html.parser')
# chicken_items = chicken_soup.find(class_='food_search_results')
# chicken_desc = chicken_items.find_all(class_="food_description")
#
# chicken_dict = {}
# for item in chicken_desc:
#     chicken_url_end = item.find('a')['href']
#     individual_chicken_text = item.text
#     # print(individual_chicken_text)
#     individual_chicken_url = baseurl + chicken_url_end
#     # print(individual_chicken_url)
#     chicken_dict[individual_chicken_text] = individual_chicken_url
#
# print(chicken_dict)
