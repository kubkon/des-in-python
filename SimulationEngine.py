#!/usr/bin/env python
# encoding: utf-8
"""
SimulationEngine.py

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

from Clock import *
from EventList import *


class SimulationEngine:
  '''
  Represents the main engine of a DES simulation
  platform
  '''
	def __init__(self):
		'''
		Constructs SimulationEngine instance
		'''
		# Create empty event list
		self.event_list = EventList()
		# Create clock
		self.clock = Clock()
	
	def add_events(self, events):
	  '''
	  Populates event list
	  '''
	  for e in events:
  	  self.event_list.add(e)
  
  def start(self, duration):
    '''
    Starts simulation
    '''


class SimulationEngineTests(unittest.TestCase):
	def setUp(self):
		pass


if __name__ == '__main__':
	unittest.main()