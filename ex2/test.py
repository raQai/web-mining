from bs4 import BeautifulSoup
from html.parser import HTMLParser
from time import sleep as wait
import re
import requests
  
  
  def generate_news_url(query, num, start, recent):
    query = '+'.join(query.split())
    url = 'https://www.google.com/search?q=' + query + '&num=' + num + '&start=' + start
    url += '&tbm=nws#q=' + query + '&tbas=0&tbs=sbd:1&tbm=nws'
    if recent in ['h', 'd', 'w', 'm', 'y']:
        url += '&tbs=qdr:' + recent
    return url
  
  def search(query, num=10, start=0, sleep=True, recent=None):
        if sleep:
            wait(1)
        url = generate_url(query, str(num), str(start), recent)
        soup = BeautifulSoup(requests.get(url).text)
        results = Google.scrape_search_result(soup)
        

        raw_total_results = soup.find('div', attrs = {'class' : 'sd'}).string
        total_results = 0
        for i in raw_total_results:
            try:
                temp = int(i)
                total_results = total_results * 10 + temp
            except:
                continue

        temp = {'results' : results,
                'url' : url,
                'num' : num,
                'start' : start,
                'search_engine': 'google'
                'total_results' : total_results,
        }
        return temp
		
		
search("test")