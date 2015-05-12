#!/usr/local/bin/python3.4
# -*- coding: iso-8859-1 -*-
import sys
import getopt
import fileinput
import consts
from collections import Counter


		
PAIRS = consts.PAIRS
CHARS = consts.CHARS


STOPMARKS = [",", ";", ".", ":", '"', "'", "?", "!", "<", ">", "(", ")", "[", "]", "-", "_"]

has_input_file = False
file_input = ''
codec = "utf-8"

# default = 36 -> amount of bigramm data for spanish language
n = 36

# CONST
UNDEFINED = 0
GER = 1
ENG = 2
SPA = 3
				
"""
MAIN FUNCTION
"""
def main(argv):
	# arg handling
	arg_handling(argv)
	
	# open file
	fs = open(file_input, 'r', encoding = codec)
	
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
	
	# print("weight1:", weight1, "\tweight2:", weight2)
	print(get_char_prob('e', SPA))
	
	prob_ger = 0
	prob_eng = 0
	prob_spa = 0
	
	language = UNDEFINED
	
	for i in range(len(list2)):
		char = list2[i][0]
		counted_prob = list2[i][2]
		perfect_prob = get_char_prob(char, GER)
		diff_prob = abs(counted_prob - perfect_prob)
		prob_ger += abs(counted_prob - get_char_prob(char, GER))
		prob_eng += abs(counted_prob - get_char_prob(char, ENG))
		prob_spa += abs(counted_prob - get_char_prob(char, SPA))

	print("char probabilities:", prob_ger, prob_eng, prob_spa)

	
	if(prob_ger < prob_eng):
		if(prob_ger < prob_spa):
			language = GER
		else:
			language = SPA
	else:
		if(prob_eng < prob_spa):
			language = ENG
		else:
			language = SPA
			
	if language == GER:
		print("detected language:", "german")
	if language == ENG:
		print("detected language:", "english")
	if language == SPA:
		print("detected language:", "spanish")
		
	#for i in range(len(PAIRS)):
	#	print(PAIRS[i][0], PAIRS[i][1], PAIRS[i][2], PAIRS[i][3])	
	
	prob_pair_ger = 0
	prob_pair_eng = 0
	prob_pair_spa = 0

	for i in range(len(list)):
		
		pair = list[i][0]
		counted_prob = list[i][2]
		perfect_prob = get_pair_prob(pair, GER)
		diff_prob = abs(counted_prob - perfect_prob)
		
		print(pair, counted_prob, perfect_prob, diff_prob)
		prob_pair_ger += abs(counted_prob - get_pair_prob(pair, GER))
		prob_pair_eng += abs(counted_prob - get_pair_prob(pair, ENG))
		prob_pair_spa += abs(counted_prob - get_pair_prob(pair, SPA))

	print("pair probabilities:", prob_pair_ger, prob_pair_eng, prob_pair_spa)

	
	if(prob_pair_ger < prob_pair_eng):
		if(prob_pair_ger < prob_pair_spa):
			language = GER
		else:
			language = SPA
	else:
		if(prob_pair_eng < prob_pair_spa):
			language = ENG
		else:
			language = SPA
			
	if language == GER:
		print("detected language:", "german")
	if language == ENG:
		print("detected language:", "english")
	if language == SPA:
		print("detected language:", "spanish")	
		
		
	
		
	sys.exit()
	
# returns the probability of given char in the given language
def get_char_prob(char, language):
	for x in CHARS:
		if char == x[0]:
			return x[language]
	return 0
	
# returns the probability of a given letter-pair in the given language
def get_pair_prob(pair, language):
	for x in PAIRS:
		print(pair, x[0], pair == x[0])
		if pair == x[0]:
			print(pair, x[0], pair == x[0])
			return x[language]
	return 0
	
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
	uniques_with_rel = get_tuple_list(unique_pairs, top_boundary, len(list))
	
	# return
	return (len(words), len(list), uniques_with_rel)

# list(word, count) -> list(word, abs. count, rel. count)
def get_tuple_list(tuple_list, amount, abs):
	list = []
	
	if (amount > 0):
		max_display = min(amount, len(tuple_list))
	else:
		max_display = len(tuple_list)
		
	
		
	for i in range(max_display):
		(word, abs_count) = tuple_list[i]
		rel_count = float(abs_count)/float(abs)
		
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

