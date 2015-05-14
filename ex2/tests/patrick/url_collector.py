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
import threading
from random import randint
from collections import Counter
from urllib.request import urlopen, Request
from urllib.parse import urlparse, urljoin, urldefrag
from bs4 import BeautifulSoup

BOUNDARY = 5
VISITOR_COUNT = 2

# multi threading locks
lock_collect = threading.Lock()
lock_history = threading.Lock()

# can only be accessed with lock_collect
link_collection = []
unique_links = set()
visited = set()

# can only be accessed with lock_history
history = set()
blocked_hosts = set()


observe = True


def main(argv):
  ''' main thread '''
  start = urlparse(argv[1])
  add_link_to_collection(start.geturl())

  history_observer = historyObserver()
  history_observer.start()

  threads = []
  for i in range(VISITOR_COUNT):
    thread = visitorThread('VISITOR ' + str(i))
    thread.start()
    threads.append(thread)
  for t in threads:
    t.join()

  # stopping the history observer before ending main
  history_observer.stop()

  print_results()

  sys.exit()


def add_link_to_collection(url):
  unique_links.add(strip_www(url))
  link_collection.append(strip_www(url))


def add_link_to_history(url):
  with lock_history:
    host = urlparse(url).netloc
    release = time.time() + randint(4,8)
    print('[ HISTORY ] added', host)
    history.add((release, host))
    blocked_hosts.add(host)


def strip_www(url):
  parsed_url = urlparse(url)
  if parsed_url.netloc.startswith('www.'):
    parsed_url = parsed_url._replace(netloc = parsed_url.netloc[4:])
  return parsed_url.geturl()


def print_results():
  cnt = Counter(link_collection)
  print('Total links collected:', len(link_collection))
  print('Unique links collected (Counter):', len(cnt))
  print('Unique links collected (Sets):', len(unique_links) + len(visited))
  print('Links visited:', len(visited))


class visitorThread(threading.Thread):
  def __init__(self, name):
      super().__init__()
      self.active = True
      self.name = '[' + name + ']'

  def run(self):
    while self.active:
      next_url = ''
      with lock_collect:
        if len(visited) >= BOUNDARY:
          self.stop()
          print(self.name, 'Top boundary reached. Stopping process.')
        else:
          next_url = self.get_next_url()
      if next_url:
        self.visit_url(next_url)

  def get_next_url(self):
    url = ''
    if len(unique_links) >= 1:
      next_url = unique_links.pop()
      if next_url not in visited:
        url = next_url
    return url

  def visit_url(self, request_url):
    print(self.name, 'visiting ', request_url)
    request_host = urlparse(request_url).netloc
    print(self.name, 'checking host', request_host)
    host_blocked = True
    while host_blocked:
      with lock_history:
        if request_host not in blocked_hosts:
          host_blocked = False
      print(self.name, 'host recently visited. waiting...')
      time.sleep(2)

    self.process_url(request_url)

  def process_url(self, request_url):
    # TODO: randomize agent
    req = Request(request_url, headers={'User-Agent': 'Mozilla/5.0'})

    print(self.name, 'requesting file')
    with urlopen(req) as url_fs:
      add_link_to_history(request_url)

      print(self.name, 'parsing content')
      soup = BeautifulSoup(url_fs.read())

      print(self.name, 'saving links')
      with lock_collect:
        for a in soup.find_all('a'):
          if a.has_attr('href'):
            # TODO: filter images
            href = a['href']
            add_link_to_collection(self.clean_url(request_url, href))
        visited.add(request_url)

  def clean_url(self, base_url, url):
    url, fragmet = urldefrag(url)
    url = urljoin(base_url, url)
    if url.endswith('/'):
      url = url[:-1]
    return url

  def stop(self):
    ''' stopping the visior thread '''
    self.active = False


class historyObserver(threading.Thread):
  def __init__(self):
    super().__init__()
    self.active = True

  def run(self):
    while self.active:
      with lock_history:
        for host in history.copy():
          if time.time() >= host[0]:
            print('[ HISTORY ] discarding', host[1]) 
            history.discard(host)
            blocked_hosts.discard(host[1])

  def stop(self):
    ''' stopping the visior thread '''
    self.active = False


if __name__ == "__main__":
  main(sys.argv)
