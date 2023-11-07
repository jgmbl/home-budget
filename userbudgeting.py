import sqlite3
import datetime


FULL_PERCENTAGE = 100

class UserBudgeting:
    """Convert percent value to numerical value"""
    def __value_percent_to_value_budgeting(self, value_percent, value):
        value_budgeting = value_percent * (value / FULL_PERCENTAGE)

        return value_budgeting
    

    """Add budgeting from form to table budgeting"""
    def add_budgeting_to_table(self, category, value_percent, income, user_id, database):

        value = self.__value_percent_to_value_budgeting(value_percent, income)
        date = datetime.datetime.now()
        date = date.strftime('%Y-%m-%d %H:%M')

        con = sqlite3.connect(database)
        cur = con.cursor()

        cur.execute("INSERT INTO  budgeting(user_id, income, category, value, value_percent, date) VALUES (?, ?, ?, ?, ?, ?)", (user_id, income, category, value, value_percent, date))
        con.commit()
        con.close()


    """Check if sum of percents is equal 100"""
    @staticmethod
    def check_sum_of_percent(*argv):
        sum_percent = 0

        for args in argv:
            sum_percent += args
        
        if sum_percent != FULL_PERCENTAGE:
            return False
        
        return True
    

    """Display category, value and value_percent from database to table on website"""
    @staticmethod
    def display_budgeting(user_id, database):
        con = sqlite3.connect(database)
        cur = con.cursor()
        
        count_rows = cur.execute("SELECT COUNT(*) FROM budgeting WHERE user_id = ?;", (user_id, ))
        counted_rows = count_rows.fetchall()[0][0]

        if counted_rows != 0:
            budgeting = cur.execute("SELECT category, value, value_percent, date FROM budgeting WHERE user_id = ? ORDER BY DATE DESC LIMIT 5", (user_id,))
            budgeting_table_cents = budgeting.fetchall()
            con.close()

            budgeting_table_dollars = []

            for category, value, value_percent, date in budgeting_table_cents:
                value = value / 100
                budgeting_table_dollars.append((category, value, value_percent, date))

            return budgeting_table_dollars
        
        else:
            budgeting_table_dollars = [('daily spendings', 0.0, 0.0, '-'), ('large spendings', 0.0, 0.0, '-'), ('investments', 0.0, 0.0, '-'), ('education', 0.0, 0.0, '-'), ('others', 0.0, 0.0, '-')]
            return budgeting_table_dollars
    
    
    """Display last income"""
    @staticmethod
    def display_last_income(user_id, database):
        con = sqlite3.connect(database)
        cur = con.cursor()
        

        income = cur.execute("SELECT income FROM budgeting WHERE user_id = ? ORDER BY DATE DESC LIMIT 1", (user_id,))
        last_income_cents = income.fetchall()
        con.close()

        try:
            last_income_cents = last_income_cents[0][0]
            last_income_dollars = last_income_cents / 100

        except:
            last_income_dollars = 0.0

        return last_income_dollars
    

    """Change value from float to int - dollars to cents"""
    def float_to_int_value(self, value):
        value = value * 100
        value = int(value)

        return value
