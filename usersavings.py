from flask import session
import datetime
import sqlite3

class UserSavings:

    """Check if the user data are empty"""
    def __check_if_user_data_are_empty(self):
        user_id = session["_user_id"]

        con = sqlite3.connect("instance/budget.db")
        cur = con.cursor()

        cur.execute("SELECT COUNT (*) FROM savings WHERE user_id = ?", (user_id, ))
        content_of_table = cur.fetchall()
        con.close()

        return content_of_table[0][0]
    

    """Add data to table spendings"""
    def add_data_to_table(self, value):
        user_id = session["_user_id"]

        current_date_and_time = datetime.datetime.now()
        current_date = current_date_and_time.strftime('%Y-%m-%d %H:%M')

        con = sqlite3.connect("instance/budget.db")
        cur = con.cursor()

        count_rows = self.__check_if_user_data_are_empty()

        if count_rows == 0:
            cur.execute("INSERT INTO savings(user_id, value, value_summary, date) VALUES (?, ?, ?, ?)", (user_id, value, value, current_date))
            con.commit()

        else:
            cur.execute("SELECT value_summary FROM savings WHERE user_id = ? ORDER BY id DESC LIMIT 1", (user_id, ))
            last_value_summary = cur.fetchall()
            last_value_summary = last_value_summary[0][0]

            current_value_summary = last_value_summary + value

            cur.execute("INSERT INTO savings(user_id, value, value_summary, date) VALUES (?, ?, ?, ?)", (user_id, value, current_value_summary, current_date))
            con.commit()
        
        con.close()
