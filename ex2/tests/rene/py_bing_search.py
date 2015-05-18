import urllib
import requests
import pdb
import time
import sys

class PyBingException(Exception):
	pass

class PyBingSearch(object):

	#QUERY_URL = 'https://api.datamarket.azure.com/Bing/Search/v1/Composite' \
	#			 + '?Sources={}&Query={}&$top={}&$format={}'
	QUERY_URL = 'https://api.datamarket.azure.com/Bing/SearchWeb/v1/Web' \
				+ '?Query={}&$top={}&$skip={}&$format={}&Market=%27de-DE%27'

	def reset(self):
		self.list = []

	def write(self, output = open("out.txt", 'w')):
		for x in self.list:
			output.write(x + "\n")
	
	def __init__(self, api_key = 'DB4KVfjMIsUrQm9H9gwQzJJvs9zKacXjP5D9Og79huI', only_german = True, safe=False):
		self.api_key = api_key
		self.safe = safe
		self.list = []
		self.german = only_german
		
	def set_none(self):
		self.german = False
		
	def set_german(self):
		self.german = True
	
	def search(self, query, limit=50, offset=0, format='json'):
		return self._search(query, limit, offset, format)

	def search_all(self, query, limit=50, format='json'):
		counter = 0
		results, next_uri = self._search(query, limit, 0, format)
		counter += len(results)
		for x in results:
			if hasattr(x, 'url'):
				if not x.url in self.list:
					self.list.append(x.url)
	
		finished = False
		nothing_counter = 0
		while counter < limit and not finished:
			print("searching for", query, "with top=50, skip=" + str(counter))
			before = len(self.list)
			max = limit - len(results)
			more_results, uri = self._search(query, 50, counter, format)
			counter += len(more_results)
			next_uri = uri
			results += more_results
			for x in more_results:
				if hasattr(x, 'url'):
					if not x.url in self.list:
						self.list.append(x.url)
						
			after = len(self.list)
			if before == after:
				nothing_counter += 1
			else:
				nothing_counter = 0
			print("\tresults:" , counter, " of limit:", limit, "links-before:", before, "links-after:", after)
			
			if nothing_counter == 3:
				finished = True
			if counter > limit - 1:
				finished = True
			time.sleep(1)
			
	
		print("-----------------------")
		print("total search results:\t", counter)
		print("unique links:\t\t", len(self.list))
		return "Search done"

	def _search(self, query, limit, offset, format):
		'''
		Returns a list of result objects, with the url for the next page bing search url.
		'''
		if self.german:
			query += " language:de"
		url = self.QUERY_URL.format(urllib.parse.quote("'{}'".format(query + " language:de")), limit, offset, format)

		r = requests.get(url, auth=("", self.api_key))
		try:
			json_results = r.json()
		except ValueError as vE:
			if not self.safe:
				raise PyBingException("Request returned with code %s, error msg: %s" % (r.status_code, r.text))
			else:
				print("[ERROR] Request returned with code %s, error msg: %s. \nContinuing in 5 seconds." % (r.status_code, r.text))
				time.sleep(5)
		try:
			next_link = json_results['d']['__next']
		except KeyError as kE:
			print("Couldn't extract next_link: KeyError: %s" % kE)
			next_link = ''

		return [Result(single_result_json) for single_result_json in json_results['d']['results']], next_link
		
	def dump(obj, nested_level=0, output=open("test2.txt", 'w')):
		spacing = ' '
		if type(obj) == dict:
			print('%s{' % ((nested_level) * spacing), file=output)
			for k, v in obj.items():
				if hasattr(v, '__iter__'):
					print('%s%s:' % ((nested_level + 1) * spacing, k), file=output)
					dump(v, nested_level + 1, output)
				else:
					print('%s%s: %s' % ((nested_level + 1) * spacing, k, v), file=output)
			print('%s}' % (nested_level * spacing), file=output)
		elif type(obj) == list:
			print('%s[' % ((nested_level) * spacing), file=output)
			for v in obj:
				if hasattr(v, '__iter__'):
					dump(v, nested_level + 1, output)
				else:
					print('%s%s' % ((nested_level + 1) * spacing, v), file=output)
			print('%s]' % ((nested_level) * spacing), file=output)
		else:
			print('%s%s' % ((nested_level) * spacing), obj, file=output)
			

class Result(object):
	'''
	The class represents a SINGLE search result.
	Each result will come with the following:

	#For the actual results#
	title: title of the result
	url: the url of the result
	description: description for the result
	id: bing id for the page

	#Meta info#:
	meta.uri: the search uri for bing
	meta.type: for the most part WebResult
	'''

	class _Meta(object):
		'''
		Holds the meta info for the result.
		'''
		def __init__(self, meta):
			self.type = meta['type']
			self.uri = meta['uri']

	def __init__(self, result):
		self.url = result['Url']
		self.title = result['Title']
		self.description = result['Description']
		self.id = result['ID']

		self.meta = self._Meta(result['__metadata'])

	
