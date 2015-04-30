#!/usr/local/bin/python3.4
# -*- coding: iso-8859-1 -*-
import sys
import getopt
import fileinput

# const
WORD = 0
CHAR = 1
PAIR = 2
STOPMARKS = [",", ";", ".", ":", '"', "'", "?", "!", "<", ">", "(", ")", "[", "]", "-", "_"]

# GLOBALS AND FLAGS
has_input_file = False
file_input = ''

has_output_file = False
file_output = ''

has_stopwords = False
file_stopwords = ''

top_boundary = 0

mode = WORD

use_global_count = False  # if set counts stopwords to total-counts

count_occurences = False  # if set counts and writes occurences of words

codec = "utf-8"           # codec of read document

global_words = []

###
### MAIN FUNCTION
###
def main(argv):
  len_var = len(sys.argv)

  try:
    opts, args = getopt.getopt(
        argv,
        "hi:o:s:n:wcp",
        ["help",
          "input-file=","output-file=","stopwords=","top-words=",
          "word","char","pair",
          "use-global-count", "gc", "count-occurences", "occ"]
        )
  except getopt.GetoptError:
    print('Please specify an input file -i <file>!')
    print('Try -h or --help for more information.')
    sys.exit(2)

  global has_input_file, file_input
  global file_input
  global has_output_file
  global file_output
  global has_stopwords
  global file_stopwords
  global top_boundary
  global mode
  global use_global_count
  global count_occurences

  for opt, arg in opts:
    if opt in ("-h", "--help"):
      with open('word_count.man', 'r', encoding = codec) as help_text_fs:
        print(help_text_fs.read())
      sys.exit()
    elif opt in ("-i", "--input-file"):
      has_input_file = True
      file_input = arg
    elif opt in ("-o", "--output-file"):
      has_output_file = True
      file_output = arg
    elif opt in ("-s", "--stopwords"):
      has_stopwords = True
      file_stopwords = arg
    elif opt in ("-n", "--top-words"):
      top_boundary = int(arg)
    elif opt in ("-w", "--word"):
      mode = WORD
    elif opt in ("-c", "--char"):
      mode = CHAR
    elif opt in ("-p", "--pair"):
      mode = PAIR
    elif opt in ("--gc", "--use-global-count"):
      use_global_count = True
    elif opt in ("--occ", "--count-occurences"):
      count_occurences = True

  if not has_input_file:
    print('Please specify an input file -i <file>!')
    print('Try -h or --help for more information.')
    sys.exit(2)

  # read file from input
  with open(file_input, 'r', encoding = codec) as input_fs:
    text = input_fs.read()

    # normalize
    text = text.lower()

    # remove marks
    for char in STOPMARKS:
      text = text.replace(char, " ")

    # convert to array
    words = text.split()

    # set global variables
    global global_words
    global_words = list(words)

    print("total words:", len(words))

    # remove stopwords
    if(has_stopwords):
      words = remove_stopwords(words)

    # sort and filter
    unique_word_tuples = create_tuple_list(words)

    print("unique words:", len(unique_word_tuples))

    if not has_output_file:
      print()
      print(top_boundary, "most used words:")
      print_tuple_list(unique_word_tuples)
    else:
      write_tuple_list(unique_word_tuples, file_output + '.txt')

    # if count occurences
    if count_occurences:
      # set global count false for occurences output
      temp = use_global_count
      use_global_count = False

      # calculate occurences tuple
      occ_tuple = convert_tuple_list(unique_word_tuples)

      # print
      if not has_output_file:
        print()
        print(top_boundary, "top occurences of words")
        print_tuple_list(occ_tuple)
      else:
        write_tuple_list(occ_tuple, file_output + '_occ.txt')

      # re-set flag
      use_global_count = temp

  sys.exit()
  return

### REMOVES STOPWORDS FROM GIVEN LIST
def remove_stopwords(words):
  with open(file_stopwords, 'r', encoding = codec) as stopword_fs:
    stopwords = stopword_fs.read()

    rem_counter = 0
    for stopword in stopwords.split():
      while stopword in words:
        rem_counter += 1
        words.remove(stopword)

    print("removed stopwords:", rem_counter)

  return words

### PRINTS THE FIRST i ITEMS
def print_tuple_list(tuple_list):
  total_count = get_total_count(tuple_list)

  # print top
  print(format('#', '6'), '\t' + format('abs', '6'), '\t' + format('rel.', '9'), '\t' + 'word')

  count = 0
  max_range = min(top_boundary, len(tuple_list)) if (top_boundary > 0) else len(tuple_list)

  for x in range(0, max_range):
    word = tuple_list[x][0]
    abs_count = tuple_list[x][1]
    rel_count = float(abs_count)/float(total_count)
    count += rel_count

    row = format(x, '6d') + ' \t' + format(abs_count, '6d') + ' \t' + format(rel_count, '.7f') + ' \t' + str(word)

    print(row)

  print("sum of shown rel.:", count)
  return

### WRITES THE TUPLE LIST TO THE output file stream
def write_tuple_list(tuple_list, output_location):
  total_count = get_total_count(tuple_list)

  max_range = min(top_boundary, len(tuple_list)) if (top_boundary > 0) else len(tuple_list)

  with open(output_location, 'w', encoding = codec) as output_fs:
    for x in range(0, max_range):
      word = tuple_list[x][0]
      abs_count = tuple_list[x][1]
      rel_count = float(abs_count)/float(total_count)

      row = format(x, '6d') + ' \t' + format(abs_count, '6d') + ' \t' + format(rel_count, '.7f') + ' \t' + str(word)

      # write line
      output_fs.write(row + "\n")

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

### RETURNS THE TOTAL COUNT OF WORDS THAT SHOULD BE USED
def get_total_count(tuple_list):
  total_count = 0
  if use_global_count:
    total_count = count_by_mode(global_words)
  else:
    for item in tuple_list:
      total_count += item[1]

  return total_count


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
if __name__ == "__main__":
  main(sys.argv[1:])

### END OF CODE
