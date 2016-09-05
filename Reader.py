#!/bin/python
# Brandon Saunders
# Magnetic Card Reader
'''
This is a simple script to read data from a magnetic card reader utilizing the track 1 and 2 protocols. 


Data Syntax:

Track 2 ("American Banking Association,") is currently most commonly used, though credit card companies have been pushing for everyone to move to Track 1. This is the track that is read by ATMs and credit card checkers. The ABA designed the specifications of this track and all world banks must abide by it. It contains the cardholder's account, encrypted PIN, plus other discretionary data.
*** Track 1 Layout: ***     

             | SS | FC |  PAN  |   Name   | FS |  Additional Data | ES | LRC |

 SS=Start Sentinel "%"
 FC=Format Code
 PAN=Primary Acct. # (19 digits max)
 FS=Field Separator "^"
 Name=26 alphanumeric characters max.
 Additional Data=Expiration Date, offset, encrypted PIN, etc.
 ES=End Sentinel "?"
 LRC=Longitudinal Redundancy Check


   *** Track 2 Layout: ***

           | SS |  PAN  | FS |  Additional Data  | ES | LRC |

 SS=Start Sentinel ";"
 PAN=Primary Acct. # (19 digits max)
 FS=Field Separator "="
 Additional Data=Expiration Date, offset, encrypted PIN, etc.
 ES=End Sentinel "?"
 LRC=Longitudinal Redundancy Check 


   *** Track 3 Layout: **  Similar to tracks 1 and 2.  Almost never used.
                           Many different data standards used.

'''
import getpass
import datetime
import csv
import os
import sys
import sqlite3
import re

OPEN_BRACKET = '['
CLOSE_BRACKET = ']'
DIGIT = '[0-9]'
LETTER = '[a-Z]'

START_SENTINEL = '%'
TRACK_ONE_FIELD_SEPARATOR = '[^]'
END_SENTINEL = '[?]'
LONGITUDINAL_REDUNDANCY_CHECK = ""
WILDCARD = '[*]'

SEMICOLON = ';'

TRACK_TWO_FIELD_SEPARATOR = "[=]"

TEST = START_SENTINEL + LETTER + WILDCARD + DIGIT 
primary_account_pattern = r"(%[A-z][0-9]+[\^][A-z]+[\/]+)"
name_pattern = r"([\^][A-z|\s]+[\/][A-z|\s]+[\^])"

TRACK_TWO = START_SENTINEL + LETTER + WILDCARD + DIGIT + TRACK_TWO_FIELD_SEPARATOR + DIGIT + WILDCARD + END_SENTINEL

conn = None
c = None

def establish_data_base():
    global conn
    conn = sqlite3.connect('magnetic_entries.db')

def create_table():
    global conn
    c = conn.cursor()
    c.execute('''
            CREATE table entries 
            (id INTEGER PRIMARY KEY ASC, name varchar(250) NOT NULL, card_number INTEGER NOT NULL, primary_account_number varchar(250) NOT NULL, additional_data varchar(250) NOT NULL, longitudinal_redundancy_check varchar(250) NOT NULL)
            ''')

def insert_row(name, card_number, primary_account_number, additional_data):
    global conn
    c.execute('''
          INSERT INTO person VALUES(1, 'name', 'card_number', 'primary_account_number', 'additional_data')
          ''')


def return_date_string():
    full_date = str(datetime.datetime.now())
    short_date = full_date[5:10]
    print(short_date)
    return short_date


def search_pattern(pattern, data):
    print("Pattern: " + pattern)
    print("String: " + data)
    compiled_pattern = re.compile(pattern)
    match = compiled_pattern.search(data)
    if(match != None):
        print(match.group(0))



def match_pattern(pattern, data):
    """
    If zero or more characters at the beginning of string match this regular expression, 
    return a corresponding match object. Return None if the string does not match the pattern; 
    note that this is different from a zero-length match.
    """
    print("Pattern: " + pattern)
    print("String: " + data)
    compiled_pattern = re.compile(pattern)
    match = compiled_pattern.match(data)
    if(match != None):
        print(match.group(0))

def listen_for_magnetic_swipe():
    while True:
        while True:
            try:
                ID = getpass.getpass(prompt = 'Please swipe your ID card. ')
                print(ID)
                search_pattern(name_pattern,ID)
            except KeyboardInterrupt:
                sys.exit(1)



if __name__ == '__main__':
    establish_data_base()
    #create_table()
    listen_for_magnetic_swipe()











