#!/usr/local/bin/python3.4
# -*- coding: utf-8 -*-
from py_bing_search import PyBingSearch
import sys

output_file = "out.txt"

EXACT = True

"""
MAIN FUNCTION
"""
def main(argv):
	query = argv[1]

	if(EXACT):
		query = '"' + query + '"'
	print("Query:", query)
	
	bing = PyBingSearch()
	
	bing.search_all(query, 1000)
	
	print("-----------------------")
	print("hits:", len(bing.list))
	print("writing results to:", output_file)
	output = open(output_file, 'w')
	
	for url in bing.list:
		output.write(url + "\n")
		
	print("writing finished")

	sys.exit()
	
	

 
if __name__ == "__main__":
	main(sys.argv)
	
"""
MAIN CALL TO RUN SCRIPT.PY
"""
if __name__ == "__main__":
	main(sys.argv[1:])

