import unittest
from userbudgeting import UserBudgeting
import sqlite3
import datetime

class TestUserBudgeting(unittest.TestCase, UserBudgeting):

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


if __name__ == "__main__":
    unittest.main()