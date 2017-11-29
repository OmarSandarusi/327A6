#!/usr/bin/env python

#--------------------------------------------------------------------
# CMPE327 Assignment 3
# Jonathan Turcotte, Omar Sandarusi
# 1048455, 10097124
# 11JLT10, 12OZS
#--------------------------------------------------------------------

import sys
import argparse
from fileio import FileIO
from commands import Commands
from util import Utility

#--------------------------------------------------------------------
# Get the command line options
#--------------------------------------------------------------------
def commandArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("accountfile")
    parser.add_argument("transactionfile")
    return parser.parse_args()

#--------------------------------------------------------------------
# Get a command from the user, and verify that it's valid
#--------------------------------------------------------------------
def getCommand():
    while (True):
        inp = Utility.getInput("").lower()

        if (validCommand(inp)):
            return inp            
        else:
            print("Input a valid command")
            
#--------------------------------------------------------------------
# Validate that this is a valid command
#--------------------------------------------------------------------
def validCommand(inp):
    if (inp in Commands.VALID_COMMANDS):
        return True
    else:
        return False

#--------------------------------------------------------------------
# Read in the given accounts file
#--------------------------------------------------------------------
def readAccounts(path):
    lines   = FileIO.readLines(path)
    cleaned = []
    
    if len(lines) < 1:
        raise ValueError('Empty Accounts File')

    # Clean and strip newlines from the numbers, then
    # ensure that they're valid account numbers
    for line in lines:
        clean = Utility.cleanString(line)
        if (not clean.isdigit() or len(clean.strip()) != 7 or (
            clean != lines[-1].strip() and clean[0] == '0')):
            raise ValueError('Invalid accounts file, error: ' + clean)
        cleaned.append(clean)
    
    # Ensure that the last line is the all zero account number
    if (cleaned[-1] != "0000000"):
        raise ValueError('Invalid accounts file, missing zero account number at file end')

    return cleaned

#--------------------------------------------------------------------
# Main
#--------------------------------------------------------------------

# Get the commandline arguments
args = commandArgs()

# Read in the accounts file
try:
    accounts = readAccounts(args.accountfile)
except ValueError as e:
    print e.message
    FileIO.writeLines(args.transactionfile, ['EOS 0000000 000 0000000 ***'])
    sys.exit()

# Instantiate our commands object
commands = Commands(accounts, args.transactionfile)

print("\n############")
print(" FRONT END")
print("############\n")

while(True):
    commands.runCommand(getCommand())