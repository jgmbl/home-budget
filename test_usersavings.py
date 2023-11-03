import unittest
from usersavings import UserSavings
import sqlite3
import datetime

class TestUserBudgeting(unittest.TestCase, UserSavings):

    def __add_data_to_table_savings(self, user_id, database):
        con = sqlite3.connect(database)
        cur = con.cursor()

        #current date
        today = datetime.datetime.today()
        current_date = today.strftime('%Y-%m-%d %H:%M')

        #get previous month date
        first_day = today.replace(day=1)
        previous_month = first_day - datetime.timedelta(days=7)
        previous_month = previous_month.strftime('%Y-%m-%d %H:%M')

        cur.execute("INSERT INTO savings(user_id, value, value_summary, date) VALUES (?, ?, ?, ?)", (user_id, 100000, 100000, previous_month))
        cur.execute("INSERT INTO savings(user_id, value, value_summary, date) VALUES (?, ?, ?, ?)", (user_id, 150000, 250000, previous_month))
        cur.execute("INSERT INTO savings(user_id, value, value_summary, date) VALUES (?, ?, ?, ?)", (user_id, 250000, 500000, previous_month))
        cur.execute("INSERT INTO savings(user_id, value, value_summary, date) VALUES (?, ?, ?, ?)", (user_id, 100000, 600000, current_date))
        cur.execute("INSERT INTO savings(user_id, value, value_summary, date) VALUES (?, ?, ?, ?)", (user_id, 200000, 800000, current_date))
        cur.execute("INSERT INTO savings(user_id, value, value_summary, date) VALUES (?, ?, ?, ?)", (user_id, 250000, 1050000, current_date))
        cur.execute("INSERT INTO savings(user_id, value, value_summary, date) VALUES (?, ?, ?, ?)", (user_id + 1, 300000, 300000, current_date))
        cur.execute("INSERT INTO savings(user_id, value, value_summary, date) VALUES (?, ?, ?, ?)", (user_id + 1, 200000, 500000, current_date))
        cur.execute("INSERT INTO savings(user_id, value, value_summary, date) VALUES (?, ?, ?, ?)", (user_id + 1, 500000, 1000000, current_date))

        con.commit()
        con.close()


    def __delete_data_from_table(self, database):
        con = sqlite3.connect(database)
        cur = con.cursor()

        #delete data from table spendings
        cur.execute("DELETE FROM savings;")
        con.commit()

        con.close()


    def test_add_data_to_table(self):
        user_id = 1
        database = "test_budget.db"

        #current date
        today = datetime.datetime.today()
        current_date = today.strftime('%Y-%m-%d %H:%M')

        con = sqlite3.connect(database)
        cur = con.cursor()

        #delete records from table savings
        self.__delete_data_from_table(database)

        #add data to database by tested methods
        self.add_data_to_table(100000, user_id, database)
        self.add_data_to_table(400000, 2, database)
        self.add_data_to_table(500000, 3, database)
        self.add_data_to_table(100000, user_id, database)
        self.add_data_to_table(300000, user_id, database)

        #select data from table savings
        data = cur.execute("SELECT id, user_id, value, value_summary, date FROM savings WHERE user_id = ?;", (user_id, ))
        result = data.fetchall()
        con.close()

        expected_result = [(1, 1, 100000, 100000, current_date), (4, 1, 100000, 200000, current_date), (5, 1, 300000, 500000, current_date)]

        self.assertEqual(result, expected_result)


    def test_sum_of_savings_current_month(self):
        user_id = 1
        database = "test_budget.db"

        #delete records from table savings
        self.__delete_data_from_table(database)

        #add records to table savings
        self.__add_data_to_table_savings(user_id, database)

        result = self.sum_of_savings_current_month(user_id, database)

        expected_result = 5500.0

        self.assertEqual(result, expected_result)




if __name__ == "__main__":
    unittest.main()