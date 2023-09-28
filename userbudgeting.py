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
    

    






