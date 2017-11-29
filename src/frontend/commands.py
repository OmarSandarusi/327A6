from util import Utility
from transactions import Transactions

#--------------------------------------------------------------------
# Contains command-specific infomation and the functions that run each command, eg. login, createacct, etc..
#--------------------------------------------------------------------
class Commands:
    # Enumeration of valid commands
    VALID_COMMANDS = [
        'login',
        'logout',
        'createacct',
        'deleteacct',
        'deposit',
        'withdraw',
        'transfer']

    def __init__(self, accounts, transactionfile): 
        self.loginType = ""     
        self.accounts  = accounts
        self.deletedAccounts = []
        self.sessionWithdraw = 0
        self.transactions = Transactions(transactionfile)

    #--------------------------------------------------------------------
    # Login command
    #--------------------------------------------------------------------
    def login(self):
        inp = Utility.getInput("Machine or agent").lower()

        if (inp not in ["machine", "agent"]):
            Utility.error("Not a valid login type.")
        else:
            self.loginType = inp
            self.transactions.clear()
            print("Logged in as " + str(self.loginType))

    #--------------------------------------------------------------------
    # Logout command
    #--------------------------------------------------------------------
    def logout(self):
        self.loginType = ""
        self.transactions.finish()
        print("Logged out")

    #--------------------------------------------------------------------
    # Createacct command
    #--------------------------------------------------------------------
    def createacct(self):
        if (self.loginType != "agent"):
            Utility.error("Only available in privileged mode")
            return

        num  = Utility.getAccountNumber("Enter the account number of the new account")
        if (num == None):
            return
        elif (num in self.accounts):
            Utility.error("That account number already exists.")
            return
        elif (num in self.deletedAccounts):
            Utility.error("That account was deleted.")
            return

        name = Utility.getAccountName("Enter the name of the new account")
        if (name == None):
            return

        self.transactions.createAccount(num, name)

    #--------------------------------------------------------------------
    # Deleteacct command
    #--------------------------------------------------------------------
    def deleteacct(self):
        if (self.loginType != "agent"):
            Utility.error("Only available in privileged mode")
            return

        num  = Utility.getAccountNumber("Enter the account number of the account to delete")
        if (num == None):
            return
        
        name = Utility.getAccountName("Enter the name of the account to delete")
        if (name == None):
            return

        # Validate that the account number exists
        if (not num in self.accounts):
            Utility.error("That account number is not valid")
        else:
            self.accounts.remove(num)
            self.deletedAccounts.append(num)
            self.transactions.deleteAccount(num, name)

    #--------------------------------------------------------------------
    # Withdraw command
    #--------------------------------------------------------------------
    def withdraw(self):
        account = Utility.getAccountNumber("Account #")
        if account is None:
            return
        if account not in self.accounts:
            Utility.error("Account does not exist")
            return

        amount = Utility.getAmount(self.loginType, "Amount in cents")
        if amount is None:
            return

        numAmount = int(amount)
        if (self.sessionWithdraw + numAmount > self.getWithdrawLimit()):
            Utility.error("This withdrawal would exceed your total allowed sum.")
            return
        
        self.sessionWithdraw += numAmount
        self.transactions.withdraw(account, amount)

    #--------------------------------------------------------------------
    # Deposit command
    #--------------------------------------------------------------------
    def deposit(self):
        account = Utility.getAccountNumber("Account #")
        if account is None:
            return
        if account not in self.accounts:
            Utility.error("Account does not exist")
            return

        amount = Utility.getAmount(self.loginType, "Amount in cents")
        if amount is None:
            return

        self.transactions.deposit(account, amount)

    #--------------------------------------------------------------------
    # Transfer command
    #--------------------------------------------------------------------
    def transfer(self):
        fromAccount = Utility.getAccountNumber("From account #")
        if fromAccount is None:
            return
        if not fromAccount in self.accounts:
            Utility.error("Account does not exist")
            return

        toAccount = Utility.getAccountNumber("To account #")
        if toAccount is None:
            return
        if not toAccount in self.accounts:
            Utility.error("Account does not exist")
            return

        if (fromAccount == toAccount):
            Utility.error("Cannot transfer from and to the same account.")
            return

        amount = Utility.getAmount(self.loginType, "Amount to transfer in cents")
        if amount is None:
            return

        self.transactions.transfer(fromAccount, toAccount, amount)

    #--------------------------------------------------------------------
    # Dispatcher function that wraps command calls with error checking logic
    #--------------------------------------------------------------------
    def runCommand(self, cmd):
        if (cmd != 'login' and self.loginType == ""):
            Utility.error("You must be logged in first")
        else:
            getattr(Commands, cmd)(self)

    #--------------------------------------------------------------------
    # Returns the withdrawal limit depending on the session type
    #--------------------------------------------------------------------
    def getWithdrawLimit(self):
        if (self.loginType == "machine"):
            return 100000
        else:
            return 99999999