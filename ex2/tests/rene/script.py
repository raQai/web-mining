#!/usr/local/bin/python3.4
# -*- coding: iso-8859-1 -*-
import sys
import getopt
import fileinput
import time
import detect
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

has_input_file = False
file_input = ''
write_output = False
file_output = "results.txt" 
codec = "utf-8"

# default = 20
n = 20

# 10 -> all pages
max_pages = 10
sleep_time = 2

base_url = "https://www.ke.tu-darmstadt.de/files/lehre/ss15/web-mining/uebung2/"
url_suffix = ".html"


"""
MAIN FUNCTION
"""
def main(argv):
	# arg handling
	arg_handling(argv)

	# open output file
	if(write_output):
		output_fs = open(file_output, 'w', encoding = codec)
	
	# get texts from websites
	for i in range(1, max_pages + 1):
		# sleep a bit between requests
		if not i == 1:
			time.sleep(sleep_time)
			
		# craft url
		url = base_url + "{:0>2d}".format(i) + url_suffix
		print("[REQUEST]", url)

		# get web page
		html = urlopen(url).read()
		soup = BeautifulSoup(html)
		
		# extract visible text
		[s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
		visible_text = soup.getText()
		
		# detect language
		lang = detect.detect_language(visible_text, n)
		
		print("[STATUS]", "text", i, "detected:", lang)
		
		if(write_output):
			output_fs.write(str(i) + " " + lang + "\n")
		
		
	# exit
	sys.exit()

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    return True
	
	
# OPTION AND ARG HANDELING
def arg_handling(argv):
	try:
		opts, args = getopt.getopt(
				argv,
				"n:",
				["amount="]
				)
	except getopt.GetoptError:
		print('Something went wrong!')
		sys.exit(2)

	global n
	
	for opt, arg in opts:
		if opt in ("-n"):
			n = int(arg)
	
"""
MAIN CALL TO RUN SCRIPT.PY
"""
if __name__ == "__main__":
	main(sys.argv[1:])

