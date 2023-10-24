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


    """Get spendings from current month"""
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


    """Get spendings from current week"""
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


    """Get all spendings"""
    def get_all_spendings(self):
        user_id = session["_user_id"]

        con = sqlite3.connect("instance/budget.db")
        cur = con.cursor()

        select_spendings = cur.execute("SELECT category, value, note, date FROM spendings WHERE user_id = ?;", (user_id, ))
        selected_spendings = select_spendings.fetchall()
        con.close()

        return selected_spendings
    

    """Get sum of spendings from current month, grouped by categories"""
    @property
    def sum_of_categories_from_current_month(self):
        data = self.get_spendings_from_current_month()

        sum_daily_spendings = 0.00
        sum_large_spendings = 0.00
        sum_investments = 0.00
        sum_education = 0.00
        sum_others = 0.00
        sum_total = 0.00

        for i in data:
            if i[0] == 'daily_spendings':
                sum_daily_spendings += i[1] 

            elif i[0] == "large_spendings":
                sum_large_spendings += i[1]

            elif i[0] == "investments":
                sum_investments += i[1]

            elif i[0] == "education":
                sum_education += i[1]

            elif i[0] == "others":
                sum_others += i[1]

        for i in data:
            sum_total += i[1]


        categories_month = {'daily_spendings': sum_daily_spendings, 'large_spendings': sum_large_spendings, 'investments': sum_investments, 'education': sum_education, 'others': sum_others, 'total': sum_total}

        return categories_month
    

    """Get sum of spendings from current week, grouped by categories"""
    @property
    def __sum_of_categories_from_current_week(self):
        data = self.get_spendings_from_current_week()

        sum_daily_spendings = 0.00
        sum_large_spendings = 0.00
        sum_investments = 0.00
        sum_education = 0.00
        sum_others = 0.00
        sum_total = 0.00

        for i in data:
            if i[0] == 'daily_spendings':
                sum_daily_spendings += i[1] 

            elif i[0] == "large_spendings":
                sum_large_spendings += i[1]

            elif i[0] == "investments":
                sum_investments += i[1]

            elif i[0] == "education":
                sum_education += i[1]

            elif i[0] == "others":
                sum_others += i[1]

        for i in data:
            sum_total += i[1]


        categories_week = {'daily_spendings': sum_daily_spendings, 'large_spendings': sum_large_spendings, 'investments': sum_investments, 'education': sum_education, 'others': sum_others, 'total': sum_total}

        return categories_week
    

    """Get sum of all spendings, grouped by categories"""
    @property
    def __sum_of_categories_all(self):
        data = self.get_all_spendings()

        sum_daily_spendings = 0.00
        sum_large_spendings = 0.00
        sum_investments = 0.00
        sum_education = 0.00
        sum_others = 0.00
        sum_total = 0.00

        for i in data:
            if i[0] == 'daily_spendings':
                sum_daily_spendings += i[1] 

            elif i[0] == "large_spendings":
                sum_large_spendings += i[1]

            elif i[0] == "investments":
                sum_investments += i[1]

            elif i[0] == "education":
                sum_education += i[1]

            elif i[0] == "others":
                sum_others += i[1]

        for i in data:
            sum_total += i[1]


        categories_all = {'daily_spendings': sum_daily_spendings, 'large_spendings': sum_large_spendings, 'investments': sum_investments, 'education': sum_education, 'others': sum_others, 'total': sum_total}

        return categories_all 


    """Displaying sum of categories by a period of time"""
    def display_sum_of_categories(self, period):
        sum_by_period = {}
        if period == "last_month":
            sum_by_period = self.sum_of_categories_from_current_month

        elif period == "last_week":
            sum_by_period = self.__sum_of_categories_from_current_week

        elif period == "all":
            sum_by_period = self.__sum_of_categories_all

        return sum_by_period