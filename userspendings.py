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

        #user_id = session["_user_id"]
        user_id = 1

        con = sqlite3.connect("instance/budget.db")
        cur = con.cursor()

        select_spendings = cur.execute("SELECT category, value, note, date FROM spendings WHERE user_id = ? AND strftime('%m', date) = ?", (user_id, current_month))
        selected_spendings = select_spendings.fetchall()
        con.close()

        return selected_spendings


    def __current_week_days(self):
        """Returns a list of days in week to current day"""
        #[[day, month, year]]

        month_days = calendar.monthcalendar(self.current_year, self.current_month)

        week_day = []
        week_single_day = []
        week_all_days = []

        for week in month_days:
            if self.current_day in week:
                week_day = week

        for day in week_day:
            week_single_day = [day, calendar.month_name[self.current_month], self.current_year]
            week_all_days.append(week_single_day)

        return week_all_days
    
