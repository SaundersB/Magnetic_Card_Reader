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
import os
import sys
import sqlite3
import re

primary_account_pattern = r"(%[A-z][0-9]+[\^])"      # Pattern to match the primary account followed by the format code.
name_pattern = r"([\^][A-z|\s]+[\/][A-z|\s]+[\^])"              # Provides the account's user name.
additional_primary_account = r"([\?][\;][0-9]+[=])"             # I've found that many times this returns the same thing as the primary account number.
additional_data_pattern = r"([=][0-9]+[\?])"                            # If Track 1 layout is used, this will return None.


class MagneticReader():
    def __init__(self):
        self.conn = None
        self.c = None
        self.name = None
        self.account_number = None
        self.additional_data = None


    def establish_data_base(self):
        """ This function will create a new database file if it does not exist. """
        self.conn = sqlite3.connect('magnetic_entries.db')
        self.c = self.conn.cursor()

    def create_table(self):
        """" 
        This function will create an entries table in the database.
        WARNING: If the table exists we'll raise an exception.
         """
        self.c = self.conn.cursor()
        try:
            self.c.execute('''
                    CREATE table entries 
                    (date varchar(250) PRIMARY KEY NOT NULL, name varchar(250) NOT NULL, primary_account_number varchar(250) NOT NULL, additional_data varchar(250) NOT NULL)
                    ''')
            print("Creating table entries.")
        except sqlite3.Error as error:
            print(error)

    def insert_row(self, name, primary_account_number, additional_data):
        print("Inserting values into row of database.")
        date = str(self.return_date_string())
        self.c.execute("insert into entries values(?, ?, ?, ?)", (date, name, primary_account_number, additional_data,))
        self.conn.commit()

    def return_date_string(self):
        full_date = str(datetime.datetime.now())
        short_date = full_date[5:10]
        return full_date

    def search_pattern(self, pattern, data):
        compiled_pattern = re.compile(pattern)
        match = compiled_pattern.search(data)
        if(match != None):
            return match.group(0)

    def match_pattern(self, pattern, data):
        """
        If zero or more characters at the beginning of string match this regular expression, 
        return a corresponding match object. Return None if the string does not match the pattern; 
        note that this is different from a zero-length match.
        """
        compiled_pattern = re.compile(pattern)
        match = compiled_pattern.match(data)
        if(match != None):
            return match.group(0)

    def obtain_user_data(self, data):
        # Search string data for intended patterns.
        primary_account = self.search_pattern(primary_account_pattern, data)
        name = self.search_pattern(name_pattern, data)
        additional_data = self.search_pattern(additional_data_pattern, data)

        self.clean_string_data(primary_account, name, additional_data)

    def clean_string_data(self, primary_account, name, additional_data):
        # Remove excess symbols.
        if(primary_account is not None):
            primary_account = primary_account.replace("^","")
            primary_account = primary_account.replace("%","")
            self.primary_account = primary_account

        if(name is not None):
            name = name.replace("^","")
            name = name.replace(" ","")
            self.name = name

        if(additional_data is not None):
            additional_data = additional_data.replace("?","")
            additional_data = additional_data.replace("=","")
            self.additional_data = additional_data


    def listen_for_magnetic_swipe(self):
        while True:
            while True:
                try:
                    ID = getpass.getpass(prompt = 'Please swipe your ID card. ')
                    print(ID)
                    self.obtain_user_data(ID)
                    self.insert_row(self.name, self.primary_account, self.additional_data)
                except KeyboardInterrupt:
                    sys.exit(1)



if __name__ == '__main__':
    reader = MagneticReader()
    reader.establish_data_base()
    reader.create_table()
    reader.listen_for_magnetic_swipe()











