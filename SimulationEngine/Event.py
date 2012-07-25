#!/usr/bin/env python
# encoding: utf-8
"""
Event.py

Created by Jakub Konka on 2012-07-23.
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


class Event(object):
  '''
  Represents an abstract event
  '''
  def __init__(self, identifier, time):
    '''
    Constructs Event instance
    
    Keyword arguments:
    identifier -- ID/type of this event
    time -- Time of occurring of this event
    '''
    self._identifier = identifier
    self._time = time
  
  @property
  def identifier(self):
    '''
    Returns id of this event
    '''
    return self._identifier
  
  @property
  def time(self):
    '''
    Returns time of occurring
    '''
    return self._time
  

class EventTests(unittest.TestCase):
  def setUp(self):
    self.e = Event("Arrival", 10)
  
  def test_properties(self):
    self.assertEquals(self.e.identifier, "Arrival")
    self.assertEquals(self.e.time, 10)
  

if __name__ == '__main__':
  unittest.main()