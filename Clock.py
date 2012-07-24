#!/usr/bin/env python
# encoding: utf-8
"""
Clock.py

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


class Clock(object):
  '''
  Represents DES simulation clock
  '''
  def __init__(self):
    '''
    Constructs Clock instance
    '''
    # Initialize current simulation time to 0
    self._simulation_time = 0

  @property
  def simulation_time(self):
    '''
    Returns current simulation time
    '''
    return self._simulation_time
	
  @simulation_time.setter
  def simulation_time(self, simulation_time):
    '''
    Sets current simulation time
    
    Keyword arguments:
    time -- Next simulation time
    '''
    self._simulation_time = simulation_time
	

class ClockTests(unittest.TestCase):
  def setUp(self):
    self.c = Clock()
  
  def test_simulation_time(self):
    self.c._simulation_time = 5
    self.assertEquals(self.c._simulation_time, 5)


if __name__ == '__main__':
  unittest.main()