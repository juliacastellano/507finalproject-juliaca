import unittest
from finalproject507 import *

class TestFoodInstance(unittest.TestCase):
    def test_food(self):
        beer = get_food_data("Beer")
        self.assertEqual(len(beer), 18)
        self.assertIsInstance(beer[0], Food)
        self.assertIs(type(beer[0].name), str)
        self.assertIsNotNone(beer[15].calories)
        self.assertIsNotNone(beer[5].protein_dv)


class TestGetFood(unittest.TestCase):
    def test_get_food(self):
        bread = get_food_data("Bread")
        self.assertEqual(len(bread), 201)
        self.assertIs(type(bread), list)
        self.assertIsInstance(bread[0], Food)


class TestDatabase(unittest.TestCase):
    def test_nutrition_table(self):
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()

        bread = get_food_data("Bread")
        make_database(bread)

        sql = 'SELECT Name FROM Nutrition_Facts'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('PILLSBURY, Crusty French Loaf, refrigerated dough (1 serving - 62 g)',), result_list)
        self.assertEqual(len(result_list), 201)

        sql = '''
            SELECT Calories, CaloriesDV, TotalFat, TotalFatDV, Cholesterol, CholesterolDV, Sodium,
                   SodiumDV, TotalCarbohydrates, TotalCarbohydratesDV, Fiber, FiberDV,
                   Sugar, SugarDV, Protein, ProteinDV
            FROM Nutrition_Facts
            WHERE Name="Bread, reduced-calorie, oat bran (1 oz - 28 g)"
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list[0]), 16)
        self.assertEqual(result_list[0][0], 57.1)
        self.assertEqual(result_list[0][14], 2.3)

        conn.close()

    def test_vitamin_table(self):
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()

        cake = get_food_data("Cake")
        make_database(cake)

        sql = 'SELECT Name FROM Vitamins_and_Minerals'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Coffeecake, cinnamon with crumb topping, dry mix, prepared (1 oz - 28 g)',), result_list)
        self.assertEqual(len(result_list), 100)


        sql = '''
            SELECT Calories, VitaminA, VitaminADV, VitaminC, VitaminCDV, Calcium,
                   CalciumDV, Potassium, PotassiumDV, Iron, IronDV
            FROM Vitamins_and_Minerals
            WHERE Name="Cake, pound, commercially prepared, fat-free (1 cake - 340 g)"
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list[0]), 11)
        self.assertEqual(result_list[0][1], 323)
        self.assertEqual(result_list[0][7], 374)

        conn.close()

if __name__ == '__main__':
    unittest.main()
