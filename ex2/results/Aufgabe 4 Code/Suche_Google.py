# Get the first 20 hits for: "Breaking Code" WordPress blog
from google import search
output = open("out-google.txt", 'w')
for url in search('"Breaking Code"',lang='de', stop=500):
	print(url)
	output.write(url + "\n")