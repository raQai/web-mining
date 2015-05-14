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
write_output = True
file_output = "challenge.txt" 
codec = "utf-8"

# default = 20
n = 20

# sleep time between each request
sleep_time = 2


urls = [
		"https://www.ke.tu-darmstadt.de/files/lehre/ss15/web-mining/uebung2/01.html",
		"https://www.ke.tu-darmstadt.de/files/lehre/ss15/web-mining/uebung2/02.html", 
		"https://www.ke.tu-darmstadt.de/files/lehre/ss15/web-mining/uebung2/03.html", 
		"https://www.ke.tu-darmstadt.de/files/lehre/ss15/web-mining/uebung2/04.html",
		"https://www.ke.tu-darmstadt.de/files/lehre/ss15/web-mining/uebung2/05.html",
		"https://www.ke.tu-darmstadt.de/files/lehre/ss15/web-mining/uebung2/06.html",
		"https://www.ke.tu-darmstadt.de/files/lehre/ss15/web-mining/uebung2/07.html",
		"https://www.ke.tu-darmstadt.de/files/lehre/ss15/web-mining/uebung2/08.html",
		"https://www.ke.tu-darmstadt.de/files/lehre/ss15/web-mining/uebung2/09.html",
		"https://www.ke.tu-darmstadt.de/files/lehre/ss15/web-mining/uebung2/10.html"
		]

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
	counter = 1
	for url in urls:
		# sleep a bit between requests
		time.sleep(sleep_time)
			
		# print
		print("[REQUEST]", url)

		# get web page
		html = urlopen(url).read()
		soup = BeautifulSoup(html)
		
		# extract visible text
		[s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
		visible_text = soup.getText()
		
		# detect language
		lang = detect.detect_language(visible_text, n)
		
		print("[STATUS]", "text", counter, "detected:", lang)
		
		if(write_output):
			output_fs.write(str(counter) + " " + lang + "\n")
			
		counter += 1
		
		
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

