from userbudgeting import UserBudgeting
from userspendings import UserSpendings

class UserSummary(UserBudgeting, UserSpendings):

    """Displaying month budgeting into dictionary"""
    def change_display_budgeting_dictionary(self, user_id, database):
        current_budgeting = self.display_budgeting(user_id, database)
        income = self.display_last_income(user_id, database)

        try:
            month_budgeting_dictionary = {'daily_spendings': current_budgeting[0][1], 'large_spendings': current_budgeting[1][1], 'investments': current_budgeting[2][1], 'education': current_budgeting[3][1], 'others': current_budgeting[4][1], 'income': income}
        
        except:
            month_budgeting_dictionary = {'daily_spendings': 0.0, 'large_spendings': 0.0, 'investments': 0.0, 'education': 0.0, 'others': 0.0, 'income': income}

        return month_budgeting_dictionary


    """Difference between budgeting and spendings"""
    def balance_of_budgeting_spendings_month(self, user_id, database):
        month_spendings = self.sum_of_categories_from_current_month(user_id, database)
        month_budgeting = self.change_display_budgeting_dictionary(user_id, database)

        #cents to dollars
        daily_spendings = (month_budgeting["daily_spendings"] * 100 - month_spendings["daily_spendings"] * 100) / 100
        large_spendings = (month_budgeting["large_spendings"] *100 - month_spendings["large_spendings"] * 100) / 100
        investments = (month_budgeting["investments"] * 100 - month_spendings["investments"] * 100) / 100
        education = (month_budgeting["education"] * 100 - month_spendings["education"] * 100) / 100
        others = (month_budgeting["others"] * 100 - month_spendings["others"] * 100) / 100
        #difference between income and sum of categories
        total = (self.display_last_income(user_id, database) * 100 - month_spendings["total"] * 100) / 100

        balance = {'daily_spendings': daily_spendings, 'large_spendings': large_spendings, 'investments': investments, 'education': education, 'others': others, 'total': total}

        return balance