import unittest
from usersummary import UserSummary
import sqlite3
import datetime


class TestUserBudgeting(unittest.TestCase, UserSummary):

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


    def __add_data_to_table_spendings(self, user_id, database):
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
        next_month = first_day + datetime.timedelta(days=32)
        next_month = next_month.strftime('%Y-%m-%d %H:%M')

        #add data to table spendings
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "daily_spendings", 1000, "test0", current_date))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "large_spendings", 2210, "test1", current_date))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "investments", 2000, "test2", current_date))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "education", 5000, "test3", previous_month))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "daily_spendings", 3333, "test4", previous_month))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "others", 4000, "test5", next_month))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "large_spendings", 1500, "test6", next_month))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, "others", 2555, "test7", current_date))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (2, "others", 2555, "test8", current_date))
        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (3, "daily_spendings", 2555, "test9", previous_month))
        
        con.commit()
        con.close()

    
    def __delete_data_from_table(self, database):
        con = sqlite3.connect(database)
        cur = con.cursor()

        #delete data from table spendings
        cur.execute("DELETE FROM budgeting;")
        cur.execute("DELETE FROM spendings;")
        con.commit()

        con.close()


if __name__ == "__main__":
    unittest.main()