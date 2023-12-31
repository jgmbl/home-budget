import sqlite3
import datetime

class UserSpendings:
    def __init__(self):
        self.current_day = datetime.datetime.now().day
        self.current_month = datetime.datetime.now().month
        self.current_year = datetime.datetime.now().year


    """Add spendings from form to table spendings"""
    def add_spendings_to_table(self, category, value, note, user_id, database):

        current_date_and_time = datetime.datetime.now()
        current_date = current_date_and_time.strftime('%Y-%m-%d %H:%M')
        
        con = sqlite3.connect(database)
        cur = con.cursor()

        cur.execute("INSERT INTO spendings(user_id, category, value, note, date) VALUES (?, ?, ?, ?, ?)", (user_id, category, self.float_to_int_value(value), note, current_date))
        con.commit()
        con.close()


    """Get spendings from current month"""
    def get_spendings_from_current_month(self, user_id, database):
        today = datetime.datetime.today()
        current_month = today.strftime("%m")

        con = sqlite3.connect(database)
        cur = con.cursor()

        select_spendings = cur.execute("SELECT category, value, note, date FROM spendings WHERE user_id = ? AND strftime('%m', date) = ? ORDER BY date DESC", (user_id, current_month))
        selected_spendings_cents = select_spendings.fetchall()
        con.close()

        selected_spendings_dollars = []
        
        for category, value, note, date in selected_spendings_cents:
            value = value / 100
            selected_spendings_dollars.append((category, value, note, date))

        return selected_spendings_dollars


    """Get spendings from current week"""
    def get_spendings_from_current_week(self, user_id, database):
        today = datetime.datetime.today()
        week_num_today = today.isocalendar()[1]
        year_today = today.year

        con = sqlite3.connect(database)
        cur = con.cursor()

        select_spendings = cur.execute("SELECT category, value, note, date FROM spendings WHERE user_id = ? AND strftime('%Y', date) = ? AND strftime('%W', date) = ? ORDER BY date DESC;", (user_id, str(year_today), str(week_num_today)))
        selected_spendings_cents = select_spendings.fetchall()
        con.close()

        selected_spendings_dollars = []

        for category, value, note, date in selected_spendings_cents:
            value = value / 100
            selected_spendings_dollars.append((category, value, note, date))

        return selected_spendings_dollars


    """Get all spendings"""
    def get_all_spendings(self, user_id, database):
        con = sqlite3.connect(database)
        cur = con.cursor()

        select_spendings = cur.execute("SELECT category, value, note, date FROM spendings WHERE user_id = ? ORDER BY date DESC;", (user_id, ))
        selected_spendings_cents = select_spendings.fetchall()
        con.close()

        selected_spendings_dollars = []

        for category, value, note, date in selected_spendings_cents:
            value = value / 100
            selected_spendings_dollars.append((category, value, note, date))

        return selected_spendings_dollars
    

    """Get sum of spendings from current month, grouped by categories"""
    def sum_of_categories_from_current_month(self,user_id, database):
        data = self.get_spendings_from_current_month(user_id, database)

        sum_daily_spendings = 0.0
        sum_large_spendings = 0.0
        sum_investments = 0.0
        sum_education = 0.0
        sum_others = 0.0
        sum_total = 0.0

        #*100 to fix the bug of rounding
        for i in data:
            if i[0] == 'daily_spendings':
                sum_daily_spendings += i[1] * 100

            elif i[0] == "large_spendings":
                sum_large_spendings += i[1] * 100

            elif i[0] == "investments":
                sum_investments += i[1] * 100

            elif i[0] == "education":
                sum_education += i[1] * 100

            elif i[0] == "others":
                sum_others += i[1] * 100

        for i in data:
            sum_total += i[1] * 100


        categories_month = {'daily_spendings': sum_daily_spendings / 100, 'large_spendings': sum_large_spendings / 100, 'investments': sum_investments / 100, 'education': sum_education / 100, 'others': sum_others / 100, 'total': sum_total / 100}

        return categories_month
    

    """Get sum of spendings from current week, grouped by categories"""
    def __sum_of_categories_from_current_week(self, user_id, database):
        data = self.get_spendings_from_current_week(user_id, database)

        sum_daily_spendings = 0.0
        sum_large_spendings = 0.0
        sum_investments = 0.0
        sum_education = 0.0
        sum_others = 0.0
        sum_total = 0.0

        #*100 to fix the bug of rounding
        for i in data:
            if i[0] == 'daily_spendings':
                sum_daily_spendings += i[1] * 100

            elif i[0] == "large_spendings":
                sum_large_spendings += i[1] * 100

            elif i[0] == "investments":
                sum_investments += i[1] * 100

            elif i[0] == "education":
                sum_education += i[1] * 100

            elif i[0] == "others":
                sum_others += i[1] * 100

        for i in data:
            sum_total += i[1] * 100

        
        categories_week = {'daily_spendings': sum_daily_spendings / 100, 'large_spendings': sum_large_spendings / 100, 'investments': sum_investments / 100, 'education': sum_education / 100, 'others': sum_others / 100, 'total': sum_total / 100}

        return categories_week
    

    """Get sum of all spendings, grouped by categories"""
    def __sum_of_categories_all(self, user_id, database):
        data = self.get_all_spendings(user_id, database)

        sum_daily_spendings = 0.0
        sum_large_spendings = 0.0
        sum_investments = 0.0
        sum_education = 0.0
        sum_others = 0.0
        sum_total = 0.0

        #*100 to fix the bug of rounding
        for i in data:
            if i[0] == 'daily_spendings':
                sum_daily_spendings += i[1] * 100

            elif i[0] == "large_spendings":
                sum_large_spendings += i[1] * 100

            elif i[0] == "investments":
                sum_investments += i[1] * 100

            elif i[0] == "education":
                sum_education += i[1] * 100

            elif i[0] == "others":
                sum_others += i[1] * 100

        for i in data:
            sum_total += i[1] * 100


        categories_all = {'daily_spendings': sum_daily_spendings / 100, 'large_spendings': sum_large_spendings  / 100, 'investments': sum_investments  / 100, 'education': sum_education  / 100, 'others': sum_others  / 100, 'total': sum_total / 100}

        return categories_all 


    """Displaying sum of categories by a period of time"""
    def display_sum_of_categories(self, period, user_id, database):
        sum_by_period = {}
        if period == "last_month":
            sum_by_period = self.sum_of_categories_from_current_month(user_id, database)

        elif period == "last_week":
            sum_by_period = self.__sum_of_categories_from_current_week(user_id, database)

        elif period == "all":
            sum_by_period = self.__sum_of_categories_all(user_id, database)

        return sum_by_period
    

    """Change value from float to int - dollars to cents"""
    def float_to_int_value(self, value):
        value = value * 100
        value = int(value)

        return value

