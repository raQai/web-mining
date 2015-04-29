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
	
	# sort
	unique_word_tuples = create_word_tuples(words)
	
	print("unique words:", len(unique_word_tuples))

	# print top 30
	tuple_list_print(unique_word_tuples, top_words)
	
	tuple_list_write(unique_word_tuples, top_words, file_listoutput_file)
	sys.exit()
	return

# TODO: remove when options/parameters implemented
def txt_read(input):
	buff = ""
	for line in input:
		buff = buff + line
	return buff	

### PRINTS THE FIRST i ITEMS
def tuple_list_print(tuple_list, top_words):
	length = len(tuple_list)
	print()
	print(top_words, "most used words:")
	print("#", '\t', "total", '\t', "rel.", '\t\t', "word")

	for x in range(0, min(top_words, length)):
		print(x, '\t', tuple_list[x][1], '\t', "{:10.5f}".format(tuple_list[x][1]/length), '\t', tuple_list[x][0])
		
	return
	
### WRITES THE TUPLE LIST TO THE output_file FILE
def tuple_list_write(tuple_list, top_words, output_file):
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

### COUNTS UNIQUE WORDS WITHOUT STOPWORDS IF SET AND RETURNS A LIST OF TUPLES
def create_word_tuples(words):
	unique_words = []
	unique_words_counter = []
	
	stopwords = ""
	# read if flag set
	if(read_stopwords):
		stopwords = file_stopwords.read()
	
	rem_stopwords = 0

	# filter words
	for word in words:
		if word not in stopwords:
			if word not in unique_words:
				unique_words.append(word)
				unique_words_counter.append(1)
			else:
				index = unique_words.index(word)
				unique_words_counter[index] += 1
		else:
				rem_stopwords += 1
	
	# print
	print("removed stopwords:", rem_stopwords)

	# create tuple words
	tuple_words = []
	for i in range(len(unique_words)):
		tuple_words.append((unique_words[i], unique_words_counter[i]))
	
	# sort words
	tuple_words = sorted(tuple_words, key=lambda x: x[1], reverse=True)
		
	# return sorted tuple words (word w, count(w))
	return tuple_words
	
## call main
main()
### END OF CODE