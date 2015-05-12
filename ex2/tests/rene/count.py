#!/usr/local/bin/python3.4
# -*- coding: iso-8859-1 -*-
import sys
import getopt
import fileinput
from collections import Counter

STOPMARKS = [",", ";", ".", ":", '"', "'", "?", "!", "<", ">", "(", ")", "[", "]", "-", "_"]

has_input_file = False
file_input = ''

n = 5

#char, german, english, spanish
CHARS = [
			('a', 0.07, 0.08, 0.13), ('b', 0.02, 0.02, 0.01), ('c', 0.03, 0.03, 0.05), ('d', 0.05, 0.04, 0.06), 
			('e', 0.17, 0.13, 0.14), ('f', 0.02, 0.02, 0.00), ('g', 0.03, 0.02, 0.01), ('h', 0.05, 0.06, 0.01), 
			('i', 0.08, 0.07, 0.06), ('j', 0.00, 0.00, 0.00), ('k', 0.01, 0.01, 0.00), ('l', 0.03, 0.04, 0.05), 
			('m', 0.03, 0.02, 0.03), ('n', 0.10, 0.07, 0.07), ('o', 0.03, 0.08, 0.09), ('p', 0.01, 0.02, 0.03), 
			('q', 0.00, 0.00, 0.01), ('r', 0.07, 0.06, 0.07), ('s', 0.07, 0.06, 0.08), ('t', 0.06, 0.09, 0.05), 
			('u', 0.04, 0.03, 0.04), ('v', 0.01, 0.01, 0.01), ('w', 0.02, 0.02, 0.00), ('x', 0.00, 0.00, 0.00), 
			('y', 0.00, 0.02, 0.01), ('z', 0.01, 0.00, 0.01)
		]
				
				
"""
MAIN FUNCTION
"""
def main(argv):
	# arg handling
	arg_handling(argv)
	
	# open file
	fs = open(file_input, 'r')
	
	# read file
	text = fs.read()
	
	# get pairs
	(words, total, list) = get_pairs(text, n)
	(words2, total2, list2) = get_chars(text, n)
	
	# print information
	print("total amount of words:", words)
	print("total amount of chars:", total2)
	print("total amount of letter-pairs:", total)
	
	print("- top chars -")
	for i in range(len(list2)):
		x = list2[i]
		print(i+1, x[0], x[1], format(x[2], '.5f'))
	
	print("")
	print("- top pairs -")
	for i in range(len(list)):
		x = list[i]
		print(i+1, x[0], x[1], format(x[2], '.5f'))

	
	weight1 = total/words
	weight2 = total2/words2
	
	print("weight1:", weight1, "\tweight2:", weight2)
	
	
	print("char\t", "german\t", "english\t", "spanish")
	
	for tuple in CHARS:
		print(tuple[0], "\t", tuple[1], "\t", tuple[2], "\t", tuple[3])
	
	sys.exit()
	
# returns (total_words, total_pairs, list) where list is a list of char-pairs with syntax: (pair, abs. count, rel. count)
def get_pairs(text, top_boundary):
	return get_list(text, top_boundary, True)
	
# returns (total_words, total_chars, list) where list is a list of chars with syntax: (char, abs. count, rel. count)
def get_chars(text, top_boundary):
	return get_list(text, top_boundary, False)

# returns (total_words, total_chars/pairs, list) where list is a list of items with syntax: (item, abs.count, rel.count). Pairs = True for pairs-list, False for char-list.
def get_list(text, top_boundary, pairs):
	# normalize
	text = text.lower()
	
	# remove marks
	for char in STOPMARKS:
		text = text.replace(char, " ")

    # convert to array
	words = text.split()

	
	leng = 0
	for word in words:
		leng += len(word)
	
	# create pair list
	list = []
	if pairs:
		list = create_pair_list(words)
	else:
		list = create_char_list(words)
	
	# get unique pairs
	unique_pairs = create_tuple_list(list)
	
	# add relative occurence
	uniques_with_rel = get_tuple_list(unique_pairs, top_boundary)
	
	# return
	return (len(words), len(list), uniques_with_rel)

# list(word, count) -> list(word, abs. count, rel. count)
def get_tuple_list(tuple_list, amount):
	list = []
	
	if (amount > 0):
		max_display = min(amount, len(tuple_list))
	else:
		max_display = len(tuple_list)
		
	for i in range(max_display):
		(word, abs_count) = tuple_list[i]
		rel_count = float(abs_count)/float(len(tuple_list))
		
		list.append((word, abs_count, rel_count))

	return list
	
# CREATES LIST PAIRS OR CHAR ITEMS BASED ON MODE
def create_pair_list(word_list):
	buff = []
	for word in word_list:
		if len(word) > 1:
			for i in range(0,len(word)-1):
				buff.append(word[i:i+2])
	return buff
	
def create_char_list(word_list):
	return list("".join(word_list))
	
def create_tuple_list(item_list):
	word_counter = Counter(item_list)
	return word_counter.most_common()


# OPTION AND ARG HANDELING
def arg_handling(argv):
	try:
		opts, args = getopt.getopt(
				argv,
				"i:n:cp",
				["input-file=", "amount="]
				)
	except getopt.GetoptError:
		print('Please specify an input file -i <file>!')
		sys.exit(2)

	global has_input_file
	global file_input
	global n
	
	for opt, arg in opts:
		if opt in ("-i", "--input-file"):
			has_input_file = True
			file_input = arg
		elif opt in ("-n"):
			n = int(arg)
			
	if not has_input_file:
		print('Please specify an input file -i <file>!')
		sys.exit(2)
	
"""
MAIN CALL TO RUN LANG_DETECT.PY
"""
if __name__ == "__main__":
	main(sys.argv[1:])

