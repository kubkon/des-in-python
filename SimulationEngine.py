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
  Represents the main engine of a DES simulation platform
  '''
  def __init__(self):
    '''
    Constructs SimulationEngine instance
    '''
    # Create empty event list
    self.event_list = []
    # Create clock
    self.clock = Clock()
    # Flag representing finishing event
    self.finish_event_exists = False
  
  def start(self):
    '''
    Starts simulation
    '''
    while len(self.event_list) != 0:
      # Remove the imminent event from the event list
      first = self.event_list.pop()
      # Advance clock to the next event
      if len(self.event_list) > 1:
        self.clock.simulation_time = self.event_list[-1].time
      # Execute the imminent event
      first.trigger_action()
  
  def stop(self, finish_time):
    '''
    Schedules finishing event
    
    Keyword arguments:
    finish_time -- Time of occurrence of the finishing event
    '''
    # Check if finishing event already scheduled
    if not self.finish_event_exists:
      # Remove any scheduled event with time of occurrence
      # exceeding the time of occurrence of the finishing
      # event
      removed = filter(lambda e: e.time > finish_time, self.event_list)
      if len(removed) > 0:
        self.event_list = [e for e in self.event_list if e not in removed]
      # Add finishing event
      self.event_list += [Event(finish_time)]
      self.finish_event_exists = True
      # Sort the list so that finishing event is first (LIFO)
      self.event_list.sort(key=lambda x: x.time)
      self.event_list.reverse()
  
  def schedule(self, event):
    '''
    Schedules event (adds it to the event list)
    
    Keyword arguments:
    event -- Event to be scheduled
    '''
    self.event_list += [event]
  

class SimulationEngineTests(unittest.TestCase):
  def setUp(self):
    # Create new simulation
    self.sim = SimulationEngine()
  
  def test_simulation(self):
    # Schedule some events
    self.sim.schedule(Event(20))
    self.sim.schedule(Event(10))
    self.sim.schedule(Event(150))
    # Schedule finishing event
    self.sim.stop(100)
    # Start simulating
    self.sim.start()


if __name__ == '__main__':
  unittest.main()