#!/usr/local/bin/python3.4
# -*- coding: utf-8 -*-
input_file_1 = "out_patrick_yey.txt"
input_file_2 = "out_kongfoos.txt"
output_file = "intersection.txt"

"""
MAIN FUNCTION
"""
def main():	
	print("Comparing links in files:", input_file_1, "with", input_file_2)
	
	# open files
	f1 = open(input_file_1, 'r')
	f2 = open(input_file_2, 'r')
	
	# get lines
	text1 = f1.read().split("\n")
	text2 = f2.read().split("\n")
	
	# add links to sets
	set1 = set()
	set2 = set()
	
	for link in text1:
		set1.add(link)
	
	for link in text2:
		set2.add(link)
	
	# intersection
	set3 = set1.intersection(set2)
	
	# print results
	print("identical links found:", len(set3))
	print("writing results to:", output_file)
	output = open(output_file, 'w')
	
	# write
	for e in set3:
		output.write(e + "\n")

	print("comparison finished")
 
if __name__ == "__main__":
	main()
	
"""
MAIN CALL TO RUN SCRIPT.PY
"""
if __name__ == "__main__":
	main()

