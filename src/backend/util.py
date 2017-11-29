import re
import sys
import os
from fileio import FileIO

#--------------------------------------------------------------------
# Encapsulation of common utilitarian functions
#--------------------------------------------------------------------
class Utility:
    errorPath = os.path.join(sys.path[0], 'error.txt')

    #--------------------------------------------------------------------
    # Decode any UTF strings to ASCII, and strip any newlines
    #--------------------------------------------------------------------
    @staticmethod
    def cleanString(string):
        return string.decode('unicode_escape').encode('ascii', 'ignore').strip("\r\n").strip("\n")

    #--------------------------------------------------------------------
    # Write an error to the console
    #--------------------------------------------------------------------
    @staticmethod
    def error(msg):
        print("Error: " + msg)

    #--------------------------------------------------------------------
    # Validate an account number
    #--------------------------------------------------------------------
    @staticmethod
    def checkAccountNumber(num):
        if len(num) != 7:
            Utility.fatal("Account number must be length 7: " + num)
        elif not num.isdigit():
            Utility.fatal("Account number not all digits: " + num)
        elif num[:1] == '0':
            Utility.fatal("Account number cannot begin with 0: " + num)

    #--------------------------------------------------------------------
    # Validate an amount
    #--------------------------------------------------------------------
    @staticmethod
    def checkAmount(amount):
        if not amount.isdigit():
            Utility.fatal("Amount is not digits: " + amount)
        elif len(amount) < 3:
            Utility.fatal("Amount not padded to three length: " + amount)

        num = int(amount)
        if num < 1:
            Utility.fatal("Amount must be 1 or greater: " + amount)

    #--------------------------------------------------------------------
    # Validate an account name
    #--------------------------------------------------------------------
    @staticmethod
    def checkAccountName(name):
        if (len(name) < 3):
            Utility.fatal("Account name must be at least 3 characters: " + name)
        elif (len(name) > 30):
            Utility.fatal("Account name must be less than 30 characters: " + name)
        elif (re.match('^[a-zA-Z0-9 ]+$', name) is None):
            Utility.fatal("Account name can only contain alphanumeric characters: " + name)
        elif (name[0] == ' ' or name[len(name) - 1] == ' '):
            Utility.fatal("Account name cannot be prefixed or end in a space: " + name)

    #--------------------------------------------------------------------
    # Logs the error to the error file and the console
    #--------------------------------------------------------------------
    @staticmethod
    def log(msg):
        FileIO.appendLine(Utility.errorPath, msg + '\n')
        Utility.error(msg)

    #--------------------------------------------------------------------
    # Calls Utility.log and then raises an error with the message
    #--------------------------------------------------------------------
    @staticmethod    
    def fatal(msg):
        Utility.log(msg)
        raise ValueError(msg)