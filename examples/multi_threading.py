#!/usr/bin/env python3.4
# coding: utf-8

'''
File    : multi_threading.py
Author  : Patrick Bogdan
Contact : patrick.bgdn@gmail.com
Date    : 2015 May 12

Description : multi threading test
'''

import sys
import time
import threading
from random import randint, uniform

blocker_lock = threading.Lock()
blocker = set()

numbers_lock = threading.Lock()
numbers = []

boundary = 10
worker_count = 3

class workerThread(threading.Thread):
  def __init__(self, number):
    ''' initializing thread with a name '''
    super().__init__()
    self.name = "[Thread_" + str(number) + "]"
    print(self.name, "__init__")
    self._active = True

  def run(self):
    ''' searching for randint in blocker. if randint is in blocker, waiting for observer '''
    while self._active:
      print(self.name, "waiting for blocker")
      with blocker_lock:
        print(self.name, "lock on blocker")
        time.sleep(uniform(0,1))
        print(self.name, blocker)
        number = randint(0,boundary)
        if len(blocker) == 0:
          print(self.name, "blocker empty, stopping thread")
          self.stop()
        elif number not in blocker:
          print(self.name, "waiting for numbers")
          with numbers_lock:
            print(self.name, "lock on numbers")
            if len(numbers) >= worker_count * boundary:
              self.stop()
            else:
              numbers.append(number)
              print(self.name, "added", number)

  def stop(self):
    ''' stopping the thread '''
    print(self.name, "stopped")
    self._active = False

class observerThread(threading.Thread):
  '''
    observing the blocker and popping an element every <self.sleep> seconds
     '''
  def __init__(self, seconds):
    ''' initializing thread with sleep timer '''
    super().__init__()
    self.sleep = seconds
    self.name = "[Observer]"
    print(self.name, "__init__")
    self._active = True

  def run(self):
    ''' running the pop method and locking blocker '''
    while self._active:
      time.sleep(self.sleep)
      print(self.name, "waiting for blocker")
      with blocker_lock:
        print(self.name, "lock on blocker")
        if len(blocker):
          elem = blocker.pop()
          print(self.name, "popped", elem)
        else:
          self.stop()

  def stop(self):
    ''' stopping the thread '''
    print(self.name, "stopped")
    self._active = False

def main( argv ):
  '''
    main calling the threads
     '''
  l = []
  l.extend(range(0,boundary))
  global blocker
  blocker = set(l)
  print(blocker)
  print("==============================")

  threads = []

  observer = observerThread(1)
  observer.start()
  threads.append(observer)

  for i in range(1, worker_count+1):
    thread = workerThread(i)
    thread.start()
    threads.append(thread)

  print(threads)
  for t in threads:
    t.join()

  print(threads)
  print("==============================")
  print("process finished")
  print(numbers)


if __name__ == "__main__":
  main(sys.argv)
