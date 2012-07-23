#!/usr/bin/env python
# encoding: utf-8
"""
EventList.py

Created by Jakub Konka on 2012-07-23.
Copyright (c) 2012 Jakub Konka. All rights reserved.

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

from Event import *


class EventList:
  '''
  Represents future event list (FEL)
  '''
  def __init__(self):
    '''
    Constructs EventList instance
    '''
    # Create empty FIFO list
    self.fifo = []
	
  def add(self, event):
    '''
    Adds event to the end of the list
    '''
    self.fifo.append(event)
  
  def get(self, index):
    '''
    Returns event at index
    '''
    return self.fifo[index]
  
  def pop(self):
    '''
    Pops event from the beginning of the list
    '''
    return self.fifo.pop(0)


class EventListTests(unittest.TestCase):
	def setUp(self):
		self.fel = EventList()
	
	def test_add(self):
	  e = Event(1)
	  self.fel.add(e)
	  self.assertEquals(self.fel.get(0), e)
	
	def test_pop(self):
	  e = Event(1)
	  self.fel.add(e)
	  self.assertEquals(self.fel.pop(), e)


if __name__ == '__main__':
	unittest.main()