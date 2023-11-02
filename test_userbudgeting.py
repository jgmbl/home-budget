import unittest
from userbudgeting import UserBudgeting
import sqlite3
import datetime

class TestUserBudgeting(unittest.TestCase, UserBudgeting):

    def __add_data_to_table_budgeting(self, user_id, database):
        con = sqlite3.connect(database)
        cur = con.cursor()

        #current date
        today = datetime.datetime.today()
        current_date = today.strftime('%Y-%m-%d %H:%M')

        #get previous month date
        first_day = today.replace(day=1)
        previous_month = first_day - datetime.timedelta(days=7)
        previous_month = previous_month.strftime('%Y-%m-%d %H:%M')

        #add data to table budgeting
        #current date
        cur.execute("INSERT INTO budgeting(user_id, income, category, value, value_percent, date) VALUES (?, ?, ?, ?, ?, ?)", (user_id, 300000, "daily_spendings", 165000, 55, current_date))
        cur.execute("INSERT INTO budgeting(user_id, income, category, value, value_percent, date) VALUES (?, ?, ?, ?, ?, ?)", (user_id, 300000, "large_spendings", 30000, 10, current_date))
        cur.execute("INSERT INTO budgeting(user_id, income, category, value, value_percent, date) VALUES (?, ?, ?, ?, ?, ?)", (user_id, 300000, "investments", 45000, 15, current_date))
        cur.execute("INSERT INTO budgeting(user_id, income, category, value, value_percent, date) VALUES (?, ?, ?, ?, ?, ?)", (user_id, 300000, "education", 30000, 10, current_date))
        cur.execute("INSERT INTO budgeting(user_id, income, category, value, value_percent, date) VALUES (?, ?, ?, ?, ?, ?)", (user_id, 300000, "others", 30000, 10, current_date))

        #last month
        cur.execute("INSERT INTO budgeting(user_id, income, category, value, value_percent, date) VALUES (?, ?, ?, ?, ?, ?)", (user_id, 200000, "daily_spendings", 40000, 20, previous_month))
        cur.execute("INSERT INTO budgeting(user_id, income, category, value, value_percent, date) VALUES (?, ?, ?, ?, ?, ?)", (user_id, 200000, "large_spendings", 40000, 20, previous_month))
        cur.execute("INSERT INTO budgeting(user_id, income, category, value, value_percent, date) VALUES (?, ?, ?, ?, ?, ?)", (user_id, 200000, "investments", 40000, 20, previous_month))
        cur.execute("INSERT INTO budgeting(user_id, income, category, value, value_percent, date) VALUES (?, ?, ?, ?, ?, ?)", (user_id, 200000, "education", 40000, 20, previous_month))
        cur.execute("INSERT INTO budgeting(user_id, income, category, value, value_percent, date) VALUES (?, ?, ?, ?, ?, ?)", (user_id, 200000, "others", 40000, 20, previous_month))

        #different user
        cur.execute("INSERT INTO budgeting(user_id, income, category, value, value_percent, date) VALUES (?, ?, ?, ?, ?, ?)", (2, 300000, "daily_spendings", 165000, 55, current_date))
        cur.execute("INSERT INTO budgeting(user_id, income, category, value, value_percent, date) VALUES (?, ?, ?, ?, ?, ?)", (2, 300000, "large_spendings", 30000, 10, current_date))
        cur.execute("INSERT INTO budgeting(user_id, income, category, value, value_percent, date) VALUES (?, ?, ?, ?, ?, ?)", (2, 300000, "investments", 45000, 15, current_date))
        cur.execute("INSERT INTO budgeting(user_id, income, category, value, value_percent, date) VALUES (?, ?, ?, ?, ?, ?)", (2, 300000, "education", 30000, 10, current_date))
        cur.execute("INSERT INTO budgeting(user_id, income, category, value, value_percent, date) VALUES (?, ?, ?, ?, ?, ?)", (2, 300000, "others", 30000, 10, current_date))

        con.commit()
        con.close()

    def __delete_data_from_table(self, database):
        con = sqlite3.connect(database)
        cur = con.cursor()

        #delete data from table spendings
        cur.execute("DELETE FROM budgeting;")
        con.commit()

        con.close()

    
    def test_add_budgeting_to_table(self):
        user_id = 1
        database = "test_budget.db"

        #current date
        today = datetime.datetime.today()
        current_date = today.strftime('%Y-%m-%d %H:%M')

        con = sqlite3.connect(database)
        cur = con.cursor()

        #delete data from table
        self.__delete_data_from_table(database)

        #add data to table budgeting by tested method
        self.add_budgeting_to_table("daily_spendings", 20, 2000, user_id, database)

        #select data from table budgeting
        data = cur.execute("SELECT id, user_id, income, category, value, value_percent, date FROM budgeting ORDER BY date DESC LIMIT 1;")
        result = data.fetchall()
        con.close()

        expected_result = [(1, 1, 2000, 'daily_spendings', 400, 20, current_date)]

        self.assertEqual(result, expected_result)


    def test_check_sum_of_percent(self):
        value_1 = self.check_sum_of_percent(1,2,3,4,5)
        value_2 = self.check_sum_of_percent(20,20,20,20,20)

        self.assertFalse(value_1)
        self.assertTrue(value_2)


    def test_display_budgeting(self):
        user_id = 1
        database = "test_budget.db"

        #current date
        today = datetime.datetime.today()
        current_date = today.strftime('%Y-%m-%d %H:%M')

        #delete data from table budgeting
        self.__delete_data_from_table(database)

        #add data to table
        self.__add_data_to_table_budgeting(user_id, database)

        result = self.display_budgeting(user_id, database)
        expected_result = [('daily_spendings', 1650.0, 55, current_date), ('large_spendings', 300.0, 10, current_date), ('investments', 450.0, 15, current_date), ('education', 300.0, 10, current_date), ('others', 300.0, 10, current_date)]

        self.assertEqual(result, expected_result)

    
    def test_display_last_income(self):
        user_id = 1
        database = "test_budget.db"

        #delete data from table budgeting
        self.__delete_data_from_table(database)

        #add data to table
        self.__add_data_to_table_budgeting(user_id, database)

        result = self.display_last_income(user_id, database)
        expected_result = 3000.0

        self.assertEqual(result, expected_result)


    def test_float_to_int_value(self):
        value1 = self.float_to_int_value(11.5)
        value2 = self.float_to_int_value(5.98)

        self.assertEqual(value1, 1150)
        self.assertEqual(type(value1), int)

        self.assertEqual(value2, 598)
        self.assertEqual(type(value2), int)



if __name__ == "__main__":
    unittest.main()