#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import fileinput
import math

# cfg
top_words = 30
read_stopwords = True
language = "german"
codec = "utf-8"

# files
path_stopwords = "stopwords/" + language
file_stopwords = ""
if(read_stopwords):
	file_stopwords = open(path_stopwords, "r", encoding = codec)

# stopmarks to be removed
stopmarks = [",", ";", ".", ":", '"', "'", "?", "!", "<", ">", "(", ")", "[", "]", "-", "_"]

# results output_file file
output_file_file = "results.txt"
file_listoutput_file = open(output_file_file, "w", encoding = codec)


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
	for char in stopmarks:
		text = text.replace(char, " ")
	

	
	# convert to array
	words = text.split()
	print("total words:", len(words))

	# remove stopwords
	if(read_stopwords):
		words = remove_stopwords(words)

	# sort
	unique_word_tuples = create_tuple_list(words)
	
	print("unique words:", len(unique_word_tuples))

	# print top 30
	print_tuple_list(unique_word_tuples, top_words)
	
	write_tuple_list(unique_word_tuples, top_words, file_listoutput_file)
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
	length = len(tuple_list)
	print()
	print(top_words, "most used words:")
	print("#", '\t', "total", '\t', "rel.", '\t\t', "word")

	for x in range(0, min(top_words, length)):
		print(x, '\t', tuple_list[x][1], '\t', "{:10.5f}".format(tuple_list[x][1]/length), '\t', tuple_list[x][0])
		
	return
	
### WRITES THE TUPLE LIST TO THE output_file FILE
def write_tuple_list(tuple_list, top_words, output_file):
	length = len(tuple_list)

	for x in range(0, min(top_words, length)):
		line = ''
		word = tuple_list[x][0]
		abs = tuple_list[x][1]
		rel = "{:10.5f}".format(tuple_list[x][1]/length)

		line += str(x) + '\t' + str(abs) + '\t' + rel + '\t' + word + '\n'
	
		# write line
		output_file.write(line)

	print("file write finished")
	return

### COUNTS UNIQUE WORDS AND RETURNS A LIST OF TUPLES
def create_tuple_list(word_list):
	unique_items = []
	item_counter = []
	
	# filter words
	for item in word_list:
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
	
## call main
main()
### END OF CODE