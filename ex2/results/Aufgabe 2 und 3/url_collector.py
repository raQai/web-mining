#!/usr/bin/env python3.4
# coding: utf-8

'''
File    : url_collector.py
Author  : Patrick Bogdan
Contact : patrick.bgdn@gmail.com
Date    : 2015 May 10

Description : url collector
'''

import sys
import time
import threading
import shutil
import detect
from random import randint
from collections import Counter
from urllib.request import urlopen, Request
from urllib.parse import urlparse, urljoin, urldefrag
from bs4 import BeautifulSoup
from colorama import Fore, Style

BOUNDARY = 1000
VISITOR_COUNT = 2

# multi threading locks
lock_collect = threading.Lock()
lock_history = threading.Lock()

# can only be accessed with lock_collect
language_collection = []
link_collection = []
link_counter = set()
unique_links = set()
visited = set()
boundary_reached = False

# can only be accessed with lock_history
history = set()
blocked_hosts = set()


def main(argv):
  ''' main thread '''
  start_url = argv[1]
  if not '//' in start_url:
    start_url = 'http://' + start_url
  start = urlparse(start_url)
  print(start)

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


class visitorThread(threading.Thread):
  def __init__(self, name):
      super().__init__()
      self.active = True
      self.name = '[' + name + ']'

  def run(self):
    while self.active:
      with lock_collect:
        next_url = self.get_next_url()
      if next_url:
        self.visit_url(next_url)

  def get_next_url(self):
    global boundary_reached
    next_url = ''

    if boundary_reached:
      self.stop()
      print(self.name, 'Top boundary reached. Stopping process.')
    else:
      # next_url will be the last item
      # therefore setting stop flag for all visitors
      if len(visited) >= BOUNDARY-1:
        boundary_reached = True
      next_url = self.pop_random_url()
    return next_url

  def pop_random_url(self):
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
          add_link_to_history(request_url)
      print(self.name, 'host recently visited. waiting...')
      time.sleep(2)

    self.process_url(request_url)

  # TODO: change for propper task processing
  def process_url(self, request_url):
    try:
      req = Request(request_url, headers={'User-Agent': 'Mozilla/5.0'})

      print(self.name, 'requesting file')
      with urlopen(req, timeout=5) as url_fs:
        print(self.name, 'parsing content')
        soup = BeautifulSoup(url_fs.read())

        print(self.name, 'saving links')
        with lock_collect:
          for a in soup('a'):
            if a.has_attr('href'):
              href = a['href']
              if not href.endswith('.png') and not href.endswith('.jpg') and not href.endswith('.pdf') and not href.endswith('.zip'):
                add_link_to_lang_collection(detect.detect_language(soup.getText(), 30))
                add_link_to_collection(adjust_url(request_url, href))
                add_link_to_counter(adjust_url(request_url, href), len(soup('a')))
          visited.add(request_url)
    except Exception:
      print(Fore.RED + self.name, 'Exception caught, skipping', Style.RESET_ALL)
      pass

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


# TODO: adapt to excercise with different sets
def add_link_to_collection(url):
  unique_links.add(strip_www(url))
  link_collection.append(strip_www(url))


def add_link_to_counter(url, count):
  link_counter.add((strip_www(url), count))


def add_link_to_lang_collection(lang):
  language_collection.append(lang)
  

def add_link_to_history(url):
  host = urlparse(url).netloc
  seconds = randint(5, 10)
  release = time.time() + seconds
  print('[ HISTORY ] added', host, 'for', seconds, 'seconds')
  history.add((release, host))
  blocked_hosts.add(host)


''' general url adjustment procedures '''
def adjust_url(base_url, url):
  url, fragmet = urldefrag(url)
  url = urljoin(base_url, url)
  if url.endswith('/'):
    url = url[:-1]
  return url


def strip_www(url):
  parsed_url = urlparse(url)
  if parsed_url.netloc.startswith('www.'):
    parsed_url = parsed_url._replace(netloc = parsed_url.netloc[4:])
  return parsed_url.geturl()


''' printing results '''
# TODO: adapt to excercise with different sets
def print_results():
  cnt = Counter(link_collection).most_common()
  print('Total links collected:', len(link_collection))
  print('Unique links collected (Counter):', len(cnt))
  print('Links visited:', len(visited))
  with open('links_collection.txt', 'w') as collection_fs:
    for link, count in cnt:
      out = format(count, '10d')
      out += ' \t' + link
      collection_fs.write(out + '\n')
  print('links_collection.txt written')
  with open('links_counter_per_page.txt', 'w') as counter_fs:
    for link, count in link_counter:
      out = format(count, '10d')
      out += ' \t' + link
      counter_fs.write(out + '\n')
  print('links_counter_per_page.txt written')
  cnt = Counter(language_collection).most_common()
  with open('language_collection.txt', 'w') as collection_fs:
    for lang, count in cnt:
      out = format(count, '10d')
      out += ' \t' + lang
      collection_fs.write(out + '\n')
  print('language_collection.txt written')
    
  

if __name__ == "__main__":
  main(sys.argv)
