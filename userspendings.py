from flask import session
import sqlite3
import datetime

class UserSpendings:
    """Add spendings from form to table spendings"""
    def add_spendings_to_table(self, category, value, note):

        date = datetime.datetime.now()
        date = date.strftime('%Y-%m-%d %H:%M')
        user_id = session["_user_id"]

        con = sqlite3.connect("instance/budget.db")
        cur = con.cursor()

        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, category, value, note, date))
        con.commit()
        con.close()