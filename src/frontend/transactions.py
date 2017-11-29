from fileio import FileIO

#--------------------------------------------------------------------
# Transaction container, exposes methods for adding different transactions to the in-memory list and then saving that list to the transaction file
#--------------------------------------------------------------------
class Transactions:
    def __init__(self, path): 
        self.path = path
        self.clear()

    #--------------------------------------------------------------------
    # Record a deposit
    #--------------------------------------------------------------------
    def deposit(self, account, amount):
        transaction = 'DEP ' + account + ' ' + amount + ' 0000000 ***'
        self._transactions.append(transaction)

    #--------------------------------------------------------------------
    # Record a withdrawl
    #--------------------------------------------------------------------
    def withdraw(self, account, amount):
        transaction = 'WDR ' + account + ' ' + amount + ' 0000000 ***'
        self._transactions.append(transaction)

    #--------------------------------------------------------------------
    # Record a transfer
    #--------------------------------------------------------------------
    def transfer(self, fromAccount, toAccount, amount):
        transaction = 'XFR ' + fromAccount + ' ' + amount + ' ' + toAccount + ' ***'
        self._transactions.append(transaction)

    #--------------------------------------------------------------------
    # Record an account creation
    #--------------------------------------------------------------------
    def createAccount(self, account, name):
        self._accountTransaction('NEW', account, name)

    #--------------------------------------------------------------------
    # Record an account deletion
    #--------------------------------------------------------------------
    def deleteAccount(self, account, name):
        self._accountTransaction('DEL', account, name)

    #--------------------------------------------------------------------
    # Internal function for common code between account creation and deletion
    #--------------------------------------------------------------------
    def _accountTransaction(self, prefix, account, name):
        transaction = prefix + ' ' + account + ' 000 0000000 ' + name
        self._transactions.append(transaction)

    #--------------------------------------------------------------------
    # Append the EOS transaction and write to disk
    #--------------------------------------------------------------------
    def finish(self): 
        self._transactions.append('EOS 0000000 000 0000000 ***')
        FileIO.writeLines(self.path, self._transactions)

    #--------------------------------------------------------------------
    # Clear the transfer file and clear our internal transfer buffer
    #--------------------------------------------------------------------
    def clear(self): 
        self._transactions = []
        FileIO.clear(self.path)
