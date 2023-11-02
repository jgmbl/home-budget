import unittest
from userspendings import UserSpendings
import sqlite3

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


if __name__ == "__main__":
    unittest.main()