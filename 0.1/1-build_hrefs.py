from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import urllib
import json

# f = open("fine-tuning01.jsonl", "w")

# connect to postgres database
import psycopg2
conn = psycopg2.connect(host="localhost", database="hv", user="postgres", password="password")

cur = conn.cursor()
cur.execute("TRUNCATE TABLE url")
conn.commit()

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
        cur.execute("INSERT INTO url(href, level, process_time) VALUES(%s, %s, NOW())", (href, level))
        conn.commit()


url_to_process = ["https://help.hitachivantara.com/Documentation/Lumada/Lumada_Data_Catalog/7.1/Use_Data_Catalog/Data_Catalog_user_features"]

l1 = get_hrefs(url_to_process)
load_href_to_table(l1, 1)

l2 = get_hrefs(get_hrefs(url_to_process))
load_href_to_table(l2, 2)

#l3 = get_hrefs(get_hrefs(get_hrefs(url_to_process)))
#load_href_to_table(l2, 3)
print("Done")

