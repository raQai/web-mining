#!/usr/bin/python

# Beispiel
#textEingabe=open('ebooks/Ten_Acres_Enough_by_Edmund_Morris.txt').read()
#textEingabe=open('stopwords/german').read()
textEingabe=open('ebooks/Die_Geschwister_Ein_Schauspiel_in_einem_Akt_by_Johann_Wolfgang_von_Goethe.txt', "r", encoding = "utf-8").read()
stopWordsDoc = ''
stopWordsDoc = open('stopwords/german').read()

def count_words(text):
  #cleaning up special characters
  for i in ["'", ",", ".", ";", ":", "?", "!", "(", ")"]:
    text = text.lower().replace(i, "")
  for i in ["-", "\n", "&"]:
    text = text.lower().replace(i, " ")

  #creating array of words
  words = text.split(" ")
  
  #removing empty words
  while True:
    if "" in words: words.remove("")
    else: break

  #storing total word count
  word_count = len(words)

  #removing stop words
  if stopWordsDoc:
    stopWords = stopWordsDoc.split("\n")
    for stopWord in stopWords:
      if stopWord in words: words.remove(stopWord)

  result = []
  distinct_words = []
  #counting words
  for word in words:
    if not word in distinct_words:
      abs_count = words.count(word)
      rel_count = float(words.count(word)) / float(word_count)
      result.append(word + " : " + str(abs_count) + " (" + str(rel_count) + "%)")
      distinct_words.append(word)

  #displaying results
  return "\n".join(sorted(result))

print(count_words(textEingabe))
#print(count_words("hallo mein ?!name ist patrick.--neben mir sitzt  christian"))
