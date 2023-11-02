import unittest
from userspendings import UserSpendings
import sqlite3
import datetime

class TestUserSpendings(unittest.TestCase, UserSpendings):

    def test_add_spendings_to_table(self):
        user_id = 1
        database = "test_budget.db"

        con = sqlite3.connect(database)
        cur = con.cursor()

        #delete data from table spendings
        cur.execute("DELETE FROM spendings;")
        con.commit()

        self.add_spendings_to_table("investments", 10.0, "Test", user_id, database)

        #select data from table spendings
        data = cur.execute("SELECT user_id, category, value, note FROM spendings ORDER BY date DESC LIMIT 1;")

        result_from_database = data.fetchall()
        con.close()

        expected_result = [(1, "investments", 1000, "Test")];

        self.assertEqual(result_from_database, expected_result)

    
    def test_get_spendings_from_current_month(self):
        user_id = 1
        database = "test_budget.db"

        #current date
        today = datetime.datetime.today()
        current_date = today.strftime('%Y-%m-%d %H:%M')

        #get previous month date
        first_day = today.replace(day=1)
        previous_month = first_day - datetime.timedelta(days=1)
        previous_month = previous_month.strftime('%Y-%m-%d %H:%M')

        #get next month date
        next_month = first_day + datetime.timedelta(days=30)
        next_month = next_month.strftime('%Y-%m-%d %H:%M')

        con = sqlite3.connect(database)
        cur = con.cursor()

        #delete data from table spendings
        cur.execute("DELETE FROM spendings;")
        con.commit()

        #add data to table spendings
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "daily_spendings", 1000, "test0", current_date))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "large_spendings", 2000, "test1", current_date))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "investment", 2050, "test2", current_date))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "education", 5000, "test3", previous_month))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "daily_spendings", 3000, "test4", previous_month))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "other", 4000, "test5", next_month))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "daily_spendings", 3000, "test6", next_month))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "education", 2000, "test7", next_month))
        con.commit()

        con.close()

        #get spendings by tested method
        result_from_database = self.get_spendings_from_current_month(user_id, database)

        expected_result = [('daily_spendings', 10.00, 'test0', current_date), ('large_spendings', 20.00, 'test1', current_date), ('investment', 20.50, 'test2', current_date)]

        self.assertEqual(result_from_database, expected_result)


    def test_get_spendings_from_current_week(self):
        user_id = 1
        database = "test_budget.db"

        #current date
        today = datetime.datetime.today()
        current_date = today.strftime('%Y-%m-%d %H:%M')

        #get previous month date
        first_day = today.replace(day=1)
        previous_month = today - datetime.timedelta(days=7)
        previous_month = previous_month.strftime('%Y-%m-%d %H:%M')

        #get next month date
        next_month = first_day + datetime.timedelta(days=30)
        next_month = next_month.strftime('%Y-%m-%d %H:%M')

        con = sqlite3.connect(database)
        cur = con.cursor()

        #delete data from table spendings
        cur.execute("DELETE FROM spendings;")
        con.commit()

        #add data to table spendings
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "daily_spendings", 1000, "test0", current_date))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "large_spendings", 2000, "test1", current_date))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "investment", 2000, "test2", current_date))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "education", 5000, "test3", previous_month))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "daily_spendings", 3000, "test4", previous_month))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "other", 4000, "test5", next_month))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "large_spendings", 1500, "test6", next_month))
        
        con.commit()
        con.close()

        #get spendings by tested method
        result_from_database = self.get_spendings_from_current_week(user_id, database)

        expected_result = [('daily_spendings', 10.00, 'test0', current_date), ('large_spendings', 20.00, 'test1', current_date), ('investment', 20.00, 'test2', current_date)]
        self.assertEqual(result_from_database, expected_result)


    def test_get_all_spendings(self):
        user_id = 1
        database = "test_budget.db"

        #current date
        today = datetime.datetime.today()
        current_date = today.strftime('%Y-%m-%d %H:%M')

        #get previous month date
        first_day = today.replace(day=1)
        previous_month = first_day - datetime.timedelta(days=7)
        previous_month = previous_month.strftime('%Y-%m-%d %H:%M')

        #get next month date
        next_month = first_day + datetime.timedelta(days=30)
        next_month = next_month.strftime('%Y-%m-%d %H:%M')

        con = sqlite3.connect(database)
        cur = con.cursor()

        #delete data from table spendings
        cur.execute("DELETE FROM spendings;")
        con.commit()

        #add data to table spendings
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "daily_spendings", 1000, "test0", current_date))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "large_spendings", 2210, "test1", current_date))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "investment", 2000, "test2", current_date))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "education", 5000, "test3", previous_month))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "daily_spendings", 3333, "test4", previous_month))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "other", 4000, "test5", next_month))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "large_spendings", 1500, "test6", next_month))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "other", 2555, "test7", current_date))
        
        con.commit()
        con.close()

        #get spendings by tested method
        result_from_database = self.get_all_spendings(user_id, database)

        expected_result = [('other', 40.00, 'test5', next_month), ('large_spendings', 15.00, 'test6', next_month), ('daily_spendings', 10.00, 'test0', current_date), ('large_spendings', 22.10, 'test1', current_date), ('investment', 20.00, 'test2', current_date), ('other', 25.55, 'test7', current_date), ('education', 50.00, 'test3', previous_month), ('daily_spendings', 33.33, 'test4', previous_month)]
        self.assertEqual(result_from_database, expected_result)


    def test_sum_of_categories_from_current_month(self):
        user_id = 1
        database = "test_budget.db"

        con = sqlite3.connect(database)
        cur = con.cursor()

        #delete data from table spendings
        cur.execute("DELETE FROM spendings;")
        con.commit()

        #current date
        today = datetime.datetime.today()
        current_date = today.strftime('%Y-%m-%d %H:%M')

        #get previous month date
        first_day = today.replace(day=1)
        previous_month = first_day - datetime.timedelta(days=7)
        previous_month = previous_month.strftime('%Y-%m-%d %H:%M')

        #get next month date
        next_month = first_day + datetime.timedelta(days=30)
        next_month = next_month.strftime('%Y-%m-%d %H:%M')

        #add data to table spendings
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "daily_spendings", 1000, "test0", current_date))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "large_spendings", 2210, "test1", current_date))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "investments", 2000, "test2", current_date))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "education", 5000, "test3", previous_month))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "daily_spendings", 3333, "test4", previous_month))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "other", 4000, "test5", next_month))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "large_spendings", 1500, "test6", next_month))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "others", 2555, "test7", current_date))
        
        con.commit()
        con.close()

        #get spendings by tested method
        result_from_database = self.sum_of_categories_from_current_month(user_id, database)

        expected_result = {'daily_spendings': 10.0, 'large_spendings': 22.10, 'investments': 20.0, 'education': 0.0, 'others': 25.55, 'total': 77.65}
        self.assertEqual(result_from_database, expected_result)

if __name__ == "__main__":
    unittest.main()