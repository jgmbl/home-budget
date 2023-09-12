from datetime import datetime
import calendar
import bcrypt
import hashlib
import sqlite3 as sql


class HomeBudget:
    def __init__(self):
        self.current_day = datetime.now().day
        self.current_month = datetime.now().month
        self.current_year = datetime.now().year


    def current_date(self):
        """Returns a tuple with day(int), month(string), year(int)"""

        return self.current_day, calendar.month_name[self.current_month], self.current_year
    

    def last_month(self):
        """Returns a list of days in month to current day"""
        #[[day, month, year]]

        month_days = calendar.monthcalendar(self.current_year, self.current_month)
        
        month_day = []
        month_all_days = []

        for week in month_days:
            for day in week:
                if day != 0 and self.current_day >= day:
                    month_day = [day, calendar.month_name[self.current_month], self.current_year]
                    month_all_days.append(month_day)
        
        return month_all_days
    

    def last_week(self):
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
            if day <= self.current_day:
                week_single_day = [day, calendar.month_name[self.current_month], self.current_year]
                week_all_days.append(week_single_day)

        return week_all_days
    

class Users:
    def __init__(self):
        self.username = ""
        self.password = ""


    def __hash_password(self):
        word = hashlib.sha256(self.password.encode('utf-8')).hexdigest()
        hashed = bcrypt.hashpw(word.encode('utf-8'), bcrypt.gensalt())
        return hashed


    def insert_db(self):
        con = sql.connect('budget.db')
        c =  con.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?);", (self.username, self.__hash_password()))
        con.commit()


    def display_db(self):
        con = sql.connect('budget.db')
        c =  con.cursor()
        c.execute("SELECT * FROM users;")
        database= c.fetchall()

        return database