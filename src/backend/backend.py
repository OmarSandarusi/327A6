#!/usr/bin/env python

#--------------------------------------------------------------------
# CMPE327 Assignment 4
# Jonathan Turcotte, Omar Sandarusi
# 1048455, 10097124
# 11JLT10, 12OZS
#--------------------------------------------------------------------

import argparse

from fileio   import FileIO
from commands import Commands
from util     import Utility

#--------------------------------------------------------------------
# Get the command line options
#--------------------------------------------------------------------
def getCommandArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("mergedtransactionfile")
    parser.add_argument("oldmasterfile")
    parser.add_argument("newmasterfile")
    parser.add_argument("newaccountsfile")
    return parser.parse_args()

#--------------------------------------------------------------------
# Parse a transaction file line into it's seperate parts
#--------------------------------------------------------------------
def parseLine(line):
    return Utility.cleanString(line).split(' ')

#--------------------------------------------------------------------
# Main
#--------------------------------------------------------------------

args     = getCommandArgs()
commands = Commands(args.oldmasterfile, args.newmasterfile, args.newaccountsfile)
lines    = FileIO.readLines(args.mergedtransactionfile)

for line in lines:
    parsed = parseLine(line)
    commands.runCommand(parsed[0], parsed[1], parsed[3], parsed[2], parsed[4])