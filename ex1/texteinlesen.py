#!/usr/bin/python

# Beispiel
#textEingabe=open('ebooks/Ten_Acres_Enough_by_Edmund_Morris.txt').read()
#textEingabe=open('stopwords/german').read()
textEingabe=open('ebooks/Die_Geschwister_Ein_Schauspiel_in_einem_Akt_by_Johann_Wolfgang_von_Goethe.txt').read()

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

  result = []
  distinct_words = []
  #counting words
  for word in words:
    if not word in distinct_words:
      result.append(word + " : " + str(words.count(word)) + " (" + str(float(words.count(word)) / float(len(words))) + "%)")
      distinct_words.append(word)

  #displaying results
  return "\n".join(sorted(result))

print(count_words("hallo mein ?!name ist patrick.--neben mir sitzt  christian"))
