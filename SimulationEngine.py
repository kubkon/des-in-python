#!/usr/bin/env python
# encoding: utf-8
"""
SimulationEngine.py

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

from Clock import *
from Event import *


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
    self.event_list = []
    # Create clock
    self.clock = Clock()
  
  def start(self):
    '''
    Starts simulation
    '''
    while len(self.event_list) != 0:
      # Remove the imminent event from the event list
      first = self.event_list.pop(0)
      # Advance clock to the next event
      if len(self.event_list) > 1:
        self.clock.simulation_time = self.event_list[0].time
      # Execute the imminent event
      first.trigger_action()
  


class SimulationEngineTests(unittest.TestCase):
  def setUp(self):
    # Create new simulation
    self.sim = SimulationEngine()
  
  def test_start(self):
    # Create a set of deterministic events
    self.sim.event_list = [Event(1), Event(2), Event(5), Event(9)]
    # Start simulating
    self.sim.start()


if __name__ == '__main__':
  unittest.main()