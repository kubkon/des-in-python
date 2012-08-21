#!/usr/bin/env python
# encoding: utf-8
"""
PRNG.py

Created by Jakub Konka on 2012-08-21.
Copyright (c) 2012 Jakub Konka.

This library is free software; you can redistribute it and/or
modify under the terms of the GNU General Public License as
published by the Free Software Foundation; version 3.0.
This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this library; if not, visit
http://www.gnu.org/licenses/gpl-3.0.html
"""

import sys
import os
import unittest
import datetime
import time
import random


class PRNG(object):
  '''
  Represents default PRNG (currently, wrapper class for random module)
  '''
  
  def __init__(self):
    '''
    Constructs PRNG instance
    '''
    # Default seed value to current datetime
    self._seed = int(time.mktime(datetime.datetime.now().timetuple()))
    # Initialize PRNG with the default seed value
    random.seed(self._seed)
  
  @property
  def seed(self):
    '''
    Returns current seed value
    '''
    return self._seed
  
  @seed.setter
  def seed(self, seed):
    '''
    Sets new seed value
    
    Keyword arguments:
    seed -- New seed value
    '''
    self._seed = seed
    # Re-initialize PRNG with new seed value
    random.seed(self._seed)
  
  def randint(self, a, b):
    '''
    Returns a random integer N such that a <= N <= b
    
    Keyword arguments:
    a -- Lower bound
    b -- Upper bound
    '''
    return random.randint(a, b)
  
  def uniform(self, a, b):
    '''
    Returns a random floating point number N such that
    a <= N <= b for a <= b and b <= N <= a for b < a
    
    Keyword arguments:
    a -- Lower bound
    b -- Upper bound
    '''
    return random.uniform(a, b)
  
  def expovariate(self, lambd):
    '''
    Returns a random floating point number N drawn
    from an exponential distribution with parameter lambd (1 / E[X])
    
    Keyword arguments:
    lambd -- Lambda parameter of exponential distribution (1 / E[X])
    '''
    return random.expovariate(lambd)

class PRNGTests(unittest.TestCase):
  def setUp(self):
    pass
  

if __name__ == '__main__':
  unittest.main()