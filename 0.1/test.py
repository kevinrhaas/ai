# get data from a database
# and write it to a csv file
# using the csv module

import csv
import sqlite3

# connect to the database
conn = sqlite3.connect('test.db')
c = conn.cursor()

# get the first record of the table monkey
c.execute('SELECT * FROM monkey')

# get the column names
col_names = [cn[0] for cx in c.description]




# loop through the column names and print them
for col in col_names:
    print col
