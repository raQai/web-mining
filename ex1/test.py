#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import fileinput
import math

# cfg
top_words = 1300
normalize = True
removemarks = True

language = "german"
output_file = "results.txt"
codec = "utf-8"

# files
path_stopwords = "stopwords/" + language
file_stopwords = open(path_stopwords, "r", encoding = codec)

path_stopmarks = "stopwords/stopmarks"
file_stopmarks = open(path_stopmarks, "r", encoding = codec)
stopmarks = file_stopmarks.read()

file_listoutput = open(output_file, "w", encoding = codec)


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

	# remove marks
	if(removemarks):
		text = txt_removemarks(text)
	
	# normalize
	if(normalize):
		text = txt_normalize(text)
	
	# count
	txt_count(text)
	
	# sort
	tuple = list_count_without_stopwords(text)
	
	print("unique words:", len(tuple))

	# print top 30
	tuple_list_print(tuple, top_words)
	
	tuple_list_write(tuple, top_words, file_listoutput)
	sys.exit()
	return

### PRINT TEXT LINE BY LINE
def txt_print(input):
	for line in input:
		print(line)
	return

def txt_read(input):
	buff = ""
	for line in input:
		buff = buff + line
	return buff
	
### COUNT WORDS IN TEXT
def txt_count(input):
	counter = 0

	words = input.split()
	for word in words:
		counter = counter + 1

	print("total words:", counter)
	return
	
### NORMALIZES INPUT TEXT, REMOVES , . ' etc. letters and makes all lowercase
def txt_normalize(input):
	flag = True
	buff = ""
	for word in input.split():
		if flag:
			buff = buff + word.lower()
			flag = False
		else:
			buff = buff + " " + word.lower()

	return buff
		
### REMOVES MARKS AND REPLACES THEM WITH " " SPACE		
def txt_removemarks(input):
	buff = ""
	for line in input:
		for char in stopmarks:
			if(removemarks):
				line = line.replace(char, " ")
		buff = buff + line

	return buff
	

### PRINTS THE FIRST i ITEMS
def tuple_list_print(tuple_list, i):
	length = len(tuple_list)
	print()
	print(i, "most used words:")
	print("#", '\t', "total", '\t', "rel.", '\t\t', "word")

	max = i
	if(i > length):
		max = length
		
	x = 0
	while x < max:
		print(x, '\t', tuple_list[x][1], '\t', math.floor(tuple_list[x][1]/length*10000)/10000, '\t', tuple_list[x][0])
		x = x + 1
		
	return
	
### WRITES THE TUPLE LIST TO THE OUTPUT FILE
def tuple_list_write(tuple_list, i, output):
	length = len(tuple_list)
	
	max = i
	if(i > length):
		max = length
		
	x = 0
	while x < max:
		line = ''
		word = tuple_list[x][0]
		abs = tuple_list[x][1]
		rel = math.floor(tuple_list[x][1]/length*10000)/10000

		line = line + str(x) + '\t' + str(abs) + '\t' + str(rel) + '\t' + word + '\n'
	
		# write line
		output.write(line)
		x = x + 1
	
	print("file write finished")
	return

### COUNTS WORDS WITHOUT STOPWORDS
def list_count_without_stopwords(list):
	list2 = []
	counter = []
	stopwords = file_stopwords.read()
	
	rem_counter = 0
	
	tuple_list = []
	
	# filter words
	for a in list.split():
		if a not in stopwords:
			if a not in list2:
				list2.append(a)
				counter.append(1)
			else:
				index = list2.index(a)
				counter[index] = counter[index] + 1
		else:
				rem_counter = rem_counter + 1
	
	print("removed stopmarks:", rem_counter)
	
	# create tuple list
	for i in range(len(list2)):
		tuple_list.append((list2[i], counter[i]))
	
	# sort list
	tuple_list_sort = sorted(tuple_list,key=lambda x: x[1], reverse=True)
		
	# return sorted tuple list (word w, count(w))
	return tuple_list_sort
	
## call main
main()
### END OF CODE