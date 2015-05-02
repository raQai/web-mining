#!/usr/local/bin/python3.4
# -*- coding: iso-8859-1 -*-
import sys
import getopt
import fileinput
from collections import Counter

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

"""
MAIN FUNCTION
"""
def main(argv):
  setup_word_counter(argv)

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

    # changes list format based on mode
    item_list = create_item_list(words)
    
    # create counter for item list
    word_collection_counter = Counter(item_list)

    # sort and apply top boundary
    if (top_boundary > 0):
      unique_word_tuples = word_collection_counter.most_common(top_boundary)
    else:
      unique_word_tuples = word_collection_counter.most_common()

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
      global use_global_count
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

  sys.exit()

"""
OUTPUT FUNCTIONS
"""
# PRINTS RESULTS TO CONSOLE WINDOW
def print_tuple_list(tuple_list):
  total_count = get_total_count(tuple_list)

  # print top
  print(format('#', '6'), '\t' + format('abs', '6'), '\t' + format('rel.', '9'), '\t' + 'word')
  print('------------------------------------------------')

  sum_rel = 0
  counter = 1

  for word_tuple in tuple_list:
    word = word_tuple[0]
    abs_count = word_tuple[1]
    rel_count = float(abs_count)/float(total_count)
    sum_rel += rel_count

    row = create_format_string(counter, abs_count, rel_count, word)
    counter += 1

    print(row)

  print("sum of shown rel.:", sum_rel)

# WRITES THE TUPLE LIST TO THE OUTPUT FILE STREAM
def write_tuple_list(tuple_list, output_location):
  total_count = get_total_count(tuple_list)

  max_range = min(top_boundary, len(tuple_list)) if (top_boundary > 0) else len(tuple_list)

  with open(output_location, 'w', encoding = codec) as output_fs:

    counter = 1

    for word_tuple in tuple_list:
      word = word_tuple[0]
      abs_count = word_tuple[1]
      rel_count = float(abs_count)/float(total_count)

      row = create_format_string(counter, abs_count, rel_count, word)
      counter += 1

      # write line to file
      output_fs.write(row + "\n")

  print("output written to", output_location)

"""
GENERAL HELPER FUNCTIONS FOR COUNTING, APPLYING FILTERS AND FORMATTING
"""
# REMOVES STOPWORDS FROM GIVEN LIST
def remove_stopwords(word_list):
  with open(file_stopwords, 'r', encoding = codec) as stopword_fs:
    stopwords = stopword_fs.read()

    rem_counter = 0
    for stopword in stopwords.split():
      rem_counter += word_list.count(stopword)
      word_list = [w for w in word_list if w != stopword]

    print("removed stopwords:", rem_counter)
  return word_list

def create_format_string(counter, abs_count, rel_count, word):
  out = format(counter, '6d')
  out += ' \t' + format(abs_count, '6d')
  out += ' \t' + format(rel_count, '.7f')
  out += ' \t' + str(word)
  return out

# CREATES LIST OF WORD, PAIR OR CHAR ITEMS BASED ON MODE
def create_item_list(word_list):
  if mode == PAIR:
    buff = []
    for word in word_list:
      if len(word) > 1:
        for i in range(0,len(word)-1):
          buff.append(word[i:i+2])
    return buff
  elif mode == CHAR:
    return list("".join(word_list))
  else:
    return word_list

# RETURNS THE TOTAL COUNT OF WORDS THAT SHOULD BE USED
def get_total_count(tuple_list):
  total_count = 0
  if use_global_count:
    total_count = count_by_mode(global_words)
  else:
    for item in tuple_list:
      total_count += item[1]

  return total_count

# RETURNS ITEM COUNT DEPENDING ON MODE
def count_by_mode(word_list):
  if(mode == WORD):
    count = len(word_list)
  if(mode == PAIR):
    count = 0
    for word in word_list:
      if len(word) > 1:
        count += len(word)-1
  if(mode == CHAR):
    # creates a string without separator of all words in word_list
    count = len("".join(word_list))
  return count

# CONVERTS TUPLE-LIST (word, occurence) TO TUPLE-LIST (occurence, sum(words with occ))
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

  return tuple_items

def setup_word_counter(argv):
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
  global has_output_file, file_output
  global has_stopwords, file_stopwords
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

"""
MAIN CALL TO RUN WORD_COUNT.PY
"""
if __name__ == "__main__":
  main(sys.argv[1:])

