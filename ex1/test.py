#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import fileinput

# const
WORD = 0
CHAR = 1
PAIR = 2
STOPMARKS = [",", ";", ".", ":", '"', "'", "?", "!", "<", ">", "(", ")", "[", "]", "-", "_"]

# cfg
top_words = 30				# displays this amount of words
read_stopwords = True		# reads and removes stopwords
language = "german"			# language of read document
codec = "utf-8"				# codec of read document
mode = PAIR					# mode = WORD, PAIR, CHAR
use_global_count = True		# if set counts stopwords to total-counts
count_occurences = True		# if set counts and writes occurences of words

# files
path_stopwords = "stopwords/" + language
file_stopwords = ""
if(read_stopwords):
	file_stopwords = open(path_stopwords, "r", encoding = codec)

# results output_file file
output_file_file = "results.txt"
file_listoutput_file = open(output_file_file, "w", encoding = codec)
output_occ_file = "occurences.txt"
if(count_occurences):
	file_occ_output_file = open(output_occ_file, "w", encoding = codec)

global_words = []

###
### MAIN FUNCTION
###
def main():
	len_var = len(sys.argv)
	
	if(len_var <= 1):
		print("not enough arguments -> exit")
		sys.exit()

		
	
	# read file from input
	# text = txt_read(fileinput.input())
	text = txt_read(fileinput.FileInput(openhook=fileinput.hook_encoded(codec)))

	# normalize
	text = text.lower()
	
	# remove marks
	for char in STOPMARKS:
		text = text.replace(char, " ")

	# convert to array
	words = text.split()
	
	# set global variables
	global use_global_count
	global global_words
	global_words = list(words)

	print("total words:", len(words))

	# remove stopwords
	if(read_stopwords):
		words = remove_stopwords(words)

	# sort
	unique_word_tuples = create_tuple_list(words)
	
	print("unique words:", len(unique_word_tuples))

	# print top
	print()
	print(top_words, "most used words:")
	print_tuple_list(unique_word_tuples, top_words)
	
	write_tuple_list(unique_word_tuples, top_words, file_listoutput_file)
	
	# if coutn occurences
	if count_occurences:
		# set global count false for occurences output
		temp = use_global_count
		use_global_count = False
		
		# calculate occurences tuple
		occ_tuple = convert_tuple_list(unique_word_tuples)
		
		# print
		print()
		print(top_words, "top occurences of words")
		print_tuple_list(occ_tuple, top_words)
	
		# write
		write_tuple_list(occ_tuple, top_words, file_occ_output_file)
		
		# re-set flag
		use_global_count = temp

	sys.exit()
	return

# TODO: remove when options/parameters implemented
def txt_read(input):
	buff = ""
	for line in input:
		buff = buff + line
	return buff	

### REMOVES STOPWORDS FROM GIVEN LIST
def remove_stopwords(words):
	stopwords = file_stopwords.read()
		
	rem_counter = 0
	for stopword in stopwords.split():
		while stopword in words:
			rem_counter += 1
			words.remove(stopword)
		
	print("removed stopwords:", rem_counter)
	return words
	
### PRINTS THE FIRST i ITEMS
def print_tuple_list(tuple_list, top_words):
	global global_words
	
	total_count = 0
	if use_global_count:
		total_count = count_by_mode(global_words)
	else:
		for tuple in tuple_list:
			total_count += tuple[1]
	
	print("#", '\t', "total", '\t', "rel.", '\t\t', "word")
	
	count = 0
	for x in range(0, min(top_words, len(tuple_list))):
		count += tuple_list[x][1]/total_count
		print(x, '\t', tuple_list[x][1], '\t', "{:10.5f}".format(tuple_list[x][1]/total_count), '\t', tuple_list[x][0])
		
	print("sum of shown rel.:", count)
	return
	
### WRITES THE TUPLE LIST TO THE output_file FILE
def write_tuple_list(tuple_list, top_words, output_file):	
	global global_words
	
	total_count = 0
	if use_global_count:
		total_count = count_by_mode(global_words)
	else:
		for tuple in tuple_list:
			total_count += tuple[1]
	
	for x in range(0, min(top_words, len(tuple_list))):
		line = ''
		word = tuple_list[x][0]
		abs = tuple_list[x][1]
		rel = "{:10.5f}".format(tuple_list[x][1]/total_count)

		line += str(x) + '\t' + str(abs) + '\t' + rel + '\t' + str(word) + '\n'
	
		# write line
		output_file.write(line)

	print("file write finished")
	return
	
### COUNTS UNIQUE WORDS AND RETURNS A LIST OF TUPLES
def create_tuple_list(word_list):
	unique_items = []
	item_counter = []

	if(mode == WORD):
		item_list = create_word_list(word_list)
	if(mode == CHAR):
		item_list = create_char_list(word_list)
	if(mode == PAIR):
		item_list = create_pair_list(word_list)
		
	
	# filter words
	for item in item_list:
		if item not in unique_items:
			unique_items.append(item)
			item_counter.append(1)
		else:
			index = unique_items.index(item)
			item_counter[index] += 1

	# create tuple words
	tuple_items = []
	for i in range(len(unique_items)):
		tuple_items.append((unique_items[i], item_counter[i]))
	
	# sort words
	tuple_items = sorted(tuple_items, key=lambda x: x[1], reverse=True)
		
	# return sorted tuple words (word w, count(w))
	return tuple_items
	
### CEATES LIST OF WORDS
def create_word_list(word_list):
	return word_list
	
### CREATES LIST OF CHARS
def create_char_list(word_list):
	buff = []
	for word in word_list:
		for char in word:
			buff.append(char)
	
	return buff
	
### CREATES LIST OF PAIRS
def create_pair_list(word_list):
	buff = []
	for word in word_list:
		if len(word) > 1:
			for i in range(0,len(word)-1):
				buff.append(word[i:i+2])
	
	return buff
	
### RETURNS ITEM COUNT DEPENDING ON MODE
def count_by_mode(word_list):
	count = 0
	if(mode == WORD):
		count = len(word_list)
	if(mode == PAIR):
		for word in word_list:
			if len(word) > 1:
				for i in range(0,len(word)-1):
					count += 1
	if(mode == CHAR):
		for word in word_list:
			for char in word:
				count += 1

	return count
	
### CONVERTS TUPLE-LIST (word, occurence) TO TUPLE-LIST (occurence, sum(words with occ))
def convert_tuple_list(tuple_list):
	buff = []
	
	unique_occurences = []
	item_counter = []
	
	for tuple in tuple_list:
		if tuple[1] in unique_occurences:
			index = unique_occurences.index(tuple[1])
			item_counter[index] += 1
		else:
			unique_occurences.append(tuple[1])
			item_counter.append(1)
			
	# create tuple occ
	tuple_items = []
	for i in range(len(unique_occurences)):
		tuple_items.append((unique_occurences[i], item_counter[i]))
	
	# sort words
	tuple_items = sorted(tuple_items, key=lambda x: x[0])

	# return
	return tuple_items
	
## call main
main()
### END OF CODE