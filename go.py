# 8Chan Scraper
# Written by @sednawk and @dade0
#

import requests
import urllib
import urlparse
from bs4 import BeautifulSoup
import sys
import os

allowed_files = ['webm', 'jpg', 'jpeg', 'gif', 'png']
files = []

if len(sys.argv) != 3:
    print "Usage: " + sys.argv[0] + " <url> <output>"
    sys.exit(1)
else:
    url = sys.argv[1]
    if sys.argv[2].endswith("/"):
    	dir = sys.argv[2]
    else:
    	dir = sys.argv[2] + "/"

resp = requests.get(url).text
soup = BeautifulSoup(resp)

name = soup.title.string
name = name.split(" - ")[1]
if name.endswith(" "):
	name = name[:-1]
name = name.replace(" ", "_")

print name

if not os.path.exists(dir + name):
	os.mkdir(dir + name)

def get_files():
	for link in soup.findAll('div', {'class': 'file'}):
		files.append("http://8chan.co" + link.findAll('a')[0]['href'])

def download_files():
	count = 0
	for i in files:
		count += 1
		print "[+] Image " + str(count)
		filename = i.split("/")[-1] 
		#print "download_files: " + filename
		
		urllib.urlretrieve(i, dir + "/" + name + "/" +filename)

print "[!] Done!"



get_files()
download_files()
