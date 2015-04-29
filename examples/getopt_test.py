#!/usr/bin/python

import sys, getopt

def main(argv):
  inputfile = ''
  anymode = False

  try:
    opts, args = getopt.getopt(argv,"hi:a",["ifile=","any"])
  except getopt.GetoptError:
    print 'getopt.py -i <inputfile> -a'
    sys.exit(2)

  for opt, arg in opts:
    if opt == '-h':
      print 'getopt.py -i <inputfile> -a'
      sys.exit()
    elif opt in ("-i", "--ifile"):
      inputfile = arg
    elif opt in ("-a", "--any"):
      anymode = True

  if anymode:
    print 'anymote on'

  print 'Input file: ', inputfile

if __name__ == "__main__":
  main(sys.argv[1:])
