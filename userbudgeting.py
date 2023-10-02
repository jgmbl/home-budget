import sqlite3
import datetime


FULL_PERCENTAGE = 100

class UserBudgeting:
    def __init__(self, value_income):
        self.value_income = value_income

    """Check if sum of percents is equal 100"""
    @staticmethod
    def check_sum_of_percent(*argv):
        sum_percent = 0

        for args in argv:
            sum_percent += args
        
        if sum_percent != FULL_PERCENTAGE:
            return False
        
        return True
    

    """Convert percent value to numerical value"""
    def __value_percent_to_value_budgeting(self, value_percent):
        value_numerical = value_percent / FULL_PERCENTAGE
        value_budgeting = value_numerical * self.value_income

        return value_budgeting
    

    """Add budgeting from form to table budgeting"""
    def add_budgeting_to_table(self, user_id, category, value_percent):

        value = self.__value_percent_to_value_budgeting(value_percent)
        date = datetime.datetime.now()
        date = date.strftime('%Y-%m-%d %H:%M')

        con = sqlite3.connect("instance/budget.db")
        cur = con.cursor()

        budgeting = cur.execute("INSERT INTO  budgeting(user_id, income, category, value, value_percent, date) VALUES (?, ?, ?, ?, ?, ?)", (user_id, self.value_income, category, value, value_percent, date))
        con.commit()
        con.close()





