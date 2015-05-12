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

# default = 20
n = 20

# print flag
print_all = False

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

	# detect language
	language = detect_language(text, n)
	
	# print result
	print("")
	print("detected language:", language)
	print("")
	
	# exit
	sys.exit()
	
# detects the language of the given input text, also normalizes, removes signs etc.
def detect_language(text, n):
	# get pairs
	(words, total, pairs) = get_pairs(text, n)
	(words2, total2, chars) = get_chars(text, n)
	
	# sum char probabilities
	prob_char_ger = 0
	prob_char_eng = 0
	prob_char_spa = 0
	
	char_lang = UNDEFINED
	
	for i in range(len(chars)):
		char = chars[i][0]
		prob_char_ger += abs(chars[i][2] - get_char_prob(char, GER))
		prob_char_eng += abs(chars[i][2] - get_char_prob(char, ENG))
		prob_char_spa += abs(chars[i][2] - get_char_prob(char, SPA))
	
	# detect language, lowest prob sum -> smallest distance -> best match
	if(prob_char_ger < prob_char_eng):
		if(prob_char_ger < prob_char_spa):
			char_lang = GER
		else:
			char_lang = SPA
	else:
		if(prob_char_eng < prob_char_spa):
			char_lang = ENG
		else:
			if(prob_char_spa < prob_char_eng):
				char_lang = SPA
			else:
				char_lang = UNDEFINED
			
	# sum pair probabilities
	prob_pair_ger = 0
	prob_pair_eng = 0
	prob_pair_spa = 0
	
	pair_lang = UNDEFINED
	
	for i in range(len(pairs)):
		pair = pairs[i][0]
		prob_pair_ger += abs(pairs[i][2] - get_pair_prob(pair, GER))
		prob_pair_eng += abs(pairs[i][2] - get_pair_prob(pair, ENG))
		prob_pair_spa += abs(pairs[i][2] - get_pair_prob(pair, SPA))	
	
	# detect language, lowest prob sum -> smallest distance -> best match
	if(prob_pair_ger < prob_pair_eng):
		if(prob_pair_ger < prob_pair_spa):
			pair_lang = GER
		else:
			pair_lang = SPA
	else:
		if(prob_pair_eng < prob_pair_spa):
			pair_lang = ENG
		else:
			if(prob_pair_spa < prob_pair_eng):
				pair_lang = SPA
			else:
				pair_lang = UNDEFINED
	
	# if print, print results
	if(print_all):
		print("probabilities\t", "german\t\t", "english\t", "spanish")
		print("chars:\t",
			"\t", format(prob_char_ger, '.5f'), 
			"\t", format(prob_char_eng, '.5f'), 
			"\t", format(prob_char_spa, '.5f')
			)
		print("pairs:\t",
			"\t", format(prob_pair_ger, '.5f'), 
			"\t", format(prob_pair_eng, '.5f'), 
			"\t", format(prob_pair_spa, '.5f')
			)

		if char_lang == GER:
			print("(chars) detected language:", "german")
		elif char_lang == ENG:
			print("(chars) detected language:", "english")
		elif char_lang == SPA:
			print("(chars) detected language:", "spanish")
		elif char_lang == UNDEFINED:
			print("(chars) detected language:", "undefined")	
		
		if pair_lang == GER:
			print("(pairs) detected language:", "german")
		elif pair_lang == ENG:
			print("(pairs) detected language:", "english")
		elif pair_lang == SPA:
			print("(pairs) detected language:", "spanish")	
		elif pair_lang == UNDEFINED:
			print("(pairs) detected language:", "undefined")

	
	# return
	if(char_lang == pair_lang):
		return language_to_string(char_lang)
	elif(char_lang == UNDEFINED):
		return language_to_string(pair_lang)
	elif(pair_lang == UNDEFINED):
		return language_to_string(char_lang)
	elif(char_lang != pair_lang):
		return language_to_string(pair_lang)
		
	# default case, code should not execute here
	return UNDEFINED
	
# returns a full string of the language const
def language_to_string(language):
	if(language == GER):
		return "german"
	elif(language == ENG):
		return "english"
	elif(language == SPA):
		return "spanish"
	else:
		return "undefnied"
	
# returns the probability of given char in the given language
def get_char_prob(char, language):
	for x in CHARS:
		if char == x[0]:
			return x[language]
	return 0
	
# returns the probability of a given letter-pair in the given language
def get_pair_prob(pair, language):
	char1 = pair[0]
	char2 = pair[1]
	index1 = ord(char1) - 97
	index2 = ord(char2) - 97
	
	# calc index and return prob
	if((0 <= index1 <= 26) and (0 <= index2 <= 26)):
		index = 26*index1 + index2
		return PAIRS[index][language]
	
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
	
	# replace
	for char in ['ö', 'ó', 'ò', 'ô']:
		text = text.replace(char, 'o')
	for char in ['ä', 'á', 'à', 'â']:
		text = text.replace(char, 'a')
	for char in ['é', 'è', 'ê']:
		text = text.replace(char, 'e')
	for char in ['í', 'ì', 'î', 'ï']:
		text = text.replace(char, 'i')
	for char in ['ü', 'ú', 'ù', 'û']:
		text = text.replace(char, 'u')
	
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

