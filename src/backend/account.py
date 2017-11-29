#--------------------------------------------------------------------
# Object representing a single account
#--------------------------------------------------------------------
class Account:
    def __init__(self, number, balance, name):
        self.number = number
        self.balance = balance
        self.name = name