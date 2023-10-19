from flask import session
import datetime
import sqlite3
import calendar

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
    

    """Add data to table savings"""
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


    """Sum of savings in current month"""
    @property
    def __sum_of_savings_current_month(self):
        user_id = session["_user_id"]

        today = datetime.datetime.today()
        current_month = today.strftime("%m")

        con = sqlite3.connect("instance/budget.db")
        cur = con.cursor()


        cur.execute("SELECT value FROM savings WHERE user_id = ? AND strftime('%m', date) = ?", (user_id, current_month))
        values_from_current_month = cur.fetchall()
        con.close()
        
        sum_of_values = 0
        for value in values_from_current_month:
            sum_of_values += value[0]

        return sum_of_values


    """Return total sum of savings"""
    @property
    def __total_sum_of_savings(self):
        user_id = session["_user_id"]

        con = sqlite3.connect("instance/budget.db")
        cur = con.cursor()

        cur.execute("SELECT value_summary FROM savings WHERE user_id = ? ORDER BY id DESC LIMIT 1", (user_id, ))
        total_sum_savings = cur.fetchall()

        con.close()

        return total_sum_savings[0][0]


    """Return dictionary of month savings information"""
    @property
    def display_current_month_information(self):
        current_month_name = calendar.month_name[datetime.datetime.today().month]

        try:
            current_month_information = {"month": current_month_name, "value": round(self.__sum_of_savings_current_month, 2), "value_total": round(self.__total_sum_of_savings, 2)}

        except:
            current_month_information = {"month": current_month_name, "value": round(0, 2), "value_total": round(0, 2)}

        return current_month_information


    """Display all history from savings"""
    def display_data_table_savings(self):
        #user_id = session["_user_id"]
        user_id = 1

        con = sqlite3.connect("instance/budget.db")
        cur = con.cursor()

        cur.execute("SELECT value, value_summary, date FROM savings WHERE user_id = ?", (user_id, ))
        data_from_table = cur.fetchall()

        con.close()

        return data_from_table