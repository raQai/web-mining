#!/usr/bin/python

textEingabe=open('ebooks/Die_Geschwister_Ein_Schauspiel_in_einem_Akt_by_Johann_Wolfgang_von_Goethe.txt', "r")  #.read() liest ganzen text
print(textEingabe)
textEingabe.close()

# textAusgabe=open("ausgeben.txt","w")

# textAusgabe.close()

# W�rter auftrennen 
# textEingabe.split(" ")

# Durchgehen
# for wort in textEingabe:
	# if wort


# Beispiel


# print(count_words("""Fischers Fritz fischt frische Fische, frische Fische fischt Fischers Fritz.
# eins; zwei, zwei; drei, drei, drei."""))

# def count_words(text):
    # """gibt aus, wie oft jedes Wort im String 'text' vorkommt"""
    # for i in ["'", ",", ".", ";", ":", "?", "!", "(", ")"]:
        # text = text.lower().replace(i, "")
    # text = text.replace("\n", " ")
    # words = text.split(" ")
    # while True:
        # if "" in words: words.remove("")
        # else: break
    # result = []
    # counted_words = []
    # for i in words:
        # if not i in counted_words:
            # result.append(i+" : "+str(words.count(i)))
            # counted_words.append(i)
    # return "\n".join(result)
 
