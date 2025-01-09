from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import urllib
import json

import sqlite3

import argparse, sys
parser=argparse.ArgumentParser()

parser.add_argument('--drop', help='Drop and rebuild the url table')
parser.add_argument('--name', help='Name of the job')
parser.add_argument('--url', help='URL to select children from')

args=parser.parse_args()


# if args.name is null then exit
if not args.name:
    print("Please provide a name for the job with --name")
    sys.exit(1)

if not args.url:
    print("Please provide a url for the job with --url")
    sys.exit(1)


# connect to postgres database
# import psycopg2
## conn = psycopg2.connect(host="localhost", database="hv", user="postgres", password="password")

conn = sqlite3.connect('repository.db')


# if args.truncate is Y or y or yes or Yes
if any(x in args.drop for x in ['Y','y','yes','Yes']):
    # truncate feature table
    # get input from the user if you are sure you want to truncate the feature table
    print("Are you sure you want to truncate the feature table?")
    user_input = input()
    if any(x in user_input for x in ['Y','y','yes','Yes']):
        # if yes, truncate the feature table
        conn.execute("DROP TABLE url")
        conn.execute("CREATE TABLE url (id INTEGER PRIMARY KEY AUTOINCREMENT, job_name TEXT, href TEXT, level INTEGER, process_time DATETIME DEFAULT CURRENT_TIMESTAMP)")
        conn.commit()


# function to get hrefs from a url
def get_hrefs(hrefset):
    hrefs = []
    for tophref in hrefset:
        # url = "https://help.hitachivantara.com/Documentation/Lumada/Lumada_Data_Catalog/7.1/Use_Data_Catalog/Data_Catalog_user_features"
        
        # try to open url and get html
        try:
            html = urlopen(tophref).read()
        except:
            print("Error opening url: " + tophref)
            continue
        
 
        rootSoup = BeautifulSoup(html, features="html.parser")
        for data in rootSoup.find_all("a", href=True): 
            href = data['href']
            if href.startswith('http'):
                # add to href to array
                hrefs.append(href)
                print(href)
                # insert into postgres database
                #cur = conn.cursor()
                #cur.execute("INSERT INTO feature(id, element, para, href, parent_url) VALUES(%s, %s, %s, %s, %s)", (id, element, para, href, url))
                #conn.commit()
    return hrefs

def load_href_to_table(hrefs, level):
    for href in hrefs:
        cur = conn.cursor()
        cur.execute("INSERT INTO url(job_name, href, level) VALUES(?, ?, ?)", (args.name, href, level))
        conn.commit()

# convert string to array
url_to_process = args.url.split(",")

# sample url
#url_to_process = ["https://help.hitachivantara.com/Documentation/Lumada/Lumada_Data_Catalog/7.1/Use_Data_Catalog/Data_Catalog_user_features"]

l1 = get_hrefs(url_to_process)
load_href_to_table(l1, 1)

l2 = get_hrefs(get_hrefs(url_to_process))
load_href_to_table(l2, 2)

#l3 = get_hrefs(get_hrefs(get_hrefs(url_to_process)))
#load_href_to_table(l2, 3)
print("Done")

