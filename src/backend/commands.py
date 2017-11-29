import sys

from util     import Utility
from accounts import Accounts

#--------------------------------------------------------------------
# Contains command-specific infomation and the functions that run each command, eg. login, createacct, etc..
#--------------------------------------------------------------------
class Commands:
    # Enumeration of valid commands
    VALID_COMMANDS = [
        'DEP',
        'WDR',
        'XFR',
        'NEW',
        'DEL',
        'EOS'
    ]

    # Enumeration of Unused values
    Unused = {
        'account' : '0000000',
        'amount'  : '000',
        'name'    : '***'
    }

    def __init__(self, oldMasterFile, newMasterFile, accountsFile): 
        self.lastCommand = ''
        self.accounts = Accounts(oldMasterFile, newMasterFile, accountsFile)

    #--------------------------------------------------------------------
    # EOS
    #--------------------------------------------------------------------
    def EOS(self, account1, account2, amount, name):
        if account1 != self.Unused['account'] or account2 != self.Unused['account']:
            Utility.fatal('Invalid account number(s) in EOS command' + account1 + ' / ' + account2)
        elif amount != self.Unused['amount']:
            self.fatalAmount('EOS', amount)
        elif name != self.Unused['name']:
            self.fatalAccountName('EOS', name)
        else:
            # If this is the second EOS in a row, exit
            if self.lastCommand == 'EOS':
                self.accounts.finish()
                sys.exit()

    #--------------------------------------------------------------------
    # Createacct
    #--------------------------------------------------------------------
    def NEW(self, account1, account2, amount, name):
        Utility.checkAccountNumber(account1)
        Utility.checkAccountName(name)
        if account2 != self.Unused['account']:
            self.fatalAccountNumber('NEW', account2)
        elif amount != self.Unused['amount']:
            self.fatalAmount('NEW', amount)

        acct = self.accounts.getAccountByNumber(account1)
        if acct is not None:
            Utility.log('Account number already exists.')
        else:
            self.accounts.addAccount(account1, name)
    #--------------------------------------------------------------------
    # Deleteacct
    #--------------------------------------------------------------------
    def DEL(self, account1, account2, amount, name):
        Utility.checkAccountNumber(account1)
        Utility.checkAccountName(name)

        if account2 != self.Unused['account']:
            self.fatalAccountNumber('DEL', account2)
        elif amount != self.Unused['amount']:
            self.fatalAmount('DEL', amount)
        else:
            self.accounts.deleteAccount(account1, name)

    #--------------------------------------------------------------------
    # Withdraw
    #--------------------------------------------------------------------
    def WDR(self, account1, account2, amount, name):
        Utility.checkAccountNumber(account1)
        Utility.checkAmount(amount)

        if account2 != self.Unused['account']:
            self.fatalAccountNumber('WDR', account2)
        elif name != self.Unused['name']:
            self.fatalAccountName('WDR', name)
        else:
            self.accounts.withdraw(account1, amount)

    #--------------------------------------------------------------------
    # Deposit
    #--------------------------------------------------------------------
    def DEP(self, account1, account2, amount, name):
        Utility.checkAccountNumber(account1)
        Utility.checkAmount(amount)

        if account2 != self.Unused['account']:
            self.fatalAccountNumber('DEP', account2)
        elif name != self.Unused['name']:
            self.fatalAccountName('DEP', name)
        else:
            self.accounts.deposit(account1, amount)

    #--------------------------------------------------------------------
    # Transfer
    #--------------------------------------------------------------------
    def XFR(self, account1, account2, amount, name):
        Utility.checkAccountNumber(account1)
        Utility.checkAccountNumber(account2)
        Utility.checkAmount(amount)

        if name != self.Unused['name']:
            self.fatalAccountName('XFR', name)
        self.accounts.transfer(account1, account2, amount)

    #--------------------------------------------------------------------
    # Dispatcher function that ensures it is a valid command
    #--------------------------------------------------------------------
    def runCommand(self, cmd, account1, account2, amount, name):
        if cmd not in Commands.VALID_COMMANDS:
            raise ValueError('Invalid command code: ' + cmd)
        else:
            getattr(Commands, cmd)(self, account1, account2, amount, name)
            self.lastCommand = cmd

    #--------------------------------------------------------------------
    # Helper functions for creating fatal errors
    #--------------------------------------------------------------------
    def fatalAccountNumber(self, command, number):
        Utility.fatal('Invalid account number in ' + command + ' command: ' + number)
 
    def fatalAccountName(self, command, name):
        Utility.fatal('Invalid account name in ' + command + ' command: ' + name)
 
    def fatalAmount(self, command, amount):
        Utility.fatal('Invalid amount in ' + command + ' command: ' + amount) 