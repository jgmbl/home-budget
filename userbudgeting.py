class UserBudgeting:
    """Check if sum of percents is equal 100"""
    @staticmethod
    def check_sum_of_percent(*argv):
        sum_percent = 0

        for args in argv:
            sum_percent += args
        
        if sum_percent != 100:
            return False
        
        return True


