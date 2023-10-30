from userbudgeting import UserBudgeting
from userspendings import UserSpendings

class UserSummary(UserBudgeting, UserSpendings):

    """Displaying month budgeting into dictionary"""
    def change_display_budgeting_dictionary(self, user_id, database):
        current_budgeting = self.display_budgeting(user_id, database)
        income = self.display_last_income(user_id, database)

        month_budgeting_dictionary = {'daily_spendings': current_budgeting[0][1], 'large_spendings': current_budgeting[1][1], 'investments': current_budgeting[2][1], 'education': current_budgeting[3][1], 'others': current_budgeting[4][1], 'income': income}
        

        return month_budgeting_dictionary


    """Difference between budgeting and spendings"""
    def balance_of_budgeting_spendings_month(self, user_id, database):
        month_spendings = self.sum_of_categories_from_current_month(user_id, database)
        month_budgeting = self.change_display_budgeting_dictionary(user_id, database)

        daily_spendings = month_budgeting["daily_spendings"] - month_spendings["daily_spendings"]
        large_spendings = month_budgeting["large_spendings"] - month_spendings["large_spendings"]
        investments = month_budgeting["investments"] - month_spendings["investments"]
        education = month_budgeting["education"] - month_spendings["education"]
        others = month_budgeting["others"] - month_spendings["others"]
        #difference between income and sum of categories
        total = self.display_last_income(user_id, database) - month_spendings["total"]

        balance = {'daily_spendings': daily_spendings, 'large_spendings': large_spendings, 'investments': investments, 'education': education, 'others': others, 'total': total}

        return balance

