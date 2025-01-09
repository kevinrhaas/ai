from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

url = "https://help.hitachivantara.com/Documentation/Lumada/Lumada_Data_Catalog/Install"
html = urlopen(url).read()
soup = BeautifulSoup(html, features="html.parser")

# kill all script and style elements
#for script in soup(["script", "style"]):
#    script.extract()    # rip it out

# get text
#text = soup.get_text()

f = open("answers.jsonl", "w")



for data in soup.find_all(["p","li"]): 
    para = data.get_text().replace("\n", "  ")
    #para.replace("\n", " ")
    #print(repr(para))
    txt = re.sub('\s\s+', ' ', para)
    #print(repr(txt))
    print ('''{"text": "''', str(txt) , '''", "metadata": "none"}''')
    strout = '''{"text": "''' + str(txt) + '''", "metadata": "none"}''' + "\n"
    f.write(strout)

f.close()

# break into lines and remove leading and trailing space on each
#lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
#chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
#text = '\n'.join(chunk for chunk in chunks if chunk)

#for string in soup.stripped_strings:
#    print(string)



