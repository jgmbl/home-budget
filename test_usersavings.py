import unittest
from userbudgeting import UserBudgeting
import sqlite3
import datetime

class TestUserBudgeting(unittest.TestCase, UserBudgeting):

    def __delete_data_from_table(self, database):
        con = sqlite3.connect(database)
        cur = con.cursor()

        #delete data from table spendings
        cur.execute("DELETE FROM savings;")
        con.commit()

        con.close()


if __name__ == "__main__":
    unittest.main()