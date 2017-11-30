from fileio import FileIO
from account import Account
from util import Utility
#--------------------------------------------------------------------
# Encapulation for the list of accounts and operations on the list
#--------------------------------------------------------------------
class Accounts:
    #--------------------------------------------------------------------
    # Load the master accounts file and construct the accounts list
    #--------------------------------------------------------------------
    def __init__(self, oldMasterFile, newMasterFile, accountsFile):
        lines = FileIO.readLines(oldMasterFile)
        self.newMasterFile = newMasterFile
        self.accountsFile = accountsFile
        self.list = []
        count = 0
        for line in lines:
            line = line.strip("\r\n ")
            params = line.split(' ')

            if (len(params) != 3):
                Utility.fatal("Line " + str(count) + " is invalid - parameter count != 3")

            self.list.append(Account(int(params[0]), int(params[1]), params[2]))
            count += 1

    #--------------------------------------------------------------------
    # Add an account
    #--------------------------------------------------------------------
    def addAccount(self, number, name): #number and balance have to be int
        if self.getAccountByNumber(number) is not None:
            Utility.log('Account already exists for account: ' + number)
        else:
            self.list.append(Account(int(number), 0, name))

    #--------------------------------------------------------------------
    # Get an account by its number
    #--------------------------------------------------------------------
    def getAccountByNumber(self, number):
        number = int(number)
        for account in self.list:
            if account.number == number:
                return account
        return None

    #--------------------------------------------------------------------
    # Get an account by its name
    #--------------------------------------------------------------------
    def getAccountByName(self, name):
        for account in self.list:
            if account.name == name:
                return account
        return None

    #--------------------------------------------------------------------
    # Delete an account
    #--------------------------------------------------------------------
    def deleteAccount(self, number, name):
        number = int(number)

        acct = self.getAccountByNumber(number)
        if acct is None:
            Utility.log('Aborting delete, account does not exist: ' + number)
            return

        if acct.balance != 0:
            Utility.log('Aborting delete, account balance is not zero: ' + number)
        elif acct.name != name:
            Utility.log('Aborting delete, account names do not match: ' + name + ' / ' + acct.name)
        else:
            for i, account in enumerate(self.list):
                if account.number == number:
                    del self.list[i]
                    break

    #--------------------------------------------------------------------
    # Deposit an amount to an account
    #--------------------------------------------------------------------
    def deposit(self, number, amount):
        number = int(number)
        amount = int(amount)

        acct = self.getAccountByNumber(number)
        if acct is None:
            Utility.log('Aborting deposit, account does not exist: ' + number)
            return
        acct.balance += amount
    
    #--------------------------------------------------------------------
    # Withdraw an amount from an account
    #--------------------------------------------------------------------
    def withdraw(self, number, amount):
        number = int(number)
        amount = int(amount)

        acct = self.getAccountByNumber(number)
        if acct is None:
            Utility.log('Aborting withdrawal, account does not exist: ' + number)
            return
        if acct.balance < amount:
            Utility.log('Aborting withdrawal, the account does not have enough funds: ' + number)
        else:
            acct.balance -= amount
    
    #--------------------------------------------------------------------
    # Transfer an amount between the two accounts
    #--------------------------------------------------------------------
    def transfer(self, fromNumber, toNumber, amount):
        fromNumber = int(fromNumber)
        toNumber = int(toNumber)
        amount = int(amount)

        fromAcct = self.getAccountByNumber(fromNumber)
        toAcct   = self.getAccountByNumber(toNumber)

        if fromAcct is None:
            Utility.log('Aborting transfer, account does not exist: ' + str(fromNumber))
        elif toAcct is None:
            Utility.log('Aborting transfer, account does not exist: ' + str(toNumber))
        elif fromNumber == toNumber:
            Utility.log('Aborting transfer, cannot transfer between the same accounts: ' + str(fromNumber) + '/' + str(toNumber))
        elif fromAcct.balance < amount:
            Utility.log('Aborting transfer, not enough funds in the source account: ' + str(fromNumber))
        else:
            fromAcct.balance -= amount
            toAcct.balance   += amount
        return

    #--------------------------------------------------------------------
    # Sort list and output the master and valid account files
    #--------------------------------------------------------------------
    def finish(self): #sort and write
        self.list = self.mergesort(self.list) 
        validAccounts = []
        master = []

        for account in self.list:
            validAccounts.append(str(account.number))

            # Format the balance to be at least three numbers
            if (account.balance == 0):
                balance = '000'
            else :
                balance = str(account.balance)
                if (len(balance) == 1):
                    balance = '00' + balance
                elif (len(balance) == 2):
                    balance = '0' + balance
                
            master.append('' + str(account.number) + ' ' + balance + ' ' + account.name)
        
        # Append the all zero account number to validAccounts
        validAccounts.append('0000000')
        
        FileIO.writeLines(self.newMasterFile, master)
        FileIO.writeLines(self.accountsFile, validAccounts)

    #--------------------------------------------------------------------
    # Sort accounts by their account number
    #--------------------------------------------------------------------
    def mergesort(self, accounts):
        if (len(accounts) == 1 or len(accounts) == 0):
            return accounts

        mid = len(accounts) / 2
        
        l = self.mergesort(accounts[:mid])
        r = self.mergesort(accounts[mid:])

        return self.merge(l, r)

    #--------------------------------------------------------------------
    # Merge two lists of accounts by order of account number
    #--------------------------------------------------------------------
    def merge(self, left, right):
        res = []
        i = 0
        j = 0

        while (i < len(left) and j < len(right)):
            if(left[i].number < right[j].number):
                res.append(left[i])
                i += 1
            else:
                res.append(right[j])
                j += 1

        while (i < len(left)):
            res.append(left[i])
            i += 1

        while (j < len(right)):
            res.append(right[j])
            j += 1
        
        return res