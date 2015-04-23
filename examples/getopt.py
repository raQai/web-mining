#!/usr/bin/python

import sys, getopt

def main(argv):
  inputfile = ''
  stopwords = ''
  comparable = ''

  try:
    opts, args = getopt.getopt(argv,"hi:s:c:",["ifile=","sfile=","cfile="])
  except getopt.GetoptError:
    print 'getopt.py -i <inputfile> -s <stopwords> -c <comparablefile>'
    sys.exit(2)

  for opt, arg in opts:
    if opt == '-h':
      print 'getopt.py -i <inputfile> -s <stopwords> -c <comparablefile>'
      sys.exit()
    elif opt in ("-i", "--ifile"):
      inputfile = arg
    elif opt in ("-s", "--sfile"):
      stopwords = arg
    elif opt in ("-c", "--cfile"):
      comparable = arg

  print 'Input file: ', inputfile
  print 'Stopword file: ', stopwords
  print 'Comparable file: ', comparable

if __name__ == "__main__":
  main(sys.argv[1:])
