from urllib.request import urlopen
import urllib
import json

import sqlite3

import argparse, sys

parser=argparse.ArgumentParser()

parser.add_argument('--file', help='Name of the file')
parser.add_argument('--name', help='Name of the job')


args=parser.parse_args()

# if args.file is null then exit
if not args.file:
    print("Please provide a name for the file with --file")
    sys.exit(1)

# if args.name is null then exit
if not args.name:
    print("Please provide a job name to pull from with --name")
    sys.exit(1)



f = open(args.file, "w")

# connect to database
conn = sqlite3.connect('repository.db')

cur = conn.cursor()

# select data from  database into a list
cur.execute("SELECT para FROM feature where process_name = '" + str(args.name) + "' and element NOT IN ('a', 'ol') order by parent_url, id")
url_to_process = cur.fetchall()

# convert list to a list of strings
url_to_process = [href[0] for href in url_to_process]

prompt = ""

# write header to file
f.write("prompt" + "\t" + "completion" + "\n")

# loop through list of urls to process and write to tab seperated file
for para in url_to_process:
    f.write(prompt + "\t" + para + "\n")


# close file
f.close()
conn.close()
print("Done")

