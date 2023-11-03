import unittest
from userbudgeting import UserBudgeting
import sqlite3
import datetime

class TestUserBudgeting(unittest.TestCase, UserBudgeting):

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

        con.commit()
        con.close()


    def __delete_data_from_table(self, database):
        con = sqlite3.connect(database)
        cur = con.cursor()

        #delete data from table spendings
        cur.execute("DELETE FROM savings;")
        con.commit()

        con.close()


if __name__ == "__main__":
    unittest.main()