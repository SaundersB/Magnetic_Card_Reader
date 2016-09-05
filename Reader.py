#Card Reader
import getpass
import datetime
import csv
import os
import sys

full_date = str(datetime.datetime.now())
short_date = full_date[5:10]
print(short_date)

while True:
    while True:
        try:
            ID = getpass.getpass(prompt = 'Please swipe your ID card. ')
            print(ID)
        except KeyboardInterrupt:
            sys.exit(1)