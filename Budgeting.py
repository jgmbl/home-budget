class Budgeting:
    @staticmethod
    def check_correct_percent(percent):
        if percent >= 0 and percent <= 100:
            return True
        
        else:
            return False
        

budgeting = Budgeting()
print(Budgeting.check_correct_percent(85))

