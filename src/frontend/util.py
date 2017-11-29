import re
import sys

#--------------------------------------------------------------------
# Encapsulation of common utilitarian functions
#--------------------------------------------------------------------
class Utility:
    #--------------------------------------------------------------------
    # Read in input from the console with a given message, appending the 
    # common input character. Prevent catch a crash if it reads in a EOF
    # and just have it exit instead
    #--------------------------------------------------------------------
    @staticmethod
    def getInput(msg):
        try:
            inp = raw_input(msg + " > ")
        except(EOFError):
            # End the program if we get an EOF
            sys.exit()
        
        return Utility.cleanString(inp)

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
    # Get and validate an account number from the user
    #--------------------------------------------------------------------
    @staticmethod
    def getAccountNumber(msg):
        inp = Utility.getInput(msg).strip()
        if len(inp) != 7 or not inp.isdigit() or inp[:1] == '0':
            Utility.error("Invalid account number")
            return None
        else:
            return inp

    #--------------------------------------------------------------------
    # Get and validate an amount from the user
    #--------------------------------------------------------------------
    @staticmethod
    def getAmount(loginType, msg):
        inp = Utility.getInput(msg).strip()
        if not inp.isdigit():
            Utility.error("Invlaid amount")
            return None
        amount = int(inp)
        if amount < 1:
            Utility.error("Invalid amount") #Urility
            return None
        if loginType == "machine" and amount > 100000:
            Utility.error("Amount cannot be over $1000 when logged in as machine")
            return None
        if amount > 99999999:
            Utility.error("Amount cannot be more than 8 digits")
            return None
        return inp

    #--------------------------------------------------------------------
    # Get and validate an account name from the user
    #--------------------------------------------------------------------
    @staticmethod
    def getAccountName(msg):
        inp = Utility.getInput(msg)
        if (len(inp) < 3):
            Utility.error("Account name must be at least 3 characters")
            return None
        elif (len(inp) > 30):
            Utility.error("Account name must be less than 30 characters")
            return None
        elif (re.match('^[a-zA-Z0-9 ]+$', inp) is None):
            Utility.error("Account name can only contain alphanumeric characters")
            return None
        elif (inp[0] == ' ' or inp[len(inp) - 1] == ' '):
            Utility.error("Account name cannot be prefixed or end in a space")
            return None
        else:
            return inp

