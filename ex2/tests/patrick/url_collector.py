#!/usr/bin/env python3.4
# coding: utf-8

'''
File    : url_collector.py
Author  : Patrick Bogdan
Contact : patrick.bgdn@gmail.com
Date    : 2015 May 10

Description : url printer
'''

import sys
import time
from collections import Counter
from threading import Thread
from urllib.request import urlopen, Request
from urllib.parse import urlparse, urljoin, urldefrag
from bs4 import BeautifulSoup

link_collection = []
unique_links = set()
visited = set()
history = set()
blocked_hosts = set()

boundary = 10
observe = True

def main( argv ):
  Thread(target=observe_history).start()
  print('-----------------------------------------')
  start = urlparse(argv[1])
  add_link(start.geturl())
  print(unique_links)
  while len(unique_links) > 0 and len(visited) < boundary:
    next_visit = unique_links.pop()
    if next_visit not in visited:
      visit_url(next_visit)

  global observe
  observe = False

  print('-----------------------------------------')
  if len(unique_links) == 0:
    print('Could not find more links. Links visited:', len(visited))
  else:
    print('Top boundary reached.')


  cnt = Counter(link_collection)
  print('Total links collected:', len(link_collection))
  print('Unique links collected:', len(cnt))
  print('Unique links collected:', len(unique_links) + len(visited))
  print('Links visited:', len(visited))
  sys.exit()

def visit_url(request_url):
  print('-----------------------------------------')
  print('[VISITING]', request_url)
  request_host = strip_www(urlparse(request_url)).netloc
  print('[HOST]', request_host)
  print('-----------------------------------------')
  while request_host in blocked_hosts:
    print('[STATUS] host recently visited. waiting...')
    time.sleep(1)
  collect_urls(request_url)
  visited.add(request_url)

def collect_urls(request_url):
  parsed = urlparse(request_url)
  
  req = Request(parsed.geturl(), headers={'User-Agent': 'Mozilla/5.0'})

  print('[STATUS] requesting file')
  with urlopen(req) as url_fs:
    host = strip_www(parsed).netloc
    history.add((time.time(), host))
    blocked_hosts.add(host)

    print('[STATUS] parsing content')
    soup = BeautifulSoup(url_fs.read())

    print('[STATUS] saving links')
    for a in soup.find_all('a'):
      if a.has_attr('href'):
        href = a['href']
        url, fragmet = urldefrag(href)
        url = strip_www(urlparse(urljoin(parsed.geturl(), url))).geturl()
        if url.endswith('/'): 
          url = url[:-1]
        add_link(url)

def add_link(url):
  unique_links.add(url)
  link_collection.append(url)

def strip_www(parsed_url):
  if parsed_url.netloc.startswith('www.'):
    parsed_url = parsed_url._replace(netloc = parsed_url.netloc[4:])
  return parsed_url

def observe_history():
  while observe:
    for host in history.copy():
      if time.time() > host[0] + 5:
        history.discard(host)
        blocked_hosts.discard(host[1])
        break


if __name__ == "__main__":
  main(sys.argv)
