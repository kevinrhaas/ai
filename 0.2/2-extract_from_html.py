from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import urllib
import json

import sqlite3

import argparse, sys

parser=argparse.ArgumentParser()

parser.add_argument('--drop', help='Do the drop option')
parser.add_argument('--name', help='Name of the job')
parser.add_argument('--url', help='URL to select children from')

args=parser.parse_args()


# if args.name is null then exit
if not args.name:
    print("Please provide a name for the job with --name")
    sys.exit(1)

if not args.url:
    print("Please provide a url prefix for the job with --url")
    sys.exit(1)


# f = open("fine-tuning01.jsonl", "w")

# connect to  database
conn = sqlite3.connect('repository.db')

cur = conn.cursor()

# select data from postgres database into a list
cur.execute("SELECT distinct href FROM url where href like '" + args.url +"%'")
url_to_process = cur.fetchall()

# convert list to a list of strings
url_to_process = [href[0] for href in url_to_process]

print(url_to_process)

# if args.truncate is Y or y or yes or Yes
if any(x in args.drop for x in ['Y','y','yes','Yes']):
    # truncate feature table
    # get input from the user if you are sure you want to truncate the feature table
    print("Are you sure you want to truncate the feature table?")
    user_input = input()
    if any(x in user_input for x in ['Y','y','yes','Yes']):
        # if yes, truncate the feature table
        print("Dropping feature table")
        cur.execute("DROP TABLE feature")
        cur.execute("CREATE TABLE feature (key INTEGER PRIMARY KEY AUTOINCREMENT, id INTEGER, element TEXT, para TEXT, href TEXT, process_name TEXT, parent_url TEXT, process_time DATETIME DEFAULT CURRENT_TIMESTAMP)")
        conn.commit()


id = 0

# loop through list of urls to process
for href in url_to_process:

    if href.startswith('http'):
        print(href)
        try:
            html = urlopen(href).read()
        except urllib.error.URLError as e: 
            ResponseData = e.reason
            print("Error opening url: " + href)
            print(ResponseData)
            continue
        except urllib.error.HTTPError as e:
            if e.code == 403:
                continue
            else:
                print("Error opening url: " + href)
                continue
        soup = BeautifulSoup(html, features="html.parser")


        
        for data in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p", "ul", "ol", "a", "pre"]):
            id += 1 
            # get the type of html element in beautifulsoup
            element = data.name

            # print(id, data)

            # if element is a ul or ol parse the list
            if element == "ul" or element == "ol":
                para = ""
                for li in data.find_all("li"):
                    para += li.get_text() 
                    
                    # trim leading and trailing spaces from string
                    para = para.strip()
                    para += ", "

                # trim back the last 2 characters from string seperator
                para = para[:-2]
                para = para.replace("\n", " ")
            if element == "a":
                # get the href of the link
                link = data.get('href')
                # convert to string
                para = str(link)
                
            else:
                para = data.get_text()
                para = para.replace("\n", " ")
            
            #print(id, element, para)
         
            # compress the whitespace
            para = re.sub('\s\s+', ' ', para)

            #print(id, element, para)

            # remove unicode values from string 
            para = para.replace("\\u201", " ")
            para = para.replace("\\u00a0", " ")
            para = para.replace("\\u00a9", " ")
            para = para.replace("\\u00ae", " ")
            para = para.replace("\r.", "")


            #print(id, element, para, href)

            # insert into postgres database
            cur = conn.cursor()
            # print(id, element, para, href)
            cur.execute("INSERT INTO feature(id, element, para, href, process_name, parent_url) VALUES(?, ?, ?, ?, ?, ?)", (id, element, para, href, args.name, args.url))
            conn.commit()

        
            #print ('''{"prompt": "", "completion": ''', str(para) , '''}''')
            # strout = '''{"prompt": "", "completion": '''+ para + '''}''' + "\n"
            # print(strout)
            # f.write(strout)

    # if id = 2 exit for loop
    #if id >= 2:
    #    break

# f.close()

conn.close()
print("Done")
