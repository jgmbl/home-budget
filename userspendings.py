from flask import session
import sqlite3
import datetime
import calendar

class UserSpendings:
    def __init__(self):
        self.current_day = datetime.datetime.now().day
        self.current_month = datetime.datetime.now().month
        self.current_year = datetime.datetime.now().year


    """Add spendings from form to table spendings"""
    def add_spendings_to_table(self, category, value, note):

        current_date_and_time = datetime.datetime.now()
        current_date = current_date_and_time.strftime('%Y-%m-%d %H:%M')
        user_id = session["_user_id"]

        con = sqlite3.connect("instance/budget.db")
        cur = con.cursor()

        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, category, value, note, current_date))
        con.commit()
        con.close()


    def get_spendings_from_current_month(self):
        today = datetime.datetime.today()
        current_month = today.strftime("%m")

        user_id = session["_user_id"]

        con = sqlite3.connect("instance/budget.db")
        cur = con.cursor()

        select_spendings = cur.execute("SELECT category, value, note, date FROM spendings WHERE user_id = ? AND strftime('%m', date) = ?", (user_id, current_month))
        selected_spendings = select_spendings.fetchall()
        con.close()

        return selected_spendings


    def get_spendings_from_current_week(self):
        today = datetime.datetime.today()
        week_num_today = today.isocalendar()[1]
        year_today = today.year

        user_id = session["_user_id"]

        con = sqlite3.connect("instance/budget.db")
        cur = con.cursor()

        select_spendings = cur.execute("SELECT category, value, note, date FROM spendings WHERE user_id = ? AND strftime('%Y', date) = ? AND strftime('%W', date) = ?;", (user_id, str(year_today), str(week_num_today)))
        selected_spendings = select_spendings.fetchall()
        con.close()

        return selected_spendings


    def get_all_spendings(self):
        user_id = session["_user_id"]

        con = sqlite3.connect("instance/budget.db")
        cur = con.cursor()

        select_spendings = cur.execute("SELECT category, value, note, date FROM spendings WHERE user_id = ?;", (user_id, ))
        selected_spendings = select_spendings.fetchall()
        con.close()

        return selected_spendings
    