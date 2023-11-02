import unittest
from userspendings import UserSpendings
import sqlite3
import datetime

class TestUserSpendings(unittest.TestCase, UserSpendings):

    def test_add_spendings_to_table(self):
        user_id = 1
        database = "test_budget.db"

        self.add_spendings_to_table("investments", 10.0, "Test", user_id, database)

        con = sqlite3.connect(database)
        cur = con.cursor()
        data = cur.execute("SELECT user_id, category, value, note FROM spendings ORDER BY date DESC LIMIT 1;")

        result_from_database = data.fetchall()
        con.close()

        expected_result = [(1, "investments", 10, "Test")];

        self.assertEqual(result_from_database, expected_result)

    
    def test_get_spendings_from_current_month(self):
        user_id = 1
        database = "test_budget.db"

        #get current month number
        today = datetime.datetime.today()
        current_date = today.strftime('%Y-%m-%d %H:%M')

        #get last month date
        first_day = today.replace(day=1)
        last_month = first_day - datetime.timedelta(days=1)
        last_month = last_month.strftime('%Y-%m-%d %H:%M')

        con = sqlite3.connect(database)
        cur = con.cursor()

        #delete data from table spendings
        cur.execute("DELETE FROM spendings;")
        con.commit()

        #add data to table spendings
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "daily_spendings", 10.0, "test0", current_date))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "large_spendings", 20.0, "test1", current_date))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "investment", 20.0, "test2", current_date))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "education", 50.0, "test3", last_month))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "daily_spendings", 30.0, "test4", last_month))
        con.commit()

        con.close()

        #get spendings by tested method
        result_from_database = self.get_spendings_from_current_month(user_id, database)

        expected_result = [('daily_spendings', 0.1, 'test0', current_date), ('large_spendings', 0.2, 'test1', current_date), ('investment', 0.2, 'test2', current_date)]

        self.assertEqual(result_from_database, expected_result)


if __name__ == "__main__":
    unittest.main()