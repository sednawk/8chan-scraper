#
# 8Chan Scraper
# Written by @sednawk and @dade0
#

import os
import sys
import urllib
import requests
import urlparse
from bs4 import BeautifulSoup
from optparse import OptionParser


allowed_files = ['webm', 'jpg', 'jpeg', 'gif', 'png']
files = []

parser = OptionParser()
parser.add_option("-t", "--thread", dest="thread", help="Thread to scrape.", metavar="THREAD")

parser.add_option("-o", "--out", dest="dir", help="Output directory.", metavar="DIRECTORY")
parser.add_option("-n", "--new", dest="new", help="Save images into a folder named after the title.", default=None, action='store_true')

(options, args) = parser.parse_args()


if not options.thread:
	parser.print_help()
	sys.exit()

url = options.thread

if not options.dir:
	print "[!] No output dir supplied."
	current = raw_input("Use current dir? [Y/n] ")
	if current.lower() == "y":
		dir = os.getcwd() + "/"
	else:
		print "bye faget"
		sys.exit()
else:
	if options.dir.endswith("/"):
		dir = options.dir
	else:
		dir = options.dir + "/"

resp = requests.get(url).text
soup = BeautifulSoup(resp)

name = soup.title.string
name = name.split(" - ")[1]
if name.endswith(" "):
	name = name[:-1]
name = name.replace(" ", "_")

def get_files():
	for link in soup.findAll('div', {'class': 'file'}):
		files.append("http://8chan.co" + link.findAll('a')[0]['href'])

def download_files(new):
	count = 0
	for i in files:
		count += 1
		print "[+] Image " + str(count)
		filename = i.split("/")[-1] 
		if new:
			if not os.path.exists(dir + name):
				os.mkdir(dir + name)
			urllib.urlretrieve(i, dir + name + "/" +filename)
		else:
			print dir +filename
			urllib.urlretrieve(i, dir +filename)

print "[!] Done!"



get_files()
download_files(options.new)
